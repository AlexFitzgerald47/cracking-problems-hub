#!/usr/bin/env python3
"""T9: controls for the lag-7 coda2 effect.

(a) ring-size stratification: in a ring of 10, lag 7 == cyclic distance 3, so the
    effect must be shown in rings where lag 7 is NOT a small cyclic distance.
(b) cyclic-distance version of the same statistic.
(c) control corpora with the same ring-size profile: herbal/pharma 'L' labels,
    Quire-20 starred-paragraph first words, and running-text words cut into
    pseudo-rings of matched length.
"""
import sys, os, math, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER
from t8_period import simmat, lag_stats, stouffer, MEAS

RNG = np.random.default_rng(4242)
NPERM = 20000


def cyc_stats(M, c, nperm=NPERM, rng=RNG):
    n = M.shape[0]
    if c > n // 2:
        return None
    i = np.arange(n)
    j = (i + c) % n
    if c * 2 == n:
        i, j = i[:n // 2], j[:n // 2]
    obs = M[i, j].mean()
    perms = np.argsort(rng.random((nperm, n)), axis=1)
    vals = M[perms[:, i], perms[:, j]].mean(axis=1)
    mu, sd = vals.mean(), vals.std(ddof=1)
    return {"obs": float(obs), "mu": float(mu), "z": float((obs - mu) / sd) if sd else 0.0,
            "p": float((np.sum(vals >= obs) + 1) / (nperm + 1))}


def zodiac_rings(minn=8):
    rows = L.load()
    z = L.ring_strings(rows)
    return {k: v for k, v in z.items() if len(v) >= minn}, rows


def control_rings(rows, size_profile):
    """Build control ring sets with the same size profile as the zodiac rings."""
    out = {}
    # (a) herbal/pharma L labels grouped per folio
    byf = {}
    for r in rows:
        if r["ltype"] == "L" and r["words"]:
            byf.setdefault(r["folio"], []).append((r["lnum"], r["line"], "".join(r["words"])))
    Lseq = [x[2] for f in sorted(byf) for x in sorted(byf[f])]
    # (b) Q20 starred-paragraph first words
    q = []
    for r in rows:
        if r["ltype"] == "S" and r["folio"] not in L.ZODIAC_FOLIOS and r["words"]:
            q.append((r["folio"], r["lnum"], r["line"], r["words"][0]))
    q.sort()
    Qseq = [x[3] for x in q]
    # (c) running text
    P = [w for r in rows if r["ltype"] == "P" for w in r["words"]]
    for name, seq in (("Llabels", Lseq), ("Q20first", Qseq), ("runningP", P)):
        rings, pos = {}, 0
        for i, n in enumerate(size_profile):
            if pos + n > len(seq):
                break
            rings[(name, i)] = seq[pos:pos + n]
            pos += n
        out[name] = rings
    return out


def profile(rings, tag, meas="coda2", lags=range(1, 11), cyclic=False):
    simf = MEAS[meas]
    mats = {k: simmat(v, simf) for k, v in rings.items()}
    line = []
    for d in lags:
        zs, obs, mus = [], [], []
        for k, M in mats.items():
            r = cyc_stats(M, d) if cyclic else lag_stats(M, d)
            if r is None:
                continue
            zs.append(r["z"]); obs.append(r["obs"]); mus.append(r["mu"])
        if zs:
            line.append((d, len(zs), sum(obs)/len(obs), sum(mus)/len(mus), stouffer(zs)))
    print(f"-- {tag} ({meas}, {'cyclic dist' if cyclic else 'linear lag'}) --")
    for d, u, o, m, z in line:
        star = "  <<<" if d == 7 else ""
        print(f"   d={d:2d} units={u:2d} obs={o:.4f} null={m:.4f} Z={z:+7.3f}{star}")
    return line


def main():
    zr, rows = zodiac_rings()
    sizes = sorted(len(v) for v in zr.values())
    print("zodiac ring sizes:", sizes, "\n")

    big = {k: v for k, v in zr.items() if len(v) >= 14}
    small = {k: v for k, v in zr.items() if len(v) < 14}
    print(f"(a) STRATIFICATION: big rings n>=14 -> {len(big)}; small n<14 -> {len(small)}")
    print("    in big rings lag 7 is cyclic distance 7 for n=15..20 (never <=5)\n")
    profile(big, "ZODIAC big rings (n>=14)")
    print()
    profile(small, "ZODIAC small rings (n<14)")

    print("\n(b) CYCLIC DISTANCE on all zodiac rings")
    profile(zr, "ZODIAC all rings", cyclic=True, lags=range(1, 11))

    print("\n(c) CONTROL CORPORA with matched ring-size profile")
    ctrl = control_rings(rows, [len(v) for v in zr.values()])
    for name, rings in ctrl.items():
        print()
        profile(rings, f"CONTROL {name} ({len(rings)} rings)")


if __name__ == "__main__":
    main()
