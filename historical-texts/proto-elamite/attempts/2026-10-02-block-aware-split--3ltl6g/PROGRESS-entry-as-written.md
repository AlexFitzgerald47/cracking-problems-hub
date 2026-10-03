# PROGRESS.md entry as written by session 3ltl6g (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.

## 2026-10-02 – M288–N45 settled by a block-aware split; the constraint set re-counted (advancing)

**Session:** Claude Opus 5, Breaker seat, drawn (stream B, `npm run draw` pick: highest
coverage debt 11.9, idle 8.5d). Starting revision `72a635b`. Trial ID: none.
Attempt directory: `attempts/2026-10-02-block-aware-split/` — read its
[`RESULTS.md`](attempts/2026-10-02-block-aware-split/RESULTS.md) for the full argument.
Predictions frozen in `5307c3b` before any result file existed.

### What was attempted

Recommended experiment 1 of the 2026-09-17 handover, as written: settle M288–N45 with a
split guaranteeing the face-blocked test enough informative `(tablet, face)` blocks,
re-screening candidates on the complement. Then recommended experiment 3, the exact-form
audit of M263 and M288.

### Changed

- **M288–N45 moves from "untestable at holdout scale" to CONFIRMED against the face
  confound.** Arm A of a pre-registered block-aware split gives face-blocked p = 0.00385
  against a p-floor of **3.0e-7** (the published holdout's floor was 0.12), BH
  q = 0.0482 over that arm's own 50 re-screened candidates, validation OR 19.29, 9
  informative blocks, 24/27 overlap. The pair re-screens on the complement at training
  OR 11.11, q = 1.1e-14. This is the first test of the pair that could have gone either
  way, and it passed.
- **The 2026-09-17 face-blocked q-column is corrected (audit).** Its raw p-values all
  reproduce exactly, but its BH ran over the **8 pairs that had already survived** the
  2026-09-04 validation rather than the **54 candidates** that validation was applied to —
  and those 8 were selected using the same holdout the face-blocked test re-uses. On the
  design's own 54-candidate basis, **two** of eight survive (M263–N01 q = 0.0155,
  M297–N39B q = 0.0392), not seven. Nothing in that session's files is altered; its
  tiering conclusions came from the bucket rotation and mostly stand, but the "seven of
  eight survive face blocking" sentence does not.
- **Tier list re-counted** (RESULTS.md §2): load-bearing M263–N01, M297–N39B;
  confirmed-on-one-split M288–N45, M243–N39B; **power-limited and undecided** M263–N30C
  (floor 0.019) and M106–N24 (2 informative blocks) — M263–N30C leaves the load-bearing
  tier not refuted but with no verdict available; uncorrected-only M297–N01, M297–N24.
- **M263's family merge is upheld** (4 testable forms, all six pairwise homogeneity tests
  on N01 at p ≥ 0.0605; on N30C all four forms at rate exactly 0.000 against a 0.063 base
  rate, every pair p = 1.0000). The folder's most robust constraint is not a merge artefact.
- **M288's merge cannot be an artefact because there is effectively no merge**: 538 of 559
  form-occurrences are the plain form. The obvious objection to the arm A result is closed.
- **M243 is the least auditable family in the set**: 46 occurrences over **15** graphical
  forms, only M243~J (18) clearing the 15-line bar, so the merge is doing real work and is
  untestable. A second reason, beside its 4 informative blocks, why it sits at the boundary.

### Evidence

Pinned corpus reproduced (LF digest `8849716c…bf2b2dcf`, 1,467 files, 4,869 eligible
lines); all 15 published rows identical; the 6 original unit tests pass. The
re-implemented screen returns **1,056 tested / 54 selected, set-identical** to
`structure_associations.analyze` on the published training set. 9 new unit tests, two of
which pin the blocked exact test against the 2026-09-04 and 2026-09-17 implementations to
1e-9 relative on all eight pairs; the published M288–N45 floor of 0.12 reproduces to ten
decimals and equals the product 0.8 × 0.5 × 0.6 × 0.5 of its four blocks' max-overlap
probabilities.

Null model / split robustness: because the face-blocked p depends only on which
informative blocks the validation set holds (proved in code), **all 32,767 carrier-tablet
assignments were enumerated exhaustively** rather than sampled — a stronger form of the
label permutation the 2026-09-23 cross-reference requires. 79.45% of power-adequate splits
fire at p ≤ 0.05, rising monotonically with block count to 100% at ≥ 11 blocks and 99.81%
among splits with floor ≤ 1e-5. **Arm A sits at the 43rd percentile of that distribution**
and 45.5% of nine-block splits have a p at least as large, so the pre-registered parity
rule picked an ordinary split, not a flattering one.

### What failed, and the negative results

- **P4 as literally written is refuted**: 79.45% of power-adequate splits fire, not ≥ 80%.
  The shortfall is the floor again — "floor ≤ 0.05" admits splits with floor 0.049 that can
  only fire on a perfect result. The conditional version is strongly confirmed.
- **Arm B is the cleanest demonstration of the floor rule this folder has produced, and it
  is a negative result.** Its observed overlap is **19 of a maximum possible 19** — the most
  extreme outcome the data can physically produce — so its p equals its floor exactly,
  0.0150, and after BH over its 53 candidates q = 0.1325: **not confirmed.** A floor below
  0.05 means the test can fire *before* multiplicity, not after. The 2026-09-17 floor rule
  should be quoted against the corrected threshold the design will actually apply.
- **M106's family merge is the one that looks unsafe and still cannot be called**: M106 vs
  M106~A on N24, rates 0.133 (n=30) vs 0.417 (n=24), OR 0.23, p = 0.0284 — but BH over the
  16 within-family homogeneity tests run here puts every one at q ≥ 0.40. A flag, not a
  finding. Split M106 by form before using that lead.
- `face_and_form.test_b` documents a `family` argument but hardcodes `family = "M297"`;
  the family loop was reimplemented in `exact_form_audit.py` rather than patching that
  session's file. The M297 numbers reproduce exactly (0.0757 / 0.6941 / 0.1377).

### Still conditional

Everything remains **structural** — no semantic, phonetic or metrological value is assigned
to M288, N45, M263, N01 or any other sign. Novelty against specialist sign-by-sign
literature is still unestablished and was not searched this session. The two arms are not
two independent replications: their test statistics use disjoint informative blocks, but
each arm's *screen* used the other arm's validation lines, so the Fisher combination
(p = 6.2e-4) is indicative only. The enumeration covers M288–N45 only.

### Artefacts produced

`attempts/2026-10-02-block-aware-split/`: `PREDICTIONS.md`, `RESULTS.md`, `recon.py`,
`block_aware_split.py`, `exact_form_audit.py`, `test_block_aware_split.py` (9 tests),
`results/{block_aware_split.json, enumeration_full.csv.gz, exact_form_audit.json}`.
Board log: `board/log/2026-10-02-a-powered-split-is-a-marginal-and-a-retest-inherits-the-screens-family.md`.

### Next receipt

Platform: Claude Code on Linux, Claude Opus 5, no third-party Python packages, whole
directory runs in under 15 s. Tool limits: none hit; the pinned corpus cloned cleanly.
Material user steering: none — drawn pick taken as drawn, no override in
`board/TOP_INTEREST.md`. Costs unknown.

---

