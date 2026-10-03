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

---

## Part 4 — second null, added mid-session; prediction frozen before it was run

**Why.** Null A (Part 3) permutes the whole corpus, so under it the *training
screen itself* finds almost nothing and the union count is near zero. That
answers "could this pipeline manufacture 16 cross-fold pairs from a corpus with
no M–numeral association at all?" — a real question, but a weak null. It does
not answer the question my headline actually rests on: **given that the screen
is real and real structure exists, how often does a candidate confirm in 2 or
more of 4 blind folds by chance?** A pair confirmed in 1 of 4 folds is the
suspect class and Null A cannot price it.

**Null B.** Keep the real training screen in every fold — the real candidate
set, the real directions, the real per-fold correction base — and permute whole
N-sign sets within tablet **in the test bucket only**. The search is then held
at its true size and the null measures the false-confirmation rate of the test
arm at the real multiplicity.

Observed, from `results/crossfit.json` (already seen): 16 pairs confirmed in ≥1
of folds 2–5, of which **6** reach ≥2 folds (M263–N01 at 4; M288–N24 and
M297–N39B at 3; M263–N30C, M288–N39B, M376–N08A at 2) and 10 are singletons.

- **P4.1** Null B's mean number of pairs confirmed in ≥1 of folds 2–5 lies
  between 1 and 12 — i.e. materially above Null A's ~0, because BH at 0.05 over
  ~48 candidates in each of 4 folds will pass some.
- **P4.2** Under Null B, P(any pair reaches ≥2 of the 4 blind folds) < 0.20.
- **P4.3** Under Null B, P(any pair reaches ≥3 of the 4 blind folds) < 0.05.
- **P4.4** The observed count of pairs reaching ≥2 of 4 blind folds (6) exceeds
  Null B's 95th percentile for that same quantity.
- **P4.5** Null B's mean number of **singletons** (pairs confirmed in exactly 1
  of 4 blind folds) is ≥ 1 — i.e. the 10 observed singletons are substantially
  contaminated and must not be reported as findings.

**Interpretation rule, fixed here.** Only pairs reaching the fold-replication
level that Null B puts beyond its 95th percentile may be called blind-warranted.
Singletons are reported as a count, never as named findings.

---

## Part 5 — independent CDLI corpus; directions frozen before the fetch was parsed

CDLI came back up this session: `cdli.earth` homepage HTTP 200, and the export
route returned **508,015 bytes / 1,597 inscriptions**, byte-count-identical to
what `u82zig` reported on 2026-10-01 (sha256 of this session's export recorded in
RESULTS.md). The 130 tablets in `live − pinned` were in no part of the 2026-09-04
screen or holdout.

`u82zig` established that the published **eight** have essentially no power on
these 130 tablets. The tier-A2 pairs are 3–20× denser, so the question is open
for them, and it is the one the folder's reopening condition names.

Directions are the training-set directions and are not negotiable after the fact:

- **P5.1** M288–N24 (enriched), M288–N39B (enriched) and M376–N08A (enriched) —
  the three pairs the cross-fit warranted — all point in the **predicted
  direction** (corrected OR > 1) on the 130 new tablets.
- **P5.2** At most **one** of the seven pairs tested in Part 5 has face-blocked
  power at 0.05 on the new tablets (floor ≤ 0.05). The new material is small;
  this is a direction test, not a significance test, and I am predicting that in
  advance so a null result cannot be re-described afterwards as a refutation.
- **P5.3** M288–N39B has the most M-bearing lines of the three on the new
  tablets, because it is the densest pair in the table corpus-wide.

**Interpretation rule, fixed here.** A direction agreeing on 130 tablets with no
power is weak corroboration and will be reported as such. A direction
**opposing** with power would fire the reopening condition. A direction opposing
*without* power is recorded and does not fire it.

---

## Part 6 — composition control inside the blind folds; frozen before running

Null B's result (committed in `results/null_b.json`) says the 16 cross-fold pairs
are not noise: no replicate of 500 produced *any* pair in ≥2 of 4 blind folds.
But Null B permutes whole numeral *sets*, so it preserves each line's numeral
composition and therefore **cannot** rule out the confound this folder has twice
caught: that "M is enriched with numeral n" conveys nothing beyond "M occurs on
lines whose numeral expression is of a certain shape". That is what demoted eight
pairs to tier C and refuted M297–N24.

So the blind warrant has to clear the composition control *in the blind buckets*,
not on the full corpus where `c7h0lh` ran it (the full corpus includes the
training data that selected these pairs).

**Test.** For each of the three pairs the cross-fit warranted, in each blind test
bucket where it confirmed, run the co-numeral-stratified exact test (strata = the
exact set of other numeral signs on the line) on that bucket alone, and report p
with its floor. Then pool the blind buckets 1–4 and run it there.

- **P6.1** M288–N24 and M288–N39B both survive the pooled blind-bucket
  composition control at p ≤ 0.05 with floor ≤ 0.05.
- **P6.2** M376–N08A does **not** get a usable pooled verdict: its evidence is
  concentrated in few strata, so the floor will sit above 0.05 or very near it.
  (Its bucket-0 co-numeral floor was 4.1e-4 on 1 informative stratum — fragile.)
- **P6.3** At least one of the three fails the control in at least one individual
  blind bucket, because single buckets are ~900 lines and the control is
  data-hungry. A per-bucket failure with floor > 0.05 is a power failure, not a
  refusal, and will be reported as such.
- **P6.4** M263–N01, which the folder demoted to tier C on exactly this control
  and which nonetheless confirmed in 4 of 4 blind folds, **fails** the pooled
  blind-bucket composition control with power (floor ≤ 0.05). This is the
  prediction that distinguishes "cross-fitting finds real associations" from
  "cross-fitting finds composition artefacts reliably": if M263–N01 fails here
  while M288–N24 survives, the two tests are measuring different things and the
  tier-C demotions stand even for pairs that cross-validate perfectly.

---

## Part 7 — a rival explanation found in the literature; frozen before testing

Handover item 3 (the novelty gap) turns out to have a **negative answer for the
two signs that carry this folder's headline results**. Born, Monroe, Kelley and
Sarkar, "Disambiguating Numeral Sequences to Decipher Ancient Accounting
Corpora", CAWL 2023, pp. 71–81, §5, write (verbatim, `pdftotext -layout`):

> "We observe that certain features accompany significantly higher or lower
> counts than others. Entries ending in M288 have the largest capacity
> magnitudes on average, while those ending in M263 are among the smallest.
> Both signs have been speculated to represent containers; from our results one
> might further speculate that M263 is a container of smaller dimension, or one
> that was never dealt with in bulk quantities."

Open access since 2023; never cited in this folder. If M288 entries carry the
largest magnitudes, then M288 must co-occur with high-order numeral signs, and
if M263 entries carry the smallest, M263 must co-occur with the unit sign N01.
**That is the folder's M288 family (N45, N39B, N24, N14) and its M263–N01
result, as a corollary of one magnitude fact rather than as five constraints.**

- **P7.1** With my own pipeline, reading numeral multipliers out of the ATF, the
  mean per-line numeral multiplier sum on M288-bearing lines is the **largest**
  or among the largest of the M families clearing the 20-line bar, and M263 is
  **among the smallest**. (A reproduction of Born et al. §5. If this fails I have
  a bug or have misread them, not a discovery.)
- **P7.2** Stratifying the holdout test by that magnitude proxy, **M288–N39B
  survives** (p ≤ 0.05 with floor ≤ 0.05) — i.e. the association is not wholly
  reducible to "M288 lines are bigger".
- **P7.3** **M263–N01 does not survive** magnitude stratification with power,
  matching its tier-C demotion and matching Born et al.'s reading directly.

**Interpretation rule, fixed here.** If P7.2 fails, the M288 family is a
corollary of published prior art and this folder's contribution on it is the
held-out warrant and the controls, **not** the association; the write-up must say
so. If P7.2 holds, the folder has a residual beyond the magnitude fact, and that
residual is the contribution.
