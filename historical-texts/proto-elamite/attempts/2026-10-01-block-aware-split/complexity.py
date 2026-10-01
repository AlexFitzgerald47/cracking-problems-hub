#!/usr/bin/env python3
"""Is line numeral-count a confound for M288-N45, or a mediator of it?

N4 in nulls.py blocks on (tablet, face, number of N-signs on the line) and
M288-N45 then fails (full corpus p = 0.057, floor 0.00056 -- the test has
power) while M297-N39B and M263-N01 still pass below 1e-5. Two readings:

  confound  M288 lines happen to carry more accounting numerals, so they pick up
            any given N-sign more often, N45 included. The association is then an
            artefact of line complexity.
  mediator  M288 lines carry more numerals *because* of what M288 does in the
            accounting, and N45 is part of that. Conditioning on numeral count
            then conditions on a consequence of the association and destroys it.

Neither reading is settled by the p-value. What distinguishes them is whether
N45 specifically is over-represented on M288 lines beyond the rate that their
numeral count alone would predict. This measures that directly, and checks the
eight fair-coin faces -- the pair's strongest evidence -- for the same effect.
"""
from __future__ import annotations

import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from face_and_form import eligible, load_lines  # noqa: E402


def main():
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)
    out = {}

    # ---- 1. do M288 lines carry more accounting numerals?
    m288 = [ln for ln in el if "M288" in ln.m_signs]
    other = [ln for ln in el if "M288" not in ln.m_signs]
    def mean(xs): return sum(xs) / len(xs)
    c288 = [len(ln.n_signs) for ln in m288]
    coth = [len(ln.n_signs) for ln in other]
    print(f"accounting N-signs per line:  M288 lines {mean(c288):.3f} (n={len(m288)})"
          f"   other lines {mean(coth):.3f} (n={len(other)})")
    print(f"  distribution M288 : {sorted(Counter(c288).items())}")
    print(f"  distribution other: {sorted(Counter(coth).items())}")
    out["numerals_per_line"] = {
        "m288_mean": mean(c288), "m288_n": len(m288),
        "other_mean": mean(coth), "other_n": len(coth),
        "m288_dist": dict(sorted(Counter(c288).items())),
        "other_dist": dict(sorted(Counter(coth).items())),
    }

    # ---- 2. N45 rate on M288 vs non-M288 lines, STRATIFIED by numeral count
    print("\nN45 rate by line numeral count (the complexity-matched comparison):")
    print(f"{'k numerals':>11} {'M288 lines':>11} {'N45|M288':>9} "
          f"{'other lines':>12} {'N45|other':>10}")
    strata = {}
    for k in sorted(set(c288) | set(coth)):
        a = [ln for ln in m288 if len(ln.n_signs) == k]
        b = [ln for ln in other if len(ln.n_signs) == k]
        if not a:
            continue
        ra = sum("N45" in ln.n_signs for ln in a) / len(a)
        rb = (sum("N45" in ln.n_signs for ln in b) / len(b)) if b else float("nan")
        strata[k] = {"m288_n": len(a), "m288_n45_rate": ra,
                     "other_n": len(b), "other_n45_rate": rb}
        print(f"{k:>11} {len(a):>11} {ra:>9.4f} {len(b):>12} {rb:>10.4f}")
    out["n45_rate_by_numeral_count"] = strata

    # Mantel-Haenszel odds ratio across numeral-count strata: the pooled
    # M288/N45 association with line complexity held fixed.
    num = den = 0.0
    for k, s in strata.items():
        a = s["m288_n45_rate"] * s["m288_n"]
        b = s["m288_n"] - a
        c = (s["other_n45_rate"] * s["other_n"]) if s["other_n"] else 0.0
        d = s["other_n"] - c
        n = s["m288_n"] + s["other_n"]
        if n:
            num += a * d / n
            den += b * c / n
    mh = num / den if den else float("inf")
    print(f"\nMantel-Haenszel OR for M288/N45, stratified by line numeral count: "
          f"{mh:.2f}")
    out["mantel_haenszel_or_stratified_by_numeral_count"] = mh

    # ---- 3. the eight fair-coin faces: which line was the longer one?
    print("\nThe eight fair-coin faces (total=2, M288 lines=1, N45 lines=1).")
    print("For each: the numeral count of the M288 line and of the other line,")
    print("and whether the N45 landed on the M288 line.")
    blocks = defaultdict(list)
    for ln in el:
        blocks[(ln.tablet, ln.surface)].append(ln)
    coin = []
    for bk, bl in sorted(blocks.items()):
        s = sum("M288" in ln.m_signs for ln in bl)
        t = sum("N45" in ln.n_signs for ln in bl)
        if (len(bl), s, t) != (2, 1, 1):
            continue
        m_line = next(ln for ln in bl if "M288" in ln.m_signs)
        o_line = next(ln for ln in bl if "M288" not in ln.m_signs)
        hit = "N45" in m_line.n_signs
        coin.append({
            "tablet": bk[0], "face": bk[1],
            "m288_line_numerals": len(m_line.n_signs),
            "other_line_numerals": len(o_line.n_signs),
            "n45_on_m288_line": hit,
            "m288_line_longer": len(m_line.n_signs) > len(o_line.n_signs),
            "equal_length": len(m_line.n_signs) == len(o_line.n_signs),
            "m288_text": m_line.text.strip(),
            "other_text": o_line.text.strip(),
        })
        print(f"  {bk[0]} {bk[1]:8} M288 line {len(m_line.n_signs)} numerals, "
              f"other {len(o_line.n_signs)};  N45 on M288 line: {hit}")
    longer = sum(c["m288_line_longer"] for c in coin)
    equal = sum(c["equal_length"] for c in coin)
    print(f"\n  M288 line was the longer of the two in {longer}/{len(coin)} faces; "
          f"equal length in {equal}/{len(coin)}.")
    if equal:
        eq = [c for c in coin if c["equal_length"]]
        heads_eq = sum(c["n45_on_m288_line"] for c in eq)
        p = sum(math.comb(len(eq), k) for k in range(heads_eq, len(eq) + 1)) / 2 ** len(eq)
        print(f"  Restricted to the {len(eq)} equal-length faces -- where line "
              f"complexity cannot\n  explain anything -- N45 landed on the M288 "
              f"line {heads_eq}/{len(eq)} times, binomial p = {p:.4f}.")
        out["equal_length_coin_faces"] = {
            "n": len(eq), "heads": heads_eq, "binomial_p": p}
    out["coin_faces"] = coin

    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "complexity.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
