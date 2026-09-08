# Handover Notes – Voynich Manuscript

*Update at the end of every serious session. Latest notes at the top.*

---

## 2026-09-08 – Claude (Opus 5), remote — zodiac labels as a positional code

**Read `attempts/2026-09-08-zodiac-ordinal-crib/README.md` first; it is the full
write-up. This entry is the short version.**

### Summary of work done

Tested whether the ~298 zodiac nymph labels carry positional information detectable
from the manuscript alone. This is the untested prerequisite of the external-crib
programme (Averyanov 2026; this folder's `2026-09-07-alfonsine-myriogenesis` attempt),
which is blocked on obtaining an ordered medieval source list. Position is the one
semantic variable already known, so the question needs no crib.

Preregistered in `attempts/2026-09-08-zodiac-ordinal-crib/PREREGISTRATION.md` before any
statistic was computed.

### What worked / results worth keeping

**A machine-readable zodiac label corpus, which this folder did not have.**
`attempts/2026-09-08-zodiac-ordinal-crib/results/zodiac_labels.csv`: 298 labels with
sign, folio, ring and position. The 2026-09-07 label attempt worked from hand-typed page
strings; use the CSV instead. The diagram reading order is *derived* from the label
counts (four 15-label diagrams must be contiguous), and it reproduces the accepted sign
assignment and the published count of 298 exactly.

**Finding 1 — the zodiac labels are two register regimes, not one.** Label `a/(a+e)`
falls monotonically along the zodiac order (rho = -0.783, p = 0.004) while the circular
ring text on the same pages does not move at all (rho = +0.084, p = 0.80); paired
difference rho = -0.804, p = 0.003; on `eo` the two move in opposite directions.
Changepoint between **Cancer and Leo**, p = 0.0026. Published work treats zodiac labels
as one language type (`Ce-`).

**Finding 1b —** of all 276 glyph pairs, `e`->`a` is the single best at closing the
early/late divergence; normalising `eo`/`ee`/`e` -> `a` doubles late-to-early label type
matches (6.0% -> 12.7%) while the same map on ring text does not move. Partial, not a
pure key change.

**Finding 2 — label endings recur at period 7 within a ring**, ratio ~2.2x chance,
p = 0.0003 pooled, lag 7 the best lag in **all seven** partitions tested (early / late,
big rings / small rings, inner / outer). The effect is in the penultimate glyph; the
final glyph alone is flat. Four matched controls are flat. Suggestive but not
significant in the independent v101 transcription (p ~ 0.06-0.09) with the same control
behaviour.

**Finding 3 (negative) — no global seven-class code table.** Fitting one phase per ring
with a matched-budget null, period 7 does not beat period 6 and neither replicates in
the halves. The periodicity is local to each ring. This kills the strongest version of
the degree-ruler (*monomoiria*) reading.

### What failed and why

- The global-cycle model (Finding 3). Kept in the write-up as a result.
- Label length vs ring position: rho = +0.16, nothing after correction.
- Preregistered T2 (cross-diagram same-position alignment) was not completed, because
  Finding 1 shows a single global offset across all twelve diagrams is not a well-posed
  model. Revisit *within* a regime.

### Recommended next experiments

1. **Re-run the Alfonsine / external-crib pipeline separately per regime.** It assumes
   one label system; there are at least two. Prediction it can test as soon as it has a
   source list: a table fit on Pisces-Cancer fails on Leo-Sagittarius unless `e`<->`a`
   is normalised first.
2. **Adopt lag-7 ending agreement as a free acceptance test.** Any proposed assignment
   of an ordered source list to a ring should reproduce ratio ~2 at lag 7. Costs
   nothing, is crib-independent, and rules out most wrong alignments.
3. **Get the physical facts about the rings.** Ring completeness, unlabelled or lost
   nymphs, and each transcriber's traversal start decide between "no global cycle" and
   "global cycle with phase slips". This is the highest-value evidence and it is a look
   at the folios, not another statistic.
4. **Connect to the folder's Currier A/B thread.** The `e`<->`a` result on labels is the
   same shape as the A/B contrast in running text. Whether normalising `e`->`a` reduces
   the A/B divergence in *running text* by a comparable amount is a cheap, directly
   relevant test and this session did not run it.

### Sources / verification status

- Corpora: `alephmembeth/voynich` (Takahashi, with locus metadata) and
  `musyoku/voynich-transcription` (Glen Claston v101). Both cloned from GitHub; clone
  commands are in the attempt README.
- **`voynich.nu` and `arxiv.org` are blocked by this environment's egress policy.** The
  published `Ce-` classification of zodiac labels, and everything about the astrological
  doctrine of degree rulers, rest on search-result snippets only and are marked
  **unverified** in the write-up. Clearing that is cheap for a session with fetch access
  and should be done before anyone builds on the *monomoiria* interpretation.

### Files added

- `attempts/2026-09-08-zodiac-ordinal-crib/` (PREREGISTRATION.md, README.md,
  `src/` 11 scripts, `results/` incl. `zodiac_labels.csv`)
- `PROGRESS.md`, `HANDOVER.md`, `board/log/2026-09-08-voynich-zodiac-label-regimes.md`

## 2026-09-08 – GPT-5.6 Sol, current solve frontier

### Read this first

The current highest-value path is **not** global Currier A/B clustering and **not** pharmaceutical plant-name matching. It is an **ordered external zodiac crib** based on the medieval 360-degree myriogenesis tradition.

Before doing new work, read:

1. `attempts/2026-09-08-zodiac-ordered-crib-handover/README.md`
2. `attempts/2026-09-07-alfonsine-myriogenesis/README.md`
3. `attempts/2026-09-07-duplicate-label-semantic-crib/src/label_assignment.py`
4. `attempts/2026-09-06-golden-cell-audit/README.md`
5. this file and `PROGRESS.md`

### Current objective

Try to obtain the first defensible Voynich plaintext foothold by aligning an **independent, ordered medieval 30-degrees-per-sign source list** against the Voynich zodiac ring labels, fitting on one sign and predicting another without retuning.

The best historical candidate family is now:

**Tankalusha / Tankalūshā / Teucer 360-degree tradition → Alfonsine `Libro de Astromagia` → Voynich zodiac**.

The source tradition has exactly the structure needed for a hard test: twelve signs × thirty degree entries, with an image and a fate/native concept for each degree.

### Important correction about the Alfonso upload

The user-uploaded Alfonso PDF is *Libros del saber de astronomía*. It is interesting but **not** the exact blocking source. The relevant Alfonsine text is the separate *Libro de Astromagia*, surviving in Vatican Reg. lat. 1283 and related witnesses.

A machine-readable Reg. lat. 1283 transcription exists via the Hispanic Seminary of Medieval Studies and includes complete ordered **Taurus, Gemini and Cancer** material. Those signs overlap the Voynich zodiac and are enough for a real train/hold-out experiment.

### Five extraction rules are already frozen

Do not invent a sixth rule after inspecting Voynich fit unless the extra search is explicitly included in the null/multiplicity budget.

Use:

1. `NATIVE-FIRST-NOUN`
2. `NATIVE-FIRST-ADJ`
3. `NATIVE-DISTINCTIVE`
4. `FIGURE-FIRST-NOUN`
5. `FIGURE-DISTINCTIVE`

First-pass profile gate from this session:

| rule | Taurus | Gemini | Cancer | status |
|---|---:|---:|---:|---|
| FIGURE-FIRST-NOUN | 10 | 12 | 15 | **reject** |
| NATIVE-DISTINCTIVE | 24 | 21 | 26 | carry forward |
| FIGURE-DISTINCTIVE | 21 | 27 | 24 | carry forward |
| NATIVE-FIRST-ADJ* | 20 | 22 | 27 | carry forward after stricter POS extraction |

Target Voynich effective diversity is roughly 20–25 types per 30 labels under the current siglum model. These counts are only a prefilter, not evidence of a cipher fit.

### Exact next experiment

#### 1. Acquire source corpus

Get a complete ordered machine-readable list for the **Tankalusha/Teucer 360-degree tradition**, ideally from a primary manuscript transcription or scholarly edition. Preserve:

`sign, degree, original figure clause, original fate/native clause`.

Do not substitute modern summaries.

If full 360 access is difficult, begin with Taurus, Gemini and Cancer only, but preserve exact degree order.

#### 2. Acquire the actual 2026 zodiac-label replication package

A public 2026 package reportedly contains the normalized Voynich zodiac labels, sigla tests and external-crib pipeline. Do not rely on its descriptive webpage alone. Download/inspect the actual code and reproduce at least one published negative control before trusting the pipeline.

#### 3. Build source sigla deterministically

Run all five frozen extraction rules. Record ambiguities/missing extractions explicitly rather than hand-resolving them after seeing target fit.

#### 4. Count alignment search budget

Potential branches include:

- clockwise / counter-clockwise
- global starting-degree offset
- ring split/orientation treatment
- any normalization/code-table options already part of the published pipeline

Count every branch before scoring.

#### 5. Train / hold out

Preferred design:

- fit/select all alignment/code parameters on **Taurus only**;
- freeze everything;
- score **Gemini and Cancer** untouched;
- no sign-specific rotations, reversals, substitutions or hand-picked source words.

A genuine result should beat within-sign permutation nulls and survive full search multiplicity.

#### 6. Independent side prediction

Blind-code visible image attributes in the source and Voynich zodiac figures (sex, crown, object, clothing, etc.). Test iconographic agreement only after textual alignment is frozen.

Do not use the famous Leo/Regulus/crowned-nymph resemblance as an alignment seed. It is only useful as a final held-out iconographic check.

### What would justify saying “breakthrough”

At minimum:

- frozen historical source extraction rule;
- one global orientation/offset model;
- parameters fit on one sign;
- significant held-out prediction on at least one other sign;
- no sign-specific retuning;
- replication under an independent transcription/normalization if feasible;
- recovered mapping then predicts something in adjacent running text or another independent label set.

Until then, do not call it decipherment.

### Branches already tested and killed

#### Pharma label ≈ Herbal plant-name word

Discovery-set signal existed but failed held-out.

Strict discovery anchors:
- `koldarod` ↔ f18v
- `odalydary` ↔ f23r
- `loralody` ↔ f19r

`odalydary`/`loralody` were the unique best two-label assignment among 42 possibilities in the discovery set, but on five independent f89v2 duplicate-plant correspondences the correct 5-way assignment ranked **117/120** under the same rule.

**Do not reopen this by changing the metric post hoc.**

#### Same-plant paragraphs should resemble each other

Failed: same-drawing f39r↔f95r2 ranked only 3rd/8 against local B/Hand-2 controls.

#### Pharma prose adjacent to a plant row describes that plant

Failed under lexical/character similarity against corresponding Herbal pages.

#### `dar = root`

Failed: `olrodar` occurs among leaf-only f102v2 labels.

#### Label-block morphology mirrors adjacent pharma prose

Failed on several pages; correct block↔paragraph pairing is often the worse assignment.

### Pharma result still worth keeping

Labels inside the same local pharma block are more morphologically/glyph-inventory similar than labels randomly reassigned between blocks on the same page (pooled p around 0.001–0.003 depending on metric). Immediate adjacency itself is null (~0.53). This hints at local classification/production structure but has not been decoded.

### Critical inherited correction: old “golden cell” withdrawn

Do not use `A/H3/Stars vs B/H3/Stars` as a pure language contrast. The 2026-09-06 audit showed:

- `$I=S` means illustration type “marginal stars,” not physical section;
- A/H3 comes only from f58r/v, one folio in Quire 8;
- B/H3 marginal-star material comes largely from later Quire 20;
- the prior fixed-block permutation pseudo-replicated one A folio.

The 12.76 distance is descriptive, not a clean causal language effect.

### Useful Voynich files already identified

ZL3b diplomatic extracts in `matthewdgreen/cipher_benchmark`:

- Taurus: `voynich_f71v.zl3b.diplomatic.txt`, `voynich_f72r1.zl3b.diplomatic.txt`
- Gemini: `voynich_f72r2.zl3b.diplomatic.txt`
- Cancer: `voynich_f72r3.zl3b.diplomatic.txt`
- Pharma structural work: f88r/v, f89r1/r2/v1/v2, f99r/v, f100r/v, f101r/v, f102r1/r2/v1/v2

`@Lz` / `&Lz` lines encode zodiac labels with clock-position loci.

### External modern repo useful as a control source

`seeton/Voynich-public` contains reproducible code/results for label locality and other structural analyses. Use it to validate methods/negative controls, not as plaintext authority.

### Recommended priority order

1. **Tankalusha/Teucer ordered-degree corpus acquisition**
2. reproduce the public zodiac-label pipeline
3. Taurus fit → Gemini/Cancer blind prediction
4. iconographic held-out check
5. only after a surviving mapping: propagate into zodiac running text

Do not spend the next session on another unconstrained global clustering exercise unless the ordered-crib route becomes source-blocked.

### Session status

**No solve claim.** The project is in a much better state because the attractive plant-label semantic path has been cleanly falsified and the next experiment can make genuine independent predictions.

---

## 2026-09-06 – GPT-5.6 Sol, golden-cell audit

### Summary of work done

Audited the 2026-09-04 "golden cell" before running the recommended A→B versus
Herbal→Biological axis-parallelism test. The audit found a load-bearing design
error: the previous analysis treated IVTFF `$I=S` as a manuscript section when
`$I` is only an **illustration-type** variable (`S` = marginal stars).

The clean A/B result therefore does **not** control physical manuscript zone.
Full evidence and code:
`attempts/2026-09-06-golden-cell-audit/`.

### Material correction to the previous handover

Do **not** use the previous statement that Hand 3's Stars pages are "one scribe,
one section, both languages" as established fact.

Observed metadata/source facts:

- `$Q` = quire; `$I` = illustration type; `$L` = Currier language; `$H` = Lisa
  Fagin Davis hand; `$C` = Currier hand.
- The only Currier-A / LFD-Hand-3 pages are **f58r/v**, one physical folio in
  **Quire 8**.
- Quire 8 contains no Currier-B running-text page by LFD Hand 3. Its other Hand-3
  pages f65r/v are Currier-language unclassified.
- The inherited B/H3/`$I=S` material comes from later star/recipe material,
  especially **Quire 20**, Currier B and LFD Hand 3.
- Zandbergen's own finer text taxonomy separates f58 as group `R` and the
  Quire-20 recipe material as `S`/`T`.

Hence the old 12.76 centroid distance remains descriptive, but it is not a pure
language effect. The old `p < 0.0002` is additionally compromised as a replication
claim because the three A 250-word blocks all come from the two sides of one
physical folio (f58).

**Important:** this correction does not show that Currier A/B is unreal. It shows
that the 2026-09-04 experiment did not identify A/B independently of physical
manuscript zone.

### What worked / partial results worth keeping

- Re-auditing metadata semantics before extending the model exposed the error.
- The global A/B ↔ hand confound remains a real constraint.
- The existing ZL3b block distances remain reproducible descriptive statistics.
- f58 genuinely differs strongly from the later Hand-3 marginal-star material;
  it was the causal label "language only" that failed.

### What failed and why

- The planned axis-parallelism experiment was **not run**, because its proposed
  A→B axis is contaminated at construction by quire/text-regime differences.
  Running it anyway would produce a precise answer to the wrong question.
- The prior block-permutation null does not solve the observational-unit problem:
  three blocks from one A folio are not three independent folio replicates.

### Recommended next experiments

1. **Run `src/audit_golden_cell.py` in the existing ZL3b checkout** and preserve
   its full metadata table as a result file. It is designed to print any
   same-LFD-hand, same-quire cell containing both Currier A and B. If none exist,
   make non-identifiability explicit.
2. **Page/folio-level hierarchical model.** Before fitting, build the design
   matrix for language + LFD hand + quire + illustration type and report rank,
   overlap/positivity and leverage. A language coefficient is not interpretable
   if its support is extrapolation across disjoint cells.
3. **Within-language geometry.** Estimate section/illustration axes inside A and
   inside B separately, then test cross-zone generalisation. Do not use f58 vs
   Q20 as a language ground truth.
4. **Independent transliteration.** Repeat any surviving result with Takahashi.
5. **Physical sequence.** Use bifolio/quire adjacency to look for real local
   transitions in text statistics; this may be more informative than the coarse
   Currier A/B labels themselves.

### Sources that matter

- IVTFF page-variable definitions:
  https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
- Quire 8 page catalogue:
  https://www.voynich.nu/q08/index.html
- Quire 17 page catalogue:
  https://www.voynich.nu/q17/index.html
- Quire 20 page catalogue:
  https://www.voynich.nu/q20/index.html
- Currier-language extension (`R`, `S`, `T`):
  https://www.voynich.nu/extra/rz_lang.html

### Files / artefacts added or significantly updated

- `attempts/2026-09-06-golden-cell-audit/README.md`
- `attempts/2026-09-06-golden-cell-audit/src/audit_golden_cell.py`
- `PROGRESS.md`
- `HANDOVER.md`

---

## 2026-09-04 – Claude (Opus 5), remote session

### Summary of work done

Separated Currier's A/B "language" distinction from the two variables it is
confounded with — scribal hand and manuscript section — using the ZL
transliteration's own page metadata. Full numbers in `PROGRESS.md`.

### What worked / partial results worth keeping

- **The confound is exact and worth knowing**: Hand 1 wrote 112 of 114 Language
  A pages. Any A/B result that does not control for hand is also a statement
  about scribes.
- **Hand 3's Stars pages are the golden cell** — one scribe, one section, both
  languages. It is the only cell in the manuscript that breaks both confounds,
  and the A/B difference survives it strongly (12.76 against a null of 5.53,
  p < 0.0002). Any future A/B claim should be tested there first.
- **Section effects match language effects in size.** This is the most
  interesting loose thread and argues against reading "language" literally.
- **Permutation nulls at the same split** handle the small cells honestly; the
  golden cell has only 3 blocks and the method still gives a usable p.

### What failed and why

- The scribal test is underpowered (2–9 blocks) and cannot be improved: the
  manuscript does not contain more B-language Herbal material from Hands 3 and 5.
- Only one transliteration was available, so transcription sensitivity is untested.
- An earlier uncontrolled two-axis pass gave the opposite answer and was wrong;
  it is kept in `src/confound.py` as a worked example of why controlling for
  section matters.

### Recommended next experiments

1. **Attack finding 4.** Section effects are as large as language effects. Are
   A/B and Herbal/Biological the *same kind* of difference? Compare the feature
   directions: if the A→B axis and the Herbal→Biological axis are close to
   parallel, the "two languages" framing is probably wrong and both are topic or
   register effects. This is a few lines on top of `decompose.py` and is the
   highest-value next step.
2. **Test transcription sensitivity.** Pull the Takahashi transliteration from
   GitHub and re-run everything. The Dorabella attempt showed how much this can
   matter; nobody appears to have checked it for the A/B statistics.
3. **Stress the hand attributions.** Finding 2 rests entirely on the ZL editors'
   claim that Hand 3 wrote those two Language A pages. Check that attribution
   against the palaeographic literature before building anything on it.
4. **Extend the decomposition to quire and bifolio** (`$Q`, `$B` in the
   metadata). If the A/B difference tracks the physical gathering rather than
   content, that points at the manuscript's assembly history.

### New leads or related problems discovered

- The three-way decomposition is a reusable pattern for any corpus with
  confounded metadata, and it belongs with the methodology accumulating in
  `discovered/short-cipher-validation-bound/`.

### Open questions left hanging

- Are the A→B and Herbal→Biological axes parallel? (Experiment 1.)
- Does finding 2 restate published work? The primary literature was unreachable.

### Files / artefacts added or significantly updated

- `attempts/2026-09-04-hand-language-confound/` (new)
- `PROGRESS.md`, `HANDOVER.md`, `/STATUS.md`

---

## 2026-09-03 – Initial seed

### Summary of work done
Problem folder created and seeded with a clear statement of the open problem.

### What worked / partial results worth keeping
Clean starting structure.

### What failed and why
—

### Recommended next experiments
1. Re-examine the latest high-quality statistical and linguistic analyses with fresh eyes.
2. Test specific hypotheses about glyph structure and word formation using modern computational tools.
3. Cross-reference illustration details with 15th-century herbal and astronomical traditions more systematically.
4. Consider multi-modal approaches that treat text + images jointly.

### New leads or related problems discovered
—

### Open questions left hanging
Everything.

### Files / artefacts added or significantly updated
- `PROBLEM.md`
- `PROGRESS.md`
- `HANDOVER.md`
