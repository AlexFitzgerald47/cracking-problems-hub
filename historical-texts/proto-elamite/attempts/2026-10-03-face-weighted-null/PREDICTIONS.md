# Frozen predictions — 2026-10-03 session

Committed **before** any p-value, critical weight or decoy result was computed. The only
numbers seen before this file was written are those in `results/preflight.json`, which
are functions of block marginals and the face distribution alone (measured confound
strength `w_hat`, and p-value floors). `preflight.py` prints no observed overlap and no
p-value, deliberately, so that it could be read at this stage.

## What was already known, and why some predictions below are labelled informed

This is an **advancing** session on a folder with two prior passes. I had already read,
and must not pretend otherwise:

* the 2026-09-04 published holdout result for M288–N45 (tablet-blocked, p = 0.0071,
  q = 0.0480, OR 16.29);
* the 2026-09-17 face-blocked result (p = 0.47, floor 0.12, untestable) and its
  full-corpus figure (p = 1.0e-4, which includes selection data);
* **the per-block observed overlaps for M288–N45 corpus-wide**, which I enumerated while
  diagnosing the power failure, before designing the new test.

That last item means **no test of M288–N45 in this session is a blind holdout.** Where a
prediction's outcome was substantially foreseeable from what I had already seen, it is
marked *informed*; those carry little evidential weight and are recorded for honesty, not
for credit. The predictions marked *prospective* concern quantities I had not computed in
any form, and they are where this session's evidence actually sits.

## Prospective predictions

**P1 — M288–N45 is the most face-explainable pair in the constraint set.** Its critical
weight (the assumed face-confound strength `w` at which it stops clearing p < 0.05 on the
bucket-0 holdout) will be the **lowest of the eight** published pairs.
*Fails if* any other pair has a lower critical weight.

**P2 — but the confound would still have to be stronger than it measures.** M288–N45's
critical weight on the holdout will fall in the interval **(1.83, 10)** — above the
measured `w_hat = 1.83`, below 10.
*Fails if* it is below 1.83, above 10, or undefined because the pair fails at w = 1.

**P3 — the three load-bearing pairs are robust to a fourfold confound.** M297–N39B,
M263–N01 and M263–N30C will each still clear p < 0.05 on the holdout at **w = 4 × w_hat**.
*Fails if* any of the three does not.

**P4 — the weighted test is calibrated on decoys.** Applied to at least 200 (M-sign,
N-sign) pairs outside the constraint set, each at its own measured `w_hat`, the test will
reject at p < 0.05 on the holdout in **no more than 8%** of cases (nominal 5%, allowing
for discreteness and for the fact that some decoys may carry real associations).
*Fails if* the rejection rate exceeds 8%.

**P5 — the instrument fixes a real inflation, and that inflation is measurable.** On
synthetic data with **no** M-sign/N-sign association but a planted face skew of the
observed magnitude, the unweighted within-tablet test (w = 1, i.e. the published 2026-09-04
test) will reject at p < 0.05 **more than 10%** of the time, while the weighted test at the
planted weight will reject **no more than 7%** of the time.
*Fails if* w = 1 rejects at ≤ 10% (no inflation to fix, and the face confound was never a
threat to the published design) or if the weighted test rejects at > 7% (the fix does not
work).

**P6 — M243–N39B is the second most fragile.** Its critical weight will rank second-lowest
of the eight.
*Fails if* it ranks fourth or lower. (Ranks are from the same computation as P1.)

## Informed predictions (low evidential weight, recorded for honesty)

**I1** — M288–N45 clears p < 0.05 on the bucket-0 holdout under the weighted null at
`w_hat = 1.83`. Foreseeable from the published tablet-blocked p = 0.0071 plus the enumerated
per-block overlaps.

**I2** — the handover's literal item 1 (a block-aware split guaranteeing ≥ 10 informative
`(tablet, face)` blocks in validation) is **feasible but a dead end**: the split will reach
a holdout p-floor below 0.01 for M288–N45, and the complement will still select the pair
under the published screening rules, but the resulting test will rest on ~12 blocks of one
degree of freedom each and will therefore be unable to distinguish the pair from any decoy
with the same block marginals. Foreseeable because I enumerated the 16 informative blocks
and their degrees of freedom while diagnosing the power failure.

## Standing interpretive limit, carried from both prior sessions

No lexical, phonetic or metrological value is assigned to any sign in this session.
Everything here is structural association and the calibration of a test for it.
