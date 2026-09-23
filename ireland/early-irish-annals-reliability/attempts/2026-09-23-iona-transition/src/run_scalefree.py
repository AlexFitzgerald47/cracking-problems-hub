# -*- coding: utf-8 -*-
"""Compositional control.

Per-year tag PROPORTIONS share one denominator, so if the foreign classes fall
the Irish classes must rise even if nothing changed about Irish reporting.  The
MIDLAND "rise" therefore cannot be read as independent evidence of anything until
it is measured scale-free.  Two ratios fix this, each computed inside one class
so that the other class's movement cannot drive it:

    SCOT / (SCOT + INSULAR)      share of FOREIGN news that is Scottish
    MIDLAND / (MIDLAND+MUNSTER)  share of IRISH regional news that is midland
"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC = [json.loads(l) for l in open("data/entries.jsonl")]
USE = [r for r in REC if not r["is_kalend"] and r["n_words"] >= 3]
for r in USE:
    r["tags"] = gazetteer.tag(r["text"])

def ratio_series(witness, num, den_extra, lo, hi):
    yk = collections.Counter(); yn = collections.Counter()
    for r in USE:
        if r["witness"] != witness or not (lo <= r["year"] < hi):
            continue
        t = r["tags"]
        inn = t[num]; ind = t[num] or t[den_extra]
        if ind:
            yn[r["year"]] += 1
            if inn:
                yk[r["year"]] += 1
    years = sorted(yn)
    return years, [yk[y] for y in years], [yn[y] for y in years]

out = {}
for label, (w, num, oth, lo, hi, mineq) in {
    "AU_SCOT_share_of_foreign":  ("AU", "SCOT", "INSULAR", 550, 1000, 40),
    "AU_MIDLAND_share_of_irish": ("AU", "MIDLAND", "MUNSTER", 550, 1000, 100),
    "CS_SCOT_share_of_foreign":  ("CS", "SCOT", "INSULAR", 550, 1000, 20),
}.items():
    y, k, n = ratio_series(w, num, oth, lo, hi)
    s, c, l, r = cp.scan(y, k, n, min_entries=mineq)
    nl = cp.permutation_null(y, k, n, n_perm=3000, min_entries=mineq)
    bt = cp.bootstrap_cut(y, k, n, n_boot=1500, min_entries=mineq)
    out[label] = {"cut": c, "stat": s, "n_units": sum(n),
                  "left": {"k": l[0], "n": l[1], "rate": l[0]/l[1]},
                  "right": {"k": r[0], "n": r[1], "rate": r[0]/r[1]},
                  "null": nl, "bootstrap_cut": bt}
    print("%-28s cut=%s stat=%.2f  %d/%d=%.3f -> %d/%d=%.3f  p=%.4f  boot95=[%s,%s]"
          % (label, c, s, l[0], l[1], l[0]/l[1], r[0], r[1], r[0]/r[1], nl["p"],
             bt["lo95"] if bt else "-", bt["hi95"] if bt else "-"))

# ---- full composition table, every cell, per 50-year block ------------------
print("\nAU composition by 50-year block (percent of non-kalend entries; classes overlap)")
print("%-10s %6s %6s %7s %8s %8s %9s" % ("block","n","SCOT","INSULAR","MIDLAND","MUNSTER","UNTAGGED"))
comp = []
for lo in range(550, 1000, 50):
    sub = [r for r in USE if r["witness"] == "AU" and lo <= r["year"] < lo + 50]
    n = len(sub)
    if not n: continue
    row = {"block": lo, "n": n}
    for t in ("SCOT", "INSULAR", "MIDLAND", "MUNSTER"):
        row[t] = sum(1 for r in sub if r["tags"][t]) / n
    row["UNTAGGED"] = sum(1 for r in sub if not any(
        r["tags"][t] for t in ("SCOT","INSULAR","MIDLAND","MUNSTER"))) / n
    comp.append(row)
    print("%-10s %6d %5.1f%% %6.1f%% %7.1f%% %7.1f%% %8.1f%%"
          % ("%d-%d"%(lo,lo+49), n, 100*row["SCOT"], 100*row["INSULAR"],
             100*row["MIDLAND"], 100*row["MUNSTER"], 100*row["UNTAGGED"]))
out["AU_composition_50yr"] = comp
json.dump(out, open("results/scalefree.json", "w"), indent=1)
print("\nwrote results/scalefree.json")
