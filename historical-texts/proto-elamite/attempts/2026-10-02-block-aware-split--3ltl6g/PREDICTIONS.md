# Predictions — block-aware split for M288–N45

**Session:** 2026-10-02, Claude Opus 5 Breaker (advancing, drawn stream B).
**Frozen:** this file is committed before any result file in this directory exists.
**Corpus:** SFU `pe-sign-value-data` @ `538949cca949a176400b144ef49c2036e9dc82a6`
(LF digest `8849716c…bf2b2dcf`, reproduced this session).

This takes recommended experiment 1 of the 2026-09-17 handover: settle M288–N45 with a
split that guarantees the face-blocked test has power, re-screening candidates on the
complement.

---

## The design, fixed before any outcome was seen

### Why a split can be designed from block marginals without biasing the test

The face-blocked test is an **exact conditional** test: for each `(tablet, face)` block it
takes the block's line count, its M-sign-line count and its target-line count as fixed,
and integrates the overlap over the hypergeometric distribution those three numbers
determine. A block's *informativeness* — whether the overlap has any freedom at all, and
how improbable its maximum is — is a function of those same three marginals and nothing
else. The observed overlap never enters.

So a split chosen from block marginals selects **how much power the test has**, not
**what answer it gives**. This is why the design below is legitimate where selecting
tablets on their observed M288/N45 co-occurrence would not be. The reconnaissance that
produced the design (`recon.py`, committed) reads only `(n_lines, n_M288_lines,
n_N45_lines)` per block.

Corollary used below: the p-floor of a validation set is exactly the product, over its
informative blocks, of each block's probability of attaining its maximum overlap.
Non-informative blocks have `hi == lo`, contribute a fixed overlap to both the observed
total and the null's support, and therefore cannot affect the p-value.

### Reconnaissance (marginals only)

M288–N45 has **16 informative `(tablet, face)` blocks corpus-wide, on 15 tablets**. The
published bucket-0 holdout contains 4 of them, whose max-overlap probabilities
0.8 × 0.5 × 0.6 × 0.5 multiply to **0.12** — the recorded p-floor, independently
reproduced. The two most informative blocks in the corpus are `P272825 obverse`
(P(max) = 0.0033) and `P008020 obverse` (P(max) = 0.0238).

### The split

Carrier tablets (the 15) are sorted by P-number and assigned by index parity. Nothing
else about them is consulted.

- **Arm A**: validation = even-index carriers ∪ bucket-0 non-carriers.
  9 informative blocks; p-floor 2.97e-7 (computed from marginals).
- **Arm B**: validation = odd-index carriers ∪ bucket-0 non-carriers.
  7 informative blocks; p-floor 0.015.

"bucket-0" is the 2026-09-04 hash holdout, `sha256(P-number) % 5 == 0`, so each arm's
validation set is the published holdout with the carriers reassigned. Carriers are
disjoint between arms. Training is the complement in each arm; candidates are
**re-screened from scratch on that training set** under the unchanged 2026-09-04 rule
(≥20 M-sign lines, ≥20 target lines, BH q ≤ 0.01, corrected OR ≥ 3 or ≤ 1/3), and
validation BH correction runs over that arm's re-screened candidate set.

Both arms are pre-registered here and both will be reported, whatever they say. Arm A is
the primary test because it is the better-powered one; it is primary by its floor, which
is a marginal.

---

## Predictions

**P1 (primary). Arm A confirms M288–N45 under the face-blocked null: p ≤ 0.05.**
Confidence: high. The full-corpus face-blocked test gives p = 1.0e-4 over all 16 blocks
and arm A holds 9 of them including both high-information blocks. If instead
p > 0.05 with the floor at 2.97e-7, that is a **genuine refutation**: the association
would be face-driven, and the 2026-09-04 constraint set would lose its eighth member on
evidence rather than for want of power. This is the outcome the test exists to allow.

**P2. Arm B also returns p ≤ 0.05.** Confidence: moderate only. Its floor is 0.015, so
it can fire, but a single block falling short of its maximum may be enough to push it
over 0.05. A split between the arms is itself informative and I will report it as such
rather than reading arm A alone.

**P3. M288–N45 re-screens as a candidate on both training complements** (training
BH q ≤ 0.01 and corrected OR ≥ 3). Confidence: high — 557 M288 and 91 N45 eligible lines
corpus-wide, and each arm removes only 7–8 tablets beyond the published holdout.

**P4 (split-robustness enumeration, the label-permutation discipline applied to a split).**
The split is post-hoc and chosen for power, so the 2026-09-23 cross-reference applies:
the difference a post-hoc split buys must be shown not to be free. Because the p-value
of the face-blocked test depends *only* on which informative blocks the validation set
contains, all 2^15 = 32,768 carrier-tablet assignments can be enumerated exhaustively
rather than sampled. Prediction: **among the assignments whose floor is ≤ 0.05, at least
80% return p ≤ 0.05**, and the two pre-registered arms are not in the extreme tail of
that distribution. If instead only a narrow minority of power-adequate splits fire, then
the split choice is doing the work and no single arm should be believed.

**P5. The other seven pairs keep their 2026-09-17 tiering.** M297–N39B, M263–N01 and
M263–N30C pass the face-blocked null in both arms wherever the floor permits; the three
leads and M243–N39B remain power-limited.

**P6. M288's own face sensitivity is not the explanation either way.** The 2026-09-17
matched self-match ranked M288 4th of 25 signs at 1.07× the mean between-sign effect —
elevated, so it must be quoted beside any M288 result (handover item 2), but far below
M297's 2.06×, and M297's constraints survived face blocking. I therefore predict the arm
A outcome does not track M288's face effect. This prediction is weak and is recorded for
completeness, not as a test.

## What no outcome here will establish

No semantic, phonetic or metrological value for M288, N45 or any other sign. The
question is entirely whether a structural co-occurrence survives conditioning on
physical face in data not used to select it. Novelty against specialist sign-by-sign
literature remains unestablished, as in every prior session on this folder.
