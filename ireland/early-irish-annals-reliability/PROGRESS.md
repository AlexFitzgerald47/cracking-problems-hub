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
