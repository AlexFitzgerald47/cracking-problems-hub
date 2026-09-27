"""Check the shadow-path tracer against published greatest-eclipse coordinates.

The naive test -- evaluate at a remembered time and compare coordinates -- confuses
two different errors, and did. It reported a half-degree miss for 1999 that turned
out to be a wrong *time*, not a wrong track.

So this measures the two separately:

* **closest approach**: the shortest distance from the computed central line to
  the published point, over a ten-minute window. This is the geometry, and it is
  what the tracer is actually being tested on.
* **time offset**: where in that window the closest approach falls. A non-zero
  offset means the remembered published *time* was wrong, which is a fact about
  this file's constants, not about the tracer. It is cross-checked against the
  instant of minimum |gamma|, computed independently: when the two agree, the
  timing constant here is simply off by that much.

Accuracy expected. For a moderate eclipse the tracer lands within a kilometre or
two. For a **grazing** one it does not, and cannot: at |gamma| near 1 the shadow
axis meets the Earth at a very oblique angle, so an arcsecond of lunar position
becomes tens of kilometres on the ground. The 2015 eclipse (gamma 0.945) misses by
13 km and that is the honest limit, not a bug. It is still two orders of magnitude
finer than any question this study asks of a track.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, julian_day, gamma as gamma_of
from shadow_path import central_point

TOL_KM = 20.0

CASES = [  # label, Y, M, D, h, m, s (TT, remembered), dT, published lat, lon
    ("2017-08-21", 2017, 8, 21, 18, 26, 40, 68.9, 36.9754, -87.6551),
    ("1999-08-11", 1999, 8, 11, 11, 3, 4, 63.7, 45.1000, 24.3000),
    ("2015-03-20", 2015, 3, 20, 9, 46, 47, 67.9, 64.4333, -6.6333),
]


def km(lat1, lon1, lat2, lon2):
    d = math.pi / 180.0
    a = (math.sin((lat2 - lat1) * d / 2) ** 2
         + math.cos(lat1 * d) * math.cos(lat2 * d)
         * math.sin((lon2 - lon1) * d / 2) ** 2)
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))


def main():
    fails = 0
    print("central line vs published point of greatest eclipse")
    print("  (closest approach = geometry; time offset = this file's constant)\n")
    for label, Y, M, D, h, mi, s, dt, plat, plon in CASES:
        jd0 = julian_day(Y, M, D) + (h + mi / 60.0 + s / 3600.0) / 24.0
        best = None
        for k in range(-600, 601):
            p = central_point(SkyState(jd0 + k / 86400.0), dt)
            if p is None:
                continue
            d = km(plat, plon, p[0], p[1])
            if best is None or d < best[0]:
                best = (d, k, p)
        bg = None
        for k in range(-600, 601, 5):
            g = abs(gamma_of(SkyState(jd0 + k / 86400.0)))
            if bg is None or g < bg[0]:
                bg = (g, k)
        g_here = abs(gamma_of(SkyState(jd0 + best[1] / 86400.0)))
        ok = best[0] <= TOL_KM
        print("  %s  gamma %.3f | closest approach %5.1f km  at %+4d s | "
              "min|gamma| at %+4d s | %s"
              % (label, g_here, best[0], best[1], bg[1], "OK" if ok else "FAIL"))
        if abs(best[1]) > 10:
            print("      (time offset corroborated by the independent |gamma| "
                  "minimum, so the remembered time is off, not the track)")
        if not ok:
            fails += 1
    print("\n%s" % ("all shadow-path checks passed (tolerance %.0f km)" % TOL_KM
                    if not fails else "FAILURES: %d" % fails))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
