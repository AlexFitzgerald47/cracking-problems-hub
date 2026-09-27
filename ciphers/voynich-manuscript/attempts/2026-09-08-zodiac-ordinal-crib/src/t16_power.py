#!/usr/bin/env python3
"""T16: power analysis for T10 (the global seven-class test).

board/PRACTICES.md: run the null, and report where it has no power. T10 failed to find
a manuscript-wide seven-class code table; that is only a result if T10 could have found
one. Here a global cycle of known strength is INJECTED into the real ring structure and
the same fit is re-run, so the negative arrives with the effect size it can rule out.

alpha = fraction of labels whose ending is dictated by its class. alpha=0 reproduces the
null; alpha=1 is a perfectly regular seven-class code.

Fast scorer: per ring and phase, the (P x ncode) class-by-coda count matrix is
precomputed, so coordinate ascent is matrix arithmetic rather than a Python loop.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L
from t6_regime import ORDER

P = 7
ALPHAS = [0.0, 0.10, 0.20, 0.30, 0.45, 0.60, 0.80, 1.0]
REPS = 20
RESTARTS = 8
NNULL = 120


def get_rings(minn=8):
    z = L.ring_strings(L.load())
    return {k: v for k, v in z.items() if len(v) >= minn}


def encode(rings):
    vocab, out = {}, []
    for k in sorted(rings, key=lambda k: (ORDER.index(k[0]), k[1])):
        out.append(np.array([vocab.setdefault(w[-2:], len(vocab)) for w in rings[k]]))
    return out, vocab


def phase_mats(seqs, ncode):
    mats = np.zeros((len(seqs), P, P, ncode), dtype=np.int32)
    for r, cod in enumerate(seqs):
        pos = np.arange(len(cod))
        for p in range(P):
            np.add.at(mats[r, p], ((pos + p) % P, cod), 1)
    return mats


def fit(mats, rng, restarts=RESTARTS):
    n = mats.shape[0]
    within = int((mats[:, 0] * (mats[:, 0] - 1) // 2).sum())
    best = -1
    for _ in range(restarts):
        ph = rng.integers(0, P, size=n)
        tot = mats[np.arange(n), ph].sum(axis=0)
        cur = int((tot * (tot - 1) // 2).sum()) - within
        for _sweep in range(6):
            moved = False
            for i in range(n):
                base = tot - mats[i, ph[i]]
                cand = base[None, :, :] + mats[i]           # (P, P, ncode)
                sc = (cand * (cand - 1) // 2).sum(axis=(1, 2)) - within
                p = int(sc.argmax())
                if sc[p] > cur:
                    cur, ph[i], tot, moved = int(sc[p]), p, base + mats[i, p], True
                else:
                    tot = base + mats[i, ph[i]]
            if not moved:
                break
        best = max(best, cur)
    return best


def z_of(seqs, ncode, rng, restarts=RESTARTS, nnull=NNULL):
    obs = fit(phase_mats(seqs, ncode), rng, restarts)
    # the null fit MUST get the same restart budget as the observed fit
    nulls = np.array([fit(phase_mats([rng.permutation(s) for s in seqs], ncode),
                          rng, restarts) for _ in range(nnull)], dtype=float)
    return (obs - nulls.mean()) / nulls.std(ddof=1), obs, nulls.mean()


def main():
    seqs, vocab = encode(get_rings())
    ncode = len(vocab)
    counts = np.bincount(np.concatenate(seqs), minlength=ncode)
    markers = np.argsort(-counts)[:P]
    inv = {v: k for k, v in vocab.items()}
    print(f"{len(seqs)} rings, {ncode} distinct codas; class markers = "
          f"{[inv[m] for m in markers]}")
    rng = np.random.default_rng(7)
    zr, obs, mu = z_of(seqs, ncode, rng, RESTARTS, 200)
    print(f"\nREAL DATA (period 7, all rings): obs={obs} null={mu:.1f} Z={zr:+.2f}\n")
    print("alpha=0 is within-ring permuted data: a true no-structure baseline")
    print(f"{'alpha':>6s} {'mean Z':>8s} {'sd':>6s} {'min Z':>7s} {'power(Z>2)':>11s}")
    out = {"real_Z": float(zr)}
    for a in ALPHAS:
        zs = []
        for rep in range(REPS):
            r = np.random.default_rng(9000 + 137 * rep + int(a * 1000))
            inj = []
            # start from within-ring PERMUTED data, so alpha=0 is a true no-structure
            # baseline rather than the observed corpus re-evaluated
            for s in [r.permutation(x) for x in seqs]:
                ph = int(r.integers(0, P))
                c = s.copy()
                hit = r.random(len(c)) < a
                idx = np.arange(len(c))
                c[hit] = markers[(idx[hit] + ph) % P]
                inj.append(c)
            zs.append(z_of(inj, ncode, r)[0])
        zs = np.array(zs)
        out[str(a)] = {"mean": float(zs.mean()), "sd": float(zs.std(ddof=1)),
                       "min": float(zs.min()), "power": float((zs > 2).mean())}
        print(f"{a:6.2f} {zs.mean():8.2f} {zs.std(ddof=1):6.2f} {zs.min():7.2f} "
              f"{(zs > 2).mean():11.2f}")
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                     'results', 't16_power.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
