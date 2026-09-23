# -*- coding: utf-8 -*-
"""Permutation null for the 2-changepoint improvement, and for the 2-cp fit itself.

Adding a second changepoint always raises the likelihood, and the improvement is
maximised over ~200x200 candidate pairs, so a chi-squared p-value on 2 df is not
the right yardstick.  The null below searches the same grid on permuted data and
so pays the same search cost.
"""
import sys, os, json, collections, random
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
for r in USE: r["tags"]=gazetteer.tag(r["text"])

def series(w,tag,lo,hi):
    yk=collections.Counter(); yn=collections.Counter()
    for r in USE:
        if r["witness"]==w and lo<=r["year"]<hi:
            yn[r["year"]]+=1
            if r["tags"][tag]: yk[r["year"]]+=1
    ys=sorted(yn); return ys,[yk[y] for y in ys],[yn[y] for y in ys]

def fit2(y,k,n,minseg=150):
    K,N=sum(k),sum(n); base=cp._ll(K,N)
    ck=[0]; cn=[0]
    for i in range(len(y)): ck.append(ck[-1]+k[i]); cn.append(cn[-1]+n[i])
    best=(-1,None,None,None)
    for i in range(len(y)-2):
        if cn[i+1]<minseg: continue
        if N-cn[i+1]<2*minseg: break
        for j in range(i+1,len(y)-1):
            n1,k1=cn[i+1],ck[i+1]
            n2,k2=cn[j+1]-cn[i+1],ck[j+1]-ck[i+1]
            n3,k3=N-cn[j+1],K-ck[j+1]
            if n2<minseg or n3<minseg: continue
            s=2*(cp._ll(k1,n1)+cp._ll(k2,n2)+cp._ll(k3,n3)-base)
            if s>best[0]: best=(s,y[i+1],y[j+1],((k1,n1),(k2,n2),(k3,n3)))
    return best

y,k,n=series("AU","SCOT",550,1000)
s1=cp.scan(y,k,n)[0]
b2=fit2(y,k,n)
obs_imp=b2[0]-s1
print("observed: 1cp stat %.2f | 2cp stat %.2f at cuts %d,%d | improvement %.2f"%(s1,b2[0],b2[1],b2[2],obs_imp))

rng=random.Random(97); K,N=sum(k),sum(n); pool=[1]*K+[0]*(N-K)
ge2=ge_imp=0; NP=2000; imps=[]; s2s=[]
for t in range(NP):
    rng.shuffle(pool); kk=[]; pos=0
    for ni in n: kk.append(sum(pool[pos:pos+ni])); pos+=ni
    a=cp.scan(y,kk,n)[0]; b=fit2(y,kk,n)[0]
    imps.append(b-a); s2s.append(b)
    if b>=b2[0]: ge2+=1
    if b-a>=obs_imp: ge_imp+=1
imps.sort(); s2s.sort()
res={"one_cp_stat":s1,"two_cp_stat":b2[0],"cuts":[b2[1],b2[2]],
     "segments":[{"k":a,"n":bq,"rate":a/bq} for a,bq in b2[3]],
     "improvement":obs_imp,"n_perm":NP,
     "p_two_cp_stat":(ge2+1)/(NP+1),"p_improvement":(ge_imp+1)/(NP+1),
     "null_improvement_p95":imps[int(0.95*NP)],"null_improvement_median":imps[NP//2],
     "null_two_cp_p95":s2s[int(0.95*NP)]}
print("permutation (same 2-D search grid, %d draws):"%NP)
print("  p(2cp stat)      = %.4f   null p95 = %.2f"%(res["p_two_cp_stat"],res["null_two_cp_p95"]))
print("  p(improvement)   = %.4f   null improvement median=%.2f p95=%.2f"
      %(res["p_improvement"],res["null_improvement_median"],res["null_improvement_p95"]))
print("  segments: %s"%["%d/%d=%.3f"%(a,bq,a/bq) for a,bq in b2[3]])
json.dump(res,open("results/twocp.json","w"),indent=1)
