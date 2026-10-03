#!/usr/bin/env python3
"""The information budget of a face-blocked test, and the split frontier.

Three questions, all about M288-N45 but all general:

1. DECOMPOSITION. A blocked exact test's attainable evidence is bounded by its
   block marginals alone. For each informative block the best it can contribute is
   P(overlap = hi); the floor of a block set is the product over blocks. This
   decomposes the corpus evidence by block size, which says *what kind of block*
   the result rests on.

2. THE SPLIT FRONTIER. The 2026-09-17 handover asks for a tablet-level split whose
   validation half holds >= 10 informative (tablet, face) blocks for the pair, with
   candidates re-screened on the complement. Only 15 tablets carry an informative
   block at all, so this enumerates every allocation of those tablets and reports
   the achievable (validation blocks, validation floor, train floor) frontier.

3. THE COIN-FLIP BLOCKS. Blocks with total=2, s=1, t=1 contribute exactly a factor
   of 1/2 each under the null. This prints their actual lines so the permutation's
   counterfactual can be inspected against the primary evidence.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import defaultdict
from pathlib import Path

_ATT = Path(__file__).resolve().parents[2] / "2026-09-17-exact-form-and-face"
sys.path.insert(0, str(_ATT))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))

from face_and_form import eligible, load_lines  # noqa: E402
from structure_associations import hypergeom_probability  # noqa: E402

M, N = "M288", "N45"


def blocks_of(lines, m_sign, n_sign):
    """(tablet, face) blocks with their marginals, bounds and member lines."""
    grouped = defaultdict(list)
    for ln in lines:
        grouped[(ln.tablet, ln.surface)].append(ln)
    out = []
    for key, bl in sorted(grouped.items()):
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo, hi = max(0, s - (total - t)), min(s, t)
        out.append({"key": key, "tablet": key[0], "total": total, "s": s, "t": t,
                    "obs": obs, "lo": lo, "hi": hi, "informative": hi > lo,
                    "lines": bl})
    return out


def null_dist(blocks):
    """Exact null distribution of total overlap, by convolution over blocks."""
    dist = [1.0]
    for b in blocks:
        local = [0.0] * (b["hi"] + 1)
        for k in range(b["lo"], b["hi"] + 1):
            local[k] = hypergeom_probability(k, b["s"], b["t"], b["total"])
        comb = [0.0] * (len(dist) + len(local) - 1)
        for i, pi in enumerate(dist):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        comb[i + j] += pi * pj
        dist = comb
    return dist


def upper_tail(blocks):
    """(p at observed, p at maximum = the floor, observed, max)."""
    if not blocks:
        return 1.0, 1.0, 0, 0
    dist = null_dist(blocks)
    obs = sum(b["obs"] for b in blocks)
    mx = sum(b["hi"] for b in blocks)
    return min(1.0, sum(dist[obs:])), min(1.0, sum(dist[mx:])), obs, mx


def main():
    corpus = Path((_ATT / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)
    allb = blocks_of(el, M, N)
    inf = [b for b in allb if b["informative"]]

    report = {"pair": f"{M}-{N}", "eligible_lines": len(el),
              "blocks_total": len(allb), "blocks_informative": len(inf)}

    # ---- 1. decomposition by block size -------------------------------------
    print("=" * 74)
    print("1. WHERE THE EVIDENCE COMES FROM  (decomposition by block size)")
    print("=" * 74)
    p_all, floor_all, obs_all, max_all = upper_tail(inf)
    print(f"all 16 informative blocks: p={p_all:.3e}  floor={floor_all:.3e}  "
          f"overlap {obs_all}/{max_all}")
    strata = {}
    for label, sel in (("total==2 (coin-flip faces)", [b for b in inf if b["total"] == 2]),
                       ("total>=3", [b for b in inf if b["total"] >= 3]),
                       ("total>=4", [b for b in inf if b["total"] >= 4]),
                       ("total>=5", [b for b in inf if b["total"] >= 5])):
        p, fl, o, mx = upper_tail(sel)
        strata[label] = {"n_blocks": len(sel), "p": p, "p_floor": fl,
                         "observed": o, "max": mx}
        print(f"  {label:28} n={len(sel):2}  p={p:.4g}  floor={fl:.3g}  "
              f"overlap {o}/{mx}")
    report["decomposition"] = strata

    # ---- 3. the coin-flip blocks, as primary evidence -----------------------
    print()
    print("=" * 74)
    print("3. THE total=2 BLOCKS: the lines the null says N45 could have moved to")
    print("=" * 74)
    coin = [b for b in inf if b["total"] == 2]
    coin_dump = []
    for b in coin:
        tab, fc = b["key"]
        print(f"\n-- {tab} {fc}   s={b['s']} t={b['t']} obs={b['obs']}")
        entry = {"tablet": tab, "face": fc, "obs": b["obs"], "lines": []}
        for ln in b["lines"]:
            tag = []
            if M in ln.m_signs:
                tag.append(M)
            if N in ln.n_signs:
                tag.append(N)
            mark = ("[" + "+".join(tag) + "]") if tag else "[ - ]"
            print(f"   {mark:14} {ln.label:5} {ln.text}")
            print(f"   {'':14} {'':5} N-signs: {sorted(ln.n_signs)}")
            entry["lines"].append({"label": ln.label, "text": ln.text,
                                   "m_signs": sorted(ln.m_signs),
                                   "n_signs": sorted(ln.n_signs),
                                   "has_m": M in ln.m_signs,
                                   "has_n": N in ln.n_signs})
        coin_dump.append(entry)
    report["coin_flip_blocks"] = coin_dump

    # ---- 2. the split frontier ----------------------------------------------
    print()
    print("=" * 74)
    print("2. THE SPLIT FRONTIER: can any tablet-level split give validation >=10?")
    print("=" * 74)
    inf_tablets = sorted({b["tablet"] for b in inf})
    print(f"tablets carrying >=1 informative block: {len(inf_tablets)}")
    by_tab = defaultdict(list)
    for b in inf:
        by_tab[b["tablet"]].append(b)
    for t in inf_tablets:
        print(f"   {t}: {len(by_tab[t])} informative block(s)")

    # Exhaustive over all 2^15 allocations of the informative-block tablets.
    best = {}
    for r in range(len(inf_tablets) + 1):
        for combo in itertools.combinations(inf_tablets, r):
            val_blocks = [b for t in combo for b in by_tab[t]]
            k = len(val_blocks)
            _, vfloor, _, _ = upper_tail(val_blocks)
            train_blocks = [b for b in inf if b["tablet"] not in combo]
            _, tfloor, _, _ = upper_tail(train_blocks)
            cur = best.get(k)
            # Best split at each validation-block count = lowest validation floor;
            # ties broken by the lowest training floor (most screening power left).
            if cur is None or (vfloor, tfloor) < (cur["val_floor"], cur["train_floor"]):
                best[k] = {"n_val_blocks": k, "val_floor": vfloor,
                           "train_floor": tfloor, "n_val_tablets": len(combo),
                           "val_tablets": list(combo),
                           "n_train_informative_blocks": len(train_blocks)}
    print()
    print(f"{'valBlk':>6} {'valFloor':>11} {'trainInfBlk':>12} {'trainFloor':>11}  "
          f"val can fire at .05")
    for k in sorted(best):
        r = best[k]
        print(f"{k:6} {r['val_floor']:11.4g} {r['n_train_informative_blocks']:12} "
              f"{r['train_floor']:11.4g}  {'YES' if r['val_floor'] <= 0.05 else 'no'}")
    report["split_frontier"] = [best[k] for k in sorted(best)]

    Path("results").mkdir(exist_ok=True)
    Path("results/budget.json").write_text(json.dumps(report, indent=2, default=str))
    print("\nwrote results/budget.json")


if __name__ == "__main__":
    main()
