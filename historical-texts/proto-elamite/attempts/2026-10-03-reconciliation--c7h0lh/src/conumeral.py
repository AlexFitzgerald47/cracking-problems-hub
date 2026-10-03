"""The adjudication: a third, independent implementation of the co-numeral
control that ux87d8 and nimur2 arrived at by different routes.

ux87d8 blocked on (tablet, face, other-N-count capped at 3) with the exact test.
nimur2 stratified on the exact other-N SET and reported a Mantel-Haenszel OR
with a permutation p.  Neither computed the folder's own p-floor for this
scheme, so neither could say which failures were refusals and which were
absences of power -- the very distinction the folder established in 2026-09-17
and applied to M288-N45.

This runs nimur2's strata (the exact other-N set: two lines in a stratum write
the same quantity apart from the target) through the folder's own exact
conditional test, and reports p, p-floor, MH-OR and informative-stratum count
together.  No numeral is assigned a value; the strata are observed co-occurring
signs only.
"""
from __future__ import annotations
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells,
                          PUBLISHED_EIGHT, odds_ratio, bh_adjust)

corpus = Path(sys.argv[1])
_, _, eligible = load_eligible(corpus)


def conumeral_key(target):
    """Stratum = the exact set of N-signs on the line OTHER than the target.
    Invariant under permutation of the target by construction: removing the
    target from a line's N-set cannot depend on whether the target is there."""
    return lambda l: frozenset(l.n_signs - {target})


print(f"{'pair':12s} {'dir':4s} {'crude OR':>9s} {'MH-OR':>8s} {'p':>10s} "
      f"{'floor':>9s} {'q(BH8)':>8s} {'infS':>5s} {'strata':>6s}  verdict")
rows, ps = [], []
for m, t, d in PUBLISHED_EIGHT:
    a, b, c, dd = crude_cells(eligible, m, t)
    r = exact_blocked(eligible, m, t, conumeral_key(t), d)
    rows.append({"pair": f"{m}-{t}", "direction": d,
                 "crude_or": odds_ratio(a, b, c, dd), **r})
    ps.append(r["p"])
qs = bh_adjust(ps)
for r, q in zip(rows, qs):
    r["q_bh8"] = q
    powered = r["floor"] <= 0.05
    r["verdict"] = ("SURVIVES" if q <= 0.05 else
                    ("FAILS (with power)" if powered else "UNTESTABLE (no power)"))
    print(f"{r['pair']:12s} {r['direction'][:3]:4s} {r['crude_or']:9.2f} "
          f"{r['mh_or']:8.2f} {r['p']:10.3g} {r['floor']:9.3g} {q:8.3g} "
          f"{r['informative_blocks']:5d} {r['blocks']:6d}  {r['verdict']}")

Path("results").mkdir(exist_ok=True)
Path("results/conumeral.json").write_text(json.dumps(rows, indent=2))
print("\nwrote results/conumeral.json")
