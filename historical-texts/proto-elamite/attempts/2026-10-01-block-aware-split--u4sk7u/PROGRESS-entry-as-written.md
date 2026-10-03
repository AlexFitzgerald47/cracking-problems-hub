# PROGRESS.md entry as written by session u4sk7u (landed by the orchestrator, 2026-10-03)

This session's own additions to `historical-texts/proto-elamite/PROGRESS.md`, preserved verbatim.
It was one of seven parallel sessions; see `HANDOVER.md` §orchestrator note 2026-10-03.


---

## 2026-10-01 – breaker session: M288–N45 settled, and the holdout retired

**Drawn, not chosen.** `npm run draw` → stream B → this folder (working, idle 8d,
debt 11.2). Took the pick and its named next move: recommended experiment 1,
*settle M288–N45 with a block-aware split*. Claim taken and released.
Full report: `attempts/2026-10-01-block-aware-split/RESULTS.md`.
Frozen before any new p-value: `attempts/2026-10-01-block-aware-split/PREDICTIONS.md`.

### Changed

- **M288–N45 is confirmed and moves from "untestable at holdout scale" to
  load-bearing.** This folder's 2026-09-17 frozen prediction **A2 is refuted**.
- **The 80/20 tablet holdout is retired for conditional tests on this corpus.** It
  protects against nothing the multiple-testing correction does not, and costs ~80 %
  of the data. Argued, simulated and priced; see below.
- **The constraint set expands from 8 to 26 pairs at p ≤ 1e-4**, 20 of them new to
  this folder. Candidate tier, not load-bearing.
- **One prediction of this session's own is withdrawn** (P5) and **one scored failed**
  (P4). An entry-level result was withdrawn mid-session as a single-tablet artefact.

### Evidence

Two reproductions before anything new. The unchanged 2026-09-04 pipeline on a fresh
clone of the pinned commit is **byte-identical** to the committed results on all 15
rows; corpus digest `8849716c…8bf2b2dcf`, exactly the Linux hash the 2026-09-17
handover predicted — no drift, no re-pin. The new generalised block code reproduces
`attempts/2026-09-17-exact-form-and-face/results/power_floor.json` to 1e-12 on **all
16 cells**. The new column/entry parser is asserted line-for-line against the audited
one on all 11,013 lines.

**P1–P3 hold.** Split: validation = every tablet owning an informative `(tablet, face)`
block (15 distinct tablets); training = the rest. The unchanged screen re-run on that
complement still selects the pair (q = 1.13e-16, OR = 10.39). Face-blocked exact test
on validation: **p = 9.695e-5**, floor 4.46e-9, 16 informative blocks. Column-level
blocking gives the identical p.

**Why 2026-09-17's test had no power — the part worth keeping.** Not sample size:
**occupancy**. M288 occupies *every* eligible line on 179 of the 350 faces where it
occurs (mean within-face occupancy 0.701), which is **rank 1 of the 145 signs** with
≥ 10 faces. 38 of the pair's 56 co-occurrences therefore fall in blocks where the
overlap is forced by arithmetic and the block contributes a point mass, not
information. A within-block conditional test is blind to a covariate that saturates
its blocks, and no amount of further data of the same kind repairs it.

**P4 failed, conservatively, and the prediction was the wrong shape.** The split is
chosen on the pair's own block marginals, so the folder's standing label-permutation
rule applies. Informativeness is a function of marginals alone and the conditional
null fixes marginals, so the selected block set should be invariant. It is:
**0 of 16,000 replicates moved the split** (2,000 × 8 pairs). But the realised
false-positive rate is 0.0150 at nominal 0.05, outside the frozen [0.03, 0.07] band.
Scored **failed**. The cause is discreteness — most informative blocks have
`hi − lo = 1` — which makes an exact test satisfy P(p ≤ α) ≤ α, not = α. A two-sided
calibration band is simply wrong for a discrete statistic.

**P5 failed.** M288 is *not* a face-level marker. With the tablet-face as the unit and
the tablet as the block, M288-bearing faces are not significantly enriched for N45:
**p = 0.109**, floor 0.0156 — powered, and it did not fire. Direction is right (face
OR 6.97) but this folder may not claim it.

**Withdrawn mid-session.** The entry-level rung (ATF `2.A.`/`2.B.` sub-lines of one
accounting entry) gave M288–N45 p = 3.125e-2 — which is exactly 2⁻⁵, the test's own
floor. Its five informative entry blocks are **all from one tablet, P008020**. It
carries no information and is withdrawn. The face-level result's 16 blocks, by
contrast, come from 15 distinct tablets, and every pair in the expanded table rests on
≥ 4.

**The holdout finding.** The 2026-09-04 holdout exists because the *screen's* pooled
Fisher p-values are invalid (same-tablet lines are not independent). The *validation*
statistic is valid on its own — it conditions on block marginals. Selecting a pair by
its own p-value needs multiple-testing correction, not a holdout. Running the valid
test corpus-wide over all 1,430 pairs meeting the published support thresholds (514 of
them powered) gives **26 pairs at p ≤ 1e-4**. The null — permute every N-sign within
each `(tablet, face)` block and re-run the whole 1,430-pair sweep, 500 times, ~257,000
null tests — gives **mean 0.02, maximum 1, permutation p = 0.0020** (the floor at 500
reps), and its **smallest p anywhere is 1.428e-5** against an observed sweep minimum of
**1.683e-29**. Every one of the 26 passes the `M036+1(N30D)` tautology check (maximum 2
bound lines anywhere, and the parser excludes pre-comma N-signs regardless; M288–N45
and M288–N39B are at zero) and rests on ≥ 4 distinct tablets.

**Also done.** The M288 exact-form audit (2026-09-17 recommended experiment 3): 538 of
559 M288 occurrences are plain `M288` and no variant reaches 20 lines, so the family
merge is vacuous for M288 and the confirmation is not a merge artefact. M263 is still
unaudited.

**Priority check** (stream B brief, before any novelty language). Crossref enumeration
from 2022, cross-checked against OpenAlex; identical author lists from both. Two items
postdate this folder's last session: **Monroe, Kelley, Born & Sarkar**, "Recent Progress
in Deciphering Proto-Elamite", *Near Eastern Archaeology* 88(4):314–323, Dec 2025,
[10.1086/738240](https://doi.org/10.1086/738240) — closed access, no OA copy, **unread**;
and **Kelley**, *Proto-Elamite*, Cambridge Elements, 18 Jul 2026,
[10.1017/9781009614559](https://doi.org/10.1017/9781009614559) — abstract verified, full
text unread. **No novelty is claimed against the specialist literature**; "new" means new
to this folder.

### Still conditional

Structural only; no sign gets a semantic, phonetic or metrological value. The corpus is
1,334/1,467 MDP (Susa). The expanded table rests on the ancillarity of selecting on
marginals — argued, simulated at the split level, priced at the sweep level, and pinned
by a unit test, but it would fail if any selection step used an overlap. None does. The
20 new pairs have had the tautology, replicate and search-budget checks and nothing
else; they sit at the tier the published eight occupied on 2026-09-04.

### Next

See `HANDOVER.md`. First move: re-run the 2026-09-17 face-blocked audit **and** the
corpus-wide sweep on a newer CDLI export, with the 26-pair table as the frozen
prediction.

### Receipt

Starting revision: `main` at the 2026-09-27 draw commit. Model/platform: Claude Opus 5,
Claude Code on the web, Linux container. Tool limits: no access to *Near Eastern
Archaeology* 88(4) (closed, no OA copy). Material user steering: none — scheduled
Breaker firing, work taken from `npm run draw`. Trial ID: none. Cost: unknown.
