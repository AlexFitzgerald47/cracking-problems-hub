"""Loader for the audited 2026-09-04 parser plus this session's block tests.

Deliberately re-implemented rather than imported from the 10-03 reconciliation
attempt: the gate below checks this file against that session's committed
numbers, so an independent implementation is worth more than a shared one.
"""
from __future__ import annotations
import importlib.util, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
ANALYSIS = REPO / "historical-texts" / "proto-elamite" / "analysis"


def load_audited():
    spec = importlib.util.spec_from_file_location(
        "structure_associations", ANALYSIS / "structure_associations.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["structure_associations"] = mod
    spec.loader.exec_module(mod)
    return mod


_sa = load_audited()
split_name = _sa.split_name
hypergeom_probability = _sa.hypergeom_probability
odds_ratio = _sa.odds_ratio


def mixed_lines_of(corpus: Path):
    files = sorted(Path(corpus).glob("*.values.atf"))
    lines = [ln for f in files for ln in _sa.parse_tablet(f)]
    return [ln for ln in lines if ln.m_signs and not ln.damaged and ln.n_signs]


def bh(ps):
    return _sa.bh_adjust(ps)


def exact_blocked(lines, m_sign, target, key, direction):
    """Exact conditional test by convolution of per-block hypergeometrics.

    Returns p, the p-floor (the smallest p these marginals can yield in the
    hypothesised direction), the observed overlap, informative-block count and
    the Mantel-Haenszel OR over the same blocks.
    """
    blocks = {}
    for ln in lines:
        blocks.setdefault(key(ln), []).append(ln)
    dist = [1.0]
    observed = hi_tot = lo_tot = informative = 0
    mh_num = mh_den = 0.0
    for bl in blocks.values():
        n = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(target in ln.n_signs for ln in bl)
        o = sum(m_sign in ln.m_signs and target in ln.n_signs for ln in bl)
        lo, hi = max(0, s - (n - t)), min(s, t)
        observed += o; hi_tot += hi; lo_tot += lo
        if hi > lo:
            informative += 1
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, n)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if not pi:
                continue
            for j, pj in enumerate(local):
                if pj:
                    comb[i + j] += pi * pj
        dist = comb
        a, b, c = o, s - o, t - o
        d = n - s - t + o
        if n:
            mh_num += a * d / n
            mh_den += b * c / n
    if direction == "enriched":
        p = min(1.0, sum(dist[observed:])); floor = min(1.0, sum(dist[hi_tot:]))
    else:
        p = min(1.0, sum(dist[:observed + 1])); floor = min(1.0, sum(dist[:lo_tot + 1]))
    return {"p": p, "floor": floor, "observed": observed, "max": hi_tot,
            "min": lo_tot, "informative_blocks": informative,
            "blocks": len(blocks), "mh_or": (mh_num / mh_den) if mh_den else float("inf")}


FACE = lambda ln: (ln.tablet, ln.surface)
TABLET = lambda ln: ln.tablet


def conumeral(target):
    """Strata = the exact set of OTHER numeral signs on the line.

    This is the composition control two 10-01/10-03 sessions invented
    independently: it asks whether the association survives comparison only
    between lines whose numeral expression is otherwise identical.
    """
    return lambda ln: frozenset(ln.n_signs - {target})
