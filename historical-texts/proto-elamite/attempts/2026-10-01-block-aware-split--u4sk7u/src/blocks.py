#!/usr/bin/env python3
"""Shared machinery for the 2026-10-01 block-aware split.

Everything here reuses the audited 2026-09-04 parser and exact statistics verbatim;
nothing re-implements them. The only new object is the block-aware split itself.

No lexical, phonetic or metrological value is assigned to any sign anywhere.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable, Sequence

_ANALYSIS = Path(__file__).resolve().parents[3] / "analysis"
sys.path.insert(0, str(_ANALYSIS))

from structure_associations import (  # noqa: E402
    Line,
    bh_adjust,
    corpus_digest,
    fisher_exact_two_sided,
    hypergeom_probability,
    odds_ratio,
    parse_tablet,
    split_name,
)

# The eight numeral associations confirmed on held-out tablets in 2026-09-04.
CONFIRMED = [
    ("M297", "N39B", "enriched"),
    ("M297", "N24", "enriched"),
    ("M297", "N01", "depleted"),
    ("M263", "N30C", "depleted"),
    ("M263", "N01", "enriched"),
    ("M243", "N39B", "enriched"),
    ("M106", "N24", "enriched"),
    ("M288", "N45", "enriched"),
]


def load_corpus(corpus_dir: Path) -> tuple[list[Line], list[Path]]:
    files = sorted(Path(corpus_dir).glob("*.values.atf"))
    if not files:
        raise SystemExit(f"no *.values.atf in {corpus_dir}")
    lines: list[Line] = []
    for path in files:
        lines.extend(parse_tablet(path))
    return lines, files


def eligible(lines: Iterable[Line]) -> list[Line]:
    """Intact lines carrying both an M-sign and an accounting N-sign (2026-09-04 filter)."""
    return [ln for ln in lines if not ln.damaged and ln.m_signs and ln.n_signs]


def face_key(line: Line) -> tuple[str, str]:
    return (line.tablet, line.surface)


def tablet_key(line: Line) -> str:
    return line.tablet


def group(lines: Sequence[Line], key: Callable[[Line], object]) -> dict[object, list[Line]]:
    out: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        out[key(ln)].append(ln)
    return dict(out)


def block_marginals(block: Sequence[Line], m_sign: str, n_sign: str) -> tuple[int, int, int, int]:
    """(total, sign-lines, target-lines, overlap) for one block."""
    total = len(block)
    s = sum(m_sign in ln.m_signs for ln in block)
    t = sum(n_sign in ln.n_signs for ln in block)
    o = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in block)
    return total, s, t, o


def is_informative(total: int, s: int, t: int) -> bool:
    """A block is informative iff its hypergeometric support has more than one point.

    Depends only on the block marginals, never on the overlap. This is what makes a
    split selected on informativeness ancillary to the conditional null.
    """
    return min(s, t) > max(0, s - (total - t))


def informative_blocks(lines: Sequence[Line], m_sign: str, n_sign: str,
                       key: Callable[[Line], object] = face_key) -> list[object]:
    out = []
    for k, bl in group(lines, key).items():
        total, s, t, _ = block_marginals(bl, m_sign, n_sign)
        if is_informative(total, s, t):
            out.append(k)
    return sorted(out, key=repr)


def blocked_exact(lines: Sequence[Line], m_sign: str, n_sign: str, direction: str,
                  key: Callable[[Line], object] = face_key) -> dict[str, object]:
    """Exact conditional test: permute the target only within each block.

    Returns the observed p, the p-floor (smallest p the test could return at these
    marginals), and the block bookkeeping. Identical in method to the 2026-09-04
    `blocked_randomization_p` and the 2026-09-17 `power_floor.floors`, generalised
    over the block key.
    """
    dist = [1.0]
    observed = max_possible = min_possible = 0
    informative = 0
    blocks = group(lines, key)
    for bl in blocks.values():
        total, s, t, o = block_marginals(bl, m_sign, n_sign)
        observed += o
        lo = max(0, s - (total - t))
        hi = min(s, t)
        max_possible += hi
        min_possible += lo
        if hi > lo:
            informative += 1
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
    if direction == "enriched":
        p = min(1.0, sum(dist[observed:]))
        floor = min(1.0, sum(dist[max_possible:]))
    elif direction == "depleted":
        p = min(1.0, sum(dist[: observed + 1]))
        floor = min(1.0, sum(dist[: min_possible + 1]))
    else:
        raise ValueError(direction)
    return {
        "p": p,
        "p_floor": floor,
        "observed_overlap": observed,
        "max_possible_overlap": max_possible,
        "min_possible_overlap": min_possible,
        "blocks": len(blocks),
        "informative_blocks": informative,
        "has_power_at_05": floor <= 0.05,
        "expected_overlap_under_null": sum(i * v for i, v in enumerate(dist)),
    }


def pooled(lines: Sequence[Line], m_sign: str, n_sign: str) -> tuple[int, int, int, int]:
    a = b = c = d = 0
    for ln in lines:
        has_m = m_sign in ln.m_signs
        has_n = n_sign in ln.n_signs
        if has_m and has_n:
            a += 1
        elif has_m:
            b += 1
        elif has_n:
            c += 1
        else:
            d += 1
    return a, b, c, d


def block_aware_split(lines: Sequence[Line], m_sign: str, n_sign: str,
                      key: Callable[[Line], object] = face_key) -> set[str]:
    """Tablets assigned to validation: every tablet owning an informative block.

    Selection uses block marginals only — never the overlap — so the conditional
    null for the validation test is unchanged (see src/calibration.py).
    """
    return {k[0] if isinstance(k, tuple) else k
            for k in informative_blocks(lines, m_sign, n_sign, key)}


def rescreen(train: Sequence[Line]) -> dict[tuple[str, str], dict[str, float]]:
    """Re-run the unchanged 2026-09-04 numeral screen on an arbitrary training set.

    Same thresholds: support >= 20 sign-lines and >= 20 target-lines, Fisher two-sided,
    Benjamini-Hochberg q <= 0.01, Haldane-corrected OR >= 3 or <= 1/3.
    """
    signs = sorted({s for ln in train for s in ln.m_signs})
    targets = sorted({n for ln in train for n in ln.n_signs})
    raw = []
    for target in targets:
        for sign in signs:
            a, b, c, d = pooled(train, sign, target)
            if a + b < 20 or a + c < 20:
                continue
            raw.append({"m": sign, "n": target, "cells": (a, b, c, d),
                        "or": odds_ratio(a, b, c, d),
                        "p": fisher_exact_two_sided(a, b, c, d)})
    qs = bh_adjust([r["p"] for r in raw])
    out = {}
    for r, q in zip(raw, qs):
        r["q"] = q
        r["selected"] = bool(q <= 0.01 and (r["or"] >= 3.0 or r["or"] <= 1 / 3))
        out[(r["m"], r["n"])] = r
    return out
