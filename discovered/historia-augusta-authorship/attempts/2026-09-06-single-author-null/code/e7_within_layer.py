"""E7 -- how many layers? Structure inside each side of the lacuna.

E5/E6 establish one boundary. That does not establish that there are exactly
two hands: it establishes that the collection is not homogeneous across the
lacuna. If the later lives are a second author, the two sigla that occupy them
(Pollio and Vopiscus) should not separate from each other; if they do, there
are more than two layers, and the "two-layer" reading is itself too coarse.

Also tested inside the earlier block:
  * the four sigla that share it;
  * the Hauptvita / Nebenvita rubric, which is the main non-authorial
    partition proposed for the collection.

Every test uses the E5 design -- 1,000-token blocks, text-level permutation --
so the numbers are directly comparable to the lacuna split.
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
SIZE = 1000
N_PERM = 5000
MFW_SIZES = [100, 200, 400]


def blocks(xs, size, field="tokens"):
    out, parent, key = [], [], []
    for s in xs:
        tk = s[field]
        for i in range(0, len(tk) - size + 1, size):
            out.append(dict(tokens=tk[i:i + size], n_tokens=size))
            parent.append(s["seg_id"])
            key.append(s["_lab"])
    return out, np.array(parent), np.array(key)


def grouped_perm(d, parent, lab, n_perm, rng):
    texts = list(dict.fromkeys(parent))
    tlab = {t: lab[parent == t][0] for t in texts}
    vals = [tlab[t] for t in texts]
    out = np.empty(n_perm)
    for i in range(n_perm):
        p = rng.permutation(vals)
        side = dict(zip(texts, p))
        out[i] = stylo.group_separation(d, np.array([side[t] for t in parent]))
    return out


def test(label, xs, labeller, words, field="tokens"):
    xs = [dict(s, _lab=labeller(s)) for s in xs]
    xs = [s for s in xs if s["_lab"] is not None]
    if len(set(s["_lab"] for s in xs)) < 2:
        print("    %-38s only one group" % label)
        return
    bl, parent, lab = blocks(xs, SIZE, field)
    if len(bl) < 8:
        print("    %-38s too few blocks (%d)" % (label, len(bl)))
        return
    z = stylo.zscore(stylo.matrix(bl, words))
    d = stylo.delta_matrix(z)
    obs = stylo.group_separation(d, lab)
    null = grouped_perm(d, parent, lab, N_PERM, RNG)
    p = (np.sum(null >= obs) + 1) / (N_PERM + 1)
    counts = "/".join("%s:%d" % (g, int((lab == g).sum()))
                      for g in sorted(set(lab)))
    print("    %-42s %-26s sep %+.4f  z %+5.2f  p %.4f"
          % (label, counts, obs, stylo.z_against(obs, null), p))


def main():
    segs = stylo.load()
    ha = sorted(stylo.by_corpus(segs, "HA"), key=lambda s: s["order"])
    pre = [s for s in ha if s["block"] == "pre"]
    post = [s for s in ha if s["block"] == "post"]

    print("E7  structure inside each side of the lacuna")
    print("    same design as E5: %d-token blocks, text-level permutation null"
          % SIZE)
    for n_mfw in MFW_SIZES:
        words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), n_mfw)
        print()
        print("  %d MFW" % n_mfw)
        print("   later block (lives 22-30):")
        test("Pollio vs Vopiscus", post, lambda s: s["siglum"], words)
        test("Pollio vs Vopiscus, narrative only", post,
             lambda s: s["siglum"], words, "tokens_nq")
        print("   earlier block (lives 1-21):")
        test("four sigla", pre, lambda s: s["siglum"], words)
        test("Spartianus vs Capitolinus", pre,
             lambda s: s["siglum"] if s["siglum"] in
             ("Spartianus", "Capitolinus") else None, words)
        test("Hauptvita vs Nebenvita", pre, lambda s: s["rubric"], words)
        test("Hauptvita vs Nebenvita, narrative only", pre,
             lambda s: s["rubric"], words, "tokens_nq")
        print("   whole collection:")
        test("Hauptvita vs Nebenvita (all 30)", ha,
             lambda s: s["rubric"], words)
        test("Hauptvita vs Nebenvita (all 30), narr.", ha,
             lambda s: s["rubric"], words, "tokens_nq")
        test("lacuna split, for comparison", ha, lambda s: s["block"], words)


if __name__ == "__main__":
    main()
