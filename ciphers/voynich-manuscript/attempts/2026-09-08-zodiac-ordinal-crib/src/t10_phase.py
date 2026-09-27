#!/usr/bin/env python3
"""T10: is the period-7 structure GLOBAL?

A merely local periodicity means each ring repeats something with period 7.
A global cycle means every ring is a window on ONE 7-class system, so that after
aligning each ring by a phase, labels sharing a class agree on their ending
ACROSS rings.

Statistic: total cross-ring coda2 agreement among label pairs assigned to the same
class, maximised over one phase per ring by coordinate ascent with restarts.
Null: the identical fitting procedure (same restarts, same ascent) applied to rings
whose labels have been permuted. This is the matched-search-budget rule from
board/PRACTICES.md; the phases are fitted in both arms.
"""
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER, SIGN

P = 7
RESTARTS = 40
NNULL = 400


def get_rings(minn=8):
    rows = L.load()
    z = L.ring_strings(rows)
    return {k: v for k, v in z.items() if len(v) >= minn}


def encode(rings, key=lambda w: w[-2:]):
    """rings -> list of (ring_id, positions array, coda code array)"""
    vocab = {}
    out = []
    for k in sorted(rings, key=lambda k: (ORDER.index(k[0]), k[1])):
        v = rings[k]
        codes = []
        for w in v:
            c = key(w)
            codes.append(vocab.setdefault(c, len(vocab)))
        out.append((k, np.arange(len(v)), np.array(codes)))
    return out, vocab


def score(units, phases, ncode):
    """Cross-ring agreement: for each class, count same-coda pairs from DIFFERENT rings."""
    # counts[class][code][ring_index]
    tot = 0
    tab = [np.zeros((ncode,), dtype=np.int64) for _ in range(P)]
    per_ring = []
    for (k, pos, cod), ph in zip(units, phases):
        cls = (pos + ph) % P
        m = np.zeros((P, ncode), dtype=np.int64)
        for c, x in zip(cls, cod):
            m[c, x] += 1
        per_ring.append(m)
    M = np.sum(per_ring, axis=0)
    # pairs within class & code, minus within-ring pairs
    allp = (M * (M - 1) // 2).sum()
    within = sum((m * (m - 1) // 2).sum() for m in per_ring)
    return int(allp - within)


def fit(units, ncode, rng, restarts=RESTARTS):
    best = -1
    bestph = None
    n = len(units)
    for _ in range(restarts):
        ph = rng.integers(0, P, size=n).tolist()
        cur = score(units, ph, ncode)
        improved = True
        while improved:
            improved = False
            for i in range(n):
                old = ph[i]
                bs, bv = cur, old
                for v in range(P):
                    if v == old:
                        continue
                    ph[i] = v
                    s = score(units, ph, ncode)
                    if s > bs:
                        bs, bv = s, v
                ph[i] = bv
                if bs > cur:
                    cur, improved = bs, True
        if cur > best:
            best, bestph = cur, list(ph)
    return best, bestph


def run(rings, tag, period=P, seed=1):
    global P
    P = period
    units, vocab = encode(rings)
    ncode = len(vocab)
    rng = np.random.default_rng(seed)
    obs, ph = fit(units, ncode, rng)
    nulls = []
    for _ in range(NNULL):
        perm = []
        for (k, pos, cod) in units:
            c = cod.copy()
            rng.shuffle(c)
            perm.append((k, pos, c))
        s, _ = fit(perm, ncode, rng, restarts=max(4, RESTARTS // 8))
        nulls.append(s)
    nulls = np.array(nulls)
    z = (obs - nulls.mean()) / nulls.std(ddof=1)
    p = (np.sum(nulls >= obs) + 1) / (len(nulls) + 1)
    print(f"{tag:28s} period={period}  rings={len(units)}  obs={obs}  "
          f"null={nulls.mean():.1f}+-{nulls.std(ddof=1):.1f}  Z={z:+.2f}  p={p:.4f}")
    return obs, ph, z, p


def main():
    rings = get_rings()
    print("== T10: global 7-class alignment, cross-ring coda2 agreement ==")
    print("(null uses the same coordinate-ascent fit on permuted rings)\n")
    res = {}
    for per in (5, 6, 7, 8, 9, 10):
        o, ph, z, p = run(rings, "ALL zodiac rings", period=per, seed=100 + per)
        res[per] = {"obs": o, "z": z, "p": p, "phases": ph}
    print()
    early = {k: v for k, v in rings.items() if ORDER.index(k[0]) < 7}
    late = {k: v for k, v in rings.items() if ORDER.index(k[0]) >= 7}
    for per in (6, 7, 8):
        run(early, "EARLY (Pisces-Cancer)", period=per, seed=200 + per)
    print()
    for per in (6, 7, 8):
        run(late, "LATE (Leo-Sagittarius)", period=per, seed=300 + per)
    json.dump({str(k): {kk: vv for kk, vv in v.items()} for k, v in res.items()},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                'results', 't10_phase.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
