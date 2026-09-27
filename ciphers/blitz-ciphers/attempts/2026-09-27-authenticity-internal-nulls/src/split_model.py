"""Over-splitting noise model.

Pelling states his own error policy explicitly: "I'd rather slightly expand the
alphabet when transcribing than make a wrong assumption that can't easily be
undone" (Cipher Mysteries, 2014-10-24).  That is the structure-DESTROYING
direction: if one glyph is inconsistently written as two codes, every bigram
through it is halved, and bigram repetition falls.  Merging two glyphs into one
code would do the opposite.

Model: choose symbol types, in descending frequency, until the chosen types cover
at least fraction phi of the tokens; relabel each such token independently to one
of `ways` random sub-codes.  Report the bigram-IC z of the result.

This is more realistic than the random-substitution model in noise_model.py and
answers the same question: how much of it is needed to reach the Blitz value?

Usage: python3 src/split_model.py <comparanda_dir>
"""
import sys, os, json
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_canonical
import fastnull

COMP = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHI = [0.0, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0]
WAYS = 2
NPERM = 1500


def oversplit(lines, phi, ways, rng):
    toks = [t for l in lines for t in l]
    n = len(toks)
    order = [s for s, _ in Counter(toks).most_common()]
    chosen, cov = set(), 0
    c = Counter(toks)
    for s in order:
        if cov / n >= phi:
            break
        chosen.add(s); cov += c[s]
    out = []
    for l in lines:
        out.append([f"{t}#{rng.integers(ways)}" if t in chosen else t for t in l])
    return out, cov / n


def blocks(doc, want):
    lines = [l for k in sorted(doc) for l in doc[k]]
    out, cur, m = [], [], 0
    for l in lines:
        cur.append(l); m += len(l)
        if m >= want:
            out.append(cur); cur, m = [], 0
    return out


res = {"phi": PHI, "ways": WAYS, "nperm": NPERM, "curves": {}}
for label, doc in (("copiale", load_canonical(os.path.join(COMP, "copiale"))),
                   ("borg", load_canonical(os.path.join(COMP, "borg")))):
    for want in (470, 629):
        bl = blocks(doc, want)[:40]
        rng = np.random.default_rng(1234)
        row = []
        for phi in PHI:
            zs, cvs, ty = [], [], []
            for i, b in enumerate(bl):
                sb, cov = oversplit(b, phi, WAYS, rng)
                r = fastnull.run(sb, nperm=NPERM, seed=4000 + i)
                zs.append(r["bigram"]["z"]); cvs.append(cov); ty.append(r["n_types"])
            zs.sort()
            row.append(dict(phi=phi, coverage=float(np.mean(cvs)),
                            mean_types=float(np.mean(ty)),
                            median=zs[len(zs) // 2], p05=zs[max(0, int(.05 * len(zs)))],
                            p95=zs[min(len(zs) - 1, int(.95 * len(zs)))]))
        res["curves"][f"{label}@{want}"] = row
        print(f"{label}@{want} (blocks={len(bl)}, {WAYS}-way split)")
        for r in row:
            print(f"   phi={r['phi']:.1f} cov={r['coverage']:.2f} types={r['mean_types']:5.1f} "
                  f"| bigram z p05={r['p05']:+6.2f} med={r['median']:+6.2f} p95={r['p95']:+6.2f}")
        sys.stdout.flush()

print("\nBlitz: p7 (n=470) z=+5.84, 53 types; p7+p8 (n=629) z=+6.81, 56 types; "
      "holdout (n=468) z=+4.94, 47 types")
json.dump(res, open(os.path.join(HERE, "out", "split_model.json"), "w"), indent=1)
print("wrote out/split_model.json")
