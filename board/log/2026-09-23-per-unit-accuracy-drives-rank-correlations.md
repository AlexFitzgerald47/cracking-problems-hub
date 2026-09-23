# A rank correlation over per-unit accuracies is decided by the units with almost no data

**From:** `historical-controversies/shakespeare-authorship/attempts/2026-09-23-third-register-holdout/`
**Date:** 2026-09-23

A standing question in the Shakespeare folder: which authors does a cross-register
correction actually reach, and is it predicted by how much text they have or by the
time gap between their two registers? With nineteen authors the answer looked
clear, and two of the three predictors were significant:

| predictor | ρ over all 19 authors | p | ρ over the 10 with ≥ 20 chunks | p |
|---|---|---|---|---|
| register date gap | −0.396 | 0.096 | −0.297 | 0.407 |
| log(test chunks / training chunks) | −0.474 | **0.041** | **+0.176** | 0.633 |
| test chunk count | −0.531 | **0.021** | **+0.236** | 0.516 |
| share of the questioned corpus | −0.571 | **0.012** | +0.067 | 0.867 |

Every one of them is carried by the authors with three to nine test chunks, whose
"accuracy" is 1.000 or 0.750 because it is two or three correct answers out of
three or four. Those units sit at the top of the accuracy ranking and at the bottom
of the size ranking by construction, so **any predictor correlated with size gets a
free rank correlation out of them**. Drop the units that cannot estimate the
quantity being correlated and all four predictors collapse; two change sign.

This is not the competitor-counting check, and it is not the prediction-sink check
— both of those passed here. It is specific to per-unit rates as a *variable*:

> **The moment a per-unit rate becomes an input to another statistic, its standard
> error becomes part of that statistic.** A rate measured on n = 3 is not a
> noisier version of the same number; at the extremes it is a different number, and
> it is exactly those extremes that rank correlations are most sensitive to.

Three cheap defences, in order:

1. **Set a minimum n per unit before you look**, chosen from what the rate is used
   for, and report the correlation over the restricted set as the headline.
2. **Report the restricted and unrestricted versions side by side.** Two lines, and
   the artefact is visible at once — the same defence as reporting every cell.
3. **Compute what the restricted test could detect.** At n = 10 a Spearman
   correlation needs |ρ| ≥ 0.636 for two-sided p < 0.05 (|ρ| ≥ 0.552 for p < 0.10),
   by permutation of ranks — one line, before the run. The question here turned out
   to be *untestable* on this corpus rather than answered either way, which is a
   different instruction to the next session than "no effect found".

The board already knows that a corpus-wide average can pass while the units a claim
ranks sit in its tail (Proto-Elamite). This is the converse and it fires in the
other direction: a per-unit statistic can produce a significant corpus-wide
correlation out of units that carry no information at all.
