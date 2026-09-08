# Progress Log – Early Irish Annals Reliability

---

## 2026-09-03 – Initial seed

Problem folder created.

---

## 2026-09-05 – First substantive attempt: astronomical retro-calculation

**Session:** Claude Code (remote), cracker, mode *starting*.
**Took:** recommended experiment #1 from the 2026-09-03 seed handover — "systematic
comparison of eclipse and astronomical notices against modern astronomical
retro-calculation".
**Code and data:** `analysis/` (all of it reproducible offline; see
`analysis/README.md`).

### The constraint that shaped the session, stated first

Network egress in this environment is policy-restricted to code-hosting and
package registries. `celt.ucc.ie`, `archive.org`, `tcd.ie`, `dias.ie`,
`chronhib.maynoothuniversity.ie`, Wikipedia and Project Gutenberg are **all
blocked**, for `curl` and for the model's own fetch tool alike; the failures are
recorded proxy-side as 403 CONNECT denials, not transient errors. So the annal
*text* could not be obtained. This is worth writing down plainly because it is a
standing fact about this environment, not a one-off: **every text-corpus problem
in the Ireland lane (`1641-depositions-quantitative`,
`cromwellian-transplantation-compliance`, `famine-parish-register-mortality`,
`bmh-mspc-divergence`, `hearth-tax-population-reconstruction`) is blocked the same
way and cannot be started here.** What *is* reachable: PyPI, npm, and any public
repository on GitHub, GitLab or Bitbucket.

That rules out the textual half of this problem and leaves the astronomical half,
which needs no corpus at all — it can be computed. It had never been done on this
board, and it is the harder half to fake.

### What was built

An offline solar-eclipse engine (`analysis/astro.py`). Sun and Moon from the
analytic theories in Meeus (full VSOP87; abbreviated ELP-2000/82) via `pymeeus`;
explicit Julian/Gregorian calendar handling; topocentric geometry by full vector
subtraction rather than parallax approximations; magnitude, obscuration, Sun
altitude, and gamma.

Δ*T* is carried as an explicit parameter throughout, never as a hidden constant,
and the central values come from the **Stephenson, Morrison & Hohenkerk (2016)**
spline (with the Morrison et al. 2021 addendum), tabulated into
`analysis/results/delta_t_stephenson2016.csv`. This matters more than it sounds:
the Morrison & Stephenson (2004) long-term parabola — the formula a quick
calculation reaches for, and the one this session started with — is wrong by
−182 s at AD 664 and **−481 s at AD 1000**. 481 s is 2° of Earth rotation, about
220 km at Irish latitudes, which is a tenth of a magnitude on the edge of a
partial eclipse. The first canon run was thrown away and regenerated for this
reason.

Because Δ*T* enters *only* through the Earth's rotation angle, the Sun and Moon
are computed once per instant and only the observer is re-rotated, so every result
is emitted as a function of Δ*T* at no extra cost.

### Validation, before anything was believed

`analysis/validate_astro.py`, all passing:

* Meeus' worked examples — JD in both calendars and the inverse, weekday, GMST,
  solar theory (25.b), lunar theory (47.a);
* **eclipse magnitude against published circumstances at greatest eclipse** for
  2017-08-21, 1999-08-11 and 2015-03-20: agreement to ≤0.0005, with computed
  Sun–Moon separations of 0.3″, 24″ and 3.6″ at the published coordinates;
* **gamma** for the same three: agreement to ≤0.001 Earth radii;
* a negative control on a new moon that produced no eclipse.

And the finder itself (`analysis/count_check.py`): at the classical |γ| < 1.5433
limit it returns **228 solar eclipses for 1901–2000, which is exactly NASA's
published count** for that century. That is the check the whole study rests on,
because every recording-rate argument about the annals divides by this number.

**A bug this caught.** The first magnitude implementation used the partial-eclipse
formula everywhere and came out 1.5–2.7% low on all three modern eclipses. The
canons define the magnitude of a *central* eclipse as the ratio of apparent
diameters, not the covered fraction. Without the modern controls this would have
been invisible and would have biased every deep eclipse in the canon downwards.

### Result 1 — the AD 664 "ninth hour", and a crux that dissolves

The Annals of Ulster enter the 664 eclipse as darkness *in nona hora*; Bede
(HE III.27) dates the same eclipse to 3 May, *hora circiter decima*. The date
disagreement is old news and the astronomy settles it flatly — **there is no solar
eclipse on 3 May 664 visible from anywhere in Ireland or Britain**; 1 May is
correct. The *hour* disagreement has, as far as this session could establish,
never been used as a constraint. It is one, because the unequal ("canonical") hour
a phase falls in is a computable function of Δ*T* alone once the site is fixed.

At the published Δ*T* for AD 664 (4074 ± 40 s), on 1 May 664:

| Site | peak magnitude | first contact | maximum | last contact |
|------|---------------|---------------|---------|--------------|
| Armagh | 0.996 | **hour 9** | **hour 10** | hour 11 |
| Iona | 0.989 | **hour 9** | **hour 10** | hour 11 |
| Clonmacnoise | 0.963 | **hour 9** | **hour 10** | hour 11 |
| Jarrow (Bede's own house) | central | hour 10 | hour 11 | hour 11 |

An unequal hour that day was 77 minutes long.

So the two statements are not in conflict and neither is an error: **the annals'
ninth hour is first contact as seen from Ireland, and Bede's tenth hour is
maximum as seen from Ireland.** Maximum falls in the ninth hour at no value of
Δ*T* within ±600 s, so if one insists the annalistic hour describes maximum, the
annalistic hour is wrong; read as onset, it is exactly right.

Robustness: the ninth-hour/first-contact identification holds for Δ*T* ≥ 3834 s at
Iona and ≥ 3894 s at Clonmacnoise, comfortably inside the published value ± several
σ. **At Armagh it is marginal** — the boundary sits at ~4060 s against a published
4074 ± 40 s, so Armagh alone would not carry the result. It is Iona and
Clonmacnoise that do.

A second observation, offered as a lead rather than a conclusion: Bede's "about the
tenth hour" fits *Irish* maximum but not Jarrow's, where maximum fell in the
eleventh hour. Given the passage's subject that is suggestive of an Irish or
Ionan source behind Bede's hour, but *circiter* is doing real work in that
sentence and one unequal hour is within its reach. Not a finding.

### Result 2 — five records audited; five hit, and they hit *Ireland*

`analysis/record_audit.py` over `analysis/annal_records.csv`:

| Record | Date tested | Deepest Irish site | Irish mag | Rome | Constantinople |
|--------|-------------|--------------------|-----------|------|----------------|
| AU 594 | 594-07-23 | Armagh | **1.061** (central) | 0.557 | 0.438 |
| AU 664 | 664-05-01 | Armagh | 0.996 | 0.739 | 0.848 |
| AU 865 | 865-01-01 | Armagh | 0.999 | 0.694 | 0.513 |
| AU 878 | 878-10-29 | Armagh | **1.025** (central) | 0.891 | 0.831 |
| AU 885 | 885-06-16 | **Iona** | **1.077** (central) | 0.477 | 0.357 |
| Bede, 3 May 664 | 664-05-03 | — | **no eclipse** | 0.000 | 0.000 |

**This table is partly circular and the circularity has to be named.** The dates
were taken from the standard modern identifications, and those identifications
were themselves made by matching annal entries to computed eclipses. That five of
five "hit" is therefore not evidence of anything. What is *not* circular is
everything the identification did not use:

* **the depth contrast.** Every one of the five was substantially deeper over
  Ireland than over Rome or Constantinople — for AU 885, 1.077 at Iona against
  0.477 at Rome. A chronicle borrowing its eclipses from Mediterranean sources
  has no mechanism to produce that; the identification procedure does not select
  for it either, since it only matches dates.
* **AU 885's descriptive claim.** The notice adds "and stars were seen in the
  sky". Stars require essentially totality. Among the sites tested, the eclipse
  was central **only at Iona** (1.077); Armagh reached 0.972 and Clonmacnoise
  0.960, at which stars are not seen. If the descriptive detail is accurate, that
  notice was written at or near Iona and not in the Irish midlands. This is the
  single sharpest datum the session produced, and it is checkable.
* **AU 594's descriptive claim.** *Mane tenebrosum*, "a dark morning". Computed:
  first contact in the first hour of daylight, maximum in the second, central at
  Armagh and Clonmacnoise. The gloss is exactly right, on a record that sits
  *before* the AD 627 threshold from which McCarthy & Breen argued all such
  notices are local observation.
* **AU 878's four-part specification** — the best test on the board, because it
  states date, feria, luna and hour at once:
  * date: real eclipse, central at Armagh (1.025) — **confirmed**;
  * feria 4 (Wednesday): computed weekday Wednesday — **confirmed**;
  * "about the seventh hour": the seventh unequal hour fell inside the eclipse
    (first contact hour 6, maximum hour 8, last contact hour 9) — **consistent**,
    though one unequal hour (≈46 min that day) before maximum;
  * luna 28: the true lunar age at maximum was 29.42 d, so **the tabular moon
    was running 1.42 days behind the sky**. That is a measurement of the
    annalist's lunar table, not an error in the observation, and it is the kind
    of quantity the computistical literature argues about.

### Result 3 — the denominator, and how much any of this can decide

`analysis/find_eclipses.py` generated the full canon of solar eclipses AD
400–1210 with local circumstances at Armagh, Iona, Clonmacnoise, Bangor, Jarrow,
Rome, Constantinople and Alexandria, over a Δ*T* grid of ±300 s in 60 s steps.
Numbers are in `analysis/RESULTS.md`; the files are
`analysis/results/eclipse_canon.csv` and `eclipse_dt_curves.json`.

The point of it is the honest one: the observed-versus-borrowed question is only
answerable where the two hypotheses predict different eclipses, and often they do
not — a large eclipse over Ireland is frequently a fair-sized one over Rome too.
`analysis/visibility_analysis.py` computes that confusion rate and emits the two
lists where the hypotheses actually part company, plus a third list for a question
nobody on this board had asked: whether the annals can locate their own
observatory, given that Iona and Clonmacnoise are three degrees of latitude apart
and can sit on opposite sides of a penumbral limit.

### What failed, and what is owed

* **First canon run discarded.** Built on the 2004 Δ*T* parabola. Regenerated on
  the Stephenson spline once the error was quantified. ~25 minutes of compute lost;
  the point is that the parabola looks respectable and is not good enough here.
* **Magnitude convention bug**, above. Caught only by the modern controls.
* **The corpus is missing and the wording is unverified.** `annal_records.csv`
  carries six records whose quotations and annal-year attachments are at
  *search-engine level only*. Every row says so. The astronomy depends only on the
  dates, so the computed circumstances stand; anything resting on the *wording* —
  which is Results 1 and 2 in their interesting parts — inherits that debt. It is
  the first thing the next agent with fetch access should clear.
* **Six records is not a study.** McCarthy & Breen (1997) work from a corpus
  running 442–1133 that includes comets, aurorae and a possible supernova as well
  as eclipses. This session could not reconstruct it. The engine is built to take
  it the moment someone can.

### Addendum, same session — the canon completed, and two more results

**AU 878's fifth element confirmed.** The notice ends "fifteen solar days having
intervened", reporting a lunar eclipse a fortnight before the solar one.
`analysis/lunar_eclipses.py` (umbral geometry, validated against published umbral
magnitudes for 2018-07-27, 2019-01-21 and 2015-09-28 to ≤0.01, with a
no-eclipse negative control) finds a **total lunar eclipse on 15 October 878**,
umbral magnitude 1.054, greatest at 04:28 UT, with the eclipsed Moon **23° above
the horizon over Ireland and the Sun 23° below it** — a fully dark sky. The
interval between greatest-eclipse instants is 14.29 days, which is 15 days counted
inclusively in the Roman manner. So AU 878 states five things and four are
confirmed outright; the one that is off (luna 28 against a true lunar age of
29.42 d) is the one that comes from a table rather than from the sky.

**The canon.** 10,019 lunations scanned, **1,930 solar eclipses AD 400–1210**
(2.38/year, the long-run rate). From Ireland: 367 with any partial phase, 70 at
magnitude ≥0.80, 37 at ≥0.90, and **only 5 central eclipses in 810 years**. Three
of the six records tested fall on those five. Per-century counts are flat, so
nothing about the recording record can be attributed to a busier sky.

**Power, stated before anyone runs the experiment.** Of the 132 eclipses deep
enough for a chronicler on either side of Europe to notice, the
Ireland-versus-Mediterranean test can decide **28** and is **blind on 28** that
were large in both places. The decisive ones are written out as
`analysis/results/prediction_irish.csv` (11) and `prediction_borrowed.csv` (17).

**A negative result, reported as confidently as the positive ones.** The idea that
the annals might locate their own scriptorium — Iona against Clonmacnoise, three
degrees of latitude apart — is much weaker than it looks. In 810 years only 13
eclipses split the two sites by ≥0.10 in magnitude with the deeper one above 0.50,
only 3 by ≥0.25, and only 2 were central at Iona but not at Clonmacnoise. The
annals record a small fraction of eclipses at all, so expect a handful of usable
cases, never a distribution. **AU 885 happens to be one of the two**, which is why
that notice carries weight the test as a whole does not. This corrects the
optimism of item 4 in the handover written earlier in the same session; the
handover has been amended rather than rewritten.

**One further observation, from the finished canon.** The five central solar
eclipses visible from Ireland in AD 400–1210 are **594, 664, 878, 885 and 1133**.
Four of the five are the notices tested in Result 2 — which proves less than it
appears, because those notices were selected for being well known and that selects
for deep eclipses. The fifth does not have that problem: **1133 is the terminal
date of McCarthy & Breen's series of Irish astronomical records**, taken from an
abstract before the canon existed, and it falls exactly on the last central
eclipse over Ireland in the window. Offered as a lead for whoever has the text:
the Irish astronomical record may begin and end with the events that could not be
missed.

### Correction, same session — Result 1's second reading

The completed canon showed that the 664 eclipse was **central at Jarrow (1.041)**
and at Bangor (1.042); the track ran across Ulster and Northumbria. The first pass
did not have that number and used it to argue, wrongly, that Bede's hour pointed
away from Jarrow. It does not. Jarrow's **first contact falls in the tenth hour**
at every Δ*T* tested, so "about the tenth hour" fits a Northumbrian observation of
onset exactly as well as an Irish observation of maximum.

Both readings survive; the astronomy cannot separate them, and `analysis/RESULTS.md`
§1 now says so instead of asserting the first. What stands unchanged is the part
that carries the weight: neither hour is an error, and the ninth hour cannot
describe maximum anywhere in Ireland at any plausible Δ*T*.

### New this session — historical-regime validation, closing a real gap

`analysis/validate_astro.py` validates the ephemeris, the geometry and the
magnitude convention against three modern eclipses. It cannot validate the Δ*T*
**model**, because modern Δ*T* is measured rather than modelled — an error in the
historical spline would leave those checks completely unmoved. Δ*T* is the
dominant uncertainty in everything here: 300 s of it moves the shadow 125 km at
Irish latitudes, the difference between a total and a deep partial eclipse at a
given monastery.

`analysis/validate_historical.py` closes that gap with four attested medieval
eclipses whose *geography* is independently recorded, spanning Δ*T* from 1,088 to
4,074 s. All four pass:

| Eclipse | Δ*T* | Attested | Computed |
|---|---|---|---|
| 1133-08-02 | 1,110 s | total in Scotland | central at Iona (1.064) and Jarrow (1.065), not in the midlands |
| 1140-03-20 | 1,088 s | total in the English Channel | nowhere central, deeper south than north |
| 885-06-16 | 2,329 s | AU: stars were seen | central at Iona alone (1.077) |
| 664-05-01 | 4,074 s | near-total across Ireland | ≥0.95 at every Irish site, central at Jarrow |

**And one unresolved discrepancy, left standing rather than smoothed over.** For
878-10-29 this engine puts the central line over Ulster — Armagh 1.025, Bangor
1.025, against Iona 0.995 and Jarrow 0.989 — while a popular secondary account
puts totality in central and northern Scotland, the opposite placement. The
authoritative path maps are on blocked hosts and the secondary account is a news
article, so this session could not adjudicate. It matters: if 878 was total over
Armagh, the annalist watched a total eclipse, and the AU 878 notice — unlike
AU 885 — does not mention stars. Either it was written where it was not total, or
the two notices differ in style. A sharp question for whoever has the text.

### Bug found by cross-checking two of this project's own outputs

Worth recording in full, because it is the kind of error that survives review: it
is small, it is systematic, and it biases in the direction that makes results
look more conservative rather than less.

**Symptom.** For the 865-01-01 eclipse at Armagh, `analysis/results/eclipse_canon.csv`
gave magnitude 0.9951 while `analysis/record_audit.py` gave 0.999 for the same
eclipse, same site, same Δ*T*. A 10-second scan settles it at 0.99941. The canon
was wrong; the audit was right.

**Cause.** `find_eclipses.py` takes each site's maximum from a two-minute grid.
For an ordinary partial eclipse that costs about 0.0002, because the magnitude has
a smooth parabolic maximum. For a **near-central** eclipse it does not. When the
topocentric separation at greatest phase is small, the separation behaves like
|*v·t*| rather than a parabola — the magnitude has a **cusp**, falling roughly
0.016 per minute either side of maximum. A two-minute grid can therefore miss the
peak by that much, and it always misses *downwards*.

**Why it matters here and nowhere else.** The error is concentrated at the top of
the range, at the boundary between "deep partial" and "central" — which is exactly
the boundary the AU 885 argument stands on ("stars were seen" requires totality)
and the boundary the count of central eclipses over Ireland is defined by. The
other tools were never affected: `record_audit.py`, `hour_analysis.py` and both
lunar routines all refine their maxima by golden-section or ternary search rather
than reading a grid.

**Fix.** `analysis/refine_canon_peaks.py` re-refines every site magnitude at or
above 0.80 by golden-section search, which is where the error can reach 0.001 or
more; below that the grid is already good to a few times 10⁻⁴. The pre-refinement
canon is kept at `analysis/results/eclipse_canon_pre_refinement.csv` so the
correction is auditable rather than invisible.

**The lesson worth carrying to other problems on the board:** this was not found
by inspecting the code. It was found because two independent paths through the
same project computed the same quantity and disagreed in the fourth decimal
place. Building the second path was not redundant.

**And then the fix was wrong, which is the more useful half of this entry.**

The first version of `refine_canon_peaks.py` refined by golden-section search on
magnitude alone. It reported 420 corrections with a largest of **+0.0735** — five
times what the cusp mechanism can produce, which should have been the tell and was
not, until the corrections were tabulated with the Sun's altitude beside them:

| Date | Site | old → new | Sun altitude at the "improved" instant |
|---|---|---|---|
| 854-07-28 | Iona | 0.808 → 0.881 | **−1.6°** |
| 966-07-20 | Constantinople | 0.850 → 0.918 | **−1.7°** |
| 639-09-03 | Clonmacnoise | 0.945 → 1.000 | **−1.4°** |
| 550-11-24 | Jarrow | 0.868 → 0.921 | **−1.5°** |

Every large correction had the Sun **below the horizon**. For an eclipse still in
progress at sunset, the unconstrained maximum lies below the horizon, so the
search walked past sunset and reported magnitudes nobody could have seen. The
canon's original altitude filter was correct and the fix had quietly removed it.
The 639-09-03 case is the sharpest warning: it would have promoted a 0.945 partial
to a 1.000 *central* eclipse over Clonmacnoise — a fictitious total eclipse,
manufactured by a bug in a correction to a bug.

The real cusp effect is what the **median** correction shows: **0.0003**, with the
865-01-01 Armagh case at 0.004 the practical worst. It is a fourth-decimal
problem, not a first-decimal one.

`refine_canon_peaks.py` now scans at 4-second resolution *inside* the visible
window instead of optimising across it — deterministic, unable to leave the
horizon constraint, and with residual cusp error bounded around 0.0005. The
pre-refinement canon is kept for comparison.

**Two lessons, both cheap to state and expensive to learn:**
1. A correction is a change, and deserves the same scepticism as the thing it
   corrects. This one was believed for about ten minutes because it was labelled
   "fix".
2. The size of a correction is evidence about the correction. +0.0735 was five
   times what the stated mechanism could produce, and that discrepancy was
   visible in the output before any of the altitudes were looked at.

**Outcome of the refinement: nothing moved.** With the horizon constraint restored
and a 4-second scan inside it, 424 site-magnitudes were corrected; the median
correction is 0.00030 and the largest 0.0298, the latter on sunset-limited
eclipses where the two-minute grid's last above-horizon sample fell short of
actual sunset. **No eclipse crossed the central threshold, and every headline
count is unchanged** — 367 with any Irish partial phase, 171 at ≥0.50, 70 at
≥0.80, 37 at ≥0.90, 17 at ≥0.95, 5 central; the power analysis still gives 11 + 17
decisive against 28 blind. All four historical-regime checks still pass.

That is the result worth recording: **the bug was real and the conclusions were
not sensitive to it.** Reporting it as "found and fixed a serious error" would
overstate it; reporting nothing would leave the canon quietly wrong for the next
agent. `analysis/results/eclipse_canon_pre_refinement.csv` is kept so the whole
correction is auditable, and `validate_astro.py` now pins both failures with a
regression check on 865-01-01 at Armagh.

### The lunar canon, completed

10,018 lunations scanned; **1,993 lunar eclipses AD 400–1210, 1,266 umbral, 710
umbral visible from Ireland, 327 of those total.** Completeness checked as for the
solar finder: 230 for 1901–2000 against a published 229.

**The headline is an availability asymmetry.** A visible umbral lunar eclipse was
**4.2× as common** as a solar eclipse of magnitude ≥0.50, and at the spectacular
end the ratio is **65 to 1** — 327 total lunar eclipses against 5 central solar
ones in 810 years. A lunar eclipse is visible from the whole night hemisphere,
lasts hours, needs no accident of geography and can be looked at directly. The
annalists had vastly more opportunity to record lunar eclipses than solar ones,
and the comparison of recording rates is therefore a test of *motive* rather than
of accuracy: portent-selection versus sky-logging. It needs only the text.

**And the borrowing test is much stronger on lunar eclipses.** The solar version
is blind on 40% of candidates and forces a judgement about how deep an eclipse
must be before someone writes it down. Lunar eclipses are identical everywhere
they can be seen, so depth carries nothing — but visibility does, and Ireland and
Constantinople are 36° of longitude apart. Result: **197 decisive cases against
the solar test's 28**, on a yes-or-no discriminator.
`analysis/results/lunar_prediction_borrowed.csv` lists the 133 eclipses that were
below the Irish horizon throughout; **any one of them appearing in the annals is a
borrowing that cannot be explained away.**

Honest nuance: proportionally the lunar test is *blinder* than the solar one (91%
of the Irish set is shared with the Mediterranean, against 40% for solar), because
the night hemisphere is large. It wins on absolute numbers, not on sample purity.

### Handover item 6 settled by computing the track rather than looking it up

The earlier entry parked the 878 discrepancy on the grounds that authoritative
path maps are on blocked hosts. That was the wrong call and is corrected here:
the path does not have to be looked up. `analysis/shadow_path.py` intersects the
shadow axis with the Earth's ellipsoid and `analysis/irish_tracks.py` traces the
central line on the ground.

Validated against published points of greatest eclipse: **0.2 km** for 2017-08-21,
**1.3 km** for 1999-08-11, 13.1 km for 2015-03-20. The last is the honest limit
rather than a bug — at |γ| near 1 the axis meets the Earth so obliquely that
arcseconds of lunar position become tens of kilometres on the ground.

**Result: the 878 path of totality passed 15 km from Armagh.** Iona was partial at
0.995 and Jarrow at 0.992. The secondary account placing totality in central and
northern Scotland is wrong. 1133 (36 km from Jarrow, 54 km from Iona) and 1140
(Wales, nowhere in Britain or Ireland central) come out where the medieval sources
put them, which is what licenses trusting the ninth-century figure.

**The tracks also change the site picture, in both directions.** AU 878 — the most
technically detailed notice in the set — corresponds to an eclipse total *directly
over Armagh*, which is where the later tradition is normally placed. But AU 885's
"stars were seen" requires totality, and totality in 885 reached **only Iona and
Dunadd**; Armagh saw 0.972. That is a century and a half after the common source
is usually taken to have left Iona. Full discussion and the caveats in
`analysis/RESULTS.md` §9, including the warning that the two Ireland-total eclipses
are the *earlier* pair and the two Iona-total ones the *later* pair — the reverse
of the naive expectation, and meaningless at n = 5.

**Two errors of my own caught in the same pass**, both recorded rather than
quietly fixed:

* The first version of the track table sampled every 4 minutes. The shadow moves
  about 240 km in that time, so every distance was quantised by up to 120 km — it
  put Jarrow 269 km from the 664 track where the true figure is 186 km. Resolution
  of a derived quantity is part of the measurement. Now sampled at 20 seconds.
* "Distance from the central line" was being read as if it decided totality. It
  does not when the Sun is low: the umbra on the ground is an ellipse that
  stretches enormously at low altitude, so a site can be far from the centre line
  and still inside the shadow. The table now reports the computed totality
  alongside the distance, and they are labelled as different tests.

### Totality over Ireland: the denominator was wrong by a factor of 3.6

The canon's "five eclipses central over Ireland" meant *central at one of four
monasteries*. The umbra is a band a few hundred kilometres wide and crosses
Munster or Leinster without going near any of them. Tracing every central eclipse
and testing the track against points spread over the island gives **18** — one
every 45 years — plus 7 across Dál Riata. Full table with the Sun's altitude in
`analysis/RESULTS.md` §14 and `analysis/results/totality_over_ireland.csv`.

Two of the five already in the audited set vindicate the method: **AU 764's
eclipse was total over Dublin and Leinster with the Sun 55° up**, while all four
canon monasteries saw 0.91–0.97 — the magnitude table alone would never have
called it central, and the notice reads *sol tenebrosus*. **AU 865 was total over
Sligo**, likewise invisible to the four-site test (Armagh 0.995).

**Thirteen totality tracks have no notice in this session's record set.** Three
are the sharp ones, falling where the annals are dense and with the Sun high:
**733-08-14 (29°), 1039-08-22 (46°), 1191-06-23 (55°)**. The last is totality
across Louth and Meath on a June afternoon; an absence at 1191 bears directly on
the §7 question of the record ending at 1133.

`analysis/results/master_events.csv` merges every prediction set: **1,031 events,
242 decisive, 789 blind (77%)**. The blind count is the reason the file exists.

### Also closed in this block

* **The borrowing tests are blind to Northumbria** (§13). Not one solar eclipse in
  810 years was deep at Jarrow and shallow in Ireland; mean magnitude difference
  0.053 against 0.392 for Ireland–Mediterranean. So "diagnostic of local
  observation" means "not copied from the Mediterranean", which is weaker. Insular
  transmission is a textual-criticism question and no astronomical test reaches it.
* **Three of eight identifications are forced** (§12) — a chronological anchor
  rather than a matching exercise — with the conditioning on identifiability
  stated so the 1-in-343 arithmetic is not mistaken for a p-value.
* **Three hour statements cannot fix the hour convention** (§10), which qualifies
  §1 and is now cross-referenced from it.
* **Seven strong eclipse pairs in 810 years** (§11), two of them years the annals
  speak to, giving the January 865 lookup as the cheapest high-value test left.
