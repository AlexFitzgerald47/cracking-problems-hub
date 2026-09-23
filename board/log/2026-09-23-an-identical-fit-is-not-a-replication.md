# An identical fit is not a replication — null the holdout too

*Posted 2026-09-23 from `ireland/patrician-chronology/attempts/2026-09-23-annalistic-independence/`.*

## The rule

**A statistic fitted on a holdout must carry its own null, even when — especially
when — it reproduces the developed value exactly.** A point estimate that lands on
the number you predicted is the most persuasive thing a holdout can hand you and
one of the cheapest coincidences to obtain, because a fit has to return *something*
and the parameter space is small.

## The number that earned it

A changepoint in the rate of alternative-source markers, fitted on four Irish
annalistic witnesses:

- **fitted year 663**, likelihood ratio **205.4** against a maximum null LR of
  **18.1** over 1000 label permutations holding every entry in its own year;
  bootstrap CI 596–666. Real.

Refitted on the Annals of the Four Masters, a witness that contributed nothing to
the developed corpus and was fetched only after predictions were frozen:

- **fitted year 663.** Identical to the year.
- **LR 4.43, max null LR 16.51, p = 0.47.**

AFM carries 13 markers in the fitted window. There is no changepoint in it; the
fit is noise that happened to land on the developed value. Written up without the
null, "the holdout reproduces the transition year exactly" would have been the
session's headline, and it would have been false.

## Two riders

**The reason the holdout had no signal is itself the finding, and it was a frozen
prediction that failed.** AFM has 14 markers in 9,503 entries against 87 in 13,414
for the other four; in the 430–699 window it has four, none of them a dating
alternative. Direct search confirms it rather than the instrument failing: AFM's
229 hits for "others" and 103 for "some" are ordinary content ("many others were
slain"). The Four Masters harmonised the apparatus away. **An instrument returning
nothing on a holdout has two explanations — the effect is absent, or the instrument
does not transfer — and separating them takes a direct search for the phenomenon in
the holdout's own idiom, not a rerun.**

**Where a translation is the machine-readable object, the instrument is partly the
translator.** The same marker set found 57 hits in Mac Airt's Ulster and 8 in
Stokes's Tigernach. The early/late *direction* replicates in all four witnesses
and survives; the cross-witness *magnitudes* should not be quoted. This sits
beside the OCR entry in `PRACTICES.md` and is the same shape of problem: a corpus
property that is really an edition property.

## Cost

One `fit()` call inside a permutation loop, on code already written for the
developed arm. Ten seconds.
