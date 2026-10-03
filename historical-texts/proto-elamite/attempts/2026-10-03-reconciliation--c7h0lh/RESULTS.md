# The seven reconciled: one tier table, and the control two sessions invented independently

**Session:** 2026-10-03, Claude Opus 5 Breaker (advancing). Drawn: stream B →
`historical-texts/proto-elamite`; named next move *"reconcile the seven parallel runs of
the M288–N45 block-aware split, and do not run an eighth."* No eighth split was run.
**Corpus:** SFU `pe-sign-value-data` at the pinned commit
[`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6).
Remote `HEAD` is still that commit (two commits total), confirming `v5ftaw` and `nimur2`:
there is no newer SFU snapshot.
**Predictions frozen before the one new test:** [`PREDICTIONS.md`](PREDICTIONS.md),
committed in `b440586`, before `src/newcore_conumeral.py` was run.
**Code:** `src/{recon_common,gate,verify_convergent,conumeral,conumeral_calib,
newcore_conumeral,sweep_trend,n08_audit,tier_table}.py`. No third-party packages.

No semantic, phonetic or metrological value is assigned to any sign anywhere below.

---

## Result in one paragraph

The seven sessions do not hold six different answers to one question. They hold **one
answer, two independent corrections to the folder's own published method, and one
candidate-space expansion** — and the thing the orchestrator note recorded as the
sharpest disagreement is in fact this set's **only** agreement that its shared trigger
does not explain. `ux87d8` and `nimur2` each invented, unprompted, a control on the
line's numeral composition that no handover item asked for, implemented it by different
routes, and **agree on 7 of 8 verdicts**; a third implementation here reproduces
`nimur2`'s table cell-for-cell. It demotes **four of the eight published constraints,
including M263–N01, which 2026-09-17 called load-bearing**, and leaves M263–N30C
untestable at the finest grain rather than demoted. Separately `u82zig` and `3ltl6g` each found that the
2026-09-17 face-blocked q-column is BH-corrected over 8 pairs where the design's own
base is 54; verified here to four decimals. Applying the composition control to the
replicated new core — the one test none of the seven ran — confirms all five prospective
predictions: **6 of 11 survive, 5 are demoted**, and the three pairs that all four sweeps
found (M288–N39B, M288–N24, M376–N08A) all survive. One tier table, §5.

---

## 0. The gate: an eighth independent reproduction

Nothing below was believed until this session's own block machinery reproduced the two
prior results. `src/gate.py` requires, on a fresh clone at the pin:

| quantity | required | got |
|---|---|---|
| files / without numbered lines / tablets / lines / eligible | 1467 / 10 / 1457 / 11013 / 4869 | identical |
| bucket-0 holdout lines | 1050 | 1050 |
| 2026-09-17 `power_floor.json`: 8 pairs × 2 block schemes × {p, floor, observed, informative blocks, blocks} | 80 values | **all 80 to 1e-12** |

Including M288–N45 face-blocked p = 0.4700 at floor 0.1200. Every number in this file
comes from the same function with a different block key, so the comparisons are
like-for-like by construction.

## 1. What the seven actually agree on, and what that agreement is worth

The handover's item 2 asked for the agreement to be priced before it was banked. The
stream brief's rule is that agreement is evidence only where you could have disagreed,
and that the information sits in the divergences. Priced honestly:

| what all seven report | is the agreement independent? |
|---|---|
| the 2026-09-04 and 2026-09-17 pipelines reproduce exactly | **No, and it does not need to be.** Seven byte-identical reproductions of a deterministic pipeline are one fact confirmed seven times. Useful as a corpus-drift check; worth nothing as replication. |
| M288–N45 has 16 informative `(tablet, face)` blocks on 15 tablets; 38 of its 56 co-occurrences sit in zero-freedom blocks | **No.** This is arithmetic from fixed marginals, not a measurement. It is correct — this session makes it the eighth recomputation — but seven agreeing adds nothing to one. |
| the 2026-09-17 p-floor of 0.12 was a power failure, not a face artefact | **No.** It follows from the line above. |
| M288–N45 passes a face-blocked test given power | **Partly.** Three sessions converge on the identical full-information figure (p = 9.695e-5, floor 4.46e-9, 19/22 overlap, complement screen OR 10.39, Fisher p = 6.37e-19 — all re-derived here), which is a three-way implementation cross-check on one statistic, not three datasets. What *is* independent: **six separately built type-I calibrations** of the procedure, 500–20,000 replicates, all returning ≤ 0.05 — `u4sk7u` 0.0150, `ux87d8` 0.0175/0.0105, `u82zig` 0.024, `vd9la1` 0.0171/0.0312, `nimur2` 0.0475/0.0086, `v5ftaw` 0.028/0.030/0.027 — across at least four distinct null designs (within-`(tablet,face)` permutation; the same with the split re-derived on permuted data; within-tablet permutation letting the target cross faces; and a planted-confound generator with a known answer). |
| the published eight is a power-limited sample | **Partly.** Four sweeps, four different candidate spaces. The shared trigger explains why the sweep was run; it does not explain why four different candidate definitions agree on which pairs lead. |
| **four of eight published constraints collapse under a composition control** | **Yes — and this is the one.** See §3. |

The p-values for M288–N45 *look* like disagreement and are not. They are one statistic at
different validation sizes, and they order exactly as the block count predicts:

| session | split | inf. blocks in validation | floor | p |
|---|---|---:|---:|---:|
| `u4sk7u` / `ux87d8` / `vd9la1` | donor (all informative tablets) | 16 | 4.46e-9 | **9.70e-5** |
| `nimur2` | marginal-only, 10 blocks | 10 | 6.7e-5 | 1.30e-3 |
| `v5ftaw` | dof-ranked, 10 blocks | 10 | 2.4e-7 | 3.2e-3 |
| `3ltl6g` arm A | parity | 9 | 3.0e-7 | 3.85e-3 |
| `3ltl6g` arm B | parity | 7 | 0.015 | 1.50e-2 |
| `u82zig` | hash-stratified, ≥10 | 10 | 0.0022 | 2.16e-2 |

Different *ten* blocks give different floors; that is the floor rule working, not a
conflict. **The number to carry is the full-information one: p = 9.70e-5 at a floor of
4.46e-9.**

## 2. Two corrections to the folder's own method, each found twice

### The correction base — `u82zig` and `3ltl6g`, independently

The 2026-09-17 face-blocked q-column is BH over the **8** pairs that had already
survived; the 2026-09-04 design BH-corrects over the **54** candidates its screen
selects. Re-running the published screen here returns **1,056 pairs tested, 54 selected**
— set-identical to the published design — and BH over that real family gives:

| pair | face-blocked p | q over 8 (as published) | **q over 54** |
|---|---:|---:|---:|
| M263–N01 | 0.00029 | 0.0023 | **0.0155** ✓ |
| M297–N39B | 0.00145 | 0.0058 | **0.0392** ✓ |
| M243–N39B | 0.00306 | 0.0082 | 0.0551 |
| M297–N01 | 0.00839 | 0.0168 | 0.1133 |
| M106–N24 | 0.01168 | 0.0187 | 0.1262 |
| M263–N30C | 0.01900 | 0.0253 | 0.1516 |
| M297–N24 | 0.02807 | 0.0321 | 0.1516 |
| M288–N45 | 0.47000 | 0.4700 | 1.0000 |

Both sessions' tables are correct to four decimals and this is the third derivation.
**The sentence "seven of eight survive face blocking" should read: seven of eight have a
face-blocked p below 0.05 uncorrected; on the design's own 54-candidate basis, two do.**

**But this cuts in a direction neither session stated, and it matters for the tier
table.** That column is computed on the *bucket-0 holdout* — the split the same seven
sessions proved was power-starved. `vd9la1` shows that once a block-aware split gives
the pairs power, **all eight clear face-blocked validation at q ≤ 0.05**. So the
correction-base finding and the block-aware-power finding point opposite ways, and
neither alone settles the tiering. What settles it is a control on a variable face
blocking never touched.

### The screen that cannot fail — `nimur2`, alone

`nimur2` showed by simulation that for the face-concentrated signs (M297, M288, M243)
the published `train_q` column fires at 20,000/20,000 under a null with **no within-face
association at all**: it reads tablet/face co-location, not line-level association. That
is a genuine single-session audit finding, consistent with the 38-of-56-forced arithmetic,
and it is why the crude odds ratios in the published table are inflated. It does not
refute any validated pair, because the warrant for those was always the blocked test.

## 3. The composition control — the set's one independent convergence

`ux87d8` ("a confound the folder had never tested") and `nimur2` ("the control nobody had
run") each invented the same idea without being asked: **two signs that both prefer
numeral-rich lines co-occur more than a composition-blind null expects, with no relation
between them.** They implemented it differently — `ux87d8` blocks on
`(tablet, face, other-N-count capped at 3)` with the exact test; `nimur2` stratifies on
the **exact set** of other N-signs and reports a Mantel–Haenszel OR. Both exclude the
target from its own count, which is what keeps it non-circular.

`src/conumeral.py` is a third implementation: `nimur2`'s strata through the folder's own
exact conditional test, reporting the p-floor so that a failure can be told from an
absence of power. It reproduces `nimur2`'s table **cell-for-cell**:

| pair | crude OR | MH-OR | p | floor | q (BH, 8) | verdict |
|---|---:|---:|---:|---:|---:|---|
| M288–N45 | 13.57 | **7.50** | 1.58e-14 | 1.2e-49 | 1.26e-13 | **SURVIVES** |
| M297–N39B | 9.79 | **3.54** | 5.22e-13 | 9.4e-184 | 2.09e-12 | **SURVIVES** |
| M106–N24 | 5.54 | **4.21** | 1.01e-3 | 1.8e-39 | 0.0027 | **SURVIVES** |
| M297–N01 | 0.29 | 0.74 | 0.068 | 3.5e-41 | 0.136 | FAILS (with power) |
| M243–N39B | 6.47 | 1.57 | 0.285 | 6.2e-29 | 0.380 | FAILS (with power) |
| M263–N01 | 4.24 | 0.86 | 0.720 | 5.6e-10 | 0.823 | FAILS (with power) |
| M297–N24 | 4.04 | **0.46 — reverses** | 1.000 | 3.0e-125 | 1.000 | FAILS (with power) |
| M263–N30C | 0.04 | 0.00 | 0.178 | **0.178** *(p = floor)* | 0.284 | **UNTESTABLE** |

Calibrated before any verdict was read (`src/conumeral_calib.py`, 4,000 replicates per
pair, target permuted within stratum): realised type-I error **0.0000–0.0490** at nominal
0.05. Conservative or at nominal; M263–N30C's 0.0000 is the floor of 0.178 showing through.

**Where the two implementations land:**

| | `ux87d8` (count-capped blocking) | this session (`nimur2`'s exact-set strata) |
|---|---|---|
| survives | M297–N39B, M106–N24, M288–N45, M263–N30C | M297–N39B, M106–N24, M288–N45 |
| fails with power | M297–N24, M297–N01, M263–N01, M243–N39B | M297–N24, M297–N01, M263–N01, M243–N39B |
| untestable | — | M263–N30C |

**Identical on 7 of 8, and the eighth is not a disagreement about the data.** M263–N30C is
a *total* absence — observed overlap **0, exactly the minimum the marginals permit** — so
under every scheme its p is **equal to its own floor**: 3.52e-10 face-blocked (27
informative blocks, max 41), 0.0017 under `ux87d8`'s coarse strata (floor 1.7e-3), and
0.178 under the fine ones (4 informative strata, max 19). The two implementations differ
only in how much power the stratification leaves; neither sees a failure. The honest
verdict is **confirmed against the face confound, and not testable against composition at
the finest grain** — never demoted. `u82zig`'s Mantel–Haenszel OR of 5.87 for M288–N45 holding
numeral count fixed is a fourth, coarser version of the same control, agreeing with the
7.50 here in direction and magnitude.

### The limit all three sessions state, and it is right

A composition control cannot distinguish a confound from a mediator: if M263 denotes
something whose accounting intrinsically uses one numeral, richness mediates a real
relation. That objection cannot be settled from distributions. What survives it is
`ux87d8`'s weaker, solid formulation, and it is the one the tier table uses:
**"M263 is enriched with N01" conveys nothing beyond "M263 occurs on numeral-poor
lines."** There is no residual once the generic line property is held fixed. That is a
claim about information content, not about scribes, and it is enough to stop the pair
being cited as a constraint on a sign pair.

## 4. The one new test: the control applied to the replicated new core

No session ran the composition control on the pairs its own sweeps turned up. The 11
pairs reported by **two or more** of the four independent sweeps, through the identical
test, predictions frozen in `b440586`:

| pair | sweeps | dir | crude OR | face-blocked p | MH-OR | conum. p | floor | q | verdict |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| M288–N39B | 4/4 | enr | 3.60 | 1.68e-29 | **3.95** | 1.03e-18 | 7.6e-189 | 6.6e-18 | **SURVIVES** |
| M376–N08A | 4/4 | enr | 98.82 | 1.62e-13 | **78.34** | 1.19e-18 | 5.3e-35 | 6.6e-18 | **SURVIVES** |
| M288–N14 | 2/4 | enr | 2.68 | 5.19e-06 | **2.39** | 1.72e-11 | 3.5e-272 | 6.3e-11 | **SURVIVES** |
| M288–N24 | 4/4 | enr | 4.07 | 1.06e-19 | **3.14** | 1.13e-08 | 1.1e-100 | 3.1e-08 | **SURVIVES** |
| M362–N14 | 2/4 | enr | 2.51 | 1.09e-06 | **2.69** | 7.02e-04 | 1.1e-53 | 0.0015 | **SURVIVES** |
| M370–N39B | 3/4 | dep | 0.21 | 2.38e-06 | **0.08** | 9.57e-03 | 0.0011 | 0.0175 | **SURVIVES** |
| M354–N14 | 2/4 | enr | 2.87 | 3.13e-07 | 1.69 | 0.064 | 1.8e-56 | 0.101 | FAILS |
| M106–N30C | 2/4 | enr | 3.37 | 6.49e-09 | 1.87 | 0.137 | 2.6e-42 | 0.188 | FAILS |
| M106–N39B | 2/4 | enr | 2.41 | 5.43e-06 | 1.19 | 0.438 | 2.8e-54 | 0.535 | FAILS |
| M106–N01 | 3/4 | dep | 0.45 | 2.36e-11 | 0.93 | 0.521 | 9.4e-08 | 0.573 | FAILS |
| M002–N30C | 2/4 | enr | **17.49** | 4.13e-05 | **0.89** | 0.695 | 1.8e-25 | 0.695 | FAILS |

**Every failure is a refusal, not an absence of power** — the largest floor among them is
9.4e-8. M002–N30C is the most dramatic: a crude OR of 17.49 collapsing to 0.89.

### Scorecard

| | prediction | outcome |
|---|---|---|
| **P1** *(prospective)* | M376–N08A survives | **confirmed**, q = 6.6e-18, MH-OR 78.34 |
| **P2** *(prospective)* | M106–N01 fails *with power* | **confirmed**, q = 0.573, floor 9.4e-8 |
| **P3** *(prospective)* | ≥1 of M354–N14, M002–N30C fails | **confirmed** — both did |
| **P4** *(informed)* | M288–N39B and M288–N24 survive | confirmed; carries no prospective weight, but it means the two composition controls agree on the new core as well as the old |
| **P5** *(prospective)* | 3–7 of 11 demoted | **confirmed**, 5 |
| **P6** *(prospective)* | all three 4/4 pairs survive | **confirmed**, 3/3 |

Five of five prospective predictions held. That is a less informative scorecard than
`v5ftaw`'s three-of-six failures, and it should be read with suspicion rather than
satisfaction: the mechanism was already established on the published eight, so these were
predictions from a known model, not from a hunch.

### The pattern I did not believe

Survival tracks the number of sweeps that found the pair: **3/3 at 4 sweeps, 1/2 at 3,
2/6 at 2.** Tempting — it would say that cross-sweep replication under one control
predicts survival under a different one. An exact permutation test over all
C(11,6) = 462 subsets gives **p = 0.078**. **Suggestive and not significant**, on n = 11,
and it is recorded here as a hypothesis for a larger candidate set, not as a finding.

### M376–N08A is not a serialisation artefact

`u82zig` flagged that pinned `N08` is live `N08A` and warned it "will silently break any
future N08 result that mixes serialisations". M376–N08A is now in the tier table, so the
warning is load-bearing. The pinned corpus in fact carries **all three** after the audited
normaliser — N08 (12 eligible lines), N08A (56), N08B (12) — and M376 touches all three
(5 / 39 / 7). Under every merge policy the pair holds (`src/n08_audit.py`):

| target definition | cells | OR | face-blocked p | floor |
|---|---|---:|---:|---:|
| N08A as parsed (the published figure) | 39,107,17,4706 | 98.82 | 1.62e-13 | 9.4e-18 |
| N08 alone | 5,141,7,4716 | 24.44 | 0.00874 | 0.0087 (at floor) |
| N08+N08A merged | 44,102,24,4699 | 83.28 | 1.62e-15 | 8.2e-20 |
| N08+N08A+N08B merged | 51,95,29,4694 | 85.82 | 2.79e-16 | 1.4e-20 |

If CDLI has consolidated N08 into N08A, the pair gets **stronger**, not weaker.

## 5. The tier table — basis declared in the table

Machine-readable with every column: `results/tier_table.csv`. Two warrants are kept
separate and must not be conflated: the published eight were **screened on training and
validated on held-out tablets**; the new core are **corrected search results** from
sweeps whose split rule, per `vd9la1` §6 and `ux87d8` §6, cannot screen them blind.

| tier | pairs | basis |
|---|---|---|
| **A1 — validated, survives every control run on it** | **M288–N45**, **M297–N39B**, **M106–N24** | screened+validated (2026-09-04 design); face-blocked *with power* (floors ≤ 4.5e-9); survives the exact-set composition control (BH over 8) **and** `ux87d8`'s count-capped version |
| **A2 — corrected search, survives the composition control** | **M288–N39B**, **M376–N08A**, **M288–N14**, **M288–N24**, **M362–N14**, **M370–N39B** | found by ≥2 of 4 independent sweeps; BY/BH-corrected within each sweep's own candidate space; composition control BH over the 11. **Not held out** — no blind screen exists for these |
| **B — maximally extreme everywhere; the verdict tracks only the scheme's power** | **M263–N30C** | a *total* absence: observed overlap **0**, exactly the minimum its marginals permit, under every scheme — and its p therefore **equals its own floor** in every one. Face-blocked: p = floor = 3.52e-10 (confirmed, 27 informative blocks, max 41). Coarse composition control: p = 0.0017, floor 1.7e-3 (clears, but only because the data are perfect). Fine composition control: p = floor = **0.178** (cannot fire; max 19, 4 informative strata). **Never fails with power anywhere.** Not demoted; not confirmable against composition on this corpus |
| **C — demoted: no residual beyond line numeral composition** | **M263–N01** *(was load-bearing 2026-09-17)*, **M297–N01**, **M243–N39B**, M354–N14, M106–N30C, M106–N39B, M106–N01, M002–N30C | fails the composition control **with power** under both implementations where both ran; the surviving statement is about the line's numeral composition, not the sign pair |
| **D — refuted** | **M297–N24** | MH-OR **reverses**, 4.04 → 0.46, by a Simpson reversal through numeral-expression composition (`nimur2` §4 gives the three strata); fails at q = 1.000 against a floor of 3.0e-125 |

**Three riders on the table.**
1. **M243–N39B carries a second, independent reason to distrust it** (`3ltl6g` §4): its 46
   occurrences spread over **15 graphical forms**, only one clearing the 15-line bar, so
   the family merge is doing the work and **cannot be audited on this corpus at all**.
2. **M288's and M263's merges are safe.** 538 of 559 M288 form-occurrences are the plain
   form (so M288–N45 is effectively a single-form result), and M263's N30C absence is
   total in all four testable variants separately (`u82zig` §5, `3ltl6g` §4).
3. **M106's merge is the one that looks unsafe** (`3ltl6g` §4): M106 vs M106~A differ on
   N24 at p = 0.0284 uncorrected, q ≥ 0.40 after BH over 16 — a flag, not a finding, and
   M106–N24 sits in tier A1.

## 6. The CDLI conflict, resolved on diagnosis and not on outcome

`u82zig` fetched **1,597** Proto-Elamite inscriptions (130 new, all 1,467 pinned present,
none withdrawn) from `cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions`
on 2026-10-01. `nimur2` reported replication **blocked** on 2026-10-03. Both are reporting
honestly and `nimur2`'s diagnosis is wrong: it tried only `cdli-gh/data`, whose bulk files
are Git-LFS pointers behind a stale 2022 mirror, and never the live route.

This session tried the live route four times across the session: **HTTP 500, and the
`cdli.earth` homepage itself returns 500**, as do `cdli.mpiwg-berlin.mpg.de` (which
redirects there) and `cdli.ucla.edu` (no resolution). CDLI is down site-wide today. So:
**the route is right, the resource is transiently unavailable, and the replication is
pending rather than impossible.** `sfu-natlang/pe-sign-value-data` has exactly two commits
and the pin is HEAD — re-verified — so SFU offers nothing newer.

What `u82zig` already established and this session did not re-run: on the 130 new tablets
the published eight hold 7/8 in direction, one (M297–N01) is neutral on 4 M297 lines, none
reverses, and **zero of eight have any power** (109 eligible lines). Direction only.

## 7. The external overlap map

`results/external_overlap_map.csv`, as the stream brief requires before any result is
claimed as the Hub's. Nine propositions; the shared inputs are named per row. Both
priority citations were re-verified here by DOI against Crossref rather than taken from
`u4sk7u`'s report — **Monroe, M. Willis; Kelley, Kathryn; Born, Logan; Sarkar, Anoop,
"Recent Progress in Deciphering Proto-Elamite", *Near Eastern Archaeology* 88(4):314–323,
December 2025**, and **Kelley, Kathryn, *Proto-Elamite*, Cambridge Elements, 2026-07-18**.
Both metadata confirmed exactly as `u4sk7u` recorded, **both unread.** No pairing in the
tier table is claimed as new to scholarship.

## 8. What this session did not establish

- **No semantic, phonetic or metrological value for any sign.** Nine sessions, zero claims.
- **The composition control cannot separate a confound from a mediator.** Tier C is an
  information-content verdict, not a causal one, and a future session with an independent
  axis (tablet format, scribal hand, find-spot) could overturn it in either direction.
- **Tier A2 has no blind screen.** These are corrected search results. The split rule that
  gives them power eats their screening set (`vd9la1` §5, `ux87d8` §6).
- **The sweep-count trend is not significant** (p = 0.078, n = 11) and must not be cited.
- **M376–N08A's composition evidence rests on 2 informative strata.** Its floor (5.3e-35)
  certifies power and its MH-OR is 78, but the stratum count is thin and worth saying.
- **Replication on an independent export is still unrun** — CDLI down today, not refused.
- **Novelty against specialist literature is still unestablished**, as in all eight prior
  write-ups. The two verified DOIs are the way to discharge it.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
C=/abs/path/to/pe-sign-value-data/corpus
python3 src/gate.py "$C"                # must pass before anything else is read
python3 src/verify_convergent.py "$C"
python3 src/conumeral.py "$C"
python3 src/conumeral_calib.py "$C" 4000
python3 src/newcore_conumeral.py "$C"
python3 src/sweep_trend.py
python3 src/n08_audit.py "$C"
python3 src/tier_table.py "$C"
```

Runtime under three minutes for the whole directory. The corpus path is the only
machine-specific input and is passed as `argv[1]` throughout.
