#!/usr/bin/env python3
"""Shared-n-gram filiation test between chronicle passages, with a null built
from random same-length windows of the same two texts.

Calibration targets (relationships already established in the literature):
  Duran  <-> Tezozomoc   : both descend from the lost 'Cronica X' (Barlow 1945)
  Mendieta <-> Torquemada: Torquemada's dependence on Mendieta (Icazbalceta 1870)
If the method recovers these, it can be trusted on the untested pairs.
"""
import re, sys, random, unicodedata, itertools, statistics

def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
    s=s.lower()
    s=re.sub(r'-\s*\n\s*','',s)
    s=re.sub(r'[^a-z0-9 ]',' ',s)
    # collapse common early-modern / OCR orthographic variation
    s=s.replace('qu','k').replace('c','k').replace('q','k')
    s=s.replace('v','u').replace('b','u').replace('z','s').replace('x','s').replace('j','s')
    s=s.replace('y','i').replace('h','').replace('ll','l').replace('rr','r')
    s=re.sub(r'(.)\1+',r'\1',s)
    return re.sub(r'\s+',' ',s).strip()

def words(path):
    return norm(open(path,encoding='utf-8',errors='replace').read()).split()

def grams(ws,n=5):
    return set(tuple(ws[i:i+n]) for i in range(len(ws)-n+1))

def overlap(a,b,n=5):
    ga,gb=grams(a,n),grams(b,n)
    if not ga or not gb: return 0.0,0
    inter=ga&gb
    return len(inter)/min(len(ga),len(gb)), len(inter)

def window(ws,center,half):
    return ws[max(0,center-half):center+half]

def find(ws,phrase):
    p=norm(phrase).split()
    for i in range(len(ws)-len(p)+1):
        if ws[i:i+len(p)]==p: return i
    return None

if __name__=='__main__':
    random.seed(20260924)
    TEXTS={
      'duran':      'raw/duran_v1_scanA.txt',
      'tezozomoc':  'raw/tezozomoc_scanB.txt',
      'mendieta':   'raw/mendieta_scanA.txt',
      'torquemada': 'raw/torquemada_v1.txt',
      'ixtlilxochitl':'raw/ixtl_B0.txt',
    }
    W={k:words(v) for k,v in TEXTS.items()}
    for k in W: print(f"{k}: {len(W[k])} normalised tokens")

    # anchors: a distinctive phrase inside each chronicler's dedication passage
    ANCH={
     'duran':       'turo este sacrificio quatro dias arreo',
     'tezozomoc':   'duro las muertes y cruel carniceria',
     'mendieta':    'se sacrificaron ochenta mil y cuatrocientas personas',
     'torquemada':  'fueron ochenta mil',
     'ixtlilxochitl':'ochenta mil y cuatrocientos hombres en este modo',
    }
    POS={}
    for k,p in ANCH.items():
        i=find(W[k],p); POS[k]=i
        print(f"anchor {k}: {'FOUND at '+str(i) if i is not None else 'NOT FOUND'}")

    HALF=1200   # ~2400-token window around each anchor
    WIN={k:window(W[k],POS[k],HALF) for k in POS if POS[k] is not None}

    print("\n=== 5-gram overlap between dedication windows, vs null of random windows ===")
    for a,b in itertools.combinations(sorted(WIN),2):
        obs,ni=overlap(WIN[a],WIN[b])
        null=[]
        for _ in range(300):
            ca=random.randrange(HALF,len(W[a])-HALF)
            cb=random.randrange(HALF,len(W[b])-HALF)
            o,_=overlap(window(W[a],ca,HALF),window(W[b],cb,HALF))
            null.append(o)
        mu=statistics.mean(null); sd=statistics.pstdev(null) or 1e-12
        z=(obs-mu)/sd
        p=(sum(1 for x in null if x>=obs)+1)/(len(null)+1)
        star='   <<<' if p<=0.01 else ''
        print(f"  {a:14s} x {b:14s} obs={obs:.5f} ({ni:4d} shared 5-grams)  null mu={mu:.5f} sd={sd:.5f}  z={z:6.1f}  p={p:.4f}{star}")
