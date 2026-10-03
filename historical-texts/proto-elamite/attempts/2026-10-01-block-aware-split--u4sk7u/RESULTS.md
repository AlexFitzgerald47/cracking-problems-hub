# M288–N45 settled, and the holdout that was costing the folder its power

**Session:** 2026-10-01 · breaker · Claude Opus 5
**Assignment:** `npm run draw` → stream B → `historical-texts/proto-elamite`; the
handover's recommended experiment 1, *settle M288–N45 with a block-aware split*.
**Corpus:** SFU `pe-sign-value-data` at the pinned commit
`538949cca949a176400b144ef49c2036e9dc82a6`, 1,467 files, Linux digest
`8849716c6afbf963e5ee02535da013c87c931c61e88e2c05ced9cd58bf2b2dcf` — the hash the
2026-09-17 handover predicted a Linux checkout would give. No drift; no re-pin.
**Frozen predictions:** `PREDICTIONS.md`, committed before any new p-value existed.

No lexical, phonetic or metrological value is assigned to any sign anywhere below.

---

## Result in one paragraph

M288–N45 **confirms**, refuting this folder's own 2026-09-17 frozen prediction A2. But
the reason it had failed is more useful than the pair: the face-blocked test had no
power because **M288 saturates its blocks** — it is the single most face-saturating
sign in the corpus, occupying *every* eligible line on 179 of the 350 faces where it
occurs, so 38 of its 56 N45 co-occurrences are logically forced and invisible to any
within-face test. Chasing that down produced the session's larger finding: for an
*exact conditional* test the 2026-09-04 design's 80/20 tablet holdout protects against
nothing and costs most of the power, because selection on block **marginals** is
ancillary to the conditional null. Replacing the holdout with multiple-testing
correction over the full candidate space and running the valid test corpus-wide yields
**26 pairs at p ≤ 1e-4 — 20 of them new to this folder — against 0.02 expected under a
500-replicate within-face permutation null** whose largest count was 1.

## Pipeline validation first

Two reproductions were run before anything new was believed.

1. The unchanged 2026-09-04 pipeline on a fresh clone: 1,467 files, 1,457 tablets,
   11,013 lines, 4,869 eligible, 15 confirmed associations — **byte-identical** to the
   committed `analysis/results/associations.json` on every cell of all 15 rows. Six
   unit tests pass.
2. This session's generalised block code reproduces the 2026-09-17
   `results/power_floor.json` to within 1e-12 on **all 16 cells** (8 pairs × 2 block
   schemes), including the observed overlap, max-possible overlap, informative-block
   count and block count. `src/validate_pipeline.py`.

A third check guards the new parser: `src/finer_blocks.py` adds column and entry
identity and is asserted line-for-line against the audited parser — same count, same
order, same `m_signs`, same `n_signs`, same damage flag on all 11,013 lines.

## The frozen predictions, scored

| | prediction | outcome | number |
|---|---|---|---|
| **P1** | block-aware split still lets the complement screen select the pair | **HOLDS** | re-screen q = 1.13e-16, pooled OR = 10.39, selected |
| **P2** | face-blocked floor ≤ 0.01 under that split | **HOLDS** | floor = 4.46e-9 |
| **P3** | face-blocked p ≤ 0.05 — the pair confirms | **HOLDS** | **p = 9.695e-5** |
| **P4** | procedure calibrated, FPR@0.05 in [0.03, 0.07] | **FAILS** | FPR = 0.0150 — *conservative*, see below |
| **P5** | M288 is a face-level marker; face-level test fires | **FAILS** | p = 0.109, floor 0.0156 (powered, did not fire) |

### P1–P3 — the pair confirms

The split: validation = **every tablet owning an informative `(tablet, face)` block**
for the pair (15 distinct tablets for M288–N45); training = all other tablets. The
unchanged 2026-09-04 screen was re-run on that complement and still selects the pair.
The face-blocked exact test on validation gives p = 9.695e-5 with 16 informative
blocks and a floor of 4.46e-9. Column-level blocking gives the identical p. M288–N45
moves from **"untestable at holdout scale"** to **load-bearing**.

Run for all eight pairs, not only the pair of interest (`src/block_aware_split.py`):
M297–N39B also confirms; the other six lose their training screen, because for those
pairs the informative blocks *are* the evidence and moving them all into validation
leaves nothing to screen on. That asymmetry is itself the clue to the holdout problem.

### P4 — the split does not inflate the test; it is conservative

The validation set is chosen using the pair's own block marginals, which is a
post-hoc, pair-specific split, and this folder's standing instruction is that such a
split carries a permutation null before its difference is interpreted. The argument
that it is safe: **informativeness is a function of the block marginals alone and
never of the overlap**, and the exact conditional null holds those marginals fixed.

`src/calibration.py` does not take that on trust. It permutes the target within every
`(tablet, face)` block over the whole corpus, re-derives the informative-block set from
the permuted data, re-splits and re-tests, 2,000 times for each of the eight pairs.
**The split moved in 0 of 16,000 replicates.** The realised false-positive rate is
0.0150 at nominal 0.05 and 0.0040 at nominal 0.01 for M288–N45, and ≤ 0.0525 / ≤ 0.0060
for every pair.

P4 is scored **failed** because its band was two-sided and 0.0150 falls below it. The
failure is in the direction that makes P3 stronger, not weaker: an exact test on a
statistic this discrete — most informative blocks have `hi − lo = 1`, so the null lives
on a coarse lattice — satisfies P(p ≤ α) ≤ α rather than = α. The frozen band was the
wrong shape for a discrete test, and that is a defect in the prediction, not a rescue
of the result.

### P5 — M288 is not a face-level marker

The occupancy diagnostic suggested M288 might be marking whole faces rather than
lines. It is not. With the tablet-face as the unit and the tablet as the block — so a
tablet's obverse is read against its own reverse — M288-bearing faces are *not*
significantly enriched for N45: **p = 0.109**, floor 0.0156, so the test was powered and
simply did not fire. Direction is right (pooled face OR 6.97, 52/298/26/1050) and the
effect may be real and small, but this folder may not claim it. Negative result,
reported as confidently as the positive one.

## Why the 2026-09-17 test failed: occupancy, not sample size

| sign | lines | faces | mean within-face occupancy | faces where it occupies *every* line |
|---|---:|---:|---:|---:|
| M106 | 59 | 31 | 0.291 | 2 (6.5 %) |
| M263 | 191 | 109 | 0.408 | 15 (13.8 %) |
| M243 | 46 | 37 | 0.573 | 13 (35.1 %) |
| M297 | 252 | 186 | 0.614 | 75 (40.3 %) |
| **M288** | **557** | **350** | **0.701** | **179 (51.1 %)** |

Among the 145 signs occurring on ≥ 10 faces, **M288 ranks first on saturation.** A
within-block conditional test cannot see a covariate that fills its blocks: where every
line of a face carries M288, any N45 on that face co-occurs with M288 by arithmetic, and
the block contributes a point mass, not information. 38 of the pair's 56 co-occurrences
sit in such blocks.

This is a **structural** power ceiling, not a sample-size one. More tablets of the same
kind add forced blocks, not evidence. The 2026-09-17 session read the floor of 0.12
correctly as "untestable" — the missing step was asking *what property of the data*
produced it.

## The block ladder, and one result withdrawn

`src/block_ladder.py` runs the exact conditional test at four grains:
tablet → face → column → **accounting entry** (ATF labels `2.A.` / `2.B.` are two
sub-lines of one numbered entry; the corpus has 401 such sub-entry lines).

M288–N45: tablet 3.21e-9 · face 9.70e-5 · column 9.70e-5 · entry 3.125e-2.

**The entry-level value is withdrawn.** Its five informative entry blocks all come from
a **single tablet, P008020**, and 3.125e-2 is exactly 2⁻⁵ — the test returned its own
floor, so it carries no information beyond "one tablet was consistent five times". Under
BH across the eight pairs the entry rung does not clear 0.05 for this pair in any case.
Five of the eight pairs have **zero** informative entry blocks, because 4,628 entry
blocks hold 4,869 lines: almost every entry is a single line. *Use independent objects as
replicates* — the face-level result, by contrast, draws its 16 blocks from **15 distinct
tablets**, and every pair in the table below rests on ≥ 4.

## The holdout was the wrong instrument

The 2026-09-04 design screens on 80 % of tablets with a pooled Fisher test, then
validates on 20 % with a blocked exact test. The holdout is there because the *screen's*
p-values are invalid — pooled Fisher treats same-tablet lines as independent, which they
are not. But the **validation statistic is valid on its own**: it conditions on block
marginals and needs no holdout at all. What reporting a pair selected by its own p-value
does require is multiple-testing correction, and BH over the candidate space supplies it.
So the holdout buys nothing the correction does not, and costs ~80 % of the data.

Running the valid test corpus-wide over every pair meeting the published support
thresholds (≥ 20 sign-lines, ≥ 20 target-lines): **1,430 candidate pairs, 514 of which
are powered** (face-blocked floor ≤ 0.05 — again a function of marginals only, so
restricting to them is ancillary too).

| threshold | pairs observed | null mean (500 reps) | null max | permutation p |
|---|---:|---:|---:|---:|
| p ≤ 0.05 | 124 | 22.57 | 39 | 0.0020 |
| p ≤ 0.01 | 62 | 3.42 | 11 | 0.0020 |
| p ≤ 1e-3 | 32 | 0.27 | 3 | 0.0020 |
| **p ≤ 1e-4** | **26** | **0.02** | **1** | **0.0020** |

The null permutes every N-sign's line membership within each `(tablet, face)` block over
the whole corpus and re-runs the entire 1,430-pair sweep, 500 times — ~257,000 null
tests. It preserves every block marginal, hence the powered set, and destroys only the
association. 0.0020 is the floor at 500 replicates. The **smallest p anywhere in the
whole null ensemble is 1.428e-5**, against an observed sweep minimum of **1.683e-29**.

### The expanded constraint set — 26 pairs at p ≤ 1e-4

Full table with all columns: `results/constraint_table.csv` / `.json`; all 514 powered pairs
in `results/search_budget_powered.csv`. The full 1,430-row dump is not committed — 
`src/search_budget.py` regenerates it in about a second, and the 916 unpowered pairs cannot
return a significant answer at any data. BY = Benjamini–
Yekutieli over the 514 powered tests (factor 6.82), which is valid under arbitrary
dependence and is the number to quote, since the 1,430 tests reuse 110 M-signs and 13
N-signs and are certainly not independent.

| pair | dir | status | pooled OR | p | BY q | inf. blocks | distinct tablets |
|---|---|---|---:|---:|---:|---:|---:|
| M288–N39B | enr | **new** | 3.60 | 1.68e-29 | 5.90e-26 | 72 | 67 |
| M263–N01 | enr | published | 4.24 | 1.49e-23 | 2.61e-20 | 55 | 54 |
| M288–N24 | enr | **new** | 4.07 | 1.06e-19 | 1.24e-16 | 44 | 41 |
| M376–N08A | enr | **new** | 98.82 | 1.62e-13 | 1.42e-10 | 16 | 12 |
| M297–N39B | enr | published | 9.79 | 9.49e-13 | 6.65e-10 | 64 | 60 |
| M106–N01 | dep | **new** | 0.45 | 2.36e-11 | 1.38e-08 | 17 | 17 |
| M263–N30C | dep | published | 0.04 | 3.52e-10 | 1.76e-07 | 27 | 25 |
| M106–N30C | enr | **new** | 3.37 | 6.49e-09 | 2.84e-06 | 4 | 4 |
| M106–N24 | enr | published | 5.54 | 6.66e-08 | 2.59e-05 | 12 | 11 |
| M297–N01 | dep | published | 0.29 | 1.32e-07 | 4.62e-05 | 61 | 59 |
| M354–N14 | enr | **new** | 2.87 | 3.13e-07 | 9.99e-05 | 27 | 24 |
| M264–N01 | enr | **new** | 4.18 | 1.06e-06 | 2.94e-04 | 20 | 20 |
| M362–N14 | enr | **new** | 2.51 | 1.09e-06 | 2.94e-04 | 12 | 9 |
| M370–N39B | dep | **new** | 0.21 | 2.38e-06 | 5.96e-04 | 16 | 15 |
| M288–N14 | enr | **new** | 2.68 | 5.19e-06 | 1.19e-03 | 65 | 56 |
| M106–N39B | enr | **new** | 2.41 | 5.43e-06 | 1.19e-03 | 15 | 14 |
| M288–N08A | dep | **new** | 0.07 | 8.87e-06 | 1.83e-03 | 7 | 5 |
| M002–N01 | dep | **new** | 0.08 | 2.30e-05 | 4.27e-03 | 22 | 21 |
| M269–N01 | enr | **new** | 4.47 | 2.31e-05 | 4.27e-03 | 19 | 19 |
| M370–N24 | dep | **new** | 0.16 | 3.65e-05 | 6.40e-03 | 14 | 13 |
| M263–N39B | dep | **new** | 0.27 | 3.95e-05 | 6.58e-03 | 29 | 28 |
| M002–N30C | enr | **new** | 17.49 | 4.13e-05 | 6.58e-03 | 16 | 15 |
| M391–N14 | dep | **new** | 0.50 | 4.35e-05 | 6.63e-03 | 11 | 10 |
| M036–N01 | dep | **new** | 0.28 | 6.78e-05 | 9.91e-03 | 57 | 55 |
| M263–N24 | dep | **new** | 0.13 | 7.84e-05 | 1.10e-02 | 21 | 21 |
| **M288–N45** | enr | published | 13.57 | 9.70e-05 | **1.31e-02** | 16 | 15 |

Six of the published eight appear; M243–N39B (1.76e-4) and M297–N24 (1.07e-2) fall below
the 1e-4 line but are not refuted.

**The tautology check the 2026-09-04 session's `M036+1(N30D)` failure demands** was run
on all 26: for each pair, how many lines carrying the M-sign have the N-sign inside the
*entry* field, where it would be a graphical component rather than an accounting numeral.
The maximum anywhere in the table is **2** (M263–N01, M288–N14), and the parser excludes
pre-comma N-signs in any case, so no pair in the table is tautological. M288–N45 and
M288–N39B are at **0**: N45 never appears bound to M288.

**Also audited:** the M288 family merge (2026-09-17 recommended experiment 3). Of 559
M288 occurrences, **538 are plain `M288`**; no variant reaches 20 lines (`M288~I` 6,
`M288~D` 4, `M288~F` 3, then singletons). The family merge is vacuous for M288, so the
confirmation is not a merge artefact. M263 remains unaudited.

## Priority check

Required by the stream B brief before any novelty language. Enumerated via Crossref
(`query.bibliographic`, from 2022) and cross-checked against OpenAlex; both indexes
return identical author lists and metadata. Two items postdate this folder's last
session and neither was known to it:

- **Monroe, M. Willis; Kelley, Kathryn; Born, Logan; Sarkar, Anoop**, "Recent Progress in
  Deciphering Proto-Elamite", *Near Eastern Archaeology* **88**(4), 314–323, December
  2025. [10.1086/738240](https://doi.org/10.1086/738240). Four authors — the Born et al.
  2022 team the handover's experiment 5 names. **Closed access, no OA copy in any
  repository indexed by OpenAlex; unread.**
- **Kelley, Kathryn**, *Proto-Elamite*, Cambridge Elements, 18 July 2026.
  [10.1017/9781009614559](https://doi.org/10.1017/9781009614559). Abstract verified;
  full text unread.

**No novelty is claimed against the specialist literature.** "New" in the table above
means new *relative to this folder's own constraint set*. The folder's standing
conditional assumption — novelty against sign-by-sign scholarship is unestablished —
stands unchanged, and these two items are now the concrete way to discharge it.

## Conditional assumptions

- Everything is structural. No sign is given a semantic, phonetic or metrological value.
- The corpus is 1,334/1,467 MDP (Susa); nothing here speaks to other provenances.
- The expanded table's validity rests on the claim that restriction to powered pairs and
  to informative blocks is ancillary. That claim is argued analytically, verified by
  simulation at the split level (0/16,000), and priced at the sweep level (500-rep
  permutation null). It would fail if some selection step used an *overlap* rather than a
  marginal; none does, and `src/test_blocks.py` pins the property in a unit test.
- The 20 new pairs have had the tautology, replicate-count and search-budget checks and
  nothing else. They are candidate constraints at the same tier the published eight
  occupied on 2026-09-04, not load-bearing results.

## Files

```
PREDICTIONS.md                     frozen before any new p-value
src/blocks.py                      shared machinery; reuses the audited parser verbatim
src/validate_pipeline.py           reproduces 2026-09-17 power_floor.json, all 16 cells
src/finer_blocks.py                column/entry parser, asserted against the audited one
src/block_aware_split.py           recommended experiment 1, all eight pairs   [P1-P3]
src/calibration.py                 2,000-rep within-block null per pair        [P4]
src/level_of_analysis.py           face-level test, occupancy, M288 form audit [P5, E6]
src/block_ladder.py                tablet -> face -> column -> entry
src/search_budget.py               corpus-wide 1,430-pair face-blocked sweep
src/sweep_null.py                  500-rep permutation null for the sweep
src/constraint_table.py            the 26-pair table with every attack column
src/test_blocks.py                 12 unit tests, all passing
results/*.json, results/constraint_table.csv, results/search_budget_powered.csv
```

Every script takes the corpus directory as `argv[1]`; clone the pinned commit and run.
