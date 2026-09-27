"""Is each eclipse identification forced, or was there a choice?

§2 flagged that the audited notices land on real eclipses partly by construction:
the dates come from modern identifications, which were themselves made by matching
annal entries to computed eclipses. That circularity is real, but it is not total,
and this measures how much of it there is.

The question: for a notice sitting at annal-year Y, **how many eclipses were
available to identify it with?** If exactly one solar eclipse was visible from
Ireland anywhere in Y ± 3 years, the identification is *forced* -- no scholar had a
choice, and the fact that it lands on the right year is then evidence about the
annals' chronology rather than about the scholar's judgement. If four were
available, the identification is a selection and proves much less.

This is the "count the competitors, do not score one" rule from
`board/PRACTICES.md`, applied to identifications instead of decipherments. It also
bears directly on the problem statement, which is about chronology: a forced
identification at annal-year Y is a hard chronological anchor.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WINDOW = 3          # annal years either side
NOTICEABLE = 0.50   # Irish magnitude a chronicler could plausibly have recorded


def main():
    canon = []
    for r in csv.DictReader(open(os.path.join(HERE, "results", "eclipse_canon.csv"))):
        try:
            m = float(r["irish_mag_central"] or 0.0)
        except ValueError:
            m = 0.0
        canon.append((int(r["year"]), r["date_julian_cal"], m))

    records = [r for r in csv.DictReader(open(os.path.join(HERE, "annal_records.csv")))
               if (r.get("type") or "solar") == "solar" and r["annal"].startswith("Annals")]

    print("Candidate eclipses within +/-%d years of the annal-year, Irish magnitude"
          " >= %.2f" % (WINDOW, NOTICEABLE))
    print("(the identification is FORCED where there is exactly one)\n")
    forced = 0
    for rec in records:
        ay = int(rec["annal_year"])
        chosen = rec["claimed_date_julian"]
        cands = [c for c in canon
                 if abs(c[0] - ay) <= WINDOW and c[2] >= NOTICEABLE]
        cands.sort(key=lambda c: -c[2])
        tag = "FORCED" if len(cands) == 1 else "%d candidates" % len(cands)
        if len(cands) == 1:
            forced += 1
        print("%-7s annal-year %4d -> %s   [%s]" % (rec["id"], ay, chosen, tag))
        for y, d, m in cands:
            mark = " <-- the identification" if d == chosen else ""
            print("        %s  Irish magnitude %.3f%s" % (d, m, mark))
        if chosen not in [c[1] for c in cands]:
            print("        !! the identified eclipse is NOT among the candidates "
                  "at this threshold")
        print()

    print("forced identifications: %d of %d" % (forced, len(records)))
    print()
    print("Reading this: a FORCED row is a genuine chronological anchor -- there was")
    print("no other eclipse a scholar could have matched, so the annal-year landing")
    print("on it is a fact about the annals. A multi-candidate row is a selection,")
    print("and section 2's circularity warning applies to it in full.")


if __name__ == "__main__":
    main()
