"""Null model for the Patrician gap.

"0 of 40 clusters reach 31 years" is a rank, not a probability: the comparison
class simply has no gap that large, so a bootstrap from it returns p = 0, which
is not a number anyone should quote.  This fits the gap distribution instead and
asks how often the fitted process would throw a gap of 31 or more.

Three fits, deliberately including one with a much heavier tail than the data
suggest, because the answer turns entirely on the tail and the data do not
constrain it:

  * geometric  -- memoryless, the natural discrete null;
  * lognormal  -- heavier;
  * Pareto     -- heaviest, fitted to the upper half only (Hill estimator).

Reported alongside is the look-anywhere version: the class contains N_gaps
consecutive steps, so the chance that SOME step reaches 31 is the quantity to
quote if one had gone hunting for the largest gap rather than being sent to
Patrick by the problem.
"""
import sys, json, math, random
from run_gap import load_clusters

TARGET = 31


def geom_p_ge(gaps, x):
    """Geometric on support {1,2,...} with mean m: P(G >= x) = (1-1/m)^(x-1)."""
    m = sum(gaps) / len(gaps)
    q = 1.0 - 1.0 / m
    return q ** (x - 1), m


def lognorm_p_ge(gaps, x):
    ls = [math.log(g) for g in gaps]
    mu = sum(ls) / len(ls)
    sd = math.sqrt(sum((l - mu) ** 2 for l in ls) / (len(ls) - 1))
    z = (math.log(x - 0.5) - mu) / sd
    return 0.5 * math.erfc(z / math.sqrt(2)), (mu, sd)


def pareto_p_ge(gaps, x):
    """Hill estimator on the upper half; deliberately the most generous tail."""
    s = sorted(gaps, reverse=True)
    k = max(3, len(s) // 2)
    xk = s[k]
    if xk < 1: xk = 1
    alpha = k / sum(math.log(s[i] / xk) for i in range(k) if s[i] > xk)
    frac = k / len(gaps)
    return frac * (x / xk) ** (-alpha), (alpha, xk)


def main(clusters_path, outp):
    C = load_clusters(clusters_path)
    gaps = [b - a for c in C for a, b in zip(c["years"], c["years"][1:])]
    n_gaps = len(gaps)
    print("pooled consecutive gaps: n=%d  min=%d  max=%d  mean=%.2f"
          % (n_gaps, min(gaps), max(gaps), sum(gaps) / n_gaps))
    print("  distribution:", sorted(gaps))

    res = {}
    pg, m = geom_p_ge(gaps, TARGET)
    print("\ngeometric  (mean %.2f):        P(gap >= %d) = %.2e" % (m, TARGET, pg))
    pl, (mu, sd) = lognorm_p_ge(gaps, TARGET)
    print("lognormal  (mu %.2f, sd %.2f): P(gap >= %d) = %.2e" % (mu, sd, TARGET, pl))
    pp, (al, xk) = pareto_p_ge(gaps, TARGET)
    print("Pareto     (alpha %.2f, x_m %d): P(gap >= %d) = %.2e" % (al, xk, TARGET, pp))

    print("\nPatrick's obit cluster has 3 consecutive steps; probability at least one")
    print("reaches %d under each fit:" % TARGET)
    for name, p in (("geometric", pg), ("lognormal", pl), ("Pareto", pp)):
        print("  %-10s %.2e" % (name, 1 - (1 - p) ** 3))
    print("\nlook-anywhere: probability that SOME step among the class's %d reaches %d:" % (n_gaps, TARGET))
    for name, p in (("geometric", pg), ("lognormal", pl), ("Pareto", pp)):
        print("  %-10s %.3f" % (name, 1 - (1 - p) ** n_gaps))

    # resolution: what gap would the empirical class alone have failed to flag?
    print("\nresolution of the empirical comparison: the class's largest observed gap is %d,"
          % max(gaps))
    print("so a Patrician gap of %d or less would not have been distinguishable from it." % max(gaps))

    res = {"n_clusters": len(C), "n_gaps": n_gaps, "gaps": sorted(gaps),
           "target": TARGET, "mean_gap": sum(gaps) / n_gaps, "max_gap": max(gaps),
           "p_geometric": pg, "p_lognormal": pl, "p_pareto": pp,
           "p_cluster_geometric": 1 - (1 - pg) ** 3,
           "p_cluster_lognormal": 1 - (1 - pl) ** 3,
           "p_cluster_pareto": 1 - (1 - pp) ** 3,
           "p_lookanywhere_geometric": 1 - (1 - pg) ** n_gaps,
           "p_lookanywhere_lognormal": 1 - (1 - pl) ** n_gaps,
           "p_lookanywhere_pareto": 1 - (1 - pp) ** n_gaps}
    json.dump(res, open(outp, "w"), indent=1)
    print("\nwrote", outp)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
