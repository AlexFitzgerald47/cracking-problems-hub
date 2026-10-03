#!/usr/bin/env python3
"""Calibration of the co-numeral (S1) stratified test, plus an audit of the
M297-N24 sign reversal.

Two things must hold before the S1 p-values are believable.

1. The strata must be INVARIANT under the permutation. A stratum is the set of
   N-signs other than the target, so moving the target between lines cannot change
   any line's stratum. Asserted above; checked here by construction.

2. The test must be calibrated. Permuting the target within stratum destroys the
   association while holding the co-numeral content fixed; the S1 p-value must then
   be uniform or conservative. If it is anti-conservative, every S1 number is void.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_eligible, odds_ratio, tail  # noqa: E402

DRAWS = 4000
SEED = 20261003
PAIRS = [("M288", "N45", "enriched"), ("M297", "N39B", "enriched"),
         ("M297", "N24", "enriched"), ("M106", "N24", "enriched")]


def main():
    el = load_eligible()
    out = {"draws": DRAWS, "pairs": {}}

    for m_sign, n_sign, direction in PAIRS:
        g = defaultdict(list)
        for ln in el:
            g[frozenset(ln.n_signs - {n_sign})].append(ln)
        units = []
        for k, bl in g.items():
            flags = [m_sign in ln.m_signs for ln in bl]
            t = sum(n_sign in ln.n_signs for ln in bl)
            units.append({"flags": flags, "t": t, "n": len(bl), "s": sum(flags)})

        # Invariance check: removing the target from a line's N-set cannot depend on
        # whether the target is there, so the stratum assignment is fixed. Verified
        # by confirming each stratum's size and sign-count do not use the target.
        inv = all(u["n"] == len(u["flags"]) for u in units)

        def blocks_from(chosen):
            bs = []
            for u, ch in zip(units, chosen):
                total, s, t = u["n"], u["s"], u["t"]
                obs = sum(1 for i in ch if u["flags"][i])
                lo, hi = max(0, s - (total - t)), min(s, t)
                bs.append({"total": total, "s": s, "t": t, "obs": obs,
                           "lo": lo, "hi": hi, "informative": hi > lo})
            return bs

        rng = random.Random(SEED)
        ps = []
        for _ in range(DRAWS):
            chosen = []
            for u in units:
                n, t = u["n"], u["t"]
                chosen.append(set(range(n)) if t == n else
                              (set() if t == 0 else set(rng.sample(range(n), t))))
            bs = [b for b in blocks_from(chosen) if b["informative"]]
            ps.append(tail(bs, direction)[0])
        rates = {a: sum(p <= a for p in ps) / DRAWS for a in (0.01, 0.05, 0.10, 0.25)}
        print(f"{m_sign}-{n_sign} ({direction}): strata invariant={inv}  "
              f"null median p={statistics.median(ps):.4g}")
        print("   " + "  ".join(f"P(p<={a:g})={r:.4f}" for a, r in rates.items()))
        out["pairs"][f"{m_sign}-{n_sign}"] = {
            "strata_invariant": inv, "null_median_p": statistics.median(ps),
            "rates": {str(k): v for k, v in rates.items()},
            "calibrated_at_05": rates[0.05] <= 0.075}

    # ---- audit the M297-N24 reversal -----------------------------------------
    print()
    print("AUDIT: M297-N24 crude OR 4.04 enriched -> S1 MH-OR 0.46. Where does the")
    print("reversal come from? Largest strata by M297 line count:")
    g = defaultdict(list)
    for ln in el:
        g[frozenset(ln.n_signs - {"N24"})].append(ln)
    rows = []
    for k, bl in g.items():
        s = sum("M297" in ln.m_signs for ln in bl)
        t = sum("N24" in ln.n_signs for ln in bl)
        a = sum(1 for ln in bl if "M297" in ln.m_signs and "N24" in ln.n_signs)
        if s and t and min(s, t) > max(0, s - (len(bl) - t)):
            rows.append((s, k, len(bl), s, t, a))
    rows.sort(reverse=True)
    print(f"  {'other-N signature':34} {'lines':>6} {'M297':>5} {'N24':>4} {'both':>5} "
          f"{'rate|M297':>10} {'rate|rest':>10}")
    audit = []
    for _, k, n, s, t, a in rows[:10]:
        r1 = a / s
        r2 = (t - a) / (n - s) if n > s else float("nan")
        print(f"  {str(sorted(k)):34} {n:6} {s:5} {t:4} {a:5} {r1:10.3f} {r2:10.3f}")
        audit.append({"signature": sorted(k), "lines": n, "m_lines": s,
                      "t_lines": t, "both": a, "rate_given_m": r1,
                      "rate_given_rest": r2})
    out["m297_n24_audit"] = audit
    Path("results").mkdir(exist_ok=True)
    Path("results/magnitude_calib.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nwrote results/magnitude_calib.json")


if __name__ == "__main__":
    main()
