# M288–N45 settled, and a confound that re-tiers half the constraint set

**Session:** 2026-10-01, Claude Opus 5 Breaker (advancing). Drawn: stream B, pick
`historical-texts/proto-elamite` (idle 7.7d, debt 10.8).
**Corpus:** SFU `pe-sign-value-data` @ [`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6),
LF digest `8849716c6afbf963e5ee02535da013c87c931c61e88e2c05ced9cd58bf2b2dcf` — verified
this session, identical to the 2026-09-17 record.
**Predictions frozen before any result file:** [`PREDICTIONS.md`](PREDICTIONS.md),
committed in `9f35608`.
**Code:** `block_aware_split.py`, `placebo_stratification.py`; 15 unit tests in
`test_block_aware_split.py`, two of which pin this attempt's statistics to the
2026-09-17 published p-values and floors.

---

## Result in one sentence

M288–N45 is **confirmed, not merely untestable**: on a split that keeps all 16 of the
corpus's informative face-blocks it passes the face-blocked exact test at p = 9.7×10⁻⁵
against a floor of 4.5×10⁻⁹, screened blind on 1,109 disjoint tablets — but the same
session found a confound the folder had never tested, numeral richness, and it destroys
**four of the eight** published constraints including one of the three the 2026-09-17
session called load-bearing, while M288–N45 survives it.

---

## 0. Reproduction first

The 2026-09-04 pipeline was re-run on a fresh clone at the pinned commit. All fifteen
result rows are identical to `analysis/results/associations.csv` — every contingency
cell, odds ratio and q-value, with no material mismatch at a 1e-12 relative tolerance.
Corpus audit matches exactly: 1,467 files, 10 without numbered lines, 1,457 tablets,
11,013 lines, 4,869 eligible, 3,819 train / 1,050 validation. The 2026-09-17 power-floor
table also reproduces exactly, including the entry this session exists to resolve:
M288–N45 face-blocked p = 0.4700, floor = 0.1200, 4 informative blocks of 290.

Both prior sessions' numbers stand. Nothing below corrects a computation; §4 corrects an
*interpretation*, and says so plainly.

## 1. The 2026-09-17 handover's recommended experiment 1

### What the problem actually was

The handover proposed modifying the tablet-level split so validation is guaranteed ≥10
informative `(tablet, face)` blocks. Enumerating the blocks first showed why that works,
and showed that the framing "modify the split" understates the fix.

A `(tablet, face)` block is **informative** for a pair when the hypergeometric support
for its overlap is non-degenerate — `min(s,t) > max(0, s−(total−t))`. The corpus contains
**52** face-blocks where M288 and N45 are both present and only **16** that are
informative: one with 4 degrees of freedom, two with 2, and thirteen with 1. The other 36
are saturated — a face whose every eligible line carries both signs has no freedom to
vary, so it contributes a point mass and no information.

Those 16 informative blocks sit on 15 tablets. The 2026-09-04 hash split sent 4 of them
to bucket 0 and the other 12 into training. **That is the whole of the problem.** A
blocked exact p-value is a function of the informative blocks alone, because degenerate
blocks convolve in a point mass that shifts the observed total and the null distribution
by the same amount. So the fix is not a cleverer split: it is to stop discarding
informative blocks, and to move the honesty burden onto the screening set instead.

### The donor split

A tablet is a **donor** for a pair when it carries at least one informative block.
Validation = the donor tablets; screening = every other tablet; disjoint by tablet, as in
2026-09-04.

Selecting blocks on informativeness is legitimate, and the reason is the load-bearing
step of the design: the exact test already conditions on each block's marginals, and
within-block permutation of the target preserves `(total, s, t)` in every block exactly.
**Donor status is therefore invariant under the null's own randomization group** — the
null cannot move a block into or out of the donor set. §2 checks that numerically rather
than taking it on trust.

### Result — prediction A1 confirmed

| | 2026-09-04 bucket-0 holdout | donor split |
|---|---:|---:|
| validation lines | 1,050 | 98 |
| face-blocks | 290 | 21 |
| **informative blocks** | **4** | **16** |
| **p-floor** | **0.1200** | **4.46×10⁻⁹** |
| observed / max overlap | 15 / 16 | 19 / 22 |
| **face-blocked p** | **0.4700** | **9.70×10⁻⁵** |

Screening on the 1,109 complement tablets (4,771 lines, 1,417 pairs screened) selects
M288–N45 at OR 10.39, Fisher p = 6.4×10⁻¹⁹, BH q = 1.1×10⁻¹⁶ — so **prediction A4 holds**
and the validation tests a candidate chosen without reference to the validation tablets.
The pair was independently pre-registered as prediction 2 of the 2026-09-04 handover.

**A1 predicted p ≤ 0.001 and was explicitly labelled NOT BLIND** — the enumeration that
established the split's feasibility also printed the overlaps. What carries the result is
not blindness but the three things that are checkable: the pair was pre-registered, the
split rule is marginals-only and provably null-invariant, and the floor is computed.

### The same pair under both confounds at once

Blocking on `(tablet, face, other-N-count)` — §3 — leaves 6 informative blocks at a floor
of 3.97×10⁻⁴, and M288–N45 still passes at **p = 1.10×10⁻²**, screened blind on the
complement at OR 12.38, q = 2.3×10⁻²². **Prediction B1 confirmed.**

**The 2026-09-17 verdict "neither confirmed nor refuted" is now resolved in favour of
confirmed.** M288 and N45 do share a face preference and a numeral-richness preference,
and neither, nor both together, accounts for their co-occurrence.

## 2. Is the donor-split test calibrated? — the null model

The selection rule is the thing most likely to be wrong, so it was tested directly.
Each replicate permutes the target within every block corpus-wide — destroying any
within-block association while preserving all block marginals — then **re-derives the
donor set on the permuted data** and re-runs the test. 2,000 replicates per scheme.

| | `tablet+face` | `tablet+face+richness` |
|---|---:|---:|
| donor set invariant (50 full-corpus checks) | **yes, 50/50** | **yes, 50/50** |
| P(p ≤ 0.05) | 0.0175 | 0.0105 |
| P(p ≤ 0.01) | 0.0035 | 0.0010 |
| P(p ≤ 0.001) | 0.00050 | 0.0010 |
| median p | 0.625 | 0.688 |

The invariance argument holds exactly, on every check. The test is **conservative**:
nominal 0.05 fires at 1.1–1.8% and nominal 0.001 at 0.05–0.1%.

**Prediction A2 is refuted, in the conservative direction.** I predicted
P(p ≤ 0.05) ∈ [0.03, 0.07]; it is 0.0175 and 0.0105. The P(p ≤ 0.001) half of the
prediction was right (0.00050, predicted [0.0002, 0.003]). The miss is discreteness: with
16 blocks of 1–4 degrees of freedom the attainable p-values are coarse, so an exact test
cannot sit flush against a nominal level. I should have predicted conservatism and did
not. The consequence for the inference is that §1's p-values **understate** the evidence —
under the richness blocking the null reaches p ≤ 0.01 in 0.1% of replicates against an
observed 0.011, and its smallest attainable p, 3.97×10⁻⁴, is the floor itself.

## 3. The numeral-richness confound — new, and larger than the face confound

The design has controlled tablet (2026-09-04) and face (2026-09-17). It has never
controlled **how numeral-rich a line is**, and the skew is bigger than the face skew that
occupied the previous session. Counting only N-signs *other than the target*, so the
stratification is not circular:

| | mean other-N-signs per line |
|---|---:|
| all eligible lines (4,869) | 1.335 |
| M288 lines (557) | 1.738 |
| **N45 lines (91)** | **2.066** |
| non-N45 lines (4,778) | 1.321 |

N45 is a rich-line sign: 2.07 other numerals per line against 1.32 for lines without it.
M288 is a rich-line sign too. Two signs that both prefer numeral-rich lines will co-occur
more often than a richness-blind null expects, with no specific relation between them —
the same shape as the face confound, with a larger skew behind it. Excluding the target
from its own count is what keeps this from being circular, and is unit-tested.

Blocking on `(tablet, face, other-N-count)`, counts capped at 3 so strata stay populated,
leaves enough informative blocks for the test to fire on seven of the eight pairs.

## 4. The re-tiering — four of eight constraints do not survive

Full corpus, all four block schemes. `p / floor`; `*` marks a floor above 0.05, where the
test has no power and failure carries no information.

| pair | 2026-09-17 tier | `tablet` | `+face` | `+richness` | `+face+richness` | verdict |
|---|---|---:|---:|---:|---:|---|
| **M297–N39B** | load-bearing | 0.0000 | 0.0000 | 0.0000 / 9.3e-23 | **0.0000** / 7.0e-18 | **survives everything** |
| **M106–N24** | lead | 0.0000 | 0.0000 | 0.0000 / 1.3e-13 | **0.0000** / 2.7e-13 | **survives everything** |
| **M263–N30C** | load-bearing | 0.0000 | 0.0000 | 0.0008 / 8.0e-04 | **0.0017** / 1.7e-03 | **survives** |
| **M288–N45** | untestable | 0.0000 | 0.0001 | 0.0000 / 5.5e-08 | **0.0110** / 4.0e-04 | **survives** |
| M297–N24 | lead | 0.0000 | 0.0107 | 0.1915 / 4.0e-19 | **0.2959** / 1.4e-14 | **richness explains it** |
| M297–N01 | lead | 0.0000 | 0.0000 | 0.5185 / 9.2e-08 | **0.5602** / 2.0e-05 | **richness explains it** |
| **M263–N01** | **load-bearing** | 0.0000 | 0.0000 | 0.5684 / 1.5e-04 | **0.4696** / 8.7e-04 | **richness explains it** |
| M243–N39B | barely testable | 0.0000 | 0.0002 | 0.5648 / 3.7e-02 | 0.5926 / 1.5e-01 `*` | **richness explains it** (on `+richness`, which has power) |

Every one of the four failures happens with the power to have confirmed: the floors are
4.0e-19, 9.2e-8, 8.7e-4 and 3.7e-2. These are refusals, not absences of power — which is
exactly the distinction the 2026-09-17 session had to establish for M288–N45, now
cutting the other way.

### The mechanism, and why both N01 constraints fall together

| pair | other-N on M-lines | on target lines | corpus | reading |
|---|---:|---:|---:|---|
| M297–N39B | 1.198 | 1.190 | 1.227 | no skew either side → survives |
| M263–N01 | **0.131** | 0.377 | 0.618 | both numeral-poor → spurious **enrichment** |
| M297–N01 | **1.270** | 0.377 | 0.618 | rich vs poor → spurious **depletion** |
| M297–N24 | 1.560 | 1.702 | 1.298 | both rich → spurious enrichment |
| M288–N45 | 1.738 | 2.066 | 1.335 | both rich, **and survives anyway** |

(The corpus column differs by row because the target is excluded from its own count; for
an N01 pair, removing N01 drops the corpus mean to 0.618.)

**N01 is the sign of numeral-poor lines** — 0.377 other numerals per line against 0.618
corpus-wide — which is unsurprising for the commonest N-sign in a corpus where 3,650 of
4,869 eligible lines carry exactly one numeral. So any M-sign's richness skew generates an
apparent N01 association, in whichever direction that skew runs. M263 lines are extremely
numeral-poor (0.131) and produced a spurious *enrichment*; M297 lines are rich (1.270) and
produced a spurious *depletion*. **Both N01 constraints, pointing in opposite directions,
are the same single artefact**, and once richness is blocked neither leaves a residual
(p = 0.47 and p = 0.56).

**Prediction B2 confirmed in substance, with one error of mine.** I predicted at least one
load-bearing pair would fail and named M297–N01 as the likeliest failure, reasoning in
advance that N01 would turn out to be the numeral-poor-line sign. The reasoning is
confirmed directly by the table. But M297–N01 was a *lead* in the 2026-09-17 tiering, not
load-bearing — I mis-stated its tier in the frozen file. The load-bearing casualty is
**M263–N01**. **B3 confirmed:** M297–N39B survives, and its richness profile is flat, which
is why. **B4 refuted:** I predicted ≥2 pairs would lose power entirely under the combined
blocking; only M243–N39B did.

### What "richness explains it" does and does not mean

It is a claim about information, not about the scribes. If M263 denotes something whose
accounting intrinsically uses a single numeral, then richness is a *mediator* of a real
relation and conditioning on it removes a real effect. That objection is sound and cannot
be settled from distributions alone. What the table does establish is the weaker, solid
statement: **"M263 is enriched with N01" conveys nothing beyond "M263 occurs on
numeral-poor lines."** There is no residual association once the generic line property is
held fixed. A constraint that survives only as a restatement of a line's numeral count is
not a constraint on a sign pair, and should not be cited as one.

### The placebo control — richness, or just finer blocking?

A floor below 0.05 establishes formally that a failing test had the power to confirm, but
it is an extreme bound and a reader may reasonably want the concrete version. So: within
each `(tablet, face)` block, shuffle the lines' richness-stratum labels among the lines.
Block sizes are preserved exactly, so the fragmentation is identical; only the association
between block membership and numeral richness is destroyed. 500 replicates.

| pair | real p | placebo median p | placebo 5–95% | placebo P(p ≤ .05) | real / placebo informative blocks | reading |
|---|---:|---:|---:|---:|---:|---|
| M297–N39B | 0.0000 | 0.0000 | 0.0000–0.0000 | 1.000 | 28 / 49.0 | survives; placebo cannot discriminate |
| M106–N24 | 0.0000 | 0.0000 | 0.0000–0.0000 | 1.000 | 13 / 12.3 | survives |
| M263–N30C | 0.0017 | 0.0000 | 0.0000–0.0000 | 1.000 | 11 / 23.0 | survives |
| **M288–N45** | **0.0110** | **0.0148** | 0.0017–0.0946 | 0.870 | 6 / 8.1 | **survives; real blocking costs it less than the placebo does** |
| M297–N24 | 0.2959 | 0.0199 | 0.0033–0.0855 | 0.844 | 18 / 28.6 | **richness kills it** |
| M297–N01 | 0.5602 | 0.0000 | 0.0000–0.0002 | 1.000 | 13 / 47.9 | **richness kills it** |
| M263–N01 | 0.4696 | 0.0000 | 0.0000–0.0000 | 1.000 | 8 / 46.2 | **richness kills it** |
| M243–N39B | 0.5926 | 0.0006 | 0.0002–0.0033 | 0.998 | 3 / 6.5 | no power under *this* scheme; killed under `+richness`, which has power |

The three refusals that matter are unambiguous: with block sizes held fixed and only the
richness content of the blocks destroyed, each failing pair comes back significant in
84–100% of replicates. Their deaths are caused by numeral richness specifically, not by
finer blocking.

Two honest riders. First, the placebo carries **more** informative blocks than the real
stratification for the failing pairs (47.9 against 13 for M297–N01, 46.2 against 8 for
M263–N01) — the real strata align with the signs' own distributions, which is itself the
confound's signature; the computed floor, not the placebo, is what certifies the real test
could still have fired, and it does (2.0e-05 and 8.7e-04). Second, for the three strongest
survivors the placebo is significant too, so it cannot discriminate for them; it earns its
keep on the failures and on M288–N45, whose real p of 0.0110 is *better* than the
power-matched placebo median of 0.0148.

## 5. Did the split buy the result for free? — prediction A3

The 2026-09-23 cross-reference requires a label permutation before interpreting any
post-hoc split. **In its literal form that test is degenerate here, and the reason is
worth recording:** donor status is fixed by the block marginals rather than chosen, so
permuting the donor label across tablets produces sets containing no informative blocks,
where the test has no power and returns p ≈ 1 by construction. A null that cannot fail is
not a null.

The question the cross-reference actually asks — did the split buy the difference for
free? — is answered by running the identical procedure at full search budget over every
pair the corpus offers. Of 997 eligible pairs, **506 have power** under the face-blocked
donor split, and M288–N45 at p = 9.70×10⁻⁵ is **21st (4.0%)**. Its BH q against the whole
507-pair powered budget is **2.34×10⁻³**. So even had the pair been discovered by an
exhaustive donor-split search rather than pre-registered and screened, it would survive
correction at that search budget. **A3 is satisfied in substance.**

The 22.9% of powered pairs reaching p ≤ 0.05 is *not* evidence of miscalibration — these
are real pairs in a real administrative corpus, many genuinely associated, and §2's null
model is what speaks to calibration. It does say the corpus is dense with structure.

## 6. Where the donor split works, and where it must not be used

A useful limit emerged. For a pair with many donor tablets, pulling them all into
validation strips the association out of the complement and the blind screen then fails:

| pair | donor tablets | full-corpus OR | complement OR | screens blind? |
|---|---:|---:|---:|---|
| M288–N45 | 15 | 13.57 | 10.39 | **yes**, q = 1.1e-16 |
| M376–N08A | 12 | 98.82 | 15.91 | no |
| M288–N24 | 41 | 4.07 | 1.57 | no |
| M288–N39B | 67 | 3.60 | 1.63 | no |

So the donor split is the right instrument for exactly the class the fixed-hash holdout
fails on — **sparse pairs, whose informative blocks are few enough that a random split
destroys them** — and the wrong instrument for dense pairs, where a plain holdout already
has power and the donor set would eat the screening set. The two designs are
complementary, not ranked.

## 7. Leads: the published eight are not the corpus's strongest structure

Running the donor-split procedure under the full `(tablet, face, other-N-count)` blocking
over all 824 eligible pairs — 296 with power — gives 14 at BH q ≤ 0.05. The top of that
list is far stronger than anything in the published set:

| pair | direction | p | BH q | informative blocks |
|---|---|---:|---:|---:|
| **M288–N39B** | enriched | 5.17e-19 | 1.53e-16 | 34 |
| **M288–N24** | enriched | 2.01e-13 | 2.98e-11 | 21 |
| M106–N30C | enriched | 9.74e-07 | 7.54e-05 | 4 |
| M106–N24 | enriched | 1.02e-06 | 7.54e-05 | 13 |
| M370–N39B | depleted | 3.57e-05 | 2.10e-03 | 10 |
| M297–N39B | enriched | 4.58e-05 | 2.10e-03 | 28 |
| M376–N08A | enriched | 4.96e-05 | 2.10e-03 | 7 |
| M288–N14 | enriched | 1.00e-04 | 3.11e-03 | 44 |
| M106–N39B | enriched | 1.04e-04 | 3.11e-03 | 14 |
| M362–N14 | enriched | 1.05e-04 | 3.11e-03 | 9 |
| M218–N24 | depleted | 2.07e-04 | 5.57e-03 | 20 |
| M263–N30C | depleted | 1.69e-03 | 4.17e-02 | 11 |
| M175–N24 | depleted | 2.08e-03 | 4.73e-02 | 9 |
| M106–N01 | depleted | 2.27e-03 | 4.81e-02 | 6 |

**These are search results under BH correction, not held-out confirmations** — per §6 their
donor splits do not screen blind, so the honest warrant is the corrected search, and that
is how they are offered. M288 carries a whole numeral profile (N39B, N24, N14 enriched;
N45 enriched; N08A's apparent depletion collapses under richness blocking to 1 informative
block and a floor of 0.86, so it is untestable rather than real). M106 appears four times.
Nothing here assigns any sign a value.

## 8. What this session did not establish

- **No semantic, phonetic or metrological value for any sign.** Everything is structural
  association, as in 2026-09-04 and 2026-09-17.
- Novelty against specialist sign-by-sign literature remains unestablished. Untested here.
- §7's pairs are corrected search results, not replications; §6 says why they cannot be
  donor-split-screened and what would be needed instead.
- The richness control cannot distinguish a confound from a mediator (§4). The defensible
  claim is about information content, and is stated as such.
- Replication on an independent CDLI export is still unrun. It is now the strongest
  outstanding falsification test, and the predictions must be stated per the **new**
  tiering, not the 2026-09-17 one.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
echo /abs/path/to/pe-sign-value-data/corpus \
  > ../2026-09-17-exact-form-and-face/corpus_path.txt
python3 -m unittest -v test_block_aware_split   # 15 tests, all must pass
python3 block_aware_split.py --replicates 2000
python3 placebo_stratification.py --replicates 500
```

No third-party packages. `corpus_path.txt` is the only machine-specific input and is
deliberately not committed.
