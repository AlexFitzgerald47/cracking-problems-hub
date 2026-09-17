#!/usr/bin/env python3
"""Rotate the tablet-level holdout across all five hash buckets.

The 2026-09-04 design screens on buckets 1-4 and validates on bucket 0. This re-runs
the face-blocked null on each bucket in turn, for the eight already-selected pairs.

This is a stability and power check, NOT five independent confirmations: the candidate
list was selected using buckets 1-4, so buckets 1-4 are in-sample for selection. What
it does establish is whether the bucket-0 outcome is typical or a draw, and in which
buckets the face-blocked test has any power at all.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from face_and_form import CONFIRMED, eligible, load_lines
from power_floor import floors


def bucket(tablet: str) -> int:
    return int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5


def main():
    lines, _ = load_lines(Path(Path(__file__).with_name("corpus_path.txt").read_text().strip()))
    el = eligible(lines)
    out = {}
    header = f"{'pair':14} " + " ".join(f"{'b'+str(b):>17}" for b in range(5))
    print(header)
    print(f"{'':14} " + " ".join(f"{'p (floor) n':>17}" for _ in range(5)))
    for m, n, d in CONFIRMED:
        row = {}
        cells = []
        for b in range(5):
            sub = [ln for ln in el if bucket(ln.tablet) == b]
            r = floors(sub, m, n, d, lambda ln: (ln.tablet, ln.surface))
            row[f"bucket_{b}"] = r
            mark = "" if r["has_power_at_05"] else "*"
            cells.append(f"{r['p']:.3f}({r['p_floor']:.2f}){mark}{r['informative_blocks']:>3}")
        out[f"{m}-{n}"] = {"direction": d, "buckets": row}
        print(f"{m+'-'+n:14} " + " ".join(f"{c:>17}" for c in cells))
    print()
    print("cells are  p(floor)informative_blocks ;  * = test has no power at 0.05")
    print()
    for pair, v in out.items():
        powered = [b for b in range(5) if v["buckets"][f"bucket_{b}"]["has_power_at_05"]]
        passed = [b for b in powered if v["buckets"][f"bucket_{b}"]["p"] <= 0.05]
        print(f"{pair:14} powered in {len(powered)}/5 buckets {powered}, "
              f"passes in {len(passed)}/{len(powered) if powered else 0} {passed}")
    Path("results").mkdir(exist_ok=True)
    Path("results/rotate_holdout.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
