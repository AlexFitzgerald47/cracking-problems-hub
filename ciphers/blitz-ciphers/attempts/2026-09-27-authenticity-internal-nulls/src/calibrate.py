"""Length-matched calibration for Tests 2 and 3.

A z-score from a shuffle null grows with text length, so "Blitz p7 has bigram-IC
z = +5.8" is uninterpretable on its own.  This builds the reference distribution
of the same z at the same token counts, by cutting Copiale and Borg into
non-overlapping contiguous line-blocks of the target size and running the
identical null on each.

Also answers FREEZE prediction 2b (power): what fraction of genuine blocks of
Blitz length still reach p < 0.05?

Usage: python3 src/calibrate.py <comparanda_dir> [nperm]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_canonical
import fastnull

COMP = sys.argv[1]
NPERM = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIZES = [159, 470, 629]


def blocks(doc, want):
    """Non-overlapping contiguous whole-line blocks of >= want tokens, taken
    across the concatenated document stream (line structure preserved)."""
    lines = [l for k in sorted(doc) for l in doc[k]]
    out, cur, n = [], [], 0
    for l in lines:
        cur.append(l); n += len(l)
        if n >= want:
            out.append(cur); cur, n = [], 0
    return out


def pct(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(p * len(v)))]


res = {"nperm": NPERM, "sizes": SIZES, "ref": {}}
for label, doc in (("copiale", load_canonical(os.path.join(COMP, "copiale"))),
                   ("borg", load_canonical(os.path.join(COMP, "borg")))):
    for want in SIZES:
        bl = blocks(doc, want)
        bz, dz, bp, dp, ns = [], [], [], [], []
        for i, b in enumerate(bl):
            r = fastnull.run(b, nperm=NPERM, seed=1000 + i)
            bz.append(r["bigram"]["z"]); dz.append(r["doublet"]["z"])
            bp.append(r["bigram"]["p_upper"]); dp.append(r["doublet"]["p_lower"])
            ns.append(r["n_tokens"])
        key = f"{label}@{want}"
        res["ref"][key] = dict(
            n_blocks=len(bl), median_tokens=sorted(ns)[len(ns) // 2],
            bigram_z=bz, doublet_z=dz,
            bigram_p05_rate=sum(1 for p in bp if p < 0.05) / len(bp),
            doublet_p05_rate=sum(1 for p in dp if p < 0.05) / len(dp))
        print(f"{key:14s} blocks={len(bl):4d} medn={res['ref'][key]['median_tokens']:4d} | "
              f"bigram z p05={pct(bz,.05):+6.2f} med={pct(bz,.5):+6.2f} p95={pct(bz,.95):+6.2f} "
              f"| power(p<.05)={res['ref'][key]['bigram_p05_rate']:.3f} "
              f"|| doublet z p05={pct(dz,.05):+6.2f} med={pct(dz,.5):+6.2f} "
              f"p95={pct(dz,.95):+6.2f} | deficit-rate={res['ref'][key]['doublet_p05_rate']:.3f}")
        sys.stdout.flush()

json.dump(res, open(os.path.join(HERE, "out", "calibration.json"), "w"), indent=1)
print("\nwrote out/calibration.json")
