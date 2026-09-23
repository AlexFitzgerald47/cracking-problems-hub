# -*- coding: utf-8 -*-
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC = [json.loads(l) for l in open("data/entries.jsonl")]
USE = [r for r in REC if not r["is_kalend"] and r["n_words"] >= 3]
for r in USE:
    r["tags"] = gazetteer.tag(r["text"])

def series(witness, tag, lo, hi):
    yk = collections.Counter(); yn = collections.Counter()
    for r in USE:
        if r["witness"] != witness or not (lo <= r["year"] < hi):
            continue
        yn[r["year"]] += 1
        if r["tags"][tag]:
            yk[r["year"]] += 1
    years = sorted(yn)
    return years, [yk[y] for y in years], [yn[y] for y in years]

def cell(witness, tag, lo, hi):
    y, k, n = series(witness, tag, lo, hi)
    return sum(k), sum(n)

out = {}

# ---- P1 ---------------------------------------------------------------------
y, k, n = series("AU", "SCOT", 550, 1000)
stat, cut, left, right = cp.scan(y, k, n)
null = cp.permutation_null(y, k, n)
boot = cp.bootstrap_cut(y, k, n)
out["P1"] = {"witness": "AU", "tag": "SCOT", "window": [550, 1000],
             "n_years": len(y), "n_entries": sum(n), "n_tagged": sum(k),
             "cut": cut, "stat": stat,
             "left": {"k": left[0], "n": left[1], "rate": left[0]/left[1]},
             "right": {"k": right[0], "n": right[1], "rate": right[0]/right[1]},
             "null": null, "bootstrap_cut": boot}
print("P1  AU SCOT 550-1000: cut=%s stat=%.2f  left %d/%d=%.4f  right %d/%d=%.4f  p=%.4f  boot95=[%s,%s]"
      % (cut, stat, left[0], left[1], left[0]/left[1], right[0], right[1], right[0]/right[1],
         null["p"], boot["lo95"], boot["hi95"]))

# ---- P3 specificity, P5 midland rise, plus Munster as a second control ------
for tag in ("INSULAR", "MIDLAND", "MUNSTER", "SCOT_AMBIG"):
    y2, k2, n2 = series("AU", tag, 550, 1000)
    s2, c2, l2, r2 = cp.scan(y2, k2, n2)
    nl = cp.permutation_null(y2, k2, n2, n_perm=2000)
    bt = cp.bootstrap_cut(y2, k2, n2, n_boot=1000)
    out[tag] = {"cut": c2, "stat": s2,
                "left": {"k": l2[0], "n": l2[1], "rate": l2[0]/l2[1]},
                "right": {"k": r2[0], "n": r2[1], "rate": r2[0]/r2[1]},
                "null": nl, "bootstrap_cut": bt}
    print("    AU %-11s cut=%s stat=%.2f  left %d/%d=%.4f -> right %d/%d=%.4f  p=%.4f  boot95=[%s,%s]"
          % (tag, c2, s2, l2[0], l2[1], l2[0]/l2[1], r2[0], r2[1], r2[0]/r2[1],
             nl["p"], bt["lo95"] if bt else "-", bt["hi95"] if bt else "-"))

# ---- P2 independent witnesses ----------------------------------------------
c = out["P1"]["cut"]
p2 = {}
a, b = cell("CS", "SCOT", 550, 723); cc, dd = cell("CS", "SCOT", 804, 1000)
p2["CS_across_lacuna"] = {"pre": [a, b], "post": [cc, dd],
    "rate_pre": a/b if b else None, "rate_post": cc/dd if dd else None,
    "fisher_p_greater": cp.fisher_exact_greater(a, b - a, cc, dd - cc)}
for w, hi in (("AI", 1000), ("AT", 767)):
    a, b = cell(w, "SCOT", 550, c); cc, dd = cell(w, "SCOT", c, hi)
    p2[w] = {"pre": [a, b], "post": [cc, dd],
             "rate_pre": a/b if b else None, "rate_post": cc/dd if dd else None,
             "fisher_p_greater": cp.fisher_exact_greater(a, b - a, cc, dd - cc)}
out["P2"] = p2
for kk, v in p2.items():
    print("P2  %-18s pre %d/%d=%.4f  post %d/%d=%.4f  fisher p=%.4f"
          % (kk, v["pre"][0], v["pre"][1], v["rate_pre"] or 0,
             v["post"][0], v["post"][1], v["rate_post"] or 0, v["fisher_p_greater"]))

json.dump(out, open("results/main.json", "w"), indent=1)
print("\nwrote results/main.json")
