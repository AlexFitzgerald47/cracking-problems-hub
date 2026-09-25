#!/usr/bin/env python3
"""Where does the max-distinct deficit live? Per-string distinctness against a
length-matched deal null, plus a length-stratified summary.

The deal null is the right comparator: it draws each string from the observed
261-letter multiset without replacement, so it already contains the "depleting
balanced supply" mechanism. Anything the data does that this null does not is
NOT explained by a bag of tiles.
"""
import collections, random, os, json
HERE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
strings=[l.strip() for l in open(os.path.join(HERE,"data","cryptograms_corrected.txt")) if l.strip()]
lengths=[len(s) for s in strings]; pool=list("".join(strings))
rng=random.Random(99); REPS=200000
per=[[] for _ in strings]
for _ in range(REPS):
    p=pool[:]; rng.shuffle(p); k=0
    for i,L in enumerate(lengths):
        per[i].append(len(set(p[k:k+L]))); k+=L
print(f"{'string':<26} {'len':>4} {'distinct':>9} {'null':>7} {'sd':>6} {'z':>7} {'p(<=)':>8}")
res=[]
for i,s in enumerate(strings):
    o=len(set(s)); a=per[i]; m=sum(a)/len(a)
    sd=(sum((x-m)**2 for x in a)/len(a))**0.5
    p=(sum(1 for x in a if x<=o)+1)/(REPS+1)
    z=(o-m)/sd if sd else 0
    print(f"{s:<26} {len(s):>4} {o:>9} {m:>7.2f} {sd:>6.2f} {z:>7.2f} {p:>8.4f}")
    res.append({"s":s,"len":len(s),"distinct":o,"null":m,"sd":sd,"z":z,"p_le":p})
# length-stratified: the 5 longest vs the rest, summed distinctness
order=sorted(range(16), key=lambda i:-lengths[i])
for cut,name in [(5,"5 longest (19-25)"),(8,"8 longest"),(16,"all 16")]:
    idx=order[:cut]
    o=sum(len(set(strings[i])) for i in idx)
    arr=[sum(per[i][r] for i in idx) for r in range(REPS)]
    m=sum(arr)/REPS; sd=(sum((x-m)**2 for x in arr)/REPS)**0.5
    p=(sum(1 for x in arr if x<=o)+1)/(REPS+1)
    print(f"\n{name}: sum distinct obs={o}  null={m:.2f} +/- {sd:.2f}  z={(o-m)/sd:+.2f}  p(<=)={p:.5f}")
json.dump(res, open(os.path.join(HERE,"out","perstring.json"),"w"), indent=2)
