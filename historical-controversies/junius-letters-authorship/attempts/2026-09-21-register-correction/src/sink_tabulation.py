#!/usr/bin/env python3
"""STEP 1 — the shift-or-loss discriminator (HANDOVER 2026-09-21, item 1).

The question this file answers, and it answers it on output that already existed:

    When cross-register attribution fails on this corpus, WHERE do the wrong
    predictions go?

If they collapse onto one or two candidates, the failure is one shared displacement
direction and centring it out is worth a session. If they scatter evenly across the
candidate set, the authorial signal is genuinely gone across the register boundary
and the folder's archival reopening condition is the only route.

PRACTICES adds a sharpening that this file implements and that the raw
concentration number does not give you: under a label shuffle, predictions
concentrate MORE, not less, because with no signal the argmin lands arbitrarily on
whichever centroid happens to sit nearest the data cloud. So "one class absorbs 40%"
is not by itself evidence of a correctable shift. What identifies a real sink is
    (a) the SAME class absorbing on every subsample replicate, and
    (b) concentration ABOVE what the label-shuffle null produces.
Both are computed here.
"""
import sys, os
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

RNG = np.random.default_rng(20260921)
N_REPLICATES = 50
N_SHUFFLES = 200


def attribute(Z, train, test_idx, truth, loo=True):
    """Nearest-centroid Delta attribution. Leave-one-out inside the training set so
    the same-register control gets no advantage the cross-register arms lack."""
    preds = []
    base = {a: (np.sum(Z[v], 0), len(v)) for a, v in train.items()}
    for i in test_idx:
        best, bd = None, np.inf
        for a, (s, n) in base.items():
            if loo and i in train[a]:
                if n <= 1:
                    continue
                c = (s - Z[i]) / (n - 1)
            else:
                c = s / n
            d = float(np.abs(Z[i] - c).mean())
            if d < bd:
                best, bd = a, d
        preds.append(best)
    acc = float(np.mean([p == t for p, t in zip(preds, truth)]))
    return preds, acc


def marginal(preds, cands):
    c = Counter(preds)
    n = len(preds)
    return {a: c[a] / n for a in cands}


def excess(pred_marg, true_marg):
    """Largest EXCESS predicted share over a class's true share.

    Raw concentration is the wrong statistic and this corpus shows why: in the
    formal-vs-formal in-distribution cell, Burke absorbs 34.9% of predictions and
    that is above the label-shuffle null -- but Burke IS 36.2% of that test set, so
    there is no sink at all. What identifies a sink is a class absorbing far MORE
    than it is owed, and the same statistic has to be computed under the shuffle."""
    return max(pred_marg[a] - true_marg[a] for a in pred_marg)


def macro_accuracy(preds, truth):
    per = defaultdict(list)
    for p, t in zip(preds, truth):
        per[t].append(p == t)
    return float(np.mean([np.mean(v) for v in per.values()])), \
        {a: float(np.mean(v)) for a, v in per.items()}


def report(name, Z, docs, train_genres, test_genres):
    train = common.index(docs, train_genres)
    test = [d["_i"] for d in docs
            if d["genre"] in test_genres and d["author"] in train
            and d["author"] not in common.NOT_CANDIDATES]
    truth = [docs[i]["author"] for i in test]
    cands = sorted(train)
    preds, acc = attribute(Z, train, test, truth)
    marg = marginal(preds, cands)
    true_marg = marginal(truth, cands)
    macro, per_class = macro_accuracy(preds, truth)
    obs_excess = excess(marg, true_marg)
    majority = max(true_marg.values())

    print(f"\n{'='*74}\n{name}")
    print(f"  train register {train_genres} -> test register {test_genres}")
    print(f"  {len(cands)} candidates, {len(test)} test documents")
    print(f"  micro accuracy {acc:.3f}   macro accuracy {macro:.3f}   "
          f"(chance {1/len(cands):.3f}, majority-class baseline {majority:.3f})")
    print(f"  {'candidate':20s} {'TRUE share':>11s} {'PRED share':>11s} {'ratio':>7s}")
    for a in sorted(cands, key=lambda a: -marg[a]):
        r = marg[a] / true_marg[a] if true_marg[a] else float("inf")
        print(f"  {a:20s} {true_marg[a]*100:10.1f}% {marg[a]*100:10.1f}% {r:7.2f}")
    top = sorted(marg.items(), key=lambda kv: -kv[1])
    print(f"  LARGEST SINK: {top[0][0]} {top[0][1]*100:.1f}% of predictions   "
          f"top-2 {(top[0][1]+top[1][1])*100:.1f}%")
    print(f"  LARGEST EXCESS over true share: {obs_excess*100:+.1f} pp")
    print("  per-class recall: " + "  ".join(
        f"{a.split('_')[-1]} {per_class[a]:.2f}" for a in sorted(per_class)))

    # ---- (a) replicate stability: equal-n subsamples of the training register
    nmin = min(len(v) for v in train.values())
    n_sub = max(8, min(nmin, 40))
    shares = defaultdict(list)
    accs = []
    for _ in range(N_REPLICATES):
        sub = {a: list(RNG.choice(v, size=min(n_sub, len(v)), replace=False))
               for a, v in train.items()}
        p, a_ = attribute(Z, sub, test, truth)
        accs.append(a_)
        m = marginal(p, cands)
        for a in cands:
            shares[a].append(m[a])
    print(f"  --- {N_REPLICATES} equal-n replicates (n={n_sub} training docs/author) ---")
    print(f"  accuracy {np.mean(accs):.3f} +- {np.std(accs):.3f}")
    stab = sorted(((np.mean(v), np.std(v), a) for a, v in shares.items()), reverse=True)
    for m, s, a in stab[:4]:
        print(f"  {a:20s} absorbs {m*100:5.1f}% +- {s*100:.1f}%")

    # ---- (b) label-shuffle null: how concentrated is chance?
    null_top, null_acc, null_exc = [], [], []
    authors = sorted(train)
    pool = [(a, i) for a in authors for i in train[a]]
    sizes = [len(train[a]) for a in authors]
    for _ in range(N_SHUFFLES):
        idxs = [i for _, i in pool]
        RNG.shuffle(idxs)
        sh, k = {}, 0
        for a, n in zip(authors, sizes):
            sh[a] = idxs[k:k + n]
            k += n
        p, a_ = attribute(Z, sh, test, truth)
        null_acc.append(a_)
        null_top.append(max(Counter(p).values()) / len(p))
        null_exc.append(excess(marginal(p, cands), true_marg))
    print(f"  --- label-shuffle null, {N_SHUFFLES} permutations ---")
    print(f"  accuracy {np.mean(null_acc):.3f}  (p95 {np.percentile(null_acc,95):.3f})")
    print(f"  largest sink under shuffle: {np.mean(null_top)*100:.1f}% "
          f"+- {np.std(null_top)*100:.1f}%   (observed {top[0][1]*100:.1f}%)")
    print(f"  largest EXCESS under shuffle: {np.mean(null_exc)*100:+.1f} pp "
          f"(p95 {np.percentile(null_exc,95)*100:+.1f})   "
          f"(observed {obs_excess*100:+.1f} pp)")
    sink_real = obs_excess > np.percentile(null_exc, 95)
    stable = stab[0][1] < 0.5 * stab[0][0]
    verdict = ("SINK: one class absorbs above its true share, beyond the shuffle null"
               + (", and stably across replicates" if stable else
                  ", but unstably across replicates")
               if sink_real else
               "NO SINK above the shuffle null -- concentration is what chance looks like")
    print(f"  VERDICT: {verdict}")

    return dict(name=name, accuracy=acc, macro_accuracy=macro,
                per_class_recall=per_class, majority_baseline=majority,
                observed_excess=obs_excess,
                shuffle_excess=[float(np.mean(null_exc)), float(np.percentile(null_exc, 95))], n_candidates=len(cands), n_test=len(test),
                chance=1 / len(cands), pred_share=marg, true_share=true_marg,
                largest_sink=[top[0][0], top[0][1]], top2=top[0][1] + top[1][1],
                replicate_share={a: [float(np.mean(v)), float(np.std(v))]
                                 for a, v in shares.items()},
                replicate_accuracy=[float(np.mean(accs)), float(np.std(accs))],
                shuffle_accuracy=[float(np.mean(null_acc)), float(np.percentile(null_acc, 95))],
                shuffle_largest_sink=[float(np.mean(null_top)), float(np.std(null_top)),
                                      float(np.percentile(null_top, 95))],
                verdict=verdict)


def main():
    docs, Z, feats = common.load()
    out = {}
    out["cross_letters_from_formal"] = report(
        "CROSS-REGISTER A: private letters scored against formal-prose centroids",
        Z, docs, common.FORMAL, common.LETTERS)
    out["cross_formal_from_letters"] = report(
        "CROSS-REGISTER B: formal prose scored against private-letter centroids",
        Z, docs, common.LETTERS, common.FORMAL)
    out["within_letters"] = report(
        "IN-DISTRIBUTION reference: private letters vs private-letter centroids",
        Z, docs, common.LETTERS, common.LETTERS)
    out["within_formal"] = report(
        "IN-DISTRIBUTION reference: formal prose vs formal-prose centroids",
        Z, docs, common.FORMAL, common.FORMAL)
    common.dump("sink_tabulation.json", out)


if __name__ == "__main__":
    main()
