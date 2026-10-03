#!/usr/bin/env python3
"""P5: is the published within-tablet test actually inflated by the face confound,
and does the weighted null fix it?

Generator. Real tablets, real faces, real line counts, real M-sign assignments. Only
the target N-sign is re-dealt, and it is re-dealt so that

  * each tablet keeps its observed target count  (tablet clustering preserved exactly)
  * a reverse line is `w_plant` times as likely to receive the target as an obverse one
  * the target has NO relationship to the M-sign whatsoever

So every rejection under this generator is a false positive, and any excess over the
nominal rate is the face confound operating through the permutation's freedom to move
the target between faces.

Reported for each test: rejection rate at alpha = 0.05 and 0.01. The published
2026-09-04 test is the w = 1 row.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import Line, split_name  # noqa: E402
from weighted_null import (  # noqa: E402
    face_weight,
    is_reverse,
    load_eligible,
    weighted_randomization_p,
)


def redeal(lines, n_sign, w_plant, rng):
    """Re-deal the target within tablet, face-weighted, independent of every M-sign."""
    by_tablet = defaultdict(list)
    for index, line in enumerate(lines):
        by_tablet[line.tablet].append(index)
    carries = [False] * len(lines)
    for indices in by_tablet.values():
        count = sum(n_sign in lines[i].n_signs for i in indices)
        if count == 0:
            continue
        if count == len(indices):
            for i in indices:
                carries[i] = True
            continue
        pool = list(indices)
        weights = [w_plant if is_reverse(lines[i]) else 1.0 for i in pool]
        for _ in range(count):
            total = sum(weights)
            threshold = rng.random() * total
            cumulative = 0.0
            for position, weight in enumerate(weights):
                cumulative += weight
                if cumulative >= threshold:
                    break
            carries[pool[position]] = True
            pool.pop(position)
            weights.pop(position)
    out = []
    for index, line in enumerate(lines):
        others = frozenset(s for s in line.n_signs if s != n_sign)
        n_signs = others | {n_sign} if carries[index] else others
        out.append(
            Line(
                tablet=line.tablet,
                surface=line.surface,
                label=line.label,
                ordinal_on_surface=line.ordinal_on_surface,
                text=line.text,
                m_signs=line.m_signs,
                n_signs=frozenset(n_signs),
                damaged=line.damaged,
            )
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=2000)
    parser.add_argument("--pair", default="M288,N45")
    parser.add_argument("--seed", type=int, default=20261003)
    parser.add_argument("--scope", default="holdout", choices=["holdout", "corpus"])
    parser.add_argument("--out", default="results/calibration.json")
    args = parser.parse_args()

    m_sign, n_sign = args.pair.split(",")
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    w_hat = face_weight(lines, m_sign, n_sign)["w"]
    scope = (
        [ln for ln in lines if split_name(ln.tablet) == "validation"]
        if args.scope == "holdout"
        else lines
    )
    rng = random.Random(args.seed)

    # Planted confound strengths: none, the measured value, and two exaggerations.
    plants = [1.0, w_hat, 2 * w_hat, 4 * w_hat]
    tests = [("w=1 (published 2026-09-04 test)", 1.0), ("w=w_hat (weighted)", w_hat)]
    results = {
        "pair": f"{m_sign}-{n_sign}",
        "scope": args.scope,
        "scope_lines": len(scope),
        "w_hat": w_hat,
        "replicates": args.replicates,
        "seed": args.seed,
        "cells": [],
    }

    print(f"{m_sign}-{n_sign}  scope={args.scope} ({len(scope)} lines)  "
          f"w_hat={w_hat:.3f}  replicates={args.replicates}\n")
    print(f"{'planted w':>10}  {'test':34} {'rej@.05':>8} {'rej@.01':>8} {'median p':>9}")
    for w_plant in plants:
        p_values = {label: [] for label, _ in tests}
        for _ in range(args.replicates):
            synthetic = redeal(scope, n_sign, w_plant, rng)
            for label, w_test in tests:
                p_values[label].append(
                    weighted_randomization_p(
                        synthetic, m_sign, n_sign, "enriched", w_test
                    )["p"]
                )
        for label, _ in tests:
            values = sorted(p_values[label])
            rejection_05 = sum(1 for p in values if p < 0.05) / len(values)
            rejection_01 = sum(1 for p in values if p < 0.01) / len(values)
            median = values[len(values) // 2]
            results["cells"].append(
                {
                    "planted_w": w_plant,
                    "test": label,
                    "reject_05": rejection_05,
                    "reject_01": rejection_01,
                    "median_p": median,
                }
            )
            print(f"{w_plant:10.3f}  {label:34} {rejection_05:8.3f} "
                  f"{rejection_01:8.3f} {median:9.3f}")
        print()

    Path("results").mkdir(exist_ok=True)
    Path(args.out).write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
