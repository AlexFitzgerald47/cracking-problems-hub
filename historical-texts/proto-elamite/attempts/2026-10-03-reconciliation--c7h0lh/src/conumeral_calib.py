"""Null model for the co-numeral test, run on MY implementation before any of
its verdicts is believed.  Permutes the target within stratum -- destroying any
association with the M-sign while preserving every stratum marginal -- and
measures the realised type-I error."""
from __future__ import annotations
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from recon_common import (load_eligible, hypergeom_probability, blocks_of,
                          PUBLISHED_EIGHT)

corpus = Path(sys.argv[1])
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
_, _, eligible = load_eligible(corpus)
rng = random.Random(20261003)


def run(m, t, direction, reps):
    """Fast path: precompute per-stratum (n, s) and the target count, then
    re-deal target labels within stratum each replicate."""
    strata = []
    for bl in blocks_of(eligible, lambda l: frozenset(l.n_signs - {t})).values():
        n = len(bl)
        s = sum(m in l.m_signs for l in bl)
        tt = sum(t in l.n_signs for l in bl)
        if s and tt and n:
            strata.append((n, s, tt))
    # exact null distribution of the total overlap, by convolution
    dist = [1.0]
    for n, s, tt in strata:
        lo, hi = max(0, s - (n - tt)), min(s, tt)
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, tt, n)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    tail = ([sum(dist[k:]) for k in range(len(dist))] if direction == "enriched"
            else [sum(dist[: k + 1]) for k in range(len(dist))])
    hits05 = hits01 = 0
    for _ in range(reps):
        tot = 0
        for n, s, tt in strata:
            # hypergeometric draw: how many of the s sign-lines get the target
            pool = [1] * tt + [0] * (n - tt)
            rng.shuffle(pool)
            tot += sum(pool[:s])
        p = tail[min(tot, len(tail) - 1)]
        hits05 += p <= 0.05
        hits01 += p <= 0.01
    return hits05 / reps, hits01 / reps


out = {}
print(f"co-numeral test, type-I error, {REPS} replicates per pair")
print(f"{'pair':12s} {'a=.05':>8s} {'a=.01':>8s}")
for m, t, d in PUBLISHED_EIGHT:
    r05, r01 = run(m, t, d, REPS)
    out[f"{m}-{t}"] = {"alpha_05": r05, "alpha_01": r01, "replicates": REPS}
    print(f"{m}-{t:12s} {r05:8.4f} {r01:8.4f}")
Path("results/conumeral_calibration.json").write_text(json.dumps(out, indent=2))
print("\nwrote results/conumeral_calibration.json")
