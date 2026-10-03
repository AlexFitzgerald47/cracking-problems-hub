#!/usr/bin/env python3
"""Diagnostic: the (tablet, face) block structure of a pair across the whole corpus.

An exact conditional test blocked on (tablet, face) can only produce evidence from
blocks where the overlap has freedom to vary. For block with `total` lines, `s`
sign-bearing lines and `t` target-bearing lines, the overlap is confined to
[max(0, s-(total-t)), min(s, t)]. The block is INFORMATIVE iff that interval has
width > 0. Those bounds are functions of the block marginals alone.
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

_ATT = Path(__file__).resolve().parents[2] / "2026-09-17-exact-form-and-face"
sys.path.insert(0, str(_ATT))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "analysis"))

from face_and_form import eligible, load_lines  # noqa: E402
from structure_associations import split_name  # noqa: E402


def block_margins(lines, m_sign, n_sign, block_key):
    """Per-block marginals and the overlap bounds they permit."""
    blocks = defaultdict(list)
    for ln in lines:
        blocks[block_key(ln)].append(ln)
    out = []
    for key, bl in blocks.items():
        total = len(bl)
        s = sum(m_sign in ln.m_signs for ln in bl)
        t = sum(n_sign in ln.n_signs for ln in bl)
        obs = sum(m_sign in ln.m_signs and n_sign in ln.n_signs for ln in bl)
        lo = max(0, s - (total - t))
        hi = min(s, t)
        out.append({"key": key, "total": total, "s": s, "t": t, "obs": obs,
                    "lo": lo, "hi": hi, "informative": hi > lo})
    return out


def main():
    corpus = Path((_ATT / "corpus_path.txt").read_text().strip())
    lines, _ = load_lines(corpus)
    el = eligible(lines)
    m, n = "M288", "N45"
    face = lambda ln: (ln.tablet, ln.surface)

    rows = block_margins(el, m, n, face)
    inf = [r for r in rows if r["informative"]]
    print(f"corpus eligible lines: {len(el)}")
    print(f"(tablet,face) blocks total: {len(rows)}   informative for {m}-{n}: {len(inf)}")
    print()
    print(f"{'tablet':10} {'face':9} {'bkt':4} {'tot':>4} {'s':>3} {'t':>3} {'obs':>4} {'lo':>3} {'hi':>3}")
    for r in sorted(inf, key=lambda r: r["key"]):
        tab, fc = r["key"]
        bkt = "VAL" if split_name(tab) == "validation" else "trn"
        print(f"{tab:10} {fc:9} {bkt:4} {r['total']:4} {r['s']:3} {r['t']:3} "
              f"{r['obs']:4} {r['lo']:3} {r['hi']:3}")
    print()
    # How many distinct tablets carry informative blocks, and how are they
    # distributed over the 5 hash buckets the published split uses?
    tabs = sorted({r["key"][0] for r in inf})
    print(f"distinct tablets carrying an informative block: {len(tabs)}")
    import hashlib
    bybkt = defaultdict(list)
    for t in tabs:
        b = int(hashlib.sha256(t.encode('ascii')).hexdigest()[:8], 16) % 5
        bybkt[b].append(t)
    for b in range(5):
        print(f"  hash bucket {b}: {len(bybkt[b])} tablets  {bybkt[b]}")
    print()
    print(f"total observed overlap over informative blocks: "
          f"{sum(r['obs'] for r in inf)} / max {sum(r['hi'] for r in inf)}")


if __name__ == "__main__":
    main()
