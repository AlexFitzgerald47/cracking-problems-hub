"""One table: every recordable sky event AD 400-1210, with its evidential value.

This session produced six separate result files, each answering part of the same
question. A future agent with the annal text should not have to join them by hand,
so this merges them into `results/master_events.csv`, one row per event, with a
`diagnostic` column saying what finding that event would support if the annals
turn out to record it -- or fail to.

The `diagnostic` values:

* `borrowed-if-recorded` — the event could not be seen from Ireland at all. Its
  presence in the annals is a borrowing and admits no other reading.
* `local-if-recorded` — visible from Ireland and not from the Mediterranean. Its
  presence supports local observation.
* `totality-in-ireland` — the umbral track crossed the island. The single most
  recordable event there is; **absence** from the annals is as informative as
  presence.
* `blind` — visible from both, or deep in both. Records nothing either way, and
  is included precisely so that nobody mistakes one for evidence.

That last category is the point of the table as much as the first three. Roughly
four fifths of the events are blind, and a study that quietly drops them will
report a hit rate that means nothing.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")


def load(name, key="date_julian_cal"):
    path = os.path.join(RES, name)
    if not os.path.exists(path):
        return {}
    return {r[key]: r for r in csv.DictReader(open(path))}


def main():
    events = list(csv.DictReader(open(os.path.join(RES, "observable_sky_events.csv"))))
    sol_borrow = load("prediction_borrowed.csv")
    sol_local = load("prediction_irish.csv")
    lun_borrow = load("lunar_prediction_borrowed.csv")
    lun_local = load("lunar_prediction_irish.csv")
    totality = {k: v for k, v in load("totality_over_ireland.csv").items()
                if v.get("crossed_ireland") in ("True", "true")}

    # Solar eclipses that were deep over the Mediterranean and invisible from
    # Ireland never appear in observable_sky_events (which is Ireland-only), so
    # they are appended rather than matched.
    out = []
    for e in events:
        d = e["date_julian_cal"]
        diag = "blind"
        why = ""
        if e["type"] == "solar":
            if d in totality:
                diag = "totality-in-ireland"
                why = ("umbral track %s km from the island"
                       % totality[d]["central_line_km_from_ireland"])
            elif d in sol_local:
                diag = "local-if-recorded"
                why = "deep over Ireland, shallow in the Mediterranean"
        else:
            if d in lun_local:
                diag = "local-if-recorded"
                why = "above the Irish horizon, below the Mediterranean one"
        out.append({**e, "diagnostic": diag, "why": why})

    for d, r in sorted(lun_borrow.items()):
        out.append({"date_julian_cal": d, "year": r["year"], "weekday": "",
                    "type": "lunar", "kind": r["kind"],
                    "magnitude": r["umbral_mag"], "best_site": "-",
                    "note": "below the Irish horizon throughout the umbral phase",
                    "diagnostic": "borrowed-if-recorded",
                    "why": "not visible from Ireland; visible from the Mediterranean"})
    for d, r in sorted(sol_borrow.items()):
        out.append({"date_julian_cal": d, "year": r["year"], "weekday": r.get("weekday", ""),
                    "type": "solar", "kind": "partial",
                    "magnitude": r.get("irish_mag_central", "0"), "best_site": "-",
                    "note": "Mediterranean magnitude high, Irish magnitude below 0.20",
                    "diagnostic": "borrowed-if-recorded",
                    "why": "deep in the Mediterranean, effectively invisible from Ireland"})

    out.sort(key=lambda r: (int(float(r["year"])), r["date_julian_cal"]))
    fields = ["date_julian_cal", "year", "weekday", "type", "kind", "magnitude",
              "best_site", "diagnostic", "why", "note"]
    path = os.path.join(RES, "master_events.csv")
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in out:
            w.writerow(r)

    from collections import Counter
    c = Counter(r["diagnostic"] for r in out)
    t = Counter((r["type"], r["diagnostic"]) for r in out)
    print("master_events.csv: %d rows\n" % len(out))
    print("  %-24s %5s  %7s %7s" % ("diagnostic", "all", "solar", "lunar"))
    for k in ("totality-in-ireland", "borrowed-if-recorded", "local-if-recorded",
              "blind"):
        print("  %-24s %5d  %7d %7d"
              % (k, c[k], t[("solar", k)], t[("lunar", k)]))
    dec = sum(c[k] for k in ("totality-in-ireland", "borrowed-if-recorded",
                             "local-if-recorded"))
    print("\n  decisive one way or another: %d of %d (%.0f%%)"
          % (dec, len(out), 100.0 * dec / len(out)))
    print("  blind: %d (%.0f%%) -- a record of any of these settles nothing"
          % (c["blind"], 100.0 * c["blind"] / len(out)))


if __name__ == "__main__":
    main()
