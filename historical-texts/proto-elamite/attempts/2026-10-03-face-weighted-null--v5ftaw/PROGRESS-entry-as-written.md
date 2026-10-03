# PROGRESS.md entry as written by session v5ftaw (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.

## 2026-10-03 – M288–N45 settled; the blocking scheme was the power failure (advancing)

**Session:** Claude Opus 5 breaker, scheduled, stream B draw (pick: highest coverage debt).
Mode: advancing.
**Full write-up, code and machine-readable output:**
`attempts/2026-10-03-face-weighted-null/` — start with `RESULTS.md`.
**Predictions frozen and committed (`10b08a6`) before any result file existed:**
`attempts/2026-10-03-face-weighted-null/PREDICTIONS.md`.

### What was attempted

The 2026-09-17 handover's recommended experiment 1, as written — a block-aware split
guaranteeing ≥ 10 informative `(tablet, face)` blocks in validation, to settle M288–N45,
which that session left *untestable* (face-blocked p-floor 0.12) rather than refuted. Then
a second, independent instrument for the same question, after diagnosing why the first one
had failed.

### Reproduction first

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pinned commit. All
fifteen rows reproduce — every cell, odds ratio and q-value — with p-values differing only
in the ~16th decimal place. All corpus audit figures match exactly. The 2026-09-17
face-blocked results, including the 0.12 floor, also reproduce. The CRLF digest trap that
session recorded is real and still benign; the LF digest is `8849716c…8bf2b2dcf`.

The SFU mirror's remote `HEAD` is **still** the pinned commit `538949c`, so the long-standing
"replicate on a newer export" item cannot be served from this repository and needs CDLI
directly.

### What worked

**1. M288–N45 is confirmed.** The block-aware split works. Validation of 9 tablets / 69
lines / 10 informative blocks; the complement of 4,800 lines independently re-selects the
pair under the published screening rules (OR 11.98, q = 1.4e-20); the face-blocked exact
test on validation returns **p = 0.0032** with a p-floor of **2.4e-7**, against 0.12 before.
The split rule uses block marginals only — never an observed overlap — which is licit
because the exact conditional test conditions on exactly those marginals.

**2. Its type-I error was measured, not asserted.** Under a generator with no association
planted (real tablets, faces, line counts and M-sign assignments; each tablet's target count
preserved; face skew planted at the measured strength), the procedure rejects at **2.8%**
against a nominal 5%, and at 2.7–3.0% across three different pair geometries. Conservative,
not inflated.

**3. The 2026-09-17 power failure was the blocking scheme, not the corpus.** 615 of 1,426
faces carry a single eligible line, so blocking on face deletes those lines rather than
controlling them. For M288–N45, **38 of 56 co-occurrences sit in zero-freedom blocks, 27 of
them on single-line faces**, and 13 of the 16 informative blocks carry one degree of freedom.

**4. A second instrument that needs no split at all.** Re-deal the target within tablet as
2026-09-04 does, but weight a reverse line `w` times an obverse one, so the face confound is
carried at an assumed strength instead of conditioned away. Exact by convolution; **w = 1
reproduces the eight published p-values to 1e-12** (asserted by the test suite). Its p-floor
for M288–N45 on the same 1,050-line holdout is **7.9e-4**, ~150× better than the face-blocked
test on identical data. Reported as a curve, so the headline is the **critical weight**:
**seven of eight pairs survive a reverse-face preference of any strength out to w = 1024, and
M288–N45 needs one 8.8× stronger than the corpus has** (measured 1.83).

### What failed, and why those are the more useful findings

**P5 refuted — the face confound inflates the published test about twofold, not tenfold.** I
predicted w = 1 would reject at > 10% under a confound planted at its observed magnitude. On
the holdout it rejects at **0.3%**, because a face confound can act in **only 5 tablets**
there for this pair (7 of its 15 observed overlaps lie beyond the reach of any face confound
at any strength — a bound available from the marginals before any test). On the full corpus,
where there is enough channel to measure it, the rate at the **measured** strength is
**0.059** against the test's own no-confound baseline of 0.027 and a nominal 0.05; the
weighted test returns 0.026. So the confound is real and worth controlling — it reaches 0.327
at 4× the measured strength — and nowhere near large enough to have produced p = 0.0071. The
2026-09-17 session was right to test face and right that it was the uncontrolled confound;
the predicted magnitude was wrong. Rider found the same way: the weighted test is calibrated
only at the confound's true strength, so **under-specifying `w` inflates it too** (0.092 at a
planted 2×`w_hat`), which is the argument for reporting the critical weight rather than one p.

**P6 refuted — the confound has a sign, and for four pairs it is protective.** I predicted
M243–N39B would be the second most fragile pair. Its p *falls* with w (0.0025 → 0.0009), as
do M297–N01's and M263–N01's, and M106–N24's is non-monotone. Weighting the target towards
the reverse lowers the null's expected overlap whenever the M-sign leans obverse, which makes
the observed overlap *more* extreme. "Both members are reverse-skewed, so this may be a face
artefact" was the right worry for M288–N45 and the wrong worry for half the set.

**I2 refuted — I called the handover's item 1 a dead end and it is not.** I predicted it would
be feasible but unable to separate the pair from a decoy with the same block marginals.
Running it on 193 powered decoys rejects 22.3% at α = 0.05, which looks exactly like that
failure; the known-answer generator shows it is **power, not inflation**. The decoy count
alone could not distinguish the two in either direction.

**A measurement correction.** The 2026-09-17 write-up quotes N45 at 30.8% reverse against a
13.5% baseline, a 2.3× skew. Measured off lines that are *not* M288 — the quantity a null
needs — the odds ratio is **1.83**. Part of N45's apparent reverse skew is carried by the
M288 lines themselves, so estimating confound strength from the whole corpus overstates it.

Three of six prospective predictions failed. Scorecard in `RESULTS.md` §6.

### Lead opened, explicitly not a result

The block-aware split is a general power amplifier with verified calibration, so it can be
run across the whole candidate grid. On 193 powered decoy pairs, **24 survive BH at q ≤ 0.05**
against 5.4 expected false positives — strongest M288–N39B (p = 5.1e-27), M288–N24 (4.2e-17),
M376–N08A (4.5e-11). **This is an unfrozen, un-budgeted screen, not a confirmation.** What it
means is that the published constraint set of eight is **power-limited, not complete**. That
is now the folder's first recommended next experiment.

### Evidence receipt

- **Changed:** M288–N45 goes from *untestable at holdout scale* to **confirmed** (p = 0.0032
  out-of-sample, face-blocked, type-I error measured at 2.8%). Two instruments added, both
  validated against the published numbers. The face confound is quantified and shown
  to roughly double the published test's false-positive rate at its actual strength (0.059
  against a 0.027 baseline, nominal 0.05) rather than to explain the result, and shown
  protective for four of the eight pairs.
- **Evidence:** pinned SFU corpus at `538949c`, nothing new fetched. 4,869 eligible lines.
  `attempts/2026-10-03-face-weighted-null/results/*.json`, 10 unit tests.
- **Still conditional:** no semantic, phonetic or metrological value for any sign. The
  weighted null assumes one multiplicative face weight shared across tablets; a confound
  varying by tablet type or scribe is untested. Novelty against specialist sign-by-sign
  literature remains unestablished. Nothing about M288–N45 in this session was a blind
  holdout — I had enumerated its per-block overlaps while diagnosing the power failure, and
  `PREDICTIONS.md` marks the affected predictions *informed*.
- **Next:** confirm the 24-pair screen properly — freeze the grid and the budget first, then
  re-run the block-aware split with BH over the declared candidate space.

### Session provenance

Starting revision: `0703725`. Platform/model: Claude Opus 5, Claude Code cloud session,
Linux. Tool limits: no third-party Python packages used; GitHub reachable (SFU mirror cloned
at the pin). Material user steering: none — scheduled firing, work taken from `npm run draw`.
Trial ID: none. Cost/elapsed: unknown.

---

