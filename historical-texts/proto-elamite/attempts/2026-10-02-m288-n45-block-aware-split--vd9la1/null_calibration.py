#!/usr/bin/env python3
"""Does the informativeness-based split inflate the face-blocked test's size?

This is prediction P2 in PREDICTIONS.md and the check that can sink the session. The
block-aware split chooses its test set by reading block marginals. The validity claim is
that marginals are ancillary to the conditional null, so such a rule cannot shift the
null. That is an argument; this measures it.

Two permutation nulls, both destroying any M/N association while preserving stated
structure, each run through the *same* split-and-test code as the real analysis:

  NULL A -- permute the N-sign indicator WITHIN each (tablet, face) block.
      Preserves every block marginal exactly, so informativeness is preserved exactly.
      This is the test's own null, so the p-value must come out ~Uniform(0,1). It is an
      implementation check: if size is not ~5% here, the code is wrong, not the design.

  NULL B -- permute the N-sign indicator WITHIN face strata across the whole corpus
      (obverse among obverse, reverse among reverse, ...). Preserves the N-sign's total
      count and its obverse/reverse skew -- the actual confound, N45 being the most
      reverse-skewed N-sign in the top-15 vocabulary -- while destroying its tablet and
      face clustering. Marginals are therefore RE-DRAWN every replicate, so the
      informativeness selection is genuinely exercised. This is the real test of P2.

Usage:  python3 null_calibration.py [reps] [/path/to/corpus]
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

from common import load_eligible
from structure_associations import hypergeom_probability

PAIR = ("M288", "N45", "enriched")
ALPHA = 0.05


def pack(lines, m_sign, n_sign):
    """Flatten the corpus into integer-indexed arrays once, so a replicate is cheap.

    Pure Python by design: the 2026-09-04 pipeline takes no third-party dependency and
    this attempt keeps that property, so any successor can run it on a bare interpreter.
    """
    m = [m_sign in ln.m_signs for ln in lines]
    n = [n_sign in ln.n_signs for ln in lines]
    block_ids, btab, bidx = {}, [], []
    for ln in lines:
        key = (ln.tablet, ln.surface)
        if key not in block_ids:
            block_ids[key] = len(block_ids)
            btab.append(ln.tablet)
        bidx.append(block_ids[key])
    tab_ids = {}
    for ln in lines:
        tab_ids.setdefault(ln.tablet, len(tab_ids))
    btab_idx = [tab_ids[t] for t in btab]
    # line indices grouped by block, and by face stratum, for the two permutations
    block_members = [[] for _ in range(len(block_ids))]
    for i, b in enumerate(bidx):
        block_members[b].append(i)
    strata = defaultdict(list)
    for i, ln in enumerate(lines):
        strata[ln.surface].append(i)
    return dict(m=m, n=n, bidx=bidx, btab_idx=btab_idx,
                block_members=block_members, strata=dict(strata),
                n_blocks=len(block_ids), n_tablets=len(tab_ids), n_lines=len(lines))


def face_blocked_p(P, n_flags, direction=PAIR[2]):
    """Split by informativeness on marginals, then the exact face-blocked p-value.

    Identical arithmetic to block_aware_split.floor_and_p; written against the packed
    arrays so a replicate costs a few milliseconds.
    """
    nb = P["n_blocks"]
    m = P["m"]
    total = [0] * nb
    s = [0] * nb
    t = [0] * nb
    obs = [0] * nb
    for i, b in enumerate(P["bidx"]):
        total[b] += 1
        if m[i]:
            s[b] += 1
            if n_flags[i]:
                obs[b] += 1
        if n_flags[i]:
            t[b] += 1
    lo = [max(0, s[b] - (total[b] - t[b])) for b in range(nb)]
    hi = [min(s[b], t[b]) for b in range(nb)]
    informative = [hi[b] > lo[b] for b in range(nb)]
    # --- the split rule: validation = tablets contributing >=1 informative block ---
    val_tabs = [False] * P["n_tablets"]
    for b in range(nb):
        if informative[b]:
            val_tabs[P["btab_idx"][b]] = True
    keep = [b for b in range(nb) if val_tabs[P["btab_idx"][b]]]
    if not keep:
        return None
    dist = [1.0]
    for b in keep:
        local = [0.0] * (hi[b] + 1)
        for v in range(lo[b], hi[b] + 1):
            local[v] = hypergeom_probability(v, s[b], t[b], total[b])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    o = sum(obs[b] for b in keep)
    mx = sum(hi[b] for b in keep)
    mn = sum(lo[b] for b in keep)
    n_inf = sum(informative)
    if direction == "enriched":
        return dict(p=min(1.0, sum(dist[o:])), p_floor=min(1.0, sum(dist[mx:])),
                    informative_blocks=n_inf, obs=o, mx=mx, val_blocks=len(keep))
    return dict(p=min(1.0, sum(dist[: o + 1])), p_floor=min(1.0, sum(dist[: mn + 1])),
                informative_blocks=n_inf, obs=o, mx=mx, val_blocks=len(keep))


def _shuffle_groups(flags, groups, rng):
    out = list(flags)
    for idx in groups:
        if len(idx) > 1:
            vals = [out[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                out[i] = v
    return out


def permute_within_blocks(P, rng):
    """NULL A: preserves every (tablet, face) marginal exactly."""
    return _shuffle_groups(P["n"], P["block_members"], rng)


def permute_within_strata(P, rng):
    """NULL B: preserves the N-sign's total count and its obverse/reverse skew only."""
    return _shuffle_groups(P["n"], list(P["strata"].values()), rng)


def main() -> None:
    reps = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    argv = ["x"] + ([sys.argv[2]] if len(sys.argv) > 2 else [])
    lines = load_eligible(argv)
    m, n, direction = PAIR
    P = pack(lines, m, n)

    real = face_blocked_p(P, P["n"])
    print(f"REAL {m}-{n}: p = {real['p']:.4e}  floor = {real['p_floor']:.3e}  "
          f"obs {real['obs']}/{real['mx']}  informative blocks {real['informative_blocks']}")
    print()

    rng = random.Random(20261002)
    out = {"pair": f"{m}-{n}", "direction": direction, "reps": reps, "real": real}
    for name, fn in (("null_A_within_block", permute_within_blocks),
                     ("null_B_within_face_strata", permute_within_strata)):
        ps, floors, infb, powered_hits = [], [], [], 0
        for _ in range(reps):
            r = face_blocked_p(P, fn(P, rng), direction)
            if r is None:
                continue
            ps.append(r["p"]); floors.append(r["p_floor"]); infb.append(r["informative_blocks"])
            if r["p_floor"] <= ALPHA and r["p"] <= ALPHA:
                powered_hits += 1
        size_all = sum(p <= ALPHA for p in ps) / len(ps)
        pw = [p for p, f in zip(ps, floors) if f <= ALPHA]
        size_powered = (sum(p <= ALPHA for p in pw) / len(pw)) if pw else float("nan")
        as_extreme = sum(p <= real["p"] for p in ps) / len(ps)
        sp = sorted(ps)
        quant = lambda q: sp[min(len(sp) - 1, int(q * len(sp)))]
        rec = {
            "n_valid_reps": len(ps),
            "size_at_0.05_all_reps": size_all,
            "size_at_0.05_among_powered": size_powered,
            "frac_reps_with_power": len(pw) / len(ps),
            "p_quantiles": {q: quant(q) for q in (0.05, 0.25, 0.5, 0.75, 0.95)},
            "mean_informative_blocks": statistics.mean(infb),
            "frac_reps_p_le_real": as_extreme,
            "procedure_hits_at_0.05": powered_hits / len(ps),
        }
        out[name] = rec
        print(f"{name}")
        print(f"  valid reps                     {rec['n_valid_reps']}")
        print(f"  mean informative blocks        {rec['mean_informative_blocks']:.1f}  (real {real['informative_blocks']})")
        print(f"  reps with power at 0.05        {rec['frac_reps_with_power']:.3f}")
        print(f"  SIZE at 0.05 (all reps)        {size_all:.4f}")
        print(f"  SIZE at 0.05 (powered reps)    {size_powered:.4f}")
        print(f"  p median / quartiles           {rec['p_quantiles'][0.5]:.3f}  "
              f"[{rec['p_quantiles'][0.25]:.3f}, {rec['p_quantiles'][0.75]:.3f}]")
        print(f"  frac reps with p <= real p     {as_extreme:.5f}")
        print()
    Path("results").mkdir(exist_ok=True)
    Path("results/null_calibration.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
