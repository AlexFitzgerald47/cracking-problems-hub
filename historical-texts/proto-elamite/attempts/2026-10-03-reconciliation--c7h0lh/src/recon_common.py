"""Shared machinery for the 2026-10-03 reconciliation session.

Imports the AUDITED 2026-09-04 parser verbatim (reproduced byte-identically by
seven independent sessions) and adds one thing none of them computed: the
explicit p-floor of the co-numeral-stratified exact test, so that a failure
under that control can be told apart from an absence of power by the folder's
own floor rule.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
ANALYSIS = REPO / "historical-texts" / "proto-elamite" / "analysis"


def _load_audited():
    spec = importlib.util.spec_from_file_location(
        "structure_associations", ANALYSIS / "structure_associations.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["structure_associations"] = mod
    spec.loader.exec_module(mod)
    return mod


sa = _load_audited()
parse_tablet = sa.parse_tablet
hypergeom_probability = sa.hypergeom_probability
fisher_exact_two_sided = sa.fisher_exact_two_sided
odds_ratio = sa.odds_ratio
bh_adjust = sa.bh_adjust
split_name = sa.split_name


def load_eligible(corpus_dir: Path):
    """The 4,869 eligible lines: intact, M-sign bearing, N-sign bearing."""
    files = sorted(Path(corpus_dir).glob("*.values.atf"))
    lines = [ln for f in files for ln in parse_tablet(f)]
    eligible = [ln for ln in lines if ln.m_signs and not ln.damaged and ln.n_signs]
    return files, lines, eligible


def blocks_of(lines, key):
    out = {}
    for ln in lines:
        out.setdefault(key(ln), []).append(ln)
    return out


def block_marginals(block_lines, m_sign, target):
    n = len(block_lines)
    s = sum(m_sign in ln.m_signs for ln in block_lines)
    t = sum(target in ln.n_signs for ln in block_lines)
    o = sum(m_sign in ln.m_signs and target in ln.n_signs for ln in block_lines)
    return n, s, t, o


def exact_blocked(lines, m_sign, target, key, direction):
    """Exact conditional test by convolution over blocks defined by `key`.

    Returns p, floor, observed, max_possible, min_possible, informative-block
    count, block count and the Mantel-Haenszel odds ratio over the same blocks.
    The floor is the p-value the test would return on the most extreme data its
    marginals permit: the folder's power rule, applied to this block scheme.
    """
    dist = [1.0]
    observed = 0
    hi_total = 0
    lo_total = 0
    informative = 0
    nblocks = 0
    mh_num = mh_den = 0.0
    for block_lines in blocks_of(lines, key).values():
        n, s, t, o = block_marginals(block_lines, m_sign, target)
        nblocks += 1
        lo = max(0, s - (n - t))
        hi = min(s, t)
        observed += o
        hi_total += hi
        lo_total += lo
        if hi > lo:
            informative += 1
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, n)
        combined = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi == 0.0:
                continue
            for j, pj in enumerate(local):
                if pj:
                    combined[i + j] += pi * pj
        dist = combined
        # Mantel-Haenszel over the same blocks
        a, b, c = o, s - o, t - o
        d = n - s - t + o
        if n:
            mh_num += a * d / n
            mh_den += b * c / n
    if direction == "enriched":
        p = min(1.0, sum(dist[observed:]))
        floor = min(1.0, sum(dist[hi_total:]))
    else:
        p = min(1.0, sum(dist[: observed + 1]))
        floor = min(1.0, sum(dist[: lo_total + 1]))
    mh = (mh_num / mh_den) if mh_den > 0 else float("inf")
    return {
        "p": p, "floor": floor, "observed": observed, "max": hi_total,
        "min": lo_total, "informative_blocks": informative, "blocks": nblocks,
        "mh_or": mh,
    }


def crude_cells(lines, m_sign, target):
    a = b = c = d = 0
    for ln in lines:
        hs = m_sign in ln.m_signs
        ht = target in ln.n_signs
        if hs and ht:
            a += 1
        elif hs:
            b += 1
        elif ht:
            c += 1
        else:
            d += 1
    return a, b, c, d


PUBLISHED_EIGHT = [
    ("M297", "N39B", "enriched"),
    ("M297", "N24", "enriched"),
    ("M297", "N01", "depleted"),
    ("M263", "N30C", "depleted"),
    ("M263", "N01", "enriched"),
    ("M243", "N39B", "enriched"),
    ("M106", "N24", "enriched"),
    ("M288", "N45", "enriched"),
]
