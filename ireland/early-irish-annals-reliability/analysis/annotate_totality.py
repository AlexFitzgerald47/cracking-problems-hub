"""Add the Sun's altitude to the totality catalogue.

`totality_over_ireland.py` answers "did the umbral track cross Ireland?" and that
was not enough. The 661-07-02 eclipse put totality across Clare and Limerick, but
at **6.5 degrees of solar altitude at 04:56 UT** -- darkness at dawn, with the Sun
barely clear of the horizon.

That changes what an absence from the annals means. A total eclipse at 50 degrees
altitude on a summer afternoon is unmissable and its omission is evidence about
the record. One at 6 degrees, minutes after sunrise, can be lost to terrain, haze
or cloud, and its omission is evidence about the weather. The two must not be
counted together, so the catalogue carries the altitude and any argument built on
it has to say which kind of event it is using.

Run after totality_over_ireland.py; rewrites the CSV in place with two columns
added.
"""

import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import SkyState, Site, julian_day, delta_t, DEG, _norm, _sub
from find_eclipses import refine_new_moon, greatest_eclipse

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results",
                    "totality_over_ireland.csv")


def sun_alt(state, site, dt):
    obs = site.vector(state.jd_tt, dt)
    v = _sub(state.sun, obs)
    up = [x / _norm(obs) for x in obs]
    c = sum(a * b for a, b in zip(up, v)) / _norm(v)
    return 90.0 - math.acos(max(-1.0, min(1.0, c))) / DEG


def main():
    rows = list(csv.DictReader(open(PATH)))
    for r in rows:
        y, m, d = [int(x) for x in r["date_julian_cal"].split("-")]
        t, _, _ = greatest_eclipse(refine_new_moon(julian_day(y, m, d)))
        dt = delta_t(y)
        site = Site("track", float(r["nearest_track_lat"]),
                    float(r["nearest_track_lon"]))
        # altitude at the instant the track is nearest the island: scan the
        # window for the closest approach time rather than assuming greatest
        # eclipse, since they differ for a track that only clips the island.
        best = None
        for i in range(-420, 421):
            jd = t + i * (30.0 / 86400.0)
            st = SkyState(jd)
            from shadow_path import central_point
            p = central_point(st, dt)
            if p is None:
                continue
            dd = math.hypot(p[0] - site.lat, (p[1] - site.lon)
                            * math.cos(site.lat * DEG))
            if best is None or dd < best[0]:
                best = (dd, jd, st)
        alt = sun_alt(best[2], site, dt) if best else None
        r["sun_alt_at_track_deg"] = round(alt, 1) if alt is not None else ""
        r["conspicuousness"] = ("high" if alt is not None and alt >= 25 else
                                "moderate" if alt is not None and alt >= 12 else
                                "low (near the horizon)")
    fields = list(rows[0].keys())
    with open(PATH, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("annotated %d rows" % len(rows))
    hits = [r for r in rows if r["crossed_ireland"] in ("True", "true")]
    print("\ntotality over Ireland, with how conspicuous it was:")
    for r in sorted(hits, key=lambda r: int(r["year"])):
        print("  %s  track %+.2f N %+.2f E  Sun %5s deg  %s"
              % (r["date_julian_cal"], float(r["nearest_track_lat"]),
                 float(r["nearest_track_lon"]), r["sun_alt_at_track_deg"],
                 r["conspicuousness"]))


if __name__ == "__main__":
    main()
