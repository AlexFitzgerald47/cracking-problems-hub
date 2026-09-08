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
