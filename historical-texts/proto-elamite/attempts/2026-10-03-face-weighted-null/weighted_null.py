#!/usr/bin/env python3
"""Exact face-weighted within-tablet null for the Proto-Elamite constraint set.

The problem this solves
-----------------------
The 2026-09-04 validation permutes the target N-sign *within tablet*, which controls
every confound constant across a tablet but lets the target move between the obverse
and the reverse. N45 is the most reverse-skewed N-sign in the corpus and M288 is also
reverse-skewed, so that freedom is exactly what a face confound would exploit.

The 2026-09-17 session's fix was to block on `(tablet, face)`. That controls face, but
it over-conditions: 615 of 1,426 faces carry a single eligible line, so for M288-N45 it
leaves 16 informative blocks out of 1,426 and discards 38 of the pair's 56
co-occurrences into zero-freedom blocks. Its p-value floor on the published holdout is
0.12 — it cannot fire at any data volume.

This module replaces the strata split with a **weighted permutation**. The target is
re-dealt within tablet, as in 2026-09-04, but non-uniformly: a reverse line is `w` times
as likely to receive the target as an obverse line. The null therefore carries the face
confound *at an assumed strength* instead of conditioning it away, which keeps every
tablet block and every co-occurrence while still removing the confound.

Two properties make it auditable:

* **w = 1 reproduces the published test exactly.** The weighted distribution collapses
  to the hypergeometric convolution of `structure_associations.blocked_randomization_p`.
  `test_weighted_null.py` asserts agreement to 1e-12 on all eight published pairs.
* **w is a free parameter, so the output is a curve, not a verdict.** Reporting p(w)
  answers "how strong would the face confound have to be to explain this away?", which
  is a quantity the blocked test cannot produce at all.

The distribution is computed exactly by convolution, not by Monte Carlo.

No lexical, phonetic or metrological value is assigned to any sign anywhere here.
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

_ANALYSIS_DIR = Path(__file__).resolve().parents[2] / "analysis"
sys.path.insert(0, str(_ANALYSIS_DIR))

from structure_associations import Line, parse_tablet  # noqa: E402

REVERSE_FACES = {"reverse"}


def load_eligible(corpus_dir: Path) -> list[Line]:
    """Intact lines carrying both an M-sign and an accounting N-sign.

    Identical eligibility filter to the 2026-09-04 numeral analysis and the
    2026-09-17 audit.
    """
    lines: list[Line] = []
    for path in sorted(corpus_dir.glob("*.values.atf")):
        lines.extend(parse_tablet(path))
    return [ln for ln in lines if not ln.damaged and ln.m_signs and ln.n_signs]


def is_reverse(line: Line) -> bool:
    return line.surface in REVERSE_FACES


def face_weight(lines: Sequence[Line], m_sign: str, n_sign: str) -> dict[str, float]:
    """Odds ratio of target presence on reverse vs obverse, among lines WITHOUT m_sign.

    Estimating the face propensity off the sign under test keeps the null's confound
    strength independent of the association it is being used to test. Haldane-Anscombe
    correction so a zero cell stays finite.
    """
    a = b = c = d = 0  # reverse&target, reverse&no, obverse&target, obverse&no
    for ln in lines:
        if m_sign in ln.m_signs:
            continue
        has = n_sign in ln.n_signs
        if is_reverse(ln):
            a, b = (a + 1, b) if has else (a, b + 1)
        else:
            c, d = (c + 1, d) if has else (c, d + 1)
    return {
        "w": ((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5)),
        "reverse_target": a,
        "reverse_other": b,
        "obverse_target": c,
        "obverse_other": d,
        "reverse_rate": a / (a + b) if a + b else float("nan"),
        "obverse_rate": c / (c + d) if c + d else float("nan"),
    }


def _log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def _face_table(n_with_sign: int, n_without_sign: int) -> list[list[float]]:
    """table[k][a] = number of ways to pick k lines of which a carry the M-sign."""
    total = n_with_sign + n_without_sign
    table = [[0.0] * (min(k, n_with_sign) + 1) for k in range(total + 1)]
    for k in range(total + 1):
        for a in range(min(k, n_with_sign) + 1):
            if k - a > n_without_sign:
                continue
            table[k][a] = math.exp(
                _log_choose(n_with_sign, a) + _log_choose(n_without_sign, k - a)
            )
    return table


def tablet_overlap_distribution(
    block: Sequence[Line], m_sign: str, n_sign: str, w: float
) -> list[float]:
    """Exact conditional distribution of the sign/target overlap within one tablet.

    Conditions on the tablet's observed target count. A reverse line is `w` times as
    likely to receive the target as an obverse line; w = 1 gives the hypergeometric.
    """
    target_count = sum(n_sign in ln.n_signs for ln in block)
    obv_with = sum(1 for ln in block if not is_reverse(ln) and m_sign in ln.m_signs)
    obv_without = sum(1 for ln in block if not is_reverse(ln) and m_sign not in ln.m_signs)
    rev_with = sum(1 for ln in block if is_reverse(ln) and m_sign in ln.m_signs)
    rev_without = sum(1 for ln in block if is_reverse(ln) and m_sign not in ln.m_signs)

    obverse = _face_table(obv_with, obv_without)
    reverse = _face_table(rev_with, rev_without)
    n_obverse = obv_with + obv_without
    n_reverse = rev_with + rev_without

    max_overlap = min(target_count, obv_with + rev_with)
    weights = [0.0] * (max_overlap + 1)
    for k_rev in range(min(n_reverse, target_count) + 1):
        k_obv = target_count - k_rev
        if k_obv < 0 or k_obv > n_obverse:
            continue
        face_factor = w ** k_rev
        for a_rev, count_rev in enumerate(reverse[k_rev]):
            if not count_rev:
                continue
            for a_obv, count_obv in enumerate(obverse[k_obv]):
                if not count_obv:
                    continue
                weights[a_rev + a_obv] += face_factor * count_rev * count_obv

    mass = sum(weights)
    if mass <= 0:
        return [1.0]
    return [value / mass for value in weights]


def weighted_randomization_p(
    lines: Sequence[Line],
    m_sign: str,
    n_sign: str,
    direction: str,
    w: float = 1.0,
    block_key: Callable[[Line], object] | None = None,
) -> dict[str, object]:
    """One-sided exact p-value for the overlap total under the face-weighted null."""
    key = block_key or (lambda ln: ln.tablet)
    blocks: dict[object, list[Line]] = defaultdict(list)
    for ln in lines:
        blocks[key(ln)].append(ln)

    distribution = [1.0]
    observed = 0
    for block in blocks.values():
        observed += sum(
            1 for ln in block if m_sign in ln.m_signs and n_sign in ln.n_signs
        )
        local = tablet_overlap_distribution(block, m_sign, n_sign, w)
        combined = [0.0] * (len(distribution) + len(local) - 1)
        for i, pi in enumerate(distribution):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        combined[i + j] += pi * pj
        distribution = combined

    support = [i for i, v in enumerate(distribution) if v > 0]
    if direction == "enriched":
        p_value = min(1.0, sum(distribution[observed:]))
        p_floor = min(1.0, sum(distribution[support[-1]:]))
    elif direction == "depleted":
        p_value = min(1.0, sum(distribution[: observed + 1]))
        p_floor = min(1.0, sum(distribution[: support[0] + 1]))
    else:
        raise ValueError(f"unknown direction: {direction}")

    mean = sum(i * v for i, v in enumerate(distribution))
    variance = sum((i - mean) ** 2 * v for i, v in enumerate(distribution))
    return {
        "p": p_value,
        "p_floor": p_floor,
        "observed_overlap": observed,
        "null_mean": mean,
        "null_sd": math.sqrt(variance),
        "blocks": len(blocks),
        "max_possible_overlap": support[-1],
        "min_possible_overlap": support[0],
        "w": w,
    }


def critical_weight(
    lines: Sequence[Line],
    m_sign: str,
    n_sign: str,
    direction: str,
    alpha: float = 0.05,
    hi: float = 4096.0,
) -> dict[str, object]:
    """Smallest assumed face-confound strength w at which the pair stops clearing alpha.

    The p-value is monotone in w for an enriched pair whose target is reverse-skewed,
    so a bisection is valid; the returned bracket is reported so a non-monotone case
    is visible rather than silent.
    """
    low = 1.0
    p_low = weighted_randomization_p(lines, m_sign, n_sign, direction, low)["p"]
    p_hi = weighted_randomization_p(lines, m_sign, n_sign, direction, hi)["p"]
    if p_low > alpha:
        return {"critical_w": None, "note": "fails already at w=1", "p_at_1": p_low}
    if p_hi <= alpha:
        return {
            "critical_w": None,
            "note": f"still clears alpha at w={hi:g}",
            "p_at_1": p_low,
            "p_at_hi": p_hi,
        }
    for _ in range(60):
        mid = math.sqrt(low * hi)
        if weighted_randomization_p(lines, m_sign, n_sign, direction, mid)["p"] <= alpha:
            low = mid
        else:
            hi = mid
    return {"critical_w": math.sqrt(low * hi), "p_at_1": p_low, "bracket": [low, hi]}
