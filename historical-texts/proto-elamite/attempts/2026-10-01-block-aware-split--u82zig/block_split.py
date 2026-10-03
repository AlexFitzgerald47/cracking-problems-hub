#!/usr/bin/env python3
"""Block-aware split for the M288-N45 constraint (folder item 1 of 2026-09-17).

The problem. The 2026-09-04 design splits tablets by sha256(P-number) % 5 and
validates on bucket 0. Under the face-blocked null of 2026-09-17 that holdout
leaves M288-N45 with only 4 informative (tablet, face) blocks and a p-value
floor of 0.12: the test cannot return a significant answer whatever the data
say. The pair was therefore neither confirmed nor refuted.

The fix. Stratify the tablet-level split on a quantity computed from BLOCK
MARGINALS ONLY -- whether a tablet contributes a (tablet, face) block in which
the exact test has any freedom at all. Marginals (block size, sign-line count,
target-line count) are exactly what the conditional test conditions on, so
selecting blocks on them is selection on an ancillary statistic and does not
disturb the null distribution. The within-block overlap, which is the quantity
under test, is never consulted by the split.

The split:
  stratum I   tablets contributing >= 1 informative block for the pair under test.
              Ordered by sha256(tablet) and added to validation until validation
              holds >= MIN_INFORMATIVE_BLOCKS informative blocks; the rest to train.
  stratum II  every other tablet. Published rule: sha256 bucket 0 -> validation.

Candidates are then re-screened on train alone with the published screening
rule, and validated with the published confirmation rule, with the exact test's
block key changed from `tablet` to `(tablet, face)`.

No lexical, phonetic or metrological value is assigned to any sign here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import (  # noqa: E402
    bh_adjust,
    corpus_digest,
    fisher_exact_two_sided,
    hypergeom_probability,
    odds_ratio,
)
from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402

MIN_INFORMATIVE_BLOCKS = 10
FACE_KEY: Callable = lambda ln: (ln.tablet, ln.surface)  # noqa: E731
TABLET_KEY: Callable = lambda ln: ln.tablet  # noqa: E731


# ----------------------------------------------------------- marginals only

def block_freedom(lines: Sequence, m_sign: str, n_sign: str, key=FACE_KEY):
    """Per-block (lo, hi, total, s, t). Marginals only -- no overlap read."""
    blocks = defaultdict(list)
    for ln in lines:
        blocks[key(ln)].append(ln)
    out = {}
    for bk, bl in blocks.items():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        out[bk] = {
            "total": total,
            "s": s,
            "t": t,
            "lo": max(0, s - (total - t)),
            "hi": min(s, t),
        }
    return out


def informative_tablets(lines, m_sign, n_sign):
    """Tablets contributing >=1 informative face block, and each one's count."""
    fr = block_freedom(lines, m_sign, n_sign)
    per_tablet = defaultdict(int)
    for (tablet, _face), v in fr.items():
        if v["hi"] > v["lo"]:
            per_tablet[tablet] += 1
    return dict(per_tablet)


def hash_order(tablet: str) -> str:
    return hashlib.sha256(tablet.encode("ascii")).hexdigest()


def published_bucket(tablet: str) -> int:
    return int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5


def build_split(lines, m_sign, n_sign, min_blocks=MIN_INFORMATIVE_BLOCKS,
                exclude_tablets=frozenset()):
    """Stratified tablet-level split. Returns (validation_tablets, diagnostics)."""
    per_tablet = informative_tablets(lines, m_sign, n_sign)
    stratum_i = sorted(
        (t for t in per_tablet if t not in exclude_tablets), key=hash_order
    )
    validation = set()
    blocks_in_validation = 0
    for tablet in stratum_i:
        if blocks_in_validation >= min_blocks:
            break
        validation.add(tablet)
        blocks_in_validation += per_tablet[tablet]
    all_tablets = {ln.tablet for ln in lines}
    stratum_ii = sorted(all_tablets - set(per_tablet))
    for tablet in stratum_ii:
        if published_bucket(tablet) == 0:
            validation.add(tablet)
    diag = {
        "informative_tablets_total": len(per_tablet),
        "informative_blocks_total": sum(per_tablet.values()),
        "stratum_i_in_validation": sorted(t for t in validation if t in per_tablet),
        "stratum_i_in_train": sorted(t for t in per_tablet if t not in validation),
        "informative_blocks_in_validation": blocks_in_validation,
        "informative_blocks_in_train": sum(per_tablet.values()) - blocks_in_validation,
        "min_blocks_target": min_blocks,
        "validation_tablet_count": len(validation),
        "train_tablet_count": len(all_tablets) - len(validation),
    }
    return validation, diag


# ----------------------------------------------------------- the exact test

def blocked_test(lines, m_sign, n_sign, direction, key=FACE_KEY):
    """Exact blocked randomization test, with the achievable p-floor beside it."""
    fr = block_freedom(lines, m_sign, n_sign, key)
    blocks = defaultdict(list)
    for ln in lines:
        blocks[key(ln)].append(ln)
    dist = [1.0]
    observed = forced = maximum = 0
    informative = 0
    for bk, bl in blocks.items():
        v = fr[bk]
        observed += sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        forced += v["lo"]
        maximum += v["hi"]
        if v["hi"] > v["lo"]:
            informative += 1
        local = [0.0] * (v["hi"] + 1)
        for k in range(v["lo"], v["hi"] + 1):
            local[k] = hypergeom_probability(k, v["s"], v["t"], v["total"])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    if direction == "enriched":
        p = min(1.0, sum(dist[observed:]))
        p_floor = min(1.0, sum(dist[maximum:]))
    else:
        lowest = next(i for i, v in enumerate(dist) if v > 0)
        p = min(1.0, sum(dist[: observed + 1]))
        p_floor = min(1.0, sum(dist[: lowest + 1]))
    return {
        "p": p,
        "p_floor": p_floor,
        "observed_overlap": observed,
        "forced_overlap": forced,
        "max_possible_overlap": maximum,
        "freedom": maximum - forced,
        "freedom_used": observed - forced,
        "informative_blocks": informative,
        "blocks": len(blocks),
        "has_power_at_05": p_floor <= 0.05,
    }


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


# ----------------------------------------------------------- screen on train

def screen(train_lines, min_sign_lines=20, min_target_lines=20):
    """The published 2026-09-04 screening rule, run on an arbitrary train set."""
    signs = sorted({s for ln in train_lines for s in ln.m_signs})
    targets = sorted({n for ln in train_lines for n in ln.n_signs})
    raw = []
    for n_sign in targets:
        for m_sign in signs:
            a, b, c, d = contingency(train_lines, m_sign, n_sign)
            if a + b < min_sign_lines or a + c < min_target_lines:
                continue
            raw.append(
                {
                    "m_sign": m_sign,
                    "n_sign": n_sign,
                    "cells": (a, b, c, d),
                    "odds_ratio": odds_ratio(a, b, c, d),
                    "p": fisher_exact_two_sided(a, b, c, d),
                }
            )
    qs = bh_adjust([r["p"] for r in raw])
    for r, q in zip(raw, qs):
        r["q"] = q
    selected = [
        r for r in raw
        if r["q"] <= 0.01 and (r["odds_ratio"] >= 3.0 or r["odds_ratio"] <= 1 / 3.0)
    ]
    return selected, raw


def validate(val_lines, selected, key=FACE_KEY):
    """Published confirmation rule with the block key swapped for (tablet, face)."""
    rows = []
    for item in selected:
        direction = "enriched" if item["odds_ratio"] > 1 else "depleted"
        cells = contingency(val_lines, item["m_sign"], item["n_sign"])
        res = blocked_test(val_lines, item["m_sign"], item["n_sign"], direction, key)
        rows.append(
            {
                "m_sign": item["m_sign"],
                "n_sign": item["n_sign"],
                "direction": direction,
                "train_odds_ratio": item["odds_ratio"],
                "train_q": item["q"],
                "validation_cells": cells,
                "validation_odds_ratio": odds_ratio(*cells),
                **res,
            }
        )
    qs = bh_adjust([r["p"] for r in rows])
    for r, q in zip(rows, qs):
        r["q"] = q
        vor, tor = r["validation_odds_ratio"], r["train_odds_ratio"]
        r["same_direction"] = (tor > 1 and vor > 1) or (tor < 1 and vor < 1)
        r["confirmed"] = bool(
            r["validation_cells"][0] + r["validation_cells"][1] >= 5
            and r["same_direction"]
            and q <= 0.05
            and (vor >= 1.5 or vor <= 1 / 1.5)
        )
    return sorted(rows, key=lambda r: r["q"])


# ----------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", default="M288-N45")
    ap.add_argument("--min-blocks", type=int, default=MIN_INFORMATIVE_BLOCKS)
    ap.add_argument("--json", default="results/block_split.json")
    args = ap.parse_args()
    m_sign, n_sign = args.pair.split("-")

    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, files = load_lines(corpus)
    el = eligible(lines)

    val_tablets, diag = build_split(el, m_sign, n_sign, args.min_blocks)
    train = [ln for ln in el if ln.tablet not in val_tablets]
    val = [ln for ln in el if ln.tablet in val_tablets]

    print(f"corpus digest {corpus_digest(files)}")
    print(f"eligible {len(el)}  train lines {len(train)}  validation lines {len(val)}")
    print(json.dumps(diag, indent=2))

    selected, raw = screen(train)
    print(f"\nscreened on train: {len(raw)} testable cells -> {len(selected)} candidates")
    target_hit = [r for r in selected if r["m_sign"] == m_sign and r["n_sign"] == n_sign]
    if target_hit:
        r = target_hit[0]
        print(f"  {args.pair} RE-SCREENS on train: OR {r['odds_ratio']:.2f} "
              f"q {r['q']:.3g} cells {r['cells']}")
    else:
        print(f"  {args.pair} DOES NOT re-screen on train -- "
              "the validation test would not be a confirmation of a screened candidate")
        bare = [r for r in raw if r["m_sign"] == m_sign and r["n_sign"] == n_sign]
        if bare:
            r = bare[0]
            print(f"  (its train stats: OR {r['odds_ratio']:.2f} q {r['q']:.3g} "
                  f"cells {r['cells']})")

    rows = validate(val, selected)
    print(f"\n{'pair':12} {'dir':9} {'OR_val':>7} {'p':>9} {'floor':>8} "
          f"{'q':>9} {'obs/frc/max':>13} {'infB':>5} conf")
    for r in rows:
        counts = (f"{r['observed_overlap']}/{r['forced_overlap']}"
                  f"/{r['max_possible_overlap']}")
        print(f"{r['m_sign']+'-'+r['n_sign']:12} {r['direction']:9} "
              f"{r['validation_odds_ratio']:7.2f} {r['p']:9.5f} {r['p_floor']:8.4f} "
              f"{r['q']:9.5f} "
              f"{counts:>13} "
              f"{r['informative_blocks']:5} {'YES' if r['confirmed'] else ''}")

    out = {
        "pair": args.pair,
        "corpus_sha256_lf": corpus_digest(files),
        "split": diag,
        "train_lines": len(train),
        "validation_lines": len(val),
        "screened_candidates": len(selected),
        "testable_cells": len(raw),
        "target_rescreened": bool(target_hit),
        "target_train": target_hit[0] if target_hit else None,
        "validation_rows": rows,
    }
    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / args.json).write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
