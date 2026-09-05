"""What the canon says, and how much it can decide.

Two jobs.

1. *Denominator.*  How many solar eclipses were actually observable from Ireland
   in each century of the annalistic window, and how deep?  Nobody can compute a
   recording rate for the annals without this, and it did not exist in machine-
   readable form on this board.

2. *Power.*  The interesting question -- were the early notices observed in
   Ireland or copied from a continental chronicle? -- is only answerable to the
   extent that the two hypotheses predict different eclipses.  They often do not:
   a large eclipse over Ireland is frequently a fair-sized one over Rome as well.
   So this computes the confusion rate directly and emits the two lists on which
   the hypotheses actually part company:

   * prediction_irish.csv -- eclipses deep over Ireland and shallow or absent in
     the Mediterranean.  If the annals were kept by observers, these are the ones
     that should be in them.
   * prediction_borrowed.csv -- eclipses deep over the Mediterranean and
     effectively invisible from Ireland.  Any of these appearing in the annals is
     a borrowing, and one that cannot be explained away.

   Neither list can be checked without the annal text, which the session that
   produced this could not reach.  They are the specification of the experiment,
   priced in advance, so that whoever has the text can run it in an hour.
"""

import csv
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
IRISH = ("Armagh", "Iona", "Clonmacnoise", "Bangor")
MED = ("Rome", "Constantinople", "Alexandria")


def load(path=None):
    path = path or os.path.join(HERE, "results", "eclipse_canon.csv")
    rows = []
    with open(path) as fh:
        for r in csv.DictReader(fh):
            for k, v in list(r.items()):
                if k in ("date_julian_cal",) or k.endswith("_ut_central"):
                    continue
                try:
                    r[k] = float(v) if v not in ("", "None") else None
                except (TypeError, ValueError):
                    pass
            rows.append(r)
    return rows


def med_mag(r):
    return max(r[s + "_mag_central"] or 0.0 for s in MED)


def irish_mag(r):
    return r["irish_mag_central"] or 0.0


def main():
    rows = load()
    n = len(rows)
    print("solar eclipses AD %d-%d anywhere on Earth: %d"
          % (rows[0]["year"], rows[-1]["year"], n))

    print("\n== depth over Ireland (Armagh / Iona / Clonmacnoise / Bangor, "
          "greatest of the four, Sun above the horizon) ==")
    bands = [(0.0, "any partial phase at all"), (0.25, "mag >= 0.25"),
             (0.50, "mag >= 0.50  (noticeable dimming)"),
             (0.80, "mag >= 0.80  (unmistakable)"),
             (0.90, "mag >= 0.90  (dramatic; the ones a chronicler notices)"),
             (0.95, "mag >= 0.95"), (1.00, "central (total or annular)")]
    span = rows[-1]["year"] - rows[0]["year"] + 1
    for thr, label in bands:
        k = sum(1 for r in rows if irish_mag(r) > thr)
        print("  %-46s %4d   (one every %.1f years)"
              % (label, k, span / k if k else float("inf")))

    print("\n== per century: eclipses observable from Ireland ==")
    print("  century   any    >=0.50  >=0.80  >=0.90  central")
    cents = sorted(set(int(r["year"]) // 100 for r in rows))
    for c in cents:
        sub = [r for r in rows if int(r["year"]) // 100 == c]
        line = [sum(1 for r in sub if irish_mag(r) > t)
                for t in (0.0, 0.5, 0.8, 0.9, 1.0)]
        print("  %3d00s  %5d %7d %7d %7d %8d" % (c, *line))

    print("\n== discriminating power: Ireland against the Mediterranean ==")
    deep_ir = [r for r in rows if irish_mag(r) >= 0.80]
    deep_med = [r for r in rows if med_mag(r) >= 0.80]
    both = [r for r in rows if irish_mag(r) >= 0.80 and med_mag(r) >= 0.80]
    only_ir = [r for r in deep_ir if med_mag(r) < 0.40]
    only_med = [r for r in deep_med if irish_mag(r) < 0.20]
    print("  deep (>=0.80) over Ireland:            %4d" % len(deep_ir))
    print("  deep (>=0.80) over the Mediterranean:  %4d" % len(deep_med))
    print("  deep in both (the test is blind here): %4d  = %.0f%% of the Irish set"
          % (len(both), 100.0 * len(both) / max(1, len(deep_ir))))
    print("  deep in Ireland, <0.40 in the Med:     %4d  <- diagnostic of observation"
          % len(only_ir))
    print("  deep in the Med, <0.20 in Ireland:     %4d  <- diagnostic of borrowing"
          % len(only_med))
    print("\n  So the test has power on %d + %d = %d of the %d eclipses that any"
          % (len(only_ir), len(only_med), len(only_ir) + len(only_med), n))
    print("  chronicler on either side could have recorded, and no power on the"
          " %d that were" % len(both))
    print("  large in both places.  A record of one of *those* decides nothing.")

    print("\n== can the annals locate their own observatory? ==")
    print("  The Chronicle of Ireland hypothesis has the common source kept at")
    print("  Iona until the middle of the eighth century and in Ireland after it.")
    print("  Iona and Clonmacnoise are 3 degrees of latitude apart, which is enough")
    print("  to put one of them inside a penumbra and the other outside it. Where")
    print("  that happens, a notice that reports depth *is* evidence of where it")
    print("  was written.")
    diag = [r for r in rows
            if abs((r["Iona_mag_central"] or 0.0) - (r["Clonmacnoise_mag_central"] or 0.0)) >= 0.25
            and max(r["Iona_mag_central"] or 0.0, r["Clonmacnoise_mag_central"] or 0.0) >= 0.5]
    iona_side = [r for r in diag
                 if (r["Iona_mag_central"] or 0.0) > (r["Clonmacnoise_mag_central"] or 0.0)]
    print("  eclipses where |mag(Iona) - mag(Clonmacnoise)| >= 0.25 and one of them")
    print("  was at least 0.50 deep:  %d  (%d favouring Iona, %d favouring Clonmacnoise)"
          % (len(diag), len(iona_side), len(diag) - len(iona_side)))
    print("  a further %d are central (total or annular) at Iona but not at Clonmacnoise,"
          % sum(1 for r in diag if (r["Iona_mag_central"] or 0) >= 1.0
                and (r["Clonmacnoise_mag_central"] or 0) < 1.0))
    print("  and %d the other way round -- these are the sharpest of all, because"
          % sum(1 for r in diag if (r["Clonmacnoise_mag_central"] or 0) >= 1.0
                and (r["Iona_mag_central"] or 0) < 1.0))
    print("  only a central eclipse brings out stars.")

    cols = ["date_julian_cal", "year", "weekday", "gamma", "irish_mag_central",
            "Armagh_mag_central", "Armagh_ut_central", "Armagh_alt_central",
            "Iona_mag_central", "Clonmacnoise_mag_central",
            "Rome_mag_central", "Constantinople_mag_central",
            "Alexandria_mag_central", "irish_mag_min_over_dt",
            "irish_mag_max_over_dt"]
    _write(os.path.join(HERE, "results", "prediction_irish.csv"),
           sorted(only_ir, key=lambda r: r["jd_tt"]), cols)
    _write(os.path.join(HERE, "results", "prediction_borrowed.csv"),
           sorted(only_med, key=lambda r: r["jd_tt"]), cols)
    _write(os.path.join(HERE, "results", "ireland_deep_eclipses.csv"),
           sorted([r for r in rows if irish_mag(r) >= 0.90],
                  key=lambda r: r["jd_tt"]), cols)
    _write(os.path.join(HERE, "results", "site_discriminating.csv"),
           sorted(diag, key=lambda r: r["jd_tt"]), cols)
    print("\nwrote prediction_irish.csv (%d), prediction_borrowed.csv (%d), "
          "ireland_deep_eclipses.csv (%d), site_discriminating.csv (%d)"
          % (len(only_ir), len(only_med),
             sum(1 for r in rows if irish_mag(r) >= 0.90), len(diag)))


def _write(path, rows, cols):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([r.get(c) for c in cols])


if __name__ == "__main__":
    main()
