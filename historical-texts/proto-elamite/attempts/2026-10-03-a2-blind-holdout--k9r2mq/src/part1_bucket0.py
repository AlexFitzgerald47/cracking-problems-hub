"""Part 1: the drawn item's test, run exactly as the handover specified it.

Re-screen on the published training set under the unchanged 2026-09-04 rule
(done: screen.json, 54 candidates), then test on bucket 0 under face blocking
AND under the co-numeral control, BH-corrected over the real candidate family of
54 rather than over the handful being looked at.

Declared exploratory: bucket 0 already carried the published validation arm, so
this is a statistic swap on seen data. Predictions P1.1-P1.3 frozen in
PREDICTIONS.md @ dc1802b.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import (load_audited, mixed_lines_of, split_name, bh, exact_blocked,
                    FACE, TABLET, conumeral)

sa = load_audited()
corpus = Path(sys.argv[1])
out = Path(__file__).resolve().parents[1] / "results"
screen = json.load(open(out / "screen.json"))
pub = {r["pair"]: r for r in json.load(open(out / "published_arm.json"))}

val = [ln for ln in mixed_lines_of(corpus) if split_name(ln.tablet) == "validation"]

rows, fps, cps, tps = [], [], [], []
for c in screen["candidates"]:
    m, t, d = c["m_sign"], c["target"], c["direction"]
    tb = exact_blocked(val, m, t, TABLET, d)
    fb = exact_blocked(val, m, t, FACE, d)
    cn = exact_blocked(val, m, t, conumeral(t), d)
    rows.append({"pair": f"{m}-{t}", "direction": d, "train_or": c["train_or"],
                 "published_val_p": pub[f"{m}-{t}"]["val_p"],
                 "published_val_q": pub[f"{m}-{t}"]["val_q"],
                 "tablet_p": tb["p"], "tablet_floor": tb["floor"],
                 "face_p": fb["p"], "face_floor": fb["floor"],
                 "face_informative_blocks": fb["informative_blocks"],
                 "face_mh_or": fb["mh_or"],
                 "conum_p": cn["p"], "conum_floor": cn["floor"],
                 "conum_informative_strata": cn["informative_blocks"],
                 "conum_mh_or": cn["mh_or"]})
    tps.append(tb["p"]); fps.append(fb["p"]); cps.append(cn["p"])

# consistency check: our tablet-blocked test must equal the published arm's test
worst = max(abs(r["tablet_p"] - r["published_val_p"]) for r in rows)
print(f"tablet-blocked vs published arm, max abs diff over 54: {worst:.2e}")
assert worst < 1e-12, "our tablet-blocked test does not match the published one"

for r, q in zip(rows, bh(tps)):
    r["tablet_q"] = q
for r, q in zip(rows, bh(fps)):
    r["face_q"] = q
for r, q in zip(rows, bh(cps)):
    r["conum_q"] = q
json.dump(rows, open(out / "part1_bucket0.json", "w"), indent=1)

A2_IN = ["M288-N39B", "M288-N24", "M376-N08A", "M370-N39B"]
print("\n=== Part 1: the four in-family tier-A2 pairs on bucket 0, BH over 54 ===")
hdr = f"{'pair':11s} {'trOR':>7s} | {'tablet p':>9s} {'q':>8s} | {'face p':>9s} {'q':>8s} {'floor':>9s} | {'conum p':>9s} {'q':>8s} {'floor':>9s}"
print(hdr); print("-" * len(hdr))
for r in rows:
    if r["pair"] in A2_IN:
        print(f"{r['pair']:11s} {r['train_or']:7.2f} | {r['tablet_p']:9.4g} {r['tablet_q']:8.4g} | "
              f"{r['face_p']:9.4g} {r['face_q']:8.4g} {r['face_floor']:9.2g} | "
              f"{r['conum_p']:9.4g} {r['conum_q']:8.4g} {r['conum_floor']:9.2g}")

print("\n=== frozen predictions ===")
f_ok = sum(1 for r in rows if r["pair"] in A2_IN and r["face_q"] <= 0.05)
c_ok = sum(1 for r in rows if r["pair"] in A2_IN and r["conum_q"] <= 0.05)
n39 = [r for r in rows if r["pair"] == "M288-N39B"][0]
print(f"P1.1 face-blocked q<=0.05 among the four: {f_ok}  (predicted 0)  "
      f"{'HELD' if f_ok == 0 else 'FAILED'}")
print(f"P1.2 co-numeral q<=0.05 among the four:   {c_ok}  (predicted <=1) "
      f"{'HELD' if c_ok <= 1 else 'FAILED'}")
print(f"P1.3 M288-N39B face p {n39['face_p']:.4g} vs published 0.01591: "
      f"{'HELD' if n39['face_p'] > 0.01591 else 'FAILED'}")

print("\n=== and what the same statistics do to the PUBLISHED EIGHT on bucket 0 ===")
EIGHT = ["M297-N39B", "M297-N24", "M297-N01", "M263-N30C", "M263-N01",
         "M243-N39B", "M106-N24", "M288-N45"]
for r in rows:
    if r["pair"] in EIGHT:
        v = []
        if r["face_q"] > 0.05:
            v.append("face FAILS" + (" (no power)" if r["face_floor"] > 0.05 else " WITH POWER"))
        if r["conum_q"] > 0.05:
            v.append("conum FAILS" + (" (no power)" if r["conum_floor"] > 0.05 else " WITH POWER"))
        print(f"  {r['pair']:11s} faceq={r['face_q']:9.4g} conumq={r['conum_q']:9.4g}  "
              f"{'; '.join(v) if v else 'holds under both'}")
print("\nwrote results/part1_bucket0.json")
