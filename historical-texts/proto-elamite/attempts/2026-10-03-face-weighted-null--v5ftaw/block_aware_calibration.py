#!/usr/bin/env python3
"""Type-I error of the block-aware split, under a generator where the answer is known.

`block_aware_decoys.py` found the procedure rejecting 22% of decoy pairs at alpha=0.05.
That is not yet evidence of inflation: the split deliberately routes the largest, densest
tablets into validation, so it also has far more power than the holdout tests, and a
decoy set drawn from a structured corpus contains real associations. More power and
inflation look identical in that statistic.

This separates them. The generator is `calibrate.redeal`: real tablets, real faces, real
line counts, real M-sign assignments, each tablet's target count preserved, a planted
face skew, and NO association between the target and any M-sign. Every rejection is
therefore a false positive by construction.

The whole procedure is re-run per replicate, including recomputing the split from the
synthetic data's own marginals, because that is what a session following the handover
would do.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import odds_ratio, split_name  # noqa: E402
from weighted_null import face_weight, load_eligible, weighted_randomization_p  # noqa: E402

from block_aware_decoys import split_for  # noqa: E402
from block_aware_split import face_blocked_p  # noqa: E402
from calibrate import redeal  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=600)
    parser.add_argument("--pair", default="M288,N45")
    parser.add_argument("--seed", type=int, default=771103)
    args = parser.parse_args()

    m_sign, n_sign = args.pair.split(",")
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    w_hat = face_weight(lines, m_sign, n_sign)["w"]
    rng = random.Random(args.seed)

    block_aware_p: list[float] = []
    weighted_holdout_p: list[float] = []
    skipped = 0
    for _ in range(args.replicates):
        synthetic = redeal(lines, n_sign, w_hat, rng)
        chosen, _, held = split_for(synthetic, m_sign, n_sign)
        if held < 10:
            skipped += 1
        else:
            validation = [ln for ln in synthetic if ln.tablet in chosen]
            train = [ln for ln in synthetic if ln.tablet not in chosen]
            a = b = c = d = 0
            for ln in train:
                has_sign = m_sign in ln.m_signs
                has_target = n_sign in ln.n_signs
                if has_sign and has_target:
                    a += 1
                elif has_sign:
                    b += 1
                elif has_target:
                    c += 1
                else:
                    d += 1
            direction = "enriched" if odds_ratio(a, b, c, d) > 1 else "depleted"
            block_aware_p.append(
                face_blocked_p(validation, m_sign, n_sign, direction)["p"]
            )
        holdout = [ln for ln in synthetic if split_name(ln.tablet) == "validation"]
        weighted_holdout_p.append(
            weighted_randomization_p(holdout, m_sign, n_sign, "enriched", w_hat)["p"]
        )

    def report(name, values):
        values = sorted(values)
        row = {
            "test": name,
            "n": len(values),
            "reject_05": sum(1 for p in values if p < 0.05) / len(values),
            "reject_01": sum(1 for p in values if p < 0.01) / len(values),
            "median_p": values[len(values) // 2],
            "p05_quantile": values[max(0, int(0.05 * len(values)) - 1)],
        }
        print(f"{name:46} n={row['n']:4}  rej@.05 {row['reject_05']:.3f}  "
              f"rej@.01 {row['reject_01']:.3f}  median {row['median_p']:.3f}")
        return row

    print(f"{m_sign}-{n_sign}: no association planted, face skew planted at "
          f"w_hat={w_hat:.3f}, {args.replicates} replicates\n")
    rows = [
        report("block-aware split, face-blocked (handover item 1)", block_aware_p),
        report("weighted null on bucket-0 holdout (this session)", weighted_holdout_p),
    ]
    out = {"pair": f"{m_sign}-{n_sign}", "planted_w": w_hat,
           "replicates": args.replicates, "skipped_replicates": skipped, "rows": rows}
    Path("results").mkdir(exist_ok=True)
    Path("results/block_aware_calibration.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
