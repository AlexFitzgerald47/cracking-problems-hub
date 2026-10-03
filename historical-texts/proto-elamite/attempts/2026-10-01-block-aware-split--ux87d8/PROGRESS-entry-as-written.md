# PROGRESS.md entry as written by session ux87d8 (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.


---

## 2026-10-01 — breaker session: the block-aware split, and the numeral-richness confound

**Session:** Claude Opus 5 Breaker (advancing). Work drawn, not chosen: `npm run draw`
gave stream B and the pick `historical-texts/proto-elamite` (working, idle 7.7d, debt
10.8). Took the pick and its first recommended experiment. Trial ID: none.
**Starting revision:** `f734a3f`. **Corpus:** SFU `pe-sign-value-data` @ `538949cc`, LF
digest `8849716c…bf2b2dcf` — recomputed and identical to the 2026-09-17 record, so the
pin is sound and the CRLF trap in the handover is confirmed as a line-ending artefact,
not drift.
**Full write-up:** `attempts/2026-10-01-block-aware-split/RESULTS.md`. Predictions frozen
in `9f35608` before any result file.

### Changed

M288–N45 is settled: **confirmed**, not merely untestable. And four of the eight
published constraints — including one the 2026-09-17 session called load-bearing — are
explained by a confound no prior session tested.

### Reproduced first

The 2026-09-04 pipeline re-ran with all fifteen rows identical (no material mismatch at
1e-12 relative tolerance) and every corpus audit figure matching. The 2026-09-17
power-floor table reproduced exactly, including M288–N45 face-blocked p = 0.4700, floor
0.1200, 4 informative blocks. Both prior sessions' computations stand; this session
corrects an interpretation, not an arithmetic.

### Evidence

**1. The recommended experiment, and why its framing understated the fix.** Enumerating
the blocks showed the corpus holds 52 face-blocks where M288 and N45 both appear and only
**16 informative** ones (1 with 4 d.f., 2 with 2, 13 with 1); the other 36 are saturated
and contribute a point mass. A blocked exact p-value is a function of the informative
blocks alone. The 2026-09-04 hash split sent 4 of the 16 to bucket 0 and 12 to training —
*that* is the whole of the power failure. So the fix is not a cleverer split but to stop
discarding informative blocks and move the honesty burden to the screening set.

**2. The donor split.** A tablet is a donor when it carries ≥1 informative block;
validation = donors, screening = the rest, disjoint by tablet. Informativeness depends
only on block marginals, which the exact test already conditions on, so **donor status is
invariant under the null's own randomization group** — verified on 50/50 full-corpus
permutation checks, in both block schemes.

| | 2026-09-04 bucket-0 | donor split |
|---|---:|---:|
| informative blocks | 4 of 290 | **16 of 21** |
| p-floor | 0.1200 | **4.46e-09** |
| face-blocked p | 0.4700 | **9.70e-05** |

Screened blind on the 1,109 complement tablets at OR 10.39, BH q = 1.1e-16, among 1,417
pairs. Under **both** confounds at once — `(tablet, face, other-N-count)` — it still
passes at p = 1.10e-02 against a floor of 3.97e-04, screened at OR 12.38, q = 2.3e-22.
The 2026-09-17 "neither confirmed nor refuted" resolves to **confirmed**.

**3. The numeral-richness confound, new this session and larger than the face confound.**
Counting N-signs other than the target, so the stratification is not circular: N45 lines
carry 2.07 other numerals against 1.32 for lines without it; M288 lines 1.74 against 1.28.
Blocking on it re-tiers the set. Four pairs fail **with the power to have confirmed**
(floors 4.0e-19, 9.2e-08, 8.7e-04, 3.7e-02):

| survives all four block schemes | explained by richness |
|---|---|
| M297–N39B, M106–N24, M263–N30C, **M288–N45** | M297–N24, M297–N01, **M263–N01** (was load-bearing), M243–N39B |

The mechanism is single and clean: **N01 is the numeral-poor-line sign** (0.377 other
numerals against 0.618 corpus-wide), unsurprising for the commonest N-sign where 3,650 of
4,869 eligible lines carry exactly one numeral. M263 lines are numeral-poor (0.131) and
produced a spurious *enrichment*; M297 lines are rich (1.270) and produced a spurious
*depletion*. **Both N01 constraints, pointing in opposite directions, are the same
artefact**, and neither leaves a residual once richness is held fixed (p = 0.47, 0.56).

**4. Null models, run before believing any of it.** (a) *Calibration*: 2,000 replicates
permuting the target within every block, re-deriving the donor set each time. The test is
**conservative** — nominal 0.05 fires at 1.1–1.8%, nominal 0.001 at 0.05–0.1% — so §1's
p-values understate the evidence. (b) *Placebo stratification*: shuffling richness labels
within each `(tablet, face)` block preserves block sizes exactly and destroys only the
richness content. Each failing pair comes back significant in 84–100% of 500 replicates,
so the deaths are caused by richness specifically and not by finer blocking. M288–N45's
real p of 0.0110 is *better* than its power-matched placebo median of 0.0148.
(c) *Search budget*: the literal label permutation the 2026-09-23 cross-reference asks
for is **degenerate here** — donor status is marginals-determined, so a permuted label
yields sets with no informative blocks and p ≈ 1 by construction. Substituted the full
budget: of 997 pairs, 506 have power, and M288–N45 ranks 21st (4.0%) with BH
q = 2.34e-03 against the whole powered budget.

**5. A limit on the new design.** The donor split screens blind only for **sparse** pairs.
With 67 donor tablets, M288–N39B's complement OR falls from 3.60 to 1.63 and the blind
screen fails; with 15 donors, M288–N45's holds at 10.39. The donor split is the right
instrument for exactly the pairs a fixed-hash holdout destroys, and the wrong one for
dense pairs. Complementary, not ranked.

**6. Leads.** Under the full blocking across all 824 eligible pairs (296 powered), 14 hold
BH q ≤ 0.05, led by **M288–N39B** (p = 5.17e-19, q = 1.53e-16, 34 informative blocks) and
**M288–N24** (p = 2.01e-13, q = 2.98e-11). These are corrected search results, not
held-out confirmations — per item 5 their donor splits cannot screen blind, and that is
how they are offered.

### Still conditional

- Everything remains **structural**. No sign is assigned a semantic, phonetic or
  metrological value, and nothing here moves toward one.
- **The richness control cannot distinguish a confound from a mediator.** If M263 denotes
  something whose accounting intrinsically uses one numeral, conditioning on richness
  removes a real effect. The defensible claim is about information content: "M263 is
  enriched with N01" conveys nothing beyond "M263 occurs on numeral-poor lines."
- Novelty against specialist sign-by-sign literature is still unestablished, as in both
  prior sessions. Untested here.
- §7's leads are search results under correction, not replications.

### Predictions, scored honestly

Frozen in `9f35608`, each labelled BLIND or NOT BLIND individually.

- **A1 confirmed** (NOT BLIND, and labelled so in advance — the feasibility enumeration
  printed the overlaps): predicted p ≤ 0.001, got 9.70e-05.
- **A2 refuted, in the conservative direction.** Predicted P(p ≤ .05) ∈ [0.03, 0.07]; it
  is 0.0175 and 0.0105. The P(p ≤ .001) half was right. The miss is discreteness — with
  blocks of 1–4 d.f. an exact test cannot sit flush against a nominal level. I should have
  predicted conservatism. It makes the reported evidence understated, not overstated.
- **A3 satisfied in substance**, by the search-budget substitute; the literal form is
  degenerate and that is recorded rather than glossed.
- **A4 confirmed.** **B1 confirmed.** **B3 confirmed.**
- **B2 confirmed in substance, with an error of mine.** I predicted a load-bearing pair
  would fail and named M297–N01 as likeliest, reasoning in advance that N01 would prove to
  be the numeral-poor-line sign — which the data confirm directly. But M297–N01 was a
  *lead* in the 2026-09-17 tiering, not load-bearing; I mis-stated its tier in the frozen
  file. The load-bearing casualty is **M263–N01**.
- **B4 refuted.** Predicted ≥2 pairs would lose power entirely under the combined
  blocking; only M243–N39B did.

### Receipt

Model/platform: Claude Opus 5, Claude Code on the web (Linux container). Tool limits: no
third-party Python packages; corpus cloned fresh at the pinned commit. Material user
steering: none — scheduled Breaker firing, work taken from `npm run draw`. Trial ID: none.
Costs unknown. Artifacts: `attempts/2026-10-01-block-aware-split/` — `RESULTS.md`,
`PREDICTIONS.md`, `block_aware_split.py`, `placebo_stratification.py`,
`test_block_aware_split.py` (15 tests, 2 pinning this attempt to the 2026-09-17 published
p-values and floors), and `results/{block_aware_split,extension,placebo}.json`.
