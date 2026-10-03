#!/usr/bin/env python3
"""Null model for the corpus-wide face-blocked sweep.

The sweep finds 26 pairs at p <= 1e-4 where independent tests would predict ~0.1.
The tests are not independent -- the same 110 M-signs and 13 N-signs are reused
across 1430 pairs -- so the analytic expectation is not trustworthy. This prices the
sweep directly: permute every N-sign's line membership within each (tablet, face)
block, re-run the entire 1430-pair sweep, and count how many pairs clear each
threshold. Repeat. The observed count is read against that distribution.

Permuting within (tablet, face) preserves every block marginal, so it preserves the
powered-pair set exactly and destroys only the M-sign/N-sign association.
"""
import json, random, sys, time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import hypergeom_probability, odds_ratio
from finer_blocks import load_fine

MIN_SUPPORT = 20
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 50
THRESHOLDS = (0.05, 0.01, 1e-3, 1e-4)

corpus = Path(sys.argv[1])
fine = load_fine(corpus)
el = [ln for ln in fine if not ln.damaged and ln.m_signs and ln.n_signs]
by_face = defaultdict(list)
for ln in el:
    by_face[(ln.tablet, ln.surface)].append(ln)
faces = list(by_face.values())

sc, tc = Counter(), Counter()
for ln in el:
    for m in ln.m_signs:
        sc[m] += 1
    for n in ln.n_signs:
        tc[n] += 1
ms = sorted(m for m, v in sc.items() if v >= MIN_SUPPORT)
ns = sorted(n for n, v in tc.items() if v >= MIN_SUPPORT)

# Precompute per-face: index lists, M-membership bitsets, and N-membership.
face_m = [[set(i for i, ln in enumerate(bl) if m in ln.m_signs) for m in ms] for bl in faces]
face_n0 = [[set(i for i, ln in enumerate(bl) if n in ln.n_signs) for n in ns] for bl in faces]
sizes = [len(bl) for bl in faces]


def sweep(face_n):
    counts = {t: 0 for t in THRESHOLDS}
    best = []
    for mi, m in enumerate(ms):
        rel = [fi for fi in range(len(faces)) if face_m[fi][mi]]
        for ni, n in enumerate(ns):
            a = sum(len(face_m[fi][mi] & face_n[fi][ni]) for fi in range(len(faces)))
            b, c = sc[m] - a, tc[n] - a
            dd = len(el) - a - b - c
            enriched = odds_ratio(a, b, c, dd) > 1
            dist = [1.0]
            obs = mx = mn = 0
            for fi in rel:
                total = sizes[fi]
                s = len(face_m[fi][mi]); t = len(face_n[fi][ni])
                o = len(face_m[fi][mi] & face_n[fi][ni])
                lo, hi = max(0, s - (total - t)), min(s, t)
                obs += o; mx += hi; mn += lo
                if hi == lo:
                    continue
                local = [hypergeom_probability(k, s, t, total) for k in range(lo, hi + 1)]
                comb = [0.0] * (len(dist) + len(local) - 1)
                for i, pi in enumerate(dist):
                    if pi:
                        for j, pj in enumerate(local):
                            if pj:
                                comb[i + j] += pi * pj
                dist = comb
            shift = sum(max(0, len(face_m[fi][mi]) - (sizes[fi] - len(face_n[fi][ni])))
                        for fi in rel)
            if enriched:
                p = sum(dist[max(0, obs - shift):]); floor = sum(dist[max(0, mx - shift):])
            else:
                p = sum(dist[: obs - shift + 1]); floor = sum(dist[: mn - shift + 1])
            p, floor = min(1.0, p), min(1.0, floor)
            if floor > 0.05:
                continue
            for t_ in THRESHOLDS:
                if p <= t_:
                    counts[t_] += 1
            best.append(p)
    best.sort()
    return counts, (best[0] if best else 1.0)


t0 = time.time()
obs_counts, obs_min = sweep(face_n0)
print(f"observed: {obs_counts}  min p = {obs_min:.3e}   ({time.time()-t0:.0f}s per sweep)")

rng = random.Random(20261001)
null_counts = {t: [] for t in THRESHOLDS}
null_min = []
for rep in range(REPS):
    face_n = []
    for fi, bl in enumerate(faces):
        per = []
        for ni in range(len(ns)):
            k = len(face_n0[fi][ni])
            per.append(set(rng.sample(range(sizes[fi]), k)) if k else set())
        face_n.append(per)
    c, mp = sweep(face_n)
    for t_ in THRESHOLDS:
        null_counts[t_].append(c[t_])
    null_min.append(mp)
    if (rep + 1) % 10 == 0:
        print(f"  {rep+1}/{REPS} done ({time.time()-t0:.0f}s)")

out = {"replicates": REPS, "observed": {str(k): v for k, v in obs_counts.items()},
       "observed_min_p": obs_min,
       "null_counts": {str(k): v for k, v in null_counts.items()},
       "null_min_p": null_min}
Path("results").mkdir(exist_ok=True)
Path("results/sweep_null.json").write_text(json.dumps(out, indent=2) + "\n")

print(f"\n{'threshold':>10} {'observed':>9} {'null mean':>10} {'null max':>9} {'p (perm)':>9}")
for t_ in THRESHOLDS:
    nc = null_counts[t_]
    pe = (sum(1 for v in nc if v >= obs_counts[t_]) + 1) / (REPS + 1)
    print(f"{t_:>10g} {obs_counts[t_]:9} {sum(nc)/len(nc):10.2f} {max(nc):9} {pe:9.4f}")
print(f"\nsmallest p anywhere in a null sweep: {min(null_min):.3e}  "
      f"(observed sweep minimum {obs_min:.3e})")
