#!/usr/bin/env python3
"""Null models for the block-aware split, and one stricter block.

N1  Split invariance. The split is built from block marginals (total, s, t).
    A null that permutes the target WITHIN each (tablet, face) block preserves
    those marginals exactly, so it must leave the split unchanged. If it does,
    the split is selection on an ancillary statistic and cannot disturb the
    conditional test. This checks that claim by brute force rather than asserting it.

N2  Uniformity under the null (prediction P4). With the split fixed, permute the
    target within each validation face-block and re-run the blocked test. The
    p-values should be ~uniform and the fraction <= 0.05 should be ~0.05.

N3  Split-label permutation (prediction P5). The 15 informative tablets could have
    been divided many ways. Sample alternative assignments that also satisfy the
    >= 10 informative-block constraint and report the distribution of the
    validation p-value, with the hash-chosen split marked in it. This is the
    2026-09-23 label-permutation discipline at the same search budget.

N4  A stricter block than face. Face blocking does not control line complexity: a
    line carrying more accounting numerals is more likely to carry any given one.
    Blocking on (tablet, face, number of N-signs on the line) holds that constant
    too. Reported with its p-floor, because the finer block costs power.
"""
from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from face_and_form import eligible, load_lines  # noqa: E402
from block_split import (  # noqa: E402
    MIN_INFORMATIVE_BLOCKS, FACE_KEY, blocked_test, build_split,
    informative_tablets, hash_order,
)

M_SIGN, N_SIGN, DIRECTION = "M288", "N45", "enriched"
COMPLEXITY_KEY = lambda ln: (ln.tablet, ln.surface, len(ln.n_signs))  # noqa: E731


def permute_target_within(lines, n_sign, key, rng):
    """Reassign which lines carry `n_sign`, uniformly within each block.

    Everything else about every line is untouched, so block marginals -- block
    size, sign-line count, target-line count -- are preserved exactly.
    """
    blocks = defaultdict(list)
    for i, ln in enumerate(lines):
        blocks[key(ln)].append(i)
    flags = [n_sign in ln.n_signs for ln in lines]
    out = list(flags)
    for idxs in blocks.values():
        k = sum(flags[i] for i in idxs)
        chosen = set(rng.sample(idxs, k))
        for i in idxs:
            out[i] = i in chosen
    # rebuild n_signs so the existing test code works unchanged
    new = []
    for ln, flag in zip(lines, out):
        ns = set(ln.n_signs)
        if flag:
            ns.add(n_sign)
        else:
            ns.discard(n_sign)
        new.append(ln.__class__(**{**ln.__dict__, "n_signs": frozenset(ns)}))
    return new


def main():
    rng = random.Random(20261001)
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)

    val_tablets, diag = build_split(el, M_SIGN, N_SIGN)
    val = [ln for ln in el if ln.tablet in val_tablets]
    real = blocked_test(val, M_SIGN, N_SIGN, DIRECTION, FACE_KEY)
    print(f"observed validation face-blocked p = {real['p']:.5f} "
          f"(floor {real['p_floor']:.4f}, {real['informative_blocks']} informative blocks)")

    out = {"observed": real, "split": diag}

    # ---- N1 split invariance
    print("\nN1  split invariance under within-face target permutation")
    same = 0
    trials = 60
    for _ in range(trials):
        perm = permute_target_within(el, N_SIGN, FACE_KEY, rng)
        vt, _ = build_split(perm, M_SIGN, N_SIGN)
        same += vt == val_tablets
    print(f"    split identical in {same}/{trials} replicates")
    out["n1_split_invariance"] = {"trials": trials, "identical": same}

    # ---- N2 uniformity (P4)
    print("\nN2  uniformity of the validation p-value under the null  (P4)")
    reps = 500
    ps = []
    for _ in range(reps):
        perm = permute_target_within(el, N_SIGN, FACE_KEY, rng)
        pv = [ln for ln in perm if ln.tablet in val_tablets]
        ps.append(blocked_test(pv, M_SIGN, N_SIGN, DIRECTION, FACE_KEY)["p"])
    frac05 = sum(p <= 0.05 for p in ps) / reps
    at_least = sum(p <= real["p"] for p in ps) / reps
    ps_sorted = sorted(ps)
    print(f"    replicates {reps};  fraction p <= 0.05 = {frac05:.3f}  "
          f"(nominal 0.05)")
    print(f"    fraction p <= observed {real['p']:.5f} = {at_least:.3f}")
    print(f"    null p quartiles: {ps_sorted[reps//4]:.3f} "
          f"{ps_sorted[reps//2]:.3f} {ps_sorted[3*reps//4]:.3f}")
    out["n2_uniformity"] = {
        "replicates": reps, "fraction_le_05": frac05,
        "fraction_le_observed": at_least,
        "quartiles": [ps_sorted[reps // 4], ps_sorted[reps // 2], ps_sorted[3 * reps // 4]],
    }

    # ---- N3 split-label permutation (P5)
    print("\nN3  alternative splits of the informative tablets  (P5)")
    per_tablet = informative_tablets(el, M_SIGN, N_SIGN)
    inf_tabs = sorted(per_tablet)
    other_val = {t for t in val_tablets if t not in per_tablet}
    alt_ps, alt_blocks = [], []
    tries = 0
    while len(alt_ps) < 2000 and tries < 60000:
        tries += 1
        rng.shuffle(inf_tabs)
        chosen, blocks = set(), 0
        for t in inf_tabs:
            if blocks >= MIN_INFORMATIVE_BLOCKS:
                break
            chosen.add(t)
            blocks += per_tablet[t]
        if blocks < MIN_INFORMATIVE_BLOCKS:
            continue
        vt = other_val | chosen
        sub = [ln for ln in el if ln.tablet in vt]
        r = blocked_test(sub, M_SIGN, N_SIGN, DIRECTION, FACE_KEY)
        alt_ps.append(r["p"])
        alt_blocks.append(r["informative_blocks"])
    alt_sorted = sorted(alt_ps)
    n = len(alt_sorted)
    print(f"    {n} alternative splits meeting the >= {MIN_INFORMATIVE_BLOCKS}-block "
          f"constraint")
    print(f"    validation p: min {alt_sorted[0]:.5f}  q1 {alt_sorted[n//4]:.5f}  "
          f"median {alt_sorted[n//2]:.5f}  q3 {alt_sorted[3*n//4]:.5f}  "
          f"max {alt_sorted[-1]:.5f}")
    print(f"    fraction of alternative splits with p <= 0.05: "
          f"{sum(p <= 0.05 for p in alt_ps)/n:.3f}")
    print(f"    hash-chosen split sits at p = {real['p']:.5f}, percentile "
          f"{sum(p <= real['p'] for p in alt_ps)/n*100:.1f}")
    out["n3_alternative_splits"] = {
        "count": n,
        "min": alt_sorted[0], "q1": alt_sorted[n // 4], "median": alt_sorted[n // 2],
        "q3": alt_sorted[3 * n // 4], "max": alt_sorted[-1],
        "fraction_le_05": sum(p <= 0.05 for p in alt_ps) / n,
        "chosen_percentile": sum(p <= real["p"] for p in alt_ps) / n * 100,
        "mean_informative_blocks": sum(alt_blocks) / n,
    }

    # ---- N4 stricter block: face + line numeral count
    print("\nN4  stricter block: (tablet, face, n_sign count on the line)")
    for label, lineset in (("full corpus", el), ("validation only", val)):
        r = blocked_test(lineset, M_SIGN, N_SIGN, DIRECTION, COMPLEXITY_KEY)
        print(f"    {label:16} p {r['p']:.5f}  floor {r['p_floor']:.5f}  "
              f"informative {r['informative_blocks']:3}  "
              f"obs/forced/max {r['observed_overlap']}/{r['forced_overlap']}"
              f"/{r['max_possible_overlap']}  "
              f"power {'YES' if r['has_power_at_05'] else 'NO'}")
        out[f"n4_complexity_block_{label.replace(' ', '_')}"] = r
    # and the same stricter block for the folder's headline pair, for comparison
    for pair in (("M297", "N39B", "enriched"), ("M263", "N01", "enriched")):
        r = blocked_test(el, pair[0], pair[1], pair[2], COMPLEXITY_KEY)
        print(f"    {pair[0]}-{pair[1]:5} full corpus  p {r['p']:.5f}  "
              f"floor {r['p_floor']:.5f}  informative {r['informative_blocks']}")
        out[f"n4_complexity_block_{pair[0]}-{pair[1]}"] = r

    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "nulls.json").write_text(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
