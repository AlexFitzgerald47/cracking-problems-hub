#!/usr/bin/env python3
"""Is the block-aware split a valid procedure, and does prior selection contaminate it?

PREDICTIONS.md P2. Two nulls, both destroying the M288-N45 association while keeping
the corpus otherwise intact.

NULL 1 (within (tablet, face)). Re-draw which lines of each block carry N45, holding
each block's line count and N45 count fixed. This is exactly the null the face-blocked
exact test computes against. Every block marginal is invariant, so the marginal-only
split rule returns the IDENTICAL split in every draw -- which is the whole argument for
why a split chosen on marginals cannot bias the test. The simulation checks the
argument instead of asserting it, and catches bugs in my own pipeline.

NULL 2 (within tablet). Re-draw which lines of each TABLET carry N45, letting N45 move
between faces. This is the looser null that contains the face-confound freedom: face
marginals now change, so the split rule's output changes from draw to draw. If a
block-aware split could manufacture significance out of a face-level skew, it shows up
here.

CONTAMINATION. 7 of the 9 canonical validation tablets sit in the 2026-09-04 training
buckets, so their lines were in-sample for the original candidate selection. The
question is whether conditioning on "an unblocked train screen would have selected this
pair" pushes the face-blocked validation p-value down. Both nulls are therefore reported
unconditionally AND conditional on the selection event.
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (  # noqa: E402
    M, N, canonical_split, face_blocks, fisher_exact_two_sided, load_eligible,
    odds_ratio, tail,
)

WANT = 10
DRAWS = 20000
SEED = 20261003
# BH q <= 0.01 over the ~1,430-candidate screen. A single Bonferroni-style threshold
# is used as the selection proxy; it is STRICTER than BH, so conditioning on it applies
# more selection pressure than the published rule did. That is the conservative
# direction for detecting contamination.
SELECT_P = 0.01 / 1430
SELECT_OR = 3.0


def units(el, key):
    """Group eligible lines into permutation units, recording only what matters:
    the has-M288 flag per line, and the number of N45 lines to re-place."""
    g = defaultdict(list)
    for ln in el:
        g[key(ln)].append(ln)
    out = []
    for k, bl in g.items():
        flags = [M in ln.m_signs for ln in bl]
        t = sum(N in ln.n_signs for ln in bl)
        out.append({"key": k, "flags": flags, "t": t,
                    "tablet": ln.tablet if False else bl[0].tablet,
                    "face": bl[0].surface})
    return out


def redraw(unit, rng):
    """Choose which `t` of the unit's lines carry N45. Returns the chosen indices."""
    n = len(unit["flags"])
    if unit["t"] == 0 or unit["t"] == n:
        return set(range(n)) if unit["t"] == n else set()
    return set(rng.sample(range(n), unit["t"]))


def blocks_from_assignment(face_units, n45_idx):
    """Rebuild (tablet, face) block marginals/overlaps from a simulated assignment."""
    out = []
    for u, chosen in zip(face_units, n45_idx):
        total = len(u["flags"])
        s = sum(u["flags"])
        t = u["t"]
        obs = sum(1 for i in chosen if u["flags"][i])
        lo, hi = max(0, s - (total - t)), min(s, t)
        out.append({"tablet": u["tablet"], "face": u["face"], "total": total,
                    "s": s, "t": t, "obs": obs, "lo": lo, "hi": hi,
                    "informative": hi > lo})
    return out


def train_screen_row(blocks, val_tablets):
    """Unblocked 2x2 for M288-N45 on the complement, from block marginals+overlap."""
    a = b = c = d = 0
    for bk in blocks:
        if bk["tablet"] in val_tablets:
            continue
        a += bk["obs"]
        b += bk["s"] - bk["obs"]
        c += bk["t"] - bk["obs"]
        d += bk["total"] - bk["s"] - bk["t"] + bk["obs"]
    return a, b, c, d


def run_null(el, face_key, label, canonical_val, recompute_split, rng):
    face_units = units(el, lambda ln: (ln.tablet, ln.surface))
    perm_units = units(el, face_key)
    # map each permutation unit's lines onto face-unit slots
    # Build index: for within-tablet permutation a unit spans several faces, so we
    # need, for each permutation unit, the (face_unit_index, within_face_index) of
    # each of its lines, in the same order `units` collected them.
    face_pos = {}
    for fi, u in enumerate(face_units):
        face_pos[u["key"]] = fi
    # recollect line->slot mapping deterministically, same grouping order as units()
    g_face = defaultdict(list)
    for ln in el:
        g_face[(ln.tablet, ln.surface)].append(ln)
    slot = {}
    for k, bl in g_face.items():
        for j, ln in enumerate(bl):
            slot[id(ln)] = (face_pos[k], j)
    g_perm = defaultdict(list)
    for ln in el:
        g_perm[face_key(ln)].append(ln)
    perm_slots = [[slot[id(ln)] for ln in g_perm[u["key"]]] for u in perm_units]

    recs = []
    for _ in range(DRAWS):
        chosen = [set() for _ in face_units]
        for u, slots in zip(perm_units, perm_slots):
            for i in redraw(u, rng):
                fi, j = slots[i]
                chosen[fi].add(j)
        bks = blocks_from_assignment(face_units, chosen)
        if recompute_split:
            vt, got = canonical_split(bks, WANT)
        else:
            vt, got = canonical_val, None
        val_inf = [bk for bk in bks if bk["informative"] and bk["tablet"] in vt]
        p, floor, obs, mx = tail(val_inf)
        a, b, c, d = train_screen_row(bks, vt)
        tp = fisher_exact_two_sided(a, b, c, d)
        tor = odds_ratio(a, b, c, d)
        recs.append({"p": p, "floor": floor, "n_inf": len(val_inf),
                     "val_tablets": tuple(sorted(vt)) if recompute_split else None,
                     "train_p": tp, "train_or": tor,
                     "selected": tp <= SELECT_P and tor >= SELECT_OR})
    return summarise(recs, label, recompute_split)


def summarise(recs, label, recompute_split):
    ps = [r["p"] for r in recs]
    sel = [r for r in recs if r["selected"]]
    sel_ps = [r["p"] for r in sel]
    print("-" * 78)
    print(label)
    print("-" * 78)
    print(f"draws: {len(recs)}")
    if recompute_split:
        distinct = len({r['val_tablets'] for r in recs})
        print(f"distinct splits chosen by the marginal-only rule: {distinct}")
        print(f"validation informative blocks: min {min(r['n_inf'] for r in recs)}, "
              f"max {max(r['n_inf'] for r in recs)}")
    else:
        print(f"split invariant across draws (marginals unchanged by this null): "
              f"{len({r['n_inf'] for r in recs}) == 1}")
    def table(name, vals):
        if not vals:
            print(f"  {name}: no draws")
            return None
        row = {a: sum(v <= a for v in vals) / len(vals)
               for a in (0.001, 0.01, 0.05, 0.10, 0.25, 0.50)}
        print(f"  {name} (n={len(vals)}): median {statistics.median(vals):.4g}")
        print("    " + "  ".join(f"P(p<={a:g})={row[a]:.4f}" for a in
                                 (0.01, 0.05, 0.10, 0.25, 0.50)))
        return row
    unc = table("unconditional", ps)
    con = table("conditional on train selection", sel_ps)
    print(f"  selection rate: {len(sel)}/{len(recs)} = {len(sel)/len(recs):.4f}")
    return {"label": label, "draws": len(recs),
            "median_unconditional": statistics.median(ps),
            "unconditional": unc, "conditional": con,
            "selection_rate": len(sel) / len(recs),
            "n_selected": len(sel),
            "distinct_splits": (len({r['val_tablets'] for r in recs})
                                if recompute_split else 1)}


def main():
    el = load_eligible()
    blocks = face_blocks(el)
    canonical_val, _ = canonical_split(blocks, WANT)
    observed_p = tail([b for b in blocks
                       if b["informative"] and b["tablet"] in canonical_val])[0]
    print("=" * 78)
    print("CALIBRATION OF THE BLOCK-AWARE SPLIT  (PREDICTIONS.md P2)")
    print("=" * 78)
    print(f"observed canonical validation p = {observed_p:.4g}")
    print(f"selection proxy: train Fisher p <= {SELECT_P:.3g} and train OR >= "
          f"{SELECT_OR} (stricter than the published BH rule)")
    print()
    rng = random.Random(SEED)
    r1 = run_null(el, lambda ln: (ln.tablet, ln.surface),
                  "NULL 1 - permute N45 within (tablet, face)  [P2a]",
                  canonical_val, False, rng)
    print()
    rng = random.Random(SEED + 1)
    r2 = run_null(el, lambda ln: ln.tablet,
                  "NULL 2 - permute N45 within tablet, N45 free to cross faces  [P2b]",
                  canonical_val, True, rng)

    out = {"observed_canonical_p": observed_p, "draws": DRAWS,
           "select_p_threshold": SELECT_P, "select_or_threshold": SELECT_OR,
           "null_1_within_face": r1, "null_2_within_tablet": r2}
    Path("results").mkdir(exist_ok=True)
    Path("results/calibration.json").write_text(json.dumps(out, indent=2, default=str))
    print()
    print("wrote results/calibration.json")


if __name__ == "__main__":
    main()
