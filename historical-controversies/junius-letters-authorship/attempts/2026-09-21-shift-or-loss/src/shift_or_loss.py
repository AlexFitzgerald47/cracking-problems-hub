#!/usr/bin/env python3
"""Track A: is the Junius register failure a shared SHIFT or a genuine LOSS of signal?

Three tests, in increasing strength:

  A1  Where do the cross-register predictions go? Collapse onto one or two classes means
      a shared displacement worth centring out; even scatter means the signal is gone.
      Concentration alone is the wrong statistic -- under a label shuffle sinks concentrate
      MORE, because with no signal the argmin lands arbitrarily. What identifies a real
      sink is the same class absorbing on every replicate, so the bootstrap is run.

  A2  The mechanism-level version, which does not go through the argmin at all: for the
      four authors surviving in both registers, is the displacement between their two
      registers pointing in the SAME direction in feature space?

  A3  The transfer test. Estimate the register shift with the held-out author entirely
      absent, apply it, re-attribute. Deliberately leave-one-AUTHOR-out, which is stricter
      than the leave-one-work-out centring the Shakespeare session used.

Predictions frozen in ../FREEZE.md before this file was run.
"""
import json, os, sys, random
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
RNG = random.Random(20260921)


def train_index(docs, genres, min_chunks=8):
    t = defaultdict(list)
    for i, d in enumerate(docs):
        if d["genre"] in genres and d["author"] not in ("Junius", "Philo_Junius"):
            t[d["author"]].append(i)
    return {a: v for a, v in t.items() if len(v) >= min_chunks}


def attribute(Z, docs, train, test_idx, shift=None):
    """shift: dict author -> vector added to the TEST document before comparison, or None."""
    preds, ok = [], 0
    for i in test_idx:
        z = Z[i]
        if shift is not None:
            z = z + shift[docs[i]["author"]]
        cents = K.centroids(Z, train, skip_idx=i)
        p = min(cents, key=lambda a: float(np.abs(z - cents[a]).mean()))
        preds.append(p)
        ok += p == docs[i]["author"]
    return ok / len(test_idx), preds


def sink_report(preds, cands, label):
    n = len(preds)
    c = Counter(preds)
    rows = [(a, c.get(a, 0), c.get(a, 0) / n) for a in sorted(cands, key=lambda a: -c.get(a, 0))]
    print(f"\n{label}  (n={n}, {len(cands)} candidates, even split = {1/len(cands):.3f})")
    for a, k, f in rows:
        if k:
            print(f"   {a:<20} {k:>4}  {f:.3f}")
    top = rows[0]
    print(f"   -> largest receiver {top[0]} at {top[2]:.3f}")
    return dict(n=n, top=top[0], top_frac=top[2],
                distribution={a: k for a, k, _ in rows})


def main():
    docs, counts, ranked = K.load_docs()
    feats = ranked[:K.N_FEATURES]
    Z = K.build_Z(counts, feats)
    out = {}

    trainF = train_index(docs, K.FORMAL)
    trainL = train_index(docs, K.LETTERS)
    testL = [i for i, d in enumerate(docs)
             if d["genre"] in K.LETTERS and d["author"] in trainF
             and d["author"] not in ("Junius", "Philo_Junius")]

    # ---------------------------------------------------------------- A1
    acc, preds = attribute(Z, docs, trainF, testL)
    print(f"CROSS-REGISTER letters->formal  accuracy {acc:.3f}  (2026-09-17 reported 0.108)")
    out["cross"] = dict(accuracy=acc)
    out["cross_sink"] = sink_report(preds, sorted(trainF), "A1  cross-register prediction sink")

    # in-distribution comparator: same candidate set, same register as the training data
    testF = [i for i, d in enumerate(docs)
             if d["genre"] in K.FORMAL and d["author"] in trainF
             and d["author"] not in ("Junius", "Philo_Junius")]
    accF, predsF = attribute(Z, docs, trainF, testF)
    print(f"\nIN-DISTRIBUTION formal->formal  accuracy {accF:.3f}")
    out["indist"] = dict(accuracy=accF)
    out["indist_sink"] = sink_report(predsF, sorted(trainF), "A1  in-distribution prediction sink")

    # label-shuffle reference: with no signal at all, how concentrated does the sink get?
    shuf_top, shuf_frac = Counter(), []
    authors = sorted(trainF)
    for _ in range(50):
        perm = authors[:]
        RNG.shuffle(perm)
        mapping = dict(zip(authors, perm))
        t2 = defaultdict(list)
        for a, v in trainF.items():
            t2[mapping[a]] = v
        _, p2 = attribute(Z, docs, dict(t2), testL)
        c = Counter(p2)
        a, k = c.most_common(1)[0]
        shuf_top[a] += 1
        shuf_frac.append(k / len(p2))
    print(f"\n   label-shuffle reference: top-receiver share {np.mean(shuf_frac):.3f} "
          f"+- {np.std(shuf_frac):.3f}; top class identity {dict(shuf_top)}")
    out["label_shuffle"] = dict(mean_top_frac=float(np.mean(shuf_frac)),
                                sd_top_frac=float(np.std(shuf_frac)),
                                top_identity=dict(shuf_top))

    # bootstrap over test documents: is it the SAME class every time?
    boot = Counter()
    for _ in range(50):
        samp = [RNG.choice(testL) for _ in testL]
        _, p3 = attribute(Z, docs, trainF, samp)
        boot[Counter(p3).most_common(1)[0][0]] += 1
    print(f"   bootstrap over test docs (50x): top receiver identity {dict(boot)}")
    out["bootstrap_top"] = dict(boot)

    # ---------------------------------------------------------------- A2
    cells = K.author_genre_cells(docs)
    both = {}
    for (a, g), v in cells.items():
        if a in ("Junius", "Philo_Junius"):
            continue
        L = [i for i, d in enumerate(docs) if d["author"] == a and d["genre"] in K.LETTERS]
        F = [i for i, d in enumerate(docs) if d["author"] == a and d["genre"] in K.FORMAL]
        if len(L) >= 8 and len(F) >= 8:
            both[a] = (L, F)
    disp = {a: Z[F].mean(0) - Z[L].mean(0) for a, (L, F) in both.items()}
    print(f"\nA2  authors surviving in both registers: {sorted(both)}")
    names = sorted(disp)
    cos = {}
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            u, v = disp[names[i]], disp[names[j]]
            c = float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))
            cos[f"{names[i]}|{names[j]}"] = c
            print(f"   cos({names[i]:<15},{names[j]:<15}) = {c:+.3f}   "
                  f"|d| = {np.linalg.norm(u):.2f} / {np.linalg.norm(v):.2f}")
    med = float(np.median(list(cos.values())))
    print(f"   median pairwise cosine = {med:+.3f}   (random 120-d: 0 +- {1/np.sqrt(120):.3f})")
    out["displacement_cosines"] = cos
    out["displacement_median_cosine"] = med

    # ---------------------------------------------------------------- A3
    print("\nA3  leave-one-AUTHOR-out register-shift centring")
    # (a) shift estimated only from the OTHER two-register authors
    shift_paired = {}
    for a in both:
        others = [x for x in both if x != a]
        shift_paired[a] = np.mean([disp[x] for x in others], 0)
    for a in trainF:
        shift_paired.setdefault(a, np.mean([disp[x] for x in both], 0))
    accA, predsA = attribute(Z, docs, trainF, testL, shift=shift_paired)
    print(f"   paired-displacement centring : {accA:.3f}   (uncorrected {acc:.3f})")
    out["corrected_paired"] = dict(accuracy=accA)
    out["corrected_paired_sink"] = sink_report(predsA, sorted(trainF),
                                               "A3  sink after paired centring")

    # (b) global register-mean centring, author-blind: subtract the mean of the letters
    #     register computed WITHOUT the test author, add the mean of the formal register
    #     computed WITHOUT the test author.
    shift_global = {}
    for a in trainF:
        Lidx = [i for i, d in enumerate(docs)
                if d["genre"] in K.LETTERS and d["author"] != a
                and d["author"] not in ("Junius", "Philo_Junius")]
        Fidx = [i for i, d in enumerate(docs)
                if d["genre"] in K.FORMAL and d["author"] != a
                and d["author"] not in ("Junius", "Philo_Junius")]
        shift_global[a] = Z[Fidx].mean(0) - Z[Lidx].mean(0)
    accB, predsB = attribute(Z, docs, trainF, testL, shift=shift_global)
    print(f"   global register-mean centring: {accB:.3f}   (uncorrected {acc:.3f})")
    out["corrected_global"] = dict(accuracy=accB)
    out["corrected_global_sink"] = sink_report(predsB, sorted(trainF),
                                               "A3  sink after global centring")

    # permutation null for the corrected numbers: same treatment, shuffled author labels
    nulls = []
    for _ in range(200):
        perm = authors[:]
        RNG.shuffle(perm)
        mapping = dict(zip(authors, perm))
        t2 = {mapping[a]: v for a, v in trainF.items()}
        sg = {mapping[a]: shift_global[a] for a in trainF}
        # test docs keep their true authors; the candidate labels are what is permuted
        okn = 0
        for i in testL:
            z = Z[i] + sg.get(docs[i]["author"], 0)
            cents = K.centroids(Z, t2, skip_idx=i)
            p = min(cents, key=lambda a: float(np.abs(z - cents[a]).mean()))
            okn += p == docs[i]["author"]
        nulls.append(okn / len(testL))
    p95 = float(np.percentile(nulls, 95))
    pval = float(np.mean([n >= accB for n in nulls]))
    print(f"   permutation null (200x): median {np.median(nulls):.3f}, p95 {p95:.3f}, "
          f"p = {pval:.3f}")
    out["null_corrected_global"] = dict(median=float(np.median(nulls)), p95=p95, p=pval)

    json.dump(out, open(os.path.join(RES, "shift_or_loss.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
