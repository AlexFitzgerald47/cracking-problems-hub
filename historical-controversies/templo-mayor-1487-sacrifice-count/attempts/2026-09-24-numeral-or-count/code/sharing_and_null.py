#!/usr/bin/env python3
"""(A) Is the four-way agreement on 80,400 remarkable given how much these
chroniclers agree on large numbers generally?
(B) Null model for Ixtlilxochitl's four-part breakdown of 80,400."""
import csv, itertools, random, collections

PRIMARY = {'duran':['duran_v1_scanA','duran_v2_scanA'],
           'ixtlilxochitl':['ixtl_B0'],
           'mendieta':['mendieta_scanA'],
           'tezozomoc':['tezozomoc_scanB'],
           'torquemada':['torquemada_v1','torquemada_v2']}

rows=[r for r in csv.DictReader(open('quantities.tsv'),delimiter='\t')]
for r in rows: r['value']=int(r['value'])

def vals(w, minv=2000, person=True):
    f=PRIMARY[w]
    return {r['value'] for r in rows if r['text'] in f and r['value']>=minv
            and r['value']<10_000_000 and (r['subject']=='person' or not person)}

V={w:vals(w) for w in PRIMARY}
print("=== (A) distinct person-quantities >= 2000 per chronicler ===")
for w in PRIMARY: print(f"  {w:15s} {len(V[w]):3d}  {sorted(V[w])}")

print("\n=== pairwise shared values (Jaccard) ===")
for a,b in itertools.combinations(PRIMARY,2):
    inter=V[a]&V[b]; uni=V[a]|V[b]
    print(f"  {a:14s} x {b:14s} shared={len(inter):2d}/{len(uni):3d}  J={len(inter)/len(uni):.3f}  {sorted(inter)}")

allv=collections.Counter()
for w in PRIMARY:
    for v in V[w]: allv[v]+=1
print("\n=== values attested in >=3 of the 5 chroniclers ===")
for v,c in sorted(allv.items()):
    if c>=3: print(f"  {v:8d} in {c} chroniclers")

print("\n=== how many of those are VIG\\DEC (div 400, not div 1000)? ===")
for v,c in sorted(allv.items()):
    if c>=3 and v%400==0 and v%1000!=0: print(f"  {v:8d} in {c} chroniclers  <-- vigesimally round, decimally odd")

# ---------- (B) null model for the four-part breakdown ----------
print("\n=== (B) Ixtlilxochitl's breakdown: 16000 / 24000 / 16000 / 24400 ===")
obs=[16000,24000,16000,24400]
print("  sum =",sum(obs), "| all div 400:", all(x%400==0 for x in obs),
      "| n div 8000:", sum(x%8000==0 for x in obs))

# empirical pool: every person-quantity in [2000, 40000] reported anywhere in the
# corpus EXCEPT the breakdown itself and except Ixtlilxochitl's own chapter LX.
pool=[r['value'] for r in rows if r['subject']=='person' and 2000<=r['value']<=40000
      and r['value'] not in (24400,)]
pool=[v for v in pool]
print(f"  empirical pool size = {len(pool)}, distinct = {len(set(pool))}")
emp_div400=sum(1 for v in pool if v%400==0)/len(pool)
emp_div8000=sum(1 for v in pool if v%8000==0)/len(pool)
print(f"  pool P(div 400) = {emp_div400:.4f}   P(div 8000) = {emp_div8000:.4f}")

random.seed(20260924)
N=1_000_000
hit=0
for _ in range(N):
    d=[random.choice(pool) for _ in range(4)]
    if all(x%400==0 for x in d) and sum(x%8000==0 for x in d)>=3: hit+=1
print(f"  MC P(all four div400 AND >=3 div8000 | empirical pool) = {hit}/{N} = {hit/N:.6g}")

# analytic, treating draws as independent with the pool's marginals
import math
p400,p8000=emp_div400,emp_div8000
# P(all div400 and >=3 div8000): since div8000 => div400 (8000 = 20*400), condition:
# choose which >=3 are div8000; the remainder must be div400-but-not-8000
q=p400-p8000
an=sum(math.comb(4,k)*p8000**k*q**(4-k) for k in (3,4))
print(f"  analytic (independent marginals)                    = {an:.6g}")

# stricter, exactly-as-observed: 3 x div8000 + 1 x (div400 not div8000)
an2=math.comb(4,3)*p8000**3*q
print(f"  analytic, exactly 3 xiquipilli + 1 non-xiquipilli    = {an2:.6g}")
