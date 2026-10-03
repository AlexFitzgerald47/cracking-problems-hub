#!/usr/bin/env python3
"""Block-aware split for the face-blocked null (HANDOVER item 1, 2026-10-02).

The 2026-09-17 session found that M288-N45 could not be settled on the bucket-0
holdout: only 4 of 290 tablet-faces were informative and the face-blocked test had a
p-value floor of 0.12, so it could not have returned a significant answer whatever the
data said. This implements the split that session recommended.

THE RULE (frozen in PREDICTIONS.md before any result existed):

    A tablet goes to VALIDATION iff it contributes at least one *informative*
    (tablet, face) block for the pair under test. Otherwise it goes to TRAINING.

"Informative" means the within-block permutation has freedom: lo < hi, where
lo = max(0, m_lines - (n_lines - n_sign_lines)) and hi = min(m_lines, n_sign_lines).
It is a function of the block MARGINALS ONLY and never of the observed overlap.

Why this is legitimate and not p-hacking: the face-blocked exact test's null
distribution is already *conditional* on each block's marginals. Marginals are ancillary,
so a block-selection rule that reads only marginals cannot shift the null. Blocks with
lo == hi have zero variance under that null -- they contribute a constant to the overlap
total and nothing to the p-value -- so excluding them from the test set discards no
information, while including them in the screening set costs the screen almost nothing.
The two halves of the procedure are therefore nearly information-disjoint by
construction. `null_calibration.py` tests the claim empirically rather than asserting it.

The split is pair-specific, so the BH correction is taken across the same eight pairs the
2026-09-04 design reported, keeping the multiplicity comparable.

Usage:  python3 block_aware_split.py [/path/to/pe-sign-value-data/corpus]
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence

from common import (CONFIRMED, Line, bh_adjust, blocked_randomization_p, block_stats,
                    face_key, fisher_exact_two_sided, hypergeom_probability,
                    load_eligible, odds_ratio)

MIN_TRAIN_SIGN_LINES = 20   # as 2026-09-04
MIN_TRAIN_TARGET_LINES = 20  # as 2026-09-04 (a + c >= 20)
MIN_VALIDATION_SIGN_LINES = 5  # as 2026-09-04


def informative_tablets(lines: Sequence[Line], m_sign: str, n_sign: str) -> set[str]:
    """Tablets contributing >=1 informative (tablet, face) block. Marginals only."""
    return {
        r["tablet"] for r in block_stats(lines, m_sign, n_sign) if r["informative"]
    }


def split_for_pair(lines: Sequence[Line], m_sign: str, n_sign: str):
    val_tablets = informative_tablets(lines, m_sign, n_sign)
    train = [ln for ln in lines if ln.tablet not in val_tablets]
    val = [ln for ln in lines if ln.tablet in val_tablets]
    return train, val, val_tablets


def contingency(lines: Sequence[Line], m_sign: str, n_sign: str):
    a = b = c = d = 0
    for ln in lines:
        hs, ht = m_sign in ln.m_signs, n_sign in ln.n_signs
        if hs and ht:
            a += 1
        elif hs:
            b += 1
        elif ht:
            c += 1
        else:
            d += 1
    return a, b, c, d


def rescreen(train: Sequence[Line], m_sign: str, n_sign: str):
    """Does (m_sign, n_sign) clear the 2026-09-04 screening gate on TRAINING only?

    BH correction is taken across every (M-family, N-sign) candidate meeting the same
    support minima on this training set, exactly as the published screen did.
    """
    m_signs = sorted({s for ln in train for s in ln.m_signs})
    n_signs = sorted({s for ln in train for s in ln.n_signs})
    cands, ps = [], []
    for n in n_signs:
        tgt = sum(n in ln.n_signs for ln in train)
        if tgt < MIN_TRAIN_TARGET_LINES:
            continue
        for m in m_signs:
            a, b, c, d = contingency(train, m, n)
            if a + b < MIN_TRAIN_SIGN_LINES or a + c < MIN_TRAIN_TARGET_LINES:
                continue
            cands.append((m, n, (a, b, c, d), odds_ratio(a, b, c, d)))
            ps.append(fisher_exact_two_sided(a, b, c, d))
    qs = bh_adjust(ps)
    out = None
    n_selected = 0
    for (m, n, cells, orr), p, q in zip(cands, ps, qs):
        selected = q <= 0.01 and (orr >= 3.0 or orr <= 1.0 / 3.0)
        if selected:
            n_selected += 1
        if m == m_sign and n == n_sign:
            out = {"cells": cells, "odds_ratio": orr, "p": p, "q": q,
                   "selected": selected}
    return out, len(cands), n_selected


def floor_and_p(val: Sequence[Line], m_sign: str, n_sign: str, direction: str):
    """Face-blocked exact p-value, its attainable floor, and block bookkeeping."""
    rows = block_stats(val, m_sign, n_sign)
    dist = [1.0]
    observed = 0
    max_possible = 0
    min_possible = 0
    informative = 0
    for r in rows:
        observed += r["overlap"]
        max_possible += r["hi"]
        min_possible += r["lo"]
        if r["informative"]:
            informative += 1
        local = [0.0] * (r["hi"] + 1)
        for k in range(r["lo"], r["hi"] + 1):
            local[k] = hypergeom_probability(k, r["m_lines"], r["n_sign_lines"],
                                             r["n_lines"])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    if direction == "enriched":
        p = min(1.0, sum(dist[observed:]))
        floor = min(1.0, sum(dist[max_possible:]))
    else:
        p = min(1.0, sum(dist[: observed + 1]))
        floor = min(1.0, sum(dist[: min_possible + 1]))
    return {
        "p": p, "p_floor": floor, "observed_overlap": observed,
        "max_possible_overlap": max_possible, "min_possible_overlap": min_possible,
        "informative_blocks": informative, "blocks": len(rows),
        "freedom_units": max_possible - min_possible,
        "has_power_at_05": floor <= 0.05,
    }


def run(lines: Sequence[Line], pairs=CONFIRMED) -> dict:
    results = []
    for m, n, direction in pairs:
        train, val, val_tablets = split_for_pair(lines, m, n)
        screen, n_cands, n_sel = rescreen(train, m, n)
        stat = floor_and_p(val, m, n, direction)
        vcells = contingency(val, m, n)
        results.append({
            "m_sign": m, "n_sign": n, "direction": direction,
            "validation_tablets": len(val_tablets), "validation_lines": len(val),
            "training_lines": len(train),
            "screen": screen, "screen_candidates": n_cands, "screen_selected": n_sel,
            "validation_cells": vcells,
            "validation_odds_ratio": odds_ratio(*vcells),
            **stat,
        })
    qs = bh_adjust([r["p"] for r in results])
    for r, q in zip(results, qs):
        r["q"] = q
        orr = r["validation_odds_ratio"]
        r["confirmed"] = bool(
            r["screen"] and r["screen"]["selected"]
            and r["has_power_at_05"]
            and q <= 0.05
            and (vs := (orr >= 1.5 if r["direction"] == "enriched"
                        else orr <= 1.0 / 1.5)) is not None and vs
            and (r["validation_cells"][0] + r["validation_cells"][1]
                 >= MIN_VALIDATION_SIGN_LINES)
        )
    return {"schema_version": 1, "rule": __doc__.split("THE RULE")[1].split("Why this")[0].strip(),
            "results": results}


def main() -> None:
    lines = load_eligible(sys.argv)
    out = run(lines)
    Path("results").mkdir(exist_ok=True)
    Path("results/block_aware_split.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"{'pair':12} {'scr q':>8} {'scrOR':>7} {'valOR':>7} {'obs/max':>8} "
          f"{'infB':>5} {'p':>10} {'floor':>10} {'q':>10} pwr cfm")
    for r in out["results"]:
        s = r["screen"]
        print(f"{r['m_sign']+'-'+r['n_sign']:12} "
              f"{(s['q'] if s else float('nan')):8.4f} "
              f"{(s['odds_ratio'] if s else float('nan')):7.2f} "
              f"{r['validation_odds_ratio']:7.2f} "
              f"{str(r['observed_overlap'])+'/'+str(r['max_possible_overlap']):>8} "
              f"{r['informative_blocks']:5} {r['p']:10.3e} {r['p_floor']:10.3e} "
              f"{r['q']:10.3e} {'Y' if r['has_power_at_05'] else 'n':>3} "
              f"{'YES' if r['confirmed'] else 'no':>3}")
    print()
    for r in out["results"]:
        print(f"{r['m_sign']+'-'+r['n_sign']:12} val {r['validation_tablets']:4} tablets / "
              f"{r['validation_lines']:5} lines, train {r['training_lines']:5} lines, "
              f"screen selected {r['screen_selected']} of {r['screen_candidates']} candidates")


if __name__ == "__main__":
    main()
