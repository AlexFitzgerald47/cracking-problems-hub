#!/usr/bin/env python3
"""Direction consistency across the five hash buckets.

A per-bucket p-value is dominated by how much power that bucket happens to have. Whether
the odds ratio still points the way the 2026-09-04 table reported is a much less
power-dependent stability check. Obverse lines only: that is the face where every pair
has support (the corpus is 86.5% obverse).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from face_and_form import CONFIRMED, contingency, eligible, load_lines

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "analysis"))
from structure_associations import odds_ratio  # noqa: E402


def bucket(tablet: str) -> int:
    return int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5


def main():
    lines, _ = load_lines(Path(Path(__file__).with_name("corpus_path.txt").read_text().strip()))
    el = [ln for ln in eligible(lines) if ln.surface in ("obverse", "reverse")]
    out = {}
    print(f"{'pair':14} {'dir':9} " + " ".join(f"{'b'+str(i)+' OR':>9}" for i in range(5)) + "  agree")
    for m, n, d in CONFIRMED:
        ors = []
        for k in range(5):
            sub = [ln for ln in el if bucket(ln.tablet) == k and ln.surface == "obverse"]
            ors.append(odds_ratio(*contingency(sub, m, n)))
        agree = sum((o > 1) if d == "enriched" else (o < 1) for o in ors)
        out[f"{m}-{n}"] = {
            "direction": d,
            "obverse_odds_ratio_by_bucket": ors,
            "buckets_agreeing": agree,
        }
        print(f"{m+'-'+n:14} {d:9} " + " ".join(f"{o:9.2f}" for o in ors) + f"  {agree}/5")
    Path("results").mkdir(exist_ok=True)
    Path("results/direction_consistency.json").write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
