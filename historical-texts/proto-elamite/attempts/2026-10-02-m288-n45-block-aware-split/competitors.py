#!/usr/bin/env python3
"""How many other (M-sign, N-sign) pairs pass this same procedure?  (P6)

board/PRACTICES.md: "Count the competitors; do not score one." Thirteen unrelated
plaintexts scored at or above the best published Dorabella claim. The analogue here is:
run the identical block-aware split and face-blocked exact test over EVERY eligible
(M-family, N-sign) pair with enough support, and ask where M288-N45 lands.

A pair is tested in whichever direction its own validation odds ratio points, which is
the permissive choice and therefore the conservative one for this question -- it gives
every competitor its best shot.

Usage:  python3 competitors.py [/path/to/corpus]
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from common import load_eligible, odds_ratio
from block_aware_split import contingency, floor_and_p, split_for_pair

MIN_SIGN_LINES = 20
MIN_TARGET_LINES = 20


def main() -> None:
    lines = load_eligible(sys.argv)
    m_counts = Counter(s for ln in lines for s in ln.m_signs)
    n_counts = Counter(s for ln in lines for s in ln.n_signs)
    m_signs = sorted(s for s, c in m_counts.items() if c >= MIN_SIGN_LINES)
    n_signs = sorted(s for s, c in n_counts.items() if c >= MIN_TARGET_LINES)
    print(f"eligible lines {len(lines)}; M-families with >={MIN_SIGN_LINES} lines: "
          f"{len(m_signs)}; N-signs with >={MIN_TARGET_LINES} lines: {len(n_signs)}; "
          f"pairs to test: {len(m_signs) * len(n_signs)}")

    rows = []
    for m in m_signs:
        for n in n_signs:
            a, b, c, d = contingency(lines, m, n)
            if a + b < MIN_SIGN_LINES or a + c < MIN_TARGET_LINES:
                continue
            train, val, val_tabs = split_for_pair(lines, m, n)
            if not val:
                continue
            vcells = contingency(val, m, n)
            if vcells[0] + vcells[1] < 5:
                continue
            vor = odds_ratio(*vcells)
            direction = "enriched" if vor >= 1.0 else "depleted"
            st = floor_and_p(val, m, n, direction)
            rows.append({
                "m_sign": m, "n_sign": n, "direction": direction,
                "validation_odds_ratio": vor, "validation_cells": vcells,
                "validation_tablets": len(val_tabs), **st,
            })

    rows.sort(key=lambda r: r["p"])
    powered = [r for r in rows if r["has_power_at_05"]]
    passing = [r for r in powered if r["p"] <= 0.05
               and (r["validation_odds_ratio"] >= 1.5 if r["direction"] == "enriched"
                    else r["validation_odds_ratio"] <= 1 / 1.5)]
    rank = next((i for i, r in enumerate(rows, 1)
                 if (r["m_sign"], r["n_sign"]) == ("M288", "N45")), None)
    rank_passing = next((i for i, r in enumerate(passing, 1)
                         if (r["m_sign"], r["n_sign"]) == ("M288", "N45")), None)
    print(f"pairs tested {len(rows)}; with power at 0.05: {len(powered)}; "
          f"passing the gate: {len(passing)}")
    print(f"M288-N45 rank by validation p: {rank} of {len(rows)} tested, "
          f"{rank_passing} of {len(passing)} passing")
    print()
    print(f"{'rank':>4} {'pair':12} {'dir':9} {'valOR':>8} {'obs/max':>9} {'infB':>5} "
          f"{'p':>11} {'floor':>11}")
    for i, r in enumerate(rows[:25], 1):
        tag = "  <<< drawn pair" if (r["m_sign"], r["n_sign"]) == ("M288", "N45") else ""
        print(f"{i:4} {r['m_sign']+'-'+r['n_sign']:12} {r['direction']:9} "
              f"{r['validation_odds_ratio']:8.2f} "
              f"{str(r['observed_overlap'])+'/'+str(r['max_possible_overlap']):>9} "
              f"{r['informative_blocks']:5} {r['p']:11.3e} {r['p_floor']:11.3e}{tag}")
    Path("results").mkdir(exist_ok=True)
    Path("results/competitors.json").write_text(json.dumps({
        "pairs_tested": len(rows), "pairs_with_power": len(powered),
        "pairs_passing": len(passing), "m288_n45_rank_all": rank,
        "m288_n45_rank_passing": rank_passing, "rows": rows}, indent=2) + "\n")


if __name__ == "__main__":
    main()
