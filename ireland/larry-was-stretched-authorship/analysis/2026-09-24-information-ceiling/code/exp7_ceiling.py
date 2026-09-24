#!/usr/bin/env python3
"""EXPERIMENT 7 -- the information ceiling, in the form PRACTICES specifies.

PRACTICES: d'_ceiling(A,B) = |mu(A) - mu(B)| / sqrt(sigma(A)^2 + sigma(B)^2),
and the Junius comparison: same-author CROSS-register distance against
different-author SAME-register distance. If the register displacement is
larger than the author displacement, a ranking that crosses the gap is
measuring the gap.

Measured over the five authors attested in both canting song and prose.
All distances are computed in one common z-space so they are comparable.
"""
import json, sys, os, random, statistics
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens, DIST
from exp4_register_gap import AUTHORS, by_a, prose

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = random.Random(1787)
CHUNK = 470        # Larry's length, so every unit is comparable to Larry

def chunks(toks, n=CHUNK, maxc=12):
    out = []
    for i in range(0, len(toks)-n+1, n):
        out.append(toks[i:i+n])
        if len(out) >= maxc:
            break
    return out

units = []          # (author, register, tokens)
for a in AUTHORS:
    for s in by_a[a]:
        t = tokens(s['text'])
        if len(t) >= 150:
            units.append((a, 'song', t))
    pt = tokens(prose[a])
    st = rng.randrange(0, max(1, len(pt)-CHUNK*12))
    for c in chunks(pt[st:]):
        units.append((a, 'prose', c))

# one common z-space over every unit
cnt = Counter()
for _, _, t in units:
    cnt.update(t)
MFW = [w for w, _ in cnt.most_common(100)]
def vec(t):
    c = Counter(t); n = len(t)
    return [c[w]/n for w in MFW]
V = [vec(t) for _, _, t in units]
m = [sum(v[j] for v in V)/len(V) for j in range(len(MFW))]
sd = [max((sum((v[j]-m[j])**2 for v in V)/len(V))**0.5, 1e-12) for j in range(len(MFW))]
Z = [[(v[j]-m[j])/sd[j] for j in range(len(MFW))] for v in V]

D = DIST['burrows']
same_auth_cross_reg, diff_auth_same_reg, same_auth_same_reg, diff_auth_cross_reg = [], [], [], []
for i in range(len(units)):
    for j in range(i+1, len(units)):
        ai, ri, _ = units[i]; aj, rj, _ = units[j]
        d = D(Z[i], Z[j])
        if ai == aj and ri != rj:   same_auth_cross_reg.append(d)
        elif ai != aj and ri == rj: diff_auth_same_reg.append(d)
        elif ai == aj and ri == rj: same_auth_same_reg.append(d)
        else:                       diff_auth_cross_reg.append(d)

def rep(name, v):
    print(f"  {name:38s} n={len(v):5d}  mean {statistics.mean(v):.3f}  sd {statistics.pstdev(v):.3f}")
    return statistics.mean(v), statistics.pstdev(v)

print(f"Burrows's Delta over {len(units)} units of {CHUNK} words, one common z-space")
print(f"({sum(1 for u in units if u[1]=='song')} canting-song units, "
      f"{sum(1 for u in units if u[1]=='prose')} prose units, {len(AUTHORS)} authors)\n")
a1 = rep("same author, SAME register", same_auth_same_reg)
a2 = rep("same author, CROSS register", same_auth_cross_reg)
b1 = rep("different author, SAME register", diff_auth_same_reg)
b2 = rep("different author, CROSS register", diff_auth_cross_reg)

print("\nThe Junius comparison:")
print(f"  same-author cross-register   {a2[0]:.3f}")
print(f"  different-author same-register {b1[0]:.3f}")
verdict = ("GAP EXCEEDS SIGNAL -- a cross-register ranking measures the register"
           if a2[0] > b1[0] else "signal exceeds gap")
print(f"  -> {verdict}")

# author signal and register signal as d'
author_d = abs(b1[0]-a1[0]) / ((statistics.pstdev(diff_auth_same_reg)**2 +
                                statistics.pstdev(same_auth_same_reg)**2) ** 0.5)
reg_d = abs(a2[0]-a1[0]) / ((statistics.pstdev(same_auth_cross_reg)**2 +
                             statistics.pstdev(same_auth_same_reg)**2) ** 0.5)
print(f"\n  d' author  (same vs diff author, register held fixed) = {author_d:.3f}")
print(f"  d' register (same vs cross register, author held fixed) = {reg_d:.3f}")
print(f"  register effect is {reg_d/author_d:.1f}x the author effect")

json.dump({'same_auth_same_reg': a1, 'same_auth_cross_reg': a2,
           'diff_auth_same_reg': b1, 'diff_auth_cross_reg': b2,
           'd_author': author_d, 'd_register': reg_d,
           'ratio': reg_d/author_d, 'n_units': len(units), 'chunk': CHUNK},
          open(f'{S}/results/exp7_ceiling.json', 'w'), indent=1)
