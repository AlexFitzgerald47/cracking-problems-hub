#!/usr/bin/env python3
"""Exact lower-tail probability for a uniform-multinomial chi-square.

P(chi2 <= c) for n items in k = 26 equiprobable bins, computed exactly.

Reduction: write n_i = base + d_i with base = n // k and sum d_i = rem = n % k.
Then chi2 = (sum d_i^2 - rem^2/k) / (n/k), a strictly increasing function of
the integer sum d_i^2, so the event "chi2 <= observed" is the integer event
"sum d_i^2 <= B" and the tail is a finite enumeration over multisets of d.
"""
from fractions import Fraction
from math import factorial
from decimal import Decimal, getcontext
getcontext().prec = 80

K = 26

def stats(counts):
    n = sum(counts); k = len(counts)
    e = Fraction(n, k)
    chi2 = sum((Fraction(c) - e) ** 2 for c in counts) / e
    base, rem = divmod(n, k)
    sumsq = sum((c - base) ** 2 for c in counts)
    return n, chi2, base, rem, sumsq

def shapes(rem, budget, base, k, cap=2_000_000):
    """Multisets (as sorted tuples) of nonzero d with sum = rem, sum d^2 <= budget."""
    top = int(budget ** 0.5)
    out = []
    def rec(maxv, sum_left, sq_left, cur):
        if len(out) > cap: raise MemoryError("shape cap exceeded")
        if sum_left == 0:
            out.append(tuple(cur)); # may still extend with +a/-a pairs
        if len(cur) >= k: return
        for d in range(min(maxv, top), -min(base, top) - 1, -1):
            if d == 0: continue
            if d * d > sq_left: continue
            # feasibility: remaining slots must be able to reach sum_left
            slots = k - len(cur) - 1
            if abs(sum_left - d) > slots * top: continue
            cur.append(d); rec(d, sum_left - d, sq_left - d * d, cur); cur.pop()
    rec(top, rem, budget, [])
    seen=set(); uniq=[]
    for t in out:
        key=tuple(sorted(t))
        if key in seen: continue
        seen.add(key); uniq.append(key)
    return uniq

def weight(dvec, n, base, k):
    from collections import Counter
    nz=len(dvec); mult=Counter(dvec)
    ways=factorial(k)
    for v in mult.values(): ways//=factorial(v)
    ways//=factorial(k-nz)
    den=1
    for d in dvec: den*=factorial(base+d)
    den*=factorial(base)**(k-nz)
    q,r=divmod(factorial(n), den)
    assert r==0
    return ways, ways*q

def exact_lower_tail(counts, k=K, cap=2_000_000):
    n, chi2, base, rem, sumsq = stats(counts)
    sh = shapes(rem, sumsq, base, k, cap)
    tot = 0; nvec = 0
    for s in sh:
        if sum(s) != rem or sum(x*x for x in s) > sumsq: continue
        w, t = weight(s, n, base, k)
        tot += t; nvec += w
    P = Decimal(tot) / Decimal(k ** n)
    return {"n": n, "chi2": float(chi2), "chi2_exact": str(chi2), "sumsq": sumsq,
            "shapes": len(sh), "count_vectors": nvec, "P_le": P}

def mc_lower_tail(counts, reps=200_000, seed=1, k=K):
    import random
    rng = random.Random(seed)
    n, chi2, base, rem, sumsq = stats(counts)
    hit = 0
    for _ in range(reps):
        c = [0]*k
        for _ in range(n): c[rng.randrange(k)] += 1
        if sum((x-base)**2 for x in c) <= sumsq: hit += 1
    return {"n": n, "chi2": float(chi2), "P_le_mc": (hit+1)/(reps+1), "hits": hit, "reps": reps}
