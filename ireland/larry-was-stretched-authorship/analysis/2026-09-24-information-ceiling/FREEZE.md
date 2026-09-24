# Frozen predictions — 2026-09-24 session

Written and committed **before** experiments 4 and 5 were run. Experiments 1–3
were already complete when this was written and their results are stated as
facts below, not predictions.

## What is already measured (not predictions)

- **Exp 1, pipeline validation.** Cosine Delta and Burrows's Delta both assign
  11/11 of the Gutenberg Federalist's `HAMILTON OR MADISON` papers to Madison,
  reproducing Mosteller & Wallace (1964). Leave-one-paper-out on the undisputed
  papers: 0.903 (Burrows, MFW=300, k=3). The pipeline works.
- **Exp 2, power surface on the Federalist.** At a questioned length of 470
  words (Larry's length) with 6,000 training words per candidate and k=3, top-1
  accuracy is 0.634; at 470 training words it is 0.433 against a chance rate of
  0.333.
- **Exp 3, genre-matched ceiling.** Leave-one-song-out over the 13 *Musa
  Pedestris* authors with ≥2 canting songs (36 songs, 8,334 words) gives 0.194
  (cosine, MFW=100) against chance 0.077; label-permutation null over 1,000
  draws gives 0.066 ± 0.047, p = 0.016. Real but very weak same-register signal.

## Predictions for Experiment 4 (the register gap), frozen

Five authors appear both in *Musa Pedestris* (canting songs) and in a large
non-song prose corpus: Ainsworth, Egan, Henley, Sims, Dekker. Three conditions,
identical candidate set (k = 5, chance = 0.200), identical test texts, identical
method; the *only* thing that changes is which register the candidate profile is
built from.

- **A — same register** (canting song attributed against other canting songs):
  predicted **above chance, roughly 0.30–0.50**.
- **B — cross register** (canting song attributed against the same authors'
  prose): predicted **at or statistically indistinguishable from chance
  (0.200)**, and clearly below A.
- **C — prose→prose at matched length** (470-word prose sample against prose
  profiles): predicted **high, ≥ 0.60**.

Ordering predicted: **C > A > B, with B inside the noise band of chance.**

If B comes out well above chance, the cross-register route is open and a
Larry attribution against Curran's oratory and Burrowes's sermons is worth
attempting. That is the outcome that would falsify this session's thesis.

## Prediction for Experiment 5 (Larry itself), frozen

Conditional on B landing at chance: ranking "The Night Before Larry Was
Stretched" against the candidates' attested prose is measuring the register gap,
not the author. The concrete, falsifiable consequence:

> **The identity of the top-ranked candidate for Larry will not be stable across
> reasonable hyperparameter settings.** Varying the distance metric (cosine /
> Burrows) and the MFW count (50 / 100 / 200 / 300) will produce **more than one
> distinct winner** across the eight cells.

If instead a single candidate wins all eight cells, that is a signal that
something real is present and this session's negative conclusion is wrong.

## Prediction for the text-witness check, frozen

Farmer's 1896 text and the *Universal Songster* (Jones & Co.) text differ in at
least two places already observed by eye ("A bit"/"And bit", "duds"/"dads").
Prediction: **the between-witness distance between two printings of Larry will
be small relative to the between-candidate distances**, i.e. the transmission
noise is not what decides the ranking. If it is comparable, no attribution of
this text is possible for a second, independent reason.
