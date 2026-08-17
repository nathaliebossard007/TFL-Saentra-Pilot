import json, math, hashlib, csv, argparse
from pathlib import Path
from dataclasses import dataclass
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def angle_wrap(x): return (x + np.pi) % (2*np.pi) - np.pi

def sensor_layout(n):
    # deterministic perimeter/interior geometry, independent of experiment seed
    rng=np.random.default_rng(7001)
    pts=[]
    for i in range(n):
        if i < 12:
            side=i%4; q=(i//4+1)/4
            if side==0: x,y=500+9000*q,500
            elif side==1: x,y=9500,500+9000*q
            elif side==2: x,y=9500-9000*q,9500
            else: x,y=500,9500-9000*q
        else:
            x,y=rng.uniform(1200,8800,2)
        pts.append(np.array([x,y,20.0]))
    return pts

def truth_at(t):
    # two constant-velocity 3D tracks crossing near center around t=60
    p0=np.array([1700+55*t, 5000+0*t, 700+0.25*t])
    p1=np.array([5000+0*t, 8300-55*t, 760-0.20*t])
    v0=np.array([55.,0.,0.25]); v1=np.array([0.,-55.,-0.20])
    return [(0,p0,v0),(1,p1,v1)]

def observe(cfg, seed):
    rng=np.random.default_rng(seed); sensors=sensor_layout(cfg['sensor_count'])
    obs=[]; eval_map={}; oid=0
    for k in range(int(cfg['duration_s']/cfg['dt_s'])+1):
        t=k*cfg['dt_s']
        for gt_id,p,v in truth_at(t):
            if gt_id==cfg['occlusion']['object'] and cfg['occlusion']['start_s']<=t<=cfg['occlusion']['end_s']:
                continue
            visible=[]
            for sid,s in enumerate(sensors):
                d=p-s; r=float(np.linalg.norm(d))
                if r<=cfg['sensor_range_m'] and rng.random()>=cfg['miss_probability']:
                    visible.append((sid,s,d,r))
            if not visible: continue
            sid,s,d,r=visible[int(rng.integers(0,len(visible)))]
            b=math.atan2(d[1],d[0]); e=math.atan2(d[2], math.hypot(d[0],d[1]))
            bn=b+rng.normal(0,math.radians(cfg['bearing_sigma_deg']))
            en=e+rng.normal(0,math.radians(cfg['elevation_sigma_deg']))
            rn=max(1.,r+rng.normal(0,cfg['range_sigma_m']))
            q=np.array([math.cos(en)*math.cos(bn), math.cos(en)*math.sin(bn), math.sin(en)])
            xyz=s+rn*q
            rec={"observation_id":oid,"sensor_id":sid,"timestamp":t,"sensor_position_xyz":s.tolist(),
                 "bearing":bn,"elevation":en,"range_estimate":rn,"range_uncertainty":cfg['range_sigma_m'],
                 "position_estimate_xyz":xyz.tolist()}
            obs.append(rec); eval_map[oid]=gt_id; oid+=1
        if rng.random()<cfg['false_detection_rate_per_sensor_frame']*cfg['sensor_count']:
            sid=int(rng.integers(0,len(sensors))); s=sensors[sid]
            b=rng.uniform(-np.pi,np.pi); e=rng.uniform(0.03,0.3); r=rng.uniform(800,cfg['sensor_range_m'])
            q=np.array([math.cos(e)*math.cos(b),math.cos(e)*math.sin(b),math.sin(e)]); xyz=s+r*q
            obs.append({"observation_id":oid,"sensor_id":sid,"timestamp":t,"sensor_position_xyz":s.tolist(),"bearing":b,"elevation":e,
                        "range_estimate":r,"range_uncertainty":cfg['range_sigma_m'],"position_estimate_xyz":xyz.tolist()}); eval_map[oid]=-1; oid+=1
    return obs, eval_map

@dataclass
class KF:
    x: np.ndarray
    P: np.ndarray
    ids: list

def kf_mats(dt, qa):
    F=np.eye(6); F[0,3]=F[1,4]=F[2,5]=dt
    G=np.zeros((6,3)); G[:3,:]=.5*dt*dt*np.eye(3); G[3:,:]=dt*np.eye(3)
    Q=(qa**2)*(G@G.T); H=np.zeros((3,6)); H[:3,:3]=np.eye(3)
    return F,Q,H

def baseline(cfg, obs):
    by_t={}
    for o in obs: by_t.setdefault(o['timestamp'],[]).append(o)
    tracks=[]; R=(cfg['range_sigma_m']**2+60**2)*np.eye(3); last_t=None
    for t in sorted(by_t):
        dt=cfg['dt_s'] if last_t is None else t-last_t; last_t=t
        F,Q,H=kf_mats(dt,cfg['baseline']['process_accel_sigma'])
        for tr in tracks: tr.x=F@tr.x; tr.P=F@tr.P@F.T+Q
        items=by_t[t]; candidates=[]
        for ti,tr in enumerate(tracks):
            S=H@tr.P@H.T+R; Si=np.linalg.inv(S)
            for oi,o in enumerate(items):
                y=np.array(o['position_estimate_xyz'])-H@tr.x; d2=float(y@Si@y)
                if d2<=cfg['baseline']['gate_mahalanobis2']: candidates.append((d2,ti,oi,y,S))
        used_t=set(); used_o=set()
        for d2,ti,oi,y,S in sorted(candidates):
            if ti in used_t or oi in used_o: continue
            tr=tracks[ti]; K=tr.P@H.T@np.linalg.inv(S); tr.x=tr.x+K@y; tr.P=(np.eye(6)-K@H)@tr.P; tr.ids.append(items[oi]['observation_id']); used_t.add(ti); used_o.add(oi)
        for oi,o in enumerate(items):
            if oi in used_o: continue
            z=np.array(o['position_estimate_xyz']); x=np.r_[z,[0.,0.,0.]]; P=np.diag([120**2]*3+[70**2]*3)
            tracks.append(KF(x,P,[o['observation_id']]))
    return [tr.ids for tr in tracks if len(tr.ids)>=3]

def edge_weight(a,b,cfg):
    dt=b['timestamp']-a['timestamp']
    if dt<=0 or dt>cfg['ric']['max_dt_s']: return 0.0
    pa=np.array(a['position_estimate_xyz']); pb=np.array(b['position_estimate_xyz']); dv=pb-pa; speed=np.linalg.norm(dv)/dt
    if speed>cfg['ric']['max_speed_mps']: return 0.0
    # spatial plausibility favors plausible displacement but does not encode identity
    expected=55*dt; resid=abs(np.linalg.norm(dv)-expected)
    w_sp=math.exp(-0.5*(resid/cfg['ric']['sigma_spatial_m'])**2)
    # uncertainty penalty explicit
    unc=(a['range_uncertainty']+b['range_uncertainty'])/2
    w_unc=1/(1+unc/100)
    return w_sp*w_unc

def ric_paths(cfg, obs):
    # DAG of relational compatibility. Extract best paths greedily; no labels used.
    O=sorted(obs,key=lambda o:(o['timestamp'],o['observation_id'])); n=len(O)
    incoming=[[] for _ in range(n)]; edges=[]
    for j in range(n):
        for i in range(max(0,j-140),j):
            w=edge_weight(O[i],O[j],cfg)
            if w>=cfg['ric']['min_edge_weight']:
                incoming[j].append((i,w)); edges.append((i,j,w))
    remaining=set(range(n)); paths=[]
    for _ in range(12):
        score=np.full(n,-1e9); prev=np.full(n,-1,dtype=int)
        for j in range(n):
            if j not in remaining: continue
            score[j]=0.0
            for i,w in incoming[j]:
                if i in remaining and score[i]>-1e8:
                    s=score[i]+math.log(max(w,1e-9))+1.4
                    if s>score[j]: score[j]=s; prev[j]=i
        end=int(np.argmax(score))
        if score[end]<4: break
        path=[]; cur=end
        while cur>=0 and cur in remaining:
            path.append(cur); cur=int(prev[cur])
        path=path[::-1]
        if len(path)<3: break
        ids=[O[i]['observation_id'] for i in path]; paths.append(ids)
        for i in path: remaining.discard(i)
    # spectral diagnostics on full undirected compatibility graph
    deg=np.zeros(n); A=np.zeros((n,n),dtype=float)
    for i,j,w in edges: A[i,j]=A[j,i]=max(A[i,j],w); deg[i]+=w; deg[j]+=w
    idx=np.where(deg>0)[0]
    diag={"n_vertices":n,"n_edges":len(edges),"edge_node_ratio":len(edges)/max(n,1)}
    if len(idx)>=2:
        As=A[np.ix_(idx,idx)]; ds=As.sum(1); inv=np.diag(1/np.sqrt(np.maximum(ds,1e-12))); L=np.eye(len(idx))-inv@As@inv
        ev=np.linalg.eigvalsh(L); diag.update({"lambda_q25":float(np.quantile(ev,.25)),"lambda_q50":float(np.quantile(ev,.5)),"lambda_q75":float(np.quantile(ev,.75)),"spectral_gap":float(ev[1]-ev[0]) if len(ev)>1 else 0.0})
    return paths,diag

def metrics(tracks, eval_map, obs, cfg):
    pur=[]; switches=0; false_merges=0; correct=0; total=0; by_gt={0:set(),1:set()}
    for ti,tr in enumerate(tracks):
        labs=[eval_map[i] for i in tr if eval_map[i]>=0]; total+=len(tr)
        if not labs: continue
        vals,counts=np.unique(labs,return_counts=True); maj=int(vals[np.argmax(counts)]); m=int(max(counts)); pur.append(m/len(labs)); correct+=m
        if len(set(labs))>1: false_merges+=1
        switches+=sum(a!=b for a,b in zip(labs,labs[1:]))
        for g in set(labs): by_gt[g].add(ti)
    frag=sum(max(0,len(v)-1) for v in by_gt.values())
    id_to_t={o["observation_id"]:o["timestamp"] for o in obs}
    recalls=[]
    for g in [0,1]:
        gt_ids={i for i,v in eval_map.items() if v==g}
        best=max((len(gt_ids.intersection(set(tr))) for tr in tracks), default=0)
        recalls.append(best/max(len(gt_ids),1))
    false_tracks=sum(1 for tr in tracks if sum(1 for i in tr if eval_map[i]<0) >= max(2, int(0.5*len(tr))))
    # Recovery: for occluded object, same inferred track must bridge last pre-gap and first post-gap observations.
    g=cfg["occlusion"]["object"]; pre=[i for i,v in eval_map.items() if v==g and id_to_t[i]<cfg["occlusion"]["start_s"]]
    post=[i for i,v in eval_map.items() if v==g and id_to_t[i]>cfg["occlusion"]["end_s"]]
    recovery=float("nan")
    if pre and post:
        last_pre=max(pre,key=id_to_t.get)
        containing=[set(tr) for tr in tracks if last_pre in tr]
        if containing:
            later=[id_to_t[i]-cfg["occlusion"]["end_s"] for i in post if any(i in tr for tr in containing)]
            if later: recovery=min(later)
    return {"track_count":len(tracks),"track_purity":float(np.mean(pur)) if pur else 0.,"identity_switches":switches,"fragmentation":frag,
            "false_merge_rate":false_merges/max(len(tracks),1),"track_precision":correct/max(total,1),
            "track_recall":float(np.mean(recalls)),"false_track_rate":false_tracks/max(len(tracks),1),"recovery_time_s":recovery}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',default=str(ROOT/'config/tfl_uas_001a_v1.json')); args=ap.parse_args()
    cfg=json.load(open(args.config)); cfg_hash=hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()
    outdir=ROOT/'results'; outdir.mkdir(exist_ok=True)
    rows=[]
    for seed in cfg['seeds']:
        obs,emap=observe(cfg,seed)
        # write observations without labels; ground truth mapping separately
        json.dump(obs,open(outdir/f'obs_seed_{seed}.json','w'))
        json.dump(emap,open(outdir/f'ground_truth_eval_seed_{seed}.json','w'))
        b=baseline(cfg,obs); r,diag=ric_paths(cfg,obs)
        for alg,tr in [('baseline_kf_nn',b),('ric_graph_v0',r)]:
            m=metrics(tr,emap,obs,cfg); row={"experiment_id":cfg['experiment_id'],"code_version":cfg['code_version'],"configuration_hash":cfg_hash,"random_seed":seed,"scenario_family":"S3+S4","algorithm":alg,**m}
            if alg=='ric_graph_v0': row.update(diag)
            rows.append(row)
            json.dump(tr,open(outdir/f'tracks_{alg}_seed_{seed}.json','w'))
    cols=sorted(set().union(*(r.keys() for r in rows)))
    with open(outdir/'summary.csv','w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
    json.dump(rows,open(outdir/'summary.json','w'),indent=2)
    for alg in ['baseline_kf_nn','ric_graph_v0']:
        rr=[r for r in rows if r['algorithm']==alg]
        print(alg, {k:round(float(np.mean([x[k] for x in rr])),4) for k in ['track_purity','identity_switches','fragmentation','false_merge_rate','track_precision','track_recall','track_count']})

if __name__=='__main__': main()
