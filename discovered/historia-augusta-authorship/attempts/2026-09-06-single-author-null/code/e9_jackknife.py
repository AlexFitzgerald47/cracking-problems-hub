"""E9 -- is the seam really at Alexander Severus, or is #18 noise?

E8 puts the strongest boundary after vita #18 (Alexander Severus) rather than
after #21 (the manuscript lacuna). Adjacent cuts are highly correlated and the
profile is a plateau, so the peak's location needs a stability test before it
can be reported as a finding.

Leave-one-vita-out: drop each of the 30 lives in turn, re-run the whole scan,
and record where the maximum lands. A peak that moves freely across the
collection when one life is removed is not a located boundary.
"""

import numpy as np

import stylo

SIZE = 1000
N_PERM = 300
N_MFW = 200


def prep(xs, words, field):
    """Blocks, their parent text index, and the vectorised distance matrix."""
    bl, parent = [], []
    for s in xs:
        tk = s[field]
        for i in range(0, len(tk) - SIZE + 1, SIZE):
            bl.append(dict(tokens=tk[i:i + SIZE], n_tokens=SIZE))
            parent.append(s["seg_id"])
    texts = list(dict.fromkeys(parent))
    tidx = {t: i for i, t in enumerate(texts)}
    pidx = np.array([tidx[p] for p in parent])
    z = stylo.zscore(stylo.matrix(bl, words))
    d = stylo.delta_matrix(z)
    iu = np.triu_indices(len(bl), 1)
    return d[iu], pidx[iu[0]], pidx[iu[1]], len(texts)


def sep(vals, ti, tj, side):
    same = side[ti] == side[tj]
    if same.all() or (~same).all():
        return np.nan
    s = vals.std()
    return (vals[~same].mean() - vals[same].mean()) / s if s else np.nan


def scan(xs, words, field, rng):
    vals, ti, tj, n_t = prep(xs, words, field)
    orders = np.array([s["order"] for s in xs])
    best_z, best_cut = -np.inf, None
    prof = []
    for k in range(3, n_t - 2):
        side = np.array([0] * k + [1] * (n_t - k))
        obs = sep(vals, ti, tj, side)
        null = np.empty(N_PERM)
        for i in range(N_PERM):
            null[i] = sep(vals, ti, tj, rng.permutation(side))
        z = (obs - null.mean()) / null.std()
        prof.append((orders[k - 1], z))
        if z > best_z:
            best_z, best_cut = z, orders[k - 1]
    return best_cut, best_z, prof


def main():
    segs = stylo.load()
    words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), N_MFW)
    ha = sorted(stylo.by_corpus(segs, "HA"), key=lambda s: s["order"])
    names = {s["order"]: s["seg_id"][3:] for s in ha}

    print("E9  leave-one-vita-out stability of the boundary location")
    print("    (cut number = order of the LAST life on the earlier side)")
    print()
    for field, lbl in (("tokens", "all text"), ("tokens_nq", "narrative only")):
        rng = np.random.default_rng(20260906)
        full_cut, full_z, _ = scan(ha, words, field, rng)
        peaks = []
        for drop in range(len(ha)):
            sub = [s for i, s in enumerate(ha) if i != drop]
            c, z, _ = scan(sub, words, field, rng)
            peaks.append(c)
        peaks = np.array(peaks)
        print("  %s: full-data peak after #%d (z %+.2f)" % (lbl, full_cut, full_z))
        vals, cnt = np.unique(peaks, return_counts=True)
        for v, n in sorted(zip(vals, cnt), key=lambda x: -x[1]):
            print("    peak after #%-2d %-26s %2d/30 leave-one-out runs"
                  % (v, names.get(int(v), "?"), n))
        print("    peak at or before #21 (the lacuna): %d/30" % (peaks <= 21).sum())
        print("    peak at or before #18: %d/30" % (peaks <= 18).sum())
        print()


if __name__ == "__main__":
    main()
