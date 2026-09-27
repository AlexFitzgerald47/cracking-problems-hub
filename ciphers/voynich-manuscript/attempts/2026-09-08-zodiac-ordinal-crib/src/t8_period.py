#!/usr/bin/env python3
"""T8: full lag/period profile of zodiac label similarity, with split-half replication.

H2 predicts a lag with astrological meaning (7 = degree-ruler / monomoiria cycle,
10 = decan, 3, 5, 9, 12) that replicates across independent groups of rings.

Unit of analysis = one ring (the transcriber's physical traversal). Similarity
matrices are precomputed so the permutation null is exact and cheap.
"""
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L, simlib
from t6_regime import ORDER, SIGN

MAXLAG = 14
NPERM = 20000
RNG = np.random.default_rng(20260908)


def simmat(seq, simf):
    n = len(seq)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            M[i, j] = M[j, i] = simf(seq[i], seq[j])
    return M


def lag_stats(M, d, nperm=NPERM, rng=RNG):
    n = M.shape[0]
    if n - d < 3:
        return None
    idx = np.arange(n - d)
    obs = M[idx, idx + d].mean()
    perms = np.argsort(rng.random((nperm, n)), axis=1)
    a = perms[:, :n - d]
    b = perms[:, d:]
    vals = M[a, b].mean(axis=1)
    mu, sd = vals.mean(), vals.std(ddof=1)
    return {"obs": float(obs), "mu": float(mu), "sd": float(sd),
            "z": float((obs - mu) / sd) if sd > 0 else 0.0,
            "p": float((np.sum(vals >= obs) + 1) / (nperm + 1)),
            "npairs": int(n - d)}


MEAS = {
    "coda2": lambda a, b: 1.0 if a[-2:] == b[-2:] else 0.0,
    "coda1": lambda a, b: 1.0 if a[-1:] == b[-1:] else 0.0,
    "coda3": lambda a, b: 1.0 if a[-3:] == b[-3:] else 0.0,
    "onset2": lambda a, b: 1.0 if a[:2] == b[:2] else 0.0,
    "lev": simlib.sim_lev,
    "lcs": simlib.sim_lcs,
    "exact": lambda a, b: 1.0 if a == b else 0.0,
}


def build_units():
    rows = L.load()
    z = L.ring_strings(rows)
    units = {}
    for (f, r), v in z.items():
        if len(v) >= 8:
            units[(f, r)] = v
    return units, z


def stouffer(zs):
    zs = [x for x in zs if x is not None]
    return sum(zs) / math.sqrt(len(zs)) if zs else float('nan')


def run(units, tag, out):
    for mname, simf in MEAS.items():
        mats = {k: simmat(v, simf) for k, v in units.items()}
        for d in range(1, MAXLAG + 1):
            zs, obs, mus, npair = [], [], [], 0
            for k, M in mats.items():
                r = lag_stats(M, d)
                if r is None:
                    continue
                zs.append(r["z"]); obs.append(r["obs"]); mus.append(r["mu"])
                npair += r["npairs"]
                out.append({"group": tag, "meas": mname, "lag": d, "unit": str(k), **r})
            if zs:
                print(f"{tag:14s} {mname:7s} lag {d:2d}  units={len(zs):2d} pairs={npair:4d} "
                      f"obs={sum(obs)/len(obs):.4f} null={sum(mus)/len(mus):.4f} Z={stouffer(zs):+7.3f}")


def main():
    units, z = build_units()
    print(f"{len(units)} rings with n>=8; "
          f"{sum(len(v) for v in units.values())} labels\n")
    out = []
    run(units, "ALL", out)

    print("\n== split-half replication (independent ring sets) ==")
    keys = sorted(units)
    early = {k: units[k] for k in keys if ORDER.index(k[0]) < 7}
    late = {k: units[k] for k in keys if ORDER.index(k[0]) >= 7}
    print(f"early rings: {len(early)}   late rings: {len(late)}\n")
    run(early, "EARLY(Psc-Cnc)", out)
    print()
    run(late, "LATE(Leo-Sgr)", out)

    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '..', 'results', 't8_period_raw.json'), 'w'))


if __name__ == '__main__':
    main()
