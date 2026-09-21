#!/usr/bin/env python3
"""Track B: is the Junius register gap partly a long-s OCR artefact?

In this panel the private-letter register is almost all 19th/20th-century reprints
(long-s damage 1e-5..2e-4) while the political-prose register is eighteenth-century
printings (0.017..0.021). Long-s damage is not uniform noise: the long s is set initially
and medially, so it lands on function words -- the features Burrows's Delta uses.

Treatment: refit the feature set to the SAME 120 count with every long-s-vulnerable
function word removed.
Null: refit the same way with an equal number of RANK-MATCHED non-vulnerable words
removed, 200 draws. Without this null a change means only that the operation moved the
number.

Every cell is printed, and the headline is a ratio of two costs from the same baseline,
per board/log/2026-09-21-rescaled-metric-invalidates-margin.md.

Predictions frozen in ../FREEZE.md before this file was run.
"""
import json, os, sys, random
from collections import Counter, defaultdict
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K
sys.path.insert(0, K.PRIOR)
import corpus as C

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")


def cell_stats(docs, Z):
    cells = K.author_genre_cells(docs)
    cents = {k: Z[v].mean(0) for k, v in cells.items()}
    same_author_cross_reg, diff_author_same_reg = [], []
    pairs = sorted(cents)
    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            (a1, g1), (a2, g2) = pairs[i], pairs[j]
            if "Junius" in a1 or "Junius" in a2:
                continue
            d = float(np.abs(cents[pairs[i]] - cents[pairs[j]]).mean())
            if a1 == a2 and g1 != g2:
                same_author_cross_reg.append((a1, g1, g2, d))
            elif a1 != a2 and g1 == g2:
                diff_author_same_reg.append(d)
    return cents, same_author_cross_reg, diff_author_same_reg


def summarise(docs, Z, label, verbose=True):
    cents, sacr, dasr = cell_stats(docs, Z)
    selfd = {a: d for a, _, _, d in sacr}
    m_cross = float(np.median([d for *_, d in sacr]))
    m_same = float(np.median(dasr))
    if verbose:
        print(f"\n--- {label}")
        print("   same author, different register (all cells):")
        for a, g1, g2, d in sorted(sacr, key=lambda t: -t[3]):
            print(f"      {a:<18} {g1:<16} vs {g2:<16} {d:.3f}")
        print(f"   median same-author cross-register      {m_cross:.3f}  (n={len(sacr)})")
        print(f"   median different-author same-register  {m_same:.3f}  (n={len(dasr)})")
        print(f"   RATIO cross/same                       {m_cross/m_same:.3f}")
    return dict(self_distances=selfd, median_cross=m_cross, median_same=m_same,
                ratio=m_cross / m_same)


def main():
    docs, counts, ranked = K.load_docs()
    out = {}

    # ---- damage rate per cell, measured on the chunk texts themselves
    by_cell = defaultdict(list)
    for d in docs:
        by_cell[(d["author"], d["genre"])].append(C.long_s_rate(d["text"]))
    print("measured long-s damage rate per (author, register) cell:")
    dmg = {}
    for k in sorted(by_cell, key=lambda k: -np.mean(by_cell[k])):
        if len(by_cell[k]) >= 8:
            dmg[f"{k[0]}|{k[1]}"] = float(np.mean(by_cell[k]))
            print(f"   {k[0]:<20} {k[1]:<16} {np.mean(by_cell[k]):.5f}  (n={len(by_cell[k])})")
    out["damage_by_cell"] = dmg

    base_feats = ranked[:K.N_FEATURES]
    vulnerable = [w for w in base_feats if K.long_s_vulnerable(w)]
    print(f"\nlong-s-vulnerable words in the baseline top-{K.N_FEATURES}: "
          f"{len(vulnerable)} -> {vulnerable}")
    out["vulnerable_features"] = vulnerable

    Zb = K.build_Z(counts, base_feats)
    base = summarise(docs, Zb, f"BASELINE ({K.N_FEATURES} function words, as 2026-09-17)")
    out["baseline"] = base

    rob_feats = K.feats_excluding(ranked, set(vulnerable))
    Zr = K.build_Z(counts, rob_feats)
    rob = summarise(docs, Zr, f"DAMAGE-ROBUST ({K.N_FEATURES} words, {len(vulnerable)} "
                              f"long-s-vulnerable removed, refitted to the same count)")
    out["damage_robust"] = rob

    # ---- the null: same number of words removed, matched on frequency rank
    rng = random.Random(4242)
    null_ratio, null_self = [], defaultdict(list)
    for _ in range(200):
        ex = K.rank_matched_null_exclusion(ranked, set(vulnerable), rng)
        f = K.feats_excluding(ranked, ex)
        s = summarise(docs, K.build_Z(counts, f), "", verbose=False)
        null_ratio.append(s["ratio"])
        for a, d in s["self_distances"].items():
            null_self[a].append(d)
    out["null_ratio"] = dict(median=float(np.median(null_ratio)),
                             p05=float(np.percentile(null_ratio, 5)),
                             p95=float(np.percentile(null_ratio, 95)))

    print("\n================ B2 / B3 verdicts ================")
    print(f"{'author':<18} {'baseline':>9} {'robust':>9} {'drop':>8}   "
          f"{'null drop (median [p05,p95])':>34}")
    verdict = {}
    for a in sorted(base["self_distances"], key=lambda a: -base["self_distances"][a]):
        b, r = base["self_distances"][a], rob["self_distances"][a]
        nd = [b - x for x in null_self[a]]
        z = (b - r - np.median(nd)) / (np.std(nd) + 1e-12)
        print(f"{a:<18} {b:>9.3f} {r:>9.3f} {b-r:>8.3f}   "
              f"{np.median(nd):>10.3f} [{np.percentile(nd,5):.3f},{np.percentile(nd,95):.3f}]"
              f"   z={z:+.2f}")
        verdict[a] = dict(baseline=b, robust=r, drop=b - r,
                          null_drop_median=float(np.median(nd)),
                          null_drop_p05=float(np.percentile(nd, 5)),
                          null_drop_p95=float(np.percentile(nd, 95)), z=float(z))
    out["self_distance_verdict"] = verdict

    print(f"\nRATIO (median same-author cross-register / median different-author same-register)")
    print(f"   baseline       {base['ratio']:.3f}")
    print(f"   damage-robust  {rob['ratio']:.3f}   "
          f"({100*(rob['ratio']-base['ratio'])/base['ratio']:+.1f}%)")
    print(f"   null           {np.median(null_ratio):.3f} "
          f"[{np.percentile(null_ratio,5):.3f}, {np.percentile(null_ratio,95):.3f}]")
    pr = float(np.mean([x <= rob["ratio"] for x in null_ratio]))
    print(f"   p(null ratio <= observed robust ratio) = {pr:.3f}")
    out["ratio_p"] = pr

    # ---- B1: are the cross-register prediction sinks biased toward clean classes?
    from shift_or_loss import train_index, attribute
    trainF = train_index(docs, K.FORMAL)
    testL = [i for i, d in enumerate(docs)
             if d["genre"] in K.LETTERS and d["author"] in trainF
             and d["author"] not in ("Junius", "Philo_Junius")]
    acc, preds = attribute(Zb, docs, trainF, testL)
    fdmg = {}
    for a in trainF:
        rates = [C.long_s_rate(docs[i]["text"]) for i in trainF[a]]
        fdmg[a] = float(np.mean(rates))
    clean = [a for a in trainF if fdmg[a] <= 4e-4]
    got = sum(1 for p in preds if p in clean)
    print(f"\nB1  formal candidates with damage <= 4e-4: {sorted(clean)}")
    print(f"    they absorb {got}/{len(preds)} = {got/len(preds):.3f} of predictions "
          f"({len(clean)}/{len(trainF)} = {len(clean)/len(trainF):.3f} of candidates)")
    out["B1"] = dict(clean=sorted(clean), frac=got / len(preds),
                     candidate_frac=len(clean) / len(trainF), damage=fdmg)

    accr, predsr = attribute(Zr, docs, trainF, testL)
    gotr = sum(1 for p in predsr if p in clean)
    print(f"    on damage-robust features: accuracy {accr:.3f} (baseline {acc:.3f}), "
          f"clean share {gotr/len(predsr):.3f}")
    out["B1_robust"] = dict(accuracy=accr, clean_frac=gotr / len(predsr))

    json.dump(out, open(os.path.join(RES, "damage_confound.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
