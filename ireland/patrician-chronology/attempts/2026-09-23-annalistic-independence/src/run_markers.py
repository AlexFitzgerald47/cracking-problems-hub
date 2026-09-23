"""Analysis 1: where in the corpus does the compiler visibly arbitrate?

Reports the marker rate by half-century for each witness separately, so that a
result cannot rest on one translator's habits, and fits a single changepoint
with a permutation null that holds each entry in its own year.
"""
import sys, json, collections, random
from common import load, WITNESSES
from markers import is_marked


def rate_table(entries, binsize=50):
    tot = collections.Counter(); mk = collections.Counter()
    for e in entries:
        b = (e["year"] // binsize) * binsize
        tot[b] += 1
        if is_marked(e["text"]):
            mk[b] += 1
    return mk, tot


def best_changepoint(entries, lo, hi):
    """Year c maximising the binomial log-likelihood of a two-rate model."""
    import math
    ys = sorted({e["year"] for e in entries if lo <= e["year"] < hi})
    xs = [(e["year"], 1 if is_marked(e["text"]) else 0) for e in entries if lo <= e["year"] < hi]
    n = len(xs); k = sum(v for _, v in xs)
    def ll(k1, n1, k2, n2):
        out = 0.0
        for kk, nn in ((k1, n1), (k2, n2)):
            if nn == 0: continue
            p = kk / nn
            if 0 < p < 1: out += kk * math.log(p) + (nn - kk) * math.log(1 - p)
        return out
    best = (None, -1e18)
    for c in ys:
        n1 = sum(1 for y, _ in xs if y < c); k1 = sum(v for y, v in xs if y < c)
        if n1 < 100 or n - n1 < 100: continue
        s = ll(k1, n1, k - k1, n - n1)
        if s > best[1]: best = (c, s)
    return best[0], best[1], n, k


def main(inp, outp):
    E = load(inp)
    out = {}
    print("marker rate by half-century, per witness")
    hdr = "%6s " % "bin" + "".join("%12s" % w for w in WITNESSES)
    print(hdr)
    per = {w: rate_table([e for e in E if e["witness"] == w]) for w in WITNESSES}
    bins = sorted({b for w in WITNESSES for b in per[w][1]})
    rows = []
    for b in bins:
        cells = []
        row = {"bin": b}
        for w in WITNESSES:
            mk, tot = per[w]
            t = tot.get(b, 0); m = mk.get(b, 0)
            cells.append("%3d/%-4d" % (m, t) if t else "     -   ")
            row[w] = [m, t]
        rows.append(row)
        print("%6d " % b + "".join("%12s" % c for c in cells))
    out["by_bin"] = rows

    print("\nearly (<=699) vs late (>=700), per witness")
    out["early_late"] = {}
    for w in WITNESSES:
        sub = [e for e in E if e["witness"] == w]
        a = [e for e in sub if e["year"] < 700]; b = [e for e in sub if e["year"] >= 700]
        ra = sum(1 for e in a if is_marked(e["text"])); rb = sum(1 for e in b if is_marked(e["text"]))
        out["early_late"][w] = {"early": [ra, len(a)], "late": [rb, len(b)]}
        print("  %s  early %3d/%-4d = %.4f   late %3d/%-4d = %.4f   ratio %.0fx"
              % (w, ra, len(a), ra / len(a), rb, len(b), rb / len(b),
                 (ra / len(a)) / (rb / len(b)) if rb else float("inf")))

    print("\nsingle changepoint on the pooled corpus, 350-1200")
    c, s, n, k = best_changepoint(E, 350, 1200)
    print("  fitted changepoint: %s  (n=%d entries, k=%d marked)" % (c, n, k))
    # permutation null: keep each entry's year, shuffle the marked labels
    rnd = random.Random(20260923)
    xs = [(e["year"], 1 if is_marked(e["text"]) else 0) for e in E if 350 <= e["year"] < 1200]
    labs = [v for _, v in xs]; yrs = [y for y, _ in xs]
    draws = []
    for _ in range(500):
        rnd.shuffle(labs)
        fake = [{"year": y, "text": "as some say" if v else "x"} for y, v in zip(yrs, labs)]
        cc, _, _, _ = best_changepoint(fake, 350, 1200)
        draws.append(cc)
    lo = sorted(draws)[int(0.025 * len(draws))]; hi = sorted(draws)[int(0.975 * len(draws))]
    print("  permutation null (500 draws, years held fixed): 95%% range %d-%d" % (lo, hi))
    out["changepoint"] = {"fitted": c, "n": n, "k": k, "null_95": [lo, hi],
                          "null_draws": draws}
    json.dump(out, open(outp, "w"), indent=1)
    print("wrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
