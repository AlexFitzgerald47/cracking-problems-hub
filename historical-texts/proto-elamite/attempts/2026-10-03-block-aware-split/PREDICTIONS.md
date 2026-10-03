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

---

# Addendum, frozen 2026-10-03 after P1–P5 were run, before P6–P7

The calibration run (`results/calibration.json`) produced one number I did not
anticipate and did not predict: under a null that destroys the within-face association
entirely, the **unblocked** training screen still selects M288–N45 with Fisher
p ≤ 7×10⁻⁶ in **20,000 of 20,000 draws** (train OR 8.1–11.8, p 10⁻¹⁷–10⁻²⁴). Verified
not to be a frozen-table bug: the train cell `a` varies 38–45 across draws.

That opens two new questions. Predictions for both are frozen here, before either is run.

## P6 — is the unblocked screen non-specific for the other seven pairs too?

Each of the eight 2026-09-04 pairs gets the same treatment: permute its target N-sign
within `(tablet, face)` over the whole corpus, and record the null distribution of the
**unblocked** corpus-wide Fisher p.

- **P6a.** I predict the screen is non-specific for **all eight** pairs — median null
  unblocked p below 10⁻⁵ for every pair — because the mechanism is tablet/face
  co-location, which is a property of administrative documents generally and not of
  M288 or N45.
- **P6b.** I predict the effect is **weaker for depleted pairs** (M297–N01, M263–N30C)
  than for enriched ones, because a depletion cannot be manufactured by co-location.
- **P6c.** If P6a holds, the `train_p`/`train_q` columns of
  `analysis/results/associations.csv` must be read as a **power filter, not evidence**,
  and that is a correction to how the published table reads — not a refutation of the
  validated associations, whose evidence is the blocked validation test.

## P7 — is M288–N45 a magnitude effect rather than a commodity association?

Descriptively (run before this addendum, so this is informed, not blind): N45 lines
carry a mean of 3.07 distinct N-signs against 1.32 elsewhere; N34 is 11.3× enriched and
N14 3.3× enriched on N45 lines, while N01 is *depleted* (0.571 vs 0.739). That is the
signature of a large quantity written out in an additive system whose lower members are
N01/N14/N34. And M288 is **not** the highest-N45-rate sign: M195 0.211, M056 0.190 and
M038 0.101 equal or beat M288's 0.101 — M288 leads the constraint set on its 557 lines
(power), not on its rate.

So the live alternative is: **N45 appears because the quantity is large, and M288 lines
carry large quantities.** The test holds the other numerals constant and asks whether
M288 adds anything.

- **P7a.** Stratifying on the exact multiset of **other** N-signs on the line (so every
  line in a stratum writes the same quantity apart from N45) and permuting N45 within
  stratum: I predict the M288–N45 association **weakens substantially** — the stratified
  odds ratio falls below half the unstratified 13.6 — but I do **not** predict it
  vanishes. Direction: still enriched.
- **P7b.** Under the strictest strata, `(tablet, face, other-N signature)`, I predict the
  test **loses power** — p-floor above 0.05 — because the strata will be nearly all
  singletons. If so that is a p-floor result, not a refutation, and must be reported as
  one.
- **P7c.** What would overturn the constraint: if the stratified test on the
  other-N signature has power (floor ≤ 0.05) and returns p > 0.05, then M288–N45 is a
  **magnitude artefact** and should be struck from the constraint set regardless of the
  block-aware result, because the face-blocked test does not control co-numeral content.
- **P7d.** What would strengthen it: if the stratified association survives with
  p < 0.05, M288–N45 is about M288 specifically and not about quantity size.

No numeral sign is assigned a value anywhere in P7. The strata are the observed
co-occurring signs themselves, so the test needs no metrology.
