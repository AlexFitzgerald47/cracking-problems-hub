"""The borrowing test, run on lunar eclipses instead of solar ones.

The solar version of this test is blind on 40% of candidates, because a big
eclipse over Ireland is often a fair-sized one over Rome as well (RESULTS.md §4).
Lunar eclipses fail differently and usefully: the *event* is identical everywhere
it can be seen, so depth carries no information at all -- but **visibility does**,
because it depends on whether the Moon is above your horizon at the time, and
Ireland and Constantinople are 36 degrees of longitude apart, more than two hours
of Earth rotation.

So the lunar discriminator is cleaner than the solar one. It is not "was it
deeper here?", which invites judgement, but "could it be seen from here at all?",
which is a yes or no. A notice of a lunar eclipse that was below the Irish horizon
throughout, in an annal whose other astronomy is demonstrably local, is a
borrowing with no room for argument.

Reads the canon rather than recomputing it. Contacts are reconstructed as
maximum +/- half the umbral duration, which is accurate to well under a minute
because an umbral eclipse is very nearly symmetric in time about greatest phase --
far below what a visibility test at a 25-sample resolution can resolve.
"""

import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, Site, DEG, _norm, _sub
from find_lunar_eclipses import MOON_HORIZON, SUN_DARK, _alt

HERE = os.path.dirname(os.path.abspath(__file__))

IRISH = [Site("Armagh", 54.3503, -6.6528), Site("Iona", 56.3350, -6.4000)]
MED = [Site("Rome", 41.9028, 12.4964), Site("Constantinople", 41.0082, 28.9784)]


def visible(jd_first, jd_last, sites, dt, samples=21):
    for site in sites:
        for i in range(samples):
            jd = jd_first + (jd_last - jd_first) * i / (samples - 1.0)
            st = SkyState(jd)
            if (_alt(st, site, dt, "moon") > MOON_HORIZON
                    and _alt(st, site, dt, "sun") < SUN_DARK):
                return True
    return False


def main():
    rows = [r for r in csv.DictReader(
        open(os.path.join(HERE, "results", "lunar_eclipse_canon.csv")))
        if float(r["umbral_mag"] or 0.0) > 0.0]
    out = []
    for r in rows:
        jd = float(r["jd_tt"])
        dur = float(r["umbral_duration_h"] or 0.0) / 24.0
        if dur <= 0:
            continue
        dt = float(r["delta_t_s"])
        a, b = jd - dur / 2.0, jd + dur / 2.0
        ir = visible(a, b, IRISH, dt)
        me = visible(a, b, MED, dt)
        out.append({"date_julian_cal": r["date_julian_cal"], "year": r["year"],
                    "kind": r["kind"], "umbral_mag": r["umbral_mag"],
                    "visible_ireland": ir, "visible_mediterranean": me})

    n = len(out)
    ir = sum(1 for r in out if r["visible_ireland"])
    me = sum(1 for r in out if r["visible_mediterranean"])
    both = sum(1 for r in out if r["visible_ireland"] and r["visible_mediterranean"])
    only_ir = [r for r in out if r["visible_ireland"] and not r["visible_mediterranean"]]
    only_me = [r for r in out if r["visible_mediterranean"] and not r["visible_ireland"]]

    print("Umbral lunar eclipses AD 400-1210: %d" % n)
    print("  visible from Ireland:                  %4d" % ir)
    print("  visible from Rome or Constantinople:   %4d" % me)
    print("  visible from both (test is blind here):%4d  = %.0f%% of the Irish set"
          % (both, 100.0 * both / max(1, ir)))
    print("  Ireland only  -> diagnostic of local observation:  %3d" % len(only_ir))
    print("  Mediterranean only -> diagnostic of borrowing:     %3d" % len(only_me))
    print()
    print("Compare the solar version (RESULTS.md section 4): 28 decisive cases")
    print("out of 132 candidates, blind on 28. Here the decisive set is %d."
          % (len(only_ir) + len(only_me)))
    print()
    print("The lunar test is also *cleaner*. Depth carries no information -- the")
    print("event is identical wherever it can be seen -- so the discriminator is")
    print("a yes or no about the horizon rather than a judgement about how deep an")
    print("eclipse has to be before someone writes it down.")

    for name, rowset in (("lunar_prediction_borrowed.csv", only_me),
                         ("lunar_prediction_irish.csv", only_ir)):
        with open(os.path.join(HERE, "results", name), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
            w.writeheader()
            for r in rowset:
                w.writerow(r)
    print("\nwrote lunar_prediction_borrowed.csv (%d), lunar_prediction_irish.csv (%d)"
          % (len(only_me), len(only_ir)))


if __name__ == "__main__":
    main()
