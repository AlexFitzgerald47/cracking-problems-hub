"""Run the PUBLISHED validation arm on all 54 selected candidates and record
exactly which criterion each one failed.

This matters for the warrant. If an A2 pair failed the published blind test on
its BH q, then re-testing it with a different statistic is test-shopping and the
promotion is not available. If it failed on the effect-size floor (OR>=1.5) or
the minimum-line bar while its q was tiny, that is a different situation: the
pre-specified test did fire, and a stronger conditional test is a legitimate
follow-up on a pre-specified family.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import load_audited, mixed_lines_of, split_name, bh

sa = load_audited()
corpus = Path(sys.argv[1])
out = Path(__file__).resolve().parents[1] / "results"
screen = json.load(open(out / "screen.json"))

mixed = mixed_lines_of(corpus)
val = [ln for ln in mixed if split_name(ln.tablet) == "validation"]

rows, ps = [], []
for c in screen["candidates"]:
    m, t, d = c["m_sign"], c["target"], c["direction"]
    pred = lambda ln, tt=t: tt in ln.n_signs
    cells = sa.contingency(val, m, pred)
    p = sa.blocked_randomization_p(val, m, pred, d)
    rows.append({"pair": f"{m}-{t}", "direction": d, "train_or": c["train_or"],
                 "val_cells": list(cells), "val_or": sa.odds_ratio(*cells),
                 "val_p": p})
    ps.append(p)
for r, q in zip(rows, bh(ps)):
    r["val_q"] = q

for r in rows:
    tro, vo = r["train_or"], r["val_or"]
    same = (tro > 1 and vo > 1) or (tro < 1 and vo < 1)
    lines = r["val_cells"][0] + r["val_cells"][1]
    fails = []
    if lines < 5:
        fails.append(f"val_sign_lines={lines}<5")
    if not same:
        fails.append("direction flipped")
    if r["val_q"] > 0.05:
        fails.append(f"q={r['val_q']:.3g}>0.05")
    if not (vo >= 1.5 or vo <= 1 / 1.5):
        fails.append(f"|val OR|={vo:.2f} inside [2/3,1.5]")
    r["published_verdict"] = "CONFIRMED" if not fails else "; ".join(fails)

json.dump(rows, open(out / "published_arm.json", "w"), indent=1)
conf = [r for r in rows if r["published_verdict"] == "CONFIRMED"]
print(f"published arm on the 54: {len(conf)} confirmed (expect 8)")
assert len(conf) == 8, [r["pair"] for r in conf]
print("  ->", ", ".join(r["pair"] for r in conf))

A2_IN = ["M288-N39B", "M376-N08A", "M288-N24", "M370-N39B"]
print("\n=== why each in-family tier-A2 pair failed the PUBLISHED arm ===")
for r in rows:
    if r["pair"] in A2_IN:
        print(f"  {r['pair']:11s} trOR={r['train_or']:7.2f} valOR={r['val_or']:6.2f} "
              f"valp={r['val_p']:.4g} valq={r['val_q']:.4g}  -> {r['published_verdict']}")
print("\nwrote results/published_arm.json")
