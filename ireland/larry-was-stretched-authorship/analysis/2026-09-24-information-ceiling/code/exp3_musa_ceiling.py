#!/usr/bin/env python3
"""EXPERIMENT 3 -- the genre-matched information ceiling.

Can a single canting song of Larry's length be attributed to its author at all,
when the candidate profiles are built from canting songs of the same period?

Farmer's *Musa Pedestris* (1896) supplies the only author-labelled, genre- and
register-matched corpus that exists for this question: 78 canting songs,
1536-1896, each bylined by Farmer with an author and a date. Authors with two
or more songs give a leave-one-song-out attribution test in exactly the regime
"The Night Before Larry Was Stretched" sits in.

Null model: the same procedure with author labels permuted across songs
(the songs, their lengths and the candidate-set structure are held fixed;
only the author labels move). 1000 draws.
"""
import json, sys, os, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import *

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
songs = json.load(open(f'{S}/corpus/musa_songs.json'))

# "Anon" is not an author: it is Farmer's label for songs of unknown authorship
# and pooling them would build a profile out of a dozen different hands.
named = [s for s in songs if s['author'] and s['author'] != 'Anon']
by_a = defaultdict(list)
for s in named:
    by_a[s['author']].append(s)
multi = {a: v for a, v in by_a.items() if len(v) >= 2}

print(f"named-author songs: {len(named)}   authors: {len(by_a)}")
print(f"authors with >=2 songs: {len(multi)}")
tot_w = 0
for a in sorted(multi, key=lambda x: -sum(s['n_words'] for s in multi[x])):
    w = sum(s['n_words'] for s in multi[a])
    tot_w += w
    print(f"   {a:22s} {len(multi[a])} songs  {w:5d} words   "
          f"(train per test song: {w - max(s['n_words'] for s in multi[a])}-"
          f"{w - min(s['n_words'] for s in multi[a])})")
print(f"   TOTAL {tot_w} words in the testable set\n")

units = [(a, s['text']) for a in multi for s in multi[a]]

def score(units, n_mfw, metric):
    n, c, cases, k = attribute_loo(units, n_mfw=n_mfw, metric=metric)
    return c, n, k, cases

results = {}
for metric in ('cosine', 'burrows'):
    for n_mfw in (50, 100, 200):
        c, n, k, cases = score(units, n_mfw, metric)
        results[f'{metric}_{n_mfw}'] = {'correct': c, 'n': n, 'k': k, 'acc': c/n}
        print(f"observed  {metric:8s} MFW={n_mfw:3d}:  {c}/{n} = {c/n:.3f}   "
              f"(k={k} candidates, chance = {1/k:.3f})")

# ---- null model: permute author labels, keep song set and structure fixed
print("\nnull model -- author labels permuted across the same songs, 1000 draws")
BEST = ('cosine', 100)
rng = random.Random(20260924)
labels = [a for a, _ in units]
texts = [t for _, t in units]
null = []
for d in range(1000):
    perm = labels[:]
    rng.shuffle(perm)
    pu = list(zip(perm, texts))
    n, c, _, _ = attribute_loo(pu, n_mfw=BEST[1], metric=BEST[0])
    null.append(c/n if n else 0.0)
null.sort()
obs = results[f'{BEST[0]}_{BEST[1]}']['acc']
mean = sum(null)/len(null)
sd = (sum((x-mean)**2 for x in null)/len(null))**0.5
p = sum(1 for x in null if x >= obs)/len(null)
print(f"  observed              {obs:.3f}")
print(f"  null mean +/- sd      {mean:.3f} +/- {sd:.3f}")
print(f"  null 95th percentile  {null[int(0.95*len(null))]:.3f}")
print(f"  p(null >= observed)   {p:.3f}")

json.dump({'results': results,
           'null': {'mean': mean, 'sd': sd, 'p': p,
                    'pct95': null[int(0.95*len(null))], 'draws': len(null)}},
          open(f'{S}/results/exp3_musa_ceiling.json', 'w'), indent=1)
