"""Re-derive, independently, the quantities the seven 10-01..10-03 sessions
agree on, so the reconciled table rests on numbers this session computed."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, exact_blocked, crude_cells, blocks_of,
                          PUBLISHED_EIGHT, split_name, odds_ratio,
                          fisher_exact_two_sided, bh_adjust)

corpus = Path(sys.argv[1])
_, _, eligible = load_eligible(corpus)
out = {}

face = lambda l: (l.tablet, l.surface)

# --- 1. M288-N45 block diagnostics -----------------------------------------
m, t = "M288", "N45"
inf_tabs, inf_blocks, forced_co, co_total = set(), 0, 0, 0
for (tab, surf), bl in blocks_of(eligible, face).items():
    n = len(bl); s = sum(m in l.m_signs for l in bl); tt = sum(t in l.n_signs for l in bl)
    o = sum(m in l.m_signs and t in l.n_signs for l in bl)
    co_total += o
    lo, hi = max(0, s - (n - tt)), min(s, tt)
    if hi > lo:
        inf_blocks += 1; inf_tabs.add(tab)
    else:
        forced_co += o
out["m288_n45_diagnostics"] = {
    "informative_blocks": inf_blocks, "distinct_tablets": len(inf_tabs),
    "co_occurrence_lines": co_total, "co_occurrences_in_forced_blocks": forced_co,
}
print("1. M288-N45:", out["m288_n45_diagnostics"])

# --- 2. The donor split (u4sk7u / ux87d8 / vd9la1 all report p=9.70e-5) -----
donor_tabs = inf_tabs
val = [l for l in eligible if l.tablet in donor_tabs]
train = [l for l in eligible if l.tablet not in donor_tabs]
r = exact_blocked(val, m, t, face, "enriched")
a, b, c, d = crude_cells(train, m, t)
out["donor_split"] = {
    "validation_tablets": len(donor_tabs), "validation_lines": len(val),
    "informative_blocks": r["informative_blocks"], "observed": r["observed"],
    "max": r["max"], "p": r["p"], "floor": r["floor"],
    "complement_screen_cells": [a, b, c, d],
    "complement_screen_or": odds_ratio(a, b, c, d),
    "complement_screen_fisher_p": fisher_exact_two_sided(a, b, c, d),
}
print(f"2. donor split: p={r['p']:.4g} floor={r['floor']:.3g} "
      f"obs/max={r['observed']}/{r['max']} inf={r['informative_blocks']} "
      f"| complement OR={odds_ratio(a,b,c,d):.2f} p={fisher_exact_two_sided(a,b,c,d):.3g}")

# --- 3. The correction base (u82zig and 3ltl6g: BH over 54, not 8) ---------
# Re-run the published screen on the published training set to get the real
# candidate family size, then BH the face-blocked holdout p-values over it.
tr = [l for l in eligible if split_name(l.tablet) == "train"]
va = [l for l in eligible if split_name(l.tablet) == "validation"]
nsigns = sorted({s for l in tr for s in l.n_signs})
raw = []
for tgt in nsigns:
    for sg in sorted({s for l in tr for s in l.m_signs}):
        aa, bb, cc, dd = crude_cells(tr, sg, tgt)
        if aa + bb < 20 or aa + cc < 20:
            continue
        raw.append((sg, tgt, odds_ratio(aa, bb, cc, dd),
                    fisher_exact_two_sided(aa, bb, cc, dd)))
qs = bh_adjust([x[3] for x in raw])
selected = [(x[0], x[1], x[2]) for x, q in zip(raw, qs)
            if q <= 0.01 and (x[2] >= 3.0 or x[2] <= 1/3)]
print(f"3. screen: {len(raw)} pairs tested, {len(selected)} selected "
      f"(2026-09-04 records 1056 tested / 54 selected)")
fb = {}
for sg, tgt, orr in selected:
    dirn = "enriched" if orr > 1 else "depleted"
    fb[(sg, tgt)] = exact_blocked(va, sg, tgt, face, dirn)["p"]
keys = list(fb)
q54 = dict(zip(keys, bh_adjust([fb[k] for k in keys])))
eight_p = [exact_blocked(va, mm, tt, face, dd)["p"] for mm, tt, dd in PUBLISHED_EIGHT]
q8 = bh_adjust(eight_p)
rows = []
for (mm, tt, dd), p8, qq8 in zip(PUBLISHED_EIGHT, eight_p, q8):
    rows.append({"pair": f"{mm}-{tt}", "face_p": p8, "q_over_8": qq8,
                 "q_over_screen": q54.get((mm, tt))})
out["correction_base"] = {"pairs_tested": len(raw), "selected": len(selected),
                          "rows": rows}
print("   pair          face p      q/8      q/screen")
for r2 in sorted(rows, key=lambda x: x["face_p"]):
    qs_ = r2["q_over_screen"]
    print(f"   {r2['pair']:12s} {r2['face_p']:.5f}  {r2['q_over_8']:.4f}  "
          f"{qs_:.4f}" if qs_ is not None else
          f"   {r2['pair']:12s} {r2['face_p']:.5f}  {r2['q_over_8']:.4f}  (not selected)")

Path("results").mkdir(exist_ok=True)
Path("results/verify_convergent.json").write_text(json.dumps(out, indent=2))
print("\nwrote results/verify_convergent.json")
