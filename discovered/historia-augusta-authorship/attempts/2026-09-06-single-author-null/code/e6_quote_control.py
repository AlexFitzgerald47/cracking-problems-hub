"""E6 -- is the two-layer break a change of hand, or a change of register?

The post-lacuna lives are 24.0% quoted material (forged letters, senatorial
acclamations, speeches) against 10.5% before the lacuna. Quotation is a
different register, so a stylometric break at the lacuna may be measuring how
much of the text is in someone else's assumed voice rather than whose hand
wrote the narrative.

The Perseus/Loeb encoding marks quoted material with <q>. This experiment
repeats E5 on the narrative only, with every <q> removed, and additionally
tests the quote-density covariate directly:

  1. the lacuna split on narrative-only text;
  2. the same split with vitae matched on quote density, so the two sides
     have comparable quotation rates;
  3. whether quote density alone predicts the pre/post label, i.e. whether a
     one-number covariate reproduces the "authorial layer".
"""

import numpy as np

import stylo

RNG = np.random.default_rng(20260906)
SIZE = 1000
N_PERM = 5000
MFW_SIZES = [100, 200, 400]


def blocks(xs, size, field):
    out, parent, order = [], [], []
    for s in xs:
        tk = s[field]
        for i in range(0, len(tk) - size + 1, size):
            out.append(dict(tokens=tk[i:i + size], n_tokens=size))
            parent.append(s["seg_id"])
            order.append(s["order"])
    return out, np.array(parent), np.array(order)


def grouped_perm(d, parent, order, cut, n_perm, rng):
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


def run(label, xs, cut, words, field):
    bl, parent, order = blocks(xs, SIZE, field)
    if len(bl) < 8:
        print("    %-30s too few blocks" % label)
        return None
    z = stylo.zscore(stylo.matrix(bl, words))
    d = stylo.delta_matrix(z)
    lab = (order > cut).astype(int)
    if len(set(lab)) < 2:
        return None
    obs = stylo.group_separation(d, lab)
    null = grouped_perm(d, parent, order, cut, N_PERM, RNG)
    p = (np.sum(null >= obs) + 1) / (N_PERM + 1)
    print("    %-30s blocks=%3d  sep %+.4f  z %+5.2f  p %.4f"
          % (label, len(bl), obs, stylo.z_against(obs, null), p))
    return obs


def qdens(s):
    return 1.0 - len(s["tokens_nq"]) / s["n_tokens"]


def main():
    segs = stylo.load()
    ha = sorted(stylo.by_corpus(segs, "HA"), key=lambda s: s["order"])
    su = sorted(stylo.by_corpus(segs, "SUET"), key=lambda s: s["order"])

    print("E6  narrative-only replication of the lacuna split")
    print("    quoted share: HA pre-lacuna %.3f, post-lacuna %.3f"
          % (1 - sum(len(s["tokens_nq"]) for s in ha if s["block"] == "pre")
             / sum(s["n_tokens"] for s in ha if s["block"] == "pre"),
             1 - sum(len(s["tokens_nq"]) for s in ha if s["block"] == "post")
             / sum(s["n_tokens"] for s in ha if s["block"] == "post")))

    for n_mfw in MFW_SIZES:
        words = stylo.mfw_list(stylo.by_corpus(segs, "CTRL"), n_mfw)
        print()
        print("  %d MFW" % n_mfw)
        run("HA, all text", ha, 21, words, "tokens")
        run("HA, narrative only (<q> cut)", ha, 21, words, "tokens_nq")
        run("Suetonius, narrative only", su, 6, words, "tokens_nq")

        # Quote-density-matched subset: keep only vitae whose quote density
        # falls in the range shared by both sides of the lacuna.
        qs = {s["seg_id"]: qdens(s) for s in ha}
        pre = [s for s in ha if s["block"] == "pre"]
        post = [s for s in ha if s["block"] == "post"]
        lo = max(min(qs[s["seg_id"]] for s in pre),
                 min(qs[s["seg_id"]] for s in post))
        hi = min(max(qs[s["seg_id"]] for s in pre),
                 max(qs[s["seg_id"]] for s in post))
        matched = [s for s in ha if lo <= qs[s["seg_id"]] <= hi]
        run("HA, quote-density-matched (%d/%d)" % (len(matched), len(ha)),
            matched, 21, words, "tokens")

    # Can a single covariate stand in for the "authorial layer"?
    print()
    q = np.array([qdens(s) for s in ha])
    lab = np.array([1 if s["block"] == "post" else 0 for s in ha])
    print("  quote density as a one-number predictor of the pre/post label")
    print("    mean quote density  pre %.3f   post %.3f" % (q[lab == 0].mean(),
                                                            q[lab == 1].mean()))
    order = np.argsort(-q)
    top = lab[order[:lab.sum()]]
    print("    the %d most-quoting vitae contain %d of the %d post-lacuna lives"
          % (lab.sum(), int(top.sum()), int(lab.sum())))
    # Rank-sum test of the covariate itself.
    ranks = np.argsort(np.argsort(q)) + 1
    u = ranks[lab == 1].sum()
    null = np.array([np.random.default_rng(i).permutation(ranks)[:lab.sum()].sum()
                     for i in range(4000)])
    print("    rank-sum of post-lacuna vitae: %d  (permutation p %.4f)"
          % (u, (np.sum(null >= u) + 1) / 4001))

    lens = np.array([s["n_tokens"] for s in ha])
    print("    corr(quote density, vita length): %+.3f" % np.corrcoef(q, lens)[0, 1])
    print("    mean vita length  pre %d   post %d"
          % (lens[lab == 0].mean(), lens[lab == 1].mean()))


if __name__ == "__main__":
    main()
