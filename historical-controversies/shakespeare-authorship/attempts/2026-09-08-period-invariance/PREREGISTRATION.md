# Preregistration — written before the experiment was run

**Session:** 2026-09-08, Claude Opus 5. **Committed before results existed.**

## The observation that prompted it

Ranking all 500 Delta features by R² of the feature regressed on composition year,
the most date-loaded features in the 2026-09-05 corpus are, almost without exception,
**orthographic variants of each other with equal and opposite slopes**:

| modern form | slope | archaic form | slope |
|---|---|---|---|
| hear | +0.80 | heare | −0.67 |
| down | +0.76 | downe | −0.68 |
| self | +0.73 | selfe | −0.69 |
| have | (—) | haue | −0.70 |
| speak | +0.69 | speake | −0.64 |
| think | +0.69 | thinke | −0.64 |
| fear | +0.67 | feare | −0.68 |
| give | +0.65 | giue | −0.67 |
| look | +0.64 | looke | −0.66 |
| us | (—) | vs | −0.67 |
| up | (—) | vp | −0.63 |

These are the final-silent-`e` and the `u`/`v` positional conventions: **printing-house
and transcription conventions, not authorial choices and not language change.**
(`hath`/`has`, F = 16.8 / 13.2, are genuine morphosyntactic change and are a different
thing; the test below deliberately leaves them intact.)

## Hypothesis

**H.** The period confound measured on 2026-09-05 — accuracy 0.83 → 0.475 when an
author's own plays within ±10 years are withheld — is substantially an artefact of
unregularised original-spelling text. Spelling variants act as a *date stamp*: a
near-free shortcut to the right author when training and test are contemporaneous, and
an active source of error when they are not.

## Pre-specified test

Apply a fixed, author-blind, outcome-blind orthographic key (lowercase; `u`→`v`;
`j`→`i`; `y`→`i`; strip apostrophes; strip trailing `e`; collapse repeated letters),
rebuild the top-500 feature set on the keys, and rerun the **identical** experiment —
same corpus, same Delta, same leave-one-play-out, same matched-subset control.

## Predictions (falsifiers)

- **P1.** ±10-year-gap accuracy rises materially above **0.475**. If it stays within
  noise of 0.475, H is dead.
- **P2.** No-gap baseline accuracy **falls or stays flat** relative to 0.824. If
  normalisation raises both, H is wrong about the mechanism (it would then just be a
  better feature set, not the removal of a date stamp).
- **P3.** The matched drop at ±10 shrinks materially from **−0.357**.
- **P4.** Mean R²(feature ~ year) falls from **0.103**.

## Pre-specified control that separates the two available explanations

Normalisation both (a) removes date-loaded features and (b) *merges* the two halves of
each variant pair, preserving the lexeme's information. A control that only does (a) —
deleting the *n* most date-loaded raw features, for *n* matched to the number of raw
features the merge consumes — distinguishes them.

- If **delete-only ≈ merge**, the finding is the weaker "date-loaded features hurt".
- If **merge > delete-only**, the finding is the strong one: the information was never
  lost, only mis-attributed, and spelling normalisation is a *free* recovery.

## What would make this a genuine result rather than a better score

The corpus is EarlyPrint/TCP original spelling. So is most early modern attribution work.
If H holds, every attribution in this field that compares texts printed decades apart on
unregularised spelling has been quoting an accuracy from the wrong regime.

---

# Second preregistration — written after conditions.json, before the ablation control

## What the first experiment showed (summary, full numbers in RESULTS.md)

Orthographic normalisation moves ±10-gap accuracy 0.482 → 0.594 and halves mean
R²(feature ~ year), 0.103 → 0.044. **P1 and P4 hold. P2 fails**: no-gap accuracy rises
too (0.820 → 0.852), so normalisation is partly just a better feature set, not purely
the removal of a date stamp. Linear detrending — the 2026-09-05 handover's own proposal 3
— **does not work at all** (±10: 0.470 vs raw 0.482, and it collapses at wide gaps).

A large residual gap remains: 0.594 with the gap against 0.880 without it.

## The variable neither session controlled

Under the ±T gap the training set does not shrink uniformly. Measured:

| gap | mean training plays | mean plays **by the true author** | authors available |
|---|---|---|---|
| ±0 | 305.8 | 12.57 | 27.0 |
| ±5 | 270.3 | 7.78 | 26.7 |
| ±10 | 241.0 | **4.65** | 25.9 |
| ±20 | 199.5 | 3.39 | 22.3 |
| ±30 | 151.7 | 3.08 | 18.5 |

Dramatists write in bursts, so a ±10-year window centred on one of an author's plays
removes most of the rest of that author's output — **63% of the true author's training
data, against 21% of everyone else's.** The 2026-09-05 matched control held the *test
set* constant but compared a 4.65-play-per-true-author condition against a
12.57-play-per-true-author condition. That session's own training-size curve
(1 play 0.523, 3 plays 0.747, 5 plays 0.794) says this alone must cost accuracy.

## Hypothesis 2

**H2.** The measured "period confound" is substantially an **author-specific data-loss
artefact** of the gap protocol, not a chronological effect.

## Pre-specified decisive test

**Size-matched random ablation.** For each test play and each gap T, count how many
plays the gap removes *from each author separately*. Then remove that exact number from
each author **at random in time** instead of by proximity, and attribute. Repeat with
several seeds. Everything else identical.

## Predictions (falsifiers)

- **P5.** If random ablation reproduces most of the drop (±10 accuracy near 0.48–0.59),
  the period effect is largely an artefact and the 2026-09-05 headline is wrong.
- **P6.** If random ablation stays near 0.83, chronology is real and the artefact
  explanation is dead.
- **P7.** The honest measure of the period effect is the difference between the
  time-based gap and its size-matched random ablation, **not** the difference from the
  full-data baseline. Whatever P5/P6 return, that difference is the number this problem
  should have been quoting.

Written before the ablation was run.
