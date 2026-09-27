#!/usr/bin/env python3
"""T17: do a diagram's nymph labels share vocabulary with that diagram's OWN circular
ring text, more than with the other eleven diagrams' ring text?

If the ring text is a caption naming the same items the labels name, the labels of
diagram i should sit closer to the ring text of diagram i than to any other. This is a
crib-free internal cross-reference test with an exact permutation null over the twelve
diagram assignments (12! is too many; 200,000 random assignments are used).
"""
import sys, os, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L, simlib
from t6_regime import ORDER, SIGN

NPERM = 200000


def main():
    rows = L.load()
    z = L.ring_strings(rows)
    lab = {f: [w for (ff, r), v in z.items() if ff == f for w in v] for f in ORDER}
    ring = {}
    for r in rows:
        if r["folio"] in ORDER and r["ltype"] == "R":
            ring.setdefault(r["folio"], []).extend(r["words"])

    # score(i,j) = mean over labels of diagram i of the best similarity to any ring-text
    # word of diagram j
    S = {}
    for i in ORDER:
        for j in ORDER:
            rj = ring[j]
            S[(i, j)] = sum(max(simlib.sim_lev(a, b) for b in rj) for a in lab[i]) / len(lab[i])

    print("mean best-match similarity, labels of ROW vs ring text of COLUMN")
    print("          " + " ".join(f"{SIGN[ORDER.index(j)][:5]:>5s}" for j in ORDER))
    for i in ORDER:
        row = " ".join(f"{S[(i,j)]:5.3f}" for j in ORDER)
        print(f"{SIGN[ORDER.index(i)][:9]:9s} {row}   self={S[(i,i)]:.3f} "
              f"rank={sorted(ORDER, key=lambda j:-S[(i,j)]).index(i)+1}/12")

    diag = sum(S[(f, f)] for f in ORDER) / 12
    off = sum(S[(i, j)] for i in ORDER for j in ORDER if i != j) / (12 * 11)
    print(f"\nmean self  = {diag:.4f}")
    print(f"mean other = {off:.4f}")

    rng = random.Random(77)
    perm = list(ORDER)
    cnt = 0
    for _ in range(NPERM):
        rng.shuffle(perm)
        d = sum(S[(i, p)] for i, p in zip(ORDER, perm)) / 12
        if d >= diag - 1e-12:
            cnt += 1
    p = (cnt + 1) / (NPERM + 1)
    print(f"permutation p (random label->ring-text assignment) = {p:.5f}")

    # exact-type overlap version
    print("\nexact type overlap (a label string occurring verbatim in ring text):")
    selfhit = sum(sum(1 for a in lab[f] if a in set(ring[f])) for f in ORDER)
    tot = sum(len(lab[f]) for f in ORDER)
    otherhit = sum(sum(1 for a in lab[i] if a in set(ring[j]))
                   for i in ORDER for j in ORDER if i != j) / 11
    print(f"  own diagram   : {selfhit}/{tot} = {selfhit/tot:.4f}")
    print(f"  other diagrams: {otherhit:.1f}/{tot} = {otherhit/tot:.4f}")

    json.dump({"self": diag, "other": off, "p": p,
               "matrix": {f"{i}|{j}": S[(i, j)] for i in ORDER for j in ORDER}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                'results', 't17_labeltext.json'), 'w'), indent=1)


if __name__ == "__main__":
    main()
