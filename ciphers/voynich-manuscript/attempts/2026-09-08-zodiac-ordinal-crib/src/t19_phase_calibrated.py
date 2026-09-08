#!/usr/bin/env python3
"""T19: budget-matched replacement for T10.

T10 fitted one phase per ring by coordinate ascent with 40 restarts for the observed
data but only 5 for each null replicate. That is the search-budget mismatch
board/PRACTICES.md warns about, and T16 measured its size: with NO cycle present the
statistic still returns Z ~ 2. This rerun gives the observed fit and every null fit the
same number of restarts, so Z = 0 means 'no signal'.

Supersedes the numbers in t10_phase.py. That script is kept for the record.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t16_power as T
from t6_regime import ORDER

RESTARTS, NNULL = 8, 400


def z_matched(seqs, ncode, rng, period):
    T.P = period
    obs = T.fit(T.phase_mats(seqs, ncode), rng, RESTARTS)
    nulls = np.array([T.fit(T.phase_mats([rng.permutation(s) for s in seqs], ncode),
                            rng, RESTARTS) for _ in range(NNULL)], dtype=float)
    z = (obs - nulls.mean()) / nulls.std(ddof=1)
    p = (np.sum(nulls >= obs) + 1) / (NNULL + 1)
    return obs, nulls.mean(), z, p


def main():
    rings = T.get_rings()
    print("== T19: global cycle test, observed and null fitted at the SAME budget ==\n")
    print(f"{'set':26s} {'period':>6s} {'rings':>5s} {'obs':>5s} {'null':>7s} {'Z':>7s} {'p':>7s}")
    out = {}
    sets = {
        "ALL zodiac rings": rings,
        "EARLY Pisces-Cancer": {k: v for k, v in rings.items() if ORDER.index(k[0]) < 7},
        "LATE Leo-Sagittarius": {k: v for k, v in rings.items() if ORDER.index(k[0]) >= 7},
    }
    for name, rr in sets.items():
        seqs, vocab = T.encode(rr)
        for per in (5, 6, 7, 8, 9, 10):
            rng = np.random.default_rng(500 + per)
            o, m, z, p = z_matched(seqs, len(vocab), rng, per)
            out[f"{name}|{per}"] = {"obs": int(o), "null": float(m), "z": float(z), "p": float(p)}
            print(f"{name:26s} {per:6d} {len(seqs):5d} {o:5d} {m:7.1f} {z:+7.2f} {p:7.4f}")
        print()
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                     'results', 't19_phase_calibrated.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
