#!/usr/bin/env python3
"""Pre-registration inputs: marginals, measured face-confound strength, p-value floors.

Everything printed here is a function of block marginals and the face distribution
only. No observed overlap and no p-value is printed, so this can be run and read
before the predictions in PREDICTIONS.md are frozen.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import split_name  # noqa: E402
from weighted_null import face_weight, is_reverse, load_eligible, weighted_randomization_p  # noqa: E402

from test_weighted_null import CONFIRMED  # noqa: E402


def main() -> None:
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    holdout = [ln for ln in lines if split_name(ln.tablet) == "validation"]
    out = {}
    print(f"eligible lines {len(lines)}, holdout (bucket 0) {len(holdout)}")
    print(f"reverse share: corpus {sum(map(is_reverse, lines))/len(lines):.3f} "
          f"holdout {sum(map(is_reverse, holdout))/len(holdout):.3f}\n")
    header = (f"{'pair':12} {'w_hat':>7} {'rev%':>6} {'obv%':>6} "
              f"{'floor@1':>9} {'floor@w':>9} {'floor@4w':>9} {'nblk':>5}")
    print(header)
    for m_sign, n_sign, direction in CONFIRMED:
        info = face_weight(lines, m_sign, n_sign)
        w_hat = info["w"]
        row = {"direction": direction, "face_weight": info}
        for label, w in (("floor_w1", 1.0), ("floor_what", w_hat), ("floor_4what", 4 * w_hat)):
            res = weighted_randomization_p(holdout, m_sign, n_sign, direction, w)
            row[label] = {
                "p_floor": res["p_floor"],
                "blocks": res["blocks"],
                "max_possible_overlap": res["max_possible_overlap"],
                "min_possible_overlap": res["min_possible_overlap"],
            }
        out[f"{m_sign}-{n_sign}"] = row
        print(f"{m_sign+'-'+n_sign:12} {w_hat:7.2f} {info['reverse_rate']*100:6.2f} "
              f"{info['obverse_rate']*100:6.2f} {row['floor_w1']['p_floor']:9.2e} "
              f"{row['floor_what']['p_floor']:9.2e} {row['floor_4what']['p_floor']:9.2e} "
              f"{row['floor_w1']['blocks']:5}")
    Path("results").mkdir(exist_ok=True)
    Path("results/preflight.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
