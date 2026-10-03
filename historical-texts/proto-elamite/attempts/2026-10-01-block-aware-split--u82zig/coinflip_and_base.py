#!/usr/bin/env python3
"""Two audits that sit beside the block-aware split.

1. The coin-flip accounting (predictions P6, P7). The face-blocked evidence for a
   pair is not its odds ratio; it is the overlap the block marginals left free.
   This separates forced from free co-occurrence and isolates the blocks whose
   marginals make them a fair coin under the null (total = 2, s = 1, t = 1).

2. The correction base. The 2026-09-17 face-blocked q-values were BH-adjusted
   across the 8 already-published pairs. The 2026-09-04 design they are compared
   against BH-adjusts across all 54 train-screened candidates. This re-runs the
   face-blocked test on the published bucket-0 holdout with the published
   correction base, so the two columns can be read like for like.
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import split_name, bh_adjust  # noqa: E402
from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402
from block_split import block_freedom, blocked_test, screen, validate, FACE_KEY  # noqa: E402


def coinflip_audit(lines, m_sign, n_sign):
    """Forced / free / fair-coin decomposition of a pair's face-blocked evidence."""
    blocks = defaultdict(list)
    for ln in lines:
        blocks[(ln.tablet, ln.surface)].append(ln)
    fr = block_freedom(lines, m_sign, n_sign)
    forced = free = observed = 0
    coin_blocks = []
    informative = []
    for bk, bl in sorted(blocks.items()):
        v = fr[bk]
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        forced += v["lo"]
        free += v["hi"] - v["lo"]
        observed += obs
        if v["hi"] > v["lo"]:
            informative.append((bk, v, obs))
        if (v["total"], v["s"], v["t"]) == (2, 1, 1):
            coin_blocks.append((bk, obs))
    heads = sum(o for _, o in coin_blocks)
    n = len(coin_blocks)
    # exact binomial tail for a fair coin
    tail = sum(math.comb(n, k) for k in range(heads, n + 1)) / 2 ** n if n else 1.0
    return {
        "pair": f"{m_sign}-{n_sign}",
        "observed_overlap": observed,
        "forced_overlap": forced,
        "freedom": free,
        "freedom_used": observed - forced,
        "informative_blocks": len(informative),
        "coin_blocks": n,
        "coin_heads": heads,
        "coin_binomial_p": tail,
        "coin_detail": [{"tablet": bk[0], "face": bk[1], "overlap": o}
                        for bk, o in coin_blocks],
        "informative_detail": [
            {"tablet": bk[0], "face": bk[1], "total": v["total"], "s": v["s"],
             "t": v["t"], "lo": v["lo"], "hi": v["hi"], "observed": o}
            for bk, v, o in informative
        ],
    }


def main():
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)

    print("=" * 74)
    print("1. COIN-FLIP ACCOUNTING -- full corpus, all eight published pairs")
    print("=" * 74)
    print(f"{'pair':12} {'obs':>5} {'forced':>7} {'free':>5} {'used':>5} "
          f"{'infB':>5} {'coins':>6} {'heads':>6} {'binom p':>9}")
    audits = {}
    for m, n, _d in CONFIRMED:
        a = coinflip_audit(el, m, n)
        audits[a["pair"]] = a
        print(f"{a['pair']:12} {a['observed_overlap']:5} {a['forced_overlap']:7} "
              f"{a['freedom']:5} {a['freedom_used']:5} {a['informative_blocks']:5} "
              f"{a['coin_blocks']:6} {a['coin_heads']:6} {a['coin_binomial_p']:9.4f}")

    t = audits["M288-N45"]
    print()
    print(f"M288-N45: {t['coin_heads']} of {t['coin_blocks']} fair-coin faces came up "
          f"heads (binomial p = {t['coin_binomial_p']:.4f}).")
    print("  the eleven two-line faces:")
    for c in t["coin_detail"]:
        print(f"    {c['tablet']} {c['face']:8} overlap {c['overlap']}")

    print()
    print("=" * 74)
    print("2. CORRECTION BASE -- face-blocked test on the PUBLISHED bucket-0 holdout")
    print("=" * 74)
    tr = [ln for ln in el if split_name(ln.tablet) == "train"]
    va = [ln for ln in el if split_name(ln.tablet) == "validation"]
    selected, raw = screen(tr)
    rows = validate(va, selected, FACE_KEY)
    by_pair = {f"{r['m_sign']}-{r['n_sign']}": r for r in rows}

    # BH across the 8 published pairs only, which is what 2026-09-17 reported
    eight = [f"{m}-{n}" for m, n, _ in CONFIRMED]
    ps8 = [by_pair[p]["p"] for p in eight]
    qs8 = bh_adjust(ps8)

    print(f"{'pair':12} {'p (face)':>10} {'floor':>8} {'q over 8':>10} "
          f"{'q over 54':>10} {'conf@54':>8}")
    base = {}
    for pair, q8 in zip(eight, qs8):
        r = by_pair[pair]
        base[pair] = {"p": r["p"], "p_floor": r["p_floor"], "q_over_8": q8,
                      "q_over_54": r["q"], "confirmed_at_54": r["confirmed"],
                      "informative_blocks": r["informative_blocks"]}
        print(f"{pair:12} {r['p']:10.5f} {r['p_floor']:8.4f} {q8:10.5f} "
              f"{r['q']:10.5f} {'YES' if r['confirmed'] else 'no':>8}")
    print()
    print(f"candidates screened on the published train split: {len(selected)}")
    print("confirmed under face blocking with the published BH base (54): "
          + ", ".join(f"{r['m_sign']}-{r['n_sign']}" for r in rows if r["confirmed"]))

    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "coinflip_and_base.json").write_text(json.dumps(
        {"coinflip": audits, "correction_base": base,
         "published_split_candidates": len(selected),
         "confirmed_face_blocked_base54": [
             f"{r['m_sign']}-{r['n_sign']}" for r in rows if r["confirmed"]],
         "all_rows_published_split": rows},
        indent=2, default=str))


if __name__ == "__main__":
    main()
