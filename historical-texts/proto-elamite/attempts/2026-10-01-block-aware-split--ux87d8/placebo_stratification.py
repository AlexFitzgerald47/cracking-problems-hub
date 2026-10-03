#!/usr/bin/env python3
"""Does a pair die under richness blocking because of richness, or because of blocking?

Blocking on (tablet, face, other-N-count) fragments the corpus into smaller blocks, and
smaller blocks mean less power. The p-value floor already separates those two cases
formally -- a pair whose floor stays below 0.05 had the power to confirm and did not --
but the floor is an extreme bound and a reader may reasonably want the concrete version.

This is the concrete version. Within each (tablet, face) block, the lines' richness
stratum labels are shuffled among the lines. That preserves every block's size exactly,
so the fragmentation is identical, and destroys only the association between block
membership and how numeral-rich a line is. If a pair dies under the real stratification
but survives the placebo, richness is what killed it.

Usage:
    python3 placebo_stratification.py --replicates 500
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence

sys.path.insert(0, str(Path(__file__).resolve().parent))

from block_aware_split import (  # noqa: E402
    BLOCK_KEYS,
    block_report,
    other_n_count,
)
from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402
from structure_associations import Line  # noqa: E402


def placebo_keys(
    lines: Sequence[Line], target: str, rng: random.Random
) -> dict[int, object]:
    """Shuffle richness labels within each (tablet, face), preserving block sizes."""
    grouped: dict[object, list[int]] = defaultdict(list)
    for index, line in enumerate(lines):
        grouped[(line.tablet, line.surface)].append(index)
    keys: dict[int, object] = {}
    for face, indices in grouped.items():
        labels = [other_n_count(lines[i], target) for i in indices]
        rng.shuffle(labels)
        for i, label in zip(indices, labels):
            keys[i] = (*face, label)
    return keys


def placebo_run(
    lines: Sequence[Line], m_sign: str, target: str, direction: str,
    replicates: int, seed: int = 20261001,
) -> dict:
    rng = random.Random(seed)
    real = block_report(
        lines, m_sign, target, BLOCK_KEYS["tablet+face+richness"], direction
    )
    indexed = list(lines)
    p_values, floors, informative = [], [], []
    for _ in range(replicates):
        keys = placebo_keys(indexed, target, rng)
        lookup = {id(line): keys[i] for i, line in enumerate(indexed)}
        report = block_report(
            indexed, m_sign, target, lambda line, _t: lookup[id(line)], direction
        )
        p_values.append(report["p"])
        floors.append(report["p_floor"])
        informative.append(report["informative_blocks"])
    p_values.sort()
    n = len(p_values)
    at_or_above = sum(p >= real["p"] for p in p_values) / n
    return {
        "pair": f"{m_sign}-{target}",
        "direction": direction,
        "real_p": real["p"],
        "real_p_floor": real["p_floor"],
        "real_informative_blocks": real["informative_blocks"],
        "real_has_power": real["has_power_at_05"],
        "placebo_replicates": n,
        "placebo_median_p": p_values[n // 2],
        "placebo_p05": p_values[max(0, int(0.05 * n) - 1)],
        "placebo_p95": p_values[min(n - 1, int(0.95 * n))],
        "placebo_fraction_significant": sum(p <= 0.05 for p in p_values) / n,
        "placebo_fraction_at_or_above_real_p": at_or_above,
        "placebo_mean_informative_blocks": sum(informative) / n,
        "placebo_mean_floor": sum(floors) / n,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=500)
    parser.add_argument("--json", type=Path, default=Path("results/placebo.json"))
    args = parser.parse_args()

    corpus = Path(
        (Path(__file__).resolve().parent.parent / "2026-09-17-exact-form-and-face"
         / "corpus_path.txt").read_text().strip()
    )
    raw, _ = load_lines(corpus)
    lines = eligible(raw)

    rows = [
        placebo_run(lines, m, n, d, args.replicates) for m, n, d in CONFIRMED
    ]
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")

    print(f"placebo: richness labels shuffled within (tablet, face); "
          f"{args.replicates} replicates\n")
    print(f"{'pair':12}{'real p':>10}{'floor':>9}{'infB':>5} | "
          f"{'placebo med':>12}{'5%':>9}{'95%':>9}{'infB':>6}{'P(sig)':>8} | verdict")
    for r in rows:
        if r["real_p"] <= 0.05:
            verdict = "survives richness"
        elif not r["real_has_power"]:
            verdict = "no power"
        elif r["placebo_median_p"] <= 0.05:
            verdict = "RICHNESS kills it"
        else:
            verdict = "blocking kills it"
        print(f"{r['pair']:12}{r['real_p']:10.4f}{r['real_p_floor']:9.1e}"
              f"{r['real_informative_blocks']:5} | {r['placebo_median_p']:12.4f}"
              f"{r['placebo_p05']:9.4f}{r['placebo_p95']:9.4f}"
              f"{r['placebo_mean_informative_blocks']:6.1f}"
              f"{r['placebo_fraction_significant']:8.3f} | {verdict}")
    print(f"\nwrote {args.json}")


if __name__ == "__main__":
    main()
