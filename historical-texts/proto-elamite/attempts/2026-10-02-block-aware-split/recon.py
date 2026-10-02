"""Marginal-only reconnaissance for the M288-N45 block-aware split.

Touches ONLY block marginals (lines per block, M288-line count, N45-line count).
The observed overlap is never read. The face-blocked exact test conditions on exactly
these marginals, so designing a split from them cannot bias the null.
"""
import sys, hashlib
from pathlib import Path
from collections import defaultdict
HERE = Path("/home/user/cracking-problems-hub/historical-texts/proto-elamite/attempts/2026-09-17-exact-form-and-face")
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis"))
from face_and_form import eligible, load_lines
from structure_associations import hypergeom_probability, split_name

corpus = Path(sys.argv[1])
lines, _ = load_lines(corpus)
el = eligible(lines)
M, N = "M288", "N45"

blocks = defaultdict(list)
for ln in el:
    blocks[(ln.tablet, ln.surface)].append(ln)

rows = []
for (tab, face), bl in blocks.items():
    total = len(bl)
    s = sum(M in ln.m_signs for ln in bl)
    t = sum(N in ln.n_signs for ln in bl)
    lo = max(0, s - (total - t)); hi = min(s, t)
    if hi > lo:
        # probability of achieving the maximum overlap, marginal-only
        pmax = hypergeom_probability(hi, s, t, total)
        rows.append((tab, face, total, s, t, lo, hi, pmax))

print(f"eligible lines {len(el)}, blocks {len(blocks)}")
print(f"informative (tablet,face) blocks for {M}-{N}: {len(rows)}")
print(f"{'tablet':10} {'face':8} {'n':>4} {'nM':>4} {'nN':>4} {'lo':>3} {'hi':>3} {'P(max)':>9} {'bucket':>6}")
tot_hi = 0
for tab, face, total, s, t, lo, hi, pmax in sorted(rows):
    b = int(hashlib.sha256(tab.encode('ascii')).hexdigest()[:8],16)%5
    tot_hi += hi
    print(f"{tab:10} {face:8} {total:4} {s:4} {t:4} {lo:3} {hi:3} {pmax:9.5f} {b:6}")
print(f"\nsum of max-possible overlap across informative blocks: {tot_hi}")
# corpus-wide marginal totals for screening feasibility
print(f"\n{M} eligible lines corpus-wide: {sum(M in ln.m_signs for ln in el)}")
print(f"{N} eligible lines corpus-wide: {sum(N in ln.n_signs for ln in el)}")
tabs = sorted({ln.tablet for ln in el})
print(f"tablets with eligible lines: {len(tabs)}")
print(f"tablets carrying an informative block: {len({r[0] for r in rows})}")
