"""Handover item 2: the three blind-warranted pairs on the 130 genuinely new
CDLI tablets, with the power stated before the verdict.

u82zig established on 2026-10-01 that the published EIGHT have essentially no
power on these 130 tablets. The tier-A2 pairs are 3-20x denser, so the question
is open for them and it is the one this folder's reopening condition names: a
tier-A pair reopens if it fails IN DIRECTION on an independent CDLI export.

The 130 tablets are in the live CDLI export and in no part of the 2026-09-04
screen or holdout. Direction predictions frozen in PREDICTIONS.md before running.

Reported per pair: contingency and corrected OR on the new tablets, the
direction verdict, and the face-blocked exact test WITH its p-floor -- on 130
tablets the floor is the number that decides whether the p-value means anything.
"""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from common import load_audited, exact_blocked, FACE, odds_ratio, conumeral

sa = load_audited()
pin, cdli = Path(sys.argv[1]), Path(sys.argv[2])
out = Path(__file__).resolve().parents[1] / "results"

pin_names = {p.name.split(".")[0] for p in pin.glob("*.values.atf")}
cdli_names = {p.name.split(".")[0] for p in cdli.glob("*.values.atf")}
new = sorted(cdli_names - pin_names)
print(f"pinned={len(pin_names)} live={len(cdli_names)} NEW={len(new)} "
      f"(u82zig reported 130)")
assert len(new) == 130, len(new)

lines = [ln for n in new for ln in sa.parse_tablet(cdli / f"{n}.values.atf")]
el = [ln for ln in lines if ln.m_signs and not ln.damaged and ln.n_signs]
print(f"new-tablet lines={len(lines)} eligible={len(el)} "
      f"(u82zig reported 109 eligible)")

# N08 -> N08A: the live export uses N08A where the 2022 pin used N08.
# results/n08_audit.json (c7h0lh) shows M376-N08A holds under every merge
# policy, so MERGE rather than drop, and the policy is stated here.
MERGE_N08 = True
if MERGE_N08:
    for ln in el:
        if "N08" in ln.n_signs:
            ln.n_signs.add("N08A")

TARGETS = [
    # blind-warranted by the cross-fit (folds 2-5), direction from training
    ("M288", "N24",  "enriched", "A2 -> blind-warranted, 3 of 4 folds"),
    ("M288", "N39B", "enriched", "A2 -> blind-warranted, 2 of 4 folds"),
    ("M376", "N08A", "enriched", "A2 -> blind-warranted, 2 of 4 folds"),
    # the folder's A1 tier, for comparison
    ("M288", "N45",  "enriched", "A1 flagship"),
    ("M297", "N39B", "enriched", "A1"),
    ("M106", "N24",  "enriched", "A1 (0 of 4 blind folds)"),
    ("M263", "N01",  "enriched", "tier C, but 4 of 4 blind folds"),
]

rows = []
print(f"\n{'pair':11s} {'tier':34s} {'a':>3s} {'b':>4s} {'c':>4s} {'d':>4s} "
      f"{'OR':>8s} {'dir':>9s} {'face p':>9s} {'floor':>9s} {'power?':>7s}")
for m, t, d, tag in TARGETS:
    a = sum(m in ln.m_signs and t in ln.n_signs for ln in el)
    b = sum(m in ln.m_signs and t not in ln.n_signs for ln in el)
    c = sum(m not in ln.m_signs and t in ln.n_signs for ln in el)
    dd = len(el) - a - b - c
    orr = odds_ratio(a, b, c, dd)
    fb = exact_blocked(el, m, t, FACE, d)
    agree = (orr > 1) if d == "enriched" else (orr < 1)
    power = fb["floor"] <= 0.05
    rows.append({"pair": f"{m}-{t}", "tier": tag, "direction": d,
                 "cells": [a, b, c, dd], "corrected_or": orr,
                 "direction_agrees": bool(agree) if (a + b) else None,
                 "face_p": fb["p"], "face_floor": fb["floor"],
                 "face_informative_blocks": fb["informative_blocks"],
                 "has_power_at_05": power,
                 "m_lines_on_new_tablets": a + b})
    dv = "n/a" if (a + b) == 0 else ("agrees" if agree else "OPPOSITE")
    print(f"{m}-{t:5s} {tag:34s} {a:3d} {b:4d} {c:4d} {dd:4d} {orr:8.2f} "
          f"{dv:>9s} {fb['p']:9.3g} {fb['floor']:9.2g} {'YES' if power else 'no':>7s}")

json.dump({"new_tablets": len(new), "new_eligible_lines": len(el),
           "n08_merge_policy": "N08 merged into N08A",
           "rows": rows}, open(out / "cdli_new.json", "w"), indent=1)
tested = [r for r in rows if r["m_lines_on_new_tablets"] > 0]
opp = [r for r in tested if r["direction_agrees"] is False]
powered = [r for r in rows if r["has_power_at_05"]]
print(f"\n{len(tested)} of {len(rows)} pairs have any M-bearing line on the new tablets.")
print(f"{len(powered)} have face-blocked power at 0.05.")
print(f"{len(opp)} point in the OPPOSITE direction: "
      f"{', '.join(r['pair'] for r in opp) if opp else 'none'}")
print("wrote results/cdli_new.json")
