#!/usr/bin/env python3
"""T18: are the zodiac labels an ordinal code at all?

Every ordinal reading of the labels — day of month, degree 1..30, planetary ruler,
decan — makes the same prediction: a small closed inventory (30, 7 or 36 items)
repeating across all twelve signs. That is a type/token statement, and it is decidable
from the corpus with no crib and no model.
"""
import sys, os, json, random, statistics, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER

rows = L.load()
z = L.ring_strings(rows)
allz = [w for k in sorted(z) for w in z[k]]
rng = random.Random(3)


def ttr(pool, n, reps=400):
    v = [len(set(rng.sample(pool, n))) / n for _ in range(reps)]
    return statistics.mean(v), (statistics.stdev(v) if len(set(v)) > 1 else 0.0)


P = [w for r in rows if r["ltype"] == "P" for w in r["words"]]
Lb = ["".join(r["words"]) for r in rows if r["ltype"] == "L" and r["words"]]
ZR = [w for r in rows if r["folio"] in ORDER and r["ltype"] == "R" for w in r["words"]]

print(f"zodiac labels: {len(allz)} tokens, {len(set(allz))} types "
      f"-> type/token {len(set(allz))/len(allz):.3f}")
print(f"  distinct last-2 glyphs : {len(set(w[-2:] for w in allz))}")
print(f"  distinct last-3 glyphs : {len(set(w[-3:] for w in allz))}")
print(f"  distinct first-2 glyphs: {len(set(w[:2] for w in allz))}\n")

out = {"zodiac_labels": len(set(allz)) / len(allz)}
for nm, pool in (("running text (P loci)", P), ("all other labels (L loci)", Lb),
                 ("zodiac ring text (R loci)", ZR)):
    m, s = ttr(pool, min(298, len(pool)))
    out[nm] = [m, s]
    sd = (len(set(allz)) / len(allz) - m) / s if s else float("inf")
    print(f"{nm:28s} 298-token sample: type/token {m:.3f} +- {s:.3f}   "
          f"zodiac labels are {sd:+.1f} SD above")

c = collections.Counter(allz)
print(f"\nrepeat spectrum across the whole zodiac section: "
      f"{dict(sorted(collections.Counter(c.values()).items()))}")
print(f"  {sum(1 for v in c.values() if v == 1)} of {len(c)} types are hapax "
      f"({sum(1 for v in c.values() if v == 1)/len(allz):.0%} of tokens)")
print("\nAn ordinal code needs <= 36 types for 298 tokens. There are 269.")
print("The whole-label ordinal readings are excluded. The cyclic structure found in")
print("T12 lives in the ENDING inventory (49 last-2 types), not in the label.")

json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                 'results', 't18_diversity.json'), 'w'), indent=1)
