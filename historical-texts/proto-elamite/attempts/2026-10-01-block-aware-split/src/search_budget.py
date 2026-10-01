#!/usr/bin/env python3
"""How many pairs clear the face-blocked test?  (Search-freedom accounting.)

The 2026-09-04 screen corrected for multiple testing on the *pooled* Fisher statistic.
The face-blocked exact test has never been run across the candidate space, so the
board does not know how surprising a face-blocked p of 1e-4 is. This runs the test on
every (M-sign, N-sign) pair meeting the published support thresholds (>=20 lines each),
in both directions, applies Benjamini-Hochberg across the whole space, and reports
where the eight published pairs land.

Speed note, and it is also the ancillarity argument made concrete: a block with
hi == lo contributes a point mass at a fixed overlap, shifting the observed count and
the whole null distribution by the same constant. Dropping such blocks leaves the
p-value exactly unchanged. The code asserts this against the full convolution.
"""
import json, sys, time
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import CONFIRMED, bh_adjust, hypergeom_probability, odds_ratio
from finer_blocks import load_fine

MIN_SUPPORT = 20


def face_blocked_p(blocks_m, m, n, direction, drop_forced=True):
    dist = [1.0]; obs = mx = mn = inf = 0
    for bl in blocks_m:
        total = len(bl)
        s = sum(m in ln.m_signs for ln in bl)
        t = sum(n in ln.n_signs for ln in bl)
        o = sum(m in ln.m_signs and n in ln.n_signs for ln in bl)
        lo, hi = max(0, s - (total - t)), min(s, t)
        obs += o; mx += hi; mn += lo
        if hi == lo:
            if drop_forced:
                continue
        else:
            inf += 1
        local = [0.0] * (hi - lo + 1) if drop_forced else [0.0] * (hi + 1)
        base = lo if drop_forced else 0
        for k in range(lo, hi + 1):
            local[k - base] = hypergeom_probability(k, s, t, total)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    shift = sum(max(0, sum(m in ln.m_signs for ln in bl)
                    - (len(bl) - sum(n in ln.n_signs for ln in bl)))
                for bl in blocks_m) if drop_forced else 0
    o_idx = obs - shift
    mx_idx = mx - shift
    mn_idx = mn - shift
    if direction == "enriched":
        p = sum(dist[max(0, o_idx):]); floor = sum(dist[max(0, mx_idx):])
    else:
        p = sum(dist[: o_idx + 1]); floor = sum(dist[: mn_idx + 1])
    return min(1.0, p), min(1.0, floor), inf, obs, mx


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

# Equivalence check: dropping forced blocks must not change any published p.
for m, n, d in CONFIRMED:
    full = face_blocked_p(faces, m, n, d, drop_forced=False)
    fast = face_blocked_p(faces, m, n, d, drop_forced=True)
    assert abs(full[0] - fast[0]) < 1e-12 and abs(full[1] - fast[1]) < 1e-12, (m, n, full, fast)
print(f"forced-block dropping verified exact on all {len(CONFIRMED)} published pairs")

t0 = time.time()
rows = []
for m in ms:
    # Restrict to faces where this sign occurs at all; others are forced for every n.
    rel = [bl for bl in faces if any(m in ln.m_signs for ln in bl)]
    for n in ns:
        a = sum(1 for ln in el if m in ln.m_signs and n in ln.n_signs)
        b = sc[m] - a
        c = tc[n] - a
        dd = len(el) - a - b - c
        orat = odds_ratio(a, b, c, dd)
        d = "enriched" if orat > 1 else "depleted"
        p, floor, inf, obs, mx = face_blocked_p(rel, m, n, d)
        rows.append({"m": m, "n": n, "direction": d, "pooled_or": orat,
                     "p": p, "p_floor": floor, "informative_blocks": inf,
                     "observed_overlap": obs, "max_possible_overlap": mx,
                     "pooled_cells": [a, b, c, dd]})
print(f"{len(rows)} pairs tested in {time.time()-t0:.0f}s")

powered = [r for r in rows if r["p_floor"] <= 0.05]
qs = bh_adjust([r["p"] for r in powered])
for r, q in zip(powered, qs):
    r["q_over_powered_space"] = q
qs_all = bh_adjust([r["p"] for r in rows])
for r, q in zip(rows, qs_all):
    r["q_over_full_space"] = q

rows.sort(key=lambda r: r["p"])
pub = {(m, n) for m, n, _ in CONFIRMED}
out = {"candidate_pairs": len(rows), "powered_pairs": len(powered),
       "min_support": MIN_SUPPORT, "rows": rows}
Path("results").mkdir(exist_ok=True)
Path("results/search_budget.json").write_text(json.dumps(out, indent=2) + "\n")

print(f"\npowered pairs (face-blocked floor <= 0.05): {len(powered)} of {len(rows)}")
for thr in (0.05, 0.01, 1e-3, 1e-4):
    k = sum(1 for r in powered if r["p"] <= thr)
    print(f"   p <= {thr:<8g}: {k:4} pairs  (expected under global null ~ {thr*len(powered):.1f})")
print(f"\nwhere the eight published pairs rank among {len(rows)} candidates, by face-blocked p:")
print(f"{'rank':>5} {'pair':12} {'dir':9} {'infBlk':>7} {'floor':>10} {'p':>11} {'q(powered)':>11}")
for i, r in enumerate(rows, 1):
    if (r["m"], r["n"]) in pub:
        print(f"{i:5} {r['m']+'-'+r['n']:12} {r['direction']:9} {r['informative_blocks']:7} "
              f"{r['p_floor']:10.2e} {r['p']:11.3e} {r.get('q_over_powered_space', float('nan')):11.3e}")
print(f"\ntop 15 pairs overall by face-blocked p (published marked *):")
for i, r in enumerate(rows[:15], 1):
    mark = "*" if (r["m"], r["n"]) in pub else " "
    print(f"{i:5}{mark} {r['m']+'-'+r['n']:12} {r['direction']:9} {r['informative_blocks']:7} "
          f"{r['p']:11.3e} {r.get('q_over_powered_space', float('nan')):11.3e} OR={r['pooled_or']:.2f}")
