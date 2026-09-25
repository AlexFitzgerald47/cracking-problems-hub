#!/usr/bin/env python3
"""
Independent cross-check of exact_tail.py by a different algorithm.

exact_tail.py enumerates multisets of deviations d_i = n_i - 10.  This script
does NOT use that reduction.  It runs a dynamic program over (bins used,
total so far, sum of squares so far) with exact integer arithmetic, pruning
only on a provable lower bound for the sum of squares the remaining bins must
contribute (a balanced split minimises sum of squares for a fixed total).

Weight carried is  W(b,t,s) = sum over count-vectors of b bins  t! / prod(n_i!),
built up with binomial coefficients, so every number is an exact integer.

Usage: python3 exact_tail_dp_check.py
"""
from math import comb, factorial
from decimal import Decimal, getcontext
getcontext().prec = 60

N, K = 263, 26
S2_MAX = 2673          # = sum n_i^2 for the observed counts

def min_future_sumsq(total, bins):
    """Minimum of sum n_i^2 over `bins` non-negative integers summing to `total`."""
    if bins == 0:
        return 0 if total == 0 else None
    q, r = divmod(total, bins)
    return r * (q + 1) ** 2 + (bins - r) * q ** 2

# dp[(t, s)] = sum over ordered count-vectors of the bins placed so far of
#              t! / prod(n_i!)   -- an exact integer
dp = {(0, 0): 1}
for b in range(K):
    bins_left_after = K - b - 1
    nd = {}
    for (t, s), w in dp.items():
        for j in range(0, N - t + 1):
            ns, nt = s + j * j, t + j
            if ns > S2_MAX:
                break
            fut = min_future_sumsq(N - nt, bins_left_after)
            if fut is None or ns + fut > S2_MAX:
                continue
            key = (nt, ns)
            # t! / prod = (t-j)!/prod_prev * C(t, j)
            nd[key] = nd.get(key, 0) + w * comb(nt, j)
    dp = nd

tot = sum(w for (t, s), w in dp.items() if t == N and s <= S2_MAX)
P = Decimal(tot) / Decimal(K ** N)
print(f"DP states at the end: {len(dp)}")
print(f"DP exact numerator digits: {len(str(tot))}")
print(f"DP P(chi2 <= observed) = {P:.10E}")
print(f"expected from enumeration: 1.7020973493E-12")
