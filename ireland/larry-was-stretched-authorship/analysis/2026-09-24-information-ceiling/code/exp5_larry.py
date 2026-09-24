#!/usr/bin/env python3
"""EXPERIMENT 5 -- rank "The Night Before Larry Was Stretched" against the
candidates' attested writing, and test the frozen stability prediction.

FREEZE.md, written before this was run, predicted: conditional on the register
channel being dead (exp4: cross-register accuracy 0.232 vs chance 0.200, 2/15
songs majority-correct, binomial p = 0.833), the top-ranked candidate for Larry
will NOT be stable across the metric x MFW grid -- more than one distinct
winner across the eight cells. A single winner everywhere would falsify the
session's negative conclusion.
"""
import json, sys, os, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens, DIST

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cands = json.load(open(f'{S}/corpus/larry_candidates.json'))
farmer = open(f'{S}/corpus/larry_farmer.txt').read()
us = open(f'{S}/corpus/candidates/larry_universalsongster1828.txt').read()

CAP = 8000
rng = random.Random(1789)

def vec(seq, mfw):
    c = Counter(seq); n = len(seq) or 1
    return [c[w]/n for w in mfw]

def zfit(vs):
    m, s = [], []
    for j in range(len(vs[0])):
        col = [v[j] for v in vs]
        mu = sum(col)/len(col)
        var = sum((x-mu)**2 for x in col)/len(col)
        m.append(mu); s.append(var**0.5 if var > 0 else 1e-12)
    return m, s

def zz(v, m, s):
    return [(v[j]-m[j])/s[j] for j in range(len(v))]

def rank(test, profiles, n_mfw, metric):
    cnt = Counter()
    for t in profiles.values():
        cnt.update(t)
    mfw = [w for w, _ in cnt.most_common(n_mfw)]
    pv = {a: vec(t, mfw) for a, t in profiles.items()}
    scale = list(pv.values())
    for a, t in profiles.items():
        h = len(t)//2
        scale.append(vec(t[:h], mfw)); scale.append(vec(t[h:], mfw))
    m, s = zfit(scale)
    prof = {a: zz(v, m, s) for a, v in pv.items()}
    q = zz(vec(test, mfw), m, s)
    return {a: DIST[metric](q, p) for a, p in prof.items()}

def cap(t, n=CAP):
    tk = tokens(t)
    if len(tk) <= n:
        return tk
    st = rng.randrange(0, len(tk)-n)
    return tk[st:st+n]

SETS = {
  'all three with attested text (oratory / sermons / verse)':
      ['Curran (oratory)', 'Burrowes (sermons)', 'Lysaght (verse)'],
  'verse only -- the one register-homogeneous comparison':
      ['Curran (verse)', 'Lysaght (verse)'],
}

out = {}
for label, keys in SETS.items():
    print(f"\n=== {label} ===")
    winners = Counter()
    rows = []
    for metric in ('cosine', 'burrows'):
        for n_mfw in (50, 100, 200, 300):
            prof = {k: cap(cands[k]) for k in keys}
            if 'Curran (verse)' in prof:
                # a 339-word profile cannot be capped up; match the other side
                prof = {k: (tokens(cands[k])[:339] if k != 'Curran (verse)'
                            else tokens(cands[k])) for k in keys}
            d = rank(tokens(farmer), prof, n_mfw, metric)
            w = min(d, key=d.get)
            winners[w] += 1
            rows.append({'metric': metric, 'mfw': n_mfw, 'winner': w,
                         'dists': {k: round(v, 4) for k, v in d.items()}})
            print(f"  {metric:8s} MFW={n_mfw:4d} -> {w:22s}  " +
                  "  ".join(f"{k.split(' ')[0]}={v:.3f}" for k, v in sorted(d.items())))
    print(f"  distinct winners across the 8 cells: {len(winners)}  {dict(winners)}")
    out[label] = {'rows': rows, 'winners': dict(winners), 'n_distinct': len(winners)}

# --- witness distance: is transmission noise comparable to candidate spacing?
print("\n=== witness check: Farmer 1896 vs Universal Songster 1828 ===")
keys = ['Curran (oratory)', 'Burrowes (sermons)', 'Lysaght (verse)']
prof = {k: cap(cands[k]) for k in keys}
for metric in ('cosine', 'burrows'):
    prof2 = dict(prof); prof2['LARRY (Universal Songster 1828)'] = tokens(us)
    d = rank(tokens(farmer), prof2, 100, metric)
    dl = d.pop('LARRY (Universal Songster 1828)')
    print(f"  {metric:8s}: Farmer-vs-UniversalSongster = {dl:.3f} | "
          f"nearest candidate = {min(d.values()):.3f} ({min(d, key=d.get)})")
    out[f'witness_{metric}'] = {'between_witness': dl,
                                'nearest_candidate': min(d.values()),
                                'nearest_name': min(d, key=d.get)}

json.dump(out, open(f'{S}/results/exp5_larry.json', 'w'), indent=1)
