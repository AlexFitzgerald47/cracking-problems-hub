# Predictions frozen before the block-aware split was run

**Session:** 2026-10-01, Claude Opus 5 Breaker (advancing), drawn stream B.
**Corpus:** SFU `pe-sign-value-data` at pinned commit
`538949cca949a176400b144ef49c2036e9dc82a6` (LF digest
`8849716c6afbf963e5ee02535da013c87c931c61e88e2c05ced9cd58bf2b2dcf`).

This file is committed **before** any result file in this directory. The split code
(`block_split.py`) and the marginal survey (`marginal_survey.py`) are committed with it,
because the split is designed from block marginals alone and those are not the quantity
under test. The validation overlaps, p-values and null models had not been computed when
this was written.

## What is already known, and therefore not a prediction

Honesty first, because it bears on how much any "confirmation" below is worth.

The 2026-09-17 session already reported that on the **full corpus** the face-blocked test
for M288–N45 has 16 informative blocks and passes at p = 1.0×10⁻⁴. The full corpus is
train ∪ validation under any split. So a significant validation p-value here is **largely
foreknown** and is not the contribution. Three things are genuinely open:

1. whether a split exists that gives validation ≥10 informative blocks **while train
   still independently re-screens the pair** under the published rule;
2. whether the result survives a null that permutes the target within faces and re-runs
   the entire design, split search included;
3. what the evidence actually consists of once the forced co-occurrences are separated
   out — the marginal survey shows 38 of the 59 maximum co-occurrences are **forced** by
   face marginals, leaving only 21 units of freedom. That number has not appeared in this
   folder before and it is the quantity any claim about this pair rests on.

## Predictions

**P1 — train re-screens the pair.** With ~10 of the 15 informative tablets moved into
validation, the published screening rule on train alone (BH q ≤ 0.01, corrected
OR ≥ 3, ≥20 sign-lines, ≥20 target-lines) still selects M288–N45 as a candidate.
*Rationale:* N45 occurs on 91 eligible lines corpus-wide and the informative tablets
hold only a minority of them; the screen is unblocked and keeps the forced
co-occurrences. **Confidence: moderate.** This is the prediction most likely to fail,
and if it fails the experiment does not deliver a confirmation of a screened candidate.

**P2 — the design reaches power.** The validation face-blocked p-value floor for
M288–N45 is ≤ 0.01, i.e. two orders of magnitude below the 0.12 floor that defeated the
bucket-0 holdout. *Rationale:* eleven of the sixteen informative blocks are two-line
faces with s = t = 1, each a fair coin under the null, so ten such blocks alone put the
floor near 2⁻¹⁰ ≈ 10⁻³.

**P3 — the pair confirms.** Validation face-blocked p ≤ 0.05, and M288–N45 is
`confirmed` under the published confirmation rule (BH q ≤ 0.05 across the re-screened
candidate set, same direction, validation OR ≥ 1.5, ≥5 validation sign-lines).
*Largely foreknown — see above. Stated so it is on the record, not as a discovery.*

**P4 — the design does not manufacture significance.** Under a null that permutes N45
presence among lines **within each (tablet, face) block** across the whole eligible
corpus and then re-runs the complete pipeline — split search, train screen, validation
test — the fraction of replicates in which M288–N45 reaches validation p ≤ 0.05 is
≤ 0.10, and consistent with the nominal 0.05. *This is the label-permutation discipline
the 2026-09-23 orchestrator cross-reference requires for a post-hoc split, applied at
the same search budget as the real run.*

**P5 — the result is not specific to the chosen split.** Across alternative assignments
of the 15 informative tablets that also satisfy the ≥10-informative-block constraint,
the median validation face-blocked p-value is ≤ 0.05.

**P6 — the coin-flip blocks, and this one is genuinely prospective.** Restrict to the
informative blocks whose marginals are exactly `total = 2, s = 1, t = 1` — a face with
two eligible lines, one carrying M288 and one carrying N45, where the null says overlap
is a fair coin. The marginal survey finds **eleven** such blocks corpus-wide. I predict
the observed overlap is **≥ 9 of 11**. *Under the null, P(≥9 of 11) = 0.0327. I have not
computed this number and it does not follow from anything in the folder: the published
full-corpus p = 1.0×10⁻⁴ is an aggregate over all 16 informative blocks and does not fix
how the eleven two-line faces individually fell.* If the count is ≤ 7 of 11 the
aggregate result is being carried by the five larger blocks and the pair's support is
thinner than any previous write-up in this folder implies.

**P7 — freedom accounting.** On the full corpus the observed overlap exceeds the forced
overlap of 38 by at least 15 of the available 21 — i.e. `freedom_used ≥ 15/21`.
*Dependent on P6 but stated separately because it is the aggregate the p-value is
computed from.*

## What would change the verdict

- P1 failing → the split-based confirmation is unavailable at this corpus size and the
  pair must wait for new tablets. Report as a negative design result.
- P4 failing → the design manufactures significance and every number from it is void.
- P6 coming in at ≤ 7 of 11 → the pair is carried by a handful of multi-line faces, and
  the honest verdict becomes "the face-blocked evidence for M288–N45 is eleven coin
  flips and they did not land", regardless of the aggregate p-value.

## Not claimed either way

No semantic, phonetic or metrological value for M288 or N45. Nothing here identifies a
commodity, a unit or a word. The question is solely whether a line-level co-occurrence
survives a null that holds the physical face fixed.
