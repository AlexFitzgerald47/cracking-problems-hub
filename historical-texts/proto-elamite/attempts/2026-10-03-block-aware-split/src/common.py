"""Shared pieces for the 2026-10-03 block-aware-split experiment."""
from __future__ import annotations

import hashlib
import sys
from collections import defaultdict
from pathlib import Path

_ATT = Path(__file__).resolve().parents[2] / "2026-09-17-exact-form-and-face"
sys.path.insert(0, str(_ATT))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))

from face_and_form import eligible, load_lines  # noqa: E402
from structure_associations import (  # noqa: E402
    bh_adjust, fisher_exact_two_sided, hypergeom_probability, odds_ratio,
)

M, N, DIRECTION = "M288", "N45", "enriched"


def corpus_path() -> Path:
    return Path((_ATT / "corpus_path.txt").read_text().strip())


def load_eligible():
    lines, _ = load_lines(corpus_path())
    return eligible(lines)


def face_blocks(lines, m_sign=M, n_sign=N):
    """Marginals and bounds per (tablet, face). Overlap bounds use marginals only."""
    grouped = defaultdict(list)
    for ln in lines:
        grouped[(ln.tablet, ln.surface)].append(ln)
    out = []
    for key, bl in sorted(grouped.items()):
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo, hi = max(0, s - (total - t)), min(s, t)
        out.append({"tablet": key[0], "face": key[1], "total": total, "s": s,
                    "t": t, "obs": obs, "lo": lo, "hi": hi, "informative": hi > lo})
    return out


def tail(blocks, direction=DIRECTION):
    """Exact blocked test: (p at observed, p at the attainable extreme = floor)."""
    if not blocks:
        return 1.0, 1.0, 0, 0
    dist = [1.0]
    for b in blocks:
        local = [0.0] * (b["hi"] + 1)
        for k in range(b["lo"], b["hi"] + 1):
            local[k] = hypergeom_probability(k, b["s"], b["t"], b["total"])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    obs = sum(b["obs"] for b in blocks)
    if direction == "enriched":
        mx = sum(b["hi"] for b in blocks)
        return min(1.0, sum(dist[obs:])), min(1.0, sum(dist[mx:])), obs, mx
    mn = sum(b["lo"] for b in blocks)
    return min(1.0, sum(dist[:obs + 1])), min(1.0, sum(dist[:mn + 1])), obs, mn


def tablet_hash(tablet: str) -> str:
    return hashlib.sha256(tablet.encode("ascii")).hexdigest()


def canonical_split(blocks, want=10):
    """The pre-registered split rule. Reads ONLY block marginals, never an overlap.

    Tablets carrying informative blocks are ordered by how many they carry (more
    first, so the quota is met with the fewest tablets removed from training) and
    then by sha256 of the tablet id, which is arbitrary but fixed. Tablets are moved
    into validation in that order until validation holds `want` informative blocks.
    Every tablet with no informative block stays in training: it cannot change this
    pair's validation p-value, because a non-informative block contributes a point
    mass to the null, and leaving it in training maximises screening power.
    """
    per_tablet = defaultdict(int)
    for b in blocks:
        if b["informative"]:
            per_tablet[b["tablet"]] += 1
    order = sorted(per_tablet, key=lambda t: (-per_tablet[t], tablet_hash(t)))
    val, got = [], 0
    for t in order:
        if got >= want:
            break
        val.append(t)
        got += per_tablet[t]
    return set(val), got


def screen_numeral(train_lines, min_sign_lines=20, min_target_lines=20,
                   q_max=0.01, or_min=3.0):
    """The published 2026-09-04 training screen, re-run verbatim on a given train set.

    Returns the set of (m_sign, n_sign) pairs selected, plus M288-N45's own row.
    """
    signs = sorted({s for ln in train_lines for s in ln.m_signs})
    targets = sorted({n for ln in train_lines for n in ln.n_signs})
    sign_lines = {s: [ln for ln in train_lines if s in ln.m_signs] for s in signs}
    target_count = {n: sum(n in ln.n_signs for ln in train_lines) for n in targets}
    total = len(train_lines)

    cand = []
    for n_sign in targets:
        c_all = target_count[n_sign]
        if c_all < min_target_lines:
            continue
        for s in signs:
            sl = sign_lines[s]
            if len(sl) < min_sign_lines:
                continue
            a = sum(n_sign in ln.n_signs for ln in sl)
            b = len(sl) - a
            c = c_all - a
            d = total - a - b - c
            cand.append({"m": s, "n": n_sign, "cells": (a, b, c, d),
                         "or": odds_ratio(a, b, c, d),
                         "p": fisher_exact_two_sided(a, b, c, d)})
    qs = bh_adjust([x["p"] for x in cand])
    selected, own = set(), None
    for x, q in zip(cand, qs):
        x["q"] = q
        if q <= q_max and (x["or"] >= or_min or x["or"] <= 1.0 / or_min):
            selected.add((x["m"], x["n"]))
        if x["m"] == M and x["n"] == N:
            own = dict(x)
    return selected, own, len(cand)
