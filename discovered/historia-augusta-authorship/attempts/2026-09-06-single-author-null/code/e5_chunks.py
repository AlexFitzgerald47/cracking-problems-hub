"""E5 -- the two-layer claim on equal-sized samples, with a grouped null.

E4 gave different answers at full length and at equalised length, which means
vita length was doing part of the work. This experiment removes length from
the design entirely: every data point is a 1,000-token block, every vita
contributes all of its blocks, and the null permutes VITAE, not blocks, so
that blocks from the same life stay together and topic correlation inside a
life cannot manufacture significance.

The same procedure is run on:
  Historia Augusta   split at the lacuna (lives 1-21 | 22-30)
  Suetonius          split at the real break in his sources (Julius-Nero |
                     Galba-Domitian), the closest single-author analogue
  Nepos              split at the midpoint of the collection

and repeated across feature-set sizes, because a result that only exists at
one MFW count is not a result.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
SIZE = 1000
N_PERM = 5000
MFW_SIZES = [50, 100, 200, 400]


def blocks(xs, size):
    """All non-overlapping blocks, tagged with their parent text."""
    out, parent, order = [], [], []
    for s in xs:
        for b in stylo.chunk(s, size):
            out.append(dict(tokens=b, n_tokens=size))
            parent.append(s["seg_id"])
            order.append(s["order"])
    return out, np.array(parent), np.array(order)


def grouped_perm(d, parent, order, cut, n_perm, rng):
    """Null: reassign whole texts to the two sides, keeping group sizes.

    Blocks inherit their parent's side, so within-text correlation is present
    in the null exactly as it is in the observation.
    """
    texts = list(dict.fromkeys(parent))
    tord = {t: order[parent == t][0] for t in texts}
    n_a = sum(1 for t in texts if tord[t] <= cut)
    out = np.empty(n_perm)
    for i in range(n_perm):
        p = rng.permutation(texts)
        side = {t: (0 if j < n_a else 1) for j, t in enumerate(p)}
        lab = np.array([side[t] for t in parent])
        out[i] = stylo.group_separation(d, lab)
    return out


def run(name, xs, cut, words, note=""):
    bl, parent, order = blocks(xs, SIZE)
    if len(bl) < 8:
        print("    %-22s too few blocks" % name)
        return
    z = stylo.zscore(stylo.matrix(bl, words))
    d = stylo.delta_matrix(z)
    lab = (order > cut).astype(int)
    obs = stylo.group_separation(d, lab)
    null = grouped_perm(d, parent, order, cut, N_PERM, RNG)
    p = (np.sum(null >= obs) + 1) / (N_PERM + 1)
    print("    %-22s blocks=%3d (%2d|%2d texts)  sep %+.4f  "
          "null %+.3f+/-%.3f  z %+5.2f  p %.4f %s"
          % (name, len(bl), len(set(parent[lab == 0])), len(set(parent[lab == 1])),
             obs, null.mean(), null.std(), stylo.z_against(obs, null), p, note))


def main():
    segs = stylo.load()
    ha = sorted(stylo.by_corpus(segs, "HA"), key=lambda s: s["order"])
    su = sorted(stylo.by_corpus(segs, "SUET"), key=lambda s: s["order"])
    ne = sorted(stylo.by_corpus(segs, "NEPOS"), key=lambda s: s["order"])

    print("E5  pre/post split on %d-token blocks, text-level permutation null"
          % SIZE)
    for n_mfw in MFW_SIZES:
        words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), n_mfw)
        print()
        print("  %d MFW" % n_mfw)
        run("Historia Augusta", ha, 21, words, "<- at the lacuna")
        run("Suetonius", su, 6, words, "<- at Galba")
        run("Nepos", ne, 13, words, "<- at midpoint")

        # Known-positive in the same design and units.
        both = su + ne
        for i, s in enumerate(both):
            s = dict(s)
            s["order"] = 1 if i < len(su) else 99
            both[i] = s
        bl, parent, order = blocks(both, SIZE)
        z = stylo.zscore(stylo.matrix(bl, words))
        d = stylo.delta_matrix(z)
        lab = (order > 50).astype(int)
        obs = stylo.group_separation(d, lab)
        null = grouped_perm(d, parent, order, 50, N_PERM, RNG)
        print("    %-22s blocks=%3d              sep %+.4f  "
              "null %+.3f+/-%.3f  z %+5.2f  p %.4f  <- two real authors"
              % ("Suetonius vs Nepos", len(bl), obs, null.mean(), null.std(),
                 stylo.z_against(obs, null),
                 (np.sum(null >= obs) + 1) / (N_PERM + 1)))


if __name__ == "__main__":
    main()
