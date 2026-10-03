#!/usr/bin/env python3
"""The confound-strength sensitivity curve, for all eight published pairs.

p(w) is the exact one-sided p-value under the null "the target has a reverse-face
preference of strength w, and no association with the M-sign". So

  p(1)       = the published 2026-09-04 within-tablet test
  p(w_hat)   = the same test with the face confound carried at its measured strength
  p(w -> inf)= the strongest face preference expressible in this null

The critical weight is where p crosses 0.05. If p stays below 0.05 out to a very large
w, no face preference of any strength accounts for the association, which is a complete
answer to the question the 2026-09-17 face-blocked test could not reach.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import split_name  # noqa: E402
from weighted_null import critical_weight, face_weight, load_eligible, weighted_randomization_p  # noqa: E402

from test_weighted_null import CONFIRMED  # noqa: E402

GRID = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 16.0, 64.0, 256.0, 1024.0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="holdout", choices=["holdout", "corpus"])
    args = parser.parse_args()

    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    scope = (
        [ln for ln in lines if split_name(ln.tablet) == "validation"]
        if args.scope == "holdout"
        else lines
    )
    print(f"scope = {args.scope} ({len(scope)} lines)\n")
    out = {"scope": args.scope, "scope_lines": len(scope), "grid": GRID, "pairs": {}}

    print(f"{'pair':12} {'dir':9} {'w_hat':>6} {'obs':>4} {'null_mu@1':>9} "
          f"{'null_mu@w':>9} " + " ".join(f"{('p@'+format(w,'g')):>9}" for w in GRID)
          + f" {'crit_w':>8}")
    for m_sign, n_sign, direction in CONFIRMED:
        w_hat = face_weight(lines, m_sign, n_sign)["w"]
        curve = {}
        for w in GRID:
            curve[f"{w:g}"] = weighted_randomization_p(scope, m_sign, n_sign, direction, w)
        at_hat = weighted_randomization_p(scope, m_sign, n_sign, direction, w_hat)
        crit = critical_weight(scope, m_sign, n_sign, direction)
        out["pairs"][f"{m_sign}-{n_sign}"] = {
            "direction": direction,
            "w_hat": w_hat,
            "at_w_hat": at_hat,
            "curve": curve,
            "critical_weight": crit,
        }
        crit_text = (
            f"{crit['critical_w']:8.2f}" if crit.get("critical_w")
            else f"{'>1024' if 'still clears' in crit.get('note','') else 'n/a':>8}"
        )
        print(f"{m_sign+'-'+n_sign:12} {direction:9} {w_hat:6.2f} "
              f"{curve['1']['observed_overlap']:4} {curve['1']['null_mean']:9.2f} "
              f"{at_hat['null_mean']:9.2f} "
              + " ".join(f"{curve[f'{w:g}']['p']:9.4f}" for w in GRID)
              + f" {crit_text}")

    Path("results").mkdir(exist_ok=True)
    Path(f"results/sensitivity_{args.scope}.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
