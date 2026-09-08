"""E8 -- where exactly is the seam, and can the scan find a seam it is given?

E5-E7 test one hypothesised cut. This scans every cut point in the collection
with the same block-level statistic, so the boundary is located from the text
rather than assumed from the manuscript lacuna.

A positive control runs first: a synthetic collection whose first half is
Suetonius and whose second half is Nepos, in that order. If the scan cannot
recover a boundary it was handed, its verdict on the Historia Augusta is
worthless.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
SIZE = 1000
N_PERM = 2000
N_MFW = 200


def blocks(xs, size, field="tokens"):
    out, parent, order = [], [], []
    for s in xs:
        tk = s[field]
        for i in range(0, len(tk) - size + 1, size):
            out.append(dict(tokens=tk[i:i + size], n_tokens=size))
            parent.append(s["seg_id"])
            order.append(s["order"])
    return out, np.array(parent), np.array(order)


def scan(xs, words, field="tokens", label=""):
    bl, parent, order = blocks(xs, SIZE, field)
    z = stylo.zscore(stylo.matrix(bl, words))
    d = stylo.delta_matrix(z)
    texts = list(dict.fromkeys(parent))
    tord = np.array([order[parent == t][0] for t in texts])
    cuts, seps, zs = [], [], []
    for c in sorted(set(tord))[:-1]:
        n_a = int((tord <= c).sum())
        if n_a < 3 or len(texts) - n_a < 3:
            continue
        lab = (order > c).astype(int)
        obs = stylo.group_separation(d, lab)
        null = np.empty(N_PERM)
        for i in range(N_PERM):
            p = RNG.permutation(texts)
            side = {t: (0 if j < n_a else 1) for j, t in enumerate(p)}
            null[i] = stylo.group_separation(
                d, np.array([side[t] for t in parent]))
        cuts.append(int(c))
        seps.append(obs)
        zs.append(stylo.z_against(obs, null))
    return np.array(cuts), np.array(seps), np.array(zs)


def show(title, cuts, seps, zs, mark=None, names=None):
    print("  %s" % title)
    best = int(np.argmax(zs))
    for i, c in enumerate(cuts):
        bar = "#" * max(0, int(round(zs[i] * 6)))
        tag = ""
        if mark is not None and c == mark:
            tag += "  <- hypothesised boundary"
        if i == best:
            tag += "  <- strongest"
        nm = (" %-26s" % names[c]) if names else ""
        print("    after #%-2d%s sep %+.3f  z %+5.2f  %s%s"
              % (c, nm, seps[i], zs[i], bar, tag))
    print("    strongest cut: after #%d (z %+.2f)" % (cuts[best], zs[best]))
    print()


def main():
    segs = stylo.load()
    words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), N_MFW)
    print("E8  cut-point scan, %d-token blocks, %d MFW, %d permutations/cut"
          % (SIZE, N_MFW, N_PERM))
    print()

    # Positive control: a seam we planted ourselves.
    su = sorted(stylo.by_corpus(segs, "SUET"), key=lambda s: s["order"])
    ne = [s for s in sorted(stylo.by_corpus(segs, "NEPOS"),
                            key=lambda s: s["order"]) if s["n_tokens"] >= 1000]
    synth = ([dict(s, order=i + 1) for i, s in enumerate(su)] +
             [dict(s, order=len(su) + i + 1) for i, s in enumerate(ne)])
    c, sp, zz = scan(synth, words)
    show("positive control: Suetonius (#1-12) then Nepos (#13-%d)" % len(synth),
         c, sp, zz, mark=len(su))

    ha = sorted(stylo.by_corpus(segs, "HA"), key=lambda s: s["order"])
    names = {s["order"]: s["seg_id"][3:] for s in ha}
    c, sp, zz = scan(ha, words, "tokens")
    show("Historia Augusta, all text", c, sp, zz, mark=21, names=names)

    c, sp, zz = scan(ha, words, "tokens_nq")
    show("Historia Augusta, narrative only (<q> cut)", c, sp, zz, mark=21,
         names=names)


if __name__ == "__main__":
    main()
