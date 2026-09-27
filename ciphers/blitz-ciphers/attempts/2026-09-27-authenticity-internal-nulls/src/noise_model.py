"""How much transcription noise would it take to turn a genuine cipher page into
the Blitz result?

PRACTICES: noise degrades order and cannot create it, so structure surviving a bad
transcription is a lower bound.  The corollary needed here is the other direction:
the Blitz bigram-structure deficit is only evidence about the document if it cannot
be produced by a plausible transcription error rate acting on a genuine text.

Noise model: independently, with probability eps, replace a token by a token drawn
from the block's own unigram distribution.  This is the mildest realistic model -
it preserves the unigram distribution in expectation (so the shuffle null is
unchanged) and destroys only adjacency, which is exactly the quantity under test.

Usage: python3 src/noise_model.py <comparanda_dir>
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_canonical
import fastnull

COMP = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NPERM = 1500
EPS = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60]
TARGETS = {"blitz_p7 (n=470)": 5.84, "blitz_p7+p8 (n=629)": 6.81,
           "holdout (n=468)": 4.94}


def corrupt(lines, eps, rng):
    pool = [t for l in lines for t in l]
    out = []
    for l in lines:
        m = list(l)
        for i in range(len(m)):
            if rng.random() < eps:
                m[i] = pool[rng.integers(len(pool))]
        out.append(m)
    return out


def blocks(doc, want):
    lines = [l for k in sorted(doc) for l in doc[k]]
    out, cur, n = [], [], 0
    for l in lines:
        cur.append(l); n += len(l)
        if n >= want:
            out.append(cur); cur, n = [], 0
    return out


res = {"eps": EPS, "nperm": NPERM, "curves": {}}
for label, doc in (("copiale", load_canonical(os.path.join(COMP, "copiale"))),
                   ("borg", load_canonical(os.path.join(COMP, "borg")))):
    for want in (470, 629):
        bl = blocks(doc, want)[:40]
        rng = np.random.default_rng(99)
        row = []
        for eps in EPS:
            zs = [fastnull.run(corrupt(b, eps, rng), nperm=NPERM, seed=3000 + i)["bigram"]["z"]
                  for i, b in enumerate(bl)]
            zs.sort()
            row.append(dict(eps=eps, median=zs[len(zs) // 2], p05=zs[max(0, int(.05 * len(zs)))],
                            p95=zs[min(len(zs) - 1, int(.95 * len(zs)))]))
        key = f"{label}@{want}"
        res["curves"][key] = row
        print(f"{key}  (n blocks={len(bl)})")
        for r in row:
            print(f"   eps={r['eps']:.2f}  bigram z: p05={r['p05']:+6.2f} "
                  f"med={r['median']:+6.2f} p95={r['p95']:+6.2f}")
        sys.stdout.flush()

print("\nBlitz observed values for comparison:")
for k, v in TARGETS.items():
    print(f"   {k}: z = {v:+.2f}")
json.dump(res, open(os.path.join(HERE, "out", "noise_model.json"), "w"), indent=1)
print("\nwrote out/noise_model.json")
