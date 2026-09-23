"""Does a changepoint in the marker rate exist, and where?

Two separate questions, which the first cut of this analysis conflated:

  * EXISTENCE -- compare the two-rate model against the one-rate model by
    likelihood ratio, and null it by shuffling the marker labels while holding
    every entry in its own year (so the year profile, which is wildly uneven,
    is preserved exactly).
  * LOCATION -- year-level bootstrap, resampling whole years with replacement.

Nulling the fitted *location* answers neither and was the wrong test.
"""
import sys, json, math, random, collections
from common import load
from markers import is_marked

MIN_SIDE = 100


def ll_bin(k, n):
    if n == 0: return 0.0
    p = k / n
    if p <= 0 or p >= 1: return 0.0
    return k * math.log(p) + (n - k) * math.log(1 - p)


def fit(xs):
    """xs: list of (year, 0/1).  Returns (cp, LR statistic)."""
    n = len(xs); k = sum(v for _, v in xs)
    base = ll_bin(k, n)
    by = collections.defaultdict(lambda: [0, 0])
    for y, v in xs:
        by[y][0] += 1; by[y][1] += v
    yrs = sorted(by)
    cn = ck = 0
    best = (None, -1e18)
    for y in yrs:
        if cn >= MIN_SIDE and n - cn >= MIN_SIDE:
            s = ll_bin(ck, cn) + ll_bin(k - ck, n - cn)
            if s > best[1]: best = (y, s)
        cn += by[y][0]; ck += by[y][1]
    if best[0] is None: return None, 0.0
    return best[0], 2 * (best[1] - base)


def main(inp, outp):
    E = load(inp)
    xs = [(e["year"], 1 if is_marked(e["text"]) else 0) for e in E if 350 <= e["year"] < 1200]
    cp, lr = fit(xs)
    n = len(xs); k = sum(v for _, v in xs)
    print("observed: n=%d  marked=%d  fitted changepoint=%d  LR=%.1f" % (n, k, cp, lr))

    rnd = random.Random(20260923)
    yrs = [y for y, _ in xs]; labs = [v for _, v in xs]
    null_lr = []
    for _ in range(1000):
        rnd.shuffle(labs)
        _, l = fit(list(zip(yrs, labs)))
        null_lr.append(l)
    ge = sum(1 for l in null_lr if l >= lr)
    print("existence: permutation null (1000 draws, years fixed)  max null LR=%.1f  "
          "p = %d/1000 = %.4f" % (max(null_lr), ge, (ge + 1) / 1001.0))

    # location: year-level bootstrap
    by = collections.defaultdict(list)
    for y, v in xs: by[y].append(v)
    yrs_u = sorted(by)
    boots = []
    for _ in range(500):
        samp = []
        for _ in range(len(yrs_u)):
            y = rnd.choice(yrs_u)
            samp.extend((y, v) for v in by[y])
        c, _ = fit(samp)
        if c is not None: boots.append(c)
    boots.sort()
    lo = boots[int(0.025 * len(boots))]; hi = boots[int(0.975 * len(boots))]
    print("location: year-level bootstrap 95%% CI = %d-%d (median %d)"
          % (lo, hi, boots[len(boots) // 2]))

    # two-rate description at the fitted point
    a = [v for y, v in xs if y < cp]; b = [v for y, v in xs if y >= cp]
    print("rates: before %d = %d/%d = %.4f   after = %d/%d = %.5f"
          % (cp, sum(a), len(a), sum(a) / len(a), sum(b), len(b), sum(b) / len(b)))
    json.dump({"cp": cp, "LR": lr, "n": n, "k": k, "p_exist": (ge + 1) / 1001.0,
               "max_null_LR": max(null_lr), "boot95": [lo, hi],
               "rate_before": sum(a) / len(a), "rate_after": sum(b) / len(b)},
              open(outp, "w"), indent=1)
    print("wrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
