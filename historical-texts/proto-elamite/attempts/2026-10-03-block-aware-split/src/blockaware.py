#!/usr/bin/env python3
"""Settle M288-N45 with a block-aware split (2026-09-17 handover, experiment 1).

The handover asks for a tablet-level split whose validation half is guaranteed at
least 10 informative (tablet, face) blocks for the pair, with candidates re-screened
on the complement. Three things are done here:

A. The pre-registered marginal-only split rule, run once.
B. EVERY admissible split enumerated, so the reported p-value is a distribution over
   splits rather than one choice I could have cherry-picked. PREDICTIONS.md records
   that per-block overlaps were already visible to me, which is exactly why no single
   split is allowed to carry the result.
C. The label-permutation null on the split itself (2026-09-23 cross-reference): hold
   every tablet's blocks in place, permute which tablets are labelled validation,
   preserve sizes, and ask whether the observed split is unusual.

Screening is the published 2026-09-04 training screen re-run verbatim on each
complement.
"""
from __future__ import annotations

import itertools
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    DIRECTION, M, N, canonical_split, face_blocks, load_eligible, odds_ratio,
    screen_numeral, tail, tablet_hash,
)

WANT = 10
SAMPLE_SCREENS = 250
SEED = 20261003


def contingency(lines, m_sign, n_sign):
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


def evaluate(blocks, val_tablets):
    """Validation-side face-blocked test for the pair, given a tablet allocation."""
    val_inf = [b for b in blocks if b["informative"] and b["tablet"] in val_tablets]
    p, floor, obs, mx = tail(val_inf)
    return {"n_val_informative": len(val_inf), "p": p, "p_floor": floor,
            "observed_overlap": obs, "max_overlap": mx,
            "has_power_at_05": floor <= 0.05}


def main():
    el = load_eligible()
    blocks = face_blocks(el)
    inf = [b for b in blocks if b["informative"]]
    per_tablet = defaultdict(int)
    for b in inf:
        per_tablet[b["tablet"]] += 1
    inf_tablets = sorted(per_tablet)

    out = {"pair": f"{M}-{N}", "direction": DIRECTION, "want_val_blocks": WANT,
           "eligible_lines": len(el), "blocks_total": len(blocks),
           "blocks_informative": len(inf),
           "informative_tablets": {t: per_tablet[t] for t in inf_tablets}}

    # ---------------------------------------------------------------- A
    print("=" * 78)
    print("A. THE PRE-REGISTERED MARGINAL-ONLY SPLIT")
    print("=" * 78)
    val_tablets, got = canonical_split(blocks, WANT)
    train = [ln for ln in el if ln.tablet not in val_tablets]
    val = [ln for ln in el if ln.tablet in val_tablets]
    sel, own, ncand = screen_numeral(train)
    res = evaluate(blocks, val_tablets)
    a, b, c, d = contingency(val, M, N)
    canon = {
        "val_tablets": sorted(val_tablets), "val_informative_blocks": got,
        "train_lines": len(train), "val_lines": len(val),
        "train_tablets": len({ln.tablet for ln in train}),
        "screen_candidates": ncand, "screen_selected_total": len(sel),
        "pair_selected_on_train": (M, N) in sel,
        "train_row": own, "validation": res,
        "val_cells": [a, b, c, d], "val_odds_ratio": odds_ratio(a, b, c, d),
    }
    out["canonical_split"] = canon
    print(f"validation tablets ({len(val_tablets)}): {sorted(val_tablets)}")
    print(f"validation informative blocks: {got}   validation lines: {len(val)}")
    print(f"train lines: {len(train)}  train tablets: {canon['train_tablets']}")
    print(f"\nre-screen on complement: {ncand} candidates, {len(sel)} selected")
    print(f"  M288-N45 selected on train? {'YES' if canon['pair_selected_on_train'] else 'NO'}")
    if own:
        print(f"  train cells {own['cells']}  OR {own['or']:.2f}  "
              f"p {own['p']:.3g}  q {own['q']:.3g}")
    print(f"\nvalidation face-blocked test:")
    print(f"  cells a,b,c,d = {a},{b},{c},{d}   OR {canon['val_odds_ratio']:.2f}")
    print(f"  overlap {res['observed_overlap']}/{res['max_overlap']} over "
          f"{res['n_val_informative']} informative blocks")
    print(f"  p = {res['p']:.4g}   p-floor = {res['p_floor']:.4g}   "
          f"power at .05: {'YES' if res['has_power_at_05'] else 'NO'}")

    # ---------------------------------------------------------------- B
    print()
    print("=" * 78)
    print(f"B. EVERY ADMISSIBLE SPLIT (validation informative blocks >= {WANT})")
    print("=" * 78)
    admissible = []
    for r in range(len(inf_tablets) + 1):
        for combo in itertools.combinations(inf_tablets, r):
            k = sum(per_tablet[t] for t in combo)
            if k < WANT:
                continue
            res_c = evaluate(blocks, set(combo))
            admissible.append({"val_tablets": list(combo), "n_val_tablets": r,
                               **res_c})
    out["n_admissible_splits"] = len(admissible)
    ps = sorted(x["p"] for x in admissible)
    floors = [x["p_floor"] for x in admissible]
    print(f"admissible splits: {len(admissible)}")
    print(f"validation p-value over splits:")
    for lab, v in (("min", ps[0]), ("5th pct", ps[int(0.05 * len(ps))]),
                   ("median", statistics.median(ps)),
                   ("95th pct", ps[int(0.95 * len(ps))]), ("max", ps[-1])):
        print(f"  {lab:10} {v:.4g}")
    frac05 = sum(p <= 0.05 for p in ps) / len(ps)
    frac01 = sum(p <= 0.01 for p in ps) / len(ps)
    print(f"  fraction of admissible splits with p <= 0.05: {frac05:.4f}")
    print(f"  fraction of admissible splits with p <= 0.01: {frac01:.4f}")
    print(f"  every admissible split has power at .05: "
          f"{all(f <= 0.05 for f in floors)}  (max floor {max(floors):.3g})")
    out["admissible_summary"] = {
        "n": len(admissible), "p_min": ps[0], "p_median": statistics.median(ps),
        "p_max": ps[-1], "p_5pct": ps[int(0.05 * len(ps))],
        "p_95pct": ps[int(0.95 * len(ps))],
        "frac_p_le_05": frac05, "frac_p_le_01": frac01,
        "max_p_floor": max(floors), "all_have_power": all(f <= 0.05 for f in floors),
    }

    # Does the complement still re-screen the pair? Sample, because each screen is
    # a full 1,430-candidate BH pass and the train sets differ by <= 15 of 1,457
    # tablets.
    rng = random.Random(SEED)
    sample = rng.sample(admissible, min(SAMPLE_SCREENS, len(admissible)))
    reselected = 0
    train_qs = []
    for x in sample:
        vt = set(x["val_tablets"])
        tr = [ln for ln in el if ln.tablet not in vt]
        s, o, _ = screen_numeral(tr)
        if (M, N) in s:
            reselected += 1
        if o:
            train_qs.append(o["q"])
    print(f"\nre-screening on the complement, {len(sample)} sampled splits:")
    print(f"  pair selected on train in {reselected}/{len(sample)} splits")
    if train_qs:
        print(f"  train q ranges {min(train_qs):.3g} .. {max(train_qs):.3g} "
              f"(threshold 0.01)")
    out["rescreen_sample"] = {"n_sampled": len(sample), "n_reselected": reselected,
                              "train_q_min": min(train_qs) if train_qs else None,
                              "train_q_max": max(train_qs) if train_qs else None}

    # ---------------------------------------------------------------- C
    print()
    print("=" * 78)
    print("C. LABEL-PERMUTATION NULL ON THE SPLIT ITSELF")
    print("=" * 78)
    print("Holds every tablet's blocks in place; permutes which tablets are labelled")
    print("validation, preserving the canonical split's tablet count. Asks whether the")
    print("observed split's validation p-value is unusual among relabellings.")
    n_val_tab = len(val_tablets)
    draws = []
    for _ in range(20000):
        combo = rng.sample(inf_tablets, n_val_tab)
        draws.append(evaluate(blocks, set(combo))["p"])
    obs_p = canon["validation"]["p"]
    below = sum(dp <= obs_p for dp in draws)
    pct = below / len(draws)
    print(f"observed canonical validation p = {obs_p:.4g}")
    print(f"label-permuted distribution ({len(draws)} draws, {n_val_tab} val tablets):")
    ds = sorted(draws)
    for lab, v in (("min", ds[0]), ("10th", ds[int(0.10 * len(ds))]),
                   ("median", statistics.median(ds)),
                   ("90th", ds[int(0.90 * len(ds))]), ("max", ds[-1])):
        print(f"  {lab:8} {v:.4g}")
    print(f"observed p sits at percentile {100 * pct:.1f} of the relabelled "
          f"distribution")
    print(f"  (P3a predicted between the 10th and 90th percentile: "
          f"{'PASS' if 0.10 <= pct <= 0.90 else 'FAIL'})")
    out["label_permutation"] = {
        "n_draws": len(draws), "n_val_tablets": n_val_tab, "observed_p": obs_p,
        "percentile_of_observed": pct, "median": statistics.median(draws),
        "p10": ds[int(0.10 * len(ds))], "p90": ds[int(0.90 * len(ds))],
        "p3a_pass": 0.10 <= pct <= 0.90,
    }

    Path("results").mkdir(exist_ok=True)
    Path("results/blockaware.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nwrote results/blockaware.json")


if __name__ == "__main__":
    main()
