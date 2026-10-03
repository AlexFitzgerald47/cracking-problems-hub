# Frozen predictions — 2026-10-01 session

Written and committed **before** any new p-value was computed. The session's starting
point is the 2026-09-17 handover's recommended experiment 1: *settle M288–N45 with a
block-aware split*.

## What had already been seen when these were written (so: not prospective)

Reproduction of the 2026-09-04 pipeline (identical, Linux digest
`8849716c…8bf2b2dcf`), the 2026-09-17 `power_floor.json` table, and one new
**exploratory diagnostic**: the within-face occupancy of each M-sign and the number of
informative `(tablet, face)` blocks per published pair. That diagnostic is reported in
RESULTS.md as exploratory and is the reason the tests below take the shape they do. Its
headline numbers, stated here so they cannot be retro-fitted:

- M288–N45 has **56** co-occurring lines in the whole corpus, but only **16** informative
  `(tablet, face)` blocks, holding **18** of those co-occurrences. **38 of 56 (68 %) fall
  in blocks where the overlap is logically forced** (the face is saturated with M288, or
  with N45).
- M288 has the highest within-face occupancy of any sign carrying a published
  constraint: mean **0.701**, and it occupies **every** eligible line in **179 of 350
  (51.1 %)** of the faces where it occurs. M297 is 0.614 / 40.3 %, M106 is 0.291 / 6.5 %.

## Prospective predictions

**P1 — split feasibility.** A deterministic block-aware split that places *every* tablet
owning an informative `(tablet, face)` block for M288–N45 into validation still leaves a
training set on which M288–N45 passes the unchanged 2026-09-04 screen (Benjamini–Hochberg
q ≤ 0.01 and Haldane-corrected pooled OR ≥ 3). **Fails if** the re-screen on the new
complement does not select the pair.

**P2 — power.** Under that split the face-blocked p-value floor for M288–N45 is ≤ 0.01,
i.e. the test can return a significant answer. **Fails if** the floor exceeds 0.05, which
is the 2026-09-17 condition for "untestable".

**P3 — verdict.** The face-blocked exact test on that validation set returns **p ≤ 0.05**:
M288–N45 **confirms**, contradicting the 2026-09-17 frozen prediction A2 ("M288–N45 does
not survive the face block"). **Fails if** p > 0.05.

**P4 — calibration of the pair-specific split.** The split is chosen using the pair's own
block marginals. Within-block permutation preserves block marginals exactly, so the
selected block set should be invariant under the null and the procedure should stay exact.
Prediction: simulating the *whole* procedure under the within-`(tablet, face)` null gives
a uniform p-value distribution — the fraction of replicates at p ≤ 0.05 falls in
**[0.03, 0.07]** over ≥ 2,000 replicates. **Fails if** it falls outside that band, which
would mean designing the split around the pair inflates the test.

**P5 — level of analysis.** M288 is a *face-level* marker, not a line-level one. At the
level of tablet-faces, faces bearing M288 are enriched for N45 relative to faces not
bearing M288, tested **within tablet** (the obverse/reverse discordant-pair exact test),
and that test has a p-floor ≤ 0.05 so it can fire. **Fails if** the face-level test has no
power (floor > 0.05) or the direction reverses.

## Exploratory, explicitly not frozen

**E6.** Across the eight published pairs, the fraction of co-occurrences lost to saturated
blocks should track how much the pair's p-value degrades when the block key moves from
tablet to `(tablet, face)`. Both columns were visible before this file was written, so
this is reported as a description, not a test.

## Null model

Every new number is reported beside a null: P1–P3 beside the P4 calibration simulation;
P5 beside a within-tablet face-label permutation (the handover's standing instruction that
*any* post-hoc face or block split must carry the label permutation before its difference
is interpreted). No lexical, phonetic or metrological value is assigned to any sign.
