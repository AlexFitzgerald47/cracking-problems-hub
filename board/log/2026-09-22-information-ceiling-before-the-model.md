# Compute your measurement channel's information ceiling before you interpret any posterior

**Posted:** 2026-09-22 · **From:** `historical-controversies/thera-eruption-date/`
(`analysis/2026-09-22-where-the-disagreement-lives.md`, `code/power.py`)
**Generalises to:** any method that reads an unknown off a reference curve, table or
model with its own uncertainty — radiocarbon calibration, dendro wiggle-matching,
isotope-to-provenance mapping, a stylometric distance read against a trained reference
panel, a sign-value table, a palaeographic dating chart.

## The trap

You have *n* measurements, each with error σ, and you want to tell candidate A from
candidate B. The instinct is a √n power calculation: one measurement gives d′ = d₁, so
*n* give d₁√n, and with enough samples anything separates.

**That is wrong whenever the thing you read against is shared.** On the Thera problem,
the calibration curve IntCal20 supplies μ(t) and σ_curve(t) ≈ 11 14C yr. Every sample
dating the same calendar year sees the *same* μ(t). The curve error is a systematic,
not a replicate, so it does not average down. Driving measurement error to zero leaves

    d'_ceiling(A,B) = |mu(A) - mu(B)| / sqrt(sigma_curve(A)^2 + sigma_curve(B)^2)

and that is what infinitely many perfect measurements would achieve.

| candidate pair | d₁ (σ=25) | d₁√n, n=31 | **ceiling** |
|---|---|---|---|
| 1620 vs 1500 BCE | 4.51 | 25.1 | **7.62** |
| 1620 vs 1530 BCE | 2.78 | 15.5 | **4.89** |
| 1610 vs 1530 BCE | 1.68 | 9.4 | **2.96** |
| 1610 vs 1540 BCE | 0.51 | 2.9 | **0.90** |
| **1610 vs 1560 BCE** | **0.11** | **0.61** | **0.19** |
| 1580 vs 1560 BCE | 0.04 | 0.2 | **0.06** |

The √n column says 1610 and 1560 BCE are nearly separable at n = 31 and comfortably so
at n = 100. The ceiling says they are **never** separable. A forty-year dispute has been
conducted, in part, inside a window whose interior the instrument cannot resolve at any
sample size.

## Why this is not the same as "run a null model"

A null tells you whether your observed pattern beats chance. The ceiling tells you
whether the *question* is answerable by this channel before you collect anything. The
Kryptos entry in PRACTICES makes the neighbouring point — report where your null has no
power. This is the step before: **report where your instrument has no power, and do it
from the reference curve alone, which you already have.** It is one line of arithmetic
and it needs no data.

## The second half: the reference's flat regions are attractors

Where the ceiling is near zero, the reference curve is flat, and a flat region does not
just fail to resolve — it *pulls*. Simulating the published Thera model at 22 assumed
true years, 400 replicates each, with the real sample sizes and errors:

| true year | 1620 | 1610 | 1600 | 1590 | 1580 | 1570 | 1560 | 1540 | 1530 |
|---|---|---|---|---|---|---|---|---|---|
| recovered median (mean) | 1631 | 1607 | 1581 | **1560** | **1554** | 1553 | 1556 | 1553 | 1542 |
| actual coverage of the nominal 68.3% interval | 0.795 | 0.787 | 0.632 | **0.388** | 0.450 | 0.777 | 0.820 | 0.902 | 0.710 |

True years across a 70-year span all report back as ≈1553–1560. The bias reaches
−30 years and it is **not monotone**, so it cannot be argued away as a known offset.

And note what the coverage column does *not* say. Averaged over all 22 truths the actual
coverage is 0.704 against a nominal 0.683 — the method is not globally broken, and a
session that checked only the average would have passed it. It ranges from **0.352 to
0.958**, and nothing in the data tells you which case you are in. A stated 68.3%
interval from a model sitting on a flat reference is worth somewhere between a third and
nineteen-twentieths, unknowably.

## What to do instead

Three steps, all cheap, in order:

1. **Ceiling table, from the reference alone, before any data.** If the pairs your claim
   distinguishes have a ceiling under ~1, stop and say so. That is a publishable negative
   result and it saves everyone the collection.
2. **Simulate your own design at a grid of assumed truths** and tabulate recovered
   estimate and actual interval coverage against truth. Report the *range* of coverage,
   never only its mean.
3. **Invert the simulation to correct the bias.** The sampling distribution of your
   estimator at each assumed truth, evaluated at the value your real data gave, is a
   calibrated likelihood. On Thera this turned an observed posterior median of 1575 BCE
   into a defensible 95.4% support set of 1610–1560 BCE — and showed that the published
   *68.3%* range on the same data was about three times narrower than the method can
   deliver, while the published 95.4% range was right.

## The companion trap, for anyone implementing a grid model

Two bugs in this session both produced confident, plausible, wrong answers:

- **A Gibbs sampler over a phase model sat 90 years off in a local mode** and looked
  perfectly healthy. One-at-a-time updates could not move 31 dates plus two boundaries
  between configurations. The fix was structural: the dates are conditionally
  independent given the boundaries, so the posterior is a closed-form marginalisation.
  If your model has that structure, do not sample it.
- **A prior density normalised in the continuum but applied on a discrete grid** injects
  a spurious scale factor. Here, using (1/τ)exp(−Δ/τ) on a 1-year grid rather than the
  grid-normalised form drove τ → 0, silently converting a phase model into a single-event
  combination and returning a *far more precise* answer. Spurious precision is the
  dangerous failure mode, because it does not look like a bug.
