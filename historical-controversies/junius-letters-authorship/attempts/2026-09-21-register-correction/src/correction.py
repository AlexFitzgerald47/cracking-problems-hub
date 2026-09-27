#!/usr/bin/env python3
"""STEP 2 — port the Shakespeare register correction to the Junius corpus.

Recipe under test (board/log/2026-09-21-confound-gaps-are-correctable.md):

  1. DETREND against date. OLS each feature on document year, fitted on the TRAINING
     register only, subtract.
  2. CENTRE on the questioned register. Subtract from each document the mean of the
     OTHER WORKS in its own register. Leave-one-WORK-out, never leave-one-AUTHOR-out:
     the author-wise version adds back z - m + (n_a/(N-n_a))(m_a - m), a multiple of
     the author's own deviation scaled by how much of the corpus he owns.

Both operations are author-blind. Neither uses the questioned document's label.

Implementation choice, stated because it matters: the register mean is the mean OF THE
WORK MEANS, not the mean of the chunks. The formal register is 69% Burke+Johnson by
chunk count, so a chunk-level mean would be largely those two authors' style and
subtracting it would not be author-blind in effect even though it is author-blind in
construction. The chunk-level variant is run as a sensitivity check.

Metrics are micro AND macro accuracy. Micro alone is uninterpretable here: the
direction-B test set is 48.7% Burke, so a constant "Burke" classifier scores 0.487,
above the 0.342 the uncorrected method achieves.
"""
import sys, os
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from sink_tabulation import attribute, marginal, excess, macro_accuracy

RNG = np.random.default_rng(20260921)
N_PERM = 200


# ------------------------------------------------------------------ corrections
def detrend(Z, docs, fit_rows, years=None):
    """OLS each feature on year, fitted on fit_rows only; subtract the fitted trend
    from every row. `years` lets a permuted year map be substituted for the null."""
    y = np.array([years[d["_i"]] if years is not None else d["year"] for d in docs],
                 dtype=float)
    yf = y[fit_rows]
    A = np.column_stack([np.ones(len(yf)), yf])
    coef, *_ = np.linalg.lstsq(A, Z[fit_rows], rcond=None)
    pred = np.column_stack([np.ones(len(y)), y]) @ coef
    return Z - pred


def register_centre(Z, docs, rows_by_register, work_level=True):
    """Leave-one-work-out centring inside each register."""
    out = Z.copy()
    for reg, rows in rows_by_register.items():
        by_work = defaultdict(list)
        for i in rows:
            by_work[docs[i]["source"]].append(i)
        if work_level:
            work_mean = {w: Z[v].mean(0) for w, v in by_work.items()}
            tot = np.sum(list(work_mean.values()), 0)
            k = len(work_mean)
            for w, v in by_work.items():
                m = (tot - work_mean[w]) / (k - 1) if k > 1 else np.zeros(Z.shape[1])
                out[v] = Z[v] - m
        else:
            tot, n = Z[rows].sum(0), len(rows)
            for w, v in by_work.items():
                s, c = Z[v].sum(0), len(v)
                m = (tot - s) / (n - c) if n > c else np.zeros(Z.shape[1])
                out[v] = Z[v] - m
    return out


def registers_of(docs):
    r = defaultdict(list)
    for d in docs:
        reg = "formal" if d["genre"] in common.FORMAL else (
            "letters" if d["genre"] in common.LETTERS else "public_letter")
        r[reg].append(d["_i"])
    return r


def apply_treatment(Z, docs, name, train_genres, years=None, work_level=True):
    regs = registers_of(docs)
    train_rows = [d["_i"] for d in docs if d["genre"] in train_genres]
    Zt = Z
    if "detrend" in name:
        Zt = detrend(Zt, docs, train_rows, years=years)
    if "centre" in name:
        Zt = register_centre(Zt, docs, regs, work_level=work_level)
    return Zt


# ------------------------------------------------------------------ evaluation
def evaluate(Z, docs, train_genres, test_genres, tag, quiet=False):
    train = common.index(docs, train_genres)
    test = [d["_i"] for d in docs
            if d["genre"] in test_genres and d["author"] in train
            and d["author"] not in common.NOT_CANDIDATES]
    truth = [docs[i]["author"] for i in test]
    cands = sorted(train)
    preds, micro = attribute(Z, train, test, truth)
    macro, per_class = macro_accuracy(preds, truth)
    marg, true_marg = marginal(preds, cands), marginal(truth, cands)
    exc = excess(marg, true_marg)
    top = max(marg.items(), key=lambda kv: kv[1])
    if not quiet:
        print(f"  {tag:34s} micro {micro:.3f}  macro {macro:.3f}  "
              f"excess {exc*100:+5.1f}pp  sink {top[0].split('_')[-1]} {top[1]*100:.0f}%")
    return dict(micro=micro, macro=macro, excess=exc, sink=[top[0], top[1]],
                per_class=per_class, n=len(test), n_cand=len(cands),
                chance=1 / len(cands), majority=max(true_marg.values()))


def francis_cell(Z, docs, quiet=False):
    """THE cell the Junius attribution has to cross, and the only one this corpus
    offers: Philip Francis's 10 acknowledged political-prose chunks scored against
    11 private-letter centroids. Same register pairing as Junius -> Francis."""
    train = common.index(docs, common.LETTERS)
    test = [d["_i"] for d in docs
            if d["genre"] == "political_prose" and d["author"] == "Philip_Francis"]
    truth = ["Philip_Francis"] * len(test)
    preds, acc = attribute(Z, train, test, truth)
    # also his rank, which is what an attribution study would actually report
    cents = {a: Z[v].mean(0) for a, v in train.items()}
    ranks = []
    for i in test:
        order = sorted(cents, key=lambda a: float(np.abs(Z[i] - cents[a]).mean()))
        ranks.append(order.index("Philip_Francis") + 1)
    if not quiet:
        print(f"    Francis political-prose -> private-letter centroids: "
              f"{int(acc*len(test))}/{len(test)} correct, "
              f"median rank {np.median(ranks):.1f} of {len(cents)}")
    return dict(correct=int(acc * len(test)), n=len(test),
                median_rank=float(np.median(ranks)), n_cand=len(cents),
                ranks=ranks)


def cost_ratio(Z, docs, quiet=False):
    """SCALE-FREE statistic. Every treatment here rescales Delta, so a before/after
    margin between two mean distances is not comparable across treatments -- that is
    the documented failure that inverted a Shakespeare headline. Report the RATIO of
    the register cost to the author cost, both measured from the same cells."""
    cells = defaultdict(list)
    for d in docs:
        cells[(d["author"], d["genre"])].append(d["_i"])
    cents = {k: Z[v].mean(0) for k, v in cells.items() if len(v) >= 8}
    dl = lambda a, b: float(np.abs(a - b).mean())
    A = [dl(c1, c2) for (a1, g1), c1 in cents.items() for (a2, g2), c2 in cents.items()
         if a1 == a2 and g1 < g2]
    B = []
    by = defaultdict(list)
    for (a, g), c in cents.items():
        by[g].append(c)
    for g, lst in by.items():
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                B.append(dl(lst[i], lst[j]))
    A, B = np.array(A), np.array(B)
    fr = dl(cents[("Philip_Francis", "private_letter")],
            cents[("Philip_Francis", "political_prose")])
    if not quiet:
        print(f"    register cost {np.median(A):.3f} / author cost {np.median(B):.3f} "
              f"= RATIO {np.median(A)/np.median(B):.3f}   "
              f"| Francis-vs-Francis {fr:.3f} = {fr/np.median(B):.2f}x author cost")
    return dict(register=float(np.median(A)), author=float(np.median(B)),
                ratio=float(np.median(A) / np.median(B)), n_A=len(A), n_B=len(B),
                francis_self=fr, francis_self_ratio=float(fr / np.median(B)))


# ------------------------------------------------------------------ main
def main():
    docs, Z, feats = common.load()
    out = {}
    arms = ["raw", "centre", "detrend", "detrend+centre"]

    for label, train_g, test_g, key in (
            ("DIRECTION B  formal prose <- private-letter centroids  (the Junius shape)",
             common.LETTERS, common.FORMAL, "B"),
            ("DIRECTION A  private letters <- formal-prose centroids",
             common.FORMAL, common.LETTERS, "A")):
        print(f"\n{'='*78}\n{label}")
        out[key] = {}
        for arm in arms:
            Zt = apply_treatment(Z, docs, arm, train_g)
            out[key][arm] = evaluate(Zt, docs, train_g, test_g, arm)

    print(f"\n{'='*78}\nIN-DISTRIBUTION REFERENCE on the same treated features")
    out["within"] = {}
    for arm in arms:
        Zt = apply_treatment(Z, docs, arm, common.LETTERS)
        out["within"][arm] = evaluate(Zt, docs, common.LETTERS, common.LETTERS,
                                      arm + " (letters)")

    print(f"\n{'='*78}\nTHE FRANCIS CELL and the scale-free cost ratio")
    out["francis"], out["ratio"] = {}, {}
    for arm in arms:
        print(f"  {arm}")
        Zt = apply_treatment(Z, docs, arm, common.LETTERS)
        out["francis"][arm] = francis_cell(Zt, docs)
        out["ratio"][arm] = cost_ratio(Zt, docs)

    print(f"\n{'='*78}\nSENSITIVITY: chunk-level register mean instead of work-level")
    out["chunk_level"] = {}
    for arm in ("centre", "detrend+centre"):
        Zt = apply_treatment(Z, docs, arm, common.LETTERS, work_level=False)
        out["chunk_level"][arm] = evaluate(Zt, docs, common.LETTERS, common.FORMAL,
                                           arm + " chunk-mean")

    print(f"\n{'='*78}\nNULL 1: permuted year map (does detrending measure chronology?)")
    src_years = {}
    for d in docs:
        src_years.setdefault(d["source"], d["year"])
    out["year_null"] = []
    for _ in range(50):
        vals = list(src_years.values())
        RNG.shuffle(vals)
        perm = dict(zip(src_years, vals))
        years = np.array([perm[d["source"]] for d in docs])
        Zt = detrend(Z, docs, [d["_i"] for d in docs if d["genre"] in common.LETTERS],
                     years=years)
        Zt = register_centre(Zt, docs, registers_of(docs))
        r = evaluate(Zt, docs, common.LETTERS, common.FORMAL, "", quiet=True)
        out["year_null"].append([r["micro"], r["macro"]])
    yn = np.array(out["year_null"])
    real = out["B"]["detrend+centre"]
    print(f"  real year map    micro {real['micro']:.3f}  macro {real['macro']:.3f}")
    print(f"  permuted (n=50)  micro {yn[:,0].mean():.3f} +- {yn[:,0].std():.3f}  "
          f"macro {yn[:,1].mean():.3f} +- {yn[:,1].std():.3f}")
    print(f"  centring alone   micro {out['B']['centre']['micro']:.3f}  "
          f"macro {out['B']['centre']['macro']:.3f}")
    print(f"  p(perm macro >= real) = {(yn[:,1] >= real['macro']).mean():.3f}")

    print(f"\n{'='*78}\nNULL 2: label permutation at matched budget, direction B, "
          "detrend+centre")
    Zt = apply_treatment(Z, docs, "detrend+centre", common.LETTERS)
    train = common.index(docs, common.LETTERS)
    test = [d["_i"] for d in docs if d["genre"] in common.FORMAL
            and d["author"] in train and d["author"] not in common.NOT_CANDIDATES]
    truth = [docs[i]["author"] for i in test]
    authors, sizes = sorted(train), [len(train[a]) for a in sorted(train)]
    nm = []
    for _ in range(N_PERM):
        idxs = [i for a in authors for i in train[a]]
        RNG.shuffle(idxs)
        sh, k = {}, 0
        for a, n in zip(authors, sizes):
            sh[a] = idxs[k:k + n]; k += n
        p, mi = attribute(Zt, sh, test, truth)
        ma, _ = macro_accuracy(p, truth)
        nm.append([mi, ma])
    nm = np.array(nm)
    print(f"  observed   micro {real['micro']:.3f}  macro {real['macro']:.3f}")
    print(f"  null       micro {nm[:,0].mean():.3f} (p95 {np.percentile(nm[:,0],95):.3f})"
          f"  macro {nm[:,1].mean():.3f} (p95 {np.percentile(nm[:,1],95):.3f})")
    print(f"  p(null macro >= observed) = {(nm[:,1] >= real['macro']).mean():.3f}")
    out["label_null"] = dict(micro=[float(nm[:,0].mean()), float(np.percentile(nm[:,0],95))],
                             macro=[float(nm[:,1].mean()), float(np.percentile(nm[:,1],95))],
                             p_macro=float((nm[:,1] >= real["macro"]).mean()))
    common.dump("correction.json", out)


if __name__ == "__main__":
    main()
