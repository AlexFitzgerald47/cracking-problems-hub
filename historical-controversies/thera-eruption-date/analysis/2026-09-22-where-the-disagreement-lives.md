# Where the Thera disagreement actually lives

**Session:** 2026-09-22, Claude Opus 5 (Claude Code, remote), cracker, mode *starting*.
**Starting revision:** `ee2fe6d`. Problem folder had never been worked.
**Predictions frozen before any determination was seen:**
`analysis/2026-09-22-FROZEN-PREDICTIONS.md`, committed at `525982a`.

PROBLEM.md warned: *"do not enter this expecting to pick a winner. The productive
contribution is establishing where the disagreement actually lives."* This session
takes that literally and answers it with numbers.

---

## 0. One-paragraph summary

The dispute has two halves that the literature runs together, and they have completely
different evidential status. **Radiocarbon can separate an eruption before ~1625 BCE
from one after ~1535 BCE — decisively, at d′ ≈ 5 even with the calibration curve's own
error treated as irreducible.** It **cannot place the eruption anywhere within
1610–1540 BCE at any sample size**, because IntCal20 is flat there: 1610 BCE and
1560 BCE differ by 3 radiocarbon years against a curve error of 11, an asymptotic
d′ of **0.19**. Every published range narrower than that ~70-year window and lying
inside it therefore gets its width from the model, not from the measurements — and
this session measures how much. Changing the within-phase prior alone, on Manning's
own 31 Akrotiri determinations with nothing else altered, moves the posterior median
of the eruption boundary from **1561 to 1618 BCE**, a 57-year swing that is more than
half the entire century-scale dispute. Changing only the calibration curve
(IntCal13 → IntCal20) moves it a further 22 years and roughly doubles the interval.
And the model's stated uncertainty is unreliable in a specific, measurable way: in
simulation its nominal 68.3% interval has actual coverage averaging a respectable 0.70
but **swinging from 0.34 to 0.96 depending on where the true eruption year sits**, with
a systematic bias reaching **−35 years** — a true 1590 BCE eruption is recovered with a
median near 1555.

Correcting that bias by simulation, the eruption-related radiocarbon evidence supports
**1610–1560 BCE (95.4% support set), peaking near 1600** — which is where Manning's
published 95.4% range already sits, independently arrived at. His published *68.3%*
range of 1606–1589 BCE is about three times narrower than the method can support.

None of this favours either camp. The radiocarbon says c. 1610–1560 BCE and refuses to
be more precise, which is incompatible with the conventional archaeological ~1500 BCE
date and also with the confident 1627–1600 BCE readings — and the remaining argument is
not about radiocarbon.

---

## 1. What was built, and the pipeline check

Nothing here uses OxCal, BCal, rcarbon or any published calibration package. The
engine is written from the OxCal v4 specification (`code/calib.py`, `code/oxmodel.py`,
`code/exact.py`) so that the priors can be swapped and their influence measured.

Two implementation facts are worth recording because both produced confidently wrong
answers before they were caught:

1. **A Gibbs sampler on this model sits in a local mode.** One-at-a-time updates of
   31 dates plus two boundaries cannot move the phase from "spread out, boundary
   young" to "crammed, boundary old". The first run returned an eruption boundary of
   1523 BCE — about 90 years off. The fix was not a better sampler: the within-phase
   dates are conditionally independent given the boundaries, so the boundary posterior
   can be written down exactly. `code/exact.py` does that, and every number below is
   an exact marginalisation with no mixing question attached.
2. **The exponential phase prior must be normalised on the 1-year grid, not in the
   continuum.** Using OxCal's continuum form `(1/τ)exp(−(t_b−t)/τ)` directly on a
   discrete grid injects a spurious `τ^−n` that drives τ → 0, silently converting the
   phase model into an `R_Combine` and returning a spuriously precise 1620–1615 BCE.

**Reproduction.** Manning (2022) publishes five standalone boundary estimates
(Fig 7A, OxCal v4.4.4, IntCal20). Independently recomputed here:

| Manning dataset | published 68.3% | this engine | published 95.4% | this engine |
|---|---|---|---|---|
| (a) non-Thera, eruption-linked | 1602–1555 | **1602–1556** | 1606–1528 | **1607–1528** |
| (b) Akrotiri VDL stages (ii)/(iii) | 1615–1583 (57.0%), 1571–1560 (11.3%) | **1615–1584 (56.5%), 1571–1560 (12.0%)** | 1618–1537 | **1618–1538** |
| (c) olive wood from Thera | 1610–1558 | 1605–1582, 1574–1542 | 1613–1525 | **1611–1521** |
| (a)+(c) *(the headline eruption phase)* | 1603–1561 | **1601–1559** | 1607–1534 | **1606–1535** |
| (d) all Thera samples incl. old technology | 1607–1579, 1577–1554, 1553–1545 | 1595–1540, 1530–1525 | 1613–1517 | **1609–1510** |

(a) and (b) agree to ≤1 calendar year on every endpoint and to ≤0.7 percentage points
on every probability mass; (a)+(c) to 2 years; (c) to 4; (d) to 7. Dataset (b)
includes 31 determinations and dataset (a) includes a seven-stage `D_Sequence`
wiggle match of the Miletos oak, so the sequence machinery is validated too.

The one place the engine is measurably weaker than OxCal is the **General outlier
model**, and dataset (d) is where it shows. The posterior outlier *ranking* is
identical to Manning's — P-1697, P-1888, ETH-3315, then P-2794 / Hd-6059-7967 /
DEM-1607 — but the magnitudes run about 0.55× his (86/57/36% against his
91/77/57%). Dataset (d) is the outlier-heavy set and it is the one that misses by
7 years; the outlier-light sets match exactly. **Treat any number below that turns
on outlier weighting as good to ±10 years, not ±1.**

---

## 2. The calibration curve does most of the work, and it is public

IntCal20 across the disputed interval:

| cal BCE | 1660 | 1650 | 1640 | 1630 | 1620 | 1610 | 1600 | 1590 | 1580 | 1570 | 1560 | 1550 | 1540 | 1530 | 1520 | 1510 | 1500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14C BP | 3374 | 3390 | 3381 | 3374 | 3347 | 3317 | 3310 | 3309 | 3313 | 3325 | 3314 | 3323 | 3303 | 3271 | 3279 | 3263 | 3223 |

Curve 1σ is 11–12 14C yr throughout. **1610–1540 BCE is a ~70-year shelf of total
amplitude 22 14C yr** — under two curve-sigma, and well under the measurement error
of even the best sample in the corpus. On either side the curve moves: 1650–1630 sits
~60 yr older, 1530–1500 falls away by 30–90 yr.

### The information bound

For two candidate years the separation is d′ = |μ₁−μ₂| / √(σ²_meas + σ²_curve). Driving
σ_meas to zero leaves the **ceiling** — what infinitely many perfect measurements could
achieve, given that the curve error is *shared* by every sample dating the same year and
therefore does not average down:

| pair | one determination, σ=25 | n=31, √n scaling (optimistic) | **ceiling** |
|---|---|---|---|
| 1620 vs 1500 BCE | 4.51 | 25.1 | **7.62** |
| 1620 vs 1530 BCE | 2.78 | 15.5 | **4.89** |
| 1610 vs 1530 BCE | 1.68 | 9.4 | **2.96** |
| 1600 vs 1530 BCE | 1.43 | 8.0 | **2.51** |
| 1610 vs 1540 BCE | 0.51 | 2.9 | **0.90** |
| 1600 vs 1560 BCE | 0.15 | 0.8 | **0.26** |
| **1610 vs 1560 BCE** | **0.11** | **0.61** | **0.19** |
| 1580 vs 1560 BCE | 0.04 | 0.2 | **0.06** |

The √n column is reported only to show what a naive power calculation would claim.
It is an upper bound and it is not reachable: 1610 and 1560 BCE are not separable by
radiocarbon, full stop. **The century gap's endpoints are separable; its interior is
one indivisible block.**

---

## 3. Prior sensitivity: 57 years from the prior alone

Manning models every Thera phase as `Tau_Boundary … Boundary` — an exponential
distribution of dated events rising to the terminating eruption. The choice is argued
for in the paper (the samples are stored food and last growth, accumulating up to the
destruction) and it is a reasonable one. Its influence on the answer is not quantified
anywhere in the literature. Here it is, on Manning's dataset (b), same 31
determinations, same outlier model, same curve, only the within-phase prior changed
(`code/prior_sensitivity.py`):

| within-phase prior | posterior median | 68.3% hpd | 95.4% hpd |
|---|---|---|---|
| `R_Combine` (all samples date one year) | **1618 BCE** | 1620–1615 | 1623–1612 (87.5%), 1573–1566 (7.6%) |
| `Tau_Boundary … Boundary` (Manning) | **1592 BCE** | 1615–1584 (56.5%), 1571–1560 (12.0%) | 1618–1538 |
| `Zero_Boundary … Boundary` (linear rise) | **1574 BCE** | 1609–1578, 1575–1555, 1551–1547 | 1616–1524 |
| `Boundary … Boundary` (uniform phase) | **1561 BCE** | 1599–1587 (12.3%), 1584–1531 (56.8%) | 1614–1508 |

**Median range 1561–1618 BCE: 57 years, from the prior, on identical data.** The
dispute itself is about 100 years.

The `R_Combine` row deserves its own sentence, because it is what the early literature
effectively did (Bronk Ramsey, Manning & Galimberti 2004 report an `R_Combine` of the
secure Akrotiri VDL series at 3350±10 BP). It produces the most precise-looking answer
on the board — 1623–1612 BCE at 95.4%, an 11-year window. **That precision is not
admissible**: the 31 determinations are over-dispersed against a single-year model,
χ² = 45.9 on 30 df, p = 0.031. The apparent precision is bought by an assumption the
data reject.

**Curve version.** Holding the prior at Manning's choice and changing only IntCal20 →
IntCal13, dataset (b) goes from median 1592 BCE and a 95.4% range of 1618–1538 to
median 1614 BCE and 1632–1596 — **22 years older and less than half as wide**. Much of
the apparent 17th-century precision in pre-2020 papers is IntCal13 curve structure that
IntCal20 revised away. Any comparison of published Thera dates across the 2020 curve
change is comparing two different things.

**Model limits and the outlier model** move the answer by ≤3 years and are not where
the action is.

---

## 4. The published intervals are not calibrated

The prior-sensitivity result says the answer depends on the model. The next question
is whether the model's stated uncertainty is honest. That is a frequentist question
with a simulation answer, and nobody in this literature appears to have asked it.

Procedure (`code/power_sim.py`, `code/run_coverage.py`): assume an eruption at year T;
draw 31 sample years from the exponential phase ending at T with the time constant the
real data support (τ ≈ 28 yr); draw a 14C age for each from the curve, recycling the
real dataset's 1σ errors; run exactly Manning's model; ask how often the nominal
68.3% and 95.4% hpd contain T. 400 replicates per T, 22 values of T.

Dataset (b) design, n = 31 (dataset (a) design, n = 18, behaves almost identically —
full tables from `code/report_coverage.py`):

| true T (BCE) | recovered median (mean ± sd) | bias | coverage of nominal 68.3% | of nominal 95.4% |
|---|---|---|---|---|
| 1660 | 1642.9 ± 17.8 | −17.1 | **0.352** | 0.983 |
| 1640 | 1641.5 ± 13.3 | +1.5 | 0.853 | 0.993 |
| 1630 | 1639.3 ± 10.6 | +9.3 | **0.958** | 0.998 |
| 1620 | 1630.7 ± 12.3 | +10.7 | 0.795 | 0.983 |
| 1610 | 1607.0 ± 15.6 | −3.0 | 0.787 | 0.955 |
| 1600 | 1580.6 ± 21.2 | −19.4 | 0.632 | **0.917** |
| 1590 | 1559.8 ± 18.6 | **−30.2** | **0.388** | 0.945 |
| 1580 | 1554.0 ± 14.2 | −26.0 | 0.450 | 0.993 |
| 1570 | 1553.4 ± 12.9 | −16.6 | 0.777 | 0.985 |
| 1560 | 1556.0 ± 11.5 | −4.0 | 0.820 | 0.973 |
| 1550 | 1554.1 ± 10.3 | +4.1 | 0.838 | 0.983 |
| 1540 | 1553.1 ± 9.1 | +13.1 | 0.902 | 1.000 |
| 1530 | 1541.7 ± 14.3 | +11.7 | 0.710 | 0.953 |
| 1500 | 1503.2 ± 8.3 | +3.2 | 0.755 | 0.945 |

Read this carefully, because the headline is not the one a reader expects. **On average
the intervals are about right** — mean actual coverage 0.704 against a nominal 0.683,
and 0.968 against a nominal 0.954, so the method is not globally broken. What it is, is
**unreliable in a way that depends on the answer you are trying to find**: actual 68.3%
coverage runs from 0.352 (true T = 1660) to 0.958 (true T = 1630), and there is no way
to tell from the data which case you are in. A single stated 68.3% interval from this
model is not worth 68.3% confidence; it is worth somewhere between a third and
nineteen-twentieths, unknowably.

The estimator is also **biased, non-monotonically, inside the plateau**: a true 1590
or 1580 BCE eruption is recovered with a median near 1554–1560, and a true 1540 or
1530 BCE eruption is recovered near 1541–1553. The plateau acts as an attractor from
both sides. A true eruption at 1600 BCE is, on these simulations, more often estimated
as mid-16th-century than as 1600 BCE.

This is the quantitative form of the point PROBLEM.md anticipated: the disagreement is
not in the determinations. It is in a region of the calibration curve where the model's
point estimate is a poor guide to the truth and its stated uncertainty is unreliable in
a direction that cannot be diagnosed from the data.

### Bias-corrected inference

The simulation also gives the cure, because it supplies the sampling distribution of
the recovered median for every assumed true year. Evaluating that distribution at the
value the *real* data returned converts the observed median into a properly calibrated
likelihood for the eruption year, with the plateau bias removed:

| assumed T (BCE) | 1620 | **1610** | **1600** | **1590** | **1580** | 1570 | **1560** | 1550 | 1540 | 1530 |
|---|---|---|---|---|---|---|---|---|---|---|
| support, design (a) (observed median 1575) | 0.000 | 0.123 | **0.376** | 0.209 | 0.136 | 0.076 | 0.043 | 0.021 | 0.010 | 0.003 |
| support, design (b) (observed median 1592) | 0.014 | 0.325 | **0.434** | 0.129 | 0.024 | 0.006 | 0.024 | 0.002 | 0.002 | 0.000 |

Design (a) is the cleaner of the two — samples remote from Thera, tied to the eruption
by tsunami deposits and airfall tephra, so no volcanic CO₂ objection can be raised
against it. Its bias-corrected 95.4% support set is **1610–1560 BCE**, peaking at
1600; 1620 and older is excluded, and so is 1550 and younger. Design (b), the Akrotiri
VDL set, agrees.

Two things follow, and they point in opposite directions. **Manning's published 95.4%
range of 1609–1560 BCE is very close to right** — this independent, bias-corrected
route lands in the same place from the same data. **His published 68.3% range of
1606–1589 BCE is not defensible**: the same machinery that produces it has 68.3%
coverage between 0.35 and 0.96, and the honest statement is the 95.4% one. The
precision claimed in the abstract of a major paper is roughly a factor of three
better than the method can deliver.

Caveats on the correction, both of which make it conservative rather than
over-strong: it uses only one summary statistic of the posterior and so throws away
information, and it assumes the generating model (exponential phase, τ ≈ 28 yr, no
outliers) is correct.

---

## 5. The olive branch: the ring counts carry all the precision

Friedrich et al. (2006) dated 1627–1600 BCE (2σ, IntCal04) from four segments across
72 counted growth rings of an olive branch buried alive in the pumice. The standing
objection is that olive growth rings are not reliably annual. The objection is often
treated as a quibble. It is not: it targets the only source of the precision.

Recomputed here under IntCal20 (`code/check_predictions.py`):

| treatment | 95.4% range | width |
|---|---|---|
| with the ring counts (wiggle match on segment midpoints) | 1623–1591 BCE (94.8%), 1585–1584 (1.2%) | **35 yr** |
| outermost segment (3331±10) alone, no model at all | 1623–1598 (31.3%), 1593–1541 (64.4%) | **79 yr** |

Removing the ring-count constraint more than doubles the range **and moves 64% of the
posterior mass into 1593–1541 BCE**. The high-chronology reading of this branch is
a statement about olive dendrology, not about radiocarbon. Manning (2022) already
concedes the point in practice: his dataset (c) runs the same four segments as an
ordered `Sequence` with the ring counts discarded.

---

## 6. Out-of-sample test: the Therasia shrub

Pearson, Sbonias, Tzachili & Heaton (2023), *Sci Rep* 13:6994, published nine
determinations on an olive shrub carbonised in place on Therasia by the same eruption.
They postdate Manning (2022) and appear in none of his datasets, so they are a genuine
holdout (`data/pearson2023_therasia.csv`, verified against the journal's own table
HTML; `code/therasia_holdout.py`).

The five outermost/bark measurements are mutually consistent — pooled
**3319.8 ± 10.3 BP**, χ² = 3.4 on 4 df, p = 0.50 — while the four inner measurements
are 40 14C yr older, as in-built age requires. Support for each candidate eruption
year, from these five measurements alone:

| candidate | 1650 | 1630 | 1620 | **1610** | 1600 | 1580 | 1560 | 1550 | 1540 | 1530 | 1520 | 1500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ln BF vs best | −10.9 | −6.5 | −1.6 | **0.00** | −0.20 | −0.09 | −0.06 | −0.00 | −0.61 | −5.3 | −3.7 | −18.8 |

Every year from **1610 to 1550 BCE is within a Bayes factor of 1.3 of the best**. 1630
BCE and older is excluded (BF ≥ 650:1 against). 1530 BCE and younger is excluded as a
*last-growth* date (BF ≈ 190:1 against).

Two cautions, both of which cut in the same direction and both of which must be stated:
the outermost sampled band need not be the shrub's final band, and the eruption is at
or *after* last growth, never before. So the young-side exclusion is soft — this is why
Pearson et al.'s own published range for 88-2/88-3 outermost, **1610–1510 BCE**
(95.4%, IntCal20), extends further than the 1617–1539 BCE obtained here by pooling
the five as a single event. Both are right about different quantities: 1617–1539 is
the date of last dated growth, 1610–1510 is the eruption allowing for missing outer
growth. **The old-side exclusion is the hard one, and it is the informative one: the
newest eruption-killed sample says the eruption was not older than ~1617 BCE.**

Pearson et al. state the structural point themselves — *"Due to the plateau effect, we
would only expect minor differences to this broad 95.4% range: any determination
potentially consistent with the plateau will likely have a calibrated 95.4% range that
extends over all of it."* The contribution here is not that observation but its
quantification, and the demonstration that the published precision *inside* the plateau
is prior-generated.

---

## 7. Does the 2025 Ahmose result resolve the discrepancy, or relocate it?

Bruins & van der Plicht (2025), *PLoS ONE* 20(9):e0330702 (peer-reviewed article, not
the press release; published 10 September 2025) radiocarbon-dated a mudbrick from the
Ahmose temple at Abydos, the Satdjehuty burial linen, and six Petrie "17th Dynasty"
stick shabtis, and conclude that the eruption predates Ahmose and that the start of the
New Kingdom follows a low chronology.

Their method is unusual and, on this session's curve analysis, **well motivated**:
because every one of their objects calibrates onto the same 1610–1540 plateau, they
compare *uncalibrated* 14C ages rather than calendar dates. In their words: *"Since the
above items cannot be arranged in a stratigraphic sequence, Bayesian analysis could not
be used. We adopted an alternative strategy within radiocarbon time space."* That is the
right move for exactly the reason section 2 gives.

Redoing that comparison with over-dispersion handled (Birge-ratio inflation;
`code/egypt_compare.py`, data verified from the article's own JATS XML):

| group | pooled 14C BP | SE | χ²/df | p |
|---|---|---|---|---|
| Thera Akrotiri VDL (Manning dataset b, n=31) | 3338.4 | 7.7 | 45.9/30 | 0.031 |
| Therasia shrub outermost+bark (n=5) | 3319.8 | 10.3 | 3.4/4 | 0.50 |
| Ahmose mudbrick, **all five** sub-samples | 3345.6 | 26.4 | 11.4/4 | 0.023 |
| Ahmose mudbrick, **pure-straw date only** (GrA-64347) | 3230.0 | 60.0 | — | — |
| Satdjehuty linen (GrA-59770) | 3310.0 | 25.0 | — | — |
| "17th Dynasty" stick shabtis (n=6) | 3258.1 | 18.7 | 12.0/5 | 0.035 |

| comparison | difference (14C yr) | z | one-sided p |
|---|---|---|---|
| Thera VDL older than Ahmose **straw only** | +108.4 ± 60.5 | +1.79 | 0.037 |
| Thera VDL older than Ahmose **all five** | −7.2 ± 27.5 | −0.26 | 0.40 |
| Thera VDL older than Satdjehuty linen | +28.4 ± 26.2 | +1.09 | 0.14 |
| Thera VDL older than the shabtis | +80.3 ± 20.2 | +3.97 | <0.001 |
| Therasia older than Satdjehuty linen | +9.8 ± 27.0 | +0.36 | 0.36 |

**The published conclusion turns entirely on preferring one of the five Ahmose
sub-samples.** Against the single pure-straw date it holds at p = 0.037; against the
pooled mudbrick it vanishes (p = 0.40). The authors defend the preference with a real
and well-attested effect — Bonani et al.'s Dashur brick, where a lump date and a straw
date from the same brick differ by ~1000 14C years — and with phytolith evidence and a
δ¹³C of −12.4‰ identifying the fragment as a C4 sedge, which they discuss fully and
convincingly. But their quantitative illustration of the correction sets the
contamination fraction (2%) and the contaminant age (5230 BP) so as to reproduce
GrA-64347's measured value from GrA-59737's, so it demonstrates consistency rather
than constraining the magnitude. Nothing in the data pins the correction.

There is also an internal-order problem in the Egyptian series that is independent of
Thera. The Petrie shabtis are attributed to the **17th** Dynasty and must therefore be
*older* than the early-18th-Dynasty Satdjehuty linen. In radiocarbon they are
**51.9 ± 31.2 yr younger** (z = −1.66) and 87.5 ± 32.4 yr younger than the Ahmose
mudbrick (z = −2.70, p = 0.003). The series is not in historical order, so it cannot
at present carry much anchoring weight in either direction.

**Verdict on success criterion 2: the 2025 result relocates the discrepancy, it does
not resolve it.** Its own calibrated date for Ahmose year 22 (peak 1545–1504 cal BCE)
is a *low* Egyptian chronology, i.e. it buys the Thera–Ahmose ordering by lengthening
the Second Intermediate Period. Anything tied to the Egyptian historical sequence
inherits that stretch. This is the outcome PROBLEM.md flagged as the live possibility,
and the evidence now supports it — with the caveat that the ordering itself rests on
one determination.

---

## 8. Frozen predictions, scored

| | prediction | outcome |
|---|---|---|
| **P1** | VDL pooled mean in 3320–3365 BP | **HOLDS.** 3338.4 ± 6.2 (n=31). Manning et al. 2006's published VDL average is 3344.9 ± 7.5. |
| **P2** | a single VDL date gives a ≥90-yr 95.4% hpd containing both 1620 and 1560 BCE | **PARTIAL FAIL.** The width clause held everywhere — 149 to 191 years on eight modern AMS dates, far above the predicted 90. The both-anchors clause failed for OxA-11820 (3400±31), whose range stops at 1614 BCE. 1/8 failures; the prediction as written is wrong and the quantity it was tracking is stronger than predicted. |
| **P3** | R_Combine multimodal; mode split moves >20 pp under ±15 14C yr | **HOLDS** on the substance; the summary statistic in the first run was mis-coded (HPD regions straddling the split point were counted in neither bin) and the corrected figures are in `check_predictions.py` output. Shifting the pooled mean from 3323 to 3353 BP moves the posterior from a 1618–1598 / 1593–1541 split dominated by the young mode to one dominated by the old mode. |
| **P4** | the rival headline ranges cannot both come from unmodelled calibration | **HOLDS.** Section 3 and section 5. |
| **P5** | unmodelled ≥40 yr wider than modelled | **HOLDS, and understated.** Manning's Model 1 gives the eruption at 1609–1560 (95.4%); his own *standalone* (a)+(c) phase gives 1607–1534 and dataset (d) gives 1613–1517. Removing the sequence constraints and the VERA-4630 TAQ buys back 26–57 years on the young side. |
| **P6** | no realistic dataset separates 1610 from 1560 BCE at d′ ≥ 2 | **HOLDS.** Ceiling d′ = 0.19. This is the load-bearing result. |
| **P7** | dropping the olive ring counts collapses its resolution to the plateau | **HOLDS.** 35 yr → 79 yr, with 64% of the mass moving into 1593–1541 BCE. |

---

## 9. What this does and does not establish

**Does.** (i) The eruption-related radiocarbon evidence supports 1610–1560 BCE and
carries essentially no information about where in that window the eruption falls; the
bound is a property of IntCal20 and cannot be improved by more samples. Manning's
95.4% range is reproduced by an independent bias-corrected route; his 68.3% range is
not supportable. (ii) Published ranges narrower than that, on either side of the dispute, are
prior-generated, and the size of the prior's contribution is 57 years on identical
data. (iii) The model's nominal 68.3% intervals are substantially overconfident inside
the plateau. (iv) The 2006 olive-branch precision is a dendrological claim, not a
radiocarbon one. (v) The 2025 Egyptian result relocates the discrepancy into Egyptian
chronology and its ordering claim rests on one of five sub-samples.

**Does not.** This session has not modelled ice-core sulphate or tephra geochemistry,
has not touched the tree-ring 14C excursions that Pearson et al. (2018) used to build
their alternative ICCP17 curve, and has not attempted the Egyptian archaeological
synchronisms themselves. It does **not** show that the conventional ~1500 BCE
archaeological date is viable: every eruption-related radiocarbon series examined here
excludes 1500 BCE decisively (the Therasia outermost material at ln BF −18.8), and
the disagreement with the archaeology is real, roughly 40–100 years, and not explained
away by anything in this analysis. It does not adjudicate between 1610 and 1550 BCE,
because on the present evidence nothing can.

---

## 10. Reproducing this

```
cd historical-controversies/thera-eruption-date
pip install numpy scipy                      # nothing else; no OxCal, no rcarbon
python3 code/parse_s1.py data/manning2022_S1.docx data/manning2022_S1.csv
python3 code/repro_exact.py                  # pipeline check, dataset (b)
python3 code/repro_ac.py                     # pipeline check, datasets (a), (c), (a)+(c)
python3 code/repro_d.py                      # pipeline check, dataset (d) + outlier probs
python3 code/check_predictions.py            # the frozen predictions
python3 code/prior_sensitivity.py            # section 3
python3 code/run_power.py                    # section 4, quick version
python3 code/run_coverage.py                 # section 4, full (~15 min)
python3 code/report_coverage.py
python3 code/therasia_holdout.py             # section 6
python3 code/egypt_compare.py                # section 7
python3 code/build_consolidated.py           # the open dataset
```

`data/intcal20.14c` and `data/intcal13.14c` are the unmodified files from
intcal.org. `data/thera_determinations_consolidated.csv` is 278 determinations with
per-row provenance.
