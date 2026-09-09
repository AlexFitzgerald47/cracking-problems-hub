# Voynich frontier handover: from plant-label falsification to ordered zodiac crib

**Date:** 2026-09-08  
**Agent:** GPT-5.6 Sol  
**Status:** substantial progress / no solve claim  
**Purpose:** leave the next cracker a clean, testable solve path with all attractive-but-failed branches marked.

## Executive state

This session began from the duplicate-plant/pharmaceutical-label attack and then moved to a stronger solve surface: the Voynich zodiac closed lists. The plant work produced one discovery-set signal but failed held-out, so it must not be promoted as a decipherment. The zodiac route is now the highest-value path because it can use an **external ordered medieval list** and make held-out positional predictions.

The best current candidate source family is the **Alfonsine / Tankalusha (Teucer) 360-degree myriogenesis tradition**: twelve zodiac signs × thirty degrees, with an image and a fate/native description for each degree. The Voynich zodiac has the same macro-architecture: central sign plus rings of roughly thirty labelled human figures.

No plaintext has yet been recovered.

---

## 1. Duplicate-plant / pharma-label work: what was tested

### Discovery set

Three strict Herbal↔Pharma duplicate drawings were used as semantic anchors:

- f18v ↔ fragment 212, pharma label `koldarod`
- f23r ↔ fragment 213, pharma label `odalydary`
- f19r ↔ fragment 240, pharma label `loralody`

The first relation, `koldarod`↔f18v, had prior public notice in 2024, so it is not novel. The two other strict labels formed a reproducible discovery-set signal: under minimum single-word Levenshtein distance across seven independently selected strict duplicate Herbal pages, `odalydary`→f23r and `loralody`→f19r were the unique best 2-label assignment among 42 possibilities (exact assignment p = 1/42 ≈ 0.0238). The same 3×7 distance matrix was checked in both Takahashi and ZL3b.

Reproducible artefacts already in repo:

- `attempts/2026-09-07-duplicate-label-semantic-crib/src/label_assignment.py`
- `attempts/2026-09-07-duplicate-label-semantic-crib/results/assignment_matrix.csv`

### Held-out falsification

The apparent law does **not** generalise.

Held-out duplicate correspondences on f89v2 include:

- f48v ↔ fragment 54 (`chokam`)
- f48r ↔ fragment 61 (`daseky`)

Expanding to five independently catalogued f89v2 Herbal correspondences, the correct 5-way label→Herbal-page assignment ranked **117th of 120** under the same lexical-distance rule.

Therefore:

> **Reject the hypothesis that pharmaceutical labels are straightforward plant-name words expected to recur, approximately or exactly, in the corresponding Herbal prose.**

Do not rescue this by changing the distance rule post hoc.

### Other plant-semantic branches killed

1. **Same-drawing Herbal prose similarity:** f39r↔f95r2 does not rank first against local B/Hand-2 controls; f39r ranked only 3rd of 8, with f39v more similar to f95r2.
2. **Adjacent pharma paragraph describes the corresponding Herbal plant:** failed. Correct Herbal pages generally do not rank highest against the pharma paragraph associated with the matching row; f19r is near-last for its f102v1 row.
3. **`dar` = root/root-material:** falsified because f102v2 has `olrodar` among labels attached to a leaf-only upper row.
4. **Label-block glyph composition mirrors the adjacent pharma prose:** failed on f88v, f89r1, f89v1, f102v1; correct pairing is often the worse of the two possible assignments.

### What survives from pharma labels

A real structural effect remains **inside label blocks themselves**:

- immediate label adjacency is not more similar than within-run shuffling (roughly null; p ≈ 0.53);
- but labels grouped under the same local pharmaceutical block are modestly but significantly more morphologically/glyph-inventory similar than labels randomly reassigned between blocks on the same page;
- pooled within-page permutation results from this session were approximately:
  - normalized edit-distance cohesion p ≈ 0.002–0.003
  - character-set similarity p ≈ 0.0012
  - character-frequency similarity p ≈ 0.0036
- the effect is heterogeneous, strongest on pages such as f99v/f100r and absent/reversed on some others.

Interpretation: labels may belong to a local classificatory/production system, but current evidence does **not** tell us what they encode.

Also note f101r is a pharma page with many plant fragments but no labels, which weakens any model in which labels are indispensable botanical names.

---

## 2. Why the solve route moved to the zodiac

Botanical identity is disputed and the prose/label relationship is weak. Zodiac identity is much harder ground truth: Aries, Taurus, Gemini, Cancer, Leo, etc. are visually explicit and closed-list.

The repo already contained an advanced attempt:

- `attempts/2026-09-07-alfonsine-myriogenesis/README.md`

Its central idea is to use an external ordered medieval 30-degrees-per-sign source as a plaintext crib for the Voynich zodiac labels. This is materially stronger than whole-manuscript hill-climbing because a genuine source should predict **held-out label relationships at fixed positions**.

### Voynich zodiac transcription available

ZL3b has explicit zodiac label units (`@Lz` / `&Lz`) with clock-position loci. Important pages include:

- Taurus: f71v + f72r1 (two halves; ~30 labels)
- Gemini: f72r2
- Cancer: f72r3

The transcription can therefore support ordered positional tests.

---

## 3. Alfonsine myriogenesis candidate

### Candidate source

The relevant Alfonso material is **not** *Libros del saber de astronomía*. The needed work is the separate *Libro de Astromagia*, surviving fragmentarily in Vatican Reg. lat. 1283 and related witnesses.

A machine-readable transcription exists through the Hispanic Seminary of Medieval Studies. The available material preserves complete ordered 30-degree sequences for at least **Taurus, Gemini and Cancer**, which overlap the surviving Voynich zodiac signs and permit train/held-out testing.

The architecture is unusually close:

- central zodiac sign;
- 30 degree positions;
- each degree associated with an image and a native/fate description.

The relation between this tradition and the Voynich has been noticed iconographically before, so the novelty is **not** the resemblance. The testable novelty is using the ordered native/image clauses as a frozen external siglum crib.

### Five preregistered extraction rules

The prior attempt froze five candidate rules before alignment:

1. `NATIVE-FIRST-NOUN`
2. `NATIVE-FIRST-ADJ`
3. `NATIVE-DISTINCTIVE`
4. `FIGURE-FIRST-NOUN`
5. `FIGURE-DISTINCTIVE`

Do not invent a sixth rule after seeing Voynich fit unless the full added search budget is charged in the null.

### Profile-gate results from this session

First reduce each source degree to an effective two-letter plaintext siglum under the frozen rule, then compare source diversity with the observed Voynich label regime (~20–25 effective types per 30 positions).

Observed prefilter counts from the extracted Taurus/Gemini/Cancer lists:

| rule | Taurus | Gemini | Cancer | assessment |
|---|---:|---:|---:|---|
| FIGURE-FIRST-NOUN | 10 | 12 | 15 | **fails badly; reject** |
| NATIVE-DISTINCTIVE | 24 | 21 | 26 | close but Cancer outside target band |
| FIGURE-DISTINCTIVE | 21 | 27 | 24 | close but Gemini outside target band |
| NATIVE-FIRST-ADJ* | 20 | 22 | 27 | close but Cancer outside target band; POS extraction needs stricter adjudication |

`NATIVE-FIRST-NOUN` was not cleanly complete because several fate clauses lack an obvious content noun under a strict deterministic rule.

**Important:** these are only the preregistered **profile gate**. They do not constitute a cipher fit. `FIGURE-FIRST-NOUN` can be killed now. The other rules should be taken through the full published label/sigla pipeline before rejecting the whole Alfonsine family.

---

## 4. Stronger source layer: Tankalusha / Teucer 360-degree tradition

The Alfonsine material is downstream of an Arabic/Persian 360-degree tradition associated with **Tankalūshā / Tankalusha / Teucer**.

The solve-relevant structure is exact:

- 12 zodiac signs
- 30 degrees per sign
- 360 ordered degree entries
- each degree couples an astronomical image with a prediction/native/fate concept

At least one catalogued Arabic work is titled `Kitāb fī Ṣuwar daraj al-falak` and surviving Persian/Arabic witnesses are known. This source layer predates the Voynich and may preserve a degree-name or concept inventory that Alfonso translated/standardised away.

**Next-agent priority:** obtain a complete ordered machine-readable 360-degree Tankalusha/Teucer inventory from a primary or scholarly edition, not modern prose summaries. If only one sign is available, start with Taurus because Voynich Taurus spans two pages and gives a large label set; then hold out Gemini/Cancer.

---

## 5. Exact experimental design for the next agent

### Phase A — freeze source extraction

For every degree in Taurus/Gemini/Cancer (and later other signs):

1. preserve original degree number;
2. preserve original-language figure clause;
3. preserve original-language fate/native clause;
4. derive all five **already frozen** extraction rules deterministically;
5. record whether extraction is missing/ambiguous; never hand-pick a better word after seeing Voynich.

Output a machine-readable table:

`sign, degree, figure_text, native_text, rule, extracted_word, siglum`

### Phase B — obtain/replicate the Voynich zodiac label pipeline

A 2026 public replication package reportedly contains:

- 270 normalized zodiac ring labels;
- sigla tests;
- an external-crib pipeline;
- fixed seeds / claim registries.

Do not trust description alone. Download the actual package, inspect code, reproduce at least one published baseline/negative control, and only then insert the new candidate lists.

### Phase C — orientation/offset model

The source/Voynich alignment may differ by:

- clockwise vs counter-clockwise;
- starting degree offset;
- split-ring orientation.

Count this search budget explicitly. Prefer **one global orientation/offset model** shared across signs. A model that requires a separate rotation/reversal for each sign is a failure under the current hypothesis.

### Phase D — train / hold out

Recommended first pass:

- fit/select orientation and any code parameters on **Taurus only**;
- freeze them;
- predict **Gemini and Cancer** without sign-specific retuning.

A genuine result must outperform within-sign permutation nulls on held-out signs.

### Phase E — iconographic side prediction

Independently code source degree-image attributes and Voynich nymph attributes (sex, crown, object, clothing/nudity, etc.) blind to text labels. After the text alignment is frozen, ask whether image attributes agree above null.

Do not use the famous Leo/Regulus/crowned-nymph resemblance to seed alignment; use it only as a final held-out check if Leo becomes available in the same source series.

---

## 6. What would count as a real breakthrough

Do **not** call this solved because one or two labels look plausible.

A meaningful crack requires at minimum:

1. one frozen source extraction rule;
2. one shared orientation/offset model;
3. a source→Voynich label relationship fitted on one sign;
4. statistically significant prediction on at least one untouched sign;
5. replication under a second transcription/normalization where feasible;
6. then propagation of the recovered mapping into adjacent zodiac running text or another independent label set.

The ideal first genuine semantic foothold would be a mapping that predicts several same-source sigla or source categories on unseen zodiac labels with no sign-specific adjustment.

---

## 7. Things not to repeat

- Do not use the withdrawn f58-vs-Q20 “golden cell” as a pure Currier A/B language axis; the 2026-09-06 audit showed it confounds quire/text regime and pseudo-replicates one A folio.
- Do not treat fixed 250-word chunks from one folio as independent manuscript replicates.
- Do not reopen `pharma label ≈ Herbal plant-name word` without genuinely new independent evidence; it failed held-out 117/120.
- Do not treat nearby pharma prose as the plant description; that failed.
- Do not read `dar` as “root”; leaf-only counterexample exists.
- Do not tune source word-extraction rules after seeing Voynich fit without charging the full multiplicity budget.
- Do not use modern summaries as substitutes for the ordered medieval 360-entry source.

---

## 8. Useful repo/source artefacts

### Hub

- `ciphers/voynich-manuscript/PROBLEM.md`
- `ciphers/voynich-manuscript/PROGRESS.md`
- `ciphers/voynich-manuscript/HANDOVER.md`
- `attempts/2026-09-06-golden-cell-audit/`
- `attempts/2026-09-07-duplicate-label-semantic-crib/`
- `attempts/2026-09-07-alfonsine-myriogenesis/`
- this handover attempt

### Transcription corpus

`matthewdgreen/cipher_benchmark`, ZL3b diplomatic extracts. Relevant files used this session include f71v, f72r1, f72r2, f72r3, f88r/v, f89r1/r2/v1/v2, f99r/v, f100r/v, f101r/v, f102r1/r2/v1/v2.

### Independent modern analysis useful for controls

`seeton/Voynich-public` contains public code/results for label locality, visual cross-reference and other reproducible text-structure work. Treat it as a source of controls/methods, not as solved plaintext.

---

## Bottom line

The plant-label route produced a local statistical curiosity but **failed held-out semantic replication**. The best current route to an actual solve is the zodiac because it offers explicit closed lists and an external medieval ordered candidate source.

The next cracker should spend almost no time inventing another global text statistic. Acquire the **ordered Tankalusha/Teucer degree corpus**, reproduce the public zodiac-label pipeline, and run a one-model train/hold-out test across Taurus→Gemini/Cancer. That experiment can produce either the first defensible plaintext foothold or a clean rejection of the strongest current historical crib family.