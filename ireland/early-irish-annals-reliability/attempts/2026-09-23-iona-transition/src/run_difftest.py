# -*- coding: utf-8 -*-
"""Do TERRITORY and IONA break at DIFFERENT dates, or is the 738 vs 830 gap what
you get for free from splitting 123 entries into two groups of 76 and 47?

Null: the two subsets are the same process.  Realised by holding every Scottish
entry in its own year and permuting only its TERRITORY/IONA label, which keeps
both the year profile and the overall Scottish time course exactly as observed
and destroys only the association between subset and date.
"""
import sys, os, json, re, collections, random
sys.path.insert(0,os.path.dirname(__file__))
import changepoint as cp

IONA=re.compile(r"(?<!Dath )(?<!Mac )\bÍ\b|\bIa\b|\bIona\b")
TERR=re.compile(r"Dál Riat|Pict|Fortriu|Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|"
 r"Mag Luinge|Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|Kingarth|"
 r"Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|Druim Alban|Iardoman|"
 r"Athfhotla|Circinn|Dún Nechtain")

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3 and r["witness"]=="AU" and 550<=r["year"]<1000]
yn=collections.Counter()
for r in USE: yn[r["year"]]+=1
YEARS=sorted(yn); NY=[yn[y] for y in YEARS]; IDX={y:i for i,y in enumerate(YEARS)}

scot=[r for r in USE if TERR.search(r["text"]) or IONA.search(r["text"])]
# an entry naming both counts as TERRITORY (the territorial detail is the rarer signal)
labels=[("T" if TERR.search(r["text"]) else "I") for r in scot]
yearsof=[r["year"] for r in scot]
print("Scottish entries %d  (TERRITORY %d, IONA-only %d)"%(len(scot),labels.count("T"),labels.count("I")))

def cut_for(lab_list, want):
    k=[0]*len(YEARS)
    for yy,lb in zip(yearsof,lab_list):
        if lb==want: k[IDX[yy]]+=1
    return cp.scan(YEARS,k,NY)[1]

cT,cI=cut_for(labels,"T"),cut_for(labels,"I")
obs=abs(cI-cT); signed=cI-cT
print("observed cuts: TERRITORY %d, IONA %d -> IONA later by %d years"%(cT,cI,signed))

rng=random.Random(606); NP=3000; ge=0; gesign=0; diffs=[]
lab=list(labels)
for _ in range(NP):
    rng.shuffle(lab)
    a,b=cut_for(lab,"T"),cut_for(lab,"I")
    if a is None or b is None: continue
    d=b-a; diffs.append(d)
    if abs(d)>=obs: ge+=1
    if d>=signed: gesign+=1
diffs.sort()
res={"n_scot":len(scot),"n_territory":labels.count("T"),"n_iona":labels.count("I"),
     "cut_territory":cT,"cut_iona":cI,"observed_gap_years":signed,
     "n_perm":len(diffs),"p_two_sided":(ge+1)/(len(diffs)+1),"p_one_sided":(gesign+1)/(len(diffs)+1),
     "null_gap_2.5":diffs[int(0.025*len(diffs))],"null_gap_97.5":diffs[int(0.975*len(diffs))],
     "null_gap_median":diffs[len(diffs)//2]}
print("label-permutation null (%d draws): gap median %d, 95%% range [%d, %d]"
      %(len(diffs),res["null_gap_median"],res["null_gap_2.5"],res["null_gap_97.5"]))
print("  p(|gap| >= observed %d)  = %.4f"%(obs,res["p_two_sided"]))
print("  p(gap >= observed %+d)   = %.4f  (one-sided: IONA breaks later)"%(signed,res["p_one_sided"]))
json.dump(res,open("results/difftest.json","w"),indent=1)
