#!/usr/bin/env python3
"""P1: does the letter balance survive the photographic correction?"""
import collections, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tail import exact_lower_tail, K
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def counts_of(text):
    c = collections.Counter(text)
    return [c.get(ch, 0) for ch in A]

for name, path in [("IACR (263 letters)", "attempts/2026-09-24-is-it-a-cipher/data/cryptograms.txt"),
                   ("photographic (261 letters)", "attempts/2026-09-25-tail-images-mechanism/data/cryptograms_corrected.txt")]:
    p = os.path.join(os.path.dirname(os.path.dirname(HERE)), "chinese-gold-bar-cipher", *path.split("/")[1:]) \
        if False else os.path.join(os.path.dirname(HERE), *path.split("/")[1:])
    txt = "".join(l.strip() for l in open(p) if l.strip())
    c = counts_of(txt)
    r = exact_lower_tail(c)
    at10 = sum(1 for x in c if x == 10)
    print(f"\n{name}")
    print(f"  counts: " + " ".join(f"{ch}{v}" for ch, v in zip(A, c) if v != 10) + f"   (+{at10} letters at exactly 10)")
    print(f"  n = {r['n']}  chi2 = {r['chi2']:.6f} (exact {r['chi2_exact']})  sum d^2 = {r['sumsq']}")
    print(f"  shapes enumerated = {r['shapes']}, count-vectors in tail = {r['count_vectors']:,}")
    print(f"  EXACT P(chi2 <= obs) = {r['P_le']:.6E}")
