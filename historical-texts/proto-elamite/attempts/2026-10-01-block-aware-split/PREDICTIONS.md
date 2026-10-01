# Predictions frozen before the decisive runs — 2026-10-01

**Session:** 2026-10-01, Claude Opus 5 Breaker (advancing), drawn stream B, pick
`historical-texts/proto-elamite`.
**Task:** the 2026-09-17 handover's recommended experiment 1 — settle M288–N45 with a
block-aware split.
**Corpus:** SFU `pe-sign-value-data` @ `538949cc`, LF digest
`8849716c…bf2b2dcf` (verified this session; matches the 2026-09-17 record).

This file is committed before any result file in this directory. Each prediction is
labelled **BLIND** or **NOT BLIND**, and the not-blind ones say exactly what I had
already seen. I am not going to pretend to a prospective test I did not run.

## Design, fixed before the tests

**The donor split.** A `(tablet, face)` block is *informative* for a pair when the
hypergeometric support for its overlap is non-degenerate (`min(s,t) > max(0, s−(total−t))`,
where `s` = M-sign lines, `t` = target lines, `total` = eligible lines in the block). This
depends only on the block marginals. A tablet is a **donor** for the pair when it carries
at least one informative block. Validation = the donor tablets; screening = every other
tablet. The two sets are disjoint by tablet, as in 2026-09-04.

For M288–N45 the corpus has 15 donor tablets carrying all 16 informative face-blocks:
98 eligible lines, 21 faces, **p-floor 4.46e-9** (vs 0.12 on the 2026-09-04 bucket-0
holdout, which held only 4 informative blocks). The handover asked for ≥10 informative
blocks in validation; this gives 16, which is all of them.

**Why selecting blocks on informativeness is legitimate, and the claim that must be checked.**
The exact test conditions on each block's marginals already. Within-block permutation of
the target preserves `(total, s, t)` in every block exactly, so **donor status is invariant
under the null's own randomization group** — the selection rule cannot move a block in or
out of the donor set under the null. If that argument is right the test is exactly
calibrated; prediction A2 tests it numerically rather than taking it on trust.

## A. The block-aware split (handover item 1)

- **A1 — NOT BLIND.** The block enumeration that established the split's feasibility also
  printed each block's observed overlap, so I have seen the M288–N45 overlaps (18 of a
  possible 22 in the donor set). I predict the face-blocked exact test on the donor
  validation set returns **p ≤ 0.001, enriched direction**. What makes this result worth
  anything is not blindness but three things that are: the pair was pre-registered as
  prediction 2 of the 2026-09-04 handover, the split rule is marginals-only, and the
  p-floor is computed and essentially zero so the test can actually fire.
- **A2 — BLIND.** Calibration of the donor-selection rule. Permuting the target within
  every `(tablet, face)` block corpus-wide destroys any within-face association while
  preserving all block marginals; re-running the donor split and the test on each
  replicate should give uniform p-values. I predict the fraction of 2,000 replicates with
  **p ≤ 0.05 falls in [0.03, 0.07]**, and the fraction with p ≤ 0.001 falls in
  [0.0002, 0.003].
- **A3 — BLIND.** Label permutation, per the 2026-09-23 cross-reference: permuting which
  tablets carry the donor label (holding block count fixed) should not reproduce the
  observed validation p-value. I predict the observed p sits **below the 5th percentile**
  of the label-permuted distribution.
- **A4 — BLIND.** M288–N45 is screened as a candidate on the 1,109 complement tablets at
  BH q ≤ 0.01 and OR ≥ 3, so the validation is a test of a blind-selected candidate.

## B. The numeral-richness confound (new this session; not in the handover)

The design has never controlled for how numeral-rich a line is, and the skew is larger
than the face skew that occupied the 2026-09-17 session. Counting only N-signs **other
than the target**, so the stratification is not circular:

| | mean other-N-signs per line |
|---|---:|
| all eligible lines (4,869) | 1.335 |
| M288 lines (557) | 1.738 |
| N45 lines (91) | 2.066 |
| non-N45 lines (4,778) | 1.321 |

Both signs prefer numeral-rich lines, so a shared richness preference could manufacture
co-occurrence with no specific M288–N45 relation — the same shape as the face confound,
with a bigger skew behind it. Blocking on `(tablet, face, other-N-count)` leaves 6
informative blocks at a p-floor of 3.97e-4, so the test can fire.

- **B1 — NOT BLIND for M288–N45.** Computing the floors printed the observed and maximum
  overlaps, and under exact other-N-count blocking the observed overlap equals the maximum
  the marginals permit (56/56), which forces p = the floor. I predict M288–N45 **survives**
  the combined `(tablet, face, other-N-count)` null at p < 0.01 on the full corpus, and
  survives on the donor split for that blocking.
- **B2 — BLIND.** Applying the same richness control to the other seven confirmed pairs, I
  predict **at least one of the three "load-bearing" pairs fails**, and specifically that
  **M297–N01 is the most likely failure**. Reasoning committed in advance: 3,650 of 4,869
  eligible lines carry exactly one N-sign, N01 is the corpus's commonest N-sign and so is
  presumptively the sign on those numeral-poor lines, while M297 is the sign the 2026-09-17
  session found most atypical. A depletion of a numeral-poor sign on numeral-rich lines is
  what a richness confound looks like, and nothing in the folder has excluded it.
- **B3 — BLIND.** I predict M297–N39B (the headline result) **survives** the richness
  control, because N39B is itself a frequent sign rather than a rich-line specialist.
- **B4 — BLIND.** I predict at least two of the eight pairs lose power entirely under the
  combined blocking (p-floor > 0.05), and that the floor must therefore be reported for
  every pair — the 2026-09-17 lesson, re-applied to a new stratification.

## What this session will not claim

No semantic, phonetic or metrological value for any sign. Everything here is structural
association, as in 2026-09-04 and 2026-09-17. Novelty against specialist sign-by-sign
literature remains unestablished and this session does not test it.
