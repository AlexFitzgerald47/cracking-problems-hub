#!/usr/bin/env python3
"""Power floor for the face-blocked null.

A pair that fails the face-blocked test has failed for one of two reasons: the
association was a face artefact, or the finer blocks left the test with no power.
Only the first is a finding. This computes, for each pair and each block scheme, the
smallest p-value the test could possibly return -- the p-value it would give if every
block showed the maximum overlap its marginals permit. If that floor exceeds 0.05, the
test could not have confirmed the pair whatever the data said, and its failure is
uninformative.

This is the Kryptos lesson from board/PRACTICES.md applied to a blocked exact test.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

from face_and_form import CONFIRMED, blocked_randomization_p, eligible, load_lines
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))
from structure_associations import hypergeom_probability, split_name  # noqa: E402


def block_distribution(lines, m_sign, n_sign, block_key):
    blocks = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)
    dist = [1.0]
    observed = 0
    max_possible = 0
    informative_blocks = 0
    for bl in blocks.values():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        observed += sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo = max(0, s - (total - t))
        hi = min(s, t)
        max_possible += hi
        if hi > lo:
            informative_blocks += 1
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, total)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    return dist, observed, max_possible, informative_blocks, len(blocks)


def floors(lines, m_sign, n_sign, direction, block_key):
    dist, obs, mx, informative, nblocks = block_distribution(lines, m_sign, n_sign, block_key)
    if direction == "enriched":
        floor = min(1.0, sum(dist[mx:]))
        actual = min(1.0, sum(dist[obs:]))
    else:
        mn = next(i for i, v in enumerate(dist) if v > 0)
        floor = min(1.0, sum(dist[: mn + 1]))
        actual = min(1.0, sum(dist[: obs + 1]))
    return {
        "p": actual,
        "p_floor": floor,
        "observed_overlap": obs,
        "max_possible_overlap": mx,
        "informative_blocks": informative,
        "blocks": nblocks,
        "has_power_at_05": floor <= 0.05,
    }


def main():
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    val = [ln for ln in eligible(lines) if split_name(ln.tablet) == "validation"]
    out = {}
    for m, n, d in CONFIRMED:
        out[f"{m}-{n}"] = {
            "direction": d,
            "tablet_blocked": floors(val, m, n, d, lambda ln: ln.tablet),
            "face_blocked": floors(val, m, n, d, lambda ln: (ln.tablet, ln.surface)),
        }
    Path("results").mkdir(exist_ok=True)
    Path("results/power_floor.json").write_text(json.dumps(out, indent=2))
    print(f"{'pair':14} {'blk':7} {'p':>9} {'floor':>9} {'obs/max':>9} {'infBlk':>7} power")
    for pair, v in out.items():
        for scheme in ("tablet_blocked", "face_blocked"):
            r = v[scheme]
            print(f"{pair:14} {scheme[:6]:7} {r['p']:9.4f} {r['p_floor']:9.4f} "
                  f"{str(r['observed_overlap'])+'/'+str(r['max_possible_overlap']):>9} "
                  f"{r['informative_blocks']:7} {'YES' if r['has_power_at_05'] else 'NO'}")
        print()


if __name__ == "__main__":
    main()
