#!/usr/bin/env python3
"""Marginal survey of (tablet, face) blocks, for designing a block-aware split.

Reads ONLY block marginals -- how many lines a face has, how many carry the
M-sign, how many carry the target N-sign. It never reads the within-block
overlap, which is the quantity the validation test is about. That separation is
what lets the split be designed before the test is run.

A block is `informative` for a pair when the exact blocked test has any freedom
inside it: hi = min(s, t) strictly exceeds lo = max(0, s - (total - t)). Both
hi and lo are functions of the marginals alone.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "analysis"))
sys.path.insert(0, str(_HERE.parents[1] / "attempts" / "2026-09-17-exact-form-and-face"))

from face_and_form import CONFIRMED, eligible, load_lines  # noqa: E402


def block_marginals(lines, m_sign, n_sign):
    """Per-(tablet, face) marginals only. Returns list of dicts, no overlaps."""
    blocks = defaultdict(list)
    for ln in lines:
        blocks[(ln.tablet, ln.surface)].append(ln)
    out = []
    for (tablet, face), bl in sorted(blocks.items()):
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        lo = max(0, s - (total - t))
        hi = min(s, t)
        out.append(
            {
                "tablet": tablet,
                "face": face,
                "total": total,
                "sign_lines": s,
                "target_lines": t,
                "lo": lo,
                "hi": hi,
                "informative": hi > lo,
                "freedom": hi - lo,
            }
        )
    return out


def main():
    corpus = Path((_HERE / "corpus_path.txt").read_text().strip())
    lines, files = load_lines(corpus)
    el = eligible(lines)
    print(f"eligible lines {len(el)}  tablets {len({l.tablet for l in el})}  "
          f"faces {len({(l.tablet, l.surface) for l in el})}")
    summary = {}
    for m, n, d in CONFIRMED:
        bm = block_marginals(el, m, n)
        inf = [b for b in bm if b["informative"]]
        tabs = sorted({b["tablet"] for b in inf})
        summary[f"{m}-{n}"] = {
            "direction": d,
            "informative_blocks": len(inf),
            "informative_tablets": tabs,
            "max_possible_overlap": sum(b["hi"] for b in bm),
            "forced_overlap": sum(b["lo"] for b in bm),
            "blocks": inf,
        }
        print(f"{m}-{n:6} informative blocks {len(inf):3}  on {len(tabs):3} tablets  "
              f"forced {sum(b['lo'] for b in bm):3} .. max {sum(b['hi'] for b in bm):3}")
    (_HERE / "results").mkdir(exist_ok=True)
    (_HERE / "results" / "marginal_survey.json").write_text(json.dumps(summary, indent=2))
    print()
    print("M288-N45 informative blocks (marginals only):")
    for b in summary["M288-N45"]["blocks"]:
        print(f"  {b['tablet']} {b['face']:8} lines {b['total']:3} "
              f"M288 {b['sign_lines']:2} N45 {b['target_lines']:2} "
              f"freedom {b['lo']}..{b['hi']}")


if __name__ == "__main__":
    main()
