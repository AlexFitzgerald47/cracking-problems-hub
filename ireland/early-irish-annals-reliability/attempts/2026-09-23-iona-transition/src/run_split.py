# -*- coding: utf-8 -*-
"""EXPLORATORY, then tested out of sample.

Leave-one-term-out moved the fitted break from 808 to 738 as soon as mentions of
IONA ITSELF were removed.  That says the Scottish tag is two processes, not one:

  TERRITORY  Dal Riata, Pictland, Argyll/Clyde topography  -- the chronicle's
             local Scottish horizon
  IONA       the monastery, by name                         -- an institution an
             Irish annalist would keep hearing about wherever he sat

A chronicle physically leaving Iona predicts the first closing while the second
stays open.  Splitting them is post hoc and is labelled as such; it is then
tested on Chronicon Scotorum, an independent manuscript tradition, straight
across its own 723-803 lacuna, which no choice made here can have tuned.
"""
import sys, os, json, re, collections, random
sys.path.insert(0,os.path.dirname(__file__))
import changepoint as cp

IONA = re.compile(r"(?<!Dath )(?<!Mac )\bÍ\b|\bIa\b|\bIona\b")
TERR = re.compile(r"Dál Riat|Pict|Fortriu|Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|"
                  r"Mag Luinge|Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|"
                  r"Kingarth|Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|"
                  r"Druim Alban|Iardoman|Athfhotla|Circinn|Dún Nechtain")

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
def ser(w,rx,lo,hi):
    yk=collections.Counter(); yn=collections.Counter()
    for r in USE:
        if r["witness"]==w and lo<=r["year"]<hi:
            yn[r["year"]]+=1
            if rx.search(r["text"]): yk[r["year"]]+=1
    ys=sorted(yn); return ys,[yk[y] for y in ys],[yn[y] for y in ys]

out={}
for name,rx in (("TERRITORY",TERR),("IONA",IONA)):
    y,k,n=ser("AU",rx,550,1000)
    s,c,l,r=cp.scan(y,k,n)
    nl=cp.permutation_null(y,k,n,n_perm=5000)
    bt=cp.bootstrap_cut(y,k,n,n_boot=2000)
    K,N=sum(k),sum(n); base=cp._ll(K,N); prof=[]; ck=cn=0
    for i in range(len(y)-1):
        ck+=k[i]; cn+=n[i]
        if cn<150 or N-cn<150: continue
        prof.append((y[i+1],2*(cp._ll(ck,cn)+cp._ll(K-ck,N-cn)-base)))
    bv=max(p[1] for p in prof); supp=[cc for cc,ss in prof if ss>=bv-3.84]
    # posterior-predictive: could this series have come from a sharp step at 740? at 808?
    rng=random.Random(31337); ppc={}
    for hyp in (740,808):
        a=sum(k[i] for i in range(len(y)) if y[i]<hyp); b=sum(n[i] for i in range(len(y)) if y[i]<hyp)
        cc2=K-a; d=N-b; p0,p1=a/b,cc2/d; cuts=[]
        for _ in range(3000):
            kk=[sum(1 for _ in range(n[i]) if rng.random()<(p0 if y[i]<hyp else p1)) for i in range(len(y))]
            _,cx,_,_=cp.scan(y,kk,n)
            if cx is not None: cuts.append(cx)
        cuts.sort()
        ppc[str(hyp)]={"rate_pre":p0,"rate_post":p1,
            "sim_median":cuts[len(cuts)//2],"sim_2.5":cuts[int(0.025*len(cuts))],
            "sim_97.5":cuts[int(0.975*len(cuts))],
            "p_as_far_as_observed":sum(1 for x in cuts if abs(x-hyp)>=abs(c-hyp))/len(cuts)}
    out["AU_"+name]={"n_tagged":K,"cut":c,"stat":s,"support_interval":[min(supp),max(supp)],
        "left":{"k":l[0],"n":l[1],"rate":l[0]/l[1]},"right":{"k":r[0],"n":r[1],"rate":r[0]/r[1]},
        "null":nl,"bootstrap_cut":bt,"ppc":ppc}
    print("AU %-9s tagged=%-4d cut=%-4d stat=%.2f  %.4f -> %.4f  perm p=%.4f  support=[%d,%d] boot95=[%d,%d]"
          %(name,K,c,s,l[0]/l[1],r[0]/r[1],nl["p"],min(supp),max(supp),bt["lo95"],bt["hi95"]))
    for h in ("740","808"):
        q=ppc[h]; print("      if a sharp step at %s: sim argmax median %d [%d,%d];  P(as far as observed) = %.4f"
              %(h,q["sim_median"],q["sim_2.5"],q["sim_97.5"],q["p_as_far_as_observed"]))

# ---- OUT OF SAMPLE: Chronicon Scotorum, across its own lacuna --------------
print("\nOUT OF SAMPLE -- Chronicon Scotorum, straight across its 723-803 lacuna:")
oos={}
for name,rx in (("TERRITORY",TERR),("IONA",IONA)):
    y,k,n=ser("CS",rx,550,1000)
    a=sum(k[i] for i in range(len(y)) if y[i]<723); b=sum(n[i] for i in range(len(y)) if y[i]<723)
    c2=sum(k[i] for i in range(len(y)) if y[i]>=804); d=sum(n[i] for i in range(len(y)) if y[i]>=804)
    p=cp.fisher_exact_greater(a,b-a,c2,d-c2)
    oos[name]={"pre":[a,b],"post":[c2,d],"rate_pre":a/b,"rate_post":c2/d,"fisher_p_greater":p,
               "fold_change":(c2/d)/(a/b) if a else None}
    print("  CS %-9s pre 723: %d/%d = %.4f   post 803: %d/%d = %.4f   fold %.2f   fisher p=%.4f"
          %(name,a,b,a/b,c2,d,c2/d,(c2/d)/(a/b) if a else float('nan'),p))
# AT, low power, direction only
print("\n  (AT ends 766, so it can only show the pre-side; reported for completeness)")
for name,rx in (("TERRITORY",TERR),("IONA",IONA)):
    y,k,n=ser("AT",rx,550,767)
    a=sum(k[i] for i in range(len(y)) if y[i]<738); b=sum(n[i] for i in range(len(y)) if y[i]<738)
    c2=sum(k[i] for i in range(len(y)) if y[i]>=738); d=sum(n[i] for i in range(len(y)) if y[i]>=738)
    p=cp.fisher_exact_greater(a,b-a,c2,d-c2) if b and d else None
    oos["AT_"+name]={"pre":[a,b],"post":[c2,d],"fisher_p_greater":p}
    print("  AT %-9s 550-737: %d/%d = %.4f   738-766: %d/%d = %.4f   fisher p=%s"
          %(name,a,b,a/b if b else 0,c2,d,c2/d if d else 0,"%.4f"%p if p else "-"))
out["out_of_sample"]=oos
json.dump(out,open("results/split.json","w"),indent=1)
print("\nwrote results/split.json")
