#!/usr/bin/env python3
"""P6: is the unblocked training screen specific to a line-level association at all?

The 2026-09-04 design selects candidates with an UNBLOCKED Fisher test on training
lines and reports `train_p`/`train_q` in the published results table. The calibration
run showed that for M288-N45 the screen fires at p <= 7e-6 in 20,000 of 20,000 draws
of a null with no within-face association whatsoever. If that holds for the other seven
pairs, the screen's q-values are a power filter and not evidence, and the published
table should be read that way.

Null: permute the pair's target N-sign within each (tablet, face) block over the whole
corpus. This destroys every within-face association while preserving each block's line
count, its sign-bearing count and its target count.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fisher_exact_two_sided, load_eligible, odds_ratio  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "2026-09-17-exact-form-and-face"))
from face_and_form import CONFIRMED  # noqa: E402

DRAWS = 4000
SEED = 20261003


def main():
    el = load_eligible()
    by_face = defaultdict(list)
    for ln in el:
        by_face[(ln.tablet, ln.surface)].append(ln)
    faces = list(by_face.values())
    total_lines = len(el)

    out = {"draws": DRAWS, "pairs": {}}
    print(f"{'pair':12} {'dir':9} {'obsOR':>7} {'obs p':>10} | "
          f"{'null OR med':>11} {'null p med':>11} {'P(p<=1e-5)':>11} {'P(p<=.05)':>10}")
    print("-" * 96)
    for m_sign, n_sign, direction in CONFIRMED:
        # precompute per-face: has-M flags, target count
        units = []
        for bl in faces:
            flags = [m_sign in ln.m_signs for ln in bl]
            t = sum(n_sign in ln.n_signs for ln in bl)
            units.append((flags, t, len(bl)))
        s_total = sum(sum(f) for f, _, _ in units)
        t_total = sum(t for _, t, _ in units)
        obs_a = sum(1 for bl in faces for ln in bl
                    if m_sign in ln.m_signs and n_sign in ln.n_signs)

        def table(a):
            b = s_total - a
            c = t_total - a
            d = total_lines - a - b - c
            return a, b, c, d

        obs_or = odds_ratio(*table(obs_a))
        obs_p = fisher_exact_two_sided(*table(obs_a))

        rng = random.Random(SEED)
        ors, ps = [], []
        for _ in range(DRAWS):
            a = 0
            for flags, t, n in units:
                if t == 0:
                    continue
                if t == n:
                    a += sum(flags)
                    continue
                for i in rng.sample(range(n), t):
                    if flags[i]:
                        a += 1
            ors.append(odds_ratio(*table(a)))
            ps.append(fisher_exact_two_sided(*table(a)))
        med_or = statistics.median(ors)
        med_p = statistics.median(ps)
        f5 = sum(p <= 1e-5 for p in ps) / DRAWS
        f05 = sum(p <= 0.05 for p in ps) / DRAWS
        print(f"{m_sign+'-'+n_sign:12} {direction:9} {obs_or:7.2f} {obs_p:10.2e} | "
              f"{med_or:11.2f} {med_p:11.2e} {f5:11.4f} {f05:10.4f}")
        out["pairs"][f"{m_sign}-{n_sign}"] = {
            "direction": direction, "observed_or": obs_or, "observed_p": obs_p,
            "null_or_median": med_or, "null_or_min": min(ors), "null_or_max": max(ors),
            "null_p_median": med_p, "null_p_min": min(ps), "null_p_max": max(ps),
            "frac_null_p_le_1e5": f5, "frac_null_p_le_05": f05,
        }
    Path("results").mkdir(exist_ok=True)
    Path("results/screen_specificity.json").write_text(json.dumps(out, indent=2))
    print("\nwrote results/screen_specificity.json")


if __name__ == "__main__":
    main()
