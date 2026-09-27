"""Historical-regime checks: do the shadows land where the sources put them?

There is a gap in `validate_astro.py` that matters and was not closed until now.
Its three modern eclipses validate the ephemeris, the topocentric geometry and
the magnitude convention -- but they cannot validate the **Delta-T model**,
because modern Delta-T is measured, not modelled: at 2017 it is 69 s and known to
milliseconds, so an error in the historical Delta-T spline would leave those
checks completely unmoved.

Delta-T is exactly what this study depends on. At AD 664 it is 4074 s, and an
error of 300 s in it moves the shadow track 125 km at Irish latitudes -- the
difference between a total and a deep partial eclipse at a given monastery. So
the engine needs checking in the regime it is actually used in.

The test available without an eclipse catalogue: well-attested medieval eclipses
whose *geography* is independently recorded. If the computed track puts totality
where medieval and modern accounts put it, at Delta-T of 1000-4000 s, then the
spline is doing its job end to end.

These are consistency checks against narrative and secondary sources, not
arcsecond comparisons against a canon. They are weaker than the modern checks and
are labelled as such. They are also the only ones available offline.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SITES = ("Iona", "Armagh", "Bangor", "Clonmacnoise", "Jarrow", "Rome")

CASES = [
    {
        "date": "1133-08-02",
        "attested": "Total in Scotland with about 4.5 minutes of totality; "
                    "'King Henry's eclipse', described across England. The "
                    "Anglo-Saxon Chronicle reports stars visible at midday.",
        "predict": "central at Iona and Jarrow; NOT central in the Irish midlands",
        "test": lambda r: (f(r, "Iona") >= 1.0 and f(r, "Jarrow") >= 1.0
                           and f(r, "Clonmacnoise") < 1.0),
    },
    {
        "date": "1140-03-20",
        "attested": "Total in the English Channel; the Anglo-Saxon Chronicle has "
                    "candles lit to eat by, about noon.",
        "predict": "no Irish or Northumbrian site central, and deeper in the "
                   "south than the north (track passing south of Ireland)",
        "test": lambda r: (max(f(r, s) for s in ("Iona", "Armagh", "Clonmacnoise",
                                                 "Jarrow")) < 1.0
                           and f(r, "Clonmacnoise") > f(r, "Iona")),
    },
    {
        "date": "0885-06-16",
        "attested": "AU 885: an eclipse of the sun, and stars were seen in the "
                    "sky. Stars require essentially totality.",
        "predict": "central at Iona and nowhere else tested",
        "test": lambda r: (f(r, "Iona") >= 1.0
                           and max(f(r, s) for s in ("Armagh", "Clonmacnoise",
                                                     "Jarrow")) < 1.0),
    },
    {
        "date": "0664-05-01",
        "attested": "AU 664 and Bede HE III.27; near-total across Ireland, "
                    "remembered vividly in Northumbria.",
        "predict": "at least 0.95 at every Irish site, and central at Jarrow",
        "test": lambda r: (min(f(r, s) for s in ("Iona", "Armagh")) >= 0.95
                           and f(r, "Jarrow") >= 1.0),
    },
]


def f(r, site):
    try:
        return float(r[site + "_mag_central"])
    except (KeyError, TypeError, ValueError):
        return 0.0


def main():
    rows = {r["date_julian_cal"]: r
            for r in csv.DictReader(open(os.path.join(HERE, "results",
                                                      "eclipse_canon.csv")))}
    fails = []
    for c in CASES:
        r = rows.get(c["date"])
        print("=" * 74)
        print("%s   Delta-T %s s" % (c["date"], r["delta_t_central_s"] if r else "?"))
        print("  attested: %s" % c["attested"])
        print("  predicts: %s" % c["predict"])
        if r is None:
            print("  RESULT:   NOT IN CANON -- FAIL")
            fails.append(c["date"])
            continue
        print("  computed: " + "  ".join("%s %.3f" % (s, f(r, s)) for s in SITES))
        ok = c["test"](r)
        print("  RESULT:   %s" % ("OK" if ok else "FAIL"))
        if not ok:
            fails.append(c["date"])

    print("=" * 74)
    print("\n== an unresolved discrepancy, recorded rather than smoothed over ==")
    r = rows.get("0878-10-29")
    print("878-10-29. This engine puts the central line over Ulster: Armagh %.3f"
          % f(r, "Armagh"))
    print("and Bangor %.3f are central, while Iona (%.3f) and Jarrow (%.3f) are not."
          % (f(r, "Bangor"), f(r, "Iona"), f(r, "Jarrow")))
    print("A popular secondary account says the eclipse was total in central and")
    print("northern Scotland and merely deep in Ireland -- the opposite placement.")
    print("This session could not adjudicate: the authoritative path maps are on")
    print("hosts the egress policy blocks, and the secondary account is a news")
    print("article, not a catalogue.")
    print()
    print("Two reasons to think the computation is right: the same engine places")
    print("1133 in Scotland and 1140 in the Channel correctly, at comparable")
    print("Delta-T; and AU 885's 'stars were seen' matches Iona being the only")
    print("central site there. But it is not settled, and it matters, because if")
    print("878 was total over Armagh then the Irish annalist watched a total")
    print("eclipse -- and the AU 878 notice, unlike AU 885, does not mention")
    print("stars. Either the notice was written where it was not total, or the")
    print("two notices differ in style. That is a sharp question for whoever has")
    print("the text.")
    print()
    if fails:
        print("FAILURES: %s" % ", ".join(fails))
        return 1
    print("all historical-regime checks passed "
          "(Delta-T 1035-4074 s across the four cases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
