#!/usr/bin/env python3
"""Content-level (not wording-level) filiation: overlap of RARE tokens --
mostly Nahuatl proper nouns and toponyms -- between the dedication windows,
against a null of random same-length windows.

Motivated by the failure of the 5-gram test to recover the established
Duran/Tezozomoc relationship: they are independent Spanish translations of a
lost Nahuatl source, so they share episodes and names but not phrasing.
"""
import re,random,itertools,statistics,collections
from parallels import norm, words, window, find

random.seed(20260924)
TEXTS={'duran':'raw/duran_v1_scanA.txt','tezozomoc':'raw/tezozomoc_scanB.txt',
       'mendieta':'raw/mendieta_scanA.txt','torquemada':'raw/torquemada_v1.txt',
       'ixtlilxochitl':'raw/ixtl_B0.txt'}
W={k:words(v) for k,v in TEXTS.items()}

# corpus-wide document frequency: a token is "rare" if it occurs in few texts
# and is long enough to be a name rather than a function word
DF=collections.Counter()
for k in W: DF.update(set(W[k]))
GLOBAL=collections.Counter()
for k in W: GLOBAL.update(W[k])
def rare(ws):
    return {t for t in ws if len(t)>=6 and GLOBAL[t]<=60}

ANCH={'duran':'turo este sacrificio quatro dias arreo',
      'tezozomoc':'duro las muertes y cruel carniceria',
      'mendieta':'se sacrificaron ochenta mil y cuatrocientas personas',
      'torquemada':'fueron ochenta mil',
      'ixtlilxochitl':'ochenta mil y cuatrocientos hombres en este modo'}
HALF=1200
POS={k:find(W[k],p) for k,p in ANCH.items()}
WIN={k:window(W[k],POS[k],HALF) for k in POS}

def jac(a,b):
    ra,rb=rare(a),rare(b)
    if not ra or not rb: return 0.0,0
    return len(ra&rb)/min(len(ra),len(rb)), len(ra&rb)

print("=== rare-token (name-level) overlap of the dedication windows ===")
print(f"{'pair':32s} {'obs':>7s} {'shared':>7s} {'null mu':>8s} {'sd':>7s} {'z':>6s} {'p':>7s}")
res={}
for a,b in itertools.combinations(sorted(WIN),2):
    obs,ni=jac(WIN[a],WIN[b])
    null=[]
    for _ in range(500):
        ca=random.randrange(HALF,len(W[a])-HALF); cb=random.randrange(HALF,len(W[b])-HALF)
        o,_=jac(window(W[a],ca,HALF),window(W[b],cb,HALF)); null.append(o)
    mu=statistics.mean(null); sd=statistics.pstdev(null) or 1e-12
    p=(sum(1 for x in null if x>=obs)+1)/(len(null)+1)
    res[(a,b)]=(obs,ni,mu,sd,(obs-mu)/sd,p)
    print(f"  {a:14s}x{b:14s} {obs:7.4f} {ni:7d} {mu:8.4f} {sd:7.4f} {(obs-mu)/sd:6.1f} {p:7.4f}"
          + ('   <<<' if p<=0.01 else ''))

print("\n=== shared rare tokens, Duran x Tezozomoc dedication windows ===")
print(sorted(rare(WIN['duran']) & rare(WIN['tezozomoc'])))
print("\n=== shared rare tokens, Duran x Ixtlilxochitl ===")
print(sorted(rare(WIN['duran']) & rare(WIN['ixtlilxochitl'])))
print("\n=== shared rare tokens, Mendieta x Torquemada ===")
print(sorted(rare(WIN['mendieta']) & rare(WIN['torquemada']))[:40])
