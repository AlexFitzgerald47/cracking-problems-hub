#!/usr/bin/env python3
"""Is the corpus pervasively structured, or is the procedure permissive?  (audits P6)

`competitors.py` finds that 121 of 560 testable (M-family, N-sign) pairs clear the
block-aware face-blocked gate. Two readings compete:

  (a) Proto-Elamite accounting really is pervasively structured -- particular commodity
      signs really do take particular numeral signs -- and the 2026-09-04 set of eight
      was a low-power sample of a much larger population; or
  (b) the procedure is permissive and 121 is mostly noise.

`null_calibration.py` answers this for one pair. This answers it for the whole sweep:
run the IDENTICAL sweep on data where every M/N association has been destroyed, and
count how many pairs pass. Null B of null_calibration.py is used -- each N-sign's
indicator is permuted within face strata, preserving its total count and its
obverse/reverse skew while destroying its association with any M-sign.

Direction is taken from the TRAINING complement, never from the validation data, so each
p-value is a clean one-sided test. (competitors.py deliberately took direction from
validation, to give every competitor its best shot; that inflates its count and is noted
in RESULTS.md. The number reported here is the clean one.)

Usage:  python3 competitor_null.py [reps] [/path/to/corpus]
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

from common import load_eligible, odds_ratio
from structure_associations import hypergeom_probability

MIN_SIGN_LINES = 20
MIN_TARGET_LINES = 20
MIN_VAL_SIGN_LINES = 5
ALPHA = 0.05


def build(lines):
    """Precompute everything invariant under an N-sign permutation."""
    blocks, btab, bidx = {}, [], []
    for ln in lines:
        key = (ln.tablet, ln.surface)
        if key not in blocks:
            blocks[key] = len(blocks)
            btab.append(ln.tablet)
        bidx.append(blocks[key])
    tab_ids = {}
    for ln in lines:
        tab_ids.setdefault(ln.tablet, len(tab_ids))
    nb, nt = len(blocks), len(tab_ids)
    btab_idx = [tab_ids[t] for t in btab]
    total = [0] * nb
    for b in bidx:
        total[b] += 1
    m_counts = Counter(s for ln in lines for s in ln.m_signs)
    n_counts = Counter(s for ln in lines for s in ln.n_signs)
    m_signs = sorted(s for s, c in m_counts.items() if c >= MIN_SIGN_LINES)
    n_signs = sorted(s for s, c in n_counts.items() if c >= MIN_TARGET_LINES)
    # per-M-sign: line flags and per-block counts (invariant across replicates)
    m_flags, m_block = {}, {}
    for m in m_signs:
        fl = [m in ln.m_signs for ln in lines]
        cnt = [0] * nb
        for i, v in enumerate(fl):
            if v:
                cnt[bidx[i]] += 1
        m_flags[m], m_block[m] = fl, cnt
    n_flags = {n: [n in ln.n_signs for ln in lines] for n in n_signs}
    strata = defaultdict(list)
    for i, ln in enumerate(lines):
        strata[ln.surface].append(i)
    return dict(bidx=bidx, btab_idx=btab_idx, total=total, nb=nb, nt=nt,
                m_signs=m_signs, n_signs=n_signs, m_flags=m_flags, m_block=m_block,
                n_flags=n_flags, strata=list(strata.values()), n_lines=len(lines))


def pair_test(G, m, n, nfl):
    """Block-aware split + exact face-blocked p, direction from the training complement."""
    nb, bidx, total = G["nb"], G["bidx"], G["total"]
    s = G["m_block"][m]
    mfl = G["m_flags"][m]
    t = [0] * nb
    obs = [0] * nb
    for i, v in enumerate(nfl):
        if v:
            b = bidx[i]
            t[b] += 1
            if mfl[i]:
                obs[b] += 1
    val_tabs = [False] * G["nt"]
    inf_any = False
    los = [0] * nb
    his = [0] * nb
    for b in range(nb):
        lo = s[b] - (total[b] - t[b])
        lo = lo if lo > 0 else 0
        hi = s[b] if s[b] < t[b] else t[b]
        los[b], his[b] = lo, hi
        if hi > lo:
            inf_any = True
            val_tabs[G["btab_idx"][b]] = True
    if not inf_any:
        return None
    keep = [b for b in range(nb) if val_tabs[G["btab_idx"][b]]]
    # --- contingency on each side, for support gates and the training direction ---
    in_val = [val_tabs[G["btab_idx"][bidx[i]]] for i in range(G["n_lines"])]
    ta = tb = tc = td = va = vb = 0
    for i in range(G["n_lines"]):
        hm, hn = mfl[i], nfl[i]
        if in_val[i]:
            if hm:
                va += 1
                if hn:
                    vb += 1
        else:
            if hm and hn:
                ta += 1
            elif hm:
                tb += 1
            elif hn:
                tc += 1
            else:
                td += 1
    if ta + tb < MIN_SIGN_LINES or ta + tc < MIN_TARGET_LINES or va < MIN_VAL_SIGN_LINES:
        return None
    train_or = odds_ratio(ta, tb, tc, td)
    direction = "enriched" if train_or >= 1.0 else "depleted"
    dist = [1.0]
    for b in keep:
        lo, hi = los[b], his[b]
        local = [0.0] * (hi + 1)
        for v in range(lo, hi + 1):
            local[v] = hypergeom_probability(v, s[b], t[b], total[b])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i2, pi in enumerate(dist):
            if pi:
                for j2, pj in enumerate(local):
                    if pj:
                        comb[i2 + j2] += pi * pj
        dist = comb
    o = sum(obs[b] for b in keep)
    mx = sum(his[b] for b in keep)
    mn = sum(los[b] for b in keep)
    if direction == "enriched":
        p = min(1.0, sum(dist[o:])); floor = min(1.0, sum(dist[mx:]))
    else:
        p = min(1.0, sum(dist[: o + 1])); floor = min(1.0, sum(dist[: mn + 1]))
    vor = odds_ratio(vb, va - vb, 0, 0) if False else None
    return dict(p=p, p_floor=floor, direction=direction, train_odds_ratio=train_or,
                observed=o, max_possible=mx, min_possible=mn)


def sweep(G, nfls):
    tested = passed = powered = 0
    rows = {}
    for m in G["m_signs"]:
        for n in G["n_signs"]:
            r = pair_test(G, m, n, nfls[n])
            if r is None:
                continue
            tested += 1
            if r["p_floor"] <= ALPHA:
                powered += 1
                if r["p"] <= ALPHA:
                    passed += 1
            rows[(m, n)] = r
    return tested, powered, passed, rows


def main() -> None:
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    argv = ["x"] + ([sys.argv[2]] if len(sys.argv) > 2 else [])
    lines = load_eligible(argv)
    G = build(lines)
    print(f"M-families {len(G['m_signs'])}, N-signs {len(G['n_signs'])}, "
          f"blocks {G['nb']}, tablets {G['nt']}")

    t0, pw0, ps0, rows0 = sweep(G, G["n_flags"])
    real = rows0.get(("M288", "N45"))
    ordered = sorted(rows0.items(), key=lambda kv: kv[1]["p"])
    rank = next(i for i, (k, _) in enumerate(ordered, 1) if k == ("M288", "N45"))
    print(f"\nREAL SWEEP (direction from training complement):")
    print(f"  tested {t0}, with power {pw0}, PASSING at 0.05: {ps0}")
    print(f"  M288-N45  p = {real['p']:.4e}  floor = {real['p_floor']:.3e}  "
          f"dir {real['direction']} (train OR {real['train_odds_ratio']:.2f})  rank {rank}/{t0}")

    rng = random.Random(20261002)
    counts, tested_counts = [], []
    hits_m288 = 0
    for rep in range(reps):
        nfls = {}
        for n, fl in G["n_flags"].items():
            out = list(fl)
            for idx in G["strata"]:
                if len(idx) > 1:
                    vals = [out[i] for i in idx]
                    rng.shuffle(vals)
                    for i, v in zip(idx, vals):
                        out[i] = v
            nfls[n] = out
        t, pw, ps, rows = sweep(G, nfls)
        counts.append(ps); tested_counts.append(t)
        r = rows.get(("M288", "N45"))
        if r and r["p"] <= real["p"]:
            hits_m288 += 1
        if (rep + 1) % 10 == 0:
            print(f"  rep {rep+1:4}: passing {ps:4} (running mean "
                  f"{statistics.mean(counts):.1f})", flush=True)

    sc = sorted(counts)
    # The full real sweep is written out because the folder's next experiment is to
    # re-derive the constraint set from it under a pre-registered multiplicity design.
    real_rows = [dict(m_sign=k[0], n_sign=k[1], rank=i, **v)
                 for i, (k, v) in enumerate(ordered, 1)]
    out = {
        "real": {"tested": t0, "with_power": pw0, "passing": ps0,
                 "m288_n45": real, "m288_n45_rank": rank, "rows": real_rows},
        "null_B_reps": reps,
        "null_passing": {"mean": statistics.mean(counts), "median": sc[len(sc)//2],
                         "min": sc[0], "max": sc[-1],
                         "p95": sc[min(len(sc)-1, int(0.95*len(sc)))],
                         "all": counts},
        "null_tested_mean": statistics.mean(tested_counts),
        "reps_with_m288_n45_as_extreme": hits_m288,
    }
    print(f"\nNULL B SWEEP over {reps} replicates:")
    print(f"  pairs passing at 0.05 -- mean {out['null_passing']['mean']:.1f}, "
          f"median {out['null_passing']['median']}, range [{sc[0]}, {sc[-1]}], "
          f"95th pct {out['null_passing']['p95']}")
    print(f"  REAL = {ps0}")
    print(f"  replicates where M288-N45 reached the real p: {hits_m288}/{reps}")
    Path("results").mkdir(exist_ok=True)
    Path("results/competitor_null.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
