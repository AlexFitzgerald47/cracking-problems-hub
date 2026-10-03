#!/usr/bin/env python3
"""P7: is M288-N45 about M288, or about the quantity being large?

N45 is the top-magnitude member of a numeral series whose lower members are
N01/N14/N34, and the descriptive picture says so loudly: N45 lines carry 3.07 distinct
N-signs against 1.32 elsewhere, N34 is 11.3x enriched and N14 3.3x enriched on N45
lines while N01 is DEPLETED (0.571 vs 0.739). That is what a large quantity written out
additively looks like. If M288's lines carry larger quantities than average, the
M288-N45 association follows with no commodity-specific content at all.

The test holds the rest of the numeral expression constant. A stratum is the exact set
of OTHER N-signs on the line, so two lines in the same stratum write the same quantity
apart from N45 itself; the target is then permuted within stratum. No numeral is
assigned a value anywhere -- the strata are the observed co-occurring signs.

Two stratifications:
  S1  other-N signature alone
  S2  (tablet, face, other-N signature) -- adds the face control on top

Reported with the p-floor, because S2 will mostly produce singleton strata and a
test with no power must not be read as a refutation.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import load_eligible, odds_ratio, tail  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "2026-09-17-exact-form-and-face"))
from face_and_form import CONFIRMED  # noqa: E402


def strata_blocks(lines, m_sign, n_sign, key):
    g = defaultdict(list)
    for ln in lines:
        g[key(ln)].append(ln)
    out = []
    for k, bl in g.items():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo, hi = max(0, s - (total - t)), min(s, t)
        out.append({"key": k, "total": total, "s": s, "t": t, "obs": obs,
                    "lo": lo, "hi": hi, "informative": hi > lo})
    return out


def mantel_haenszel(blocks):
    """Stratified odds ratio; strata with a zero margin contribute nothing."""
    num = den = 0.0
    for b in blocks:
        a = b["obs"]
        bb = b["s"] - a
        c = b["t"] - a
        d = b["total"] - b["s"] - b["t"] + a
        n = b["total"]
        if n == 0:
            continue
        num += a * d / n
        den += bb * c / n
    return (num / den) if den else float("inf")


def run(lines, m_sign, n_sign, direction, key, label):
    blocks = strata_blocks(lines, m_sign, n_sign, key)
    inf = [b for b in blocks if b["informative"]]
    p, floor, obs, extreme = tail(inf, direction)
    return {"stratification": label, "n_strata": len(blocks),
            "n_informative": len(inf),
            "mean_stratum_size": sum(b["total"] for b in blocks) / max(1, len(blocks)),
            "p": p, "p_floor": floor, "observed_overlap": obs,
            "extreme_overlap": extreme, "has_power_at_05": floor <= 0.05,
            "mh_odds_ratio": mantel_haenszel(inf) if inf else None}


def main():
    el = load_eligible()
    out = {"pairs": {}}

    def other_sig(ln, n_sign):
        return frozenset(ln.n_signs - {n_sign})

    print("Unstratified corpus-wide odds ratio, then the same pair with the rest of")
    print("the numeral expression held constant.")
    print()
    hdr = (f"{'pair':12} {'dir':9} {'crudeOR':>8} | {'S1 strata':>9} {'inf':>4} "
           f"{'S1 MH-OR':>9} {'S1 p':>9} {'S1 floor':>9} {'pow':>4}")
    print(hdr)
    print("-" * len(hdr))
    for m_sign, n_sign, direction in CONFIRMED:
        a = sum(1 for ln in el if m_sign in ln.m_signs and n_sign in ln.n_signs)
        b = sum(1 for ln in el if m_sign in ln.m_signs) - a
        c = sum(1 for ln in el if n_sign in ln.n_signs) - a
        d = len(el) - a - b - c
        crude = odds_ratio(a, b, c, d)
        s1 = run(el, m_sign, n_sign, direction,
                 lambda ln, t=n_sign: other_sig(ln, t), "other_N_signature")
        s2 = run(el, m_sign, n_sign, direction,
                 lambda ln, t=n_sign: (ln.tablet, ln.surface, other_sig(ln, t)),
                 "tablet_face_other_N_signature")
        print(f"{m_sign+'-'+n_sign:12} {direction:9} {crude:8.2f} | "
              f"{s1['n_strata']:9} {s1['n_informative']:4} "
              f"{(s1['mh_odds_ratio'] or 0):9.2f} {s1['p']:9.4g} "
              f"{s1['p_floor']:9.3g} {'YES' if s1['has_power_at_05'] else 'no':>4}")
        out["pairs"][f"{m_sign}-{n_sign}"] = {
            "direction": direction, "crude_odds_ratio": crude,
            "crude_cells": [a, b, c, d], "S1": s1, "S2": s2}

    print()
    hdr2 = (f"{'pair':12} {'S2 strata':>9} {'inf':>4} {'S2 MH-OR':>9} {'S2 p':>9} "
            f"{'S2 floor':>9} {'pow':>4}  <- strictest, face + co-numeral")
    print(hdr2)
    print("-" * len(hdr2))
    for k, v in out["pairs"].items():
        s2 = v["S2"]
        print(f"{k:12} {s2['n_strata']:9} {s2['n_informative']:4} "
              f"{(s2['mh_odds_ratio'] or 0):9.2f} {s2['p']:9.4g} "
              f"{s2['p_floor']:9.3g} {'YES' if s2['has_power_at_05'] else 'no':>4}")

    Path("results").mkdir(exist_ok=True)
    Path("results/magnitude.json").write_text(json.dumps(out, indent=2, default=str))
    print("\nwrote results/magnitude.json")


if __name__ == "__main__":
    main()
