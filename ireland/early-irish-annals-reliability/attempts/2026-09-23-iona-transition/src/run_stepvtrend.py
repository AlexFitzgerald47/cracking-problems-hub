# -*- coding: utf-8 -*-
"""(a) Is a searched STEP really better than a SMOOTH decline, once the step pays
for its search?  (b) Is any one gazetteer term carrying the break?"""
import sys, os, json, collections, random, math, re
sys.path.insert(0,os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
for r in USE: r["tags"]=gazetteer.tag(r["text"])

def au_series(pred):
    yk=collections.Counter(); yn=collections.Counter()
    for r in USE:
        if r["witness"]=="AU" and 550<=r["year"]<1000:
            yn[r["year"]]+=1
            if pred(r): yk[r["year"]]+=1
    ys=sorted(yn); return ys,[yk[y] for y in ys],[yn[y] for y in ys]

def logistic_fit(Y,K,NN,iters=500):
    b0,b1=math.log(0.05/0.95),0.0
    for _ in range(iters):
        g0=g1=h00=h01=h11=0.0
        for i in range(len(Y)):
            x=(Y[i]-775)/100.0
            p=1/(1+math.exp(-(b0+b1*x))); w=NN[i]*p*(1-p); res_=K[i]-NN[i]*p
            g0+=res_; g1+=res_*x; h00+=w; h01+=w*x; h11+=w*x*x
        det=h00*h11-h01*h01
        if abs(det)<1e-12: break
        b0+=(h11*g0-h01*g1)/det; b1+=(-h01*g0+h00*g1)/det
    return b0,b1

def ll_of(b0,b1,Y,K,NN):
    ll=0.0
    for i in range(len(Y)):
        x=(Y[i]-775)/100.0; p=min(max(1/(1+math.exp(-(b0+b1*x))),1e-12),1-1e-12)
        ll+=K[i]*math.log(p)+(NN[i]-K[i])*math.log(1-p)
    return ll

def ll_step(Y,K,NN,cut):
    a=sum(K[i] for i in range(len(Y)) if Y[i]<cut); b=sum(NN[i] for i in range(len(Y)) if Y[i]<cut)
    return cp._ll(a,b)+cp._ll(sum(K)-a,sum(NN)-b)

Y,K,NN=au_series(lambda r: r["tags"]["SCOT"])
b0,b1=logistic_fit(Y,K,NN); lin=ll_of(b0,b1,Y,K,NN)
best=max(((ll_step(Y,K,NN,Y[i+1]),Y[i+1]) for i in range(len(Y)-1)
          if sum(NN[:i+1])>=150 and sum(NN[i+1:])>=150))
obs_gain=best[0]-lin
print("observed: best step at %d, ll=%.2f; logistic trend ll=%.2f; gain=%.2f"%(best[1],best[0],lin,obs_gain))

rng=random.Random(555); NP=2000; ge=0; gains=[]
for _ in range(NP):
    k=[sum(1 for _ in range(NN[i]) if rng.random() < 1/(1+math.exp(-(b0+b1*(Y[i]-775)/100.0))))
       for i in range(len(Y))]
    c0,c1=logistic_fit(Y,k,NN); l=ll_of(c0,c1,Y,k,NN)
    bs=max(ll_step(Y,k,NN,Y[i+1]) for i in range(len(Y)-1)
           if sum(NN[:i+1])>=150 and sum(NN[i+1:])>=150)
    g=bs-l; gains.append(g)
    if g>=obs_gain: ge+=1
gains.sort()
p_step=(ge+1)/(NP+1)
print("simulating under the fitted SMOOTH trend, %d draws, same step search:"%NP)
print("  p(step gain) = %.4f   null gain median=%.2f  p95=%.2f"%(p_step,gains[NP//2],gains[int(0.95*NP)]))

# ---- leave-one-term-out --------------------------------------------------
TERMS={"Iona":r"(?<!Dath )(?<!Mac )\bÍ\b|\bIa\b|\bIona\b","Pict":r"Pict",
       "DalRiata":r"Dál Riat","Fortriu":r"Fortriu",
       "otherplaces":r"Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|Mag Luinge|Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|Kingarth|Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|Druim Alban|Iardoman|Athfhotla|Circinn|Dún Nechtain"}
print("\nleave-one-term-out (does one term carry the break?)")
loo={}
for drop in [None]+list(TERMS):
    keep=[p for t,p in TERMS.items() if t!=drop]
    rx=re.compile("|".join(keep))
    y2,k2,n2=au_series(lambda r,rx=rx: bool(rx.search(r["text"])))
    s,c,l,r_=cp.scan(y2,k2,n2)
    nl=cp.permutation_null(y2,k2,n2,n_perm=1500)
    loo[drop or "ALL"]={"cut":c,"stat":s,"n_tagged":sum(k2),"p":nl["p"],
                        "left_rate":l[0]/l[1],"right_rate":r_[0]/r_[1]}
    print("  drop %-12s tagged=%-4d cut=%-5s stat=%-6.2f %.4f->%.4f  p=%.4f"
          %(drop or "(none)",sum(k2),c,s,l[0]/l[1],r_[0]/r_[1],nl["p"]))

json.dump({"step_vs_trend":{"best_cut":best[1],"ll_step":best[0],"ll_trend":lin,
           "gain":obs_gain,"p_budget_matched":p_step,"null_gain_p95":gains[int(0.95*NP)],
           "logit_slope_per_century":b1},
           "leave_one_term_out":loo}, open("results/stepvtrend.json","w"),indent=1)
print("\nwrote results/stepvtrend.json")
