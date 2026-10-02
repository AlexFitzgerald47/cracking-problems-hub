# M288–N45 settled, and the constraint set re-counted on its own multiplicity basis

**Session:** 2026-10-02, Claude Opus 5 Breaker (advancing; drawn, stream B).
**Corpus:** SFU `pe-sign-value-data` @ [`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6),
LF digest `8849716c…bf2b2dcf` — reproduced, matching the 2026-09-17 correction.
**Predictions frozen before any result existed:** [`PREDICTIONS.md`](PREDICTIONS.md), commit
`5307c3b`, one commit before this file.
**Code:** `recon.py`, `block_aware_split.py`, `exact_form_audit.py`; 9 unit tests in
`test_block_aware_split.py`, two of which pin this file's blocked exact test against the
already-audited 2026-09-04 and 2026-09-17 implementations.

---

## Result in one sentence

M288–N45 is **confirmed** under the face-blocked null on a block-aware holdout that gives
the test a p-floor of 3.0e-7 instead of 0.12 (arm A: p = 0.0039, BH q = 0.048 over the
arm's own 50 re-screened candidates, OR 19.3) — but the same session finds that the
2026-09-17 "seven of eight survive face blocking" headline rests on a BH correction over
the 8 already-surviving pairs rather than the 54 the holdout was used to winnow, and on
the design's own multiplicity basis **two** of the eight survive, not seven.

---

## 0. Reproduction, before anything new

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pin. All 15 result
rows reproduce: every contingency cell, odds ratio and q-value identical to the committed
`analysis/results/associations.csv`, p-values differing only in the ~16th decimal place.
Corpus audit matches exactly (1,467 files, 10 without numbered lines, 1,457 tablets,
11,013 lines, 4,869 eligible, 3,819 train / 1,050 validation). The six original unit
tests pass.

Two further reproductions, each load-bearing for what follows:

1. **The selection stage.** This session re-implements the screen so it can be re-run on a
   different training set. On the *published* training set it returns **1,056 pairs tested,
   54 selected, set-identical** to `structure_associations.analyze`'s selection. The
   re-implementation is therefore the same screen, not a similar one.
2. **The face-blocked test.** `test_block_aware_split.py` requires this file's blocked
   exact test to return the 2026-09-04 tablet-blocked p-values *and* the 2026-09-17
   face-blocked p-values and floors to 1e-9 relative. It does, for all eight pairs. The
   published M288–N45 floor of **0.12** is reproduced to ten decimal places, and is exactly
   the product 0.8 × 0.5 × 0.6 × 0.5 of its four informative blocks' max-overlap
   probabilities.
3. **The M297 exact-form audit** reproduces at 0.0757 / 0.6941 / 0.1377.

---

## 1. The block-aware split

### Why a split may be designed from marginals

The face-blocked test is exact and conditional: each `(tablet, face)` block's line count,
M-sign-line count and target-line count are held fixed and the overlap is integrated over
the hypergeometric distribution they determine. Whether a block is *informative* (the
overlap has freedom: `min(s,t) > max(0, s-(n-t))`) and how improbable its maximum is are
functions of those same three marginals. **The observed overlap never enters.** So a split
rule reading only marginals chooses how much power the test has, not what answer it gives.

Two consequences used throughout:

- **The p-floor of an enriched face-blocked test is exactly the product, over the
  validation set's informative blocks, of each block's probability of attaining its
  maximum overlap.** Proved in code (`test_floor_is_product_of_block_max_probabilities`)
  and verified against the published 0.12.
- **Non-informative blocks cannot change the p-value.** They have `hi == lo`, so they add
  the same constant to the observed total and to the null's support
  (`test_non_informative_block_cannot_change_the_p_value`). This is what makes the
  enumeration in §3 exhaustive rather than sampled.

### Reconnaissance (marginals only — `recon.py`)

M288–N45 has **16 informative `(tablet, face)` blocks corpus-wide, on 15 tablets**, out of
1,426 blocks. The published bucket-0 holdout holds 4 of them. The two most informative
blocks in the corpus are `P272825 obverse` (P(max) = 0.0033, 25 lines) and `P008020
obverse` (P(max) = 0.0238, 10 lines); the remaining fourteen are mostly 2-line blocks with
P(max) = 0.5.

That distribution is the whole problem in one line: **56 of the corpus's M288/N45
co-occurrences sit in blocks where the overlap is forced by the marginals and contributes
nothing to any test.** The association is abundant and nearly untestable at the same time.

### The split, pre-registered

The 15 carrier tablets, sorted by P-number, assigned by index parity; validation also
takes the bucket-0 non-carriers, so each arm is the published holdout with the carriers
reassigned. Carriers are disjoint between arms. Candidates are **re-screened from scratch**
on each complement under the unchanged 2026-09-04 rule, and validation BH runs over that
arm's own candidate set.

| | published bucket-0 | arm A | arm B |
|---|---:|---:|---:|
| validation tablets | 297 | 233 | 232 |
| validation eligible lines | 1,050 | 1,105 | 1,063 |
| informative blocks for M288–N45 | 4 | **9** | **7** |
| p-floor | **0.12** | **3.0e-7** | **0.015** |
| re-screened candidates | 54 | 50 | 53 |
| M288–N45 training OR / q | — | 11.11 / 1.1e-14 | 11.13 / 5.4e-17 |
| observed / max overlap | 15/16 | 24/27 | **19/19** |
| face-blocked p | 0.47 | **0.00385** | 0.0150 |
| BH q over the arm's candidates | 1.00 | **0.0482** | 0.1325 |
| validation OR | 16.29 | 19.29 | 22.74 |
| confirmed | no (no power) | **YES** | no |

### P1 confirmed: M288–N45 survives face blocking on a powered holdout

Arm A gives p = 3.85e-3 against a floor of 3.0e-7 — a test that could have returned any
answer, and returned a significant one. After BH over the arm's own 50 re-screened
candidates, q = 0.0482, and the pair clears every element of the 2026-09-04 confirmation
rule (same direction, q ≤ 0.05, OR ≥ 1.5). **M288–N45 is no longer "untestable at holdout
scale"; it is confirmed against the face confound on data not used to select it.**

The honest qualifier: q = 0.0482 is as close to the 0.05 boundary as 2026-09-04's original
q = 0.0480 was. The difference is what the number now means. In 2026-09-04 the boundary
q came from a test that was not controlling for face at all; in 2026-09-17 the pair's
failure came from a test that could not fire. Arm A is the first time the pair has faced a
test that could go either way, and the pair passed it.

### P2 half-confirmed, and arm B is the cleanest demonstration of the floor rule on this board

Arm B's observed overlap is **19 of a maximum possible 19**. Every one of its seven
informative blocks showed the greatest overlap its marginals permit — the most extreme
result the data could physically produce — and the p-value is therefore *exactly* its floor,
0.015. P2 predicted p ≤ 0.05 and that holds. But BH over arm B's 53 candidates gives
q = 0.1325, so the pair is **not** confirmed on arm B.

This is worth stating plainly because it is counter-intuitive: **arm B's data are perfect
and arm B still cannot confirm the pair.** A p-floor below 0.05 means the test can fire
before multiplicity; it does not mean the test can fire after it. The 2026-09-17 floor rule
should be extended accordingly — quote the floor against the *corrected* threshold the
design will actually apply, not against 0.05.

### P3 confirmed

M288–N45 re-screens as a candidate on both complements, at training OR 11.1 and
q ≈ 1e-14 / 1e-17. The pair is not a creature of the published split's training set.

---

## 2. The audit: the 2026-09-17 face-blocked q-column is not on the design's multiplicity basis

This was not something the session set out to find. It fell out of running the design's own
screen on a new split and noticing that the published split, run through the identical
machinery, does not reproduce "seven of eight".

**The p-values are not in dispute.** Every raw face-blocked p-value from 2026-09-17
reproduces exactly (0.0014514, 0.028073, 0.0083903, 0.019004, 0.00028646, 0.0030637,
0.011685, 0.47). The disagreement is entirely about what family they are corrected over.

- 2026-09-04's validation applies BH across **all 54 screened candidates** — that is what
  `discover_and_validate` does, one validation p-value per selected item.
- 2026-09-17's face-blocked column applies BH across **the 8 pairs that had already
  survived that validation.**

Those 8 were selected *using the same holdout data* the face-blocked test then re-uses. So
correcting over 8 corrects over the survivors of a search conducted on the test set, which
understates the search. On the design's own basis — the same 54 candidates, same holdout,
same face-blocked test, BH over 54:

| pair | face-blocked p | q over 8 (as published 2026-09-17) | **q over 54** | floor | informative blocks |
|---|---:|---:|---:|---:|---:|
| M263–N01 | 0.00029 | 0.0023 | **0.0155** ✓ | 7.7e-7 | 12 |
| M297–N39B | 0.00145 | 0.0058 | **0.0392** ✓ | 1.2e-9 | 16 |
| M243–N39B | 0.00306 | 0.0082 | 0.0552 | 4.8e-5 | 4 |
| M297–N01 | 0.00839 | 0.0168 | 0.1133 | 8.2e-10 | 16 |
| M106–N24 | 0.01169 | 0.0187 | 0.1262 | 3.5e-4 | 2 |
| M263–N30C | 0.01900 | 0.0253 | 0.1516 | **0.019** | 5 |
| M297–N24 | 0.02807 | 0.0321 | 0.1516 | 1.5e-4 | 7 |
| M288–N45 | 0.47 | 0.47 | 1.00 | **0.12** | 4 |

**Two of eight survive, not seven.** The 2026-09-17 session's substantive conclusions
mostly stand — its tiering came from the five-bucket rotation using raw per-bucket
p ≤ 0.05, not from this column — but the sentence "Seven of the 2026-09-04 constraint set's
eight numeral associations survive a null that blocks on physical face" should read: *seven
of eight have a face-blocked p below 0.05 uncorrected; on the design's own 54-candidate BH
basis, two do.* The correction is recorded in `PROGRESS.md` and does not touch that
session's files.

**And the same correction applies to this session.** It is why arm A's headline is quoted
at q = 0.0482 over 50 candidates rather than at p = 0.0039, and why arm B is reported as
not confirmed despite a perfect result.

### The re-counted tier list

Taking the three splits run through identical machinery (published, arm A, arm B) and the
2026-09-17 bucket rotation together:

| tier | pairs | basis |
|---|---|---|
| **Load-bearing** | M263–N01, M297–N39B | confirmed on all three splits at BH over the arm's own candidate set; 12–18 informative blocks; floors ≤ 1.2e-9 |
| **Confirmed, single split** | M288–N45 (arm A), M243–N39B (arm A) | clear the corrected threshold on one arm, q = 0.048/0.054 on the others — boundary cases, not refuted |
| **Power-limited, undecided** | M263–N30C (floor 0.019), M106–N24 (2 informative blocks, floor 3.5e-4) | cannot reach a corrected threshold on this corpus at this split size; no verdict is available |
| **Uncorrected-only** | M297–N01, M297–N24 | raw p ≤ 0.05 face-blocked on every split, never clear BH over the real candidate family |

M263–N30C deserves emphasis: it was in 2026-09-17's load-bearing tier, and on the
corrected basis it is **not refuted but undecided** — its floor of 0.019 is below 0.05 and
above the corrected threshold it would need. Exactly the trap arm B illustrates.

---

## 3. P4: the split-robustness enumeration — exhaustive, not sampled

The 2026-09-23 cross-reference requires a post-hoc split to show that the difference it
buys is not free. Because the face-blocked p depends only on which informative blocks the
validation set holds (§1), **all 2^15 − 1 = 32,767 assignments of the carrier tablets can
be enumerated exactly**, which is strictly stronger than the label permutation the rule
asks for: it is the whole reference distribution rather than a sample of it.

| floor cap | splits | p ≤ 0.05 | fraction | median p |
|---:|---:|---:|---:|---:|
| ≤ 0.05 | 31,726 | 25,205 | **0.7945** | 0.0064 |
| ≤ 0.01 | 28,671 | 23,539 | 0.8210 | 0.0044 |
| ≤ 0.001 | 24,402 | 20,030 | 0.8208 | 0.0033 |
| ≤ 1e-4 | 17,839 | 15,561 | 0.8723 | 0.0028 |
| ≤ 1e-5 | 9,716 | 9,698 | **0.9981** | 0.0022 |

By informative-block count the fraction firing rises monotonically: 53% at 5 blocks, 71% at
7, 81% at 8, **92% at 9**, 97% at 10, and **100% at 11 or more** (every one of the 4,305
splits with ≥ 11 blocks fires).

**P4 as literally written is narrowly refuted: 79.45%, not ≥ 80%.** The shortfall is not
split-dependence of the finding — it is the floor again. "Powered at floor ≤ 0.05" admits
splits whose floor is 0.049, which can only fire on a perfect result. Restrict to splits
that are *decisively* powered (floor ≤ 1e-5, arm A's regime at 3.0e-7) and 99.81% fire.

**P4's second clause is confirmed, and it is the one that matters:** neither arm is in the
tail of its own reference distribution.

- Arm A: p = 0.00385; **2,473 of the 5,434 nine-block splits (45.5%) have a p at least as
  large.** It sits at the 43rd percentile of all 31,726 power-adequate splits.
- Arm B: p = 0.0150; 51.6% of seven-block splits have a p at least as large.

So the pre-registered parity rule picked a thoroughly ordinary split and the result is a
property of the corpus, not of the split. A Fisher combination of the two arms, whose
informative blocks are disjoint, gives p = 6.2e-4; that figure is indicative only, because
each arm's *screen* used the other arm's validation lines, and it is not the headline.

---

## 4. Exact-form audit of M263 and M288 (handover item 3), and M106

Reusing `face_and_form.exact_forms` verbatim. Note that `face_and_form.test_b` documents
itself as taking a `family` argument but hardcodes `family = "M297"`; the family loop is
reimplemented in `exact_form_audit.py` for that reason. The M297 numbers reproduce exactly.

| family | form-occurrences on eligible lines | distinct forms | forms with ≥ 15 | merge testable? |
|---|---|---:|---:|---|
| **M288** | M288 **538**, M288~I 6, M288~D 4, M288~F 3, others ≤ 2 | 9 | 1 | **no — and that is the answer** |
| **M263** | M263 93, M263~A 34, M263~B1 27, M263~1 23, M263~B 6, … | 10 | 4 | yes |
| **M243** | M243~J 18, M243 5, M243~E 4, M243~B 4, … | **15** | 1 | no — and that is a problem |
| M297 | M297 175, M297~B 62, M297~D 10, … | 5 | 2 | yes (done 2026-09-17) |
| M106 | M106 30, M106~A 24, M106~2 5 | 3 | 2 | yes |

Counts are form-occurrences, which slightly exceed line counts because a line can carry two
forms of one family: M288 has 559 occurrences on 557 eligible lines, M263 193 on 191, M243
46 on 46, M106 59 on 59.

**M288's merge cannot be an artefact, because there is effectively no merge.** 538 of 559
M288 form-occurrences (96.2%) are the plain graphical form, and no variant reaches 7. This
closes, rather than fails, the obvious objection to the result in §1: the pair confirmed in
arm A is a pair about one graphical form, and the family reduction is doing almost no work.

**M263's merge is upheld.** Four forms are testable and all six pairwise homogeneity tests
on N01 give p ≥ 0.06 (lowest: M263~A vs M263~1, p = 0.0605), while on N30C all four forms
show a rate of **exactly 0.000** against a base rate of 0.063 and every pairwise test gives
p = 1.0000. The depletion is uniform across the family. The folder's most robust constraint
is not a merge artefact. (M263~A is 34/34 lines with N01 — an extreme that a future session
may want to look at on its own terms.)

**M243 is the opposite case to M288, and the least auditable family in the constraint set.**
Its 46 occurrences are spread over **15 distinct graphical forms**; the plain form has 5,
the largest (M243~J) has 18, and only that one clears the 15-line bar — so the merge is
genuinely doing the work here and *cannot be audited at all* on this corpus. This is not an
error in the published analysis, which documents the family reduction, but it means
"M243–N39B" is a statement about a 15-way merge whose homogeneity is untestable, and that
is a second, independent reason — beside its 4 informative blocks — why the constraint sits
at the corrected boundary on every split. Any future use of it should say so.

**M106 is the one merge that looks unsafe, and it does not survive correction.** M106 and
M106~A differ on N24 at p = 0.0284 (rates 0.133 on 30 lines vs 0.417 on 24, OR 0.23, a
3.1-fold rate gap):
the association is carried disproportionately by M106~A. **But BH over the 16 within-family
homogeneity tests run here puts every one of them at q ≥ 0.40**, so this is a flag, not a
finding. It is recorded because M106–N24 is already an undecided, 2-informative-block lead,
and the cheap thing for any future session to do is split it by form before using it.

**P6** is as predicted but carries no weight: M288's 2026-09-17 face effect was 1.07× the
mean between-sign effect (4th of 25 signs), elevated but far below M297's 2.06×, and the
arm A result does not track it. Quoted here because handover item 2 requires the per-sign
face effect beside any M288 claim.

---

## 5. What this session did not establish

- **No semantic, phonetic or metrological value for any sign.** M288, N45, M263 and N01
  remain uninterpreted. Everything here is structural co-occurrence conditioned on physical
  face.
- **Novelty against specialist sign-by-sign literature remains unestablished**, exactly as
  in 2026-09-04 and 2026-09-17. Nothing in this session searched that literature, and no
  claim of priority is made.
- **The two arms are not two independent replications.** Their test statistics use disjoint
  informative blocks, but each arm's screen used the other arm's validation lines, so the
  Fisher combination in §3 is indicative only.
- **Replication on an independent CDLI export is still unrun** and remains the strongest
  available falsification test for all of this.
- The enumeration in §3 characterises the space of block-aware splits for M288–N45 only; it
  was not repeated for the other seven pairs.
- The homogeneity audit tests only forms with ≥ 15 eligible lines, so it is silent about
  rare variants, and it is uncorrected within family by design (the BH over 16 is reported
  alongside).

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
echo /abs/path/to/pe-sign-value-data/corpus > corpus_path.txt
PE_CORPUS="$(cat corpus_path.txt)" python3 -m unittest -v test_block_aware_split   # 9 tests
python3 recon.py "$(cat corpus_path.txt)"
python3 block_aware_split.py "$(cat corpus_path.txt)" --json results/block_aware_split.json
python3 exact_form_audit.py
```

No third-party packages; runtime under 15 s for the whole directory. `corpus_path.txt` is
the only machine-specific input and is deliberately not committed.
