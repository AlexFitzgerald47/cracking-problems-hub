# Progress Log – Voynich Manuscript

*Append new entries at the top. Never delete previous entries.*

---

## 2026-09-08 – GPT-5.6 Sol, semantic-crib falsification and zodiac pivot

### What was attempted

Pushed the 2026-09-07 duplicate-plant/pharmaceutical-label lead through held-out tests, then moved to the stronger closed-list zodiac route. The session also audited the pre-existing Alfonsine myriogenesis attempt and identified the earlier Tankalusha/Teucer 360-degree tradition as the best current external crib family.

Full continuation handover:
`attempts/2026-09-08-zodiac-ordered-crib-handover/README.md`.

### Duplicate-plant result: discovery signal but held-out failure

Three strict Herbal↔Pharma duplicate drawings were used as anchors:

- f18v ↔ fragment 212, label `koldarod`
- f23r ↔ fragment 213, label `odalydary`
- f19r ↔ fragment 240, label `loralody`

`koldarod`↔f18v had prior public notice in 2024. The two other labels produced a real discovery-set result: among seven strict duplicate Herbal pages, minimum single-word edit distance gave the correct `odalydary`→f23r and `loralody`→f19r assignment as the unique best of 42 possibilities (1/42 ≈ 0.0238). The distance matrix was checked in Takahashi and ZL3b.

This **did not replicate**. On five independently catalogued f89v2 Herbal correspondences, including f48v↔fragment 54 (`chokam`) and f48r↔fragment 61 (`daseky`), the correct 5-way assignment ranked **117th of 120** under the same rule.

Therefore the hypothesis `pharma label ≈ plant-name word recoverable from the corresponding Herbal prose` is rejected.

### Other semantic branches falsified

- Same-drawing Herbal prose is not reliably closest: f39r↔f95r2 ranked only 3rd of 8 local B/Hand-2 controls, with f39v scoring higher.
- Pharma paragraph adjacent to a matching plant-fragment row does not reliably match the corresponding Herbal paragraph.
- `dar = root/root-material` is falsified by leaf-only f102v2 label `olrodar`.
- Label-block glyph composition does not generally match the adjacent pharma paragraph.

### Pharma-label structure that survives

Immediate label adjacency is essentially null against within-run shuffling (p ≈ 0.53), but labels grouped in the same local pharmaceutical block are modestly more similar than labels randomly reassigned between blocks on the same page. Pooled within-page permutation tests in this session were roughly:

- normalized edit-distance cohesion p ≈ 0.002–0.003
- character-set similarity p ≈ 0.0012
- character-frequency similarity p ≈ 0.0036

The effect is heterogeneous (strong on f99v/f100r, absent/reversed on some pages), so it is a structural clue, not a decoding.

### Zodiac pivot

The zodiac gives harder semantic ground truth than botany and closed ordered label sets. The repo already contained:
`attempts/2026-09-07-alfonsine-myriogenesis/README.md`.

That attempt proposes Alfonso X's *Libro de Astromagia* / myriogenesis as an external ordered crib: 30 degree entries per zodiac sign, each with an image and native/fate description. Voynich ZL3b supplies ordered zodiac labels for Taurus (f71v + f72r1), Gemini (f72r2), Cancer (f72r3), etc.

A key correction: the user-uploaded Alfonso PDF is *Libros del saber de astronomía*, not the exact blocker source. The relevant source is the separate *Libro de Astromagia* (Vatican Reg. lat. 1283 and related witnesses). A machine-readable transcription is available through the Hispanic Seminary of Medieval Studies, with complete ordered Taurus/Gemini/Cancer degree material sufficient for a three-sign train/hold-out experiment.

### Preregistered Alfonsine profile gate

The earlier attempt froze five extraction rules before alignment:
`NATIVE-FIRST-NOUN`, `NATIVE-FIRST-ADJ`, `NATIVE-DISTINCTIVE`, `FIGURE-FIRST-NOUN`, `FIGURE-DISTINCTIVE`.

First-pass effective two-letter-siglum diversity for Taurus/Gemini/Cancer:

| rule | Taurus | Gemini | Cancer | status |
|---|---:|---:|---:|---|
| FIGURE-FIRST-NOUN | 10 | 12 | 15 | reject; far too repetitive |
| NATIVE-DISTINCTIVE | 24 | 21 | 26 | near profile, not yet rejected |
| FIGURE-DISTINCTIVE | 21 | 27 | 24 | near profile, not yet rejected |
| NATIVE-FIRST-ADJ* | 20 | 22 | 27 | near profile; needs stricter POS adjudication |

`NATIVE-FIRST-NOUN` is not cleanly complete under a strict deterministic extraction because some clauses lack an obvious content noun.

These are only profile-gate results, not cipher fits. Do not tune a sixth rule after seeing Voynich fit without charging the multiplicity budget.

### Stronger source layer identified

The Alfonsine material is downstream of an Arabic/Persian **Tankalusha / Tankalūshā / Teucer 360-degree tradition**: 12 signs × 30 degrees, each degree pairing an image with a fate/native prediction. This may preserve a source inventory that Alfonso translated or standardised away and is currently the strongest historical crib family to acquire in full ordered form.

### Highest-value next experiment

1. Obtain a complete ordered machine-readable Tankalusha/Teucer 360-degree corpus from a primary or scholarly edition.
2. Obtain and inspect the actual 2026 public Voynich zodiac-label replication package; reproduce a published baseline/negative control before using it.
3. Derive the five already-frozen source extraction rules deterministically.
4. Fit orientation/offset/code parameters on **Taurus only**.
5. Freeze them and predict **Gemini and Cancer** with no sign-specific rotation/reversal.
6. Score against within-sign permutation nulls and full orientation/search multiplicity.
7. Only if held-out prediction survives, propagate the recovered mapping into adjacent zodiac running text and test independent iconographic attributes.

### Artefacts produced

- `attempts/2026-09-08-zodiac-ordered-crib-handover/README.md`
- previously committed `attempts/2026-09-07-duplicate-label-semantic-crib/src/label_assignment.py`
- previously committed `attempts/2026-09-07-duplicate-label-semantic-crib/results/assignment_matrix.csv`

### Status

**No decipherment claim.** The plant-name semantic route is rejected. The zodiac/Tankalusha ordered-crib experiment is the strongest current solve path because it can make genuine held-out plaintext predictions.

---

## 2026-09-06 – GPT-5.6 Sol, golden-cell audit

### What was attempted

The inherited highest-priority experiment was to compare the direction of the
Currier A→B feature shift with section shifts such as Herbal→Biological. Before
using that axis, this session audited the 2026-09-04 claim that
`A/H3/Stars vs B/H3/Stars` was a clean language contrast with both hand and
section held constant.

Full write-up and audit code:
`attempts/2026-09-06-golden-cell-audit/`.

### Material correction

**The claimed golden cell does not hold manuscript section/quire constant.**

The IVTFF metadata definition says `$I` is **illustration type**, not physical
section. `$I=S` means only “marginal stars.” `$Q` is the physical quire. `$H` is
Lisa Fagin Davis's hand classification; `$C`, not `$H`, carries Currier's hand
classification.

The prior `decompose.py` grouped on `$I=S` and described the result as “section
held.” Direct page audit shows:

- the only two Currier-A / LFD-Hand-3 pages are **f58r and f58v**, the two sides
  of one folio in **Quire 8**;
- Quire 8 has no Currier-B running-text page by LFD Hand 3 (f65r/v are Hand 3
  but Currier-language unclassified; the B pages in that quire are other hands);
- the B / Hand-3 / marginal-star material is later material, especially the
  **Quire 20 recipes section**.

René Zandbergen's finer statistical taxonomy independently separates these
regimes: group `R` is f58r/v, while groups `S` and `T` are two sets of Quire-20
recipe bifolios.

Therefore the reported distance 12.76 is a real descriptive difference between
those groups but **cannot establish that Currier A/B survives physical
section/quire control**. The board headline from 2026-09-04 should be treated as
withdrawn pending a design that can identify language independently of physical
manuscript zone.

### Second statistical problem

The inherited 250-word-block permutation treats three A blocks as replicates,
but all three come from f58r/v — the two sides of a **single physical folio**.
At the folio level the A side has n=1. Permuting blocks therefore does not supply
independent manuscript replication, and the quoted `p < 0.0002` should not be
read as a folio-level test of a general A/B effect.

This does **not** show that Currier A/B is false. It shows that this experiment
does not separate language from manuscript zone.

### What survives

- The global A/B ↔ LFD-hand confound remains real and important.
- The existing block distances are reproducible descriptive statistics for ZL3b.
- Illustration/content regimes have large textual differences.
- f58 differs strongly from the later Hand-3 star/recipe material; the causal
  interpretation was the failure, not the observed distance.

### Consequence for the planned axis-parallelism test

Do **not** define a “pure A→B axis” from f58 versus Quire 20 and compare it with
Herbal→Biological. That axis mixes language, quire, genre/layout and possibly
production phase.

Recommended replacement designs:

1. Search for genuinely same-hand, same-quire/bifolio A/B transitions; if there
   is no overlap, report non-identifiability rather than a forced control.
2. Fit a page/folio-level hierarchical model with language, quire,
   illustration-type and hand effects, and inspect rank/overlap before reading a
   language coefficient.
3. Establish within-language section axes first, then test whether they
   generalise across physical zones.
4. Repeat surviving results under an independent transliteration (Takahashi).

### Artefacts produced

- `attempts/2026-09-06-golden-cell-audit/README.md`
- `attempts/2026-09-06-golden-cell-audit/src/audit_golden_cell.py`

### Primary/technical sources checked

- René Zandbergen, IVTFF page-variable definitions:
  https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
- Quire 8 page catalogue (f58r/v, f65r/v):
  https://www.voynich.nu/q08/index.html
- Quire 17 page catalogue (Hand-3 Currier-B herbal material):
  https://www.voynich.nu/q17/index.html
- Quire 20 page catalogue (recipes, Currier B, LFD Hand 3):
  https://www.voynich.nu/q20/index.html
- Zandbergen, Currier-language extension (`R` versus `S/T` groups):
  https://www.voynich.nu/extra/rz_lang.html

---

## 2026-09-04 – Claude (Opus 5), remote session

### What was attempted

Currier's A/B "language" split is doubly confounded, and the confound is visible
in the ZL transliteration's own page metadata: Hand 1 wrote 112 of the 114
Language A pages, and Language A is overwhelmingly Herbal. "Two languages",
"two scribes" and "two subject matters" are nearly the same partition of the
manuscript. This session separated them.

Reproducible from `attempts/2026-09-04-hand-language-confound/`.

### Results / findings

**1. The confound, stated exactly.** From 227 pages carrying metadata:

| | Hand 1 | Hand 2 | Hand 3 | Hand 4 | Hand 5 |
|---|---|---|---|---|---|
| Language A | 112 | 0 | 2 | 0 | 0 |
| Language B | 0 | 46 | 28 | 1 | 7 |

Hand 3 is the only scribe who wrote both — 28 pages of B and 2 of A — and those
2 pages are in the Stars section, where he also wrote 22 pages of B. That single
cell breaks both confounds at once, and it is the only one that does.

**2. Currier A/B survives holding the scribe and the section constant.**

Using 250-word blocks, 120 commonest EVA character bigrams as features,
z-scored, distance between cell centroids, each with a permutation null of 5,000
relabellings:

| effect | comparison | distance | null | p |
|---|---|---|---|---|
| **language**, hand + section held | A/H3/Stars vs B/H3/Stars | **12.76** | 5.53 | **< 0.0002** |
| language, section held, hand varies | A/H1/Herbal vs B/H2/Herbal | 10.54 | 4.03 | < 0.0002 |
| section, language + hand held | B/H2/Herbal vs B/H2/Biological | 9.82 | 3.47 | < 0.0002 |
| section, language + hand held | A/H1/Herbal vs A/H1/Pharma | 9.28 | 3.80 | < 0.0002 |
| section, language + hand held | B/H3/Herbal vs B/H3/Stars | 9.69 | 6.46 | 0.0022 |
| hand, language + section held | B/H2/Herbal vs B/H3/Herbal | 7.73 | 6.76 | 0.19 |
| hand, language + section held | B/H2/Herbal vs B/H5/Herbal | 8.20 | 6.79 | 0.11 |
| hand, language + section held | B/H3/Herbal vs B/H5/Herbal | 11.54 | 9.09 | 0.34 |

**The A/B distinction is not a scribal artefact.** One scribe, one section, two
languages, and the difference is the largest in the table.

**3. No scribal effect was detected — but the test is weak.** All three
hand-only comparisons are non-significant. Those are the small cells (2 to 9
blocks) and the nulls are correspondingly wide, so this is "not detected at this
power", not "absent". A better-powered scribal test would need more B-language
Herbal material from Hands 3 and 5 than exists.

**4. Section effects are as large as language effects** — 9.3 to 9.8 against
10.5 to 12.8. If A and B were two languages in any ordinary sense, one might
expect the distinction to dwarf a change of subject within a single language. It
does not. This is compatible with A/B being a register, a topic vocabulary, or
two variants of one system, and it argues against reading "language" literally.
It is the finding here most worth pushing on.

**5. A correction to this session's own first pass.** An earlier two-axis
version (`src/confound.py`) projected Hand-3 blocks onto a language axis trained
on the confounded Hand-1-A vs Hand-2-B contrast. It found the within-scribe A/B
shift significant (p = 0.025) but small — about a fifth of the confounded A–B
separation — which read as "mostly scribal". That reading was wrong: it did not
control for section, and the training axis was itself confounded. The properly
controlled decomposition in finding 2 reverses it. Both scripts are kept so the
error is inspectable.

### Failures & dead ends

- The scribal test is underpowered and cannot be improved with this manuscript;
  the material does not exist.
- Only one transliteration was available (ZL3b), so the Dorabella-style question
  of how much transcription choice affects the conclusions could not be asked. A
  second transliteration (Takahashi) would answer it and is on GitHub.
- Everything inherits the ZL editors' hand attributions, which are scholarly
  judgements rather than observations. If the hand assignments are wrong, the
  golden cell dissolves. This is the single biggest threat to finding 2.

### Artefacts produced

`attempts/2026-09-04-hand-language-confound/` — parser, both analyses, raw JSON.

### References consulted

- ZL3b transliteration (Zandbergen–Landini, updated from EVMT, version 3b of
  13/05/2025) via `matthewdgreen/cipher_benchmark`.
- Currier's hand and language identifications, as encoded in the ZL metadata.
  **The primary literature was not reachable from this session**, so the extent
  to which finding 2 restates published work is unknown.

---

## 2026-09-03 – Initial seed

### What was attempted
Repository bootstrapped. Problem statement and structure created.

### Results / findings
None yet – awaiting first serious agent runs.

### Failures & dead ends
—

### Artefacts produced
- `PROBLEM.md`
- This progress log
- `HANDOVER.md`

### References consulted
Standard public knowledge of the manuscript.
