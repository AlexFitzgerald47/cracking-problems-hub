# -*- coding: utf-8 -*-
import sys, os, json, collections, math, re
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

REC = [json.loads(l) for l in open("data/entries.jsonl")]
USE = [r for r in REC if not r["is_kalend"] and r["n_words"] >= 3]
for r in USE:
    r["tags"] = gazetteer.tag(r["text"])

def series(w, tag, lo, hi):
    yk = collections.Counter(); yn = collections.Counter()
    for r in USE:
        if r["witness"] == w and lo <= r["year"] < hi:
            yn[r["year"]] += 1
            if r["tags"][tag]: yk[r["year"]] += 1
    ys = sorted(yn); return ys, [yk[y] for y in ys], [yn[y] for y in ys]

out = {}
y, k, n = series("AU", "SCOT", 550, 1000)

# ---- profile likelihood over the cut ---------------------------------------
K, N = sum(k), sum(n); base = cp._ll(K, N)
prof = []; ck = cn = 0
for i in range(len(y) - 1):
    ck += k[i]; cn += n[i]
    if cn < 150 or N - cn < 150: continue
    prof.append((y[i+1], 2*(cp._ll(ck,cn)+cp._ll(K-ck,N-cn)-base)))
best = max(p[1] for p in prof)
# a 2-unit drop in log-lik (statistic drop of ~3.84) is the usual support interval
supp = [c for c, s in prof if s >= best - 3.84]
out["profile"] = {"best_stat": best, "argmax": max(prof, key=lambda p: p[1])[0],
                  "support_interval_chi1": [min(supp), max(supp)],
                  "curve": prof}
print("AU SCOT profile: argmax=%d  max stat=%.2f  chi2(1) support interval=[%d, %d]"
      % (out["profile"]["argmax"], best, min(supp), max(supp)))
for c in (727, 740, 750, 760, 780, 800, 808, 816, 825, 850):
    hit = [s for cc, s in prof if cc == c]
    print("     fixed cut %d -> stat %.2f%s" % (c, hit[0] if hit else float('nan'),
          "   <- literature's c.740" if c == 740 else ("   <- argmax" if c == 808 else "")))
out["fixed_cuts"] = {str(c): ([s for cc, s in prof if cc == c] or [None])[0]
                     for c in (727,740,750,760,780,800,808,816,825,850)}

# ---- two-changepoint fit ----------------------------------------------------
bestpair = (-1, None, None)
cum_k = [0]; cum_n = [0]
for i in range(len(y)):
    cum_k.append(cum_k[-1]+k[i]); cum_n.append(cum_n[-1]+n[i])
for i in range(len(y)-2):
    for j in range(i+1, len(y)-1):
        n1, k1 = cum_n[i+1], cum_k[i+1]
        n2, k2 = cum_n[j+1]-cum_n[i+1], cum_k[j+1]-cum_k[i+1]
        n3, k3 = N-cum_n[j+1], K-cum_k[j+1]
        if min(n1,n2,n3) < 150: continue
        s = 2*(cp._ll(k1,n1)+cp._ll(k2,n2)+cp._ll(k3,n3)-base)
        if s > bestpair[0]: bestpair = (s, y[i+1], y[j+1], (k1,n1),(k2,n2),(k3,n3))
print("\n2-changepoint: cuts=%d,%d stat=%.2f  segs %d/%d=%.3f | %d/%d=%.3f | %d/%d=%.3f  (1-cp stat %.2f, d.stat=%.2f on 2 extra df)"
      % (bestpair[1], bestpair[2], bestpair[0],
         bestpair[3][0],bestpair[3][1],bestpair[3][0]/bestpair[3][1],
         bestpair[4][0],bestpair[4][1],bestpair[4][0]/bestpair[4][1],
         bestpair[5][0],bestpair[5][1],bestpair[5][0]/bestpair[5][1],
         best, bestpair[0]-best))
out["two_changepoint"] = {"stat": bestpair[0], "cuts": [bestpair[1], bestpair[2]],
    "segments": [{"k":s[0],"n":s[1],"rate":s[0]/s[1]} for s in bestpair[3:]],
    "improvement_over_one": bestpair[0]-best}

# ---- term-level decomposition: is one term carrying the whole effect? ------
TERMS = {"Iona (Í/Ia/Iona)": r"(?<!Dath )(?<!Mac )\bÍ\b|\bIa\b|\bIona\b",
         "Pict*": r"Pict", "Dál Riata": r"Dál Riat", "Fortriu": r"Fortriu",
         "other Scottish places": r"Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|Mag Luinge|Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|Kingarth|Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|Druim Alban|Iardoman|Athfhotla|Circinn|Dún Nechtain"}
print("\nAU SCOT decomposed by term (counts of entries matching, per 50-yr block)")
hdr = "%-10s %6s " % ("block", "n") + " ".join("%-22s" % t for t in TERMS)
print(hdr)
dec = []
for lo in range(550, 1000, 50):
    sub = [r for r in USE if r["witness"]=="AU" and lo <= r["year"] < lo+50]
    if not sub: continue
    row = {"block": lo, "n": len(sub)}
    cells = []
    for t, pat in TERMS.items():
        c = sum(1 for r in sub if re.search(pat, r["text"]))
        row[t] = c; cells.append("%-22s" % ("%d (%.1f%%)" % (c, 100*c/len(sub))))
    dec.append(row)
    print("%-10s %6d " % ("%d-%d"%(lo,lo+49), len(sub)) + " ".join(cells))
out["term_decomposition"] = dec
json.dump(out, open("results/profile.json","w"), indent=1)
print("\nwrote results/profile.json")
