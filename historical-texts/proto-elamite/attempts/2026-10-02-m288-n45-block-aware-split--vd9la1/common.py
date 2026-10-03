#!/usr/bin/env python3
"""Shared loading/stat helpers for the 2026-10-02 M288-N45 block-aware split.

Everything here reuses the audited 2026-09-04 parser and the 2026-09-17
re-parameterised blocked randomization verbatim. Nothing is re-implemented.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Sequence

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
sys.path.insert(0, str(_ROOT / "analysis"))
sys.path.insert(0, str(_ROOT / "attempts" / "2026-09-17-exact-form-and-face"))

from structure_associations import (  # noqa: E402
    Line, bh_adjust, fisher_exact_two_sided, hypergeom_probability,
    odds_ratio, parse_tablet, split_name,
)
from face_and_form import CONFIRMED, blocked_randomization_p, eligible, load_lines  # noqa: E402

TARGET = ("M288", "N45", "enriched")


def corpus_dir(argv: Sequence[str]) -> Path:
    if len(argv) > 1:
        return Path(argv[1])
    return Path(_HERE.joinpath("corpus_path.txt").read_text().strip())


def load_eligible(argv: Sequence[str]) -> list[Line]:
    lines, _ = load_lines(corpus_dir(argv))
    return eligible(lines)


def face_key(ln: Line):
    return (ln.tablet, ln.surface)


def block_stats(lines: Sequence[Line], m_sign: str, n_sign: str, block_key=face_key):
    """Per-block marginals for the exact face-blocked null.

    A block is *informative* iff the permutation has any freedom in it, i.e. the
    hypergeometric support has more than one point (lo < hi). Non-informative blocks
    contribute a constant to the overlap total and zero variance, so they cannot
    affect the p-value except through that constant.
    """
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)
    rows = []
    for key, bl in blocks.items():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo = max(0, s - (total - t))
        hi = min(s, t)
        rows.append({
            "block": key, "tablet": key[0] if isinstance(key, tuple) else key,
            "surface": key[1] if isinstance(key, tuple) else None,
            "n_lines": total, "m_lines": s, "n_sign_lines": t,
            "overlap": obs, "lo": lo, "hi": hi, "informative": hi > lo,
        })
    return rows
