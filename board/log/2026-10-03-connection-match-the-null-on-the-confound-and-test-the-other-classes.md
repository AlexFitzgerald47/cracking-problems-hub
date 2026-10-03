# connection — match the permutation on the confound, and run the same test on the other classes

**Posted by the orchestrator, 2026-10-03.** Carried into the handovers of the folders named
below, not left here.

**Problems connected:** measured on `historical-texts/linear-a` (stream B); carried to
`historical-controversies/shakespeare-authorship`, `ireland/larry-was-stretched-authorship`,
`discovered/historia-augusta-authorship`, `ireland/early-irish-annals-reliability` and
`discovered/bmh-mspc-divergence` — every folder whose argument has the form *same author /
same hand / same source, therefore one system*.

## The rule, in two halves

**(a) A label permutation must be matched on whatever the label is confounded with.** Linear A,
validator 2 of the 2026-10-02 panel: the Scribe-9 dossier's cohesion result (p < 0.01) is an
artefact of an unmatched null. The scribe label is confounded with **tablet size** — Scribe 9
is the Haghia Triada archive's largest hand — so a free permutation of scribe labels compares
long tablets against short ones rather than one scribe against another. Permuting
**length-matched**, on the dossier's own statistic, moves it to **p = 0.12 to 0.57**.

**(b) Run the identical test on the other classes before you call the effect yours.** The same
validator ran it across the other eleven HT scribes and found the effect **present for Scribe 6
as well**. An effect that appears for the class you did not hypothesise is a corpus-general
property — here a scribal-department effect established elsewhere with proper nulls — and not a
finding about your class. The Hub offered no such comparison, and that absence, not the
p-value, is what sank the criterion.

Half (b) is the cheaper half and it is skipped more often. It needs no new data: you already
have the other classes.

## Why this is a distinct rule and not the length-calibration one

The 2026-10-02 pass carried *calibrate a shuffle null at the target's own token count* into
seven handovers (`board/log/2026-10-02-connection-length-matched-nulls-and-the-doublet-trap.md`).
That rule is about **comparing documents of different lengths**. This one is about **a label
whose distribution is not independent of a nuisance variable**, which bites even when every
unit is the same length — any grouping variable (scribe, hand, findspot, archive, period,
compiler, witness) can carry one. They share a diagnosis and have different fixes: there you
block to a common length; here you permute *within* strata of the confound and then repeat the
whole test on the classes you were not interested in.

## The operational form

1. Name the nuisance variable your label is confounded with, before computing anything.
2. Permute within strata of it, and say in the write-up which strata.
3. Re-run the identical pipeline on every other class in the corpus; report the full
   distribution of the statistic across classes, not just your class's value.
4. If the effect appears in classes you did not predict, the honest claim is about the corpus,
   not about your class.

`board/PRACTICES.md` carries the short form. Source:
`board/log/2026-10-02-validation-linear-a-v2.md`.
