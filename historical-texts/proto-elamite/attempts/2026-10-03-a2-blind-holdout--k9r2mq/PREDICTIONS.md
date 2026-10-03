# Frozen predictions — 2026-10-03 A2 blind-holdout session

**Committed before the corresponding code was run.** Written after seeing: the
corpus audit, the re-screen (1,056 tested / 54 selected), and the *published*
validation arm on bucket 0 (all 54 values). Written before seeing: any
face-blocked or co-numeral p-value on bucket 0 for a non-published pair, and
before any fold other than bucket 0 was ever computed by anyone in this folder.

## What is blind and what is not

- **Bucket 0 is not blind.** The 2026-09-04 design screened on buckets 1–4 and
  tested on bucket 0; this session has now re-derived all 54 of those bucket-0
  values. Any further bucket-0 test is a *statistic swap on seen data*, and is
  recorded below as exploratory, not as a warrant.
- **Buckets 1, 2, 3 and 4 have never been used as test sets** by any session in
  this folder. Folds 2–5 below are genuinely blind.

## Part 1 — exploratory, bucket 0, statistic swap (NOT a warrant)

The handover of 2026-10-03 proposed testing the tier-A2 pairs on bucket 0 under
face blocking and under the co-numeral control, BH-corrected over 54. Predictions:

- **P1.1** Under the **face-blocked** statistic on bucket 0, **zero** of the four
  in-family A2 pairs (M288–N39B, M288–N24, M376–N08A, M370–N39B) reaches
  q ≤ 0.05 over base 54. Reason: face blocking is a strict refinement of the
  published tablet-blocked test, so it cannot gain power on average, and the best
  of the four already stands at tablet-blocked q = 0.0954.
- **P1.2** Under the **co-numeral** statistic on bucket 0, **at most one** of the
  four reaches q ≤ 0.05 over base 54.
- **P1.3** Face-blocked p for M288–N39B on bucket 0 is **larger** than its
  published tablet-blocked p of 0.01591.

## Part 2 — pre-registered, blind: 5-fold cross-fitted screen-and-test

Design, fixed here before running: for each bucket b in 0..4, screen on the other
four buckets under the **unchanged** 2026-09-04 numeral rule (occupancy a+b ≥ 20
and a+c ≥ 20; training BH q ≤ 0.01; |OR| ≥ 3 or ≤ 1/3) and test on bucket b with
the **published** within-tablet exact randomization test, BH-corrected **within
that fold over that fold's own selected set**, plus the published direction,
effect-size (val OR ≥ 1.5 or ≤ 2/3) and minimum-5-validation-line criteria. Fold
1 (test = bucket 0) must reproduce the published eight exactly; it is the gate,
not evidence. Folds 2–5 are the blind test.

- **P2.1** Fold 1 confirms exactly the published eight. *(gate)*
- **P2.2** The union of pairs confirmed in at least one of folds 2–5 is **strictly
  larger than 8**. (This is the folder's "the published eight is a power-limited
  sample" hypothesis, stated as a prediction about data not used to derive it.)
- **P2.3** **M288–N45**, the folder's flagship A1 result, is confirmed in **at
  least one** of folds 2–5.
- **P2.4** **M297–N39B**, the strongest published pair (train OR 9.07), is
  confirmed in **at least two** of folds 2–5.
- **P2.5** **M288–N39B**, the densest tier-A2 pair, is confirmed in **at least
  one** of folds 2–5. If it is, the A2 tier's missing warrant is supplied by a
  blind test rather than by a statistic swap.
- **P2.6** **M297–N24** (tier D — refuted by a Simpson reversal through numeral
  composition) is confirmed in **at least two** of folds 2–5. Cross-fitting buys
  power, not composition control, so a composition artefact should *replicate*
  under this design. If it does, cross-validation is shown not to be a substitute
  for the composition control.

## Part 3 — null model (run after Part 2, prediction frozen here)

Null: permute whole N-sign sets among the eligible lines **within each tablet**,
destroying M–numeral association while preserving tablet structure, line counts,
and the joint composition of each numeral expression. Re-run the entire 5-fold
pipeline on each replicate.

- **P3.1** Median number of pairs confirmed in ≥1 fold under the null is **≤ 1**.
- **P3.2** The observed union count from Part 2 exceeds the **95th percentile** of
  the null distribution.
- **P3.3** The null's own fold-1 confirmation count has median **0**.

## Interpretation rule, fixed in advance

A tier-A2 pair may be promoted to A1 **only** via Part 2 — confirmed blind in at
least one fold whose test bucket is not 0, under the unchanged rule, with the
fold's own correction base. A Part 1 result may not promote anything, whatever it
shows. If Part 2 confirms nothing beyond the published eight, the conclusion is
that the published eight is **not** demonstrably a power-limited sample on this
corpus, and the A2 tier stays unwarranted.
