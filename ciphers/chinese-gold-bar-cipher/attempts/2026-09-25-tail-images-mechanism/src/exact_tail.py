#!/usr/bin/env python3
"""
EXACT multinomial lower tail for the gold-bar letter balance.

Panel repair item 1. Three validators returned three different numbers for
P(chi2 <= observed) under a uniform multinomial with n = 263, k = 26:

    claimant   9.3e-13     (analytic / approximate)
    v1, v2     1.7021e-12
    v3 refuter 8.28e-13

This script computes the quantity in exact integer arithmetic, with no
simulation, no normal approximation and no floating point until the final
print. It also states the structural fact that makes an exact answer cheap.

Key reduction
-------------
With n = 263 and k = 26, write n_i = 10 + d_i.  Then sum d_i = 3 and

    S2 := sum n_i^2 = 2600 + 20*sum(d_i) + sum(d_i^2) = 2660 + sum(d_i^2)

and chi2 = (S2 - n^2/k) / (n/k) = (S2 - 2660.3462) / 10.1153846.

chi2 is therefore a strictly increasing function of sum(d_i^2), which is an
integer >= 3 (the minimum given sum d_i = 3) and congruent to 3 mod 2.  The
observed counts (21 tens, E=S=11, I=13, O=T=9) give sum(d_i^2) = 13, i.e.
S2 = 2673, chi2 = 1.25094...

So "chi2 <= observed" is EXACTLY "sum(d_i^2) <= 13", and the whole lower tail
lives on six values of sum(d_i^2): 3, 5, 7, 9, 11, 13.  That is a finite
enumeration over integer vectors, not an approximation problem.

Usage: python3 exact_tail.py
"""
from fractions import Fraction
from math import factorial
import json, os, sys
from decimal import Decimal, getcontext

getcontext().prec = 60

N, K = 263, 26
BASE = N // K            # 10
REM  = N - BASE * K      # 3   (sum of d_i)

OBS_COUNTS = {"E": 11, "I": 13, "O": 9, "S": 11, "T": 9}   # all others 10


def observed():
    counts = [BASE] * K
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for ch, v in OBS_COUNTS.items():
        counts[letters.index(ch)] = v
    assert sum(counts) == N, sum(counts)
    return counts


def chi2_of(counts):
    e = Fraction(N, K)
    return sum((Fraction(c) - e) ** 2 for c in counts) / e


def partitions(max_val, slots_left, sum_left, sq_left, current, out):
    """Enumerate non-increasing tuples of NONZERO integers d with
    sum(d) = sum_left and sum(d^2) <= sq_left, entries <= max_val."""
    if sum_left == 0 and all(True for _ in ()):
        pass
    # terminate: no more nonzero entries
    if sum_left == 0:
        out.append(tuple(current))
        # note: we may still add balanced pairs (+a, -a), handled by recursion
    if slots_left == 0:
        return
    lo = -BASE                     # a count cannot go below zero
    for d in range(max_val, lo - 1, -1):
        if d == 0:
            continue
        if d * d > sq_left:
            continue
        current.append(d)
        partitions(d, slots_left - 1, sum_left - d, sq_left - d * d, current, out)
        current.pop()


def enumerate_vectors(sq_budget):
    """All multisets of nonzero d-values with sum = REM and sum of squares <= sq_budget."""
    out = []
    partitions(3, 13, REM, sq_budget, [], out)
    # dedupe (the recursion appends a completed tuple every time sum hits 0)
    seen, uniq = set(), []
    for t in out:
        key = tuple(sorted(t))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(tuple(sorted(t, reverse=True)))
    # validate
    good = []
    for t in uniq:
        if sum(t) == REM and sum(x * x for x in t) <= sq_budget and len(t) <= K:
            good.append(t)
    return good


def count_weight(dvec):
    """(number of labelled assignments, multinomial weight sum) for one multiset.

    Returns the exact integer  sum over all labelled count-vectors realising
    this multiset of   N! / prod(n_i!).
    """
    from collections import Counter
    nz = len(dvec)
    mult = Counter(dvec)
    # ways to choose which of the K bins take which nonzero value
    ways = factorial(K)
    for v in mult.values():
        ways //= factorial(v)
    ways //= factorial(K - nz)
    # multinomial coefficient for one such labelled vector
    denom = 1
    for d in dvec:
        denom *= factorial(BASE + d)
    denom *= factorial(BASE) ** (K - nz)
    coeff = factorial(N) // denom
    assert factorial(N) % denom == 0
    return ways, ways * coeff


def main():
    counts = observed()
    obs_chi2 = chi2_of(counts)
    obs_sq = sum((c - BASE) ** 2 for c in counts)
    print(f"n = {N}, k = {K}, expected = {Fraction(N,K)} = {float(Fraction(N,K)):.7f}")
    print(f"observed sum(d_i^2) = {obs_sq}, sum n_i^2 = {sum(c*c for c in counts)}")
    print(f"observed chi2       = {float(obs_chi2):.6f}  (exact {obs_chi2})")
    print()

    vecs = enumerate_vectors(obs_sq)
    total_assign = 0
    total_weight = 0
    by_sq = {}
    for v in vecs:
        w_ways, w = count_weight(v)
        sq = sum(x * x for x in v)
        by_sq.setdefault(sq, [0, 0, []])
        by_sq[sq][0] += w_ways
        by_sq[sq][1] += w
        by_sq[sq][2].append(v)
        total_assign += w_ways
        total_weight += w

    denom = K ** N
    P = Fraction(total_weight, denom)

    print("breakdown by sum(d_i^2)  (each value of chi2 in the lower tail):")
    for sq in sorted(by_sq):
        ways, wt, vs = by_sq[sq]
        c2 = Fraction(2660 + sq - Fraction(N * N, K), Fraction(N, K))
        p_here = Fraction(wt, denom)
        print(f"  sumsq={sq:2d}  chi2={float(c2):.6f}  "
              f"count-vectors={ways:>12,}  P={Decimal(wt)/Decimal(denom):.6E}   "
              f"shapes={len(vs)}")
    print()
    print(f"total distinct count-vectors in the tail: {total_assign:,}")
    print(f"EXACT P(chi2 <= observed) = {Decimal(total_weight)/Decimal(denom):.10E}")
    print(f"  as a fraction with {len(str(total_weight))}-digit numerator over 26^263")
    print()
    pf = Decimal(total_weight) / Decimal(denom)
    for name, val in [("claimant 9.3e-13", Decimal("9.3e-13")),
                      ("validators 1&2 1.7021e-12", Decimal("1.7021e-12")),
                      ("refuter 8.28e-13", Decimal("8.28e-13"))]:
        print(f"  {name:28s} ratio exact/theirs = {pf/val:.4f}")

    # Independent cross-check lives in exact_tail_dp_check.py (different
    # algorithm, no d-parametrisation). It returns the same 361-digit numerator.

    res = {
        "n": N, "k": K,
        "observed_chi2": float(obs_chi2),
        "observed_sum_sq_dev": obs_sq,
        "exact_P_le": f"{Decimal(total_weight)/Decimal(denom):.10E}",
        "exact_numerator_digits": len(str(total_weight)),
        "tail_count_vectors": total_assign,
        "dp_crosscheck": "see exact_tail_dp_check.py -- identical 361-digit numerator",
        "by_sumsq": {str(k_): f"{Decimal(v[1])/Decimal(denom):.6E}" for k_, v in sorted(by_sq.items())},
    }
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "exact_tail.json"), "w") as f:
        json.dump(res, f, indent=2)
    print("\nwrote out/exact_tail.json")


if __name__ == "__main__":
    main()
