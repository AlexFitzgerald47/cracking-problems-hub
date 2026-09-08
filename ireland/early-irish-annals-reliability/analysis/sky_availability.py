"""What an Irish observer could actually have seen, AD 400-1210.

Merges the solar and lunar canons into one dated list of observable events, which
is the denominator the whole "how reliable are the annals?" question needs and
which did not exist in machine-readable form before this session.

The comparison it exists to enable: a lunar eclipse is a far more *available*
event than a solar one. It is visible from the entire night hemisphere rather
than a narrow track, it lasts hours rather than minutes, and it needs no accident
of geography. If the annals record solar eclipses at a markedly higher rate than
lunar ones, the tradition was selecting for portent value rather than logging the
sky. If the rates are similar, it was logging. That is a testable question about
the *motivation* of the record, approaching McCarthy & Breen's eschatological
argument from the opposite direction, and it needs only the annal text plus this
table.

Thresholds are deliberately conservative and are stated with the output, because
the answer depends on them: "observable" is not the same as "would be noticed",
and a reader should be able to move the line and see what happens.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

# A solar eclipse below this magnitude is not obvious to an unaided observer who
# is not looking for it; a partial phase of 0.3 passes unnoticed in daily life.
SOLAR_NOTICEABLE = 0.50
SOLAR_DRAMATIC = 0.90


def load(name):
    with open(os.path.join(RES, name)) as fh:
        return list(csv.DictReader(fh))


def f(r, k):
    v = r.get(k)
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main():
    solar = load("eclipse_canon.csv")
    lunar = load("lunar_eclipse_canon.csv")

    events = []
    for r in solar:
        m = f(r, "irish_mag_central")
        if m < SOLAR_NOTICEABLE:
            continue
        events.append({
            "date_julian_cal": r["date_julian_cal"], "year": int(r["year"]),
            "weekday": r["weekday"], "type": "solar",
            "kind": "central" if m >= 1.0 else ("deep partial" if m >= SOLAR_DRAMATIC
                                                else "partial"),
            "magnitude": round(m, 3),
            "best_site": max(("Armagh", "Iona", "Clonmacnoise", "Bangor"),
                             key=lambda s: f(r, s + "_mag_central")),
            "note": "UT %s at Armagh" % (r.get("Armagh_ut_central") or "-"),
        })
    for r in lunar:
        if r.get("visible_from_ireland") not in ("True", "true", True):
            continue
        um = f(r, "umbral_mag")
        if um <= 0.0:
            continue
        events.append({
            "date_julian_cal": r["date_julian_cal"], "year": int(r["year"]),
            "weekday": r["weekday"], "type": "lunar",
            "kind": "total" if um >= 1.0 else "partial umbral",
            "magnitude": round(um, 3),
            "best_site": r.get("irish_site") or "-",
            "note": "Moon %s deg up, %s of umbral phase in a dark sky"
                    % (r.get("moon_alt_deg"), r.get("frac_umbral_visible")),
        })
    events.sort(key=lambda e: (e["year"], e["date_julian_cal"]))

    out = os.path.join(RES, "observable_sky_events.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(events[0].keys()))
        w.writeheader()
        for e in events:
            w.writerow(e)

    y0 = min(e["year"] for e in events)
    y1 = max(e["year"] for e in events)
    span = y1 - y0 + 1

    def n(t, kinds=None):
        return sum(1 for e in events
                   if e["type"] == t and (kinds is None or e["kind"] in kinds))

    print("Observable astronomical events from Ireland, AD %d-%d" % (y0, y1))
    print("Thresholds: solar magnitude >= %.2f with the Sun up; lunar umbral "
          "phase with the" % SOLAR_NOTICEABLE)
    print("Moon above the horizon and the Sun below -6 deg. Move them and the "
          "counts move.\n")
    print("  solar, magnitude >= %.2f            %4d   (one every %.1f years)"
          % (SOLAR_NOTICEABLE, n("solar"), span / max(1, n("solar"))))
    print("    of which >= %.2f                  %4d" % (
        SOLAR_DRAMATIC, n("solar", ("deep partial", "central"))))
    print("    of which central                 %4d" % n("solar", ("central",)))
    print("  lunar, umbral phase visible        %4d   (one every %.1f years)"
          % (n("lunar"), span / max(1, n("lunar"))))
    print("    of which total                   %4d" % n("lunar", ("total",)))
    print("  TOTAL observable events            %4d   (one every %.1f years)"
          % (len(events), span / len(events)))
    print()
    ratio = n("lunar") / float(max(1, n("solar")))
    print("**A visible umbral lunar eclipse was %.1fx as common as a solar eclipse"
          % ratio)
    print("  of magnitude %.2f or more.** That is the asymmetry the recording-rate"
          % SOLAR_NOTICEABLE)
    print("  test turns on: the annals had far more opportunity to record lunar")
    print("  eclipses than solar ones, so equal counts in the text would mean a")
    print("  strong solar bias, not parity.")
    print()
    print("per century (observable from Ireland):")
    print("  century   solar>=0.50   solar>=0.90   lunar umbral   lunar total")
    for c in sorted(set(e["year"] // 100 for e in events)):
        sub = [e for e in events if e["year"] // 100 == c]
        print("  %3d00s  %11d %13d %14d %13d"
              % (c,
                 sum(1 for e in sub if e["type"] == "solar"),
                 sum(1 for e in sub if e["type"] == "solar"
                     and e["kind"] in ("deep partial", "central")),
                 sum(1 for e in sub if e["type"] == "lunar"),
                 sum(1 for e in sub if e["type"] == "lunar" and e["kind"] == "total")))
    print("\nwrote %s (%d rows)" % (out, len(events)))


if __name__ == "__main__":
    main()
