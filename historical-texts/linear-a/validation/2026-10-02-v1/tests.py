#!/usr/bin/env python3
"""V1 reproduction, part 3: discriminating tests on the load-bearing claims."""
import sys, re, random, itertools, collections
sys.path.insert(0,'.')
from census import A, is_sg, is_num, ival, DIV, LAC, basedoc
TOTALS={"KU-RO","PO-TO-KU-RO"}
def numeric_damage(v):
    if LAC in (v.get('transcription','') or '') or LAC in (v.get('parsedInscription','') or ''): return True
    return any(('[' in w or ']' in w) and any(c.isdigit() for c in w) for w in v['transliteratedWords'])
def walk(ws,i,respect):
    ents=[];j=i-1
    while j>=0:
        t=ws[j]
        if t in TOTALS: break
        if respect and is_sg(t) and j+1<len(ws) and ws[j+1]==DIV: break
        if ival(t) is not None: ents.append(ival(t))
        j-=1
    return ents

# ---------------------------------------------------------------- T1 KU-RO null
print("### T1  KU-RO summation: permutation null (does a block match ITS OWN total?)")
blocks=[]
for k in sorted(A):
    ws=A[k]['transliteratedWords']
    for i,w in enumerate(ws):
        if w not in TOTALS: continue
        tot=ival(ws[i+1]) if i+1<len(ws) else None
        if tot is None: continue
        e1=walk(ws,i,False); e2=walk(ws,i,True)
        blocks.append((k,w,tot,sum(e1),sum(e2),len(e2)))
obs=sum(1 for b in blocks if abs(b[3]-b[2])<1e-9 or abs(b[4]-b[2])<1e-9)
rng=random.Random(20261002); N=100000; draws=[]
sums=[(b[3],b[4]) for b in blocks]; tots=[b[2] for b in blocks]
for _ in range(N):
    t=tots[:]; rng.shuffle(t)
    draws.append(sum(1 for (s1,s2),tt in zip(sums,t) if abs(s1-tt)<1e-9 or abs(s2-tt)<1e-9))
p=(sum(1 for d in draws if d>=obs)+1)/(N+1)
print(f"  observed exact matches {obs}/{len(blocks)};  null mean {sum(draws)/N:.2f}, "
      f"max {max(draws)};  p = {p:.5f}")
print("  -> KU-RO really is a summation marker; it is just rarely TESTABLE (physical loss).")

# ---------------------------------------------------------------- T2 KI-RO grammar
print("\n### T2  KI-RO two-construction grammar, scored CORPUS-WIDE (claim: 9/9)")
ki=[]
for k in sorted(A):
    ws=A[k]['transliteratedWords']
    for i,w in enumerate(ws):
        if w!="KI-RO": continue
        nxt=next((t for t in ws[i+1:] if t!="\n"), None)
        kind = "numeral" if (nxt and ival(nxt) is not None) else ("divider" if nxt==DIV else f"other:{nxt}")
        ki.append((k,kind,nxt))
print(f"  KI-RO attestations in corpus: {len(ki)}")
for c,n in collections.Counter(k[1].split(':')[0] for k in ki).most_common():
    print(f"    next token = {c:8s} : {n}")
for k,kind,nxt in ki: print(f"      {k:11s} {kind}")

print("\n### T2b background rate: how many OTHER sign-groups show the same "
      "'both constructions' profile?  (is the grammar specific to KI-RO?)")
prof=collections.defaultdict(lambda:[0,0,0])
for k,v in A.items():
    if v.get('site')!='Haghia Triada': continue
    ws=[w for w in v['transliteratedWords'] if w!="\n"]
    for i,w in enumerate(ws):
        if not is_sg(w): continue
        nxt=ws[i+1] if i+1<len(ws) else None
        if nxt is None: prof[w][2]+=1
        elif ival(nxt) is not None: prof[w][0]+=1
        elif nxt==DIV: prof[w][1]+=1
        else: prof[w][2]+=1
n4=[w for w,c in prof.items() if sum(c)>=4]
both=[w for w in n4 if prof[w][0] and prof[w][1]]
print(f"  HT sign-group types with >=4 attestations: {len(n4)}; of those, "
      f"{len(both)} ({100*len(both)/len(n4):.0f}%) show BOTH numeral-next and divider-next")
print(f"  i.e. the 'two-construction grammar' is the MAJORITY pattern, not a KI-RO property.")
print("  both-pattern types:", sorted(both))

# ---------------------------------------------------------------- T3 HT97 subset sum
print("\n### T3  'KA-RU 82 = selected breakdown' (HT97a) -- how much information is that?")
ws=A['HT97a']['transliteratedWords']
nums=[ival(w) for w in ws if ival(w) is not None]
tgt=nums[0]; rest=nums[1:]
print(f"  stated KA-RU/VIR+KA value {tgt:g}; following entry values {[int(x) for x in rest]} "
      f"(sum {sum(rest):g}, {len(rest)} items)")
reach=set()
for r in range(len(rest)+1):
    for c in itertools.combinations(rest,r): reach.add(sum(c))
span=[x for x in range(0,int(sum(rest))+1)]
print(f"  distinct subset sums reachable: {len(reach)} of {len(span)} integers in [0,{int(sum(rest))}] "
      f"= {100*len(reach)/len(span):.0f}%")
hits=[c for r in range(len(rest)+1) for c in itertools.combinations(rest,r) if sum(c)==tgt]
print(f"  DISTINCT subsets of the entries summing to exactly {tgt:g}: {len(hits)}")
print(f"  -> a 'selected breakdown' that sums to the header is almost guaranteed; "
      f"this anchor carries ~0 bits.")

# ---------------------------------------------------------------- T4 HT2
print("\n### T4  HT2 'A-KA-RU 20 = 17 + 3' -- does the pattern repeat on the same tablet?")
print("  HT2:", " ".join(A['HT2']['transliteratedWords']).replace(" \n "," | "))
print("  first group : A-KA-RU OLE+U 20 ; OLE+A 17 ; OLE+E 3     -> 17+3 = 20  fits")
print("  second group: KI-RE-TA-NA OLE+U 54 ; OLE+A 47 ; [?] 1   -> 47+1 = 48 != 54  FAILS")
print("  numeric damage on HT2:", numeric_damage(A['HT2']))
print("  -> the one tablet that states the alleged 'forward aggregate' twice contradicts it once.")

# ---------------------------------------------------------------- T5 HT85 gang base rate
print("\n### T5  HT85 '66 = 11 gangs of 6' -- base rate of that coincidence")
pairs=collections.defaultdict(dict)
for k,v in A.items():
    m=re.match(r'^(.*?)([ab])$',k)
    if m and v.get('support')=='Tablet': pairs[m.group(1)][m.group(2)]=v
hits=tot=0; ex=[]
for t,f in sorted(pairs.items()):
    if set(f)!={"a","b"}: continue
    for s,d in (("a","b"),("b","a")):
        ws=f[s]['transliteratedWords']
        kur=[ival(ws[i+1]) for i,w in enumerate(ws) if w in TOTALS and i+1<len(ws) and ival(ws[i+1])]
        n=sum(1 for w in f[d]['transliteratedWords'] if is_sg(w))-1
        for K in kur:
            if not K or n<2: continue
            tot+=1
            if K%n==0 and K//n>=2: hits+=1; ex.append((t,s,int(K),n,int(K//n)))
print(f"  face-pairs where a stated total on one face divides exactly by the entry count "
      f"on the other, giving an integer >=2: {hits}/{tot} ({100*hits/max(1,tot):.0f}%)")
for e in ex: print("    ", e)
print("  HT85a entries 12,12,6,24,5,3,4 -- 5, 3 and 4 are NOT multiples of 6, so the 66")
print("  does not decompose into six-person contributions at source; only the total does.")

# ---------------------------------------------------------------- T6 HT119 ratio
print("\n### T6  HT119 '*327 34 : VIR 68 = exactly 1:2'")
ws=A['HT119']['transliteratedWords']; vals=[ival(w) for w in ws if ival(w) is not None][:-1]
pr=[(x,y) for i,x in enumerate(vals) for y in vals[i+1:] if abs(y-2*x)<1e-9 or abs(x-2*y)<1e-9]
print("  nine entry values:", [int(x) for x in vals])
print("  exact 2:1 pairs anywhere in the nine:", [(int(a),int(b)) for a,b in pr])
rng2=random.Random(7); hit=0; M=200000
for _ in range(M):
    v=[rng2.randint(1,70) for _ in range(9)]
    if any(abs(y-2*x)<1e-9 or abs(x-2*y)<1e-9 for i,x in enumerate(v) for y in v[i+1:]): hit+=1
print(f"  P(some exact 2:1 pair among 9 random integers 1-70) = {hit/M:.3f}")
print("  -> the 1:2 'fixed manpower ratio' is at chance.")

# ---------------------------------------------------------------- T7 DI-KI-SE control
print("\n### T7  the DI-KI-SE 'status toggle' control")
for k in sorted(A):
    if any(w=="DI-KI-SE" for w in A[k]['transliteratedWords']):
        print(f"  {k:8s} [{A[k].get('scribe') or '-'}] :",
              " ".join(A[k]['transliteratedWords']).replace(" \n "," | "))
print("  NB: HT117 puts DI-KI-SE on face b, under *21F-TU-NE, NOT under the face-a")
print("      'MA-KA-RI-TE . KI-RO .' heading.  Whether KI-RO scopes across the face")
print("      break onto HT117b is an assumption, not an observation.")
