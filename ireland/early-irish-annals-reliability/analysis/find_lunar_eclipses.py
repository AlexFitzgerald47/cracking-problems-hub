"""Lunar-eclipse canon AD 400-1210, with Irish visibility.

Why this matters as much as the solar canon: the annals record lunar eclipses
too -- AU 878 records one a fortnight before its solar eclipse -- and a lunar
eclipse is a far more *available* event than a solar one. It is visible from the
entire night hemisphere rather than a narrow track, it lasts hours rather than
minutes, and it needs no accident of geography. So the denominator for "how much
of the sky did the annalists record?" is not the 367 solar eclipses with any
Irish partial phase; it is that plus this.

That asymmetry is itself testable. If the annals record solar eclipses at a much
higher rate than lunar ones despite lunar eclipses being commoner and easier,
the recording tradition was selecting for portent value rather than logging the
sky. If the rates are similar, it was logging.

Visibility here means what an observer in Ireland could actually have seen: the
Moon above the horizon *and* the Sun below it, at some point between first and
last umbral contact.
"""

import csv
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, julian_day, calendar_date, weekday, DEG,
                   delta_t, _norm, _sub)
from find_eclipses import refine_new_moon, SYNODIC
from lunar_eclipses import (umbral_circumstances, greatest_lunar_eclipse,
                            refine_full_moon)

SITES = [Site("Armagh", 54.3503, -6.6528),
         Site("Iona", 56.3350, -6.4000),
         Site("Clonmacnoise", 53.3269, -7.9847)]

# Refracted horizon for the Moon's centre, and the Sun far enough down that a
# partial umbral phase is actually discernible (civil twilight).
MOON_HORIZON = -0.5667
SUN_DARK = -6.0


def _alt(state, site, dt, body):
    obs = site.vector(state.jd_tt, dt)
    v = _sub(getattr(state, body), obs)
    up = [x / _norm(obs) for x in obs]
    c = sum(a * b for a, b in zip(up, v)) / _norm(v)
    return 90.0 - math.acos(max(-1.0, min(1.0, c))) / DEG


def contacts(jd_max, half_window_h=3.5, n=85):
    """First and last umbral contact by scan-and-bisect; None if not umbral."""
    step = 2 * half_window_h / 24.0 / (n - 1)
    start = jd_max - half_window_h / 24.0
    mags = [(start + i * step, umbral_circumstances(start + i * step)["umbral_mag"])
            for i in range(n)]
    peak = max(range(n), key=lambda i: mags[i][1])
    if mags[peak][1] <= 0.0:
        return None, None

    def bisect(a, b):
        for _ in range(30):
            m = 0.5 * (a + b)
            if umbral_circumstances(m)["umbral_mag"] > 0.0:
                b = m
            else:
                a = m
        return 0.5 * (a + b)

    first = last = None
    for i in range(peak, 0, -1):
        if mags[i - 1][1] <= 0.0 < mags[i][1]:
            first = bisect(mags[i - 1][0], mags[i][0])
            break
    for i in range(peak, n - 1):
        if mags[i][1] > 0.0 >= mags[i + 1][1]:
            last = bisect(mags[i + 1][0], mags[i][0])
            break
    return first, last


def irish_visibility(jd_first, jd_last, dt, samples=25):
    """Best Moon altitude in a dark sky between the umbral contacts."""
    best = {"site": None, "moon_alt": -90.0, "jd": None, "frac_visible": 0.0}
    for site in SITES:
        seen = 0
        top = -90.0
        top_jd = None
        for i in range(samples):
            jd = jd_first + (jd_last - jd_first) * i / (samples - 1.0)
            st = SkyState(jd)
            malt = _alt(st, site, dt, "moon")
            salt = _alt(st, site, dt, "sun")
            if malt > MOON_HORIZON and salt < SUN_DARK:
                seen += 1
                if malt > top:
                    top, top_jd = malt, jd
        frac = seen / float(samples)
        if top > best["moon_alt"]:
            best = {"site": site.name, "moon_alt": top, "jd": top_jd,
                    "frac_visible": frac}
    return best


def main(y0=400, y1=1210):
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "results")
    jd0, jd1 = julian_day(y0, 1, 1.0), julian_day(y1, 1, 1.0)

    t_wall = time.time()
    jd = refine_full_moon(jd0)
    while jd < jd0:
        jd = refine_full_moon(jd + SYNODIC)

    rows = []
    n_lun = 0
    while jd < jd1:
        n_lun += 1
        t, c = greatest_lunar_eclipse(jd)
        if c["penumbral_mag"] > 0.0:
            year, month, day = calendar_date(t)
            dt = delta_t(year)
            first, last = contacts(t)
            kind = ("total" if c["umbral_mag"] >= 1.0 else
                    "partial umbral" if c["umbral_mag"] > 0.0 else "penumbral")
            rec = {"jd_tt": round(t, 5), "year": year, "month": month,
                   "day": int(math.floor(day)),
                   "date_julian_cal": "%04d-%02d-%02d" % (year, month,
                                                          int(math.floor(day))),
                   "weekday": weekday(t), "kind": kind,
                   "umbral_mag": round(c["umbral_mag"], 4),
                   "penumbral_mag": round(c["penumbral_mag"], 4),
                   "beta_deg": round(c["beta"], 4),
                   "delta_t_s": round(dt, 0)}
            if first is not None and last is not None:
                rec["umbral_duration_h"] = round((last - first) * 24.0, 2)
                v = irish_visibility(first, last, dt)
                rec["irish_site"] = v["site"]
                rec["moon_alt_deg"] = round(v["moon_alt"], 1)
                rec["frac_umbral_visible"] = round(v["frac_visible"], 2)
                rec["visible_from_ireland"] = v["moon_alt"] > MOON_HORIZON
            else:
                rec["umbral_duration_h"] = 0.0
                rec["irish_site"] = None
                rec["moon_alt_deg"] = None
                rec["frac_umbral_visible"] = 0.0
                rec["visible_from_ireland"] = False
            rows.append(rec)
            if len(rows) % 200 == 0:
                sys.stderr.write("  %d lunar eclipses, at %s, %.0fs\n"
                                 % (len(rows), rec["date_julian_cal"],
                                    time.time() - t_wall))
                sys.stderr.flush()
        jd = refine_full_moon(jd + SYNODIC)

    with open(os.path.join(out, "lunar_eclipse_canon.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)

    umbral = [r for r in rows if r["umbral_mag"] > 0.0]
    vis = [r for r in umbral if r["visible_from_ireland"]]
    tot = [r for r in vis if r["umbral_mag"] >= 1.0]
    sys.stderr.write("lunations:                        %d\n" % n_lun)
    sys.stderr.write("lunar eclipses (any penumbral):   %d\n" % len(rows))
    sys.stderr.write("  of which umbral:                %d\n" % len(umbral))
    sys.stderr.write("  umbral AND visible from Ireland:%d\n" % len(vis))
    sys.stderr.write("  total AND visible from Ireland: %d\n" % len(tot))
    sys.stderr.write("wall time: %.0f s\n" % (time.time() - t_wall))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 400, int(a[1]) if len(a) > 1 else 1210)
