"""Can the annals' hour statements measure the Earth's rotation?

Experiment 5 in HANDOVER.md, and this is the calculation that decides whether it
is worth a session.  The idea: an annalistic "at the ninth hour" is a constraint
on Delta-T, because the unequal hour a phase falls in is a step function of it.
Stephenson's first-millennium Delta-T curve rests on Babylonian, Chinese and Arab
records; an independent Irish constraint would be worth having.

The geometry is exact and simple.  The eclipse happens at a fixed TT.  A site's
local apparent solar time at that instant is a function of UT = TT - Delta-T, and
LAT tracks UT one for one, so **raising Delta-T by d seconds moves the eclipse d
seconds earlier in local apparent time**.  The unequal-hour boundaries, by
contrast, are fixed by date and latitude and do not move with Delta-T at all.

So one correct hour statement constrains Delta-T to an interval exactly one
unequal hour wide.  That is the whole result, and everything below is working out
what it is worth.

Run against the real canon, so the hour widths are the actual ones for the actual
dates rather than an average.
"""

import csv
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, Site, julian_day, delta_t, delta_t_sigma
from hour_analysis import daylight_bounds

ARMAGH = Site("Armagh", 54.3503, -6.6528)
HERE = os.path.dirname(os.path.abspath(__file__))


def hour_widths(min_mag=0.90):
    """Unequal-hour length, in seconds, for every plausibly-recorded eclipse."""
    out = []
    with open(os.path.join(HERE, "results", "eclipse_canon.csv")) as fh:
        for r in csv.DictReader(fh):
            if float(r["irish_mag_central"] or 0.0) < min_mag:
                continue
            y, m, d = [int(x) for x in r["date_julian_cal"].split("-")]
            jd_noon = julian_day(y, m, d) + 0.5
            dt = delta_t(y)
            sr, ss, _, _ = daylight_bounds(jd_noon, ARMAGH, dt)
            out.append({"date": r["date_julian_cal"], "year": y,
                        "hour_s": (ss - sr) / 12.0 * 3600.0,
                        "mag": float(r["irish_mag_central"])})
    return out


def expected_intersection(widths, n, trials=20000, seed=11):
    """Monte Carlo width of the intersection of n correct hour constraints.

    Each statement puts Delta-T in an interval of width W_i that contains the
    truth at a uniformly random offset -- uniform because the phase of the
    eclipse relative to the hour boundaries is unrelated to Delta-T.
    """
    rng = random.Random(seed)
    tot = 0.0
    empty = 0
    for _ in range(trials):
        picks = rng.sample(widths, n) if n <= len(widths) else \
            [rng.choice(widths) for _ in range(n)]
        lo, hi = -1e18, 1e18
        for w in picks:
            u = rng.random() * w
            lo = max(lo, -u)
            hi = min(hi, w - u)
        if hi <= lo:
            empty += 1
        else:
            tot += hi - lo
    return tot / max(1, trials - empty), empty / float(trials)


def main():
    w = hour_widths()
    widths = [x["hour_s"] for x in w]
    widths.sort()
    n = len(widths)
    print("Eclipses deep enough over Ireland to be plausibly recorded "
          "(magnitude >= 0.90): %d" % n)
    print("Unequal-hour length at Armagh on those dates:")
    print("  shortest %.0f s (%.0f min, midwinter)   longest %.0f s (%.0f min, midsummer)"
          % (widths[0], widths[0] / 60, widths[-1], widths[-1] / 60))
    print("  median   %.0f s (%.0f min)" % (widths[n // 2], widths[n // 2] / 60))
    print()
    print("A single correct hour statement therefore pins Delta-T to an interval")
    print("one unequal hour wide: typically +/-%.0f s." % (widths[n // 2] / 2))
    print("The published 1-sigma on Delta-T in this window is 15-50 s "
          "(Stephenson et al. 2016).")
    print("  -> one statement is about %.0fx too coarse to be worth anything."
          % (widths[n // 2] / 2 / 40.0))
    print()
    print("Intersecting N independent correct statements:")
    print("   N   expected interval   half-width   vs published sigma(40 s)")
    for k in (1, 2, 3, 5, 10, 20, 30, 50, 100):
        width, _ = expected_intersection(widths, k)
        print("  %3d   %8.0f s        +/-%6.0f s      %5.1fx worse"
              % (k, width, width / 2, width / 2 / 40.0))
    print()
    target = 80.0
    k = 1
    while k < 4000:
        width, _ = expected_intersection(widths, k, trials=3000)
        if width <= target:
            break
        k = int(k * 1.5) + 1
    print("To match the published precision (interval <= %.0f s, i.e. +/-40 s)"
          % target)
    print("you would need roughly **%d** independent correct hour statements." % k)
    print("The entire Irish astronomical corpus, 442-1133, contains of the order")
    print("of twenty records, and only some of them state an hour at all.")
    print()
    print("== the failure mode that actually kills it ==")
    print("The arithmetic above assumes every statement is correct *and* that you")
    print("know which contact it describes. Neither holds. AU 664 and Bede report")
    print("the same eclipse one unequal hour apart because one records onset and")
    print("the other maximum (see RESULTS.md section 1). Assign the phase wrongly")
    print("for even one record and its interval is disjoint from the rest:")
    for bad in (1, 2):
        good = 15
        print("   %d misassigned among %d: intersection is empty in %.0f%% of draws"
              % (bad, good + bad,
                 100.0 * _empty_rate(widths, good, bad)))
    print()
    print("VERDICT: experiment 5 is not worth a session as a Delta-T measurement.")
    print("An hour statement is a ~3000 s constraint against a 40 s published")
    print("error, the corpus is two orders of magnitude too small to close that,")
    print("and a single phase misassignment empties the intersection. Use the")
    print("hour statements the other way round, as RESULTS.md section 1 does:")
    print("fix Delta-T from the published curve and let it tell you which contact")
    print("a notice describes. That question the data can answer.")


def _empty_rate(widths, good, bad, trials=5000, seed=5):
    """Fraction of draws where one misassigned phase empties the intersection."""
    rng = random.Random(seed)
    empty = 0
    for _ in range(trials):
        lo, hi = -1e18, 1e18
        for _ in range(good):
            w = rng.choice(widths)
            u = rng.random() * w
            lo, hi = max(lo, -u), min(hi, w - u)
        for _ in range(bad):
            w = rng.choice(widths)
            u = rng.random() * w
            # wrong contact: the interval sits a whole unequal hour away
            lo, hi = max(lo, -u + w), min(hi, 2 * w - u)
        if hi <= lo:
            empty += 1
    return empty / float(trials)


if __name__ == "__main__":
    main()
