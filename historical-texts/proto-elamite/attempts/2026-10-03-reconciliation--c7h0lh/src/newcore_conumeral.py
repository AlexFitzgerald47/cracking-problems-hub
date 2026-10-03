"""The one new test: the co-numeral control applied to the replicated new core.

The 11 pairs appearing in >=2 of the four independent candidate-expansion sweeps
of 10-01..10-03.  No session ran this control on them.  Predictions frozen in
PREDICTIONS.md, committed before this file was run."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells,
                          odds_ratio, bh_adjust)

NEW_CORE = [  # (m, n, direction, sweeps_reporting_it)
    ("M288", "N39B", "enriched", 4), ("M288", "N24", "enriched", 4),
    ("M376", "N08A", "enriched", 4),
    ("M106", "N01", "depleted", 3), ("M370", "N39B", "depleted", 3),
    ("M106", "N30C", "enriched", 2), ("M288", "N14", "enriched", 2),
    ("M106", "N39B", "enriched", 2), ("M362", "N14", "enriched", 2),
    ("M354", "N14", "enriched", 2), ("M002", "N30C", "enriched", 2),
]

corpus = Path(sys.argv[1])
_, _, eligible = load_eligible(corpus)
face = lambda l: (l.tablet, l.surface)
conum = lambda t: (lambda l: frozenset(l.n_signs - {t}))

rows, ps = [], []
for m, t, d, sw in NEW_CORE:
    a, b, c, dd = crude_cells(eligible, m, t)
    fb = exact_blocked(eligible, m, t, face, d)
    cn = exact_blocked(eligible, m, t, conum(t), d)
    rows.append({"pair": f"{m}-{t}", "direction": d, "sweeps": sw,
                 "cells": [a, b, c, dd], "crude_or": odds_ratio(a, b, c, dd),
                 "face_blocked_p": fb["p"], "face_blocked_floor": fb["floor"],
                 "conumeral_p": cn["p"], "conumeral_floor": cn["floor"],
                 "conumeral_mh_or": cn["mh_or"],
                 "conumeral_informative_strata": cn["informative_blocks"]})
    ps.append(cn["p"])
for r, q in zip(rows, bh_adjust(ps)):
    r["conumeral_q"] = q
    powered = r["conumeral_floor"] <= 0.05
    r["verdict"] = ("SURVIVES" if q <= 0.05 else
                    ("FAILS (with power)" if powered else "UNTESTABLE (no power)"))

print(f"{'pair':12s} {'sw':>2s} {'dir':4s} {'crudeOR':>8s} {'face p':>10s} "
      f"{'MH-OR':>7s} {'conum p':>10s} {'floor':>9s} {'q':>9s} {'infS':>4s}  verdict")
for r in rows:
    print(f"{r['pair']:12s} {r['sweeps']:2d} {r['direction'][:3]:4s} "
          f"{r['crude_or']:8.2f} {r['face_blocked_p']:10.3g} "
          f"{r['conumeral_mh_or']:7.2f} {r['conumeral_p']:10.3g} "
          f"{r['conumeral_floor']:9.2g} {r['conumeral_q']:9.3g} "
          f"{r['conumeral_informative_strata']:4d}  {r['verdict']}")

n_sv = sum(r["verdict"] == "SURVIVES" for r in rows)
print(f"\nsurvives {n_sv}/11, demoted {11 - n_sv}/11")
Path("results/newcore_conumeral.json").write_text(json.dumps(rows, indent=2))
print("wrote results/newcore_conumeral.json")
