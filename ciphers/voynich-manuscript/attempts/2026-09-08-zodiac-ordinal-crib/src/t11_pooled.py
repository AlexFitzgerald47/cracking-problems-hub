#!/usr/bin/env python3
"""T11: pooled lag analysis with nested ending features.

The ring-averaged Stouffer combination in T8 is not directly comparable across
features. Here every lag-d pair in every ring is pooled into one contingency and
the null permutes labels within each ring, so observed and null are the same
quantity. Nested features (last1 < last2 < last3) must move consistently: any pair
that gains a last-2 match also gains a last-1 match.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER

NPERM = 20000
FEATS = {
    "last1": lambda w: w[-1:],
    "last2": lambda w: w[-2:],
    "last3": lambda w: w[-3:],
    "penult_only": lambda w: w[-2:-1],
    "first1": lambda w: w[:1],
    "first2": lambda w: w[:2],
    "len": lambda w: str(len(w)),
}


def pooled(rings, feat, maxlag=10, nperm=NPERM, seed=9):
    rng = np.random.default_rng(seed)
    codes = {}
    seqs = []
    for k in sorted(rings, key=lambda k: (ORDER.index(k[0]), k[1])):
        seqs.append(np.array([codes.setdefault(feat(w), len(codes)) for w in rings[k]]))
    out = {}
    for d in range(1, maxlag + 1):
        obs = tot = 0
        usable = [s for s in seqs if len(s) - d >= 1]
        if not usable:
            continue
        for s in usable:
            obs += int(np.sum(s[:-d] == s[d:]))
            tot += len(s) - d
        nulls = np.zeros(nperm)
        for i in range(nperm):
            c = 0
            for s in usable:
                p = rng.permutation(s)
                c += int(np.sum(p[:-d] == p[d:]))
            nulls[i] = c
        mu, sd = nulls.mean(), nulls.std(ddof=1)
        out[d] = {"obs": obs, "tot": tot, "null": float(mu), "sd": float(sd),
                  "z": float((obs - mu) / sd) if sd else 0.0,
                  "p": float((np.sum(nulls >= obs) + 1) / (nperm + 1))}
    return out


def main():
    rows = L.load()
    z = L.ring_strings(rows)
    rings = {k: v for k, v in z.items() if len(v) >= 8}
    print(f"{len(rings)} rings, {sum(len(v) for v in rings.values())} labels\n")
    print(f"{'feature':12s} {'lag':>3s} {'obs':>5s} {'/pairs':>6s} {'null':>7s} {'ratio':>6s} {'Z':>7s} {'p':>8s}")
    allout = {}
    for fname, f in FEATS.items():
        res = pooled(rings, f)
        allout[fname] = res
        for d, r in res.items():
            flag = " <<<" if d == 7 else ""
            print(f"{fname:12s} {d:3d} {r['obs']:5d} {r['tot']:6d} {r['null']:7.1f} "
                  f"{r['obs']/r['null'] if r['null'] else 0:6.2f} {r['z']:+7.2f} {r['p']:8.4f}{flag}")
        print()
    json.dump(allout, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        '..', 'results', 't11_pooled.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
