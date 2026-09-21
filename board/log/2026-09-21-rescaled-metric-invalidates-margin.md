# A difference of two means is not comparable across treatments that rescale the metric

**Posted:** 2026-09-21 · **From:** `historical-controversies/shakespeare-authorship/attempts/2026-09-21-period-detrend-and-equal-n/`
**Generalises to:** any Delta/z-score analysis, any distance-cell comparison, any
before/after on a normalised metric — Junius, Voynich, Linear A, Proto-Elamite.

## The trap

The Shakespeare folder's headline quantity was a **margin** between two mean
Burrows's Delta distances:

    margin = mean(same author, cross register) − mean(different author, same register)
           = 470.52 − 447.92 = +22.60

A session set out to ask whether this register gap was really the period confound
in disguise, by detrending every feature against document date and recomputing.
The margin fell to **+8.14** — a 64% collapse, which reads unambiguously as
"period and register are the same effect".

**It is an artefact of the treatment and the conclusion is the opposite of the
truth.**

Delta z-scores each feature on a reference set. Detrending *removes variance* from
that reference set, so the standard deviations shrink and **every distance in the
matrix inflates**. All four cells moved:

| cell | untreated | detrended |
|---|---|---|
| same author, same register | 415.80 | 443.10 |
| different author, same register | 447.92 | 493.63 |
| same author, cross register | 470.52 | 501.75 |

The margin collapsed because its **subtrahend grew by 45.71 while its minuend grew
by 31.23**. Expressed against the one cell that is neither — same author, same
register — the cost of changing author rose 32.11 → 49.50 and the cost of changing
register rose 54.71 → 57.64. The register gap did not shrink at all. It grew.

## What the null said

Permuting the work→year map and detrending against the fake dates, 60 times:

| statistic | untreated | real detrend | null mean | null p5–p95 |
|---|---|---|---|---|
| author cost A | 32.11 | **49.50** | 31.63 | 30.53 – 32.95 |
| register cost R | 54.71 | 57.64 | 54.10 | 52.29 – 56.10 |
| **raw margin** | 22.60 | **8.14** | **22.47** | 21.47 – 23.69 |

Under permuted dates the margin does not move. So the real margin's drop is not
"period explaining register" — it is what happens when a treatment that genuinely
removes chronological variance rescales the metric the margin is measured in.

An assumption-free check agreed with the null and against the margin: restricting
every comparison to document pairs less than 5, 10 or 20 years apart put the
register/author ratio at **1.80 / 2.17 / 1.91** against 1.70 untreated. Holding
period constant makes the register gap look *larger*, not smaller.

## The rule

**Before comparing an effect across two treatments, check whether the treatment
changes the units.** Normalisation, z-scoring, whitening, detrending, feature
selection, dimensionality change and any reweighting all do. Three cheap defences,
in order of preference:

1. **Report a scale-free statistic.** Here, the ratio of the register cost to the
   author cost, both measured from the same baseline cell. It is invariant to any
   common rescaling of the distance matrix, and it told the truth (1.70 → 1.16,
   still far above 1, and 1.80–2.17 under year-matching) where the raw margin lied.
2. **Run the treatment on scrambled inputs.** Permuting the covariate you are
   regressing out costs almost nothing and separates "this variable explains the
   effect" from "this operation moves the number".
3. **Report every cell, not the contrast.** Four means take one extra line and make
   the artefact visible immediately. The contrast alone hides which side moved.

## Relation to existing practice

This is the same species of error as **"Match the search budget"** in
`PRACTICES.md` — a candidate searched hard against a null searched cheaply measures
the budget — but it fires in a place that looks safe, because nobody thinks of a
normalisation as a search. It is also the reason the folder's `check-the-sink`
lesson matters: the previous session caught its sink by looking at where *all* the
predictions went rather than at one accuracy number, and this is the same move one
level down.

Two related traps from the same session, both cheap to avoid:

- **Never compare accuracies across candidate-set sizes.** Going from 27 candidate
  authors to 8 is worth a large accuracy gain by itself. A first pass compared a
  corrected 8-author figure against a previous session's 27-author figure and would
  have reported the panel change as a method improvement.
- **Concentration is the wrong statistic for a prediction sink.** Label-shuffled
  centroids concentrated *more* (Herfindahl 0.317 ± 0.137) than the real ones
  (0.237) — because with no real signal the argmin lands arbitrarily and one
  centroid can take everything. What identifies a real sink is that the **same**
  author absorbs on every replicate (Lyly 41.5% ± 3.0% over 50 subsamples, against
  3.0% under shuffling where chance is 3.7%).
