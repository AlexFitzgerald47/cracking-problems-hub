#!/usr/bin/env python3
"""EXPERIMENT 6 -- is "Lysaght wins" a fact about Larry, or about the profiles?

Exp 5's register-homogeneous test (Curran's 339 words of verse vs an equal
slice of Lysaght's verse) gave Lysaght in all 8 metric x MFW cells. A stable
winner looks like a result. PRACTICES rule 2 says test it as a sink: feed the
SAME two profiles a set of songs that neither man wrote and see who wins.

If Lysaght also wins for songs of known, different authorship, then "Lysaght"
is where this comparison sends everything and Larry's result carries no
information about Larry.

Also re-runs the exp5 ranking on the second Larry witness (Universal Songster
1828), to check whether the two printings rank the candidates the same way.
"""
import json, sys, os
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens
from exp5_larry import rank, cands, farmer, us, cap

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
songs = json.load(open(f'{S}/corpus/musa_songs.json'))

cv = tokens(cands['Curran (verse)'])
lv = tokens(cands['Lysaght (verse)'])[:len(cv)]
prof2 = {'Curran (verse)': cv, 'Lysaght (verse)': lv}

print(f"profiles: Curran {len(cv)} words vs Lysaght {len(lv)} words (matched)\n")
print("Feeding the same two profiles every named-author song in Musa Pedestris")
print("-- none of which was written by Curran or Lysaght:\n")

tally = Counter()
per_song = []
for s in songs:
    if not s['author'] or s['author'] == 'Anon' or s['n_words'] < 100:
        continue
    wins = Counter()
    for metric in ('cosine', 'burrows'):
        for n_mfw in (50, 100, 200, 300):
            d = rank(tokens(s['text']), prof2, n_mfw, metric)
            wins[min(d, key=d.get)] += 1
    top = wins.most_common(1)[0][0]
    tally[top] += 1
    per_song.append({'title': s['title'], 'author': s['author'],
                     'majority_winner': top, 'lysaght_cells': wins['Lysaght (verse)']})

n = len(per_song)
ly = tally['Lysaght (verse)']
print(f"  songs tested: {n}")
for a, c in tally.most_common():
    print(f"    majority winner {a:18s}: {c:3d}  ({c/n:.1%})")
allcells = sum(p['lysaght_cells'] for p in per_song)
print(f"  Lysaght wins {allcells}/{n*8} = {allcells/(n*8):.1%} of all cells")
print(f"\n  Larry (Farmer 1896) gave Lysaght 8/8 cells.")
print(f"  Songs by other authors give Lysaght {allcells/(n*8):.1%} of cells on average,")
print(f"  and Lysaght is the majority winner for {ly}/{n} of them.")

# --- second witness
print("\n=== does the second Larry witness rank the same way? ===")
keys = ['Curran (oratory)', 'Burrowes (sermons)', 'Lysaght (verse)']
prof3 = {k: cap(cands[k]) for k in keys}
for name, txt in (('Farmer 1896', farmer), ('Universal Songster 1828', us)):
    w = Counter()
    for metric in ('cosine', 'burrows'):
        for n_mfw in (50, 100, 200, 300):
            d = rank(tokens(txt), prof3, n_mfw, metric)
            w[min(d, key=d.get)] += 1
    print(f"  {name:26s}: {dict(w)}")

json.dump({'tally': dict(tally), 'n': n, 'lysaght_cell_rate': allcells/(n*8),
           'per_song': per_song},
          open(f'{S}/results/exp6_sink_null.json', 'w'), indent=1)
