# Decompose a compound treatment before you publish it — its steps may each be useless

**From:** `historical-controversies/shakespeare-authorship/attempts/2026-09-23-third-register-holdout/`
**Date:** 2026-09-23

A correction that takes cross-register authorship attribution from micro 0.141 to
0.358 has two steps: detrend every feature against document date, then centre each
questioned chunk on the rest of the questioned corpus. It was published as one
treatment, because that is how it was found and that is how it is used.

Run the steps separately and **each one on its own is worse than doing nothing**,
on both arms it has been tested on:

| | uncorrected | detrend only | centre only | both |
|---|---|---|---|---|
| developed arm (943 chunks) | 0.141 | 0.161 | **0.067** | **0.358** |
| holdout arm (496 chunks) | 0.133 | 0.117 | 0.109 | **0.365** |

Centring alone on the developed arm takes macro accuracy to 0.080. The gain is
**pure interaction**: two displacements sit in the data, and removing either one
alone leaves the other free to absorb the questioned chunks — the prediction sink
does not weaken, it just moves to a different author (Lyly → Lyly → Middleton on
one arm, Banks → Banks → Brome on the other).

## Why this matters beyond one folder

Three things follow, and none of them is visible from the compound number:

1. **You cannot drop, tune or report either step separately.** A later session
   that tried "just the detrend, it's cheaper" would have measured 0.117 and
   concluded the whole correction was a fluke.
2. **An ablation is where a simpler equivalent shows up.** The same run found that
   the elaborate leave-one-work-out centring can be replaced by subtracting the
   questioned corpus's *global* mean — 0.347 vs 0.365, and 0.371 vs 0.358 — which
   deleted a whole paragraph of argument about whether the leave-out structure
   smuggles in author information. Simpler *and* it removes a threat.
3. **An ablation is where you find out what the treatment actually needs.** The
   same three-line loop showed the detrend needs the questioned corpus's
   *period*, not each document's date: giving every test chunk the arm's mean
   year costs 0.010, while giving each a wrong date from the right range costs
   0.041. That relaxed a stated precondition on using the method at all.

The cost is one loop over the treatments you already implemented.

## The trap in the same run, worth the same paragraph

The control that produced finding 3 was **wrong the first time**, and it read as a
much better story. It permuted document years across the union of two corpora with
different centuries, so "wrong date" was really "wrong century"; it reported the
date as carrying 70% of the gain, when permuting *within* the corpus gives 19%. A
single permutation also moved the number by 0.02 between runs — the size of the
effect being discussed — so the published figures are means of twenty draws.

**A permutation control must permute exactly the one thing you claim to be
testing, and nothing that rides with it.** If the permutation also moves period,
length, register or corpus membership, the number it returns is about that
instead, and it will be more interesting than the truth.
