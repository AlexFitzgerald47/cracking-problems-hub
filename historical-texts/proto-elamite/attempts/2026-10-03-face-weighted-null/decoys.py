#!/usr/bin/env python3
"""P4: the weighted test's rejection rate on pairs that were never selected.

Procedure, identical in shape to the real one and run per pair:
  1. take the direction from the TRAINING buckets (1-4) odds ratio, never the holdout;
  2. measure w_hat off lines not carrying the M-sign, as the real test does;
  3. run the weighted exact test once on the bucket-0 holdout.

Decoys are every (M-sign, N-sign) pair meeting the published support minima that is
not one of the eight confirmed constraints. Most carry no association, so the
rejection rate is an upper bound on the procedure's false-positive rate: any genuine
association among the decoys inflates it, it cannot deflate it.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import odds_ratio, split_name  # noqa: E402
from weighted_null import face_weight, load_eligible, weighted_randomization_p  # noqa: E402

from test_weighted_null import CONFIRMED  # noqa: E402

EXCLUDED = {(m, n) for m, n, _ in CONFIRMED}
MIN_TRAIN_SIGN_LINES = 20
MIN_TRAIN_TARGET_LINES = 20
MIN_VALIDATION_SIGN_LINES = 5


def cells(lines, m_sign, n_sign):
    a = b = c = d = 0
    for line in lines:
        has_sign = m_sign in line.m_signs
        has_target = n_sign in line.n_signs
        if has_sign and has_target:
            a += 1
        elif has_sign:
            b += 1
        elif has_target:
            c += 1
        else:
            d += 1
    return a, b, c, d


def main() -> None:
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    train = [ln for ln in lines if split_name(ln.tablet) == "train"]
    holdout = [ln for ln in lines if split_name(ln.tablet) == "validation"]

    m_counts = Counter(s for ln in train for s in ln.m_signs)
    n_counts = Counter(s for ln in train for s in ln.n_signs)
    m_signs = sorted(s for s, c in m_counts.items() if c >= MIN_TRAIN_SIGN_LINES)
    n_signs = sorted(s for s, c in n_counts.items() if c >= MIN_TRAIN_TARGET_LINES)
    print(f"candidate grid: {len(m_signs)} M-signs x {len(n_signs)} N-signs")

    rows = []
    for m_sign in m_signs:
        for n_sign in n_signs:
            if (m_sign, n_sign) in EXCLUDED:
                continue
            ta, tb, tc, td = cells(train, m_sign, n_sign)
            if ta + tb < MIN_TRAIN_SIGN_LINES:
                continue
            va, vb, _, _ = cells(holdout, m_sign, n_sign)
            if va + vb < MIN_VALIDATION_SIGN_LINES:
                continue
            train_or = odds_ratio(ta, tb, tc, td)
            direction = "enriched" if train_or > 1 else "depleted"
            w_hat = face_weight(lines, m_sign, n_sign)["w"]
            result = weighted_randomization_p(holdout, m_sign, n_sign, direction, w_hat)
            published = weighted_randomization_p(holdout, m_sign, n_sign, direction, 1.0)
            rows.append(
                {
                    "m_sign": m_sign,
                    "n_sign": n_sign,
                    "direction": direction,
                    "train_odds_ratio": train_or,
                    "w_hat": w_hat,
                    "p_weighted": result["p"],
                    "p_floor_weighted": result["p_floor"],
                    "p_published": published["p"],
                    "has_power_05": result["p_floor"] <= 0.05,
                }
            )

    powered = [r for r in rows if r["has_power_05"]]
    def rate(items, key, alpha):
        return sum(1 for r in items if r[key] < alpha) / len(items) if items else float("nan")

    summary = {
        "decoys": len(rows),
        "decoys_with_power_at_05": len(powered),
        "weighted_reject_05_all": rate(rows, "p_weighted", 0.05),
        "weighted_reject_05_powered": rate(powered, "p_weighted", 0.05),
        "weighted_reject_01_powered": rate(powered, "p_weighted", 0.01),
        "published_reject_05_powered": rate(powered, "p_published", 0.05),
        "published_reject_01_powered": rate(powered, "p_published", 0.01),
    }
    print(json.dumps(summary, indent=2))
    print("\nmost extreme decoys under the weighted test (powered only):")
    for r in sorted(powered, key=lambda r: r["p_weighted"])[:12]:
        print(f"  {r['m_sign']}-{r['n_sign']:7} {r['direction']:9} w_hat {r['w_hat']:6.2f} "
              f"p_weighted {r['p_weighted']:.5f}  p_published {r['p_published']:.5f}")

    Path("results").mkdir(exist_ok=True)
    Path("results/decoys.json").write_text(
        json.dumps({"summary": summary, "rows": rows}, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()
