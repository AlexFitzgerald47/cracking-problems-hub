"""Generate the solar-eclipse canon for the Irish annals window, offline.

Two stages:

1. Walk every lunation in the study window, refine the instant of conjunction in
   apparent longitude, and find the minimum *geocentric* Sun-Moon separation near
   it.  Below ~1.6 degrees the Moon's shadow cone reaches the Earth somewhere.
2. For each such eclipse, sample the four hours either side of that minimum and
   compute topocentric circumstances at a set of sites, for a *grid of Delta-T
   values* rather than a single assumed one.  Delta-T enters only through the
   Earth's rotation angle, so this costs nothing extra: the Sun and Moon are
   computed once per instant and only the observer is re-rotated.

The point of the Delta-T grid is that the first-millennium value is uncertain by
several hundred seconds, which is several degrees of Earth rotation and therefore
the difference between a deep eclipse over Ireland and a shallow one.  Any claim
that survives across the whole grid is safe; any claim that does not is reported
with the Delta-T interval it needs.
"""

import csv
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, local_circumstances, julian_day,
                   calendar_date, weekday, delta_t, delta_t_sigma, gamma)

SYNODIC = 29.530588853
ECLIPSE_GAMMA_LIMIT = 1.5433

SITES = [
    # Irish and Iona annalistic centres
    Site("Armagh", 54.3503, -6.6528),
    Site("Iona", 56.3350, -6.4000),
    Site("Clonmacnoise", 53.3269, -7.9847),
    Site("Bangor", 54.6600, -5.6700),
    # Comparanda: the plausible sources of a *borrowed* notice
    Site("Jarrow", 54.9800, -1.4700),
    Site("Rome", 41.9028, 12.4964),
    Site("Constantinople", 41.0082, 28.9784),
    Site("Alexandria", 31.2001, 29.9187),
]

IRISH = ("Armagh", "Iona", "Clonmacnoise", "Bangor")

# Delta-T grid, as offsets in seconds from the Stephenson, Morrison & Hohenkerk
# (2016) spline.  That determination carries a 1-sigma error of 15-50 s across
# this window, so +/-300 s is roughly +/-7 sigma at the worst year: the grid
# exists to *document* that the results are insensitive to Delta-T, not because
# the uncertainty is large.  60 s is 0.25 degrees of Earth rotation.
DT_OFFSETS = list(range(-300, 301, 60))


def _delta_lon(jd):
    """Apparent longitude of Moon minus Sun, wrapped to (-180, 180]."""
    from pymeeus.Epoch import Epoch
    from pymeeus.Sun import Sun
    from pymeeus.Moon import Moon
    ep = Epoch(jd)
    slon = float(Sun.apparent_geocentric_position(ep)[0])
    mlon = float(Moon.apparent_ecliptical_pos(ep)[0])
    d = (mlon - slon) % 360.0
    if d > 180.0:
        d -= 360.0
    return d


def refine_new_moon(jd_guess):
    """Secant iteration on Moon-Sun apparent longitude difference."""
    t0 = jd_guess
    f0 = _delta_lon(t0)
    t1 = t0 - f0 / 12.19  # deg/day mean elongation rate
    for _ in range(6):
        f1 = _delta_lon(t1)
        if abs(f1) < 1e-6 or abs(f1 - f0) < 1e-12:
            break
        t2 = t1 - f1 * (t1 - t0) / (f1 - f0)
        t0, f0, t1 = t1, f1, t2
    return t1


def greatest_eclipse(jd_conj):
    """Golden-section minimum of |gamma| near conjunction.

    Minimising |gamma| rather than the geocentric angular separation gives the
    instant of *greatest eclipse* as the canons define it, and returns the
    quantity that decides whether an eclipse occurs at all.
    """
    a, b = jd_conj - 0.4, jd_conj + 0.4
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc = abs(gamma(SkyState(c)))
    fd = abs(gamma(SkyState(d)))
    for _ in range(30):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = abs(gamma(SkyState(c)))
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = abs(gamma(SkyState(d)))
    t = (a + b) / 2.0
    st = SkyState(t)
    return t, gamma(st), st.elongation()


def scan_eclipse(jd_min, half_window_h=4.0, step_min=2.0):
    """Topocentric maxima at every site, for every Delta-T on the grid."""
    year = calendar_date(jd_min)[0]
    dt_central = delta_t(year)
    n = int(2 * half_window_h * 60 / step_min) + 1
    step = step_min / 1440.0
    start = jd_min - half_window_h / 24.0

    best = {}
    for i in range(n):
        jd = start + i * step
        st = SkyState(jd)
        # Topocentric separation differs from geocentric by at most the lunar
        # parallax (~1 deg), so instants well outside that band cannot produce an
        # eclipse anywhere and are skipped.
        if st.elongation() > 2.8:
            continue
        for site in SITES:
            for off in DT_OFFSETS:
                c = local_circumstances(st, site, dt_central + off)
                if c["mag"] <= 0.0 or c["alt"] < -0.9:
                    continue
                key = (site.name, off)
                cur = best.get(key)
                if cur is None or c["mag"] > cur["mag"]:
                    best[key] = {"mag": c["mag"], "obsc": c["obsc"],
                                 "alt": c["alt"], "jd": jd}
    return dt_central, best


def main(y0=400, y1=1210, out_dir=None):
    out_dir = out_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "results")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    jd_start = julian_day(y0, 1, 1.0)
    jd_end = julian_day(y1, 1, 1.0)

    t_wall = time.time()
    # Anchor the lunation walk on an actual conjunction inside the window.
    jd = refine_new_moon(jd_start)
    while jd < jd_start:
        jd = refine_new_moon(jd + SYNODIC)

    rows = []
    dt_curves = {}
    n_lun = 0
    while jd < jd_end:
        n_lun += 1
        jd_min, gam, sep = greatest_eclipse(jd)
        # Classical condition for the penumbra to touch the Earth at all.  At
        # this exact threshold the finder returns 228 solar eclipses for
        # 1901-2000, which is NASA's published count for that century (Five
        # Millennium Catalog); see count_check.py.
        if abs(gam) < ECLIPSE_GAMMA_LIMIT:
            year, month, day = calendar_date(jd_min)
            di = int(math.floor(day))
            rec = {
                "jd_tt": round(jd_min, 5),
                "year": year, "month": month, "day": di,
                "date_julian_cal": "%04d-%02d-%02d" % (year, month, di),
                "weekday": weekday(jd_min),
                "gamma": round(gam, 4),
                "geo_sep_deg": round(sep, 4),
            }
            dt_central, best = scan_eclipse(jd_min)
            rec["delta_t_central_s"] = round(dt_central, 1)
            rec["delta_t_sigma_s"] = round(delta_t_sigma(year), 1)
            curves = {}
            for site in SITES:
                mags = [best.get((site.name, off), {"mag": 0.0})["mag"]
                        for off in DT_OFFSETS]
                curves[site.name] = [round(m, 4) for m in mags]
                c0 = best.get((site.name, 0))
                rec[site.name + "_mag_central"] = round(c0["mag"], 4) if c0 else 0.0
                rec[site.name + "_alt_central"] = round(c0["alt"], 1) if c0 else None
                if c0:
                    ut = (c0["jd"] - dt_central / 86400.0)
                    frac = (ut + 0.5) % 1.0
                    rec[site.name + "_ut_central"] = "%02d:%02d" % (
                        int(frac * 24), int((frac * 24 % 1) * 60))
                else:
                    rec[site.name + "_ut_central"] = None
                rec[site.name + "_mag_max_over_dt"] = round(max(mags), 4)
                rec[site.name + "_mag_min_over_dt"] = round(min(mags), 4)
            rec["irish_mag_central"] = round(
                max(rec[s + "_mag_central"] for s in IRISH), 4)
            rec["irish_mag_max_over_dt"] = round(
                max(rec[s + "_mag_max_over_dt"] for s in IRISH), 4)
            rec["irish_mag_min_over_dt"] = round(
                max(rec[s + "_mag_min_over_dt"] for s in IRISH), 4)
            rows.append(rec)
            dt_curves[rec["date_julian_cal"]] = curves
            if len(rows) % 100 == 0:
                sys.stderr.write("  %d eclipses, at %s, %.0fs\n" %
                                 (len(rows), rec["date_julian_cal"],
                                  time.time() - t_wall))
                sys.stderr.flush()
        jd = refine_new_moon(jd + SYNODIC)

    fields = list(rows[0].keys())
    with open(os.path.join(out_dir, "eclipse_canon.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    with open(os.path.join(out_dir, "eclipse_dt_curves.json"), "w") as fh:
        json.dump({"delta_t_offsets_s": DT_OFFSETS,
                   "note": "magnitude at each site as a function of Delta-T "
                           "offset from the Stephenson, Morrison & Hohenkerk "
                           "(2016) spline",
                   "curves": dt_curves}, fh)

    sys.stderr.write("lunations scanned: %d\n" % n_lun)
    sys.stderr.write("eclipses found:    %d\n" % len(rows))
    sys.stderr.write("wall time:         %.0f s\n" % (time.time() - t_wall))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 400, int(a[1]) if len(a) > 1 else 1210)
