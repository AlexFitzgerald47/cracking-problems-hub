# Predictions, frozen before the tests they govern

**Session:** 2026-10-03, Claude Opus 5 Breaker (advancing), stream B draw.
**Drawn next move:** 2026-09-17 handover experiment 1 — settle M288–N45 with a
block-aware split.

This file is committed **before** any result file in this directory. What it can and
cannot claim is stated honestly below, because one part of the drawn experiment cannot
be prospective and saying so is cheaper than pretending otherwise.

---

## What is already visible to me, and therefore cannot be predicted

Before writing this file I ran `src/blockdiag.py` and `src/budget.py`, which print the
**per-block observed overlap** for M288–N45 on every informative `(tablet, face)` block
in the corpus, and the 2026-09-17 session already published the bucket-0 aggregate
(15 of a possible 16). So:

> **The block-aware split test of M288–N45 is NOT a prospective test and will not be
> reported as one.** I have seen the per-block outcomes. Any single split I choose
> could be cherry-picked to maximise significance.

Two things are done about that, both pre-registered here:

1. **No split is chosen.** `src/blockaware.py` enumerates **every** allocation of the
   informative-block tablets that meets the specification, and reports the **whole
   distribution** of validation p-values over admissible splits — not one split.
2. **The split rule may read only block marginals** (`total`, `s`, `t`) and never an
   observed overlap. The exact conditional test conditions on exactly those marginals,
   so a selection that is a function of them alone leaves the null distribution intact.
   That is an argument, so prediction P2 below tests it by simulation rather than
   asserting it.

## P1 — prospective, against a corpus not yet in hand

A retrieval researcher is looking for a current CDLI Proto-Elamite export. I have not
seen it. If an independent or newer export is obtained, then on it:

- **P1a.** M288 is **enriched** with N45 (corrected OR > 1) on the new tablets.
- **P1b.** The three load-bearing pairs hold in direction: M297–N39B enriched,
  M263–N01 enriched, M263–N30C depleted.
- **P1c.** The face-blocked test for M288–N45 on new tablets alone will **lack power**
  (p-floor > 0.05) unless the export adds more than ~400 eligible lines, because
  informative blocks for this pair arrive at roughly 16 per 4,869 eligible lines.

## P2 — calibration of the split rule, pre-registered before running

Under a null that destroys the association but preserves what the test conditions on:

- **P2a.** Permuting N45 **within each `(tablet, face)` block** leaves every block
  marginal unchanged, so the marginal-only split rule selects the **identical** split in
  every draw, and the validation p-value is **uniform** on its discrete support.
  Expected: P(p ≤ 0.05) ≈ 0.05, no excess.
- **P2b.** Permuting N45 **within tablet** (the looser null, which lets N45 move between
  faces and so *includes* the face-confound freedom) will also leave the validation
  p-value uniform or conservative. P(p ≤ 0.05) ≤ 0.05.
- **P2c.** If either comes out anti-conservative, the block-aware split is an invalid
  procedure and the drawn experiment must be reported as refuted, not completed.

## P3 — the label-permutation null on the split itself

Per the 2026-09-23 cross-reference (every post-hoc split carries the permutation null at
the same search budget):

- **P3a.** Permuting the validation/train **label** across the informative-block tablets,
  holding each tablet's blocks in place and preserving sizes, will show the observed
  split's validation p-value is **not** unusual within that distribution — i.e. the
  split does not buy the result. I predict the observed split lands between the 10th and
  90th percentile of the label-permuted distribution.

## P4 — what would change the verdict on M288–N45

Stated now so it cannot be reverse-engineered from the result:

- **Confirmed** if the admissible-split distribution puts the **median** validation
  p-value below 0.05 with a p-floor below 0.05, P2 passes, and P3 shows the split is not
  load-bearing.
- **Refuted as a face artefact** if the median validation p-value exceeds 0.05 while
  p-floors are below 0.05 — i.e. the test had power and did not fire.
- **Still untestable** if admissible splits cannot simultaneously give a validation
  p-floor ≤ 0.05 and a complement that re-screens the pair.

## P5 — block-size robustness

- **P5a.** I predict the result is **not** carried by the two-line `total=2` faces alone.
  Restricted to blocks with `total ≥ 3`, the full-corpus face-blocked test will still
  reach p < 0.05.

*(P5a is honest-but-not-blind: `src/budget.py` had already printed the stratum, so it is
recorded as a check I had already seen, not as a frozen prediction. It is listed so the
write-up cannot later promote it.)*
