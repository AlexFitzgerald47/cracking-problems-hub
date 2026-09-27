#!/usr/bin/env python3
"""STEP 6 — the power analysis. What can this corpus actually decide?

`worklevel.py` finds the correction changes WHICH works are recovered without
changing HOW MANY (3 of 7 either way). Before reading that as "the correction does
nothing", and before a future session re-runs it hoping for a cleaner answer, work
out what a 7-work test can detect at all.
"""
import sys, os
from collections import defaultdict
import numpy as np
from scipy.stats import binomtest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from worklevel import work_level
from correction import detrend, register_centre, registers_of

N_CAND = 11


def macro_by_author(rows):
    per = defaultdict(list)
    for r in rows:
        per[r["author"]].append(r["correct"])
    return float(np.mean([np.mean(v) for v in per.values()])), \
        {a: f"{sum(v)}/{len(v)}" for a, v in per.items()}


def main():
    docs, Z, feats = common.load()
    train_rows = [d["_i"] for d in docs if d["genre"] in common.LETTERS]
    out = {}

    print("=" * 78)
    print("WORK-LEVEL SCORE, PER AUTHOR (the unbiased view of worklevel.py TEST 1)")
    for tag, dt, ct in (("uncorrected", False, False), ("detrend + centre", True, True)):
        Zt = detrend(Z, docs, train_rows) if dt else Z
        Zw = register_centre(Zt, docs, registers_of(docs), True) if ct else Zt
        rows = work_level(docs, Zw, Zw, common.LETTERS, common.FORMAL)
        m, detail = macro_by_author(rows)
        n_ok = sum(r["correct"] for r in rows)
        print(f"\n  {tag}: {n_ok}/{len(rows)} works, author-macro {m:.3f}")
        for a, s in sorted(detail.items()):
            print(f"      {a:20s} {s}")
        out[tag] = dict(works_correct=n_ok, n_works=len(rows), author_macro=m,
                        detail=detail)

    print("\n" + "=" * 78)
    print("WHAT A 7-WORK TEST CAN DETECT  (chance = 1/11 per work)")
    p0 = 1 / N_CAND
    print(f"  k correct   one-sided binomial p against chance {p0:.3f}")
    for k in range(0, 8):
        p = binomtest(k, 7, p0, alternative="greater").pvalue
        flag = "  <-- first k that clears 0.05" if p < 0.05 and \
            binomtest(k - 1, 7, p0, alternative="greater").pvalue >= 0.05 else ""
        mark = "  <-- observed, both arms" if k == 3 else ""
        print(f"    {k}/7      p = {p:.4f}{flag}{mark}")
    out["binomial_table"] = {k: float(binomtest(k, 7, p0, alternative="greater").pvalue)
                             for k in range(8)}

    print("""
  So 3/7 clears 0.05 on its own -- but that is the score of BOTH arms, so it cannot
  separate them. The question this folder needs answered is not "is cross-register
  attribution above chance" but "is the corrected arm better than the uncorrected
  one", and that is a PAIRED comparison on the same 7 works.""")

    print("\n" + "=" * 78)
    print("THE PAIRED TEST, WHICH IS THE ONE THAT MATTERS")
    print("""  McNemar on the 7 works: uncorrected right / corrected wrong = Burke x3;
  uncorrected wrong / corrected right = Francis x1, Johnson x2. Discordant pairs
  b=3, c=3.""")
    from scipy.stats import binomtest as bt
    p_mc = bt(3, 6, 0.5).pvalue
    print(f"  exact McNemar two-sided p = {p_mc:.3f} -- a dead heat, by construction.")
    print("""  The smallest two-sided p a 7-work McNemar can reach is with all 7
  discordant and all one way:""")
    print(f"    b=7, c=0  ->  p = {bt(7, 7, 0.5).pvalue:.4f}")
    print(f"    b=6, c=0  ->  p = {bt(6, 6, 0.5).pvalue:.4f}")
    print(f"    b=5, c=0  ->  p = {bt(5, 5, 0.5).pvalue:.4f}  <-- P-FLOOR: 5 discordant")
    print("""    pairs all in one direction is the MINIMUM this test needs to fire at
    0.05, and only 7 works exist. The paired test is not underpowered by bad luck;
    it is nearly unusable by construction.""")
    out["mcnemar"] = dict(b=3, c=3, p=float(p_mc),
                          floor_5=float(bt(5, 5, 0.5).pvalue))

    print("\n" + "=" * 78)
    print("HOW MANY INDEPENDENT CROSS-REGISTER WORKS WOULD BE NEEDED?")
    print("""  Assume the honest read of the chunk-level evidence: the correction lifts
  per-work accuracy from chance (1/11 = 0.09) to roughly the corrected author-macro
  (0.50). Required n for a one-sided binomial at alpha=0.05 with 80% power:""")
    for n in range(4, 31):
        # smallest k with p<0.05 under H0
        k_crit = next((k for k in range(n + 1)
                       if binomtest(k, n, p0, alternative="greater").pvalue < 0.05), None)
        if k_crit is None:
            continue
        # power under p=0.50
        from scipy.stats import binom
        pw = 1 - binom.cdf(k_crit - 1, n, 0.50)
        if pw >= 0.80:
            print(f"    n = {n} works: reject at k >= {k_crit}, power {pw:.2f} "
                  f"<-- SUFFICIENT")
            out["n_needed_unpaired"] = n
            break
        if n <= 12:
            print(f"    n = {n} works: reject at k >= {k_crit}, power {pw:.2f}")
    print(f"""
  And for the PAIRED comparison, which is the real question, a McNemar test needs at
  least 5 discordant works all one way merely to reach p < 0.05. At the observed
  discordance rate (6 of 7 works discordant) that means roughly 6-8 independent
  cross-register works with a CONSISTENT direction of change. This corpus has 7 works
  from 4 authors, and 3 of those 7 are Burke's.""")

    print("\n" + "=" * 78)
    print("AND THE BINDING CONSTRAINT IS NOT THE TEST, IT IS APPLICABILITY")
    print("""  Even a decisive verdict on the correction would not transfer to Junius.
  The centring step needs independent works in the QUESTIONED register. Junius's
  register holds two works and both are editions of his own collection. The repair
  used in junius_apply.py -- centring him on five political-prose pamphlets -- is a
  register substitution, not the recipe, and its own validation cell is ONE work.""")
    common.dump("power.json", out)


if __name__ == "__main__":
    main()
