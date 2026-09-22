# Frozen predictions — 2026-09-22, before any determination was looked at

Written and committed **before** the session held a single Thera radiocarbon
determination. Everything below is derived from the IntCal20 calibration curve alone
(`data/intcal20.14c`, Reimer et al. 2020), which is the model, not the test data. The
determinations are being gathered in parallel and have not been seen at the time of this
commit. Board practice: `board/PRACTICES.md`, "Leap freely; freeze predictions before
testing them."

## What the curve alone already says

IntCal20 14C age on the calendar years at issue:

| cal BC | 1660 | 1650 | 1640 | 1630 | 1620 | 1610 | 1600 | 1590 | 1580 | 1570 | 1560 | 1550 | 1540 | 1530 | 1520 | 1510 | 1500 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 14C BP | 3374 | 3390 | 3381 | 3374 | 3347 | 3317 | 3310 | 3309 | 3313 | 3325 | 3314 | 3323 | 3303 | 3271 | 3279 | 3263 | 3223 |

Curve 1σ over this stretch is 11–12 14C yr. **1610–1540 BC is a ~70-year plateau of total
amplitude 22 14C yr**, i.e. about 1.4 curve-sigma and well under the measurement error of
a good sample. The years either side of it are not flat: 1650–1630 sits ~60 yr older,
1530–1500 sits 30–90 yr younger.

## The claim this session will test

**The century-gap dispute has two halves with completely different evidential status, and
the literature treats them as one.** Separating "eruption before ~1625 BC" from "eruption
after ~1535 BC" is something radiocarbon can do. Placing the eruption *within* 1610–1540
BC is something radiocarbon cannot do at any sample size, because IntCal20 is flat there.
Any published range narrower than ~70 years lying inside that window is therefore being
set by the model — phase priors, sequence constraints, wiggle-match ring offsets — and not
by the calibration of the determinations.

## Predictions (falsifiable, about evidence not yet held)

**P1.** The Akrotiri Volcanic Destruction Level (VDL) short-lived determinations, once
assembled, will have an error-weighted pooled mean in **3320–3365 BP**.
*Fails if the pooled mean falls outside that band.*

**P2.** A single VDL short-lived determination at 1σ ≈ 20–30 will calibrate under IntCal20
(uniform prior) to a 95.4% HPD **spanning ≥ 90 calendar years and containing both 1620 BC
and 1560 BC**. *Fails if any such single date gives a 95.4% HPD narrower than 90 years, or
one that excludes either anchor.*

**P3.** An R_Combine of the VDL short-lived set will be **multi-modal** inside 1700–1500 BC
(≥ 2 disjoint 95.4% HPD regions), and the mass split between the older (≈1620s) and
younger (≈1600–1540) modes will move by **> 20 percentage points** when the pooled 14C
mean is shifted by ±15 14C yr — a shift smaller than published inter-laboratory offset
claims. *Fails if the combined posterior is unimodal, or if it is that insensitive.*

**P4.** The published headline ranges on either side of this dispute (Friedrich et al.
2006's 1627–1600 BC; the mid-16th-century ranges of the Therasia olive and the annual-record
papers) **cannot both be recovered by single-date or R_Combine calibration of their own
determinations**. The difference will trace to model structure, not to the measurements.
*Fails if uniform-prior calibration of the published determinations reproduces both.*

**P5.** Calibrating the VDL set with a flat prior will give a 95.4% interval **≥ 40
calendar years wider** than the published modelled interval for the same data.
*Fails if the unmodelled interval is within 40 years of the modelled one.*

**P6 (the information bound — the load-bearing one).** No assembled VDL dataset of realistic
size (n < 50 determinations, 1σ ≥ 15) will separate **1610 BC from 1560 BC** at d′ ≥ 2. The
asymptotic ceiling computed from the curve alone, with measurement error driven to zero and
only the shared curve error left, is **d′ = 0.19** for that pair, and ≤ 0.9 for every pair
inside 1610–1540 BC. *Fails if any honest 14C-only analysis of these data separates two
years inside that window.*

**P7.** Because the olive-branch wiggle-match draws its precision from ring-count offsets
rather than from the calibration, the growth-ring objection is **not peripheral**: removing
the ring-offset constraint and calibrating its segments as an unordered set should collapse
its resolution to the full plateau. *Fails if the olive segments retain a sub-70-year range
without the ring-count constraint.*

## Pipeline reproduction check (must pass before anything above is believed)

Recover a **published** IntCal20-calibrated range for a named, published determination to
within **5 calendar years** at both 68.3% and 95.4%, using this repository's own engine
(`code/calib.py`) and no external calibration software. If that fails, the finding is a
bug, not a result.

## Method note recorded in advance

d′ between two candidate years for n determinations is **not** d₁·√n. The curve error is
*shared* — every sample dating the same calendar year sees the same μ(t) — so it does not
average down. The √n formula is an upper bound on power and the asymptotic ceiling above is
the honest one. Reporting √n scaling here would overstate what radiocarbon can do, which is
the direction this dispute already errs in.
