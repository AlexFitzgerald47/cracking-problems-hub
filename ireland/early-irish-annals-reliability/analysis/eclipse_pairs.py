"""Solar/lunar eclipse pairs a fortnight apart, both visible from Ireland.

AU 878 records a lunar eclipse and then a solar eclipse fifteen days later, and
says so explicitly -- "fifteen solar days having intervened". That clause is not
decoration. Noticing that the two belong together requires either watching the sky
across a fortnight or knowing the theory that puts them there, and the Irish
computistical literature knew the theory.

So pairs are a sharper probe than single notices. A chronicle that records isolated
eclipses is recording prodigies. A chronicle that records *both members* of a pair,
and links them, is doing something closer to astronomy.

This finds every pair in the two canons: a solar eclipse and a lunar eclipse 12 to
18 days apart, with both visible from Ireland on the criteria their canons already
apply. It costs nothing -- both canons are already on disk -- and it produces a
list a future agent can check against the text directly.

The counting caveat, stated because it decides how the result reads: eclipse pairs
are *not* rare. They are the normal structure of an eclipse season, so the base
rate is high and finding pairs in the canon proves nothing by itself. What is
informative is the fraction of *available* pairs the annals record, against the
fraction of isolated eclipses they record.
"""

import csv
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")

MIN_GAP, MAX_GAP = 12.0, 18.0
SOLAR_VISIBLE = 0.50   # magnitude over Ireland worth calling an event


def main():
    solar = []
    for r in csv.DictReader(open(os.path.join(RES, "eclipse_canon.csv"))):
        try:
            m = float(r["irish_mag_central"] or 0.0)
        except ValueError:
            m = 0.0
        if m >= SOLAR_VISIBLE:
            solar.append({"jd": float(r["jd_tt"]), "date": r["date_julian_cal"],
                          "mag": m, "year": int(r["year"])})
    lunar = []
    for r in csv.DictReader(open(os.path.join(RES, "lunar_eclipse_canon.csv"))):
        if r.get("visible_from_ireland") not in ("True", "true"):
            continue
        try:
            um = float(r["umbral_mag"] or 0.0)
        except ValueError:
            um = 0.0
        if um <= 0.0:
            continue
        lunar.append({"jd": float(r["jd_tt"]), "date": r["date_julian_cal"],
                      "mag": um, "year": int(r["year"]),
                      "total": um >= 1.0})

    pairs = []
    for s in solar:
        for l in lunar:
            gap = s["jd"] - l["jd"]
            if MIN_GAP <= abs(gap) <= MAX_GAP:
                pairs.append({
                    "year": s["year"],
                    "first": "lunar" if gap > 0 else "solar",
                    "lunar_date": l["date"], "lunar_umbral_mag": round(l["mag"], 3),
                    "lunar_total": l["total"],
                    "solar_date": s["date"], "solar_irish_mag": round(s["mag"], 3),
                    "gap_days": round(abs(gap), 2)})
    pairs.sort(key=lambda p: p["lunar_date"])

    out = os.path.join(RES, "eclipse_pairs.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(pairs[0].keys()))
        w.writeheader()
        for p in pairs:
            w.writerow(p)

    span = 810.0
    strong = [p for p in pairs if p["solar_irish_mag"] >= 0.80 and p["lunar_total"]]
    print("solar eclipses over Ireland at magnitude >= %.2f:  %d" % (SOLAR_VISIBLE, len(solar)))
    print("umbral lunar eclipses visible from Ireland:        %d" % len(lunar))
    print("pairs %.0f-%.0f days apart, both visible:            %d  (one every %.1f years)"
          % (MIN_GAP, MAX_GAP, len(pairs), span / max(1, len(pairs))))
    print("  lunar first:  %d      solar first: %d"
          % (sum(1 for p in pairs if p["first"] == "lunar"),
             sum(1 for p in pairs if p["first"] == "solar")))
    print("  'strong' pairs (solar >= 0.80 AND lunar total):  %d  (one every %.0f years)"
          % (len(strong), span / max(1, len(strong))))
    print()
    print("AU 878 is one of these. The strong pairs, which are the ones a")
    print("chronicle keeping any kind of sky-watch should have caught:")
    for p in strong:
        print("  %s (lunar %s%s)  ->  %s (solar %.3f)   %.1f d"
              % (p["lunar_date"], p["lunar_umbral_mag"],
                 ", total" if p["lunar_total"] else "",
                 p["solar_date"], p["solar_irish_mag"], p["gap_days"]))
    print("\nwrote %s (%d pairs)" % (out, len(pairs)))
    print("\nBASE RATE WARNING: pairs are the normal structure of an eclipse")
    print("season, not a rarity. Finding them here proves nothing. The question")
    print("for the text is what FRACTION of available pairs the annals record,")
    print("compared with the fraction of isolated eclipses they record.")


if __name__ == "__main__":
    main()
