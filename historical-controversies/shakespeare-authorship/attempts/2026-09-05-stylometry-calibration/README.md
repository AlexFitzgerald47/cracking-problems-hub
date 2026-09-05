# Attempt: what can stylometry actually resolve in early modern drama?

**Date:** 2026-09-05 · **Status:** complete; calibration result · **Reproducible:** yes

This does not adjudicate the authorship question. It calibrates the instrument the
question is usually settled with.

Stylometric verdicts are quoted in this debate without a stated error rate. Before any
verdict carries weight, someone has to measure what Burrows's Delta can resolve on this
material: how many plays per candidate it needs, how much questioned text it needs, and
whether it is measuring authorship or something else.

## Headline

On 312 single-author plays by 27 dramatists (1583–1700, 6.4M words), Delta attributes
**82.4%** correctly, against 3.7% uniform chance and a label-permutation null of 3.8%
(max 6.4% over 25 permutations). The instrument works.

But roughly half of that is chronology, not authorship:

| training plays withheld from within ±N years of the questioned play | accuracy | same plays, no gap | drop |
|---|---|---|---|
| ±0 (n=312) | 0.817 | 0.824 | −0.006 |
| **±5 (n=295)** | **0.654** | 0.834 | **−0.180** |
| **±10 (n=255)** | **0.475** | 0.831 | **−0.357** |
| ±20 (n=115) | 0.496 | 0.809 | −0.313 |
| ±30 (n=45) | 0.644 | 0.800 | −0.156 |

The third column is the control that makes this readable. Widening the gap shrinks the
testable set, so the drop could have been composition rather than period. It is not: the
*same* plays score 80–83% when the gap is removed. Withholding an author's own work from
within a decade of the questioned play cuts accuracy from 83% to 48%.

The ±30 row (n=45) is noisy and should not be read as recovery.

## What it needs to work

| training plays per author | accuracy | | questioned-text words | accuracy |
|---|---|---|---|---|
| 1 | 0.523 ± 0.031 | | 500 | 0.228 |
| 2 | 0.663 ± 0.053 | | 1,000 | 0.465 |
| 3 | 0.747 ± 0.024 | | 2,000 | 0.676 |
| 4 | 0.764 ± 0.036 | | 5,000 | 0.769 |
| 5 | 0.794 ± 0.022 | | 10,000 | 0.801 |
| 8 | 0.837 ± 0.019 | | 20,000 | 0.827 |

Three to five plays per candidate, and about 5,000 words of the questioned text, before
the method is worth consulting.

## What this means for the authorship question

It cuts against confident stylometric claims in **both** directions.

A candidate can only be tested at anything like 82% accuracy if they left several plays,
in the same genre, written within about a decade of the questioned work. Oxford died in
1604 with no surviving drama under his name; Bacon wrote essays, not plays. Against such
candidates the method is operating in the regime where it scores near 48%, or cannot be
run at all — so "stylometry rules them out" is a much weaker statement than the headline
number suggests.

That is not an argument for those candidates. A weak test is not evidence *for* anything,
and nothing here disturbs the documentary case. The conclusion is narrower and duller:
**stylometry is not the instrument that settles this question**, and papers on either side
that quote an attribution accuracy without a period control are quoting the wrong number.

## Corpus

`dracor-org/engdracor` (English Drama Corpus, TEI derived from EarlyPrint/TCP), 753 plays,
filtered to 312 single-author plays by the 27 authors with at least six. Anonymous plays
and Seneca translations excluded.

**It contains no Shakespeare.** His quartos appear in the metadata but have no TEI file.
That is left alone rather than patched from another repository: splicing in a modernised
Shakespeare text would confound authorship with edition and spelling convention, which is
precisely the class of artefact this attempt exists to measure. The calibration does not
need him — it measures the method, not the man.

```
src/corpus.py     builds and caches the play corpus from the TEI
src/delta.py      Burrows's Delta; z-scored on training statistics only
src/calibrate.py  the four experiments, and the matched-subset period control
results/          raw JSON
```

## Reproduction

```
pip install numpy
git clone --depth 1 https://github.com/dracor-org/engdracor /home/user/dracor-org/engdracor
cd src
python calibrate.py             # ~20s
python calibrate.py --control   # ~2 min
```

## Method notes

Features are the relative frequencies of the 500 commonest words. Z-scoring uses
**training-set statistics only** — scaling on the whole corpus leaks the questioned text
into its own normalisation and inflates accuracy. Attribution is nearest author centroid
by Manhattan distance. Every accuracy is leave-one-play-out.
