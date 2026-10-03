"""Re-screen the published training set under the UNCHANGED 2026-09-04 rule and
enumerate the real candidate family.

The 2026-09-17 session corrected over 8 (and a later one over 16). Both are the
wrong base: BH on the validation arm must be taken over every candidate the
training screen *carried forward*, because that is the family the validation
test was applied to. This script recovers that number from the audited parser
rather than trusting the figure in any handover.

Output: results/screen.json
  tested      - raw candidates that cleared the occupancy bars (the search space)
  selected    - candidates passing training BH q<=0.01 AND |OR| gate (the base)
  published   - the 8 that additionally cleared the published validation criteria
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import (load_audited, mixed_lines_of, split_name)

sa = load_audited()
corpus = Path(sys.argv[1])
out = Path(__file__).resolve().parents[1] / "results"

files = sorted(corpus.glob("*.values.atf"))
lines = [ln for f in files for ln in sa.parse_tablet(f)]
mixed = [ln for ln in lines if ln.m_signs and not ln.damaged and ln.n_signs]
train = [ln for ln in mixed if split_name(ln.tablet) == "train"]
val = [ln for ln in mixed if split_name(ln.tablet) == "validation"]
print(f"mixed={len(mixed)} train={len(train)} validation={len(val)}")

# EXACTLY the published numeral_association candidate construction
train_signs = sorted({s for ln in train for s in ln.m_signs})
n_signs = sorted({s for ln in train for s in ln.n_signs})
print(f"M families in train: {len(train_signs)}   N signs in train: {len(n_signs)}")

raw = []
for t in n_signs:
    pred = lambda ln, target=t: target in ln.n_signs
    for m in train_signs:
        a, b, c, d = sa.contingency(train, m, pred)
        if a + b < 20 or a + c < 20:        # published occupancy bars
            continue
        raw.append({"m_sign": m, "target": t, "cells": [a, b, c, d],
                    "train_or": sa.odds_ratio(a, b, c, d),
                    "train_p": sa.fisher_exact_two_sided(a, b, c, d)})

qs = sa.bh_adjust([r["train_p"] for r in raw])
for r, q in zip(raw, qs):
    r["train_q"] = q
sel = [r for r in raw
       if r["train_q"] <= 0.01 and (r["train_or"] >= 3.0 or r["train_or"] <= 1 / 3)]
print(f"\nTESTED (search space)        = {len(raw)}")
print(f"SELECTED (correction base)   = {len(sel)}")

for r in sel:
    r["direction"] = "enriched" if r["train_or"] > 1 else "depleted"
    r["val_cells"] = list(sa.contingency(val, r["m_sign"],
                                         lambda ln, t=r["target"]: t in ln.n_signs))

json.dump({"tested": len(raw), "selected": len(sel),
           "m_families_train": len(train_signs), "n_signs_train": len(n_signs),
           "train_lines": len(train), "validation_lines": len(val),
           "candidates": sel}, open(out / "screen.json", "w"), indent=1)

A2 = [("M288", "N39B"), ("M376", "N08A"), ("M288", "N14"),
      ("M288", "N24"), ("M362", "N14"), ("M370", "N39B")]
selset = {(r["m_sign"], r["target"]) for r in sel}
rawmap = {(r["m_sign"], r["target"]): r for r in raw}
print("\n=== are the tier-A2 pairs inside the published screened family? ===")
for p in A2:
    r = rawmap.get(p)
    if r is None:
        print(f"  {p[0]}-{p[1]:5s}  NOT EVEN TESTED (fails an occupancy bar)")
        continue
    print(f"  {p[0]}-{p[1]:5s}  trOR={r['train_or']:7.2f} trq={r['train_q']:.3g}  "
          f"{'IN the 54' if p in selset else 'screened OUT by the published rule'}")
print("wrote results/screen.json")
