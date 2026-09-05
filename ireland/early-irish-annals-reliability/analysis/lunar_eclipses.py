"""Umbral lunar-eclipse geometry, added for one record and validated first.

The AU 878 notice ends "fifteen solar days having intervened", i.e. it reports a
*lunar* eclipse a fortnight before the solar one.  That is a fifth independent,
falsifiable element in a record that already states date, feria, luna and hour,
so it is worth the fifty lines.

Geometry (Meeus ch. 54).  At opposition the Moon's angular distance from the
antisolar point is compared with the radius of the Earth's shadow at the Moon's
distance:

    sigma_umbra    = 1.02 * (pi_moon + pi_sun - s_sun)
    sigma_penumbra = 1.02 * (pi_moon + pi_sun + s_sun)

the 1.02 being the conventional enlargement for the Earth's atmosphere.  Umbral
magnitude is then (sigma_umbra + s_moon - beta) / (2 * s_moon).

Validated below against published umbral magnitudes for three modern eclipses
before it is used on anything historical.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, julian_day, calendar_date, DEG, AU_KM,
                   SUN_RADIUS_KM, MOON_RADIUS_KM, EARTH_EQ_RADIUS_KM,
                   _angle, _norm, delta_t)
from find_eclipses import refine_new_moon, SYNODIC

SHADOW_ENLARGEMENT = 1.02


def umbral_circumstances(jd_tt):
    st = SkyState(jd_tt)
    rs, rm = st.sun, st.moon
    ds, dm = _norm(rs), _norm(rm)
    anti = (-rs[0], -rs[1], -rs[2])
    beta = _angle(anti, rm)

    pi_moon = math.asin(EARTH_EQ_RADIUS_KM / dm) / DEG
    pi_sun = math.asin(EARTH_EQ_RADIUS_KM / ds) / DEG
    s_sun = math.asin(SUN_RADIUS_KM / ds) / DEG
    s_moon = math.asin(MOON_RADIUS_KM / dm) / DEG

    umbra = SHADOW_ENLARGEMENT * (pi_moon + pi_sun - s_sun)
    penumbra = SHADOW_ENLARGEMENT * (pi_moon + pi_sun + s_sun)
    return {"beta": beta, "s_moon": s_moon,
            "umbral_mag": (umbra + s_moon - beta) / (2.0 * s_moon),
            "penumbral_mag": (penumbra + s_moon - beta) / (2.0 * s_moon)}


def greatest_lunar_eclipse(jd_full_guess, half_window_d=0.4):
    """Minimise beta near opposition; returns (jd_tt, circumstances)."""
    a, b = jd_full_guess - half_window_d, jd_full_guess + half_window_d
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    c, d = b - gr * (b - a), a + gr * (b - a)
    fc, fd = umbral_circumstances(c)["beta"], umbral_circumstances(d)["beta"]
    for _ in range(30):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - gr * (b - a)
            fc = umbral_circumstances(c)["beta"]
        else:
            a, c, fc = c, d, fd
            d = a + gr * (b - a)
            fd = umbral_circumstances(d)["beta"]
    t = 0.5 * (a + b)
    return t, umbral_circumstances(t)


def full_moon_near(jd):
    """Instant of the full moon nearest jd (half a synodic month from new)."""
    nm = refine_new_moon(jd)
    cands = [nm + SYNODIC / 2.0, nm - SYNODIC / 2.0]
    return min(cands, key=lambda t: abs(t - jd))


def validate():
    fails = []
    # Published umbral magnitudes at greatest eclipse.
    cases = [((2018, 7, 27, 20, 22), 1.6087),
             ((2019, 1, 21, 5, 12), 1.1951),
             ((2015, 9, 28, 2, 47), 1.2764)]
    for (Y, M, D, h, mi), want in cases:
        jd = julian_day(Y, M, D) + (h + mi / 60.0) / 24.0 + 69.0 / 86400.0
        t, c = greatest_lunar_eclipse(jd, 0.1)
        ok = abs(c["umbral_mag"] - want) <= 0.01
        print("  %04d-%02d-%02d umbral magnitude %.4f vs published %.4f  %s"
              % (Y, M, D, c["umbral_mag"], want, "OK" if ok else "FAIL"))
        if not ok:
            fails.append((Y, M, D))
    # Negative control: a full moon with no eclipse.
    jd = full_moon_near(julian_day(2019, 4, 19))
    t, c = greatest_lunar_eclipse(jd)
    ok = c["umbral_mag"] <= 0.0
    print("  2019-04-19 full moon, no umbral eclipse: umbral magnitude %.3f  %s"
          % (c["umbral_mag"], "OK" if ok else "FAIL"))
    if not ok:
        fails.append("negative control")
    return fails


def main():
    print("== validation ==")
    fails = validate()
    if fails:
        print("\nVALIDATION FAILED -- do not use the historical result below")
    print("\n== AU 878: 'fifteen solar days having intervened' ==")
    print("The solar eclipse is 878-10-29 (Julian).  If a lunar eclipse preceded")
    print("it by about a fortnight, it falls at the full moon nearest 878-10-14.")
    jd_solar = julian_day(878, 10, 29) + 0.5
    jd_full = full_moon_near(jd_solar - 15.0)
    t, c = greatest_lunar_eclipse(jd_full)
    y, m, d = calendar_date(t)
    dt = delta_t(y)
    ut = t - dt / 86400.0
    frac = (ut + 0.5) % 1.0
    print("  full moon nearest that date: %04d-%02d-%02d (Julian calendar)"
          % (y, m, int(math.floor(d))))
    print("  greatest eclipse %02d:%02d UT" % (int(frac * 24), int((frac * 24 % 1) * 60)))
    print("  Moon's distance from the antisolar point: %.4f deg" % c["beta"])
    print("  UMBRAL magnitude    %.4f" % c["umbral_mag"])
    print("  penumbral magnitude %.4f" % c["penumbral_mag"])
    interval = jd_solar - t
    print("  interval to the solar eclipse: %.2f days" % interval)


if __name__ == "__main__":
    main()
