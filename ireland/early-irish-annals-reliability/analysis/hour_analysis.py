"""The AD 664 'ninth hour' crux, as an astronomical constraint.

The Annals of Ulster enter the eclipse at 664 as darkness on the kalends of May
*in nona hora*; Bede (HE III.27) dates the same eclipse to 3 May, *hora circiter
decima*.  The astronomy settles the date outright -- there is no eclipse on 3 May
664 -- but the hour has never been used as a constraint, and it is one, because
the unequal ("canonical") hour a phase falls in is a computable function of
Delta-T alone once the site is fixed.

So this module inverts the question.  Instead of asking "which source has the
right hour?", which cannot be answered without assuming Delta-T, it asks: *for
which values of Delta-T is each source right?*  The answer is a pair of
intervals that can be compared against Delta-T determined independently from
other ancient eclipses.

Hours are counted in the Roman/monastic scheme in use in seventh-century Ireland:
the first hour begins at sunrise, the twelfth ends at sunset, and each is one
twelfth of the actual daylight length, so an hour on 1 May at Armagh is about 78
minutes, not 60.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, local_circumstances, julian_day, DEG,
                   delta_t, delta_t_sigma, gmst_deg, _norm, _sub, _angle)

SITES = {
    "Armagh": Site("Armagh", 54.3503, -6.6528),
    "Iona": Site("Iona", 56.3350, -6.4000),
    "Clonmacnoise": Site("Clonmacnoise", 53.3269, -7.9847),
    "Jarrow": Site("Jarrow", 54.9800, -1.4700),
}

REFRACTED_HORIZON = -0.8333  # standard sunrise/sunset altitude


def sun_altitude(state, site, delta_t_s):
    obs = site.vector(state.jd_tt, delta_t_s)
    ts = _sub(state.sun, obs)
    up = [x / _norm(obs) for x in obs]
    cosz = sum(a * b for a, b in zip(up, ts)) / _norm(ts)
    return 90.0 - math.acos(max(-1.0, min(1.0, cosz))) / DEG


def local_apparent_time(state, site, delta_t_s):
    """Local apparent solar time in hours, from the Sun's true hour angle."""
    jd_ut = state.jd_tt - delta_t_s / 86400.0
    sx, sy, sz = state.sun
    ra = math.atan2(sy, sx) / DEG % 360.0
    lst = (gmst_deg(jd_ut) + site.lon) % 360.0
    h = (lst - ra + 180.0) % 360.0 - 180.0
    return (h / 15.0 + 12.0) % 24.0


def _root(f, a, b, n=40):
    fa = f(a)
    for _ in range(n):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fa < 0) == (fm < 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def daylight_bounds(jd_noon, site, delta_t_s):
    """Sunrise and sunset as local apparent times."""
    def alt(jd):
        return sun_altitude(SkyState(jd), site, delta_t_s) - REFRACTED_HORIZON
    rise = _root(alt, jd_noon - 0.5, jd_noon, 34)
    setj = _root(lambda j: -alt(j), jd_noon, jd_noon + 0.5, 34)
    return (local_apparent_time(SkyState(rise), site, delta_t_s),
            local_apparent_time(SkyState(setj), site, delta_t_s), rise, setj)


def canonical_hour(t_lat, sunrise_lat, sunset_lat):
    """1..12 across daylight, in the unequal-hour scheme; None outside it."""
    if t_lat < sunrise_lat or t_lat > sunset_lat:
        return None
    frac = (t_lat - sunrise_lat) / (sunset_lat - sunrise_lat)
    return min(12, int(frac * 12) + 1)


def eclipse_phases(jd_center, site, delta_t_s, half_window_h=3.0):
    """(first contact, maximum, last contact) as JD_TT, plus peak magnitude."""
    def mag(jd):
        return local_circumstances(SkyState(jd), site, delta_t_s)["mag"]

    n = 145
    step = 2 * half_window_h / 24.0 / (n - 1)
    start = jd_center - half_window_h / 24.0
    samples = [(start + i * step, mag(start + i * step)) for i in range(n)]
    peak_i = max(range(n), key=lambda i: samples[i][1])
    if samples[peak_i][1] <= 0.0:
        return None
    # refine the maximum by ternary search
    a = samples[max(0, peak_i - 1)][0]
    b = samples[min(n - 1, peak_i + 1)][0]
    for _ in range(40):
        m1 = a + (b - a) / 3.0
        m2 = b - (b - a) / 3.0
        if mag(m1) < mag(m2):
            a = m1
        else:
            b = m2
    jd_max = 0.5 * (a + b)
    first = last = None
    for i in range(peak_i, 0, -1):
        if samples[i - 1][1] <= 0.0 < samples[i][1]:
            first = _root(lambda j: mag(j) - 1e-6, samples[i - 1][0], samples[i][0], 34)
            break
    for i in range(peak_i, n - 1):
        if samples[i][1] > 0.0 >= samples[i + 1][1]:
            last = _root(lambda j: -(mag(j) - 1e-6), samples[i][0], samples[i + 1][0], 34)
            break
    return first, jd_max, last, mag(jd_max)


def analyse(year=664, month=5, day=1, dt_offsets=range(-600, 601, 20)):
    jd_noon = julian_day(year, month, day) + 0.5
    dt_c = delta_t(year)
    out = []
    for site_name, site in SITES.items():
        for off in dt_offsets:
            dt = dt_c + off
            sr, ss, _, _ = daylight_bounds(jd_noon, site, dt)
            ph = eclipse_phases(jd_noon + 0.2, site, dt)
            if ph is None:
                continue
            first, jmax, last, peak = ph
            row = {"site": site_name, "delta_t_s": round(dt, 0),
                   "delta_t_offset_s": off,
                   "sunrise_lat": round(sr, 3), "sunset_lat": round(ss, 3),
                   "hour_length_min": round((ss - sr) / 12.0 * 60.0, 1),
                   "peak_mag": round(peak, 4)}
            for label, jd in (("first", first), ("max", jmax), ("last", last)):
                if jd is None:
                    row[label + "_lat"] = None
                    row[label + "_hour"] = None
                    continue
                t = local_apparent_time(SkyState(jd), site, dt)
                row[label + "_lat"] = round(t, 3)
                row[label + "_hour"] = canonical_hour(t, sr, ss)
            out.append(row)
    return out


if __name__ == "__main__":
    import csv
    rows = analyse()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results",
                       "ad664_hour_analysis.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # Report the Delta-T intervals in which each source's hour is correct.
    from astro import delta_t as _dt, delta_t_sigma as _sig
    dt0, sig = _dt(664), _sig(664)
    print("Stephenson et al. (2016) Delta-T at AD 664 = %.0f s +/- %.0f s\n" % (dt0, sig))
    for site in SITES:
        sub = [r for r in rows if r["site"] == site]
        if not sub:
            continue
        print("%s: hour length %.1f min, sunrise %.2f, sunset %.2f LAT"
              % (site, sub[0]["hour_length_min"], sub[0]["sunrise_lat"],
                 sub[0]["sunset_lat"]))
        for phase in ("first", "max", "last"):
            by_hour = {}
            for r in sub:
                by_hour.setdefault(r[phase + "_hour"], []).append(r["delta_t_s"])
            parts = ["hour %s for dT in [%.0f, %.0f]" % (h, min(v), max(v))
                     for h, v in sorted(by_hour.items(), key=lambda kv: (kv[0] is None, kv[0]))]
            print("   %-6s %s" % (phase, "; ".join(parts)))
        at0 = min(sub, key=lambda r: abs(r["delta_t_s"] - dt0))
        print("   at the published Delta-T (%.0f s): first = hour %s, max = hour %s,"
              " last = hour %s, peak magnitude %.3f"
              % (at0["delta_t_s"], at0["first_hour"], at0["max_hour"],
                 at0["last_hour"], at0["peak_mag"]))
        print("")
