#!/usr/bin/env python3
"""Similarity measures and permutation machinery."""
import random


def lev(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def sim_lev(a, b):
    m = max(len(a), len(b))
    return 1.0 - lev(a, b) / m if m else 1.0


def lcs_len(a, b):
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0]
        for j, cb in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if ca == cb else max(cur[-1], prev[j]))
        prev = cur
    return prev[-1]


def sim_lcs(a, b):
    m = max(len(a), len(b))
    return lcs_len(a, b) / m if m else 1.0


def onset(w, n=2):
    return w[:n]


def sim_onset(a, b, n=2):
    return 1.0 if onset(a, n) == onset(b, n) else 0.0


def coda(w, n=2):
    return w[-n:]


def sim_coda(a, b, n=2):
    return 1.0 if coda(a, n) == coda(b, n) else 0.0


MEASURES = {
    "lev": sim_lev,
    "lcs": sim_lcs,
    "onset2": sim_onset,
    "coda2": sim_coda,
}


def lag_mean(seq, d, simf):
    """Mean similarity between elements d apart (linear, not cyclic)."""
    n = len(seq)
    if n - d < 1:
        return None
    vals = [simf(seq[i], seq[i + d]) for i in range(n - d)]
    return sum(vals) / len(vals)


def lag_profile(seq, simf, maxlag):
    return {d: lag_mean(seq, d, simf) for d in range(1, maxlag + 1)}


def perm_test_lag(seq, d, simf, nperm=10000, rng=None):
    """Two-sided-ish: returns (observed, null_mean, null_sd, z, p_right)."""
    rng = rng or random.Random(20260908)
    obs = lag_mean(seq, d, simf)
    if obs is None:
        return None
    work = list(seq)
    nulls = []
    for _ in range(nperm):
        rng.shuffle(work)
        nulls.append(lag_mean(work, d, simf))
    mu = sum(nulls) / len(nulls)
    var = sum((x - mu) ** 2 for x in nulls) / (len(nulls) - 1)
    sd = var ** 0.5
    ge = sum(1 for x in nulls if x >= obs)
    return {
        "obs": obs, "null_mean": mu, "null_sd": sd,
        "z": (obs - mu) / sd if sd > 0 else 0.0,
        "p_right": (ge + 1) / (len(nulls) + 1),
    }
