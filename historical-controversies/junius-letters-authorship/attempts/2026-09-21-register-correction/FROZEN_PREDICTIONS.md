# Frozen predictions — 2026-09-21 register-correction session

Committed **before** `src/correction.py` was written or run. Only `src/sink_tabulation.py`
output had been seen at the time of writing. Git history is the freeze.

## What had been seen

The 2026-09-17 results reproduce byte-identically (`git diff` on `results/` empty after
re-running `prediction_test.py`). The sink tabulation returned:

| cell | micro | macro | largest excess over true share | sink stability over 50 replicates |
|---|---:|---:|---:|---|
| A cross: letters from formal centroids (8 cand) | 0.108 | 0.118 | +34.1 pp (Wilkes) | 34.1% ± 12.2%, split 3 ways |
| B cross: formal from letter centroids (11 cand) | 0.342 | 0.176 | +25.2 pp (Burke) | 70.6% ± 7.4%, one class |
| in-distribution letters (11 cand) | 0.848 | 0.850 | +2.1 pp | — |
| in-distribution formal (8 cand) | 0.909 | 0.883 | +2.7 pp | — |

Direction **B** is the one with the Junius question's shape: a questioned document in the
public/formal polemical register scored against candidate centroids that survive only in
private letters. It shows a single, stable, large sink. Direction A does not.

## Predictions

**P1.** Register-centring (leave-one-**work**-out, author-blind) raises direction-B
**macro** accuracy from 0.176 to **above 0.30**.

**P2.** Direction-B largest excess-over-true-share falls from +25.2 pp to **below +15 pp**.

**P3.** Direction **A** improves by *less* than direction B on macro accuracy, because it
has no stable single sink to remove. It may not improve at all.

**P4.** The single most relevant cell in the whole problem — Philip Francis's 10
acknowledged *political-prose* chunks scored against 11 private-letter centroids, i.e.
exactly the comparison the Junius attribution has to make — currently recovers **0 of 10**.
I predict correction recovers **at most 4 of 10**.
*Failure condition for this session's pessimism:* if it recovers **≥ 7 of 10**, the
register block is substantially removable, and the folder's "evidence-blocked" status
must change rather than be re-stated.

**P5.** The scale-free register/author cost ratio (median same-author cross-register
centroid Delta ÷ median different-author same-register centroid Delta, both from the same
baseline cell) stays **above 1.0** under every treatment. The Shakespeare precedent is that
the gap itself does not shrink; what changes is the attribution failure the gap predicts.

**P6.** Detrending against year will behave *worse* here than on the Shakespeare corpus,
because this corpus has no document-level dates. Every source carries one period midpoint,
and in the private-letter register ten of the eleven candidate authors contribute exactly
one source each — so the year covariate is very nearly a relabelling of author identity.
Prediction: on a permuted-year null the detrend arm moves the accuracy by an amount
comparable to the real-year arm, i.e. it is measuring the operation, not chronology.
