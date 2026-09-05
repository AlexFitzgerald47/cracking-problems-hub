"""Pipeline checks for astro.py.

Rule of the Hub: if you cannot recover what is already known, you have a bug and
not a discovery.  These check the calendar, the sidereal time, the two analytic
theories and the end-to-end eclipse geometry against published values.
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (julian_day, calendar_date, weekday, gmst_deg, SkyState, Site,
                   local_circumstances, delta_t_ms2004)

FAILS = []


def check(name, got, want, tol, unit=""):
    ok = abs(got - want) <= tol
    print("%-58s %14.6f vs %14.6f  %s%s" %
          (name, got, want, "OK" if ok else "FAIL", (" " + unit) if unit else ""))
    if not ok:
        FAILS.append(name)


def main():
    print("== calendar (Meeus ch.7 worked examples) ==")
    check("JD 2000-01-01.5 Gregorian", julian_day(2000, 1, 1.5), 2451545.0, 1e-9)
    check("JD 1582-10-15.0 Gregorian", julian_day(1582, 10, 15.0), 2299160.5, 1e-9)
    check("JD 1582-10-04.0 Julian", julian_day(1582, 10, 4.0), 2299159.5, 1e-9)
    check("JD 1957-10-04.81 Gregorian", julian_day(1957, 10, 4.81), 2436116.31, 1e-6)
    check("JD 333-01-27.5 Julian", julian_day(333, 1, 27.5), 1842713.0, 1e-9)
    check("JD -4712-01-01.5 Julian", julian_day(-4712, 1, 1.5), 0.0, 1e-9)

    y, m, d = calendar_date(1842713.0)
    check("inverse 1842713 -> year", y, 333, 0)
    check("inverse 1842713 -> month", m, 1, 0)
    check("inverse 1842713 -> day", d, 27.5, 1e-9)
    y, m, d = calendar_date(2436116.31)
    check("inverse 2436116.31 -> year", y, 1957, 0)
    check("inverse 2436116.31 -> day", d, 4.81, 1e-6)

    # 1954 June 30 was a Wednesday (Meeus 7.e)
    check("weekday 1954-06-30 (3=Wed)", weekday(julian_day(1954, 6, 30.0)), 3, 0)

    print("\n== sidereal time (Meeus 12.a) ==")
    # 1987 April 10.0 UT -> mean sidereal time at Greenwich 197.693195 deg
    check("GMST 1987-04-10.0 UT", gmst_deg(2446895.5), 197.693195, 1e-4, "deg")

    print("\n== solar theory (Meeus 25.b, 1992 Oct 13.0 TD) ==")
    st = SkyState(julian_day(1992, 10, 13.0))
    # apparent longitude 199 deg 54' 21.56" ; radius vector 0.99760775 AU
    import astro
    from pymeeus.Epoch import Epoch
    from pymeeus.Sun import Sun
    lon, lat, r = Sun.apparent_geocentric_position(Epoch(julian_day(1992, 10, 13.0)))
    check("Sun apparent longitude", float(lon), 199.90599, 3e-4, "deg")
    check("Sun radius vector", float(r), 0.99760775, 1e-6, "AU")

    print("\n== lunar theory (Meeus 47.a, 1992 Apr 12.0 TD) ==")
    from pymeeus.Moon import Moon
    L, B, D, P = Moon.apparent_ecliptical_pos(Epoch(julian_day(1992, 4, 12.0)))
    check("Moon apparent longitude", float(L), 133.167265, 5e-4, "deg")
    check("Moon latitude", float(B), -3.229126, 5e-4, "deg")
    check("Moon distance", float(D), 368409.7, 2.0, "km")
    check("Moon equatorial parallax", float(P), 0.991990, 1e-4, "deg")

    print("\n== end-to-end eclipse geometry: modern eclipses with known truth ==")
    # 2017 Aug 21 total solar eclipse. Greatest eclipse 18:26:40 TD (dT = 68.9 s),
    # at 36.97 N, 87.65 W; magnitude 1.0306.
    jd = julian_day(2017, 8, 21) + (18 + 26 / 60.0 + 40 / 3600.0) / 24.0
    st = SkyState(jd)
    site = Site("greatest-2017", 36.9754, -87.6551)
    c = local_circumstances(st, site, 68.9)
    check("2017-08-21 magnitude at greatest", c["mag"], 1.0306, 0.001)
    check("2017-08-21 Sun altitude at greatest", c["alt"], 63.8, 0.6, "deg")

    # 1999 Aug 11 total solar eclipse. Greatest 11:03:04 TD (dT = 63.7 s),
    # 45.10 N, 24.30 E; magnitude 1.0286.
    jd = julian_day(1999, 8, 11) + (11 + 3 / 60.0 + 4 / 3600.0) / 24.0
    st = SkyState(jd)
    site = Site("greatest-1999", 45.1, 24.3)
    c = local_circumstances(st, site, 63.7)
    check("1999-08-11 magnitude at greatest", c["mag"], 1.0286, 0.001)

    # 2015 Mar 20 total solar eclipse; greatest 09:46:47 TD (dT = 67.9 s),
    # 64.43 N, 6.63 W; magnitude 1.0445.
    jd = julian_day(2015, 3, 20) + (9 + 46 / 60.0 + 47 / 3600.0) / 24.0
    st = SkyState(jd)
    site = Site("greatest-2015", 64.4333, -6.6333)
    c = local_circumstances(st, site, 67.9)
    check("2015-03-20 magnitude at greatest", c["mag"], 1.0445, 0.001)

    print("\n== gamma (least distance of shadow axis from Earth centre) ==")
    from astro import gamma
    for label, (Y, M, D, h, mi, sec), want in [
            ("2017-08-21", (2017, 8, 21, 18, 26, 40), 0.4367),
            ("1999-08-11", (1999, 8, 11, 11, 3, 4), 0.5062),
            ("2015-03-20", (2015, 3, 20, 9, 46, 47), 0.9454)]:
        jdg = julian_day(Y, M, D) + (h + mi / 60.0 + sec / 3600.0) / 24.0
        check("gamma " + label, gamma(SkyState(jdg)), want, 0.002)

    # Negative control: an ordinary new moon with no eclipse anywhere.
    jd = julian_day(2016, 4, 7) + 11.5 / 24.0
    st = SkyState(jd)
    check("2016-04-07 no-eclipse elongation > 1.6 deg",
          1.0 if st.elongation() > 1.6 else 0.0, 1.0, 0.0)

    print("\n== Delta-T parabola ==")
    check("dT(1820)", delta_t_ms2004(1820), -20.0, 1e-9, "s")
    check("dT(2000)", delta_t_ms2004(2000), 83.68, 0.01, "s")

    print("")
    if FAILS:
        print("FAILURES: %d" % len(FAILS))
        for f in FAILS:
            print("  - " + f)
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
