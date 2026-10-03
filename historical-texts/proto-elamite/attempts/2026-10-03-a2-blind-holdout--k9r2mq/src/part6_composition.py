"""Part 6: the composition control inside the blind buckets.

c7h0lh ran this control on the full eligible corpus, which contains the training
data that selected these pairs. Here it runs on the blind test buckets only --
buckets 1-4 individually, and pooled -- so the control is applied to data that
did not select the pair.

Strata = the exact set of OTHER numeral signs on the line. The test asks whether
the association survives comparison only between lines whose numeral expression
is otherwise identical.

Predictions P6.1-P6.4 frozen in PREDICTIONS.md @ 28fff42.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import mixed_lines_of, exact_blocked, conumeral, FACE, odds_ratio
from fastfold import bucket

corpus = Path(sys.argv[1])
out = Path(__file__).resolve().parents[1] / "results"
cf = json.load(open(out / "crossfit.json"))
counts = cf["blind_fold_counts"]

el = mixed_lines_of(corpus)
blind = [ln for ln in el if bucket(ln.tablet) != 0]

TARGETS = [
    ("M288", "N24",  "enriched", "warranted 3/4 folds"),
    ("M288", "N39B", "enriched", "warranted 2/4 folds"),
    ("M376", "N08A", "enriched", "warranted 2/4 folds"),
    ("M263", "N01",  "enriched", "tier C, yet 4/4 folds"),
    ("M297", "N39B", "enriched", "tier A1, 3/4 folds"),
    ("M288", "N45",  "enriched", "tier A1 flagship, 1/4 folds"),
]

rows = []
print("=== pooled blind buckets 1-4 (%d lines): co-numeral control ===" % len(blind))
print(f"{'pair':11s} {'note':28s} {'crude OR':>9s} {'MH OR':>8s} {'p':>11s} "
      f"{'floor':>10s} {'strata':>6s} {'verdict':>22s}")
for m, t, d, note in TARGETS:
    a = sum(m in ln.m_signs and t in ln.n_signs for ln in blind)
    b = sum(m in ln.m_signs and t not in ln.n_signs for ln in blind)
    c = sum(m not in ln.m_signs and t in ln.n_signs for ln in blind)
    dd = len(blind) - a - b - c
    cn = exact_blocked(blind, m, t, conumeral(t), d)
    fb = exact_blocked(blind, m, t, FACE, d)
    powered = cn["floor"] <= 0.05
    passes = cn["p"] <= 0.05 and powered
    verdict = ("SURVIVES" if passes else
               ("REFUSED (has power)" if powered else "no power - uninformative"))
    rows.append({"pair": f"{m}-{t}", "note": note, "blind_folds": len(counts.get(f"{m}-{t}", [])),
                 "pooled_cells": [a, b, c, dd], "pooled_crude_or": odds_ratio(a, b, c, dd),
                 "pooled_conum_p": cn["p"], "pooled_conum_floor": cn["floor"],
                 "pooled_conum_mh_or": cn["mh_or"],
                 "pooled_conum_strata": cn["informative_blocks"],
                 "pooled_face_p": fb["p"], "pooled_face_floor": fb["floor"],
                 "pooled_verdict": verdict})
    print(f"{m}-{t:5s} {note:28s} {odds_ratio(a,b,c,dd):9.2f} {cn['mh_or']:8.2f} "
          f"{cn['p']:11.4g} {cn['floor']:10.2g} {cn['informative_blocks']:6d} "
          f"{verdict:>22s}")

print("\n=== per blind bucket ===")
per = {}
for m, t, d, note in TARGETS:
    key = f"{m}-{t}"
    per[key] = {}
    cells = []
    for b_ in (1, 2, 3, 4):
        sub = [ln for ln in el if bucket(ln.tablet) == b_]
        cn = exact_blocked(sub, m, t, conumeral(t), d)
        powered = cn["floor"] <= 0.05
        v = ("surv" if (cn["p"] <= 0.05 and powered) else
             ("REFUSED" if powered else "nopow"))
        per[key][str(b_)] = {"p": cn["p"], "floor": cn["floor"],
                             "strata": cn["informative_blocks"], "verdict": v}
        cells.append(f"b{b_}:{v}({cn['p']:.3g}/f{cn['floor']:.1g})")
    print(f"  {key:11s} " + "  ".join(cells))

json.dump({"pooled": rows, "per_bucket": per}, open(out / "part6_composition.json", "w"), indent=1)

g = {r["pair"]: r for r in rows}
surv = lambda k: g[k]["pooled_verdict"] == "SURVIVES"
p61 = surv("M288-N24") and surv("M288-N39B")
p62 = not surv("M376-N08A") or g["M376-N08A"]["pooled_conum_floor"] > 0.01
anyfail = any(v["verdict"] != "surv" for k in ("M288-N24", "M288-N39B", "M376-N08A")
              for v in per[k].values())
p64 = (g["M263-N01"]["pooled_verdict"] == "REFUSED (has power)")
print("\n=== frozen predictions ===")
print(f"P6.1 M288-N24 and M288-N39B both survive pooled: {'HELD' if p61 else 'FAILED'}")
print(f"P6.2 M376-N08A has no usable pooled verdict:      {'HELD' if p62 else 'FAILED'} "
      f"(floor={g['M376-N08A']['pooled_conum_floor']:.3g}, "
      f"strata={g['M376-N08A']['pooled_conum_strata']})")
print(f"P6.3 >=1 of the three fails in >=1 single bucket:  {'HELD' if anyfail else 'FAILED'}")
print(f"P6.4 M263-N01 fails pooled WITH power:             {'HELD' if p64 else 'FAILED'} "
      f"(p={g['M263-N01']['pooled_conum_p']:.4g}, "
      f"floor={g['M263-N01']['pooled_conum_floor']:.2g})")
print("\nwrote results/part6_composition.json")
