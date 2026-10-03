# PROGRESS.md entry as written by session vd9la1 (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.

## 2026-10-02 – M288–N45 settled by a block-aware split; "the eight constraints" demoted to a sample (advancing)

**Session:** Breaker, Claude Opus 5, Claude Code cloud, scheduled. Mode: advancing.
**Drawn, not chosen:** `npm run draw` → stream B (rotation after the 2026-09-27 stream-A
session) → `historical-texts/proto-elamite`, highest coverage debt in the stream (idle 8.3 d,
debt 11.7). Took the pick. Named next move was HANDOVER item 1.
**Full write-up, code and machine-readable output:**
`attempts/2026-10-02-m288-n45-block-aware-split/` — start with `RESULTS.md`.
**Predictions frozen and committed (`31a1004`) before any file in `results/` existed:**
`PREDICTIONS.md`. Trial ID: none.

### Changed

HANDOVER item 1 is **discharged**: M288–N45, left by 2026-09-17 as "untestable rather than
refuted" (p-floor 0.12 on the bucket-0 holdout), is now **confirmed** against the face confound.
A second, larger result arrived with it and corrects this folder's framing: the 2026-09-04 set of
eight constraints is a low-power sample of a pervasively structured corpus, not the set of its
associations.

### Evidence

- **Reproduction first.** The 2026-09-04 pipeline re-run unchanged on a fresh clone at the pinned
  commit: all fifteen rows identical in every cell, odds ratio and q-value (p-values differ in the
  last one or two floating-point digits); corpus audit exact (1,467 files, 10 empty, 1,457 tablets,
  11,013 lines, 4,869 eligible). The CRLF/LF digest caveat is confirmed exactly as the handover
  recorded it — `8849716c…bf2b2dcf` on Linux, not drift. The 2026-09-17 self-match ratio
  reproduces at 0.406 against 0.408.
- **Why the pair was untestable — structural, not a matter of holdout size.** Of the 50
  `(tablet, face)` blocks carrying an M288+N45 line, **36 are forced** (`lo == hi`, zero variance
  under the conditional null) and **27 of those are single-line faces**. The face-blocked null
  therefore discards **38 of the 56 co-occurrence lines as information-free by construction**,
  leaving **16 informative blocks corpus-wide**, spread b0=4, b1=1, **b2=0**, b3=7, b4=4. No 20 %
  holdout could have settled this pair.
- **The split rule.** A tablet goes to validation iff it contributes ≥1 informative block for the
  pair under test; otherwise to training. Determined by block **marginals only**, never by the
  observed overlap — so it is ancillary to a null that is already conditional on those marginals.
  One of the 16 selected blocks has overlap **0** (maximally against the hypothesis), which is
  what a marginal-only rule looks like.
- **M288–N45:** p-floor **0.12 → 4.46×10⁻⁹**, face-blocked p **0.47 → 9.69×10⁻⁵**, BH q across the
  eight **1.29×10⁻⁴**, validation OR 13.47, plus an independent re-screen on the 4,771 training
  lines at **q ≤ 10⁻⁴, OR 10.39** that provably never sees a validation line.
- **The decisive null (P2, P3 — both confirmed).** 20,000 replicates each of two permutation
  nulls through the full split-and-test code. Size at α = 0.05 is **0.0171** (permute within
  block) and **0.0312** (permute within face strata, preserving N45's obverse/reverse skew and
  re-drawing marginals every replicate). Both **under** nominal: the procedure is conservative,
  not permissive. Replicates reaching the real p: **2/20,000** and **1/20,000**.
- **The ranking's required face number.** M288's own face effect is **0.0238 vs a mean
  between-sign signal of 0.0222 (ratio 1.07)** — one of four signs exceeding it individually,
  so the face-blocked test with real power was necessary, not decorative.

### What failed

- **P6 failed, and it is the session's most consequential finding.** Sweeping every
  `(M-family, N-sign)` pair with ≥20 lines per margin through the identical procedure, direction
  taken from the training complement: **72 of 390 testable pairs pass at 0.05**, against a NULL B
  expectation over 200 replicates of **mean 9.4, median 9, full range [3, 19]** — about **12×
  enrichment** (18.5 % vs 1.5 %, reported both ways because the null sweep tests more pairs,
  608.6 vs 390). Predicted < 40. Combined with the calibration above, the permissiveness branch is
  closed, so the conclusion is that **Proto-Elamite accounting is pervasively structured at the
  sign-pair level and the "eight confirmed constraints" was a low-power sample of that
  population.** M288–N45's own p-value is untouched; what changes is what membership in the eight
  *means*. Pairs ranking above it that 2026-09-04 never reported include M288–N39B (1.7×10⁻²⁹),
  M288–N24 (1.1×10⁻¹⁹), M376–N08A (1.6×10⁻¹³) and M106–N01 (2.4×10⁻¹¹). Rank was confirmed
  (14/390, predicted top 15); the count was not.
- **P5 failed, and corrects the 2026-09-17 tiering.** I predicted M243–N39B would have <10
  informative blocks and a floor above 0.01. It has **12 blocks and a floor of 6.46×10⁻⁹** and
  clears validation at p = 1.75×10⁻⁴. "Barely testable" was a fact about a 20 % holdout, not about
  the corpus — the power existed and the bucket split was wasting it. I inherited that verdict and
  repeated it in a frozen prediction without re-deriving it.
- **Six of the eight pairs clear validation but fail the re-screen — and that is my split rule,
  not evidence against them.** The rule moves 34–100 % of a pair's co-occurrence evidence into
  validation; when the fraction is high the screen is gutted. M106–N24 loses **all 14** of its
  co-occurrence lines and its training odds ratio **inverts to 0.44**. A session reading that as
  "M106–N24 refuted" would be reading its own split. M288–N45 pays the least of any enriched pair
  (33.9 %), precisely because its evidence sits mostly in forced single-line faces — so this rule
  suits this pair unusually well and is **not** a general replacement for a random holdout.
- **A deliberate deviation that inflates a number, recorded so it is not cited.**
  `competitors.py` takes direction from the *validation* odds ratio (giving every competitor its
  best shot) and reports 560 tested / 121 passing / rank 27. That is double-dipping.
  `competitor_null.py` takes direction from the training complement and is the source of every
  figure above. **Cite 72, not 121.**

### Still conditional

Everything remains structural — no phonetic, lexical or metrological value is assigned to any
sign. One corpus snapshot; replication on an independent CDLI export is still unrun and remains
the strongest falsification test. Novelty against specialist sign-by-sign literature is still
unestablished, and is now a *sharper* gap than before, because the sweep names ~72 associations
rather than 8.

### Next

See `HANDOVER.md`. First item: re-derive the constraint set from the 72-pair sweep with a
pre-registered multiplicity design, rather than inheriting the eight.

### Verification

- `python3 -m unittest -v test_block_aware_split.py` — **10/10 passed**, including the
  load-bearing `test_reproduces_2026_09_17_face_blocked_values`, which requires the exact function
  behind every number here to return all eight of the 2026-09-17 face-blocked p-values **and**
  floors on that session's bucket-0 holdout to a relative tolerance of 1e-12, with the reference
  **read from** that session's committed `results/power_floor.json` rather than retyped.
- `python3 -m unittest -q test_structure_associations.py` (2026-09-04 suite) — 6/6 passed.
- `test_split_is_invariant_to_observed_overlap` permutes N45 within each `(tablet, face)` block 25
  times, preserving all marginals and moving only the overlap, and requires the validation tablet
  set to be identical every time. It is — the ancillarity argument checked, not just asserted.
- Reproduction of the 2026-09-04 run diffed cell-by-cell against the committed
  `analysis/results/associations.csv`.
- Starting revision `a85de81`. Platform: Linux, Python 3 standard library only (the folder's
  no-third-party-dependency property is preserved; an initial numpy draft was rewritten in pure
  Python). Costs unknown. No material user steering — scheduled firing, no live input.

---

