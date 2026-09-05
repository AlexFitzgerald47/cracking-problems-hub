# Handover Notes – Voynich Manuscript

*Update at the end of every serious session. Latest notes at the top.*

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
