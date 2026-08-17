"""TFL-UAS-SPATIAL-001 v1.0: generate, construct, then evaluate relational states."""
from __future__ import annotations
import hashlib, json, math, shutil
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
ALG=ROOT/'data/algorithm_visible'; EVAL=ROOT/'data/evaluator_only'; OUT=ROOT/'results/exploratory'; DIAG=ROOT/'diagnostics'
SEEDS=range(101,121); SCENARIOS=['S1_global_translation','S2_global_rotation','S3_independent_random_motion','S4_apparent_spatial_organization','S5_perturbation_recovery']
PAIRS=[(i,j) for i in range(4) for j in range(i+1,4)]
DT=1.0; T=np.arange(181,dtype=float)

def write(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,separators=(',',':')),encoding='utf-8')
def track_id(seed,i): return 'trk_'+hashlib.sha256(f'spatial001/{seed}/{i}'.encode()).hexdigest()[:12]

def centroid(seed):
    ph=.004*T+.02*seed
    return np.stack([4200+18*T+180*np.sin(ph),3600+12*T+150*np.cos(ph),850+25*np.sin(.01*T+.1*seed)],1)

def positions(seed,scenario):
    rng=np.random.default_rng(7000+seed); c=centroid(seed); off=np.array([[-260,-170,0],[260,-170,0],[-260,170,0],[260,170,0]],float)
    ps=[]
    if scenario in ('S1_global_translation','S2_global_rotation','S5_perturbation_recovery'):
        for i,o in enumerate(off):
            if scenario=='S1_global_translation': scale=np.ones(181); ang=np.zeros(181)
            elif scenario=='S2_global_rotation': scale=np.ones(181); ang=.012*T+.08*np.sin(.02*T+.1*seed)
            else:
                scale=np.ones(181); scale[(T>=70)&(T<=100)]=1.8
                ang=.006*T
            x=o[0]*scale; y=o[1]*scale; co=np.cos(ang); si=np.sin(ang)
            rel=np.stack([co*x-si*y,si*x+co*y,np.zeros(181)],1)
            ps.append(c+rel+rng.normal(0,[2,2,1],(181,3)))
    elif scenario=='S3_independent_random_motion':
        for i,o in enumerate(off):
            q=np.zeros((181,3)); q[0]=o
            for k in range(1,181): q[k]=.97*q[k-1]+rng.normal(0,[5,5,1.5])
            ps.append(c+q+rng.normal(0,[2,2,1],(181,3)))
    else:
        # Local density is retained, but each object's relative placement is
        # repeatedly re-sampled, preventing persistent same-object relations.
        for i,o in enumerate(off):
            q=np.empty((181,3))
            for k in range(181):
                block=k//15; local=np.random.default_rng(900000+seed*31+block*7+i).normal(0,[210,140,35])
                q[k]=local+np.array([30*np.sin(.08*k+i),25*np.cos(.07*k+i),8*np.sin(.11*k+i)])
            ps.append(c+q+rng.normal(0,[2,2,1],(181,3)))
    return np.array(ps)

def make_track_record(seed,scenario):
    p=positions(seed,scenario); v=np.gradient(p,axis=1)/DT; a=np.gradient(v,axis=1)/DT; tracks=[]
    for i in range(4):
        tracks.append([{'track_id':track_id(seed,i),'timestamp':float(k),'position_xyz':p[i,k].round(6).tolist(),'velocity_xyz':v[i,k].round(6).tolist(),'acceleration_xyz':a[i,k].round(6).tolist(),'state_uncertainty':[16,16,4]} for k in range(181)])
    return {'track_states':tracks}

def arrays(rec):
    p=np.array([[x['position_xyz'] for x in tr] for tr in rec['track_states']],float)
    v=np.array([[x['velocity_xyz'] for x in tr] for tr in rec['track_states']],float)
    a=np.array([[x['acceleration_xyz'] for x in tr] for tr in rec['track_states']],float)
    return p,v,a

def relation_state(rec):
    p,v,a=arrays(rec); extent=np.maximum(np.ptp(p,axis=0).mean(axis=0),1e-6); scale=float(np.linalg.norm(extent)); rigid=[]; shape=[]; graph=[]; local=[]; spectra=[]
    pair_d=[]; pair_dd=[]; pair_h=[]
    for i,j in PAIRS:
        d=np.linalg.norm(p[i]-p[j],axis=1); dd=np.gradient(d); rv=v[i]-v[j]; den=np.linalg.norm(v[i],axis=1)*np.linalg.norm(v[j],axis=1)
        h=np.sum(v[i]*v[j],axis=1)/np.maximum(den,1e-9); pair_d.append(d); pair_dd.append(dd); pair_h.append(h)
    pair_d=np.array(pair_d); pair_dd=np.array(pair_dd); pair_h=np.array(pair_h); norm_d=pair_d/np.maximum(np.mean(pair_d,axis=0),1e-6)
    for k in range(181):
        w=np.exp(-0.5*norm_d[:,k]**2); A=np.zeros((4,4)); q=0
        for i,j in PAIRS: A[i,j]=A[j,i]=w[q]; q+=1
        deg=A.sum(1); inv=np.diag(1/np.sqrt(np.maximum(deg,1e-12))); L=np.eye(4)-inv@A@inv; eig=np.linalg.eigvalsh(L)
        graph.append({'weights':w.tolist(),'connectivity':float(np.count_nonzero(deg)/4),'clustering':float(np.mean([A[i,j]*A[j,k]*A[k,i] for i,j,k in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]])),'spectral_gap':float(eig[1]-eig[0]),'eigenvalues':eig.tolist(),'operator_change':0.0})
        rigid.append(np.r_[pair_d[:,k],pair_dd[:,k],pair_h[:,k]].tolist()); shape.append(np.r_[norm_d[:,k],pair_dd[:,k]/np.maximum(np.mean(pair_d[:,k]),1e-6),pair_h[:,k]].tolist())
        local.append(np.c_[A.sum(1),np.mean(pair_d[:,k].reshape(3 if False else 6) if False else np.array([pair_d[q,k] for q,(ii,jj) in enumerate(PAIRS) for node in [ii,jj]]).reshape(4,3),axis=1)].tolist())
    for k in range(1,181): graph[k]['operator_change']=float(np.linalg.norm(np.array(graph[k]['weights'])-np.array(graph[k-1]['weights'])))
    return {'rigid_relational_state':rigid,'shape_state':shape,'local_neighborhood_state':local,'global_spatial_relational_state':graph}

def distance(x,y):
    a=np.asarray(x,float); b=np.asarray(y,float); return float(np.linalg.norm(a-b)/max(np.sqrt(a.size),1))
def diagnostics(states):
    rigid=np.array(states['rigid_relational_state']); shape=np.array(states['shape_state']); graph=states['global_spatial_relational_state']; local=np.array(states['local_neighborhood_state'])
    pair_p=float(np.mean(np.abs(np.diff(rigid[:,:6],axis=0))<12)); local_p=float(np.mean(np.abs(np.diff(local,axis=0))<.25)); global_p=float(np.mean([distance(graph[k]['weights'],graph[k-1]['weights'])<.05 for k in range(1,181)]))
    ds=[distance(rigid[k],rigid[k-1]) for k in range(1,181)]; shape_ds=[distance(shape[k],shape[k-1]) for k in range(1,181)]
    return {'pair_relational_persistence':pair_p,'local_relational_persistence':local_p,'global_relational_state_persistence':global_p,'relational_state_distance_mean':float(np.mean(ds)),'temporal_state_change_mean':float(np.mean(ds)),'shape_state_change_mean':float(np.mean(shape_ds)),'graph_spectral_gap_mean':float(np.mean([x['spectral_gap'] for x in graph])),'graph_operator_change_mean':float(np.mean([x['operator_change'] for x in graph]))}

def main():
    for d in (ALG,EVAL,OUT,DIAG):
        if d.exists(): shutil.rmtree(d)
        d.mkdir(parents=True,exist_ok=True)
    metadata=[]; sample_no=1
    for seed in SEEDS:
        for scenario in SCENARIOS:
            sid=f'sample_{sample_no:04d}'; sample_no+=1; rec=make_track_record(seed,scenario)
            write(ALG/(sid+'.json'),rec)
            write(EVAL/(f'eval_{sample_no-1:04d}.json'),{'sample_id':sid,'scenario_id':scenario,'seed':seed,'expected_property':{'S1_global_translation':'rigid_invariant','S2_global_rotation':'rigid_invariant','S3_independent_random_motion':'persistence_decay','S4_apparent_spatial_organization':'low_false_persistence','S5_perturbation_recovery':'recovery'},'perturbation_start_s':70 if scenario.startswith('S5') else None,'perturbation_end_s':100 if scenario.startswith('S5') else None})
            metadata.append((sid,rec))
    # Algorithm-visible phase: no evaluator path is opened here.
    raw=[]
    for sid,rec in metadata:
        if any(key in rec for key in ('scenario_id','expected_property','seed')): raise RuntimeError('label leakage in algorithm-visible record')
        raw.append({'sample_id':sid,'states':relation_state(rec)})
    write(OUT/'raw_relational_states.json',raw)
    # Determinism and schema gates before evaluator loading.
    if relation_state(make_track_record(101,SCENARIOS[0])) != raw[0]['states']: raise RuntimeError('determinism gate failed')
    if any(any(k in x['states'] for k in ('scenario_id','expected_property','seed')) for x in raw): raise RuntimeError('state output leakage')
    # Evaluator-only phase starts only after raw output exists.
    truths={}; metrics=[]
    for path in sorted(EVAL.glob('eval_*.json')):
        e=json.loads(path.read_text(encoding='utf-8')); truths[e['sample_id']]=e
    for row in raw:
        e=truths[row['sample_id']]; m=diagnostics(row['states']); m.update({'sample_id':row['sample_id'],'scenario_id':e['scenario_id'],'seed':e['seed']}); metrics.append(m)
    grouped={}
    for s in SCENARIOS:
        rr=[m for m in metrics if m['scenario_id']==s]; grouped[s]={k:float(np.mean([x[k] for x in rr])) for k in rr[0] if k not in ('sample_id','scenario_id','seed')}
    # Recovery is registered and descriptive, not a tuned threshold.
    for m,row in zip(metrics,raw):
        if m['scenario_id']=='S5_perturbation_recovery':
            r=np.array(row['states']['rigid_relational_state']); base=np.mean(np.linalg.norm(r[30:60]-r[29:59],axis=1)); post=np.linalg.norm(r-r[59],axis=1); after=np.where(post[101:]<=base*1.2)[0]; m['recovery_latency_s']=float(after[0]+1 if len(after) else 180)
        else: m['recovery_latency_s']=None
    write(DIAG/'exploratory_metrics.json',{'status':'EXPLORATORY — REVIEW REQUIRED BEFORE EXTENSION','by_scenario':grouped,'records':metrics,'truth_loaded_after_raw_states':True})
    write(OUT/'exploratory_manifest.json',{'sample_count':len(raw),'seed_range':[101,120],'scenario_count':5,'raw_written_before_truth':True,'classifier_used':False})
    print(f'SPATIAL-001 exploratory raw states={len(raw)} metrics={len(metrics)} review_required=True')
if __name__=='__main__': main()
