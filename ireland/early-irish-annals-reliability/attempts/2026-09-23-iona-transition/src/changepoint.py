# -*- coding: utf-8 -*-
"""Single-changepoint binomial scan with a permutation null and a bootstrap CI."""
import math, random

def _ll(k, n):
    if n == 0 or k == 0 or k == n:
        return 0.0
    p = k / n
    return k * math.log(p) + (n - k) * math.log(1 - p)

def scan(years, k, n, min_entries=150):
    """years sorted; k[i],n[i] tagged/total for that year.
    Returns (stat, cut, left(k,n), right(k,n)) where `cut` is the first year of
    the right-hand segment."""
    K, N = sum(k), sum(n)
    base = _ll(K, N)
    ck = cn = 0
    best = (-1.0, None, None, None)
    for i in range(len(years) - 1):
        ck += k[i]; cn += n[i]
        if cn < min_entries or (N - cn) < min_entries:
            continue
        s = 2.0 * (_ll(ck, cn) + _ll(K - ck, N - cn) - base)
        if s > best[0]:
            best = (s, years[i + 1], (ck, cn), (K - ck, N - cn))
    return best

def permutation_null(years, k, n, n_perm=5000, min_entries=150, seed=11):
    """Reassign tagged entries across years at random, holding each year's total
    entry count fixed.  This is the null of 'the tag rate is constant in time'
    with the corpus's real, very uneven year sizes preserved."""
    rng = random.Random(seed)
    K, N = sum(k), sum(n)
    pool = [1] * K + [0] * (N - K)
    obs = scan(years, k, n, min_entries)[0]
    ge = 0; stats = []
    for _ in range(n_perm):
        rng.shuffle(pool)
        kk, pos = [], 0
        for ni in n:
            kk.append(sum(pool[pos:pos + ni])); pos += ni
        s = scan(years, kk, n, min_entries)[0]
        stats.append(s)
        if s >= obs:
            ge += 1
    stats.sort()
    return {"observed": obs, "p": (ge + 1) / (n_perm + 1), "n_perm": n_perm,
            "null_p95": stats[int(0.95 * n_perm)], "null_max": stats[-1],
            "null_median": stats[n_perm // 2]}

def bootstrap_cut(years, k, n, n_boot=2000, min_entries=150, seed=23):
    """Resample YEARS with replacement (the year is the replication unit: entries
    within a year share a source and are not independent)."""
    rng = random.Random(seed)
    m = len(years); cuts = []
    for _ in range(n_boot):
        idx = sorted(rng.randrange(m) for _ in range(m))
        yy = [years[i] for i in idx]
        kk = [k[i] for i in idx]
        nn = [n[i] for i in idx]
        c = scan(yy, kk, nn, min_entries)[1]
        if c is not None:
            cuts.append(c)
    cuts.sort()
    if not cuts:
        return None
    return {"n": len(cuts), "lo95": cuts[int(0.025 * len(cuts))],
            "hi95": cuts[int(0.975 * len(cuts))], "median": cuts[len(cuts) // 2]}

def fisher_exact_greater(a, b, c, d):
    """One-sided P(X >= a) for the 2x2 [[a,b],[c,d]] hypergeometric."""
    from math import comb
    n1, n2 = a + b, c + d
    t = a + c
    tot = n1 + n2
    lo = max(0, t - n2); hi = min(n1, t)
    denom = comb(tot, t)
    return sum(comb(n1, x) * comb(n2, t - x) for x in range(a, hi + 1)) / denom
