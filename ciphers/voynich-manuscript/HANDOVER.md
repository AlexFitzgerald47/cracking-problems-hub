# Handover Notes – Voynich Manuscript

*Update at the end of every serious session. Latest notes at the top.*

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
