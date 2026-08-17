"""Frozen v1.1 exploratory pipeline: generate, fit, predict, then evaluate."""
from __future__ import annotations
import hashlib, json, math, shutil
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
ALG, EVAL, TRAIN = ROOT/'data/algorithm_visible', ROOT/'data/evaluator_only', ROOT/'data/training_visible'
PRED, DIAG = ROOT/'results/exploratory/predictions', ROOT/'diagnostics'
SEEDS_TRAIN, SEEDS_TEST = range(101,111), range(111,121)
CLASSES = [('apparent_group',0),('coordinated_group',1)]

def tid(seed, i): return 'trk_'+hashlib.sha256(f'v11-track/{seed}/{i}'.encode()).hexdigest()[:12]
def make_states(seed, coordinated):
    t=np.arange(181,dtype=float); rng=np.random.default_rng(seed*1009+(1 if coordinated else 0))
    phase=0.006*t; centroid=np.stack([4100+22*t+260*np.sin(phase),3700+15*t+180*np.cos(phase),900+35*np.sin(.012*t)],1)
    offsets=np.array([[-240,-160,0],[240,-160,0],[-240,160,0],[240,160,0]],float); states=[]
    for i,off in enumerate(offsets):
        ph=.031*t + (0 if coordinated else [0,np.pi/2,np.pi,3*np.pi/2][i]) + .13*seed
        scale=1+.08*np.sin(ph)
        angle=.10*np.sin(.018*t+.07*seed) if coordinated else .10*np.sin(.018*t+.07*seed+[0,.4,.8,1.2][i])
        x,y=off[0]*scale,off[1]*scale; c,s=np.cos(angle),np.sin(angle)
        rel=np.stack([c*x-s*y,s*x+c*y,np.zeros_like(t)],1)
        noise=rng.normal(0,[8,8,4],size=(181,3))
        p=centroid+rel+noise
        v=np.gradient(p,axis=0); a=np.gradient(v,axis=0)
        states.append([{'track_id':tid(seed,i),'timestamp':float(k),'position_xyz':p[k].round(6).tolist(),'velocity_xyz':v[k].round(6).tolist(),'acceleration_xyz':a[k].round(6).tolist(),'state_uncertainty':[64,64,16]} for k in range(181)])
    return {'track_states':states}

def features(sample):
    p=np.array([[s['position_xyz'] for s in tr] for tr in sample['track_states']],float); v=np.array([[s['velocity_xyz'] for s in tr] for tr in sample['track_states']],float)
    speed=np.linalg.norm(v,axis=2); out=[speed.mean(),p[:,:,2].mean(),np.linalg.norm(v.mean(0),axis=1).mean()]
    ds=[]; relcorr=[]; temporal=[]
    for i in range(4):
      for j in range(i+1,4):
        d=np.linalg.norm(p[i]-p[j],axis=1); rv=np.linalg.norm(v[i]-v[j],axis=1)
        ds.append(d); relcorr.append(float(np.corrcoef(d[:-1],d[1:])[0,1])); temporal.append(float(np.mean(np.abs(np.diff(d))<12)))
    ds=np.array(ds); out += [ds.mean(),np.ptp(p,axis=0).mean(),float(np.mean([np.dot(v[i,k],v[j,k])/(np.linalg.norm(v[i,k])*np.linalg.norm(v[j,k])+1e-9) for i in range(4) for j in range(i+1,4) for k in range(181)]))]
    baseline=np.array(out,float)
    rel=np.array([np.mean(relcorr),np.std(relcorr),np.mean(temporal),np.std(temporal),float(np.mean(ds[:,-1])),float(np.mean(np.std(ds,axis=1)))])
    # Graph sequence from pairwise distance stability; spectral block is diagnostic extension.
    graph=[]; eig=[]
    for k in range(10,181,5):
      A=(np.exp(-np.var(ds[:,:k],axis=1)/4000)>0.42).astype(float); M=np.zeros((4,4)); q=0
      for i in range(4):
       for j in range(i+1,4): M[i,j]=M[j,i]=A[q]; q+=1
      d=M.sum(1); L=np.eye(4)-np.diag(1/np.sqrt(np.maximum(d,1e-9)))@M@np.diag(1/np.sqrt(np.maximum(d,1e-9))); eig.append(np.linalg.eigvalsh(L)); graph.append(M)
    eig=np.array(eig); rel=np.r_[rel,float(np.mean([np.count_nonzero(g)/2 for g in graph])),float(np.std([np.count_nonzero(g)/2 for g in graph]))]
    spectral=np.array([np.mean(eig[:,1]-eig[:,0]),np.std(eig[:,1]-eig[:,0]),np.mean(eig),np.std(eig)])
    return {'baseline':baseline,'relational':rel,'spectral':spectral}

def write_json(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,separators=(',',':')),encoding='utf-8')
def marginal(sample):
    f=features(sample)['baseline']; return f.tolist()
def audit(rows):
    result={}
    for col in range(len(rows[0]['marginals'])):
      vals=np.array([r['marginals'][col] for r in rows]); y=np.array([r['label'] for r in rows]); best=0
      for q in np.unique(vals):
       for s in (-1,1):
        pred=(s*vals>=s*q); best=max(best,.5*((pred[y==1]).mean()+(~pred[y==0]).mean()))
      result[str(col)]=float(best)
    return result
def main():
    for d in (ALG,EVAL,TRAIN,PRED,DIAG):
      if d.exists(): shutil.rmtree(d)
      d.mkdir(parents=True,exist_ok=True)
    trainX=[]; trainy=[]; train_meta=[]; test_rows=[]
    n=1
    for seed in list(SEEDS_TRAIN)+list(SEEDS_TEST):
      for cls,label in CLASSES:
        sample=make_states(seed,label==1)
        if seed in SEEDS_TRAIN:
          x=features(sample); trainX.append(np.r_[x['baseline'],x['relational'],x['spectral']].tolist()); trainy.append(label); train_meta.append({'sample_id':f'train_{len(trainy):04d}','label':label,'seed':seed})
        else:
          sid=f'sample_{n:04d}'; n+=1
          write_json(ALG/(sid+'.json'),sample)
          write_json(EVAL/(f'eval_{n-1:04d}.json'),{'sample_id':sid,'ground_truth_coordination_state':'coordinated' if label else 'independent','scenario_class':cls,'scenario_variant':'v11_exploratory','seed':seed,'ground_truth_object_id':[tid(seed,i) for i in range(4)]})
          test_rows.append((sid,sample,label))
    write_json(TRAIN/'training_features.json',{'feature_definition':'baseline+relational+spectral v1.1','rows':[{'sample_id':m['sample_id'],'label':m['label'],'features':x} for m,x in zip(train_meta,trainX)],'labels_are_training_only':True})
    # Determinism check uses exact regenerated test state.
    if make_states(111,False)!=test_rows[0][1]: raise RuntimeError('determinism check failed')
    # Fit only from training partition; test labels are not passed to this procedure.
    X=np.array(trainX); y=np.array(trainy); models={}
    for name,sl in [('A_conventional_kinematic_baseline',slice(0,7)),('B_temporal_relational_no_spectral',slice(7,16)),('C_temporal_relational_with_spectral',slice(7,None))]:
      model=LogisticRegression(C=1.0,solver='liblinear',max_iter=2000,random_state=0).fit(X[:,sl],y); models[name]=(model,sl)
    predictions=[]
    for sid,sample,_ in test_rows:
      f=features(sample); z=np.r_[f['baseline'],f['relational'],f['spectral']]
      for name,(model,sl) in models.items():
        prob=float(model.predict_proba(z[sl].reshape(1,-1))[0,1]); predictions.append({'sample_id':sid,'model':name,'probability':prob,'predicted_label':int(prob>=.5),'train_samples':len(y),'truth_loaded':False})
    write_json(PRED/'predictions.json',predictions); write_json(PRED/'prediction_manifest.json',{'test_sample_count':len(test_rows),'prediction_count':len(predictions),'truth_loaded':False,'supervised_training_partition':'data/training_visible/training_features.json'})
    audit_rows=[{'sample_id':sid,'label':label,'marginals':marginal(sample)} for sid,sample,label in test_rows]; audits=audit(audit_rows)
    write_json(DIAG/'v1.1_marginal_audit.json',{'status':'validation','audits':audits,'rows':audit_rows,'max_allowed_balanced_accuracy':.85})
    if max(audits.values())>.85:
      write_json(ROOT/'REVIEW_REQUIRED_v1.1.json',{'what_happened':'Anti-trivial marginal audit failed','relevant_metrics':audits,'why_stopped':'A one-variable marginal remains too predictive; A/B/C interpretation is prohibited.','options':['review simulator and freeze a new version','retain v1.1 as failed validation'],'recommended_action':'Conservative scientific review before any further execution.'}); raise SystemExit('REVIEW_REQUIRED: anti-trivial audit failed')
    truth={r[0]:r[2] for r in test_rows}; summary={}
    for name in models:
      rr=[r for r in predictions if r['model']==name]; yy=np.array([truth[r['sample_id']] for r in rr]); pp=np.array([r['predicted_label'] for r in rr]); ss=np.array([r['probability'] for r in rr]); summary[name]={'status':'EXPLORATORY — NOT A SCIENTIFIC DECISION','balanced_accuracy':float(((pp[yy==1]).mean()+(pp[yy==0]==0).mean())/2),'ROC_AUC':float(roc_auc_score(yy,ss))}
    write_json(ROOT/'results/exploratory/summary.json',summary); print('v1.1 exploratory validation passed; metrics written for review only')
if __name__=='__main__': main()
