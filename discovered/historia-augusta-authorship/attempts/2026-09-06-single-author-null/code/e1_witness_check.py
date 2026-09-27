"""E1 -- input validation: are the features stable across two digitisations?

The Perseus HA is an OCR of Magie's Loeb text; the Latin Library HA is an
independently keyed text of unstated edition. If the same vita in the two
witnesses is as far apart in feature space as two different vitae are, then
nothing measured downstream is a property of the text.

Reported: cross-witness distance for the same vita, against the distribution
of distances between different vitae inside a single witness.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
N_MFW = 200


def main():
    segs = stylo.load()
    ha = stylo.by_corpus(segs, "HA")
    ll = {s["seg_id"].split(":", 1)[1]: s for s in stylo.by_corpus(segs, "HA_LL")}

    # Alexander Severus is truncated in the Latin Library (3 of 68 chapters);
    # it is excluded from this comparison and reported as a known defect.
    keys = [s["seg_id"].split(":", 1)[1] for s in ha]
    trunc = [k for k in keys
             if ll[k]["n_tokens"] < 0.5 * next(s for s in ha
                                               if s["seg_id"].endswith(":" + k))["n_tokens"]]
    use = [k for k in keys if k not in trunc]

    ref = stylo.by_corpus(segs, "CTRL")
    words = stylo.mfw_list([s for s in ref if s["author"] not in ("Nepos",)], N_MFW)

    a = [next(s for s in ha if s["seg_id"] == "HA:" + k) for k in use]
    b = [ll[k] for k in use]

    ma, mb = stylo.matrix(a, words), stylo.matrix(b, words)
    # One shared standardisation, so the two witnesses live in the same space.
    both = np.vstack([ma, mb])
    mu, sd = both.mean(axis=0), both.std(axis=0)
    za, zb = stylo.zscore(ma, mu, sd), stylo.zscore(mb, mu, sd)

    same = np.abs(za - zb).mean(axis=1)
    dwithin = stylo.delta_matrix(za)
    iu = np.triu_indices(len(use), 1)
    diff = dwithin[iu]

    print("E1  cross-witness stability of the %d-MFW profile" % N_MFW)
    print("    vitae compared              : %d (excluded as truncated: %s)"
          % (len(use), ", ".join(trunc) or "none"))
    print("    same vita, two witnesses    : mean Delta %.3f  (max %.3f, %s)"
          % (same.mean(), same.max(), use[int(np.argmax(same))]))
    print("    different vitae, one witness: mean Delta %.3f  (5th pct %.3f)"
          % (diff.mean(), np.percentile(diff, 5)))
    print("    separation ratio            : %.2fx" % (diff.mean() / same.mean()))
    n_overlap = int((same[:, None] > diff[None, :]).sum())
    print("    same-vita pairs further apart than a different-vita pair: "
          "%d of %d comparisons (%.1f%%)"
          % (n_overlap, same.size * diff.size,
             100.0 * n_overlap / (same.size * diff.size)))

    worst = np.argsort(-same)[:5]
    print("    least stable vitae          : %s"
          % ", ".join("%s %.2f" % (use[i], same[i]) for i in worst))

    # Token-count agreement is a crude but independent check on completeness.
    ratio = np.array([b[i]["n_tokens"] / a[i]["n_tokens"] for i in range(len(use))])
    print("    token-count ratio LL/Perseus: median %.3f, range %.3f-%.3f"
          % (np.median(ratio), ratio.min(), ratio.max()))
    odd = [use[i] for i in range(len(use)) if not 0.85 < ratio[i] < 1.15]
    print("    vitae differing >15%% in length: %s" % (", ".join(odd) or "none"))


if __name__ == "__main__":
    main()
