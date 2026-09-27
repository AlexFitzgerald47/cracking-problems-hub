#!/usr/bin/env python3
"""STEP 3 — is the correction APPLICABLE to this corpus, and to Junius in particular?

The centring step subtracts, from each document, the mean of the OTHER WORKS in its
own register. That is author-blind by construction. It is only author-blind IN EFFECT
if no single author owns a large share of the works in that register -- otherwise a
writer has his own style subtracted from himself, and the correction destroys exactly
the author it is supposed to preserve.

The Shakespeare corpus had 943 non-dramatic chunks over 27 dramatists. This one does
not. This file measures the work composition of every register, then runs a
DIAGNOSTIC (not a usable method -- it looks at the author label) that removes all of a
document's own author's works from its centring reference. If the authors who collapse
under the real correction recover under the diagnostic, domination is the cause.
"""
import sys, os
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from sink_tabulation import attribute, marginal, excess, macro_accuracy
from correction import detrend, registers_of, evaluate, apply_treatment


def centre_excluding(Z, docs, rows_by_register, mode):
    """mode='work'   : leave-one-work-out   (the real, author-blind method)
       mode='author' : leave-one-author-out (LABEL-LEAKING DIAGNOSTIC ONLY)"""
    out = Z.copy()
    for reg, rows in rows_by_register.items():
        by_work = defaultdict(list)
        for i in rows:
            by_work[docs[i]["source"]].append(i)
        wmean = {w: Z[v].mean(0) for w, v in by_work.items()}
        wauth = {w: docs[by_work[w][0]]["author"] for w in by_work}
        for w, v in by_work.items():
            if mode == "work":
                others = [x for x in wmean if x != w]
            else:
                others = [x for x in wmean if wauth[x] != wauth[w]]
            if not others:
                continue
            out[v] = Z[v] - np.mean([wmean[x] for x in others], 0)
    return out


def main():
    docs, Z, feats = common.load()
    regs = registers_of(docs)

    print("=" * 78)
    print("WORK COMPOSITION OF EACH REGISTER  (the applicability precondition)")
    for reg, rows in regs.items():
        works = {}
        for i in rows:
            works.setdefault(docs[i]["source"], docs[i]["author"])
        c = Counter(works.values())
        n = len(works)
        print(f"\n  {reg}: {n} works")
        for a, k in c.most_common():
            share_after_loo = (k - 1) / (n - 1) if n > 1 else 1.0
            flag = "  <-- dominates its own centring reference" if share_after_loo >= 0.2 else ""
            print(f"    {a:20s} {k} work(s)   own share of a leave-one-work-out "
                  f"reference: {share_after_loo*100:.0f}%{flag}")

    print("\n" + "=" * 78)
    print("DIAGNOSTIC: does Burke recover when his OWN works are kept out of the")
    print("centring reference? (label-leaking; diagnostic only, not a method)")
    train_rows = [d["_i"] for d in docs if d["genre"] in common.LETTERS]
    for mode in ("work", "author"):
        Zt = detrend(Z, docs, train_rows)
        Zt = centre_excluding(Zt, docs, regs, mode)
        r = evaluate(Zt, docs, common.LETTERS, common.FORMAL,
                     f"detrend + centre[{mode}]")
        print("      per-class recall: " + "  ".join(
            f"{a.split('_')[-1]} {v:.2f}" for a, v in sorted(r["per_class"].items())))

    print("\n" + "=" * 78)
    print("CAN THE CORRECTION BE APPLIED TO JUNIUS AT ALL?")
    pub = regs["public_letter"]
    works = {}
    for i in pub:
        works.setdefault(docs[i]["source"], []).append(docs[i]["author"])
    for w, a in works.items():
        print(f"    work {w}: {dict(Counter(a))}")
    print("""
  The questioned register for the actual Junius attribution is `public_letter`, and it
  contains exactly TWO works -- and they are two editions of the SAME collection. A
  leave-one-work-out centring reference for a Junius-1772 chunk is therefore the
  Junius-1813 text: the same letters, by the same author, in another edition. The
  2026-09-17 session established that the edition effect is tiny next to the author
  effect (mean document-to-centroid Delta 0.773 across editions against 0.770 within
  one, versus 0.835 for a different author) -- which is exactly what makes it fatal
  here. The two works are near-identical, so centring subtracts Junius from Junius.
  The direct centroid-to-centroid distance between the two editions is printed below;
  compare it with the different-author same-register median of 0.471.""")

    # Quantify it: how much of the public-letter centring reference is Junius?
    j = [i for i in pub if docs[i]["author"] == "Junius"]
    print(f"\n    public_letter register: {len(pub)} chunks, "
          f"{len(j)} of them Junius ({len(j)/len(pub)*100:.0f}%)")
    d72 = [i for i in pub if docs[i]["source"] == "junius_1772_wikisource"
           and docs[i]["author"] == "Junius"]
    d13 = [i for i in pub if docs[i]["source"] == "junius_1813_ocr"
           and docs[i]["author"] == "Junius"]
    if d72 and d13:
        c72, c13 = Z[d72].mean(0), Z[d13].mean(0)
        print(f"    Delta(Junius-1772 centroid, Junius-1813 centroid) = "
              f"{float(np.abs(c72-c13).mean()):.3f}")
        print("    That is the whole of the leave-one-work-out centring reference "
              "available to Junius.")

    common.dump("applicability.json", dict(
        register_works={reg: Counter(
            docs[i]["author"] for i in {docs[j]["source"]: j for j in rows}.values())
            for reg, rows in regs.items()}))


if __name__ == "__main__":
    main()
