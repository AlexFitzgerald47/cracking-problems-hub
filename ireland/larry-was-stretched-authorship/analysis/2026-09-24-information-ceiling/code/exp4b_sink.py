#!/usr/bin/env python3
"""EXPERIMENT 4b -- is condition B distinguishable from chance, and where do
its predictions go?

Two corrections to the naive reading of exp4:

 1. The unit of independence is the SONG, not the (song x prose-window x
    hyperparameter) cell. Exp4's n=180 for condition B is 15 songs measured 12
    times. The binomial test below uses 15.
 2. PRACTICES rule 2: concentration of predictions on one candidate is the
    signature of a dead channel, so tabulate the sink and compare it with a
    matched no-signal null rather than reading accuracy alone.
"""
import json, sys, os, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens
from exp4_register_gap import (AUTHORS, by_a, prose, classify, prose_profiles, K)
from math import comb

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = random.Random(99)

REPS, MFW, METRIC = 40, 100, 'cosine'
per_song = defaultdict(list)
sink = Counter()
for _ in range(REPS):
    prof = prose_profiles(rng)
    for a in AUTHORS:
        for s in by_a[a]:
            pred, _ = classify(tokens(s['text']), prof, MFW, METRIC)
            per_song[(a, s['title'])].append(pred == a)
            sink[pred] += 1

print(f"condition B, {METRIC} MFW={MFW}, {REPS} prose-window draws")
print(f"songs: {len(per_song)}   k = {K}, chance = {1/K:.3f}\n")
print("per-song rate of correct attribution (unit of independence = song):")
maj = 0
for (a, t), v in sorted(per_song.items()):
    r = sum(v)/len(v)
    maj += r > 0.5
    print(f"   {a:18s} {t[:34]:34s} {r:5.2f}")
print(f"\nsongs attributed correctly in a MAJORITY of draws: {maj}/{len(per_song)}")

n, x, p0 = len(per_song), maj, 1/K
pval = sum(comb(n, i)*p0**i*(1-p0)**(n-i) for i in range(x, n+1))
print(f"exact binomial, H0: p = {p0:.3f}   P(X >= {x}) = {pval:.3f}")

print("\nsink -- where every prediction went (all authors' songs pooled):")
tot = sum(sink.values())
for a, c in sink.most_common():
    print(f"   {a:18s} {c:5d}  {c/tot:5.1%}")
print(f"   (a flat channel would put {1/K:.1%} on each; the largest sink here"
      f" holds {max(sink.values())/tot:.1%})")

json.dump({'per_song': {f'{a}|{t}': sum(v)/len(v) for (a, t), v in per_song.items()},
           'majority_correct': maj, 'n_songs': n, 'binom_p': pval,
           'sink': dict(sink)},
          open(f'{S}/results/exp4b_sink.json', 'w'), indent=1)
