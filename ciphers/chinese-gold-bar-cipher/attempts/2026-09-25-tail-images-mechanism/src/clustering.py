#!/usr/bin/env python3
"""EXPLORATORY (not frozen): is the repeated-letter excess in the long strings
a *local* clustering effect -- equal letters close together -- or spread out?

Statistic: for each string, the number of ordered pairs (i,j), i<j, with
s[i]==s[j] and j-i <= d, for d = 1..5. Deal null as before. Reported with the
number of statistics computed so the budget is visible; treat as a lead, not a
result.
"""
import collections, random, os, json
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
strings=[l.strip() for l in open(os.path.join(HERE,"data","cryptograms_corrected.txt")) if l.strip()]
lengths=[len(s) for s in strings]; pool=list("".join(strings))
def close_pairs(ss,d):
    n=0
    for s in ss:
        for i in range(len(s)):
            for j in range(i+1, min(i+d+1, len(s))):
                if s[i]==s[j]: n+=1
    return n
rng=random.Random(31337); REPS=100000
DS=[1,2,3,4,5]
obs={d:close_pairs(strings,d) for d in DS}
null={d:[] for d in DS}
for _ in range(REPS):
    p=pool[:]; rng.shuffle(p); k=0; sim=[]
    for L in lengths: sim.append(p[k:k+L]); k+=L
    for d in DS: null[d].append(close_pairs(sim,d))
print(f"{'d':>3} {'obs':>6} {'null':>8} {'sd':>6} {'z':>7} {'p(>=)':>8} {'p(<=)':>8}")
res={}
for d in DS:
    a=null[d]; m=sum(a)/REPS; sd=(sum((x-m)**2 for x in a)/REPS)**0.5
    z=(obs[d]-m)/sd
    phi=(sum(1 for x in a if x>=obs[d])+1)/(REPS+1)
    plo=(sum(1 for x in a if x<=obs[d])+1)/(REPS+1)
    print(f"{d:>3} {obs[d]:>6} {m:>8.2f} {sd:>6.2f} {z:>7.2f} {phi:>8.5f} {plo:>8.5f}")
    res[d]={"obs":obs[d],"null":m,"sd":sd,"z":z,"p_ge":phi,"p_le":plo}
json.dump(res, open(os.path.join(HERE,"out","clustering.json"),"w"), indent=2)
print("\n5 statistics computed; Bonferroni 0.05 threshold = 0.01.")
