#!/usr/bin/env python3
"""V1 reproduction, part 4: the label-permutation the board's cross-reference demands.
Does the Scribe-9 set cohere more than an arbitrary 10-tablet slice of the same archive?"""
import sys, re, random, collections
sys.path.insert(0,'.')
from census import A, is_sg, basedoc
def docs_of(pred):
    d={}
    for k,v in A.items():
        if not pred(v): continue
        d.setdefault(basedoc(k), set()).update(w for w in v['transliteratedWords'] if is_sg(w))
    return d
HT = docs_of(lambda v: v.get('site')=='Haghia Triada' and v.get('support')=='Tablet')
HT = {k:v for k,v in HT.items() if v}
S9 = sorted(set(basedoc(k) for k,v in A.items() if v.get('scribe')=='HT Scribe 9'))
S9 = [t for t in S9 if t in HT]
ADMIN={"KU-RO","PO-TO-KU-RO","KI-RO","KU-DA","A-DU","KA-PA","SA-RA₂","A-KA-RU","KA-RU"}
# Davis & Valerio's 19-word Haghia Triada circuit -- a CORPUS-WIDE phenomenon that is
# not a property of Scribe 9, listed verbatim from the claimant's own quotation of them.
CIRCUIT={"DA-RI-DA","PA₃-NI","PA₃-NI-NA","U-*325-ZA","U-DE-ZA","DA-SI-*118","KU-ZU-NI",
         "TE-KI","TE-KE","DA-RE","TE-TU","ME-ZA","RA-TI-SE","RE-DI-SE","WA-DU-NI-MI",
         "MA-DI","QA-*310-I","PA-DE","*306-TU","*324-DI-RA","TA-I-*123","A-RU","KU-PA₃-NU"}

def coh(tabs, drop=frozenset()):
    c=collections.Counter()
    for t in tabs:
        for w in HT[t]-drop: c[w]+=1
    sh=sorted(w for w,n in c.items() if n>=2)
    return len(sh), sh

rng=random.Random(20261002); N=50000
allt=sorted(HT); sz={t:len(HT[t]) for t in allt}
def run(label, drop):
    obs, sh = coh(S9, drop)
    tgt=sum(len(HT[t]-drop) for t in S9)
    d=[coh(rng.sample(allt,len(S9)),drop)[0] for _ in range(N)]
    p=(sum(1 for x in d if x>=obs)+1)/(N+1)
    d2=[];tr=0
    while len(d2)<5000 and tr<400000:
        tr+=1; pick=rng.sample(allt,len(S9))
        if abs(sum(len(HT[t]-drop) for t in pick)-tgt)<=0.10*max(tgt,1): d2.append(coh(pick,drop)[0])
    p2=(sum(1 for x in d2 if x>=obs)+1)/(len(d2)+1) if d2 else float('nan')
    ds=sorted(d)
    print(f"  {label}")
    print(f"    observed shared types = {obs}  {sh}")
    print(f"    unmatched null : mean {sum(d)/N:5.2f}  95% [{ds[int(.025*N)]},{ds[int(.975*N)]}]  p = {p:.4f}")
    if d2:
        d2s=sorted(d2); n2=len(d2)
        print(f"    SIZE-MATCHED null (+-10% of {tgt} types, n={n2}): mean {sum(d2)/n2:5.2f} "
              f"95% [{d2s[int(.025*n2)]},{d2s[int(.975*n2)]}]  p = {p2:.4f}")

print("### P1  Scribe-9 dossier cohesion vs. random 10-tablet slices of the SAME archive")
print(f"  pool: {len(allt)} HT tablets; Scribe-9 set = {S9}")
run("(a) all sign-groups", frozenset())
run("(b) drop the universal administrative operators", frozenset(ADMIN))
run("(c) drop operators AND the Davis-Valerio 19-node circuit words", frozenset(ADMIN|CIRCUIT))

print("\n### P2  how much of the 'dossier' is circuit vocabulary that spans the whole archive?")
sh=coh(S9)[1]
print("  shared types:", sh)
print("  of which admin operators:", [w for w in sh if w in ADMIN])
print("  of which Davis-Valerio circuit nodes:", [w for w in sh if w in CIRCUIT])
print("  residue genuinely specific to the dossier:",
      [w for w in sh if w not in ADMIN and w not in CIRCUIT])
for w in sh:
    hosts=sorted(t for t in allt if w in HT[t])
    print(f"    {w:14s} on {len(hosts):2d} HT tablets ({sum(1 for t in hosts if t in S9)} of them Scribe 9): {hosts}")

print("\n### P3  permute the 'exception' vs 'ordinary' label INSIDE Scribe 9")
exc=["HT94","HT117"]; ordn=["HT85","HT87","HT122"]
def cross(e,o):
    we=set().union(*[HT[t] for t in e]); wo=set().union(*[HT[t] for t in o]); return len(we&wo), sorted(we&wo)
obs,shx=cross(exc,ordn); pool=exc+ordn
ds=[]
for _ in range(20000):
    p=pool[:]; rng.shuffle(p); ds.append(cross(p[:2],p[2:])[0])
print(f"  observed {obs} shared {shx}; null mean {sum(ds)/len(ds):.2f}; "
      f"p = {(sum(1 for d in ds if d>=obs)+1)/(len(ds)+1):.4f}")
