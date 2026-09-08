"""E3 -- the six sigla: does the collection's own authorship claim show up?

The Historia Augusta names six authors. If those six are real hands, vitae
sharing a siglum should sit closer together than vitae with different sigla.

Reported: the standardised within/between gap for the six sigla, against a
label-permutation null; the same statistic for each siglum on its own; and the
same statistic for a genuine two-author case (Suetonius vs Nepos) measured in
the same units, so the HA number can be read against a known-positive.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
N_MFW = 200
N_PERM = 20000


def main():
    segs = stylo.load()
    ha = stylo.by_corpus(segs, "HA")
    ha.sort(key=lambda s: s["order"])
    words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), N_MFW)

    z = stylo.zscore(stylo.matrix(ha, words))
    d = stylo.delta_matrix(z)
    sigla = np.array([s["siglum"] for s in ha])

    obs = stylo.group_separation(d, sigla)
    null = stylo.perm_null_labels(d, sigla, N_PERM, RNG)
    p = (np.sum(null >= obs) + 1) / (N_PERM + 1)

    print("E3  six-siglum test on the Historia Augusta (%d vitae, %d MFW)"
          % (len(ha), N_MFW))
    print("    sigla: %s" % ", ".join("%s(%d)" % (s, int((sigla == s).sum()))
                                      for s in sorted(set(sigla))))
    print("    separation (between - within, /sd) : %+.4f" % obs)
    print("    permutation null                   : %+.4f +/- %.4f"
          % (null.mean(), null.std()))
    print("    z                                  : %+.2f" % stylo.z_against(obs, null))
    print("    p (one-sided, %d permutations)     : %.4f" % (N_PERM, p))

    print()
    print("    per-siglum (own vitae vs the rest):")
    for s in sorted(set(sigla)):
        if (sigla == s).sum() < 2:
            print("      %-12s n=%d  (single vita, no within-group distance)"
                  % (s, int((sigla == s).sum())))
            continue
        lab = np.where(sigla == s, 1, 0)
        o = stylo.group_separation(d, lab)
        n2 = stylo.perm_null_labels(d, lab, 4000, RNG)
        print("      %-12s n=%2d  sep %+.4f  z %+5.2f  p %.3f"
              % (s, int((sigla == s).sum()), o, stylo.z_against(o, n2),
                 (np.sum(n2 >= o) + 1) / 4001))

    # A known-positive measured the same way: two real authors, same genre.
    su = stylo.by_corpus(segs, "SUET")
    ne = [s for s in stylo.by_corpus(segs, "NEPOS") if s["n_tokens"] >= 700]
    both = su + ne
    z2 = stylo.zscore(stylo.matrix(both, words))
    d2 = stylo.delta_matrix(z2)
    lab2 = np.array(["Suetonius"] * len(su) + ["Nepos"] * len(ne))
    o2 = stylo.group_separation(d2, lab2)
    n3 = stylo.perm_null_labels(d2, lab2, N_PERM, RNG)
    print()
    print("    ruler -- two genuinely different authors, same genre:")
    print("      Suetonius (%d lives) vs Nepos (%d lives): sep %+.4f  z %+.2f  p %.4f"
          % (len(su), len(ne), o2, stylo.z_against(o2, n3),
             (np.sum(n3 >= o2) + 1) / (N_PERM + 1)))
    print("      HA six-siglum separation as a fraction of that: %.1f%%"
          % (100.0 * obs / o2))

    # Same-siglum pairs are also mostly adjacent-in-order pairs. Report how
    # much of any siglum effect is really a neighbourhood effect.
    n = len(ha)
    iu = np.triu_indices(n, 1)
    gap = np.abs(iu[0] - iu[1])
    same = sigla[iu[0]] == sigla[iu[1]]
    print()
    print("    confound check -- distance in the collection's order:")
    print("      mean order-gap, same siglum      : %.1f" % gap[same].mean())
    print("      mean order-gap, different siglum : %.1f" % gap[~same].mean())
    r = np.corrcoef(gap, d[iu])[0, 1]
    print("      corr(order gap, Delta distance)  : %+.3f" % r)


if __name__ == "__main__":
    main()
