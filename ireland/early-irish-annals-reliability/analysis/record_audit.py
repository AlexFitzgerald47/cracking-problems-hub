"""Audit each annalistic eclipse notice against the computed sky.

Every record in annal_records.csv carries some combination of a date, a weekday
(feria), an age of the moon (luna) and an hour of the day.  Each of those is an
independent, falsifiable claim, and each is computable here.  The AU 878 notice
carries all four at once and is therefore the single strongest test on the board:
a record that gets date, weekday, lunar age and hour simultaneously right is very
hard to explain as a borrowing or a back-calculation.

What is *not* claimed: that the wording in annal_records.csv is correct.  Network
egress in the session that built this file blocked celt.ucc.ie and every other
text repository, so the quotations are at search-engine level and are marked as
such.  The astronomy below is independent of them -- it depends only on the dates
-- but any conclusion drawn from the wording inherits that debt.
"""

import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astro import (SkyState, Site, local_circumstances, julian_day, weekday,
                   calendar_date, delta_t, delta_t_sigma, gamma)
from hour_analysis import (SITES, daylight_bounds, canonical_hour,
                           eclipse_phases, local_apparent_time)
from find_eclipses import refine_new_moon

WEEKDAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday"]


def true_lunar_age(jd):
    """Days since the last true conjunction of Sun and Moon."""
    t = refine_new_moon(jd)
    while t > jd:
        t = refine_new_moon(t - 29.530588853)
    return jd - t


def audit(rec, dt_offsets=(-120, 0, 120)):
    y, m, d = [int(x) for x in rec["claimed_date_julian"].split("-")]
    jd_noon = julian_day(y, m, d) + 0.5
    dt0 = delta_t(y)
    out = {"id": rec["id"], "annal": rec["annal"],
           "date": rec["claimed_date_julian"],
           "delta_t_s": round(dt0, 0), "delta_t_sigma_s": round(delta_t_sigma(y), 0)}

    # Weekday (feria: 1 = Sunday, so feria 4 = Wednesday)
    wd = weekday(jd_noon)
    out["computed_weekday"] = WEEKDAY_NAMES[wd]
    out["computed_feria"] = wd + 1
    if rec["claimed_weekday"]:
        out["feria_ok"] = (int(rec["claimed_weekday"]) == wd + 1)

    # Was there an eclipse at all, and how deep in Ireland?
    st = SkyState(jd_noon)
    best = None
    for site_name in ("Armagh", "Iona", "Clonmacnoise"):
        site = SITES[site_name]
        ph = eclipse_phases(jd_noon, site, dt0, half_window_h=8.0)
        if ph is None:
            continue
        first, jmax, last, peak = ph
        sr, ss, _, _ = daylight_bounds(jd_noon, site, dt0)
        row = {"site": site_name, "peak_mag": round(peak, 4)}
        for label, jd in (("first", first), ("max", jmax), ("last", last)):
            if jd is None:
                row[label + "_hour"] = None
                continue
            t = local_apparent_time(SkyState(jd), site, dt0)
            row[label + "_lat"] = round(t, 3)
            row[label + "_hour"] = canonical_hour(t, sr, ss)
        row["lunar_age_days"] = round(true_lunar_age(jmax), 3)
        out.setdefault("sites", []).append(row)
        if best is None or peak > best["peak_mag"]:
            best = row
    out["eclipse_in_ireland"] = best is not None
    if best:
        out["best_site"] = best["site"]
        out["peak_mag_ireland"] = best["peak_mag"]
        out["lunar_age_days"] = best["lunar_age_days"]
        if rec["claimed_hour"]:
            ch = int(rec["claimed_hour"])
            out["claimed_hour"] = ch
            out["hour_matches_phase"] = [
                p for p in ("first", "max", "last")
                if best.get(p + "_hour") == ch] or ["none"]
            # Weaker but fairer test: did the claimed hour fall anywhere inside
            # the eclipse?  An unequal hour is 45-80 minutes wide depending on
            # the season, so "about the Nth hour" is a coarse instrument and
            # asking it to name the exact contact is asking too much of it.
            fh_, lh_ = best.get("first_hour"), best.get("last_hour")
            out["hour_within_eclipse"] = (
                fh_ is not None and lh_ is not None and fh_ <= ch <= lh_)
        if rec["claimed_luna"]:
            out["claimed_luna"] = int(rec["claimed_luna"])
            # luna N on the day of conjunction means the tabular moon is
            # (30 - N) days behind the true new moon, give or take the
            # convention for luna 1.
            out["luna_minus_true_age"] = round(
                int(rec["claimed_luna"]) - (best["lunar_age_days"] + 30.0) % 30.0, 2)

    # Was it visible in the Mediterranean instead?  This is the borrowing test.
    for site_name in ("Rome", "Constantinople"):
        site = Site(site_name, *{"Rome": (41.9028, 12.4964),
                                 "Constantinople": (41.0082, 28.9784)}[site_name])
        ph = eclipse_phases(jd_noon, site, dt0, half_window_h=8.0)
        out["peak_mag_" + site_name.lower()] = round(ph[3], 4) if ph else 0.0
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    recs = list(csv.DictReader(open(os.path.join(here, "annal_records.csv"))))
    results = [audit(r) for r in recs]
    for r in results:
        print("=" * 72)
        print("%s  (%s, annal date %s)" % (r["id"], r["annal"], r["date"]))
        print("  Delta-T %.0f +/- %.0f s" % (r["delta_t_s"], r["delta_t_sigma_s"]))
        print("  weekday computed: %s (feria %d)%s"
              % (r["computed_weekday"], r["computed_feria"],
                 "" if "feria_ok" not in r else
                 ("  -- claimed feria %s: %s" %
                  (r.get("claimed_feria", "?"), "MATCH" if r["feria_ok"] else "MISMATCH"))))
        if not r["eclipse_in_ireland"]:
            print("  NO SOLAR ECLIPSE VISIBLE FROM IRELAND ON THIS DATE")
        else:
            print("  deepest in Ireland: %s, magnitude %.3f, true lunar age %.2f d"
                  % (r["best_site"], r["peak_mag_ireland"], r["lunar_age_days"]))
            for s in r["sites"]:
                print("     %-14s mag %.3f  first h%s (%.2f)  max h%s (%.2f)  last h%s (%.2f)"
                      % (s["site"], s["peak_mag"], s.get("first_hour"),
                         s.get("first_lat", float("nan")), s.get("max_hour"),
                         s.get("max_lat", float("nan")), s.get("last_hour"),
                         s.get("last_lat", float("nan"))))
            if "claimed_hour" in r:
                print("  claimed hour %d matches phase: %s ; within the eclipse: %s"
                      % (r["claimed_hour"], ", ".join(r["hour_matches_phase"]),
                         "YES" if r.get("hour_within_eclipse") else "NO"))
            if "claimed_luna" in r:
                print("  claimed luna %d; true lunar age %.2f d -> tabular moon runs %+.2f d"
                      % (r["claimed_luna"], r["lunar_age_days"], r["luna_minus_true_age"]))
        print("  Mediterranean control: Rome %.3f, Constantinople %.3f"
              % (r["peak_mag_rome"], r["peak_mag_constantinople"]))

    import json
    with open(os.path.join(here, "results", "record_audit.json"), "w") as fh:
        json.dump(results, fh, indent=1)


if __name__ == "__main__":
    main()
