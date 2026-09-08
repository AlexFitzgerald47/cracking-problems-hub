"""Where the shadow actually fell: tracing the central line on the ground.

Handover item 6 was "settle the 878 track", and it was parked on the grounds that
the authoritative path maps sit on hosts the egress policy blocks. That was the
wrong call. The path does not have to be looked up -- it can be computed, from the
same vectors the rest of this engine already produces.

The geometry is a line-ellipsoid intersection. The shadow axis runs from the
centre of the Sun through the centre of the Moon; where it meets the Earth's
surface is the point of central eclipse at that instant, and tracking it through
the eclipse traces the central line. The ellipsoid is handled by scaling z by
1/(1-f), which turns it into a sphere, solving there, and scaling back.

Longitude needs the Earth's rotation angle and therefore Delta-T, so the *track*
is Delta-T-dependent even though the *time* is not -- 300 s of Delta-T slides the
whole path 1.25 degrees west. Latitude is nearly unaffected. That is exactly why
the historical-regime checks in validate_historical.py matter: they are what
licenses trusting a computed track in the ninth century.
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, local_circumstances, julian_day, gmst_deg,
                   calendar_date, delta_t, DEG, EARTH_EQ_RADIUS_KM,
                   EARTH_FLATTENING, _norm, _sub)

F = EARTH_FLATTENING
E2 = 2.0 * F - F * F


def central_point(state, delta_t_s):
    """Geodetic (lat, lon_east) where the shadow axis meets the Earth, or None.

    None means the axis misses the Earth entirely -- a partial eclipse everywhere.
    """
    rs, rm = state.sun, state.moon
    ax = _sub(rm, rs)
    n = _norm(ax)
    u = (ax[0] / n, ax[1] / n, ax[2] / n)

    # Scale z so the ellipsoid becomes a sphere of radius EARTH_EQ_RADIUS_KM.
    k = 1.0 / (1.0 - F)
    p0 = (rm[0], rm[1], rm[2] * k)
    d = (u[0], u[1], u[2] * k)

    a = d[0] * d[0] + d[1] * d[1] + d[2] * d[2]
    b = 2.0 * (p0[0] * d[0] + p0[1] * d[1] + p0[2] * d[2])
    c = (p0[0] * p0[0] + p0[1] * p0[1] + p0[2] * p0[2]
         - EARTH_EQ_RADIUS_KM * EARTH_EQ_RADIUS_KM)
    disc = b * b - 4.0 * a * c
    if disc < 0.0:
        return None
    s = (-b - math.sqrt(disc)) / (2.0 * a)   # near side, toward the Moon
    x = rm[0] + s * u[0]
    y = rm[1] + s * u[1]
    z = rm[2] + s * u[2]

    jd_ut = state.jd_tt - delta_t_s / 86400.0
    lon = (math.atan2(y, x) / DEG - gmst_deg(jd_ut) + 180.0) % 360.0 - 180.0
    lat = math.atan2(z, (1.0 - E2) * math.sqrt(x * x + y * y)) / DEG
    return lat, lon


def trace(jd_greatest, delta_t_s, half_window_h=2.5, step_min=5.0):
    """The central line: (jd, lat, lon) while the axis touches the Earth."""
    out = []
    n = int(2 * half_window_h * 60 / step_min) + 1
    for i in range(n):
        jd = jd_greatest + (-half_window_h * 60 + i * step_min) / 1440.0
        p = central_point(SkyState(jd), delta_t_s)
        if p is not None:
            out.append((jd, p[0], p[1]))
    return out


def nearest_approach(track, lat, lon):
    """Great-circle distance, km, from a site to the closest point of the track."""
    best = None
    for _, la, lo in track:
        dlat = (la - lat) * DEG
        dlon = (lo - lon) * DEG
        m = math.sin(dlat / 2) ** 2 + math.cos(la * DEG) * math.cos(lat * DEG) \
            * math.sin(dlon / 2) ** 2
        dist = 2 * 6371.0 * math.asin(min(1.0, math.sqrt(m)))
        if best is None or dist < best:
            best = dist
    return best
