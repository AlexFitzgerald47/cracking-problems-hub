# -*- coding: utf-8 -*-
"""Posterior-predictive check: is the observed AU Scottish series consistent with
a SHARP single step at the traditional c.740, or with one at the fitted 808?

The power run showed this corpus localises a clean 2x step to within 20 years in
78% of replicates, so 'underpowered' is NOT an available excuse for the argmax
landing at 808.  Either the step is late, or it is not sharp.
"""
import sys, os, json, collections, random, statistics
sys.path.insert(0,os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
for r in USE: r["tags"]=gazetteer.tag(r["text"])
yk=collections.Counter(); yn=collections.Counter()
for r in USE:
    if r["witness"]=="AU" and 550<=r["year"]<1000:
        yn[r["year"]]+=1
        if r["tags"]["SCOT"]: yk[r["year"]]+=1
Y=sorted(yn); K=[yk[y] for y in Y]; NN=[yn[y] for y in Y]
obs_stat,obs_cut,_,_=cp.scan(Y,K,NN)
rng=random.Random(8080)

def fitted(cut):
    a=sum(K[i] for i in range(len(Y)) if Y[i]<cut); b=sum(NN[i] for i in range(len(Y)) if Y[i]<cut)
    c=sum(K[i] for i in range(len(Y)) if Y[i]>=cut); d=sum(NN[i] for i in range(len(Y)) if Y[i]>=cut)
    return (a/b, c/d, a,b,c,d)

def ppc(cut, nsim=3000):
    p0,p1,a,b,c,d=fitted(cut)
    cuts=[]
    for _ in range(nsim):
        k=[sum(1 for _ in range(NN[i]) if rng.random() < (p0 if Y[i]<cut else p1)) for i in range(len(Y))]
        s,cc,_,_=cp.scan(Y,k,NN)
        if cc is not None: cuts.append(cc)
    cuts.sort()
    return {"cut":cut,"rate_pre":p0,"rate_post":p1,"cells":[a,b,c,d],
            "sim_cut_median":cuts[len(cuts)//2],
            "sim_cut_2.5":cuts[int(0.025*len(cuts))],"sim_cut_97.5":cuts[int(0.975*len(cuts))],
            "p_argmax_at_least_as_far_as_obs":sum(1 for x in cuts if abs(x-cut)>=abs(obs_cut-cut))/len(cuts),
            "p_argmax_ge_808":sum(1 for x in cuts if x>=808)/len(cuts),
            "p_argmax_le_740":sum(1 for x in cuts if x<=740)/len(cuts)}

print("observed: argmax=%d  stat=%.2f"%(obs_cut,obs_stat))
res={}
for cut in (740,808):
    r=ppc(cut); res["H%d"%cut]=r
    print("\nH_%d: fitted rates %.4f -> %.4f  (cells %d/%d and %d/%d)"
          %(cut,r["rate_pre"],r["rate_post"],r["cells"][0],r["cells"][1],r["cells"][2],r["cells"][3]))
    print("  simulated argmax: median %d, 95%% range [%d, %d]"%(r["sim_cut_median"],r["sim_cut_2.5"],r["sim_cut_97.5"]))
    print("  P(argmax at least as far from %d as the observed %d) = %.4f"%(cut,obs_cut,r["p_argmax_at_least_as_far_as_obs"]))
    print("  P(argmax >= 808) = %.4f   P(argmax <= 740) = %.4f"%(r["p_argmax_ge_808"],r["p_argmax_le_740"]))

# ---- linear-trend alternative: is the decline gradual rather than stepped? --
import math
def logistic_fit(Y,K,NN,iters=400):
    b0,b1=math.log(0.05/0.95),0.0
    for _ in range(iters):
        g0=g1=h00=h01=h11=0.0
        for i in range(len(Y)):
            x=(Y[i]-775)/100.0
            eta=b0+b1*x; p=1/(1+math.exp(-eta)); w=NN[i]*p*(1-p)
            res_=K[i]-NN[i]*p
            g0+=res_; g1+=res_*x; h00+=w; h01+=w*x; h11+=w*x*x
        det=h00*h11-h01*h01
        if abs(det)<1e-12: break
        b0+= (h11*g0-h01*g1)/det; b1+= (-h01*g0+h00*g1)/det
    ll=0.0
    for i in range(len(Y)):
        x=(Y[i]-775)/100.0; p=1/(1+math.exp(-(b0+b1*x)))
        p=min(max(p,1e-12),1-1e-12)
        ll+=K[i]*math.log(p)+(NN[i]-K[i])*math.log(1-p)
    return b0,b1,ll
b0,b1,ll_lin=logistic_fit(Y,K,NN)
ll_null=cp._ll(sum(K),sum(NN))
# step model log-lik at the fitted cut
a=sum(K[i] for i in range(len(Y)) if Y[i]<obs_cut); b=sum(NN[i] for i in range(len(Y)) if Y[i]<obs_cut)
ll_step=cp._ll(a,b)+cp._ll(sum(K)-a,sum(NN)-b)
print("\nmodel comparison on AU SCOT 550-1000 (log-likelihood, higher is better):")
print("  constant rate                 %.2f   (1 param)"%ll_null)
print("  smooth logistic trend in year %.2f   (2 params, slope %.3f per century)"%(ll_lin,b1))
print("  single step at fitted %d      %.2f   (3 params: 2 rates + a searched cut)"%(obs_cut,ll_step))
print("  -> trend beats constant by %.2f; step beats trend by %.2f"%(ll_lin-ll_null, ll_step-ll_lin))
res["trend"]={"logit_b0":b0,"logit_slope_per_century":b1,"ll_constant":ll_null,
              "ll_trend":ll_lin,"ll_step":ll_step}
json.dump(res,open("results/gof.json","w"),indent=1)
print("\nwrote results/gof.json")
