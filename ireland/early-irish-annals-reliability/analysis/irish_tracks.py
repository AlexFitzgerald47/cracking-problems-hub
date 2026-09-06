"""The central line on the ground for the eclipses that matter to this problem.

Settles handover item 6 -- where the 878 track actually ran -- by computing it
rather than looking it up, and does the same for every solar eclipse that was
central over Ireland in the study window.

Accuracy, from validate_shadow_path.py: about 1 km at moderate gamma, degrading
to roughly 13 km for a grazing eclipse. Every question asked here is at the scale
of hundreds of kilometres, so the tracer is far finer than it needs to be.

Delta-T caveat, and it is the real one: longitude is Delta-T-dependent. 300 s
slides the whole track 1.25 degrees of longitude, about 80 km at Irish latitudes.
The Stephenson spline gives 15-50 sigma in this window, so the track is good to
about 10 km from that source -- but a reader who prefers a different Delta-T should
shift the longitudes by 0.00417 degrees per second and re-read.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, local_circumstances, julian_day, delta_t,
                   delta_t_sigma, gamma as gamma_of)
from shadow_path import central_point, trace
from find_eclipses import refine_new_moon, greatest_eclipse, SYNODIC

SITES = {"Armagh": (54.3503, -6.6528), "Bangor (Down)": (54.6600, -5.6700),
         "Iona": (56.3350, -6.4000), "Clonmacnoise": (53.3269, -7.9847),
         "Jarrow": (54.9800, -1.4700), "Dunadd": (56.0847, -5.4869)}

CASES = [(594, 7, 23), (664, 5, 1), (878, 10, 29), (885, 6, 16),
         (1133, 8, 2), (1140, 3, 20)]


def km(lat1, lon1, lat2, lon2):
    d = math.pi / 180.0
    a = (math.sin((lat2 - lat1) * d / 2) ** 2
         + math.cos(lat1 * d) * math.cos(lat2 * d)
         * math.sin((lon2 - lon1) * d / 2) ** 2)
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))


def main():
    for y, m, d in CASES:
        jd_seed = refine_new_moon(julian_day(y, m, d))
        t, g, _ = greatest_eclipse(jd_seed)
        dt = delta_t(y)
        # 20-second sampling. At 4 minutes the shadow moves roughly 240 km
        # between samples, which quantises every distance below by up to 120 km --
        # enough to have made Jarrow look 269 km from the 664 track when the true
        # figure is 186 km. Resolution of a derived quantity is part of the
        # measurement, not a detail.
        tr = trace(t, dt, half_window_h=3.5, step_min=1.0 / 3.0)
        print("=" * 74)
        print("%04d-%02d-%02d   gamma %+.4f   Delta-T %.0f +/- %.0f s"
              % (y, m, d, g, dt, delta_t_sigma(y)))
        if not tr:
            print("  the shadow axis misses the Earth: partial everywhere")
            continue
        # the portion of the track nearest the British Isles
        near = min(tr, key=lambda r: km(54.5, -6.0, r[1], r[2]))
        print("  central line spans lat %+.1f to %+.1f, lon %+.1f to %+.1f"
              % (min(r[1] for r in tr), max(r[1] for r in tr),
                 min(r[2] for r in tr), max(r[2] for r in tr)))
        print("  closest point to the Irish Sea: %+.2f N, %+.2f E" % (near[1], near[2]))
        print("  site: distance from the central line, and what was actually seen")
        rows = []
        for name, (la, lo) in SITES.items():
            dmin = min(km(la, lo, r[1], r[2]) for r in tr)
            site = Site(name, la, lo)
            best = (-1.0, None)
            for i in range(-420, 421):
                c = local_circumstances(SkyState(t + i * (30.0 / 86400.0)), site, dt)
                if c["alt"] < -0.9:
                    continue
                if c["mag"] > best[0]:
                    best = (c["mag"], c)
            c = best[1]
            total = (c is not None
                     and c["sep"] <= abs(c["s_moon"] - c["s_sun"]))
            rows.append((dmin, name, best[0], c["alt"] if c else None, total))
        for dmin, name, mag, alt, total in sorted(rows):
            print("     %-15s %6.0f km   magnitude %.4f   Sun %+5.1f deg   %s"
                  % (name, dmin, mag, alt if alt is not None else float("nan"),
                     "TOTAL" if total else "partial"))
        print("     note: distance from the central line does not decide totality"
              " when the Sun is low --")
        print("     the umbra on the ground is an ellipse that stretches enormously"
              " at low altitude.")
    print("=" * 74)


if __name__ == "__main__":
    main()
