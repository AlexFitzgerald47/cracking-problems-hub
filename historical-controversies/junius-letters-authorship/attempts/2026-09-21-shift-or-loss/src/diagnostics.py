#!/usr/bin/env python3
"""Two repairs and one new diagnostic.

REPAIR 1 (B1). FREEZE.md set the "clean candidate" cut at long-s damage <= 4e-4 and named
Wilkes as clean on the manifest's 0.0004. Measured per chunk, Wilkes's political prose sits
almost exactly on that cut, so the prediction's verdict flips with a rounding decision. A
threshold placed on a data value is a bad test. The continuous statistic -- rank correlation
between a candidate's damage rate and its share of the cross-register predictions -- has no
such knife edge and is what B1 should have specified.

REPAIR 2 / NEW (A2). Median pairwise cosine +0.267 is well above random but the centring
built on it failed. The quantity that actually decides whether centring can work is not the
cosine's sign but the SHARED FRACTION of displacement energy: how much of each author's
register displacement lies along the direction common to all of them. Centring can only
remove that part; the rest it leaves behind, while adding the estimation error of the shared
direction. This computes it.
"""
import json, os, sys
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K
sys.path.insert(0, K.PRIOR)
import corpus as C
from shift_or_loss import train_index, attribute

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        for pos, i in enumerate(order):
            r[i] = pos
        return r
    rx, ry = rank(x), rank(y)
    rx = np.array(rx) - np.mean(rx)
    ry = np.array(ry) - np.mean(ry)
    return float(rx @ ry / (np.linalg.norm(rx) * np.linalg.norm(ry)))


def main():
    docs, counts, ranked = K.load_docs()
    Z = K.build_Z(counts, ranked[:K.N_FEATURES])
    out = {}

    # ---------------- REPAIR 1
    trainF = train_index(docs, K.FORMAL)
    testL = [i for i, d in enumerate(docs)
             if d["genre"] in K.LETTERS and d["author"] in trainF
             and d["author"] not in ("Junius", "Philo_Junius")]
    _, preds = attribute(Z, docs, trainF, testL)
    share = Counter(preds)
    rows = []
    for a in sorted(trainF):
        dmg = float(np.mean([C.long_s_rate(docs[i]["text"]) for i in trainF[a]]))
        rows.append((a, dmg, share.get(a, 0) / len(preds), len(trainF[a])))
    rows.sort(key=lambda r: r[1])
    print("B1 repaired: candidate damage rate vs share of the 323 cross-register predictions")
    print(f"{'candidate':<18}{'damage':>10}{'pred share':>12}{'n train':>9}")
    for a, dmg, s, n in rows:
        print(f"{a:<18}{dmg:>10.5f}{s:>12.3f}{n:>9}")
    rho = spearman([r[1] for r in rows], [r[2] for r in rows])
    rho_n = spearman([r[3] for r in rows], [r[2] for r in rows])
    print(f"\n   Spearman(damage, prediction share)     = {rho:+.3f}  (n = 8 candidates)")
    print(f"   Spearman(train size, prediction share) = {rho_n:+.3f}")
    out["B1_repaired"] = dict(rows=[dict(author=a, damage=d, share=s, n=n) for a, d, s, n in rows],
                              spearman_damage=rho, spearman_trainsize=rho_n)

    # ---------------- REPAIR 2 / A2 shared fraction
    both = {}
    for a in set(d["author"] for d in docs):
        if "Junius" in a:
            continue
        L = [i for i, d in enumerate(docs) if d["author"] == a and d["genre"] in K.LETTERS]
        F = [i for i, d in enumerate(docs) if d["author"] == a and d["genre"] in K.FORMAL]
        if len(L) >= 8 and len(F) >= 8:
            both[a] = (L, F)
    disp = {a: Z[F].mean(0) - Z[L].mean(0) for a, (L, F) in both.items()}
    names = sorted(disp)
    D = np.array([disp[a] for a in names])

    # leave-one-out shared direction: the only honest version, since including an author
    # in the mean guarantees his own displacement projects onto it.
    print("\nA2 repaired: how much of each author's register displacement is SHARED?")
    print(f"{'author':<18}{'|d|':>8}{'shared |proj|':>15}{'shared frac':>13}")
    fracs = {}
    for i, a in enumerate(names):
        m = np.delete(D, i, 0).mean(0)
        mh = m / np.linalg.norm(m)
        proj = float(D[i] @ mh)
        f = proj ** 2 / float(D[i] @ D[i])
        fracs[a] = f
        print(f"{a:<18}{np.linalg.norm(D[i]):>8.2f}{proj:>15.2f}{f:>13.3f}")
    med = float(np.median(list(fracs.values())))
    print(f"   median shared fraction = {med:.3f}  -> {100*(1-med):.0f}% of each author's "
          f"register displacement is author-specific")
    # how much of the summed displacement energy the common direction carries
    mh = D.mean(0) / np.linalg.norm(D.mean(0))
    tot = float((D ** 2).sum())
    common = float(((D @ mh) ** 2).sum())
    print(f"   corpus-wide: common direction carries {common/tot:.3f} of total "
          f"displacement energy")
    out["shared_fraction"] = dict(per_author=fracs, median=med,
                                  common_energy_fraction=common / tot)

    # what centring can and cannot remove, stated in the metric that matters
    print("\n   consequence: leave-one-author-out centring can remove at most the shared part.")
    for a in names:
        print(f"      {a:<18} residual after perfect centring = "
              f"{np.sqrt(1-fracs[a])*np.linalg.norm(disp[a]):.2f} of {np.linalg.norm(disp[a]):.2f}")

    json.dump(out, open(os.path.join(RES, "diagnostics.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
