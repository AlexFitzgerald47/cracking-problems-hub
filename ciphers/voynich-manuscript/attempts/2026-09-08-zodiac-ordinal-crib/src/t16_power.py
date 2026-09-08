#!/usr/bin/env python3
"""T16: power analysis for T10 (the global seven-class test).

`board/PRACTICES.md`: run the null, and report where it has no power. T10 failed to
find a manuscript-wide seven-class code table. That is only a result if T10 could have
found one. Here a global cycle of known strength is INJECTED into the real ring
structure and T10 is re-run, so the negative comes with the alpha it can actually rule
out.

alpha = fraction of labels whose ending is dictated by its class. alpha=0 is the null;
alpha=1 is a perfectly regular seven-class code; real medieval list codes would sit
somewhere in between.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
import t10_phase as T
from t6_regime import ORDER

ALPHAS = [0.0, 0.15, 0.30, 0.50, 0.75, 1.0]
REPS = 12
RESTARTS = 12
NNULL = 100


def fit_and_z(units, ncode, rng):
    obs, _ = T.fit(units, ncode, rng, restarts=RESTARTS)
    nulls = []
    for _ in range(NNULL):
        perm = []
        for (k, pos, cod) in units:
            c = cod.copy(); rng.shuffle(c)
            perm.append((k, pos, c))
        s, _ = T.fit(perm, ncode, rng, restarts=max(3, RESTARTS // 4))
        nulls.append(s)
    nulls = np.array(nulls, dtype=float)
    return (obs - nulls.mean()) / nulls.std(ddof=1)


def main():
    T.P = 7
    rings = T.get_rings()
    units, vocab = T.encode(rings)
    ncode = len(vocab)
    # the seven most frequent codas stand in for the seven class markers
    counts = np.zeros(ncode, dtype=int)
    for _, _, cod in units:
        for c in cod:
            counts[c] += 1
    markers = list(np.argsort(-counts)[:7])
    print(f"{len(units)} rings, {ncode} distinct codas; class markers = "
          f"{[k for k, v in sorted(vocab.items(), key=lambda kv: kv[1]) if v in markers]}\n")
    print(f"{'alpha':>6s} {'mean Z':>8s} {'sd':>6s} {'min':>7s} {'frac Z>2':>9s}")
    out = {}
    for a in ALPHAS:
        zs = []
        for rep in range(REPS):
            rng = np.random.default_rng(1000 * rep + int(a * 100))
            inj = []
            for (k, pos, cod) in units:
                ph = int(rng.integers(0, 7))
                c = cod.copy()
                for i in range(len(c)):
                    if rng.random() < a:
                        c[i] = markers[(i + ph) % 7]
                inj.append((k, pos, c))
            zs.append(fit_and_z(inj, ncode, rng))
        zs = np.array(zs)
        out[a] = {"mean": float(zs.mean()), "sd": float(zs.std(ddof=1)),
                  "min": float(zs.min()), "power": float((zs > 2).mean())}
        print(f"{a:6.2f} {zs.mean():8.2f} {zs.std(ddof=1):6.2f} {zs.min():7.2f} "
              f"{(zs > 2).mean():9.2f}")
    print("\nobserved Z on the real data (T10, period 7, all rings) = +2.05")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     '..', 'results', 't16_power.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
