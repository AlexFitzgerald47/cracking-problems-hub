#!/usr/bin/env python3
"""T20: the per-sign label profile the Alfonsine crib gate needs.

The parallel 2026-09-08 GPT-5.6 Sol session preregistered a profile gate for candidate
external crib lists: a rule's extracted two-letter sigla must land near the observed
Voynich per-sign diversity (it used "~20-25 distinct effective types per 30") before any
positional alignment is attempted. That target was carried as a remembered figure. This
computes it directly from the corpus, per sign, for every reduction the gate might use.
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER, SIGN

rows = L.load()
z = L.ring_strings(rows)
out = []
print(f"{'sign':13s} {'n':>3s} {'full':>5s} {'first2':>7s} {'first3':>7s} "
      f"{'last2':>6s} {'last3':>6s} {'first+last':>10s}")
for i, f in enumerate(ORDER):
    v = [w for (ff, r), vv in z.items() if ff == f for w in vv]
    row = dict(sign=SIGN[i], folio=f, n=len(v),
               distinct_full=len(set(v)),
               distinct_first2=len(set(w[:2] for w in v)),
               distinct_first3=len(set(w[:3] for w in v)),
               distinct_last2=len(set(w[-2:] for w in v)),
               distinct_last3=len(set(w[-3:] for w in v)),
               distinct_first1last1=len(set(w[:1] + w[-1:] for w in v)))
    out.append(row)
    print(f"{SIGN[i]:13s} {row['n']:3d} {row['distinct_full']:5d} {row['distinct_first2']:7d} "
          f"{row['distinct_first3']:7d} {row['distinct_last2']:6d} {row['distinct_last3']:6d} "
          f"{row['distinct_first1last1']:10d}")

tot = {k: sum(r[k] for r in out) for k in out[0] if k.startswith("distinct") or k == "n"}
print(f"\nper-30 equivalents (mean over the eight full 30-label signs):")
full = [r for r in out if r["n"] >= 29]
for k in ("distinct_full", "distinct_first2", "distinct_first3", "distinct_last2",
          "distinct_last3", "distinct_first1last1"):
    m = sum(r[k] for r in full) / len(full)
    n = sum(r["n"] for r in full) / len(full)
    print(f"  {k:22s} {m:5.1f} per {n:.1f} labels  ({m/n*30:5.1f} per 30)")

print("\nGATE: a candidate crib rule's per-sign siglum diversity must match the column")
print("it is being compared against. Two-letter sigla taken from the FRONT of the label")
print("give ~9 types per 30, not ~20-25; the ~20-25 figure matches a THREE-letter front")
print("reduction or a first+last reduction. Choose the column deliberately.")

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results",
                       "zodiac_label_profile.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
