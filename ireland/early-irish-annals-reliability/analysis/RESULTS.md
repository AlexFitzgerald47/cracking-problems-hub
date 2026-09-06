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

> **Read §10 before quoting this paragraph.** The reading above assumes the
> unequal-*interval* hour convention. §10 adds a third hour statement (AU 764),
> shows that three records cannot establish which convention the annalists used,
> and identifies which part of this section survives all three: that maximum
> falls in the ninth hour under *no* convention. The identification of AU's hour
> with first contact specifically is one of two live readings, not a result.

Robustness (`results/ad664_hour_analysis.csv`, Δ*T* scanned in 20 s steps): the
ninth-hour/first-contact identification holds for Δ*T* ≥ 3834 s at Iona and
≥ 3894 s at Clonmacnoise — comfortably inside the published value ± several σ.
**At Armagh it is marginal**, with the boundary at ~4060 s against 4074 ± 40 s.
Iona and Clonmacnoise carry the result; Armagh alone would not.

### Correction to this section, made later in the same session

The finished canon shows something the first pass did not have: **the 664 eclipse
was *central* at Jarrow (1.041)**, Bede's own monastery, and at Bangor in Co. Down
(1.042). The track ran across Ulster and Northumbria. That admits a second reading
of the hour pair, and it is at least as good as the first:

| | AU's ninth hour | Bede's tenth hour |
|---|---|---|
| **Reading (a)** | first contact, Ireland | maximum, Ireland |
| **Reading (b)** | first contact, Ireland | **first contact, Jarrow** (hour 10, at every Δ*T* tested) |

Reading (b) explains the one-hour difference purely by where the two observers
stood, without requiring the sources to describe different phases of the eclipse.
It is the more economical account, and Jarrow having seen totality makes a
Northumbrian observation behind Bede's hour more likely, not less — which is the
opposite of the lead offered in the first pass, when Jarrow's magnitude was not
yet known.

**The astronomy cannot choose between (a) and (b)** and this document should not
pretend otherwise. What it does establish, on either reading, is the thing that
matters: **neither hour is an error**, and the ninth hour cannot describe maximum
anywhere in Ireland at any plausible Δ*T*. The earlier framing — "the annals record
onset and Bede records maximum" — was too confident about which of two equally
good readings is right, and is corrected here rather than quietly amended above.

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

*A note on which number is which, because two tables in this document use
different conventions and a reader will otherwise trip on it.* The table above
reports the deepest of **Armagh, Iona and Clonmacnoise** — the three sites
`record_audit.py` examines — while §4 and §7 report `irish_mag_central` from the
canon, which is the deepest of **four**, adding Bangor in Co. Down. That is why
664 appears here as 0.996 (Armagh) and elsewhere as 1.042: the eclipse was central
at Bangor. Both numbers are right; they answer different questions. Post-refinement
the two pipelines agree to better than 0.001 on every site they share.

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

---

## 6. Experiment 5 is dead: the hour statements cannot measure Delta-T

The handover written earlier in this session proposed running the AD 664 argument
backwards — using annalistic hour statements as an independent Irish constraint on
the Earth's rotation, since Stephenson's first-millennium curve rests on
Babylonian, Chinese and Arab records and not on Irish ones. `deltat_power.py`
prices that experiment before anyone spends a session on it. It does not survive.

**The geometry is exact.** An eclipse happens at a fixed TT. A site's local
apparent solar time at that instant is a function of UT = TT − Δ*T*, and LAT
tracks UT one for one, so raising Δ*T* by *d* seconds moves the eclipse *d*
seconds earlier in local apparent time. The unequal-hour boundaries are fixed by
date and latitude and do not move with Δ*T* at all. **So one correct hour
statement constrains Δ*T* to an interval exactly one unequal hour wide** — and
nothing better is available from it.

Measured on the real canon (the 37 eclipses at Irish magnitude ≥0.90, with the
actual hour length at Armagh on each date):

| | |
|---|---|
| shortest unequal hour | 2,203 s (37 min, midwinter) |
| longest | 5,166 s (86 min, midsummer) |
| median | 4,333 s (72 min) |
| **one statement therefore gives** | **±2,167 s** |
| published 1σ on Δ*T* here | 15–50 s |

One statement is ~54× too coarse. Intersecting *N* independent correct
statements (Monte Carlo, 20,000 draws each):

| N | expected interval | half-width | vs published σ |
|---|---|---|---|
| 1 | 4,040 s | ±2,020 s | 50× worse |
| 5 | 1,260 s | ±630 s | 16× worse |
| 20 | 359 s | ±179 s | 4.5× worse |
| 50 | 149 s | ±74 s | 1.9× worse |
| 100 | 74 s | ±37 s | comparable |

**Matching the published precision needs about 139 correct hour statements. The
entire Irish astronomical corpus 442–1133 runs to roughly twenty records, and not
all of them state an hour.** Two orders of magnitude short.

**And the arithmetic above is the optimistic case**, because it assumes you know
which contact each notice describes. Section 1 of this document shows you often
do not: AU and Bede report the same eclipse one unequal hour apart precisely
because one records onset and the other maximum. Misassign the phase for even one
record and its interval is disjoint from the others:

| Misassigned | Intersection empty in |
|---|---|
| 1 of 16 | **94% of draws** |
| 2 of 17 | 99% of draws |

So the method is not merely imprecise, it is brittle in the direction that
produces confident nonsense — a narrow surviving interval from a corpus with one
bad phase assignment would look like a *better* result, not a worse one.

**Verdict: do not run experiment 5.** Run it backwards instead, as section 1
does — fix Δ*T* from the published curve, and let it tell you which contact a
notice describes. That is the question this data can actually answer, and it is
the one that bears on the annals rather than on geophysics.

*(This closes item 5 of the handover. The handover has been amended in place
rather than rewritten.)*

---

## 7. The record ends at 1133; the sky does not

McCarthy & Breen's series of Irish astronomical records runs 442–1133, and §4
noted that 1133 is also the last **central** solar eclipse visible from Ireland in
this window. That looked like the sky explaining the terminus. The canon says
otherwise once you drop from "central" to "unmissable":

| Date (Julian) | Best Irish magnitude | |
|---|---|---|
| 1133-08-02 | **1.064** | central at Iona — the last central one |
| 1140-03-20 | 0.977 | |
| 1147-10-26 | 0.916 | |
| 1180-01-28 | 0.945 | |
| **1185-05-01** | **0.998** | at Iona; 52 years after 1133 |
| 1191-06-23 | 0.954 | |

**Five eclipses of magnitude ≥0.90 over Ireland after 1133**, one of them at 0.998
— a daylight event nobody standing outside could miss, and indistinguishable in
depth from the 865 eclipse that the annals *do* record (0.999). Against 32 such
eclipses in the 733 years before 1133, the post-1133 rate (5 in 76 years) is if
anything slightly *higher*.

*(An earlier draft of this paragraph said 1185 was "deeper than three of the six
notices audited". That was wrong — it is marginally shallower than all of them —
and is corrected here rather than silently edited. The point it was making
survives: 0.998 is not a marginal event.)*

So if the Irish astronomical record does stop at 1133, **the sky is not the
reason**. That is a statement about the recording tradition — a change in what the
annalists thought worth writing down, or in who was writing — and it is exactly
the kind of claim the annals are usually asked about and rarely answered with
independent evidence.

**Two caveats, both load-bearing.** First, the 1133 terminus is taken from an
abstract at search-level verification; it may be the scope of a study rather than
the end of a tradition, and AU itself continues to 1540. Second, this is a
prediction, not a result: it says *if* the record stops, look for a human cause.
Checking it costs one grep of the annals for the years 1140, 1147, 1180, 1185 and
1191. **1185-05-01 is the decisive one** — if a 0.998 eclipse over Ireland is
absent from the annals, the tradition had stopped recording the sky.

---

## 8. The lunar canon, and an asymmetry the annals can be tested against

`find_lunar_eclipses.py`, AD 400–1210: **10,018 lunations scanned, 1,993 lunar
eclipses, 1,266 of them umbral.** Completeness checked the same way as the solar
finder — **230 for 1901–2000 against a published 229**, the one difference a
grazing case at penumbral magnitude 0.009, which is a threshold convention rather
than a missed or invented eclipse. Files: `results/lunar_eclipse_canon.csv`,
`observable_sky_events.csv`.

### What was actually available to an Irish observer

"Visible" here means the Moon above the horizon **and** the Sun below −6°, at some
point between the umbral contacts — i.e. an eclipse someone could have watched,
not merely one that happened.

| | Count, AD 400–1210 | Rate |
|---|---|---|
| solar, magnitude ≥0.50 with the Sun up | 171 | one every 4.7 years |
| solar, ≥0.90 | 37 | one every 22 years |
| **solar, central** | **5** | one every 162 years |
| **lunar, umbral phase visible** | **710** | one every 1.1 years |
| **lunar, total and visible** | **327** | one every 2.5 years |

**A visible umbral lunar eclipse was 4.2× as common as a solar eclipse of
magnitude 0.50 or more. At the spectacular end the ratio is 65 to 1: 327 total
lunar eclipses against 5 central solar ones.**

That asymmetry is the point. A lunar eclipse is visible from the entire night
hemisphere rather than a narrow track, lasts hours rather than minutes, needs no
accident of geography, and can be looked at directly. **The annals had vastly more
opportunity to record lunar eclipses than solar ones.**

So the recording-rate comparison is sharp, and it needs only the text:

* If the annals record **solar eclipses at anything like the rate they record
  lunar ones**, the tradition was selecting for portent value, not logging the
  sky — a total eclipse of the sun is an omen, and a lunar eclipse a fortnight
  later is an event.
* If the **rates track availability**, it was logging.

This approaches McCarthy & Breen's argument that the motive was religious and
eschatological from the opposite direction to theirs: they read it out of the
records' content, this reads it out of what the records *omit* relative to what
the sky supplied. Per-century counts are in `results/sky_availability.txt` and are
flat, so nothing here can be attributed to the sky becoming busier or quieter.

### The borrowing test works far better on lunar eclipses

The solar version of the observed-vs-borrowed test (§4) is blind on 40% of its
candidates, because a big eclipse over Ireland is often a fair-sized one over Rome
too, and it forces a judgement about how deep an eclipse has to be before someone
writes it down. Lunar eclipses fail differently and more usefully: the event is
**identical everywhere it can be seen**, so depth carries no information at all —
but *visibility* does, because it depends on whether the Moon is above your horizon
at the time, and Ireland and Constantinople are 36° of longitude apart.

`lunar_borrowing.py`, over the 1,266 umbral eclipses:

| | Count |
|---|---|
| visible from Ireland | 703 |
| visible from Rome or Constantinople | 772 |
| visible from both — the test is blind here | 639 (91% of the Irish set) |
| **Ireland only** → diagnostic of local observation | **64** |
| **Mediterranean only** → diagnostic of borrowing | **133** |

**197 decisive cases against the solar test's 28** — seven times the power, and on
a cleaner discriminator: a yes-or-no about the horizon rather than a judgement
about magnitude. Note the honest nuance: proportionally the lunar test is *blinder*
(91% vs 40%), because the night hemisphere is large and Ireland and Rome usually
share it. It wins on absolute numbers, not on cleanliness of the sample.

`results/lunar_prediction_borrowed.csv` (133) is the strongest single artefact
this session produced for a future agent. **Any one of those eclipses appearing in
the Irish annals is a borrowing that cannot be explained away** — the Moon was
below the Irish horizon throughout, in an annal whose other astronomy is
demonstrably local. `lunar_prediction_irish.csv` (64) is the converse.

AU 878 already records one solar and one lunar eclipse a fortnight apart, and gets
both right.

---

## 9. Where the shadow actually fell — and what it says about who was watching

Handover item 6 was "settle the 878 track", parked because the authoritative path
maps sit on blocked hosts. That was the wrong call: **the path does not have to be
looked up, it can be computed.** `shadow_path.py` intersects the shadow axis with
the Earth's ellipsoid; `irish_tracks.py` traces the central line.

**Validation** (`validate_shadow_path.py`), against published points of greatest
eclipse, measuring geometry and timing separately:

| Eclipse | γ | closest approach of the computed line |
|---|---|---|
| 2017-08-21 | 0.437 | **0.2 km** |
| 1999-08-11 | 0.506 | **1.3 km** |
| 2015-03-20 | 0.945 | 13.1 km |

The 2015 figure is the honest limit, not a bug: at |γ| near 1 the axis meets the
Earth very obliquely, so arcseconds of lunar position become tens of kilometres on
the ground. Every question below is at the scale of hundreds of kilometres.

*(The 1999 case also caught an error in this project's own constants. A naive test
reported a half-degree miss; separating the two error sources showed the computed
track passes 1.3 km from the published point 64 s later than the time recorded
here — and the independent |γ| minimum agrees to within a second. The remembered
time was wrong, not the track.)*

### The tracks

Distance is from the central line; "TOTAL/partial" is what the site actually saw,
computed independently. The two are not the same test — at low Sun altitude the
umbra on the ground is an ellipse that stretches enormously, so a site can be far
from the centre line and still inside it.

| Eclipse | Central line ran over | Total at | Partial at |
|---|---|---|---|
| **594-07-23** | Ulster and the midlands — 13 km from Bangor, 18 km from Armagh, 78 km from Clonmacnoise | Armagh, Bangor, Clonmacnoise, Jarrow, Dunadd | **Iona (0.989)** |
| **664-05-01** | north Irish Sea — 40 km from Jarrow, 51 km from Bangor | Bangor, Jarrow | **Armagh (0.996)**, Iona, Clonmacnoise |
| **878-10-29** | **15 km from Armagh** | Armagh, Bangor | Clonmacnoise, Iona, Jarrow (all 0.99+) |
| **885-06-16** | 105 km from Iona, 158 km from Dunadd | **Iona, Dunadd only** | Armagh (0.972), Clonmacnoise (0.960) |
| 1133-08-02 | 36 km from Jarrow, 54 km from Iona and Dunadd | Jarrow, Dunadd, Iona | Armagh (0.963), Clonmacnoise (0.925) |
| 1140-03-20 | Wales; nowhere in Ireland or Britain central | — | all |

### Item 6 is settled

**The 878 path of totality passed 15 km from Armagh.** Iona was partial at 0.995,
Jarrow at 0.992. The popular secondary account placing totality in central and
northern Scotland is wrong; §2's magnitudes were right, and now they are backed by
a track rather than by point values alone. 1133 and 1140 come out where the
medieval sources put them, which is what licenses trusting the ninth-century
result.

### What this does to the "who was watching" question

Two of the audited notices now carry a site implication, and **they point in
opposite directions**:

* **AU 878 fits Armagh.** The most technically detailed notice in the set — feria,
  luna, hour, and a lunar eclipse a fortnight earlier — corresponds to an eclipse
  that was **total directly over Armagh**. That is exactly where the later annalistic
  tradition is normally placed.
* **AU 885 fits Iona, and that is the awkward one.** "Stars were seen" requires
  totality, and totality in 885 reached **only Iona and Dunadd** — Armagh saw
  0.972, Clonmacnoise 0.960. But 885 is a century and a half *after* the point at
  which the common source is usually taken to have moved from Iona to Ireland. If
  that notice is an eyewitness record, either the Ionan chronicle was still
  contributing in the 880s or AU drew on an Ionan source later than is usually
  assumed.

**And a warning against the obvious reading.** The two eclipses that were total
over *Ireland* are 594 and 878; the two total over *Iona* are 885 and 1133 — the
later pair. That is the reverse of the naive Iona-then-Ireland expectation, and
with a sample of five it means nothing on its own. It is a reason to run this test
properly on the full corpus rather than on the eclipses that happen to be famous,
and a reminder that §4's verdict on site discrimination — corroboration only,
never primary evidence — still holds.

**Both points inherit the verification debt on the wording.** If AU 885 does not
say stars were seen, the second bullet evaporates.

### One thing the tracks make sharper, and it is a real puzzle

If 878 was total over Armagh, an observer there watched the sun go out. The AU 878
notice, as far as this session could establish it, gives feria, luna and hour —
the apparatus of a computist — and **does not mention darkness or stars**, while
AU 885, recording an eclipse that was merely 0.97 at Armagh, reportedly *does*.
Three readings, and the text decides between them in an afternoon:

1. the 878 notice was written where it was not total, by someone with good
   calendrical data but no dramatic sight to report;
2. the two notices come from different compilers with different habits;
3. the 878 notice does mention darkness and this session's search-level text is
   incomplete — the most likely explanation, and the cheapest to check.

### A closed avenue, so nobody spends a session on it

It is natural to think an annalistic **hour** might locate the scriptorium, since
local time varies with longitude. It cannot, and the arithmetic is one line.
Irish and Ionan houses span **4.87° of longitude** — Skellig to Bangor — which is
**19.5 minutes** of local apparent time; Armagh against Clonmacnoise is **5.3
minutes**. An unequal hour on the relevant dates runs **37 to 86 minutes**. The
entire island is under half of the shortest unequal hour in the year, so no hour
statement can distinguish any two Irish sites, however precise the record or the
Δ*T*.

Latitude, not longitude, is what carries site information here — via which sites
the umbral track crossed, as in the table above. That is the only channel that
works, and §4 already prices it as corroboration rather than evidence.

---

## 10. Which hour convention? Three records cannot tell you — and that qualifies §1

Adding AU 764 (*Sol tenebrosus in hora tertia diei*, 4 June 764 — a real eclipse,
Irish magnitude 0.968, Rome 0.635) gives three annalistic hour statements, and
three is enough to ask which hour convention the annalists were using. Irish
computists knew more than one:

* **unequal interval** — "hora N" is the Nth twelfth of daylight, a span of 37–86
  minutes depending on the season. This is what §1 assumed.
* **unequal instant** — "hora N" is the canonical hour itself, the moment
  sunrise + N·h*, as terce, sext and none are points in the office rather than
  spans.
* **equinoctial** — "hora N" is N fixed hours after a 6 a.m. day-start, the
  convention of the computistical tables rather than the sundial.

Residuals at Armagh, in minutes, negative meaning the stated hour is early:

| Record | interval (mid) vs first / max | instant vs first / max | equinoctial vs first / max |
|---|---|---|---|
| AU 664 *hora nona* | −38 / −103 | **+0** / −64 | −51 / −115 |
| AU 764 *hora tertia* | −123 / −207 | −80 / −165 | **−5** / −90 |
| AU 878 *hora septima* | +35 / −40 | +58 / −16 | +72 / **−2** |
| **mean \|residual\|** | 65 / 117 | 46 / 82 | **43 / 69** |

Equinoctial wins on the mean, but **not by enough to believe, and the per-record
pattern is the giveaway**: 664 fits *instant-vs-first-contact* to the minute, 764
fits *equinoctial-vs-first-contact* to five minutes, and 878 fits
*equinoctial-vs-maximum* to two. Each record matches a *different* one of six
combinations almost perfectly.

With three records and six (convention × phase) combinations, that is what chance
produces. It is the trap `board/PRACTICES.md` calls *count the competitors, do not
score one*, and the honest reading of this table is that **three hour statements
cannot determine the convention.** The best mean residual, 43 minutes, is not much
better than a null in which the stated hour is placed at random within an hour of
the truth.

### What this does to §1

§1 read AU 664's ninth hour as first contact. That reading **assumes the unequal
interval convention**, and this section shows the assumption is not established.
Under the equinoctial convention "hora nona" is 15:00 local apparent time, 51
minutes *before* first contact — on which reading the annalistic hour is simply
early rather than exactly right.

**What survives every convention** is the load-bearing half, and it is worth
stating plainly because it is what the section is actually for:

> Maximum falls in the ninth hour under **none** of the three conventions —
> interval puts maximum in hour 10, instant leaves it 64 minutes later, and
> equinoctial 115 minutes later.

So the AU and Bede statements still cannot both describe maximum, and AU's cannot
describe maximum at all. That much is convention-independent, Δ*T*-independent and
stands. The stronger claim in §1 — that AU's hour *is* first contact — should be
read as one of two live readings, not as established.

**What would settle it:** a dozen hour statements rather than three. The full
442–1133 corpus plausibly contains them, and the same table computed over a dozen
records would separate 43 minutes from 65 with something like confidence. That is
a much better use of the hour data than trying to measure Δ*T* with it (§6).

---

## 11. Eclipse pairs: the sharpest cheap test left

AU 878 records a lunar eclipse and then a solar eclipse fifteen days later, and
says so — *"fifteen solar days having intervened"*. That clause is the most
interesting six words in the audited set. Noticing that two eclipses a fortnight
apart belong together requires either watching across a fortnight or knowing the
theory that puts them there. A chronicle that records isolated eclipses is
recording prodigies; one that records *both members of a pair and links them* is
doing something closer to astronomy.

`eclipse_pairs.py` finds every solar/lunar pair 12–18 days apart with both members
visible from Ireland:

| | |
|---|---|
| solar eclipses over Ireland at magnitude ≥0.50 | 171 |
| umbral lunar eclipses visible from Ireland | 710 |
| **pairs, both visible** | **93** (one every 8.7 years) |
| **"strong" pairs — solar ≥0.80 *and* lunar total** | **7** (one every 116 years) |

**The seven strong pairs in eight centuries:**

| Lunar member | Solar member | Gap |
|---|---|---|
| 561-05-15 (total, 1.006) | 561-04-30 (0.853) | 14.7 d |
| 807-02-26 (total, 1.037) | 807-02-11 (0.916) | 14.7 d |
| 810-12-14 (total, 1.021) | 810-11-30 (0.876) | 14.3 d |
| 854-08-12 (total, 1.143) | 854-07-28 (0.828) | 14.2 d |
| **865-01-15 (total, 1.075)** | **865-01-01 (0.999)** | 14.2 d |
| **878-10-15 (total, 1.054)** | **878-10-29 (1.025)** | 14.4 d |
| 966-08-04 (total, 1.205) | 966-07-20 (0.832) | 14.4 d |

**Two of the seven are years the annals already speak to.** AU 878 records both
members and links them. **AU 865 records the solar member** — "an eclipse of the
sun on the kalends of January", which is 865-01-01 exactly — and its partner, a
*total* lunar eclipse on 15 January 865, sits fourteen days later.

### The prediction, and it costs one lookup

**Does AU record a lunar eclipse in January 865?**

* If **yes**, then the one chronicle-linked pair becomes two, and the case that
  someone was systematically watching rather than noting prodigies gets much
  stronger — two pairs a decade apart is a habit, one is an anecdote.
* If **no**, the asymmetry is itself informative: the annalist recorded the solar
  member of a pair whose lunar member was total and unmissable, which points to
  selection by portent value rather than sky-watching, and bears directly on §8's
  availability argument.

The other five pairs are the same test at lower prior: 561, 807, 810, 854, 966.
**810 is worth a second look** for an unrelated reason — it is the year of Dúngal's
letter to Charlemagne on the solar eclipses of 810, one of the few securely dated
astronomical texts by a named Irish scholar. This canon finds only *one* solar
eclipse visible from Europe that year (30 November, Irish 0.876, Rome 0.872,
Constantinople 0.959); the other three were far southern (γ = −1.11, −1.40, +1.45)
and touched no European sky. Whether that is a problem for the "double eclipse"
tradition, or simply a misreading of it on this session's part, needs the letter
itself — which is why it is filed as a lead and not a finding.

### The base-rate warning, which decides how all of this reads

**Pairs are not rare.** They are the normal structure of an eclipse season, and 93
of them in 810 years is the expected consequence of the geometry, not a discovery.
Finding pairs in the canon proves nothing whatever. The informative quantity is
the *fraction* of available pairs the annals record, measured against the fraction
of isolated eclipses they record. Both denominators are now on disk; only the
numerators need the text.
