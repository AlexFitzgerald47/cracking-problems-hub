# Frozen predictions — block-aware split for the face-blocked null

**Session:** 2026-10-02, Breaker (Claude Opus 5, Claude Code cloud), advancing.
**Committed before any result file in this directory exists.** Git history is the receipt.
**Corpus:** SFU `pe-sign-value-data` @ `538949cca949a176400b144ef49c2036e9dc82a6`, LF digest
`8849716c…bf2b2dcf` (reproduced this session; see PROGRESS).

Task drawn: `historical-texts/proto-elamite`, stream B. The folder's named next move is
HANDOVER item 1 — *settle M288–N45 with a block-aware split*.

---

## 0. What the diagnostics have already shown me (declared, NOT claimed as prospective)

Before freezing I ran one marginal-only diagnostic and I am declaring its content so that
nothing below is credited as a blind prediction when it is not.

I have seen, for M288–N45 on the **full** eligible corpus (4,869 lines, 1,426 tablet-faces):

- 16 of 1,426 `(tablet, face)` blocks are **informative** (the within-block permutation has
  freedom, i.e. `lo < hi`); they carry **21 units of freedom** in total.
- 50 blocks carry ≥1 line with both signs (56 such lines), but **36 of those 50 are forced**
  (`lo == hi`) and **27 of the 36 are single-line faces**. So the face-blocked null discards
  38 of the 56 co-occurrence lines as information-free *by construction*.
- Informative blocks per hash bucket: b0 = 4, b1 = 1, b2 = **0**, b3 = 7, b4 = 4. This is why
  2026-09-17 found the pair "powered in 3 of 5 buckets".
- Observed overlap across the 16 informative blocks is **18 of a maximum 21**.
- The p-floor is multiplicative over informative blocks; all 16 together give a floor of
  **4.5e-9**, and even three informative tablets give 7.9e-6.

**Consequence I must not launder.** Given 18/21 observed and a floor of 4.5e-9, the
direction and rough magnitude of the M288–N45 outcome under a maximal-power split are
**foreseeable from the diagnostic above**. Prediction P1 below is therefore labelled
**exploratory/foreseen**, not a prospective holdout. The predictions that carry real risk
in this session are P2–P6, and none of them has been computed.

## 1. The procedure being frozen

For a pair `(M, N)`:

1. **Split rule (marginal-only, no search, no tuning).** A tablet is assigned to
   **validation** iff it contributes at least one *informative* `(tablet, face)` block for
   that pair; otherwise **training**. Informativeness is a function of block marginals
   (`n_lines`, `m_lines`, `n_sign_lines`) only — never of the observed overlap. The split is
   pair-specific and fully determined; no tablet is in both sides.
2. **Re-screen on the complement.** The pair must clear the published 2026-09-04 screening
   gate using **training lines only**: two-sided Fisher p, BH `q <= 0.01` across all
   screened `(M-family, N-sign)` candidates, and corrected `OR >= 3` or `<= 1/3`.
3. **Confirm on validation** with the 2026-09-17 face-blocked exact randomization
   (`block_key = (tablet, face)`), BH `q <= 0.05` across the eight pairs, same direction,
   corrected `OR >= 1.5` or `<= 2/3`.
4. **Report the p-floor** for every pair, as 2026-09-17 established.

**Validity claim being staked:** conditioning on block marginals is ancillary, so selecting
blocks on informativeness cannot bias a test whose null distribution is already conditional
on those marginals. P2 is the empirical test of that claim, and it is the one that can sink
this session.

## 2. Predictions

**P1 (exploratory/foreseen — not a prospective holdout).** Under the split rule, M288–N45
clears the validation gate with p well below 0.05 and a floor below 1e-6. *Failure
condition:* it does not clear, or the re-screen on the complement fails.

**P2 (prospective, decisive).** The procedure has **nominal size**. Under a target
permutation that destroys the M288–N45 association while *preserving N45's
obverse/reverse skew* (permute the N45 indicator within face strata), the full end-to-end
procedure — re-screen plus face-blocked validation at p <= 0.05 — fires on **at most 7%** of
≥1,000 replicates. *Failure condition:* a rate above 7% means the informativeness-based
split inflates size and this session's headline is withdrawn, M288–N45 included.

**P3 (prospective).** Under that same permutation null, the pair's observed statistic is
extreme: **fewer than 1% of replicates** reach a face-blocked p as small as the real one.

**P4 (prospective).** The three 2026-09-17 load-bearing pairs — M297–N39B, M263–N01,
M263–N30C — all clear the gate under the maximal-power split too. *Failure condition:* any
of the three fails with a floor below 0.05, which would demote a load-bearing constraint.

**P5 (prospective).** M243–N39B, the pair 2026-09-17 called "barely testable", has **fewer
than 10 informative blocks corpus-wide** and will still carry a floor above 0.01 — i.e. the
split rule cannot rescue it, because the corpus has no freedom to give it. *Failure
condition:* its floor comes out below 0.001, meaning the earlier "barely testable" verdict
understated the available power.

**P6 (prospective, competitor count).** Running the identical procedure over **every**
eligible `(M-family, N-sign)` pair, M288–N45 ranks in the **top 15** by validation p-value,
and the number of pairs passing the full gate is **under 40**. *Failure condition:* a long
tail of passing competitors would mean the procedure is permissive rather than that this
pair is special.

## 3. What this session will not claim

No phonetic, lexical or metrological value for M288, N45 or any other sign. The output is a
structural constraint and a statement about how much power the corpus can supply for one.
Novelty against specialist sign-by-sign literature remains unestablished.
