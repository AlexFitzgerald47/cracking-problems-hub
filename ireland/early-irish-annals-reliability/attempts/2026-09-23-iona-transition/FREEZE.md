# Frozen predictions — 2026-09-23, before any time series was computed

Written and committed **before** the changepoint code was run. What had been
inspected at freeze time: (a) the XML markup structure of the four CELT files;
(b) corpus-wide *totals* of candidate surface forms, to build the gazetteer;
(c) the two pipeline-validation checks below. **No per-year series, no
proportion, and no changepoint statistic had been computed on any tag.**

## Pipeline validation — run before freezing, both passed

These are reproductions of published facts, used to prove the parser, not
findings. Reported here so that the freeze is honest about what had been seen.

**V1 — the Annals of Ulster AD offset.** Mac Airt & Mac Niocaill's edition states
that AU's own `AD nnn` figure runs one year behind the true year down to 1014 and
is correct thereafter. Extracting the `AD nnn` string from AU's kalend entries and
differencing it against CELT's year container recovers exactly that, having been
told nothing about it:

| AU range | n kalends with an AD figure | offset 0 | offset +1 |
|---|---|---|---|
| 431–599 | 163 | 55 | 108 |
| 600–799 | 199 | 1 | 198 |
| 800–1013 | 213 | 0 | 212 (one outlier at +5) |
| 1014–1131 | 116 | 115 | 1 |

The +1 offset becomes unbroken at **AU 489**; the fifth-century section is where
it is being established and is inconsistent, which is also as described.

**V2 — manuscript lacunae.** Scanning for year gaps of >3 years recovers three
independently documented lacunae that were nowhere encoded in the markup:
Chronicon Scotorum **723–803**, Tigernach **767–973** (and 1004–1016), Annals of
Ulster **1133–1154** (TCD MS 1282's gap at 1115.4–1162.3, partly supplied from a
second MS). These match the editions' own descriptions.

**Consequence for the design, noticed at freeze time:** the CS lacuna 723–803
sits exactly over the window this attempt is about, and AT stops at 766. So CS
*cannot* locate a changepoint near 740 — but it can do something arguably better,
a clean two-sample comparison of the rate before 723 against the rate after 803,
straight across the hole. AT has only 27 years on the far side and is declared
underpowered in advance rather than after the fact.

## The hypothesis

The standard reconstruction (Bannerman; Smyth; Charles-Edwards, *The Chronicle of
Ireland*, 2006) is that a chronicle kept at Iona from the later 6th century was
continued in Ireland from roughly the second quarter of the 8th century — the
move is usually placed c. 740, sometimes c. 727 — and that this common chronicle
is the shared source of AU and the Clonmacnoise group (AT, CS) down to 911.

If that is right, it is a claim about where a manuscript physically sat, and it
should leave a measurable fingerprint: the rate at which Scottish news enters the
record should fall, and the rate of news from wherever the chronicle went should
rise, *in the same few decades*.

The rival explanation that must be beaten is that Iona simply became less
newsworthy — plausible, because Iona was raided in 795, 806 and 825 and its
community partly relocated to Kells. That rival makes a different date prediction.

## Predictions

Tag definitions are frozen in `src/gazetteer.py` (place-names and ethnonyms only;
personal names excluded; ambiguous terms — Cruithin, Alba, Scotia/Scots, Rechru,
Manu, Lismore — excluded from the primary tag and kept for a sensitivity run).
Unit of analysis: the non-kalend annalistic entry with ≥3 words. Per-year
statistic: tagged entries / total entries.

**P1 (AU, primary).** A single-changepoint binomial scan of the SCOT proportion
in AU over 550–1000 puts its maximum in **[715, 765]**.
*Fails if* the argmax falls outside [700, 780], **or** a permutation null
(entries reassigned across years, per-year entry counts held fixed, 5,000 draws)
does not give p < 0.01 for the maximum statistic.

**P2 (independent witnesses — evidence not used to derive P1).**
(a) **CS**: SCOT rate over 550–722 exceeds SCOT rate over 804–1000, Fisher exact
p < 0.05.
(b) **AI**: SCOT rate over [550, ĉ) exceeds [ĉ, 1000), where ĉ is AU's fitted
changepoint.
(c) **AT**: same contrast over [550, ĉ) vs [ĉ, 766]. *Declared underpowered in
advance*; reported for direction only.
*Fails if* (a) fails, or if two of the three point the wrong way.

**P3 (specificity).** The INSULAR series (Saxons, Britons, Northumbria, Wales) in
AU does **not** show a significant fall at the same changepoint.
*If it does*, the chronicle did not lose Scottish news specifically, it lost
foreign news generally, and the Iona reading loses its force. I will say so.

**P4 (beating the Viking rival).** AU's SCOT changepoint is **not** in [785, 835].
*If it is*, the raids-and-relocation explanation is preferred over a scriptorium
move and I will prefer it.

**P5 (the two-sided test — the strong one).** At AU's SCOT changepoint there is a
simultaneous **rise** in the MIDLAND series, whose own upward changepoint falls
within ±40 years of the SCOT changepoint.
*This is what separates "a chronicle moved" from "Iona stopped mattering".* A
fall with no matching rise anywhere is consistent with the rival and I will
report it as such.

## Declared in advance

- SCOT is a small tag: 262 entries in the whole four-witness corpus. Changepoint
  *location* will have a wide confidence interval and the power analysis is part
  of the result, not an excuse offered afterwards.
- AU, AT, CS and AI are not independent samples — sharing a source is the
  hypothesis. What is independent is the **manuscript tradition** (Ulster /
  Clonmacnoise / Munster), so a redactional artefact peculiar to AU should not
  reproduce in AI.
- Tag precision will be audited by hand on a random sample of 40 SCOT-tagged and
  40 untagged entries, and the audit reported whatever it shows.
