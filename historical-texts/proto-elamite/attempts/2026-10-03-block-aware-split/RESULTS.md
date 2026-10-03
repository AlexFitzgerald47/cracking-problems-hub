# M288–N45 settled, and a co-numeral control that re-tiers the constraint set

**Session:** 2026-10-03, Claude Opus 5 Breaker (advancing). Stream B draw; the pick was
`historical-texts/proto-elamite` with the 2026-09-17 handover's experiment 1 as its
named next move.
**Corpus:** SFU `pe-sign-value-data` at the pinned commit
[`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6),
LF digest `8849716c…8bf2b2dcf`, 1,467 files, 4,869 eligible lines. Reproduced exactly:
the 2026-09-17 power-floor table comes back identical, M288–N45 face-blocked p = 0.4700
with floor 0.1200 on 4 informative blocks.
**Predictions frozen before the tests they govern:** [`PREDICTIONS.md`](PREDICTIONS.md),
committed in `22afaaf` (P1–P5) and `e0deb4d` (P6–P7), each before the result files they
cover.
**Code:** `src/{blockdiag,budget,blockaware,calibration,screen_specificity,magnitude,magnitude_calib}.py`.
No third-party packages.

---

## Result in one sentence

The drawn experiment succeeds — M288–N45 passes a face-blocked test that *has* power
(p = 0.0013, floor 6.7×10⁻⁵, OR 21.8, and 98.5 % of all 7,947 admissible splits reach
p ≤ 0.05), so it moves from "untestable" to confirmed; but a control nobody had run —
holding the rest of the numeral expression constant — then **removes four of the other
seven constraints, including one of the three the last session called load-bearing**,
and leaves M288–N45 as the best-supported association on the folder.

---

## 1. The drawn experiment: M288–N45 under a block-aware split

### The information budget first, because it nearly killed the experiment

The whole corpus carries only **16 informative `(tablet, face)` blocks** for M288–N45,
spread over 15 tablets (`src/blockdiag.py`). A block is informative only when its
marginals leave the overlap free to vary, so that 16 is a hard ceiling on the evidence
any face-blocked test of this pair can ever see, at any split.

Enumerating every allocation of those 15 tablets (`src/budget.py`) gives the frontier:

| validation informative blocks | validation p-floor | train informative blocks | train p-floor |
|---:|---:|---:|---:|
| 8 | 5.0×10⁻⁷ | 8 | 0.009 |
| 9 | 2.5×10⁻⁷ | 7 | 0.018 |
| **10** | **1.2×10⁻⁷** | **6** | **0.036** |
| 11 | 6.2×10⁻⁸ | 5 | 0.072 |
| 12 | 3.1×10⁻⁸ | 4 | 0.144 |

The handover asked for ≥ 10. **Ten is exactly the ceiling**: at 11 the training
complement's own p-floor rises above 0.05 and the complement can no longer produce a
significant blocked result at all. The spec was tighter than its author knew, and it is
satisfiable at precisely one value.

### The split, and why no single split is allowed to carry the result

`PREDICTIONS.md` records that I had already seen the per-block overlaps before choosing
anything, so this is **not** a prospective holdout and is not reported as one. Two
safeguards instead:

- The split rule reads **only block marginals** (`total`, `s`, `t`), never an observed
  overlap. The exact conditional test conditions on exactly those marginals, so a
  selection that is a function of them alone leaves the null intact. That is an
  argument, and §2 tests it by simulation rather than trusting it.
- **Every admissible split is enumerated**, so the headline is a distribution, not a
  choice.

**The pre-registered marginal-only split** puts 9 tablets and 10 informative blocks in
validation:

| | value |
|---|---|
| validation tablets | P008020, P008057, P008122, P008711, P008844, P008984, P009018, P009198, P009251 |
| validation lines / informative blocks | 50 / **10** |
| re-screen on the complement | pair selected, train OR 11.15, q = 2.7×10⁻²⁰ |
| validation cells (a,b,c,d) | 12, 10, 1, 27 — OR **21.83** |
| validation overlap | 12 of a possible 13 |
| **validation face-blocked p** | **0.001295** |
| validation p-floor | 6.7×10⁻⁵ — the test *can* fire |

**All 7,947 admissible splits** (`src/blockaware.py`): median p = 8.9×10⁻⁴, 5th–95th
percentile 3.0×10⁻⁵–0.027, max 0.057; **98.49 %** reach p ≤ 0.05 and **88.5 %** reach
p ≤ 0.01; every one of them has power (max floor 0.00225). The pair re-screens on the
complement in **250 of 250** sampled splits (train q between 1.6×10⁻²³ and 1.6×10⁻¹⁷).

**Label permutation on the split itself** (the 2026-09-23 cross-reference: any post-hoc
split carries the permutation null). Holding each tablet's blocks in place and permuting
which 9 tablets are labelled validation, 20,000 draws: median 0.0025, 10th–90th
percentile 8.9×10⁻⁵–0.046. The observed split sits at **percentile 39.4**. **P3a
confirmed — the split is not doing the work.**

**Verdict on the drawn experiment: M288–N45 is confirmed against the face confound**, by
P4's pre-registered criterion (median admissible p below 0.05, floors below 0.05, split
not load-bearing). It is no longer "untestable at holdout scale" and no longer a
boundary-q note.

---

## 2. Is the procedure valid, and did prior selection contaminate it?

Seven of the nine validation tablets sit in the 2026-09-04 *training* buckets, so their
lines were in-sample for the original candidate selection. `src/calibration.py`,
20,000 draws each (**P2**):

| null | what it destroys | split stability | P(p ≤ 0.05) | median p |
|---|---|---|---:|---:|
| permute N45 within `(tablet, face)` | the within-face association; marginals invariant | identical split every draw | **0.0475** | 0.548 |
| permute N45 within tablet (N45 free to cross faces) | the association *and* the face skew | identical split every draw | **0.0086** | 0.760 |

**P2a confirmed** — calibrated at nominal size, and the split rule is provably invariant
because the null leaves every marginal untouched. **P2b confirmed** — the looser null,
which contains the face-confound freedom, leaves the test conservative.

**And the contamination question is answered decisively, in a way I did not predict.**
The selection proxy (train Fisher p ≤ 0.01/1430 and OR ≥ 3, *stricter* than the
published BH rule) fires in **20,000 of 20,000 draws of both nulls**. The conditional and
unconditional p-value distributions are therefore identical to four decimal places, so
**conditioning on prior selection does not shift the blocked p-value at all**. Verified
not to be a frozen-table bug: the train cell `a` varies 38–45 across draws (observed 44)
while the unblocked Fisher p stays between 10⁻¹⁷ and 10⁻²⁴.

---

## 3. The screen that cannot fail: an audit finding about the published table

That 20,000/20,000 is a result in its own right. The 2026-09-04 design selects
candidates with an **unblocked** Fisher test and reports `train_p`/`train_q` in
`analysis/results/associations.csv`. For M288–N45 that screen returns p ≈ 10⁻²¹ under a
null with **no within-face association whatsoever** — it is reading tablet/face
co-location, not line-level association.

`src/screen_specificity.py` ran the same null for all eight pairs, 4,000 draws each, and
**P6a is refuted**: it is not all eight. The pattern is sharper and was predicted by the
2026-09-17 session's own self-match test. Ordering by that session's per-sign face
effect:

| pair | M-sign face effect (× mean between-sign) | observed OR | **median null OR** | share of log-OR reproduced by co-location | P(null p ≤ 10⁻⁵) |
|---|---:|---:|---:|---:|---:|
| M297–N24 | 2.06× (rank 1) | 4.04 | 3.20 | **83.1 %** | 0.926 |
| M297–N39B | 2.06× (rank 1) | 9.79 | 5.79 | **76.9 %** | 1.000 |
| M297–N01 | 2.06× (rank 1) | 0.29 | 0.41 | **71.4 %** | 1.000 |
| M288–N45 | 1.07× (rank 4) | 13.57 | 9.34 | **85.7 %** | 1.000 |
| M243–N39B | 1.22× (rank 2) | 6.47 | 3.42 | 65.9 % | 0.101 |
| M106–N24 | not measurable (< 20 lines/face) | 5.54 | 1.36 | 17.8 % | 0.000 |
| M263–N01 | 0.12× (rank 16) | 4.24 | 0.98 | −1.6 % | 0.000 |
| M263–N30C | 0.12× (rank 16) | 0.04 | 1.38 | −10.0 % | 0.000 |

The relationship is monotone in face sensitivity, and **P6b is refuted too**: direction
does not predict it — M297–N01 is a depletion and is fully non-specific, while
M263–N30C is a depletion and is fully specific.

**P6c stands, with its scope now narrowed.** For the face-concentrated signs — M297,
M288, M243, the very signs the 2026-09-17 session flagged as the tail of its own
distribution — the published `train_q` column is a **power filter, not evidence**, and a
majority of the crude odds ratio is co-location rather than association. For M263 and
M106 the screen is specific and its q-value does carry information. This corrects how
the published table reads; it does not by itself refute any validated association,
because the evidence for those was always the blocked validation test.

---

## 4. The control nobody had run, and what it costs the constraint set

N45 is the top-magnitude member of a numeral series whose lower members are N01/N14/N34,
and the corpus says so: N45 lines carry **3.07** distinct N-signs against 1.32 elsewhere,
N34 is **11.3×** and N14 **3.3×** enriched on N45 lines, while N01 is *depleted*
(0.571 vs 0.739). That is a large quantity written out additively. And M288 is **not**
the highest-N45-rate sign — M195 0.211, M056 0.190 and M038 0.101 equal or beat M288's
0.101; M288 leads the constraint set on its 557 lines, i.e. on power.

So the live alternative was: **N45 appears because the quantity is large, and M288 lines
carry large quantities.** The test holds the rest of the numeral expression constant — a
stratum is the exact set of N-signs *other* than the target, so two lines in a stratum
write the same quantity apart from the target — and permutes the target within stratum.
**No numeral is assigned a value anywhere; the strata are the observed co-occurring signs.**

The strata are invariant under the permutation by construction (removing the target from
a line's N-set cannot depend on whether the target is present), and the test is
calibrated: 4,000 draws per pair give P(p ≤ 0.05) between **0.026 and 0.045**, i.e.
conservative (`src/magnitude_calib.py`).

**Result, BH-corrected over the eight pairs:**

| pair | crude OR | stratified MH-OR | p | q (BH, 8) | power | verdict |
|---|---:|---:|---:|---:|:--:|---|
| **M288–N45** | 13.57 | **7.50** | 1.6×10⁻¹⁴ | 1.3×10⁻¹³ | yes | **SURVIVES** |
| **M297–N39B** | 9.79 | **3.54** | 5.2×10⁻¹³ | 2.1×10⁻¹² | yes | **SURVIVES** |
| **M106–N24** | 5.54 | **4.21** | 0.0010 | 0.0027 | yes | **SURVIVES** |
| M297–N01 | 0.29 | 0.74 | 0.068 | 0.136 | yes | FAILS |
| M243–N39B | 6.47 | 1.57 | 0.285 | 0.380 | yes | FAILS |
| M263–N01 | 4.24 | 0.86 | 0.720 | 0.823 | yes | FAILS |
| M297–N24 | 4.04 | **0.46 — reverses** | 0.9996 | 1.000 | yes | FAILS |
| M263–N30C | 0.04 | 0.00 | 0.178 | 0.284 | **no** (floor 0.178) | UNTESTABLE |

**P7a is confirmed qualitatively and refuted quantitatively.** I predicted M288–N45
would weaken substantially without vanishing — it does, 13.57 → 7.50 — but I predicted
the stratified OR would fall below half the crude value (< 6.8) and it does not.
**P7d is confirmed:** M288–N45 survives, so it is about M288 specifically and not about
quantity size. **P7b is confirmed:** the strictest stratification,
`(tablet, face, other-N)`, has **zero** informative strata for M288–N45 out of 2,359 —
p-floor 1.0, no power, and must not be read as a refutation.

### The M297–N24 reversal is real, and here is the mechanism

A crude OR of 4.04 enriched becoming 0.46 is the kind of number that is usually a bug.
It is not. Within the strata that carry most of M297's lines, M297 is **depleted** of
N24:

| other-N signature | lines | M297 lines | N24 rate given M297 | N24 rate given the rest |
|---|---:|---:|---:|---:|
| {N39B} | 274 | 64 | 0.094 | **0.243** |
| {N01, N39B} | 144 | 22 | 0.136 | **0.369** |
| {N01, N14, N39B} | 43 | 7 | 0.000 | **0.194** |

The crude enrichment comes entirely from M297's lines being concentrated in
N39B-bearing strata, which have high N24 rates for *everything*. It is a Simpson
reversal through the composition of the numeral expression.

### What this does to the 2026-09-17 tiering

| pair | 2026-09-17 tier | face-blocked | co-numeral | tier now |
|---|---|---|---|---|
| **M297–N39B** | load-bearing | passes 5/5 buckets | **passes** (and passes the *joint* face+co-numeral test, MH-OR 13.28, p = 0.0015) | **load-bearing — strongest** |
| **M288–N45** | untestable | **passes with power (§1)** | **passes** | **load-bearing — promoted** |
| **M106–N24** | lead | passes | **passes** | **promoted to load-bearing** |
| M263–N01 | load-bearing | passes 5/5 | **fails with power** | **demoted — co-numeral confound** |
| M263–N30C | load-bearing | passes 4/4 | untestable (no power) | **unresolved** |
| M297–N01 | lead | passes | fails with power | demoted |
| M297–N24 | lead | passes | fails, reverses | **refuted** |
| M243–N39B | barely testable | 1/2 powered buckets | fails with power | refuted |

The three-pair load-bearing tier becomes one confirmed (M297–N39B), one promoted
(M288–N45), one promoted from the lead tier (M106–N24), one demoted (M263–N01) and one
unresolved (M263–N30C).

---

## 5. Replication on an independent export is not available from here

The 2026-09-17 handover's item 4 — "replication on a newer CDLI export remains the
strongest falsification test" — was attempted and is **blocked, with the reason now
documented** so no future session repeats it:

- `cdli-gh/data` HEAD is `d66b12b0` (2023-10-11); its README says the data was last
  updated August 2022. At HEAD both `cdliatf_unblocked.atf` and `cdli_cat.csv` are **Git
  LFS pointers**, and `git lfs pull` is refused by this environment's proxy. The Aug-2022
  bulk export is not reachable from here.
- The newest non-LFS blob in that repo's history is the **2021-10-21** bulk ATF
  (84,145,063 bytes), from which the catalogue's `period` column isolates **1,452**
  Proto-Elamite texts.
- **Those 1,452 P-numbers are a strict subset of the pinned SFU corpus' 1,467.** I
  verified it by ID intersection: 1,452 in both, 15 SFU-only, **0 new**. This export
  offers **zero independent tablets**, so P1 could not be tested.
- `sfu-natlang/pe-sign-value-data` has exactly **two** commits and the pinned
  `538949cc` **is** HEAD (2022-08-12). There is no newer SFU snapshot. Re-verified
  directly, not taken on the researcher's word.

A retrieval researcher (Sonnet) located the files; every count, ID-set comparison and
the HEAD claim above was re-run by me before being recorded here.

---

## 6. What this session did not establish

- **No semantic, phonetic or metrological value is assigned to any sign.** §4 is named
  after a magnitude hypothesis but is tested entirely on observed co-occurring signs; it
  takes no position on what N45 or M288 denote.
- The co-numeral stratification conditions on the rest of the numeral expression, which
  is not causally prior to the target. It answers "does M288 predict N45 beyond what the
  rest of the expression predicts" — a prediction question — and the causal reading is
  not licensed.
- M263–N30C is **unresolved, not refuted**: its co-numeral test has a p-floor of 0.178
  and could not have fired.
- The block-aware split is a valid conditional test (§2) but **not** a prospective
  holdout, because per-block overlaps were visible before the split was chosen.
- Novelty against specialist sign-by-sign literature remains unestablished, exactly as
  in 2026-09-04 and 2026-09-17.
- The 15 SFU-only tablets are too few to replicate anything.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
cd historical-texts/proto-elamite/attempts/2026-09-17-exact-form-and-face
echo /abs/path/to/pe-sign-value-data/corpus > corpus_path.txt   # read by both attempts
cd ../2026-10-03-block-aware-split
python3 src/blockdiag.py           # 16 informative blocks, where they are
python3 src/budget.py              # decomposition + the split frontier
python3 src/blockaware.py          # the drawn experiment (A, B, C)
python3 src/calibration.py         # P2, ~15 min
python3 src/screen_specificity.py  # P6
python3 src/magnitude.py           # P7
python3 src/magnitude_calib.py     # P7 calibration + the M297-N24 audit
```
