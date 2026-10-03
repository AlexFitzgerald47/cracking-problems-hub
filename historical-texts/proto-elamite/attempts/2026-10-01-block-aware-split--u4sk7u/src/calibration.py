#!/usr/bin/env python3
"""Does designing the split around the pair inflate the test?  (Frozen prediction P4.)

The validation set is chosen as "every tablet owning an informative (tablet, face)
block for this pair". That is a post-hoc, pair-specific split, and the folder's
standing instruction is that such a split must carry a permutation null before its
difference is interpreted.

The argument that it is safe: informativeness is a function of the block marginals
(total, sign-lines, target-lines) alone and never of the overlap, and the exact
conditional null holds those marginals fixed. The selected block set is therefore
invariant under the null, so the selection cannot move the null distribution.

This file does not take that on trust. It simulates the WHOLE procedure -- permute
the target within each (tablet, face) block over the entire corpus, re-derive the
informative-block set from the permuted data, re-split, re-test -- and checks three
things: that the split is in fact invariant, that the p-values are uniform, and that
the realised false-positive rate at 0.05 lands in the frozen [0.03, 0.07] band.
"""
import json, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from blocks import (CONFIRMED, block_aware_split, blocked_exact, eligible, face_key,
                    group, load_corpus)

corpus = Path(sys.argv[1])
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
lines, _ = load_corpus(corpus)
el = eligible(lines)
blocks_by_face = group(el, face_key)


class Perm:
    """A line whose target membership has been permuted within its block."""
    __slots__ = ("tablet", "surface", "m_signs", "has_target")

    def __init__(self, ln, has_target):
        self.tablet, self.surface = ln.tablet, ln.surface
        self.m_signs, self.has_target = ln.m_signs, has_target


def permuted_corpus(n_sign, rng):
    out = []
    for bl in blocks_by_face.values():
        flags = [n_sign in ln.n_signs for ln in bl]
        rng.shuffle(flags)
        out.extend(Perm(ln, f) for ln, f in zip(bl, flags))
    return out


def marg(block, m_sign):
    total = len(block)
    s = sum(m_sign in ln.m_signs for ln in block)
    t = sum(ln.has_target for ln in block)
    o = sum(m_sign in ln.m_signs and ln.has_target for ln in block)
    return total, s, t, o


def run(perm, m_sign, direction):
    """Full procedure on permuted data: derive informative blocks, split, test."""
    by_face = {}
    for ln in perm:
        by_face.setdefault((ln.tablet, ln.surface), []).append(ln)
    val_tablets = set()
    for (tab, _surf), bl in by_face.items():
        total, s, t, _ = marg(bl, m_sign)
        if min(s, t) > max(0, s - (total - t)):
            val_tablets.add(tab)
    dist = [1.0]
    observed = 0
    from blocks import hypergeom_probability
    for (tab, _surf), bl in by_face.items():
        if tab not in val_tablets:
            continue
        total, s, t, o = marg(bl, m_sign)
        observed += o
        lo, hi = max(0, s - (total - t)), min(s, t)
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, total)
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    p = sum(dist[observed:]) if direction == "enriched" else sum(dist[: observed + 1])
    return min(1.0, p), val_tablets


out = {"replicates": REPS, "pairs": {}}
for m, n, d in CONFIRMED:
    rng = random.Random(20261001)
    real_split = block_aware_split(el, m, n, face_key)
    ps, split_changed = [], 0
    for _ in range(REPS):
        perm = permuted_corpus(n, rng)
        p, vt = run(perm, m, d)
        ps.append(p)
        split_changed += (vt != real_split)
    ps.sort()
    rate05 = sum(p <= 0.05 for p in ps) / REPS
    rate01 = sum(p <= 0.01 for p in ps) / REPS
    # Kolmogorov-Smirnov against Uniform(0,1). The exact test is conservative on a
    # discrete statistic, so one-sided excess over uniform is what matters.
    ks = max(max(abs((i + 1) / REPS - p), abs(i / REPS - p)) for i, p in enumerate(ps))
    out["pairs"][f"{m}-{n}"] = {
        "split_invariant_under_null": split_changed == 0,
        "replicates_where_split_moved": split_changed,
        "false_positive_rate_at_0.05": rate05,
        "false_positive_rate_at_0.01": rate01,
        "ks_statistic_vs_uniform": ks,
        "median_p": ps[REPS // 2],
    }
    print(f"{m}-{n:6} split invariant: {str(split_changed == 0):5}  "
          f"FPR@.05 = {rate05:.4f}  FPR@.01 = {rate01:.4f}  KS = {ks:.4f}  median p = {ps[REPS//2]:.3f}")

Path("results").mkdir(exist_ok=True)
Path("results/calibration.json").write_text(json.dumps(out, indent=2) + "\n")
r = out["pairs"]["M288-N45"]["false_positive_rate_at_0.05"]
print(f"\nP4 band [0.03, 0.07] for M288-N45: {r:.4f} -> {'HOLDS' if 0.03 <= r <= 0.07 else 'FAILS'}")
