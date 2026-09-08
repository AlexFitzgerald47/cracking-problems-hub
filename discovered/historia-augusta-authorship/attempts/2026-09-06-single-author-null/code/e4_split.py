"""E4 -- the two-layer claim, against a matched single-author null.

The strongest computational result on the Historia Augusta (Stover &
Kestemont, BICS 59.2, 2016) reports not six hands but two authorial layers,
corresponding roughly to the Hauptviten and the later lives, with the
discontinuity falling near the great lacuna.

A collection read in order will always have *some* best cut. The question this
experiment asks is whether the Historia Augusta's best cut is larger than the
best cut found by the identical procedure inside a collection of lives that is
certainly by one author.

Nulls:
  order-permutation  -- shuffle the texts and re-run the search. Answers "is
                        there sequential structure at all?"
  Suetonius, Nepos   -- single authors, same genre, ordered collections, run
                        through the same statistic. Answers "is the Historia
                        Augusta's structure larger than what one hand
                        produces?"

Both a full-length and a length-equalised variant are reported, because
frequency estimates from long texts are less noisy than from short ones and
the Historia Augusta's long vitae are not evenly spread across the order.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
N_MFW = 200
N_PERM = 4000
EQ = 1000  # tokens per text in the length-equalised variant


def ordered(segs, corpus):
    xs = stylo.by_corpus(segs, corpus)
    xs.sort(key=lambda s: s["order"])
    return xs


def truncate(xs, size):
    out = []
    for s in xs:
        if s["n_tokens"] < size:
            continue
        t = dict(s)
        t["tokens"] = s["tokens"][:size]
        t["n_tokens"] = size
        out.append(t)
    return out


def analyse(name, xs, words, note=""):
    z = stylo.zscore(stylo.matrix(xs, words))
    d = stylo.delta_matrix(z)
    obs, k = stylo.best_contiguous_split(d)
    null = stylo.perm_null_split(d, N_PERM, RNG)
    p = (np.sum(null >= obs) + 1) / (N_PERM + 1)
    print("    %-26s n=%2d  best split after #%-2d  S=%+.3f  "
          "null %+.3f+/-%.3f  z=%+5.2f  p=%.4f %s"
          % (name, len(xs), k, obs, null.mean(), null.std(),
             stylo.z_against(obs, null), p, note))
    return dict(name=name, n=len(xs), k=k, S=obs,
                z=stylo.z_against(obs, null), p=p, d=d, xs=xs)


def main():
    segs = stylo.load()
    words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), N_MFW)

    ha = ordered(segs, "HA")
    su = ordered(segs, "SUET")
    ne = ordered(segs, "NEPOS")

    print("E4  best contiguous split in an ordered collection of lives")
    print("    features: %d MFW; null: %d random reorderings" % (N_MFW, N_PERM))
    print()
    print("  full length")
    r_ha = analyse("Historia Augusta", ha, words,
                   "<- lacuna falls after #21")
    analyse("Suetonius (one author)", su, words)
    analyse("Nepos (one author)", ne, words)

    print()
    print("  length-equalised at %d tokens per life" % EQ)
    r_ha_eq = analyse("Historia Augusta", truncate(ha, EQ), words,
                      "<- lacuna falls after #21")
    analyse("Suetonius (one author)", truncate(su, EQ), words)
    analyse("Nepos (one author)", truncate(ne, EQ), words)

    # The specific split the two-layer hypothesis predicts.
    print()
    print("  the lacuna split specifically (HA #1-21 vs #22-30), full length")
    d = r_ha["d"]
    lab = np.array([0] * 21 + [1] * 9)
    o = stylo.group_separation(d, lab)
    n2 = stylo.perm_null_labels(d, lab, 20000, RNG)
    print("    separation %+.4f  z %+.2f  p %.4f"
          % (o, stylo.z_against(o, n2), (np.sum(n2 >= o) + 1) / 20001))
    print("    (for scale, two real authors of the same genre, Suetonius vs")
    print("     Nepos, score +1.253 on this statistic -- see E3)")

    print()
    print("  separation profile across every candidate cut (HA, full length):")
    for k in range(3, 28):
        lab = np.array([0] * k + [1] * (30 - k))
        s = stylo.group_separation(d, lab)
        bar = "#" * max(0, int(round(s * 40)))
        mark = "  <- lacuna" if k == 21 else ""
        print("    after #%-2d %+.3f %s%s" % (k, s, bar, mark))


if __name__ == "__main__":
    main()
