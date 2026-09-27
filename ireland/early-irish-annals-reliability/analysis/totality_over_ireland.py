"""Every solar eclipse whose path of totality crossed Ireland, AD 400-1210.

The canon reports magnitude at four monasteries, and on that basis five eclipses
were "central over Ireland". That undercounts the thing that actually matters. The
umbra is a track a few hundred kilometres wide sweeping across the country; it can
cross Munster or Connacht without coming near Armagh, Iona, Clonmacnoise or
Bangor. For the question "how often did an Irishman see the sun go out?" the right
test is whether the shadow touched the island at all, not whether it touched four
particular buildings.

That is a total eclipse *somewhere in Ireland* -- the single most recordable
astronomical event there is, and therefore the sharpest possible probe of whether
the annals were recording the sky.

Method: trace the central line coarsely for every eclipse that has one, keep those
whose track approaches the island, then re-trace those finely. Two-stage because a
fine trace of all 1,930 eclipses would take half an hour and 95% of them are
nowhere near.

The island is represented by a polygon-free bounding test plus a distance to the
nearest of a set of points spread over it -- deliberately crude, because the umbral
half-width is itself 50-150 km and a coastline traced to the kilometre would be
false precision.
"""

import csv
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, julian_day, calendar_date, weekday, delta_t
from shadow_path import central_point, trace
from find_eclipses import refine_new_moon, greatest_eclipse, SYNODIC

# Points spread over the island; distance is taken to the nearest of them.
IRELAND = [(55.20, -7.30), (54.60, -5.90), (54.35, -6.65), (53.90, -6.40),
           (53.35, -6.26), (53.33, -7.98), (53.27, -9.05), (52.66, -8.63),
           (52.27, -7.11), (51.90, -8.47), (51.55, -9.50), (54.27, -8.47),
           (52.83, -6.95), (52.13, -10.27), (54.99, -7.32)]
DALRIATA = [(56.335, -6.40), (56.085, -5.487), (55.60, -6.28)]  # Iona, Dunadd, Islay

NEAR_KM = 900.0     # stage-1 filter: worth a fine trace
HIT_KM = 120.0      # umbral half-width scale: the shadow plausibly touched


def km(lat1, lon1, lat2, lon2):
    d = math.pi / 180.0
    a = (math.sin((lat2 - lat1) * d / 2) ** 2
         + math.cos(lat1 * d) * math.cos(lat2 * d)
         * math.sin((lon2 - lon1) * d / 2) ** 2)
    return 2 * 6371.0 * math.asin(min(1.0, math.sqrt(a)))


def min_dist(track, points):
    best = None
    arg = None
    for _, la, lo in track:
        for pla, plo in points:
            d = km(la, lo, pla, plo)
            if best is None or d < best:
                best, arg = d, (la, lo)
    return best, arg


def main(y0=400, y1=1210):
    here = os.path.dirname(os.path.abspath(__file__))
    jd0, jd1 = julian_day(y0, 1, 1.0), julian_day(y1, 1, 1.0)
    t_wall = time.time()

    jd = refine_new_moon(jd0)
    while jd < jd0:
        jd = refine_new_moon(jd + SYNODIC)

    rows = []
    n_ecl = n_central = 0
    while jd < jd1:
        t, g, _ = greatest_eclipse(jd)
        if abs(g) < 1.5433:
            n_ecl += 1
            dt = delta_t(calendar_date(t)[0])
            coarse = trace(t, dt, half_window_h=3.5, step_min=2.0)
            if coarse:
                n_central += 1
                d, _ = min_dist(coarse, IRELAND)
                if d < NEAR_KM:
                    fine = trace(t, dt, half_window_h=3.5, step_min=1.0 / 3.0)
                    d_ir, p_ir = min_dist(fine, IRELAND)
                    d_dr, _ = min_dist(fine, DALRIATA)
                    if d_ir < HIT_KM or d_dr < HIT_KM:
                        y, m, dd = calendar_date(t)
                        rows.append({
                            "date_julian_cal": "%04d-%02d-%02d"
                                               % (y, m, int(math.floor(dd))),
                            "year": y, "weekday": weekday(t),
                            "gamma": round(g, 4),
                            "central_line_km_from_ireland": round(d_ir, 0),
                            "central_line_km_from_dal_riata": round(d_dr, 0),
                            "nearest_track_lat": round(p_ir[0], 2),
                            "nearest_track_lon": round(p_ir[1], 2),
                            "crossed_ireland": d_ir < HIT_KM,
                            "crossed_dal_riata": d_dr < HIT_KM,
                            "delta_t_s": round(dt, 0)})
        jd = refine_new_moon(jd + SYNODIC)

    fields = ["date_julian_cal", "year", "weekday", "gamma",
              "central_line_km_from_ireland", "central_line_km_from_dal_riata",
              "nearest_track_lat", "nearest_track_lon", "crossed_ireland",
              "crossed_dal_riata", "delta_t_s"]
    out = os.path.join(here, "results", "totality_over_ireland.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    ir = [r for r in rows if r["crossed_ireland"]]
    dr = [r for r in rows if r["crossed_dal_riata"]]
    both = [r for r in rows if r["crossed_ireland"] and r["crossed_dal_riata"]]
    span = y1 - y0
    print("solar eclipses AD %d-%d:                 %d" % (y0, y1 - 1, n_ecl))
    print("  of which central somewhere on Earth:   %d" % n_central)
    print("  path of totality within %.0f km of Ireland:      %d  (one every %.0f years)"
          % (HIT_KM, len(ir), span / max(1, len(ir))))
    print("  path within %.0f km of Iona / Dunadd / Islay:    %d  (one every %.0f years)"
          % (HIT_KM, len(dr), span / max(1, len(dr))))
    print("  both:                                            %d" % len(both))
    print("  Ireland but NOT Dal Riata:                       %d"
          % (len(ir) - len(both)))
    print("  Dal Riata but NOT Ireland:                       %d"
          % (len(dr) - len(both)))
    print()
    print("the eclipses whose totality reached Ireland:")
    for r in ir:
        print("  %s  gamma %+.3f  track at %+.2f N %+.2f E  (%.0f km)"
              % (r["date_julian_cal"], r["gamma"], r["nearest_track_lat"],
                 r["nearest_track_lon"], r["central_line_km_from_ireland"]))
    print("\nwrote %s (%d near-miss and hit rows)" % (out, len(rows)))
    print("wall time %.0f s" % (time.time() - t_wall))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(int(a[0]) if a else 400, int(a[1]) if len(a) > 1 else 1210)
