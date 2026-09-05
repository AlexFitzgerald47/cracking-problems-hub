"""Correct a systematic underestimate at the top of the solar canon.

**The bug.** `find_eclipses.py` finds each site's maximum by sampling the eclipse
window every two minutes and taking the best sample. For most eclipses that is
harmless: the magnitude has a smooth parabolic maximum and a one-minute offset
costs about 0.0002.

For *near-central* eclipses it is not harmless, and those are exactly the ones
that matter here. When the topocentric separation at greatest phase is small, the
separation behaves like |v·t| rather than a parabola -- the magnitude has a **cusp**
at maximum, dropping linearly at roughly 0.016 per minute. A two-minute grid can
therefore miss the peak by up to about 0.016 in magnitude, and it always misses
downwards.

Caught by comparing two of this project's own outputs: the canon gave 0.9951 for
865-01-01 at Armagh where `record_audit.py`, which refines properly, gave 0.999.
A 10-second scan confirms 0.99941. The canon was wrong, not the audit.

This matters at exactly one place -- the boundary between "deep partial" and
"central" -- which is the boundary the AU 885 argument and the count of central
eclipses both stand on.

**The fix.** Rather than re-run the 26-minute canon at a finer step, refine only
where it can matter: any site whose grid magnitude is at least `THRESHOLD`, by
golden-section search around the grid peak. Everything below that is already
accurate to a few times 1e-4.
"""

import csv
import math
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, local_circumstances, delta_t
from find_eclipses import SITES, IRISH, DT_OFFSETS

THRESHOLD = 0.80
HERE = os.path.dirname(os.path.abspath(__file__))
CANON = os.path.join(HERE, "results", "eclipse_canon.csv")


MIN_SUN_ALT = -0.9   # the canon's definition of "as seen": Sun above the horizon


def refine(jd_guess, site, dt, half_min=2.5, step_s=4.0):
    """Best magnitude near jd_guess **with the Sun still up**.

    A fine scan rather than a golden section, and that is deliberate. The first
    version of this function used golden-section search on magnitude alone, and
    it was wrong: for an eclipse still in progress at sunset the unconstrained
    maximum lies *below the horizon*, so the search walked past sunset and
    reported a magnitude nobody could have seen. Eight sites gained more than
    0.01 that way, the worst 0.0735, and every one of them had the Sun below
    -0.9 degrees at the "improved" instant. The original canon's altitude filter
    was right and the fix broke it.

    A 4-second scan bounds the residual cusp error at about 0.0005, well below
    anything that matters, and cannot leave the visible window.
    """
    n = int(2 * half_min * 60 / step_s) + 1
    best = None
    for i in range(n):
        t = jd_guess + (-half_min * 60 + i * step_s) / 86400.0
        c = local_circumstances(SkyState(t), site, dt)
        if c["alt"] < MIN_SUN_ALT:
            continue
        if best is None or c["mag"] > best["mag"]:
            best = c
    return best


def main():
    rows = list(csv.DictReader(open(CANON)))
    fields = list(rows[0].keys())
    shutil.copy(CANON, CANON.replace(".csv", "_pre_refinement.csv"))

    by_name = {s.name: s for s in SITES}
    touched = 0
    promoted = []
    biggest = 0.0
    for r in rows:
        dt_c = float(r["delta_t_central_s"])
        jd = float(r["jd_tt"])
        for name, site in by_name.items():
            key = name + "_mag_central"
            try:
                old = float(r[key])
            except (TypeError, ValueError):
                continue
            if old < THRESHOLD:
                continue
            # The grid peak time is not stored, so re-scan coarsely then refine.
            best_t, best_m = None, -1.0
            for i in range(-120, 121):
                t = jd + i * (2.0 / 1440.0)
                c0 = local_circumstances(SkyState(t), site, dt_c)
                if c0["alt"] < MIN_SUN_ALT:
                    continue
                if c0["mag"] > best_m:
                    best_t, best_m = t, c0["mag"]
            if best_t is None:
                continue
            c = refine(best_t, site, dt_c)
            if c is None:
                continue
            new = c["mag"]
            if new > old + 1e-6:
                touched += 1
                biggest = max(biggest, new - old)
                if old < 1.0 <= new:
                    promoted.append((r["date_julian_cal"], name, old, new))
                r[key] = round(new, 4)
                r[name + "_alt_central"] = round(c["alt"], 1)
        for k, agg in (("irish_mag_central", "_mag_central"),):
            r[k] = round(max(float(r[s + agg]) for s in IRISH), 4)

    with open(CANON, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print("refined %d site-magnitudes at or above %.2f" % (touched, THRESHOLD))
    print("largest single correction: +%.4f in magnitude" % biggest)
    if promoted:
        print("\ncrossed the central threshold (were reported as deep partial, "
              "are actually total or annular):")
        for d, s, o, n in promoted:
            print("  %s  %-14s %.4f -> %.4f" % (d, s, o, n))
    else:
        print("\nno eclipse crossed the central threshold")
    print("\npre-refinement canon kept at results/eclipse_canon_pre_refinement.csv")


if __name__ == "__main__":
    main()
