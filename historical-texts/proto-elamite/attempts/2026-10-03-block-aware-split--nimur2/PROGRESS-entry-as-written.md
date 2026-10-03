# PROGRESS.md entry as written by session nimur2 (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.

## 2026-10-03 – block-aware split settles M288–N45; a co-numeral control re-tiers the set (advancing)

**Session:** Claude Opus 5 Breaker, scheduled, stream B draw. Mode: advancing.
**Full write-up, code and machine-readable output:**
`attempts/2026-10-03-block-aware-split/` — start with `RESULTS.md`.
**Predictions frozen and committed before the tests they govern:** `PREDICTIONS.md`
there, in `22afaaf` (P1–P5) and `e0deb4d` (P6–P7).

### What was attempted

The drawn next move — the 2026-09-17 handover's experiment 1, settling M288–N45 with a
block-aware split — and then two follow-ups that the first one's by-products forced.

### Reproduction first

The 2026-09-17 power-floor table comes back identical on a fresh clone at the pinned
commit, M288–N45 included (face-blocked p = 0.4700, floor 0.1200, 4 informative blocks
of 290). All 14 unit tests in the previous attempt pass. The LF digest is `8849716c…`
as that session recorded; the CRLF trap did not bite.

### What worked

**1. The drawn experiment succeeds, and M288–N45 is confirmed against the face
confound.** The pre-registered marginal-only split puts 10 informative `(tablet, face)`
blocks in validation: face-blocked p = **0.001295**, p-floor 6.7×10⁻⁵, OR 21.83, overlap
12 of 13, and the pair re-screens on the complement at q = 2.7×10⁻²⁰. Rather than trust
one split — `PREDICTIONS.md` records that per-block overlaps were visible to me first,
so this is a valid conditional test but **not** a prospective holdout — all **7,947**
admissible splits were enumerated: median p = 8.9×10⁻⁴, **98.5 %** reach p ≤ 0.05, and
every one has power. The label-permutation null puts the chosen split at **percentile
39.4**, so the split is not load-bearing. The pair is no longer "untestable at holdout
scale".

**2. The handover's "≥ 10 blocks" spec turns out to be satisfiable at exactly one
value.** The corpus holds only **16** informative blocks for this pair over 15 tablets,
a hard ceiling at any split. Enumerating the frontier: at 10 validation blocks the
training complement retains a p-floor of 0.036; at 11 it rises to 0.072 and the
complement can no longer return a significant blocked result. Ten was the ceiling, not a
round number.

**3. Prior selection does not contaminate the blocked test, and that is now measured
rather than argued.** Seven of the nine validation tablets are in the 2026-09-04
training buckets. Two nulls at 20,000 draws each: permuting N45 within `(tablet, face)`
leaves the test calibrated (P(p ≤ 0.05) = 0.0475) and provably leaves the split
invariant; permuting within tablet, which hands N45 the face-confound freedom, leaves it
conservative (0.0086). Conditioning on selection shifts the p-value distribution by
nothing at all — see below for why.

### What failed, and what that cost the folder

**4. P6 refuted: the published training screen is non-specific, but only for some
signs.** I predicted all eight pairs; it is not all eight. The unblocked Fisher screen
the 2026-09-04 design selects on fires at p ≤ 7×10⁻⁶ in **20,000 of 20,000** draws of a
null with no within-face association at all — it reads tablet/face co-location. Checked
for a frozen-table bug: train cell `a` varies 38–45 while p stays at 10⁻¹⁷–10⁻²⁴. Across
all eight pairs the effect is **monotone in the 2026-09-17 session's own per-sign face
effect**: for M297 (2.06× the mean between-sign signal) 71–83 % of the crude log-odds is
reproduced by co-location, for M288 (1.07×) 86 %, and for M263 (0.12×) essentially none.
So `train_q` in `analysis/results/associations.csv` is a **power filter, not evidence**,
for the face-concentrated signs M297/M288/M243 — and genuine evidence for M263/M106.
P6b also refuted: direction does not predict it (M297–N01 is a depletion and fully
non-specific; M263–N30C is a depletion and fully specific).

**5. A control nobody had run removes four of the other seven constraints.** N45 is the
top-magnitude member of a series whose lower members are N01/N14/N34, and the corpus
reads that way: N45 lines carry 3.07 distinct N-signs against 1.32, N34 is 11.3× and N14
3.3× enriched, N01 *depleted*. M288 is also not the highest-N45-rate sign (M195 0.211,
M056 0.190 beat its 0.101) — it leads on its 557 lines, i.e. on power. So the live
alternative was that N45 marks a large quantity and M288 lines carry large quantities.
Stratifying on the exact set of **other** N-signs on the line and permuting the target
within stratum — no numeral assigned a value anywhere, the strata are the observed
co-occurring signs — the test is calibrated (P(p ≤ 0.05) = 0.026–0.045) and strata are
invariant by construction. BH-corrected over the eight pairs:

| pair | crude OR | stratified MH-OR | q | power | verdict |
|---|---:|---:|---:|:--:|---|
| M288–N45 | 13.57 | 7.50 | 1.3×10⁻¹³ | yes | survives |
| M297–N39B | 9.79 | 3.54 | 2.1×10⁻¹² | yes | survives |
| M106–N24 | 5.54 | 4.21 | 0.0027 | yes | survives |
| M297–N01 | 0.29 | 0.74 | 0.136 | yes | fails |
| M243–N39B | 6.47 | 1.57 | 0.380 | yes | fails |
| M263–N01 | 4.24 | 0.86 | 0.823 | yes | **fails — was load-bearing** |
| M297–N24 | 4.04 | **0.46, reverses** | 1.000 | yes | refuted |
| M263–N30C | 0.04 | — | 0.284 | **no**, floor 0.178 | unresolved |

The M297–N24 reversal is not a bug: within the strata holding most of M297's lines it is
*depleted* of N24 ({N39B}: 0.094 vs 0.243; {N01,N39B}: 0.136 vs 0.369; {N01,N14,N39B}:
0.000 vs 0.194). The crude enrichment is a Simpson reversal through the composition of
the numeral expression.

**Net effect on the 2026-09-17 tiering:** M297–N39B confirmed (and it alone survives the
*joint* face + co-numeral test, MH-OR 13.28, p = 0.0015); M288–N45 promoted from
untestable to load-bearing; M106–N24 promoted from lead; M263–N01 **demoted** from
load-bearing; M263–N30C unresolved; M297–N01, M297–N24 and M243–N39B refuted or
demoted. **P7a was confirmed qualitatively and refuted quantitatively** — I predicted
the stratified OR would fall below half the crude 13.57 and it fell only to 7.50.

**6. Independent replication is unavailable from here, with the reason now on record.**
`cdli-gh/data` HEAD is `d66b12b0` (2023-10-11) but its bulk ATF and catalogue are Git
LFS pointers the proxy refuses. The newest non-LFS blob is the 2021-10-21 export, whose
1,452 catalogue-identified Proto-Elamite texts are a **strict subset** of the pinned
SFU 1,467 — 1,452 in both, 15 SFU-only, **0 new**. And `sfu-natlang/pe-sign-value-data`
has exactly two commits: the pinned `538949cc` **is** HEAD. So handover item 4 is
evidence-blocked, not merely unrun. A Sonnet researcher located the files; every count,
the ID intersection and the HEAD claim were re-run by me before being recorded.

### Changed / Evidence / Still conditional / Next

- **Changed.** M288–N45: untestable → confirmed. M263–N01: load-bearing → demoted.
  M106–N24: lead → load-bearing. M297–N24: refuted. `train_q` reinterpreted as a power
  filter for the face-concentrated signs.
- **Evidence.** Pinned SFU corpus only, LF digest `8849716c…`; plus an ID-level
  comparison against the 2021-10-21 CDLI bulk export.
- **Still conditional.** Everything remains structural; no sign has a semantic,
  phonetic or metrological value. The co-numeral control conditions on something not
  causally prior to the target, so it licenses a prediction claim and not a causal one.
  M263–N30C is unresolved for want of power, not refuted.
- **Next.** See HANDOVER.md — the joint face + co-numeral test on M106–N24 and
  M263–N01, which is written and has power, is the first item.

### Receipt

Starting revision `0703725`. Model/platform: Claude Opus 5, Claude Code remote (Linux).
Tool limits: proxy blocks Git LFS, so the Aug-2022 CDLI export is unreachable; no
archival or paywalled access needed or used. Material user steering: none — scheduled
firing, work taken from `npm run draw`. Trial ID: none. Costs unknown.

### Verification

- `python3 -m unittest test_face_and_form` (previous attempt) — 14/14 pass.
- `python3 power_floor.py` reproduces the 2026-09-17 table exactly, M288–N45 included.
- Every new test ships its own calibration null; no p-value in this entry is reported
  without one (`results/calibration.json`, `results/magnitude_calib.json`).
- The 20,000/20,000 selection rate was checked against a frozen-table bug by printing
  the train cell distribution (a ∈ [38, 45], observed 44).

---

