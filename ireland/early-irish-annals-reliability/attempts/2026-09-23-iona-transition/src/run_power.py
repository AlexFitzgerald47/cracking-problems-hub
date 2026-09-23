# -*- coding: utf-8 -*-
"""How big a step, and how precisely located, could this corpus actually detect?

Simulation uses AU's REAL per-year entry counts for 550-1000, so the very uneven
year sizes (and the fact that a 6th-century year may hold 2 entries and a
9th-century year 12) are preserved exactly.  Only the tag is synthetic.
"""
import sys, os, json, collections, random, statistics
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
for r in USE: r["tags"]=gazetteer.tag(r["text"])
yn=collections.Counter()
for r in USE:
    if r["witness"]=="AU" and 550<=r["year"]<1000: yn[r["year"]]+=1
YEARS=sorted(yn); NY=[yn[y] for y in YEARS]; N=sum(NY)
TRUE_CUT=740
rng=random.Random(4242)

def simulate(p_pre, ratio):
    p_post=p_pre*ratio
    return [sum(1 for _ in range(NY[i]) if rng.random() < (p_pre if YEARS[i]<TRUE_CUT else p_post))
            for i in range(len(YEARS))]

def crit_value(K, n_perm=400, alpha=0.05):
    pool=[1]*K+[0]*(N-K); stats=[]
    for _ in range(n_perm):
        rng.shuffle(pool); kk=[]; pos=0
        for ni in NY: kk.append(sum(pool[pos:pos+ni])); pos+=ni
        stats.append(cp.scan(YEARS,kk,NY)[0])
    stats.sort(); return stats[int((1-alpha)*n_perm)]

P_PRE = 0.080   # AU's observed pre-738 Scottish rate
NSIM = 400
rows=[]
print("AU 550-1000: %d years, %d entries.  Simulated step at %d, pre-rate %.3f."%(len(YEARS),N,TRUE_CUT,P_PRE))
print("%-8s %-9s %-7s %-7s %-9s %-10s"%("ratio","E[tagged]","crit","power","med|err|","P(|err|<=20yr)"))
for ratio in (1.0, 0.75, 0.5, 0.35, 0.25, 0.15, 0.05):
    exp_k=int(round(sum(NY[i]*(P_PRE if YEARS[i]<TRUE_CUT else P_PRE*ratio) for i in range(len(YEARS)))))
    cv=crit_value(exp_k)
    hits=0; errs=[]
    for _ in range(NSIM):
        k=simulate(P_PRE,ratio)
        s,c,_,_=cp.scan(YEARS,k,NY)
        if s>=cv:
            hits+=1
            if c is not None: errs.append(abs(c-TRUE_CUT))
    power=hits/NSIM
    med=statistics.median(errs) if errs else float("nan")
    within=sum(1 for e in errs if e<=20)/NSIM if errs else 0.0
    rows.append({"ratio":ratio,"expected_tagged":exp_k,"crit":cv,"power":power,
                 "median_abs_error_yr":med,"p_within_20yr":within})
    print("%-8.2f %-9d %-7.2f %-7.3f %-9s %-10.3f"%(ratio,exp_k,cv,power,
          "%.0f"%med if errs else "-",within))

# how many tagged entries would be needed to localise a 2x drop to +-20 years?
print("\nLocalisation vs corpus size (step 0.080 -> 0.040 at 740; AU year profile scaled up):")
scale_rows=[]
for mult in (1, 2, 4, 8, 16):
    NYs=[ni*mult for ni in NY]; Ns=sum(NYs)
    errs=[]; 
    for _ in range(300):
        k=[sum(1 for _ in range(NYs[i]) if rng.random() < (0.080 if YEARS[i]<TRUE_CUT else 0.040))
           for i in range(len(YEARS))]
        s,c,_,_=cp.scan(YEARS,k,NYs,min_entries=150*mult)
        if c is not None: errs.append(abs(c-TRUE_CUT))
    errs.sort()
    r={"corpus_multiple":mult,"expected_tagged":int(round(0.06*Ns)),
       "median_abs_error_yr":errs[len(errs)//2],"p90_abs_error_yr":errs[int(0.9*len(errs))],
       "p_within_20yr":sum(1 for e in errs if e<=20)/len(errs)}
    scale_rows.append(r)
    print("  x%-3d entries=%-6d tagged~%-5d  median|err|=%-4d  p90|err|=%-4d  P(|err|<=20)=%.2f"
          %(mult,Ns,r["expected_tagged"],r["median_abs_error_yr"],r["p90_abs_error_yr"],r["p_within_20yr"]))

json.dump({"detection":rows,"localisation":scale_rows,
           "au_year_profile":{"n_years":len(YEARS),"n_entries":N}},
          open("results/power.json","w"),indent=1)
print("\nwrote results/power.json")
