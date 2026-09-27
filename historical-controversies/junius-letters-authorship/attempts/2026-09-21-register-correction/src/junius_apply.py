#!/usr/bin/env python3
"""STEP 4 — apply the corrected protocol to Junius himself, and validate it first.

`applicability.py` shows the plain recipe cannot be used on Junius: his questioned
register (`public_letter`) holds two works and both are editions of his own
collection, so a leave-one-work-out centring reference for Junius IS Junius.

There is one defensible repair. Junius's register is public political polemic, and
the panel holds five INDEPENDENT works in that register: Wilkes's *English Liberty*,
Price's *Observations*, Pownall's *Administration of the Colonies*, Boyd's
*Miscellaneous Works* and Francis's *Two Speeches*. None is by Junius. Centring
Junius on the mean of those five works is author-blind with respect to Junius and
uses no public_letter text at all.

Before trusting it on Junius it is validated on the one cell that has a known answer
in exactly this configuration: Philip Francis's *Two Speeches* (political prose)
against private-letter centroids, centred on the OTHER FOUR political works. That is
the same operation, the same registers, and a ground truth.

A caveat that runs one way only: the centring reference for Junius includes Francis's
own *Two Speeches*. If Francis were Junius, subtracting it would remove part of the
candidate's own style from the questioned text, biasing AGAINST Francis. The run is
therefore repeated with that work dropped from the reference.
"""
import sys, os
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from correction import detrend, register_centre, registers_of
from sink_tabulation import attribute, macro_accuracy

POLITICAL_WORKS = ("bim_eighteenth-century_english-liberty-being-a_wilkes-john_1769_1",
                   "observationsonna00pric", "administrationb01wargoog",
                   "miscellaneouswor01boydiala", "twospeechesinhou00franiala")


def build(docs, Z, reference_works, do_detrend=True, do_centre=True):
    """Return (Z_train, Z_quest) under the protocol. Training = private letters,
    centred leave-one-work-out inside the letters register. Questioned documents are
    centred on the mean of `reference_works`, excluding the document's own work."""
    Zt = Z
    train_rows = [d["_i"] for d in docs if d["genre"] in common.LETTERS]
    if do_detrend:
        Zt = detrend(Zt, docs, train_rows)
    Zq = Zt.copy()
    if do_centre:
        regs = {"letters": train_rows}
        Zt2 = register_centre(Zt, docs, regs, work_level=True)
        wrows = defaultdict(list)
        for d in docs:
            if d["source"] in reference_works:
                wrows[d["source"]].append(d["_i"])
        wmean = {w: Zt[v].mean(0) for w, v in wrows.items()}
        for d in docs:
            others = [wmean[w] for w in wmean if w != d["source"]]
            if others:
                Zq[d["_i"]] = Zt[d["_i"]] - np.mean(others, 0)
        return Zt2, Zq
    return Zt, Zq


def run(docs, Z, reference_works, tag, do_detrend=True, do_centre=True):
    Ztr, Zq = build(docs, Z, reference_works, do_detrend, do_centre)
    train = common.index(docs, common.LETTERS)
    cents = {a: Ztr[v].mean(0) for a, v in train.items()}

    # ---- validation cell: Francis's Two Speeches, known answer
    ftest = [d["_i"] for d in docs if d["source"] == "twospeechesinhou00franiala"
             and d["author"] == "Philip_Francis"]
    ranks, ok = [], 0
    for i in ftest:
        order = sorted(cents, key=lambda a: float(np.abs(Zq[i] - cents[a]).mean()))
        ranks.append(order.index("Philip_Francis") + 1)
        ok += order[0] == "Philip_Francis"
    print(f"\n{tag}")
    print(f"  VALIDATION  Francis political prose -> private-letter centroids: "
          f"{ok}/{len(ftest)} top-1, median rank {np.median(ranks):.1f} of {len(cents)}"
          f"   (chance top-1 {1/len(cents):.3f}, chance median rank {(len(cents)+1)/2:.1f})")

    # ---- Junius
    out_j = {}
    for src in ("junius_1772_wikisource", "junius_1813_ocr"):
        jt = [d["_i"] for d in docs if d["author"] == "Junius" and d["source"] == src]
        if not jt:
            continue
        per = Counter()
        dist = defaultdict(list)
        for i in jt:
            ds = {a: float(np.abs(Zq[i] - cents[a]).mean()) for a in cents}
            per[min(ds, key=ds.get)] += 1
            for a, v in ds.items():
                dist[a].append(v)
        cen = Zq[jt].mean(0)
        cd = sorted(((float(np.abs(cen - c).mean()), a) for a, c in cents.items()))
        fr = [k for k, (_, a) in enumerate(cd, 1) if a == "Philip_Francis"][0]
        print(f"  JUNIUS ({src.split('_')[1]}): centroid ranking, "
              f"Philip Francis is #{fr} of {len(cd)}")
        for k, (d, a) in enumerate(cd, 1):
            mark = "   <-- CANDIDATE" if a == "Philip_Francis" else ""
            print(f"      {k:2d}. {d:.3f}  {a}{mark}")
        print(f"      document-level votes: " +
              ", ".join(f"{a.split('_')[-1]} {n}" for a, n in per.most_common(4)))
        out_j[src] = dict(francis_rank=fr, ranking=[[a, d] for d, a in cd],
                          votes=dict(per))
    return dict(validation=dict(top1=ok, n=len(ftest), median_rank=float(np.median(ranks)),
                                n_cand=len(cents)), junius=out_j)


def main():
    docs, Z, feats = common.load()
    out = {}
    out["uncorrected"] = run(docs, Z, POLITICAL_WORKS,
                             "ARM 0  UNCORRECTED (baseline, same code path)",
                             do_detrend=False, do_centre=False)
    out["corrected"] = run(docs, Z, POLITICAL_WORKS,
                           "ARM 1  detrend + centre on 5 political works")
    out["corrected_no_francis"] = run(
        docs, Z, tuple(w for w in POLITICAL_WORKS if w != "twospeechesinhou00franiala"),
        "ARM 2  as ARM 1 but Francis's own Two Speeches dropped from the reference")
    out["centre_only"] = run(docs, Z, POLITICAL_WORKS,
                             "ARM 3  centring only, no detrend", do_detrend=False)

    print("\n" + "=" * 78)
    print("BINOMIAL CHECK on the validation cell (n is small and this matters)")
    from scipy.stats import binomtest
    for k, v in out.items():
        r = v["validation"]
        p = binomtest(r["top1"], r["n"], 1 / r["n_cand"], alternative="greater").pvalue
        print(f"  {k:22s} {r['top1']}/{r['n']} top-1 vs chance {1/r['n_cand']:.3f}"
              f"   one-sided p = {p:.3f}")
        v["validation"]["binom_p"] = float(p)
    print("\n  The smallest p this cell can produce is "
          f"{binomtest(10, 10, 1/11, alternative='greater').pvalue:.2e} (a perfect 10/10),")
    print("  so it is not p-floor-limited; it is simply a 10-document test.")
    common.dump("junius_apply.json", out)


if __name__ == "__main__":
    main()
