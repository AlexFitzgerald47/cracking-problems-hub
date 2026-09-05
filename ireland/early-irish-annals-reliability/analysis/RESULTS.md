# Results — astronomical retro-calculation for the early Irish annals

**Session:** 2026-09-05, cracker, mode *starting*. First substantive work on this
problem, and the first on the Hub's Ireland lane.

**One-line summary.** The annals' astronomical notices can be tested without the
annals, because the sky can be computed; doing so resolves the AD 664
"ninth hour / tenth hour" disagreement between the Annals of Ulster and Bede as
onset versus maximum — both correct — and shows that AU 885's "stars were seen"
is true only at Iona.

**What this is not.** It is not a reading of the annals. The corpus was
unreachable from this session (see `../PROGRESS.md`); six notices were tested, at
search-level verification, and their wording is not confirmed against a critical
edition. Read the verification status in `annal_records.csv` before quoting
anything here.

---

## 0. The instrument, and why you should believe it

`astro.py` computes the Sun and Moon from the analytic theories in Meeus (full
VSOP87; abbreviated ELP-2000/82) via `pymeeus`, with Δ*T* from the Stephenson,
Morrison & Hohenkerk (2016) spline. No ephemeris download, no network. Topocentric
geometry is done by full vector subtraction, so magnitudes and distances are exact
given the positions rather than parallax-approximated.

Validation (`validate_astro.py`, all passing — run it first):

| Check | Result |
|-------|--------|
| Meeus' worked examples: JD both calendars + inverse, weekday, GMST | pass |
| Meeus 25.b (solar theory), 47.a (lunar theory) | pass, to <5×10⁻⁴ deg |
| Magnitude at greatest eclipse, 2017-08-21 / 1999-08-11 / 2015-03-20 | agrees to ≤0.0005 |
| Sun–Moon separation at the published greatest-eclipse coordinates | 0.3″, 24″, 3.6″ |
| Gamma for the same three eclipses | agrees to ≤0.001 Earth radii |
| Negative control: a new moon with no eclipse | pass |
| **Finder completeness: solar eclipses 1901–2000** | **228 — exactly NASA's published count** |

The last line is the one the study rests on. Every argument about what the annals
did or did not record divides by that number.

**Δ*T* matters more than it looks.** The Morrison & Stephenson (2004) long-term
parabola is off by −182 s at AD 664 and −481 s at AD 1000. 481 s is 2° of Earth
rotation, ~220 km at Irish latitudes — a tenth of a magnitude at the edge of a
partial eclipse. The first canon run was built on the parabola and was discarded.
Use `astro.delta_t()`.

---

## 1. AD 664: the hour crux dissolves

The Annals of Ulster enter the eclipse as darkness on the kalends of May *in nona
hora*. Bede (HE III.27) dates it to 3 May, *hora circiter decima*. The date
disagreement is well known; the hour disagreement has, as far as this session
could establish, never been used as a constraint — and it is one, because the
unequal ("canonical") hour a phase falls in is a computable function of Δ*T* once
the site is fixed.

**Date.** There is no solar eclipse on 3 May 664 visible from anywhere in Ireland
or Britain. 1 May is correct, and the eclipse was near-total across Ireland.

**Hour**, at Δ*T* = 4074 ± 40 s (Stephenson et al. 2016), unequal hour = 77 min:

| Site | peak magnitude | first contact | maximum | last contact |
|------|---------------|---------------|---------|--------------|
| Armagh | 0.996 | **hour 9** | **hour 10** | hour 11 |
| Iona | 0.989 | **hour 9** | **hour 10** | hour 11 |
| Clonmacnoise | 0.963 | **hour 9** | **hour 10** | hour 11 |
| Jarrow | central | hour 10 | hour 11 | hour 11 |

So **the annals' ninth hour is first contact and Bede's tenth hour is maximum, as
seen from Ireland.** Neither is an error and they are not in conflict. Maximum
falls in the ninth hour at no Δ*T* within ±600 s of the published value, so the
annalistic hour is only wrong if one insists it describes maximum.

Robustness (`results/ad664_hour_analysis.csv`, Δ*T* scanned in 20 s steps): the
ninth-hour/first-contact identification holds for Δ*T* ≥ 3834 s at Iona and
≥ 3894 s at Clonmacnoise — comfortably inside the published value ± several σ.
**At Armagh it is marginal**, with the boundary at ~4060 s against 4074 ± 40 s.
Iona and Clonmacnoise carry the result; Armagh alone would not.

A lead, not a finding: Bede's "about the tenth hour" fits *Irish* maximum and not
Jarrow's, where maximum fell in the eleventh hour. *Circiter* is doing real work
in that sentence, so this is suggestive of an Irish or Ionan source behind Bede's
hour and no more than that.

---

## 2. Six notices audited

`record_audit.py`; full output in `results/record_audit.json`.

| Record | Date tested | Deepest Irish site | Irish mag | Rome | Constantinople |
|--------|-------------|--------------------|-----------|------|----------------|
| AU 594 | 594-07-23 | Armagh | **1.061** central | 0.557 | 0.438 |
| AU 664 | 664-05-01 | Armagh | 0.996 | 0.739 | 0.848 |
| AU 865 | 865-01-01 | Armagh | 0.999 | 0.694 | 0.513 |
| AU 878 | 878-10-29 | Armagh | **1.025** central | 0.891 | 0.831 |
| AU 885 | 885-06-16 | **Iona** | **1.077** central | 0.477 | 0.357 |
| Bede, 3 May 664 | 664-05-03 | — | **no eclipse** | 0.000 | 0.000 |

**The hit rate is partly circular and is not offered as evidence.** These dates
come from the standard modern identifications, which were themselves made by
matching annal entries to computed eclipses. What the identification procedure did
*not* use, and what therefore counts:

**AU 885 localises itself.** The notice adds "and stars were seen in the sky".
Stars require essentially totality. The eclipse was central **only at Iona**
(1.077); Armagh reached 0.972 and Clonmacnoise 0.960, at which stars are not seen.
If the descriptive detail is accurate, that notice was written at or near Iona.
This is the sharpest single datum here and it is independently checkable.

**AU 594's gloss is exact.** *Mane tenebrosum*, "a dark morning": computed first
contact in the first hour of daylight, maximum in the second, central at Armagh
and Clonmacnoise. This sits *before* the AD 627 threshold from which McCarthy &
Breen argued all such notices are local observation.

**AU 878 states four things at once and gets three of them right.**

| Element claimed | Computed | Verdict |
|-----------------|----------|---------|
| IV Kal. Nov. (29 Oct) | real eclipse, central at Armagh (1.025) | confirmed |
| feria 4 (Wednesday) | Wednesday | confirmed |
| "about the seventh hour" | hour 7 lies inside the eclipse; first contact hour 6, maximum hour 8 | consistent, one unequal hour (≈46 min) before maximum |
| luna 28 | true lunar age at maximum 29.42 d | **the tabular moon ran 1.42 days behind the sky** |

That last row is not an error in the record; it is a measurement of the
annalist's lunar table, and it is the kind of quantity the computistical
literature argues about.

**Depth contrast.** All five annalistic eclipses were substantially deeper over
Ireland than over Rome or Constantinople. A chronicle borrowing its eclipses from
Mediterranean sources has no mechanism for that, and the date-matching
identification procedure does not select for it.

---

## 3. AU 878's fifth element: the lunar eclipse a fortnight before

The notice ends "fifteen solar days having intervened" — it reports a *lunar*
eclipse a fortnight before the solar one. `lunar_eclipses.py` adds umbral geometry
(Meeus ch. 54), validated first against published umbral magnitudes:

| Eclipse | computed | published | |
|---------|----------|-----------|--|
| 2018-07-27 | 1.6162 | 1.6087 | OK |
| 2019-01-21 | 1.2039 | 1.1951 | OK |
| 2015-09-28 | 1.2864 | 1.2764 | OK |
| 2019-04-19 full moon | −9.392 | (no eclipse) | OK |

The consistent +0.008 to +0.010 bias is the shadow-enlargement convention (1.02 is
used here); it is an order of magnitude below anything that matters at this
distance in time, but it is there and should not be polished away.

**Result.** At the full moon before the solar eclipse there was a **total lunar
eclipse on 15 October 878** (Julian), umbral magnitude **1.054**, greatest at
04:28 UT — and from Ireland the eclipsed Moon stood **23° above the horizon with
the Sun 23° below it**, i.e. in a fully dark sky. The interval between the two
greatest-eclipse instants is 14.29 days, which is 15 days counted inclusively in
the Roman manner, exactly as the notice says.

So AU 878 states five things and the sky confirms four of them outright:

| Element | Verdict |
|---------|---------|
| 29 October, solar eclipse | confirmed — central at Armagh, magnitude 1.025 |
| feria 4 (Wednesday) | confirmed |
| a lunar eclipse "fifteen days" earlier | confirmed — total, 15 October, inclusive interval 15 days, observable |
| "about the seventh hour" | consistent — inside the eclipse, one unequal hour (≈46 min) before maximum |
| luna 28 | true lunar age 29.42 d — the tabular moon ran **1.42 days behind the sky** |

A record that gets a solar eclipse, its weekday, and a preceding total lunar
eclipse at the stated interval all correct is very hard to explain as anything but
observation, or as a copy from someone else's observation made at this latitude.
The one element that is *off* is the one that comes from a table rather than the
sky.

---

## 4. The denominator, and the honest limits of the test

`find_eclipses.py`, AD 400–1210: **10,019 lunations scanned, 1,930 solar
eclipses** — 2.38 per year, the long-run rate. Full output in
`results/eclipse_canon.csv` and `results/eclipse_dt_curves.json`; summary in
`results/visibility_summary.txt`.

### How often was there anything to see from Ireland

| Depth over Ireland (best of Armagh / Iona / Clonmacnoise / Bangor, Sun up) | Count | Rate |
|---|---|---|
| any partial phase | 367 | one every 2.2 years |
| ≥ 0.50 (noticeable dimming) | 171 | one every 4.7 years |
| ≥ 0.80 (unmistakable) | 70 | one every 11.6 years |
| ≥ 0.90 (the kind a chronicler notices) | 37 | one every 21.9 years |
| ≥ 0.95 | 17 | one every 47.6 years |
| central (total or annular) | **5** | one every 162 years |

**Only five central solar eclipses were visible from Ireland in 810 years.** Three
of the six records tested fall on them. That is worth stating precisely because it
cuts both ways: the coincidence is striking, and it is also exactly what one would
expect if chroniclers record the events that are impossible to miss.

**And the five are these:**

| Date (Julian) | Armagh | Iona | Rome | In the record? |
|---|---|---|---|---|
| 594-07-23 | **1.061** | 0.989 | 0.557 | AU 594, *mane tenebrosum* |
| 664-05-01 | 0.994 | 0.986 | 0.739 | AU 664 / Bede III.27 (central at Bangor, 1.042) |
| 878-10-29 | **1.025** | 0.995 | 0.891 | AU 878, the five-element notice |
| 885-06-16 | 0.971 | **1.077** | 0.477 | AU 885, "stars were seen" |
| 1133-08-02 | 0.963 | **1.064** | 0.880 | — |

Four of the five are the notices tested above. **The fifth is 1133, and 1133 is
the year in which McCarthy & Breen's series of Irish astronomical records ends.**

That last point is not something the selection could have produced. The records
here were chosen because they are the well-known ones, which biases hard towards
deep eclipses and makes the four-of-five overlap much less impressive than it
looks. But the terminal date of the published series was taken from an abstract,
before the canon existed, and it lands exactly on the last central solar eclipse
visible from Ireland in this window. If the Irish astronomical record begins and
ends with the events that were impossible to miss, that is a statement about the
recording tradition — and it is checkable by anyone who can open the annals.

Per-century counts are in `results/visibility_summary.txt`; they are flat, at
40–50 eclipses of any depth per century, so nothing in the recording record can be
explained by the sky becoming busier.

### Where the observed-versus-borrowed test has power, and where it has none

| | Count |
|---|---|
| deep (≥0.80) over Ireland | 70 |
| deep (≥0.80) over the Mediterranean | 90 |
| **deep in both — the test is blind here** | **28** (40% of the Irish set) |
| deep in Ireland, <0.40 in the Mediterranean → diagnostic of observation | 11 |
| deep in the Mediterranean, <0.20 in Ireland → diagnostic of borrowing | 17 |

Of the 132 eclipses deep enough for a chronicler on either side to notice, **the
test can decide 28 and is blind on 28.** A notice of one of the blind ones settles
nothing, whichever way it reads. Those 28 decisive eclipses are written out as
`results/prediction_irish.csv` (11) and `results/prediction_borrowed.csv` (17).
**This is the experiment, specified and priced in advance**: any of the borrowed
list appearing in the annals is decisive against local observation; absences from
the Irish list measure recording practice rather than knowledge.

### A test that turned out weaker than it looked — reported anyway

The Chronicle of Ireland hypothesis puts the common source at Iona until the
mid-eighth century and in Ireland after it. Since Iona and Clonmacnoise are three
degrees of latitude apart, a notice reporting *depth* should in principle say
where it was written. It mostly cannot:

| Split between Iona and Clonmacnoise | Count in 810 years |
|---|---|
| difference ≥ 0.10, deeper site ≥ 0.50 | 13 (10 favour Iona) |
| difference ≥ 0.25 | 3 |
| difference ≥ 0.40 | 1 |
| **central at Iona but not Clonmacnoise** | **2** |
| central at Clonmacnoise but not Iona | 1 |

Twelve usable cases in eight centuries, of which the annals will have recorded a
handful at most. **This is a negative result and it belongs in the record:** the
site-discrimination test cannot carry a conclusion on its own. It can corroborate
one argued on other grounds — and AU 885 is one of the two "central at Iona, not
at Clonmacnoise" cases, which is why that notice is worth more than the others.

---

## 5. What would change these conclusions

* **The wording.** If AU 664 does not read *in nona hora*, Result 1 evaporates. If
  AU 885 does not say stars were seen, the Iona localisation goes with it. Six
  quotations at search-level verification are the weakest link here and are
  flagged as such in `annal_records.csv`.
* **The annal-year attachments.** This session tested *dates*, taking the
  standard identifications on trust. Whether each notice actually sits at the
  corresponding annal-year in AU — the chronological question this problem is
  really about — was not testable without the text.
* **A larger record set.** Six notices support observations, not statistics.
  McCarthy & Breen work from a corpus running 442–1133. The engine is built to
  take it.
* **Δ*T*.** Only the AD 664 hour result is sensitive, and only at Armagh, where
  the boundary sits within 1σ of the published value. Everything else in this
  document is stable across ±300 s, which is ±7σ.
