#!/usr/bin/env python3
"""The 2026-09-17 handover's item 1, executed as written, and its ceiling.

The instruction: "modify the tablet-level split so that validation is guaranteed >= 10
informative (tablet, face) blocks for the pair under test, re-screen candidates on the
complement, and re-run."

Split rule, fixed before use and using block MARGINALS ONLY -- never an observed
overlap. Informativeness of a (tablet, face) block for a pair is a function of
(line count, sign-line count, target-line count) alone, and the exact conditional test
conditions on exactly those three numbers, so selecting blocks on them does not bias
the conditional p-value. Selecting on observed overlap would, which is why the rule may
not see it.

  1. For each (tablet, face) block compute degrees of freedom d = min(s,t) - max(0, s-(n-t)).
  2. Rank the tablets containing at least one block with d > 0 by their total d
     descending, breaking ties by tablet id ascending.
  3. Walk that ranking, assigning tablets to validation, until validation holds >= 10
     informative blocks. Every remaining tablet goes to training.
  4. Re-screen on training under the published rules (BH q <= 0.01, |OR| >= 3).
  5. Run the face-blocked exact test on validation.

Also reported: the attainable ceiling. Because the test conditions on each block's
marginals, the whole evidence base is the per-block degrees of freedom, and the
smallest p-value the design can ever return is the product of the single most extreme
outcome in each block. That number is a property of the corpus, not of the split.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import (  # noqa: E402
    bh_adjust,
    fisher_exact_two_sided,
    odds_ratio,
)
from weighted_null import load_eligible  # noqa: E402

PAIR = ("M288", "N45", "enriched")
TARGET_BLOCKS = 10


def block_freedom(lines, m_sign, n_sign):
    blocks = defaultdict(list)
    for line in lines:
        blocks[(line.tablet, line.surface)].append(line)
    out = {}
    for key, block in blocks.items():
        n = len(block)
        s = sum(1 for ln in block if m_sign in ln.m_signs)
        t = sum(1 for ln in block if n_sign in ln.n_signs)
        out[key] = {"n": n, "s": s, "t": t,
                    "dof": min(s, t) - max(0, s - (n - t))}
    return out


def face_blocked_p(lines, m_sign, n_sign, direction):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))
    from structure_associations import hypergeom_probability
    blocks = defaultdict(list)
    for line in lines:
        blocks[(line.tablet, line.surface)].append(line)
    distribution = [1.0]
    observed = 0
    informative = 0
    for block in blocks.values():
        n = len(block)
        s = sum(1 for ln in block if m_sign in ln.m_signs)
        t = sum(1 for ln in block if n_sign in ln.n_signs)
        observed += sum(1 for ln in block if m_sign in ln.m_signs and n_sign in ln.n_signs)
        lo, hi = max(0, s - (n - t)), min(s, t)
        if hi > lo:
            informative += 1
        local = [0.0] * (hi + 1)
        for k in range(lo, hi + 1):
            local[k] = hypergeom_probability(k, s, t, n)
        combined = [0.0] * (len(distribution) + len(local) - 1)
        for i, pi in enumerate(distribution):
            if pi:
                for j, pj in enumerate(local):
                    if pj:
                        combined[i + j] += pi * pj
        distribution = combined
    support = [i for i, v in enumerate(distribution) if v > 0]
    if direction == "enriched":
        p = min(1.0, sum(distribution[observed:]))
        floor = min(1.0, sum(distribution[support[-1]:]))
    else:
        p = min(1.0, sum(distribution[: observed + 1]))
        floor = min(1.0, sum(distribution[: support[0] + 1]))
    return {"p": p, "p_floor": floor, "observed_overlap": observed,
            "informative_blocks": informative, "blocks": len(blocks),
            "max_possible_overlap": support[-1]}


def screen(train_lines, m_sign, n_sign):
    """Does the published screening rule still select this pair on the complement?"""
    m_signs = sorted({s for ln in train_lines for s in ln.m_signs})
    n_signs = sorted({s for ln in train_lines for s in ln.n_signs})
    raw = []
    for n_target in n_signs:
        for m_candidate in m_signs:
            a = b = c = d = 0
            for ln in train_lines:
                has_sign = m_candidate in ln.m_signs
                has_target = n_target in ln.n_signs
                if has_sign and has_target:
                    a += 1
                elif has_sign:
                    b += 1
                elif has_target:
                    c += 1
                else:
                    d += 1
            if a + b < 20 or a + c < 20:
                continue
            raw.append({"m": m_candidate, "n": n_target,
                        "or": odds_ratio(a, b, c, d),
                        "p": fisher_exact_two_sided(a, b, c, d),
                        "cells": (a, b, c, d)})
    q_values = bh_adjust([r["p"] for r in raw])
    selected = []
    for row, q in zip(raw, q_values):
        row["q"] = q
        if q <= 0.01 and (row["or"] >= 3.0 or row["or"] <= 1 / 3):
            selected.append(row)
    mine = [r for r in selected if r["m"] == m_sign and r["n"] == n_sign]
    return {"selected_count": len(selected),
            "pair_selected": bool(mine),
            "pair_row": mine[0] if mine else
                        next((r for r in raw if r["m"] == m_sign and r["n"] == n_sign), None)}


def main() -> None:
    m_sign, n_sign, direction = PAIR
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    freedom = block_freedom(lines, m_sign, n_sign)
    informative = {k: v for k, v in freedom.items() if v["dof"] > 0}

    by_tablet = defaultdict(list)
    for (tablet, surface), info in informative.items():
        by_tablet[tablet].append(info["dof"])
    ranking = sorted(by_tablet.items(), key=lambda kv: (-sum(kv[1]), kv[0]))

    validation_tablets: set[str] = set()
    blocks_held = 0
    for tablet, dofs in ranking:
        if blocks_held >= TARGET_BLOCKS:
            break
        validation_tablets.add(tablet)
        blocks_held += len(dofs)

    validation = [ln for ln in lines if ln.tablet in validation_tablets]
    train = [ln for ln in lines if ln.tablet not in validation_tablets]

    result = face_blocked_p(validation, m_sign, n_sign, direction)
    screening = screen(train, m_sign, n_sign)

    # Attainable ceiling of the whole face-blocked design, over the entire corpus.
    ceiling = face_blocked_p(lines, m_sign, n_sign, direction)
    dof_histogram: dict[int, int] = defaultdict(int)
    for info in informative.values():
        dof_histogram[info["dof"]] += 1

    out = {
        "pair": f"{m_sign}-{n_sign}",
        "split_rule": "tablets ranked by total block degrees of freedom, "
                      "marginals only, until validation holds >= 10 informative blocks",
        "validation_tablets": sorted(validation_tablets),
        "validation_lines": len(validation),
        "train_lines": len(train),
        "informative_blocks_corpus": len(informative),
        "dof_histogram": dict(sorted(dof_histogram.items())),
        "validation_test": result,
        "training_screen": {k: v for k, v in screening.items() if k != "pair_row"},
        "training_screen_pair_row": screening["pair_row"],
        "full_corpus_face_blocked_ceiling": ceiling,
    }
    print(json.dumps(out, indent=2, default=str))
    Path("results").mkdir(exist_ok=True)
    Path("results/block_aware_split.json").write_text(
        json.dumps(out, indent=2, default=str) + "\n"
    )


if __name__ == "__main__":
    main()
