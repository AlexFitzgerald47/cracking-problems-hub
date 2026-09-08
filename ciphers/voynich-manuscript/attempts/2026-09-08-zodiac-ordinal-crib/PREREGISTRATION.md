# Preregistration — Voynich zodiac labels as a positional / cyclic code

**Date:** 2026-09-08 (written before any statistic was computed)
**Session:** Claude (Opus 5), remote
**Attempt folder:** `attempts/2026-09-08-zodiac-ordinal-crib/`

## The question

The Voynich zodiac diagrams (f70v1–f73v) carry ~298 short labels attached to nymphs,
arranged in rings around a central zodiac medallion, ~30 per sign (15 per half-diagram
for the four split signs). Every serious reading of this section assumes the labels are
an **ordered list of ~30 items per sign** — degrees, days, or degree-natives. The
published external-crib programme (Averyanov 2026; and this Hub's own
`2026-09-07-alfonsine-myriogenesis` attempt) assumes those items are **names**, and is
blocked on obtaining an external ordered source list.

That programme has an untested prerequisite. **If the labels carry positional
information at all, that information is detectable from the manuscript alone**, without
any external crib, because position is the one semantic variable we already know.

## Hypotheses

- **H0 (null).** Zodiac labels carry no information about their ring position. Their
  internal similarity is the generic similarity of the Voynichese label register.
- **H1 (ordinal).** Labels encode ordinal position within the sign (1..30). Prediction:
  label at position *k* in one sign resembles the label at position *k* in another sign,
  under a single global rotation offset, more than chance.
- **H2 (cyclic attribute).** Labels encode a repeating astrological attribute of the
  degree — decan (period 10), planetary ruler / chronocrator (period 7), triplicity, or
  similar. Prediction: within-diagram label similarity is elevated at a specific lag *p*,
  and the same *p* replicates across diagrams.
- **H3 (register only).** Labels are structured (heavy `ot-`/`ok-` onsets) but that
  structure is a property of the label register anywhere in the manuscript, not of
  zodiac position.

## Frozen test battery

All similarity is computed on cleaned lowercase EVA strings. Primary similarity:
`1 - Levenshtein(a,b)/max(|a|,|b|)`. Secondary (robustness): normalised longest common
subsequence, and a purely categorical onset-class match.

**T1 — within-diagram lag autocorrelation.** For each ring (a ring, not a diagram, is
the observational unit: rings are the physical traversal order), compute mean similarity
at lag *d* = 1..7. Null: 10,000 permutations of labels *within that ring*. Combine rings
by Fisher / Stouffer over ring-level z-scores. Report every lag; do not select one after
the fact.

**T2 — cross-diagram positional alignment.** For each pair of diagrams of equal label
count, and each cyclic offset *o*, compute mean similarity between position *k* and
position *k+o*. H1 requires a *single* offset that wins consistently across pairs, not a
per-pair best offset. Null: permutation of one member of the pair. The per-pair maximum
over offsets must be scored against a null taking the same maximum.

**T3 — periodicity.** Over each ring, compute the mean similarity at every lag up to
half the ring length, and test for a peak at a period that replicates across rings.
Candidate periods with prior astrological meaning are 3, 5, 7, 9, 10, 12; all lags are
reported so that a post-hoc pick is visible as one.

**T4 — register control.** Repeat T1 on non-zodiac label sets (herbal `L` labels,
pharmaceutical labels, Quire-20 star-paragraph first words) where the ordering is
physical but carries no known ordinal semantics. Any zodiac effect must exceed the
control effect; otherwise it is H3.

**T5 — ring / draw-order confound.** Physically adjacent labels were written adjacently.
Any lag-1 elevation is therefore uninformative about semantics. Only structure at lag
>= 2, or cross-diagram structure, counts as evidence for H1/H2.

## Falsifiers, stated in advance

- H1 dies if no single global offset beats the permutation null across held-out diagram
  pairs, or if the winning offset differs per pair.
- H2 dies if the best lag does not replicate across rings, or if the same lag effect
  appears in the T4 control sets.
- A positive result on any test must survive re-running with a second transcription
  before it is reported as anything but provisional.

## Multiplicity budget, declared now

Similarity measures: 3. Lags examined in T1/T3: 1..15. Offsets in T2: up to 30.
Control sets in T4: 3. The battery is therefore ~4,000 elementary comparisons; a
nominal p of 0.01 on a single cell is worth nothing. The reportable outcomes are
(a) an effect that replicates across independent rings at the *same* parameter, or
(b) a clean negative.
