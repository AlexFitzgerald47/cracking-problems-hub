#!/usr/bin/env python3
"""A hard bound on how much of the observed overlap the face confound can touch.

The within-tablet permutation can move a target between faces only inside a tablet
that (a) has freedom at all (0 < target count < line count) and (b) actually has
eligible lines on more than one face. Overlap contributed by any other tablet is
beyond the reach of a face confound of *any* strength, because there is no cross-face
move available to it.

This is a bound from the block marginals and the face layout, not a simulation.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))

from structure_associations import split_name  # noqa: E402
from weighted_null import load_eligible  # noqa: E402

from test_weighted_null import CONFIRMED  # noqa: E402


def bound(lines, m_sign, n_sign):
    blocks = defaultdict(list)
    for line in lines:
        blocks[line.tablet].append(line)
    exposed = reachable = total = 0
    exposed_tablets = free_tablets = 0
    for block in blocks.values():
        overlap = sum(1 for ln in block if m_sign in ln.m_signs and n_sign in ln.n_signs)
        total += overlap
        target_count = sum(1 for ln in block if n_sign in ln.n_signs)
        has_freedom = 0 < target_count < len(block)
        multi_face = len({ln.surface for ln in block}) > 1
        if has_freedom:
            free_tablets += 1
            reachable += overlap
        if has_freedom and multi_face:
            exposed_tablets += 1
            exposed += overlap
    return {
        "observed_overlap": total,
        "overlap_in_tablets_with_any_freedom": reachable,
        "overlap_in_tablets_where_face_can_act": exposed,
        "overlap_beyond_reach_of_any_face_confound": total - exposed,
        "tablets_with_freedom": free_tablets,
        "tablets_where_face_can_act": exposed_tablets,
        "face_exposed_fraction": exposed / total if total else float("nan"),
    }


def main() -> None:
    corpus = Path(Path(__file__).with_name("corpus_path.txt").read_text().strip())
    lines = load_eligible(corpus)
    holdout = [ln for ln in lines if split_name(ln.tablet) == "validation"]
    out = {}
    print(f"{'pair':12} {'scope':8} {'obs':>4} {'free':>5} {'faceable':>9} "
          f"{'unreachable':>12} {'tabl_free':>9} {'tabl_face':>9}")
    for m_sign, n_sign, _ in CONFIRMED:
        for label, scope in (("holdout", holdout), ("corpus", lines)):
            row = bound(scope, m_sign, n_sign)
            out[f"{m_sign}-{n_sign}/{label}"] = row
            print(f"{m_sign+'-'+n_sign:12} {label:8} {row['observed_overlap']:4} "
                  f"{row['overlap_in_tablets_with_any_freedom']:5} "
                  f"{row['overlap_in_tablets_where_face_can_act']:9} "
                  f"{row['overlap_beyond_reach_of_any_face_confound']:12} "
                  f"{row['tablets_with_freedom']:9} {row['tablets_where_face_can_act']:9}")
        print()
    Path("results").mkdir(exist_ok=True)
    Path("results/channel_bound.json").write_text(json.dumps(out, indent=2) + "\n")


if __name__ == "__main__":
    main()
