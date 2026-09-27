"""Test 1 of FREEZE.md (EXPLORATORY): do Blitz pages 7 and 8 share a symbol
distribution, measured against length-matched between-page and within-page
reference distributions from Copiale and Borg?

Statistic: two-sample chi-square homogeneity, standardised by a pooled-permutation
null at the observed sizes (470, 159).  Every genuine reference pair uses exactly
the same sizes, so the z-scores are directly comparable.

Usage: python3 src/test1_homogeneity.py <comparanda_dir> [nperm]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_blitz, load_canonical, flat, homogeneity_z, contiguous_block

COMP = sys.argv[1]
NPERM = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NA, NB = 470, 159

blitz = load_blitz(os.path.join(HERE, "data"))
a, b = flat(blitz["p7"]), flat(blitz["p8"])
assert (len(a), len(b)) == (NA, NB), (len(a), len(b))

res = {"sizes": [NA, NB], "nperm": NPERM}
bl = homogeneity_z(a, b, NPERM, seed=1)
res["blitz"] = bl
print(f"BLITZ p7 vs p8: chi2={bl['obs']:.1f} null_mean={bl['mean']:.1f} "
      f"sd={bl['sd']:.1f}  z={bl['z']:+.2f}  p={bl['p_upper']:.5f}")


def refs(label, doc):
    keys = sorted(doc)
    between, within = [], []
    for i in range(len(keys) - 1):
        x = contiguous_block(doc[keys[i]], NA)
        y = contiguous_block(doc[keys[i + 1]], NB)
        if x and y:
            between.append((keys[i], keys[i + 1],
                            homogeneity_z(x, y, NPERM, seed=100 + i)["z"]))
    # within: 470 then the next 159 tokens of the same continuous page stream
    for i, k in enumerate(keys):
        toks = flat(doc[k])
        if len(toks) >= NA + NB:
            within.append((k, homogeneity_z(toks[:NA], toks[NA:NA + NB],
                                            NPERM, seed=500 + i)["z"]))
    return between, within


summary = {}
for label, doc in (("copiale", load_canonical(os.path.join(COMP, "copiale"))),
                   ("borg", load_canonical(os.path.join(COMP, "borg")))):
    btw, wth = refs(label, doc)
    bz = sorted(z for _, _, z in btw)
    wz = sorted(z for _, z in wth)

    def q(v, p):
        return v[min(len(v) - 1, int(p * len(v)))] if v else None
    summary[label] = dict(
        n_between=len(bz), between_min=bz[0] if bz else None,
        between_med=q(bz, .5), between_p95=q(bz, .95), between_max=bz[-1] if bz else None,
        n_within=len(wz), within_med=q(wz, .5), within_p95=q(wz, .95),
        within_max=wz[-1] if wz else None,
        n_between_ge_blitz=sum(1 for z in bz if z >= bl["z"]),
        n_within_ge_blitz=sum(1 for z in wz if z >= bl["z"]),
        between_z=bz, within_z=wz)
    s = summary[label]
    print(f"\n{label}: between-page pairs n={s['n_between']}  "
          f"z min={s['between_min']:+.2f} med={s['between_med']:+.2f} "
          f"p95={s['between_p95']:+.2f} max={s['between_max']:+.2f}")
    print(f"{label}: within-page  splits n={s['n_within']}  "
          f"z med={s['within_med']:+.2f} p95={s['within_p95']:+.2f} "
          f"max={s['within_max']:+.2f}")
    print(f"{label}: genuine pairs at or above Blitz z: "
          f"between {s['n_between_ge_blitz']}/{s['n_between']}, "
          f"within {s['n_within_ge_blitz']}/{s['n_within']}")

res["reference"] = summary
json.dump(res, open(os.path.join(HERE, "out", "test1_homogeneity.json"), "w"), indent=1)
print("\nwrote out/test1_homogeneity.json")
