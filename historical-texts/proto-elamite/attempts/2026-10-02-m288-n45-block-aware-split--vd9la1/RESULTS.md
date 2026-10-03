# Settling M288–N45: a block-aware split, and why "the eight constraints" was the wrong frame

**Session:** 2026-10-02, Breaker (Claude Opus 5, Claude Code cloud), advancing.
**Drawn:** `npm run draw` → stream B (rotation after 2026-09-27 stream A) → `historical-texts/proto-elamite`,
highest coverage debt in the stream. Named next move: HANDOVER item 1.
**Corpus:** SFU `pe-sign-value-data` @ [`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6),
LF digest `8849716c…bf2b2dcf`.
**Predictions frozen in [`PREDICTIONS.md`](PREDICTIONS.md), commit `31a1004`,** before any file in
`results/` existed.
**Code:** `common.py`, `block_aware_split.py`, `null_calibration.py`, `competitors.py`,
`competitor_null.py`; 10 tests in `test_block_aware_split.py`, all passing.

---

## Result in one sentence

M288–N45 is **confirmed** against the face confound — p = 9.7×10⁻⁵ at a p-floor of 4.5×10⁻⁹,
on a split that hands the exact test every informative block in the corpus and still clears an
independent re-screen on the complement — but the same sweep shows **72 of 390 testable
(M-sign, N-sign) pairs clear that gate against a null expectation of 9.4**, so the 2026-09-04
set of eight was a low-power *sample* of a pervasively structured corpus rather than the set of
its associations, and M288–N45 ranks 14th in it.

---

## 0. Reproduction first

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pinned commit. Every one of
the fifteen result rows reproduces: all contingency cells, odds ratios and q-values are identical
to the committed `analysis/results/associations.csv`, with p-values differing only in the last
one or two floating-point digits. Corpus audit matches exactly — 1,467 files, 10 without numbered
lines, 1,457 tablets, 11,013 lines, 4,869 eligible, 3,819 train / 1,050 validation. The six
`analysis/` unit tests pass.

The CRLF/LF digest caveat the handover flagged is confirmed exactly as recorded: a Linux checkout
gives `8849716c…bf2b2dcf` where `associations.json` records the Windows CRLF hash
`ee4fa7ba…c083d6a`. **It is not corpus drift. Do not re-pin.**

The 2026-09-17 matched self-match also reproduces: face-effect / sign-effect ratio **0.406**
against the recorded 0.408 (that script resamples, so small movement is expected).

**The load-bearing test.** `test_reproduces_2026_09_17_face_blocked_values` requires the
`floor_and_p` function behind every number below to return all eight of the 2026-09-17
face-blocked p-values *and* floors when handed that session's bucket-0 holdout, to a relative
tolerance of 1e-12. The reference is read from that session's committed
`results/power_floor.json` rather than retyped. It passes, so the new figures are like-for-like
with the old by construction.

---

## 1. Why the pair was untestable: 38 of its 56 co-occurrence lines carry no information

2026-09-17 established that the face-blocked test on bucket 0 had a p-floor of 0.12 and could not
return a significant answer whatever the data said. This session's first move was to ask *why*,
and the answer is structural rather than a matter of holdout size.

A `(tablet, face)` block is **informative** iff the within-block permutation has freedom —
`lo < hi`, where `lo = max(0, m_lines − (n_lines − n_sign_lines))` and
`hi = min(m_lines, n_sign_lines)`. A block with `lo == hi` is **forced**: its overlap is fixed by
its marginals, so it contributes a constant to the overlap total and *exactly zero* to the
p-value.

For M288–N45 across the whole eligible corpus (4,869 lines, 1,426 tablet-faces):

| | count |
|---|---:|
| blocks carrying ≥1 line with both signs | 50 |
| …of which **forced** (`lo == hi`) | **36** |
| …of which forced *and a single-line face* | **27** |
| informative blocks, corpus-wide | **16** |
| co-occurrence lines | 56 |
| co-occurrence lines in forced blocks | **38** |

So the face-blocked null discards **38 of the 56 co-occurrence lines as information-free by
construction**, and 27 of the 36 forced blocks are single-line faces — a face carrying one
eligible line, with M288 and N45 both on it, has no permutation freedom at all. The p-floor is
multiplicative over informative blocks (verified: bucket 0's four blocks give
0.8 × 0.6 × 0.5 × 0.5 = 0.12, reproducing the recorded floor exactly).

The 16 informative blocks are also distributed very unevenly across the 2026-09-04 hash buckets —
b0 = 4, b1 = 1, **b2 = 0**, b3 = 7, b4 = 4 — which is precisely why that session found the pair
"powered in 3 of 5 buckets". A 20% holdout gets about a fifth of 16 blocks. **No holdout of that
size could ever have settled this pair**, and the fix is not more data but a split that stops
throwing informative blocks away.

---

## 2. The split rule, and why selecting on it is not p-hacking

> **A tablet goes to VALIDATION iff it contributes at least one informative `(tablet, face)`
> block for the pair under test. Otherwise it goes to TRAINING.**

Fully determined, no tuning, no search over splits, no tablet on both sides. Informativeness is a
function of block **marginals** only — never of the observed overlap.

**Why it is legitimate.** The face-blocked exact test's null distribution is *already conditional*
on each block's marginals. Marginals are ancillary, so a block-selection rule that reads only
marginals cannot shift the null. Forced blocks have zero variance under that null, so excluding
them from the test set discards no information while leaving them available to the screen.

Two things make that argument checkable rather than rhetorical:

- `test_split_is_invariant_to_observed_overlap` permutes N45 *within* each `(tablet, face)` block
  25 times — preserving every marginal, moving only the overlap — and requires the validation
  tablet set to be bit-identical each time. It is.
- The selection is visibly not cherry-picking in the pair's favour. The two blocks with the most
  permutation freedom are `P008020 obverse` (overlap 4 of 4, maximally *for* the hypothesis) and
  `P272825 obverse` (overlap **0** of 2, maximally *against* it). A marginal-only rule takes both.
  One of the 16 selected blocks has zero overlap.

§3 measures the claim instead of arguing it.

---

## 3. The decisive check: the procedure has nominal size (P2, P3 — both confirmed)

20,000 replicates each, the full split-and-test code, two nulls that destroy any M/N association:

| | NULL A — permute N45 within each `(tablet, face)` | NULL B — permute N45 within face strata corpus-wide |
|---|---:|---:|
| preserves | every block marginal exactly | N45's total count and its obverse/reverse skew |
| destroys | the overlap only | tablet and face clustering; marginals re-drawn each rep |
| mean informative blocks | 16.0 (real: 16) | 16.7 (real: 16) |
| **size at α = 0.05** | **0.0171** | **0.0312** |
| median p | 0.625 | 0.610 |
| replicates reaching the real p | **2 / 20,000 (0.010 %)** | **1 / 20,000 (0.005 %)** |

**P2 predicted ≤ 7 %; both nulls come in under the nominal 5 %.** The test is *conservative*, as a
highly discrete exact test should be. Null B is the one that matters: it re-draws the marginals
every replicate, so the informativeness selection is genuinely exercised, and it still does not
inflate size. The ancillarity argument holds empirically.

Null A doubles as an implementation check. Under it the p-value must be uniform, and
2 of 20,000 replicates at or below p = 9.69×10⁻⁵ is exactly what uniformity predicts
(expectation 1.9). **P3 predicted < 1 %; observed 0.005–0.010 %.**

---

## 4. M288–N45 under the block-aware split (P1 — confirmed, declared foreseen)

Validation: 15 tablets, 98 lines, 16 informative blocks, observed overlap 19 of a possible 22.

| | bucket-0 holdout (2026-09-17) | block-aware split (this session) |
|---|---:|---:|
| informative blocks | 4 of 290 | **16 of 1,426** |
| **p-floor** | **0.12** — could not fire | **4.46×10⁻⁹** |
| face-blocked p | 0.47 | **9.69×10⁻⁵** |
| BH q across the eight | — | **1.29×10⁻⁴** |
| validation odds ratio | 16.29 | **13.47** |
| re-screen on complement | n/a | **q ≤ 1×10⁻⁴, OR 10.39, selected** |

The re-screen is a genuine independent gate: it runs on the 4,771 training lines, over all 1,417
candidate pairs meeting the 2026-09-04 support minima, with BH correction — and
`test_rescreen_uses_training_only_and_selects_m288_n45` asserts it never sees a validation line.

**P1 was labelled exploratory/foreseen in `PREDICTIONS.md` and must stay labelled that way.** With the
§1 diagnostic already showing 18 of 21 overlap across the informative blocks and an all-blocks
floor of 4.5×10⁻⁹, the outcome was foreseeable before the test was run. The session's prospective risk sat in P2–P6.

**Verdict: M288–N45 is confirmed against the face confound.** 2026-09-17's "untestable rather
than refuted" is resolved in favour of the constraint. The reopening condition in §7 is the usual
one, not a residual doubt about this test.

---

## 5. The split rule's cost, and the six pairs that fail the re-screen

Running the identical procedure on all eight 2026-09-04 pairs gives an outcome that needs stating
carefully, because the naive reading is wrong.

| pair | infB | obs/max | p-floor | face-blocked p | q | clears validation | re-screen q | re-screen OR | **confirmed** |
|---|---:|---:|---:|---:|---:|:--:|---:|---:|:--:|
| M297–N39B | 64 | 79/101 | 5.7e-42 | 9.49e-13 | 3.79e-12 | yes | 0.0000 | 6.23 | **YES** |
| M288–N45 | 16 | 19/22 | 4.46e-09 | 9.69e-05 | 1.29e-04 | yes | 0.0000 | 10.39 | **YES** |
| M263–N01 | 55 | 107/111 | 4.6e-31 | 1.49e-23 | 1.19e-22 | yes | 0.1023 | 2.26 | no (screen) |
| M263–N30C | 27 | 0/41 | 3.52e-10 | 3.52e-10 | 9.38e-10 | yes | 0.0394 | 0.07 | no (screen) |
| M297–N01 | 61 | 43/97 | 4.7e-39 | 1.32e-07 | 2.11e-07 | yes | 0.0026 | 0.47 | no (OR gate) |
| M106–N24 | 12 | 14/19 | 3.9e-16 | 6.66e-08 | 1.33e-07 | yes | 1.0000 | 0.44 | no (screen) |
| M243–N39B | 12 | 15/18 | 6.46e-09 | 1.75e-04 | 2.01e-04 | yes | 0.2692 | 2.75 | no (screen) |
| M297–N24 | 34 | 27/49 | 2.0e-26 | 1.07e-02 | 1.07e-02 | yes | 0.0348 | 2.50 | no (screen) |

**All eight pairs now have ample power (every floor ≤ 3.5×10⁻¹⁰ except the two at ~5×10⁻⁹) and all
eight clear the face-blocked validation test at q ≤ 0.05.** Only two also clear the re-screen —
and that is a property of my split rule, not evidence against the other six.

The mechanism is exact. The rule moves every tablet with an informative block into validation, and
those are precisely the tablets where the two signs co-occur *with freedom*. So it strips the
screen of a pair-specific fraction of that pair's evidence:

| pair | co-occurrence lines | moved to validation | full-corpus OR | **training OR** | screen |
|---|---:|---:|---:|---:|:--|
| M288–N45 | 56 | 19 (**33.9 %**) | 13.57 | **10.39** | passes |
| M297–N01 | 117 | 43 (36.8 %) | 0.29 | 0.47 | fails OR gate (q = 0.0026) |
| M297–N39B | 135 | 79 (58.5 %) | 9.79 | **6.23** | passes |
| M297–N24 | 44 | 27 (61.4 %) | 4.04 | 2.50 | fails (OR < 3) |
| M263–N01 | 176 | 107 (60.8 %) | 4.24 | 2.26 | fails (q = 0.10) |
| M243–N39B | 22 | 15 (68.2 %) | 6.47 | 2.75 | fails (OR < 3) |
| M106–N24 | 14 | 14 (**100 %**) | 5.54 | **0.44 — direction flips** | fails (q = 1.0) |
| M263–N30C | 0 | 0 | 0.04 | 0.07 | fails (q = 0.039) |

**The cost of the split is proportional to how much of a pair's evidence lives in informative
blocks — and M288–N45 pays the least of any enriched pair.** The very property that made it
untestable on a 20 % holdout, its evidence being concentrated in forced single-line faces, is what
leaves its screen intact when the informative tablets are removed. This rule happens to suit this
pair almost perfectly, which is worth saying out loud rather than presenting as a general method.

M106–N24 is the clearest case: all 14 of its co-occurrence lines sit in informative blocks, so the
training set contains none and the training odds ratio **inverts** to 0.44. A session that read
that as "M106–N24 refuted" would be reading its own split.

**P4 confirmed as stated.** Its failure condition was any load-bearing pair failing *with a floor
below 0.05*. All three — M297–N39B, M263–N01, M263–N30C — have floors ≤ 4.6×10⁻³¹ and clear
validation at q ≤ 1.2×10⁻²². None is demoted.

**P5 FAILED, and the earlier tiering is corrected.** I predicted M243–N39B would have fewer than
10 informative blocks corpus-wide and a floor above 0.01, with a stated failure condition of a
floor below 0.001. It has **12 informative blocks and a floor of 6.46×10⁻⁹**, and clears validation
at p = 1.75×10⁻⁴. 2026-09-17's "barely testable, powered in only 2 of 5 buckets" was a fact about
a 20 % holdout, not about the corpus: **the power was there and the bucket split was wasting it.**
The honest reading is that I inherited that verdict and repeated it in a frozen prediction without
re-deriving it.

---

## 6. P6 failed, and this is the session's most consequential finding

The frozen prediction was that M288–N45 would rank in the top 15 of all pairs put through this
procedure, and that **fewer than 40** pairs would pass. Sweeping every `(M-family, N-sign)` pair
with ≥ 20 supporting lines on each margin, direction taken from the training complement so each
p-value is a clean one-sided test:

| | real corpus | NULL B, 200 replicates |
|---|---:|---:|
| pairs testable | 390 | 608.6 (mean) |
| …with power at 0.05 | 292 | — |
| **pairs passing at 0.05** | **72** | **mean 9.4, median 9, range [3, 19], 95th pct 14** |
| passing as a share of testable | **18.5 %** | **1.5 %** |
| M288–N45 rank | **14 / 390** | reached the real p in **0 / 200** replicates |

**Rank confirmed (14th, inside the predicted top 15); count failed badly (72 against a predicted
< 40).**

The null sweep tests *more* pairs than the real one (608.6 vs 390) because permuting an N-sign
spreads it across more faces and so creates more informative blocks and clears the support gates
more often. The denominators therefore differ, and the comparison is reported both ways above:
72/390 = 18.5 % against 9.4/608.6 = 1.5 %, about **12× enrichment** either way, with the real
count far outside the null's entire 200-replicate range.

So the 72 is **not** procedural permissiveness — §3 already showed the test is conservative, and
the null sweep confirms it at corpus scale. The conclusion is the other branch:

> **Proto-Elamite accounting is pervasively structured at the sign-pair level, and the
> 2026-09-04 "eight confirmed constraints" was a low-power sample of that population, not the set
> of associations the corpus supports.**

This does not weaken M288–N45, whose own p-value is unaffected. It changes what membership in the
eight *means*. Pairs ranking above M288–N45 that the 2026-09-04 design never reported include
M288–N39B (p = 1.7×10⁻²⁹), M288–N24 (1.1×10⁻¹⁹), M376–N08A (1.6×10⁻¹³), M106–N01 (2.4×10⁻¹¹) and
M354–N14 (3.1×10⁻⁷). The folder's constraint list should be read as "eight that a 20 % holdout at
these thresholds happened to catch", and any future argument resting on a pair *being one of the
eight* needs re-grounding.

A deliberate deviation, recorded because it inflates a number: `competitors.py` takes each pair's
direction from its *validation* odds ratio, to give every competitor its best shot. That is
double-dipping and yields 560 tested / 121 passing / rank 27. `competitor_null.py` takes direction
from the training complement, which is the clean one-sided procedure, and is the source of every
figure in the table above. **The 72 is the number to cite; the 121 is not.**

### The face-effect number this ranking is required to carry

HANDOVER item 2 requires any ranking to report the face effect of the signs it ranks.
Re-running `matched_selfmatch.py`: corpus-wide face effect / sign effect = **0.406**
(2026-09-17: 0.408), and **M288's own face effect is 0.0238 against a mean between-sign signal of
0.0222 — a ratio of 1.07**, making it one of the four signs that individually exceed the
between-sign signal. M288 is genuinely face-sensitive, which is exactly why this pair needed a
face-blocked test with real power, and why the §3 calibration under a face-skew-preserving null is
load-bearing rather than decorative.

---

## 7. Status, limits, and what is not claimed

**Settled.** M288–N45 is confirmed against the face confound: p = 9.69×10⁻⁵ at a floor of
4.46×10⁻⁹, procedure size 1.7–3.1 % at nominal 5 %, 1–2 of 20,000 null replicates as extreme, and
an independent re-screen on 4,771 held-out-from-validation lines at q ≤ 10⁻⁴. HANDOVER item 1 is
discharged.

**Corrected.** M243–N39B is not "barely testable" (12 informative blocks, floor 6.46×10⁻⁹). The
constraint set's eight members are a power-limited sample of ≥ 72 comparable associations.

**Limits.**
- Nothing here assigns a phonetic, lexical or metrological value to M288, N45 or any other sign.
  The result is a structural constraint and a statement about how much power the corpus can supply.
- The split rule is pair-specific, so BH correction is taken across the same eight pairs the
  2026-09-04 design reported; the 72-pair sweep is reported as raw counts against its own null,
  not as 72 individually corrected discoveries.
- The rule suits M288–N45 unusually well (§5). It is not a general-purpose replacement for a
  random holdout, and a successor applying it elsewhere must report the moved-evidence fraction.
- One corpus snapshot. Replication on an independent CDLI export remains the strongest
  falsification test and is still unrun.
- Novelty against specialist sign-by-sign literature remains unestablished — now a sharper gap
  than before, since the sweep names ~72 associations rather than 8.

**Reopening condition.** M288–N45 reopens if it fails, in direction, on an independent CDLI
export, or if the SFU value-annotation layer this corpus depends on is revised for M288 or N45.
