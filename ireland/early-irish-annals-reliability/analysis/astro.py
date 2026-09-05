"""Offline solar-eclipse retrocalculation for the Irish annals problem.

No network, no downloaded ephemeris: positions come from the analytic theories in
Meeus, *Astronomical Algorithms* (2nd ed.) as implemented by ``pymeeus`` — full
VSOP87 for the Sun, the abbreviated ELP-2000/82 for the Moon.  Quoted accuracy is
~10" in lunar longitude and ~4" in latitude over the historical range, i.e. well
under 0.01 in eclipse magnitude, and far below the uncertainty contributed by
Delta-T.

Everything here is deliberately explicit rather than delegated:

* calendar handling (Julian before 1582-10-15, Gregorian after) is implemented
  and unit-tested, because the whole problem is about dates;
* Delta-T is a *parameter*, never a hidden constant.  Delta-T enters only through
  the Earth's rotation angle, so for a fixed TT instant the Sun and Moon are
  computed once and the observer is simply re-rotated for each trial Delta-T.
  That makes "for which Delta-T was this eclipse large at Armagh?" cheap to ask.

Angles are degrees, distances kilometres, times Julian Day numbers.
"""

import math
import os

from pymeeus.Epoch import Epoch
from pymeeus.Sun import Sun
from pymeeus.Moon import Moon
from pymeeus.Coordinates import true_obliquity, nutation_longitude

AU_KM = 149597870.7
EARTH_EQ_RADIUS_KM = 6378.14
EARTH_FLATTENING = 1.0 / 298.257
SUN_RADIUS_KM = 696000.0
MOON_RADIUS_KM = 1737.4
DEG = math.pi / 180.0


# --------------------------------------------------------------------------
# Calendar
# --------------------------------------------------------------------------

def julian_day(year, month, day, gregorian=None):
    """JD from a calendar date (day may be fractional).

    ``gregorian=None`` selects the historically-used calendar: Julian up to
    1582 October 4, Gregorian from 1582 October 15.
    """
    if gregorian is None:
        gregorian = (year, month, math.floor(day)) >= (1582, 10, 15)
    y, m = year, month
    if m <= 2:
        y -= 1
        m += 12
    if gregorian:
        a = math.floor(y / 100.0)
        b = 2 - a + math.floor(a / 4.0)
    else:
        b = 0
    return (math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1))
            + day + b - 1524.5)


def calendar_date(jd, gregorian=None):
    """Inverse of :func:`julian_day`; returns (year, month, fractional day)."""
    if gregorian is None:
        gregorian = jd >= 2299160.5
    jd = jd + 0.5
    z = math.floor(jd)
    f = jd - z
    if gregorian:
        alpha = math.floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - math.floor(alpha / 4.0)
    else:
        a = z
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f
    month = e - 1 if e < 14 else e - 13
    year = c - 4716 if month > 2 else c - 4715
    return int(year), int(month), day


def weekday(jd):
    """0 = Sunday ... 6 = Saturday, for the given JD."""
    return int(math.floor(jd + 1.5)) % 7


# --------------------------------------------------------------------------
# Delta-T
# --------------------------------------------------------------------------

def delta_t_ms2004(year):
    """Morrison & Stephenson (2004) long-term parabola, seconds.

    dT = -20 + 32 u^2, u = (year - 1820)/100.  This is the standard first-order
    description of the Earth's tidal deceleration and is the *central* estimate
    used here.  It is not accurate to better than several hundred seconds in the
    first millennium; nothing in this module depends on it being right, because
    Delta-T is always carried as an explicit parameter.
    """
    u = (year - 1820.0) / 100.0
    return -20.0 + 32.0 * u * u


_DT_TABLE = None


def _load_dt_table():
    global _DT_TABLE
    if _DT_TABLE is None:
        import csv
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "results", "delta_t_stephenson2016.csv")
        tab = {}
        with open(path) as fh:
            for row in csv.DictReader(fh):
                tab[int(row["year"])] = (float(row["delta_t_s"]),
                                         float(row["sigma_s"]))
        _DT_TABLE = tab
    return _DT_TABLE


def delta_t(year):
    """Delta-T in seconds: Stephenson, Morrison & Hohenkerk (2016) spline.

    Falls back to the 2004 parabola outside the tabulated range.  See
    make_deltat_table.py for provenance.  Use this, not the parabola: at AD 1000
    they differ by 481 s, which is 2 degrees of Earth rotation.
    """
    tab = _load_dt_table()
    y = int(math.floor(year))
    if y in tab:
        v0 = tab[y][0]
        v1 = tab.get(y + 1, (v0, 0.0))[0]
        return v0 + (v1 - v0) * (year - y)
    return delta_t_ms2004(year)


def delta_t_sigma(year):
    """1-sigma uncertainty on delta_t(), seconds."""
    tab = _load_dt_table()
    y = int(math.floor(year))
    if y in tab:
        return tab[y][1]
    return delta_t_sigma_ms2004(year)


def delta_t_sigma_ms2004(year):
    """Published 1-sigma envelope for the parabola, seconds.

    Morrison & Stephenson (2004) give the standard error of the parabola as
    dT_sigma = 0.8 * u^2 * 100 s  (i.e. 80 u^2).  Used only to set the width of
    the Delta-T scan; results are reported as a function of Delta-T anyway.
    """
    u = (year - 1820.0) / 100.0
    return 80.0 * u * u


# --------------------------------------------------------------------------
# Positions
# --------------------------------------------------------------------------

def _ecl_to_eq(lon_deg, lat_deg, eps_deg):
    lon, lat, eps = lon_deg * DEG, lat_deg * DEG, eps_deg * DEG
    x = math.cos(lat) * math.cos(lon)
    y = math.cos(lat) * math.sin(lon) * math.cos(eps) - math.sin(lat) * math.sin(eps)
    z = math.cos(lat) * math.sin(lon) * math.sin(eps) + math.sin(lat) * math.cos(eps)
    return x, y, z


class SkyState(object):
    """Geocentric equatorial vectors of Sun and Moon at one TT instant."""

    __slots__ = ("jd_tt", "sun", "moon", "eps", "dpsi")

    def __init__(self, jd_tt):
        ep = Epoch(jd_tt)
        slon, slat, srad = Sun.apparent_geocentric_position(ep)
        mlon, mlat, mdist, mppi = Moon.apparent_ecliptical_pos(ep)
        eps = float(true_obliquity(ep))
        self.jd_tt = jd_tt
        self.eps = eps
        self.dpsi = float(nutation_longitude(ep))
        sr = float(srad) * AU_KM
        ux, uy, uz = _ecl_to_eq(float(slon), float(slat), eps)
        self.sun = (sr * ux, sr * uy, sr * uz)
        md = float(mdist)
        vx, vy, vz = _ecl_to_eq(float(mlon), float(mlat), eps)
        self.moon = (md * vx, md * vy, md * vz)

    def elongation(self):
        """Geocentric Sun-Moon angular separation, degrees."""
        return _angle(self.sun, self.moon)


def _angle(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    c = max(-1.0, min(1.0, dot / (na * nb)))
    return math.acos(c) / DEG


def gmst_deg(jd_ut):
    """Greenwich mean sidereal time in degrees, from UT (Meeus 12.4)."""
    t = (jd_ut - 2451545.0) / 36525.0
    theta = (280.46061837 + 360.98564736629 * (jd_ut - 2451545.0)
             + 0.000387933 * t * t - t * t * t / 38710000.0)
    return theta % 360.0


class Site(object):
    """An observing site on the ellipsoid."""

    def __init__(self, name, lat_deg, lon_deg_east, height_m=0.0):
        self.name = name
        self.lat = lat_deg
        self.lon = lon_deg_east
        self.height = height_m
        phi = lat_deg * DEG
        u = math.atan((1.0 - EARTH_FLATTENING) * math.tan(phi))
        h = height_m / 1000.0 / EARTH_EQ_RADIUS_KM
        self.rho_sin = (1.0 - EARTH_FLATTENING) * math.sin(u) + h * math.sin(phi)
        self.rho_cos = math.cos(u) + h * math.cos(phi)

    def vector(self, jd_tt, delta_t_s):
        """Geocentric equatorial rectangular vector of the observer, km."""
        jd_ut = jd_tt - delta_t_s / 86400.0
        lst = (gmst_deg(jd_ut) + self.lon) * DEG
        r_xy = self.rho_cos * EARTH_EQ_RADIUS_KM
        return (r_xy * math.cos(lst), r_xy * math.sin(lst),
                self.rho_sin * EARTH_EQ_RADIUS_KM)


# --------------------------------------------------------------------------
# Local circumstances
# --------------------------------------------------------------------------

def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _norm(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


def local_circumstances(state, site, delta_t_s):
    """Topocentric magnitude, obscuration and Sun altitude at one instant.

    magnitude follows the standard definition (fraction of the solar *diameter*
    covered); obscuration is the covered fraction of the solar *disc area*.
    """
    obs = site.vector(state.jd_tt, delta_t_s)
    ts = _sub(state.sun, obs)
    tm = _sub(state.moon, obs)
    ds, dm = _norm(ts), _norm(tm)
    sep = _angle(ts, tm)
    s_sun = math.asin(SUN_RADIUS_KM / ds) / DEG
    s_moon = math.asin(MOON_RADIUS_KM / dm) / DEG

    # Magnitude convention follows Espenak's canon, which validate_astro.py
    # confirms to +/-0.0005 on three modern eclipses: for a central (total or
    # annular) eclipse the magnitude is the ratio of apparent *diameters*; for a
    # partial eclipse it is the covered fraction of the solar diameter.  The two
    # branches are discontinuous at second contact; that is the convention, not
    # a bug.  Everything Irish in this study is partial, so the second branch is
    # what actually carries the results.
    if sep >= s_sun + s_moon:
        mag = 0.0
    elif sep <= abs(s_moon - s_sun):
        mag = s_moon / s_sun
    else:
        mag = (s_sun + s_moon - sep) / (2.0 * s_sun)

    obsc = _obscuration(sep, s_sun, s_moon)

    # Sun altitude, geometric (no refraction).
    up = (obs[0] / _norm(obs), obs[1] / _norm(obs), obs[2] / _norm(obs))
    cosz = sum(x * y for x, y in zip(up, ts)) / ds
    alt = 90.0 - math.acos(max(-1.0, min(1.0, cosz))) / DEG
    return {"sep": sep, "mag": mag, "obsc": obsc, "alt": alt,
            "s_sun": s_sun, "s_moon": s_moon}


def _obscuration(d, r_s, r_m):
    """Area fraction of the solar disc covered (two overlapping circles)."""
    if d >= r_s + r_m:
        return 0.0
    if d <= r_m - r_s:
        return 1.0
    if d <= r_s - r_m:
        return (r_m / r_s) ** 2
    d2, rs2, rm2 = d * d, r_s * r_s, r_m * r_m
    a1 = math.acos(max(-1.0, min(1.0, (d2 + rs2 - rm2) / (2.0 * d * r_s))))
    a2 = math.acos(max(-1.0, min(1.0, (d2 + rm2 - rs2) / (2.0 * d * r_m))))
    area = (rs2 * (a1 - math.sin(2.0 * a1) / 2.0)
            + rm2 * (a2 - math.sin(2.0 * a2) / 2.0))
    return area / (math.pi * rs2)


def gamma(state):
    """Least distance of the shadow axis from the Earth's centre, in equatorial
    radii, positive north.  This is the quantity tabulated as "gamma" in the
    standard eclipse canons, and it is what decides whether an eclipse happens at
    all: the penumbra misses the Earth entirely beyond |gamma| ~ 1.55.
    """
    rs, rm = state.sun, state.moon
    ax = _sub(rm, rs)
    n = _norm(ax)
    u = (ax[0] / n, ax[1] / n, ax[2] / n)
    proj = sum(a * b for a, b in zip(rm, u))
    p = (rm[0] - proj * u[0], rm[1] - proj * u[1], rm[2] - proj * u[2])
    mag = _norm(p) / EARTH_EQ_RADIUS_KM
    # Sign: north of the axis is positive.  Take the Earth's rotation axis,
    # remove its component along the shadow axis, and compare.
    k = (0.0, 0.0, 1.0)
    kd = k[2] * u[2]
    kp = (-kd * u[0], -kd * u[1], 1.0 - kd * u[2])
    s = sum(a * b for a, b in zip(p, kp))
    return mag if s >= 0 else -mag
