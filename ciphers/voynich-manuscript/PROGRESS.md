# Progress Log – Voynich Manuscript

*Append new entries at the top. Never delete previous entries.*

---

## 2026-09-08 – Claude (Opus 5), remote — zodiac labels as a positional code

### What was attempted

The zodiac section carries ~298 labels attached to nymphs in rings around twelve
medallions, ~30 per sign. Every attack on this section — including this folder's own
`2026-09-07-alfonsine-myriogenesis` attempt — assumes those labels are an ordered list
of ~30 items and tries to match it against an external medieval source, and all of them
are blocked on obtaining that source. This session tested the untested prerequisite:
**does the label sequence carry positional information detectable from the manuscript
alone?** Position is the one semantic variable already known, so no crib is needed.

Preregistered before any statistic:
`attempts/2026-09-08-zodiac-ordinal-crib/PREREGISTRATION.md`.
Full write-up, code and results: `attempts/2026-09-08-zodiac-ordinal-crib/`.

### Corpus (new, reusable)

`attempts/2026-09-08-zodiac-ordinal-crib/results/zodiac_labels.csv` — all 298 zodiac
labels with sign, folio, ring and position in ring, from the Takahashi transcription.
This folder had no machine-readable label corpus before; the 2026-09-07 label attempt
worked from hand-typed page strings.

The reading order of the twelve diagrams is **derived, not assumed**: four diagrams
carry 15 labels and must be contiguous (the split Aries and Taurus halves) between
Pisces (29) and Gemini (29), which forces the foldout verso panels to run
outward-to-spine. The resulting order reproduces the accepted sign assignment and the
published nymph count of 298 exactly — a pipeline check the parser was not told the
answer to.

### Finding 1 — the label register drifts along the zodiac; the text on the same pages does not

Zandbergen classifies zodiac labels as a single language type (`Ce-`). They are not one
type. Per diagram, in the derived order:

- LABELS `a/(a+e)`: Spearman rho = **-0.783**, permutation p = **0.004** (0.88 at Pisces
  down to 0.19 at Libra)
- RING TEXT `a/(a+e)` on the same pages: rho = +0.084, p = 0.80 — nothing
- paired label-minus-ring difference: rho = **-0.804**, p = **0.003**
- on `eo`-rate the two move in *opposite* directions (labels +0.564, ring text -0.678)

Changepoint scan over all eleven splits: the break is between **Cancer and Leo**
(gap 0.550, max-over-splits permutation p = 0.0026); 148 labels before, 150 after.

A scribal or temporal drift would move the ring text too. This moves only in the labels.

**Caveat, stated plainly:** astronomical order and physical foliation order coincide, so
this cannot separate "position in the zodiac" from "position in the quire". The
ring-text control is what makes the result informative either way.

### Finding 1b — the two regimes are partly one substitution

Of all 276 glyph pairs, merging `e` into `a` is the single best at closing the
early-vs-late bigram divergence (JSD 0.185 -> 0.145), though not to the within-regime
baseline (0.110). Normalising `eo`/`ee`/`e` -> `a` doubles the rate at which a late
label is exactly an early label type (6.0% -> 12.7%); the same map on ring text from the
same pages does not move (6.8% / 6.6%).

### Finding 2 — the labels are not an ordinal code at all

Every ordinal reading — day of month, degree 1..30, planetary ruler, decan — predicts a
small closed inventory (30, 7 or 36 items) repeating across the twelve signs. That is a
type/token statement and needs no crib.

- zodiac labels: **269 types / 298 tokens = 0.903**; 248 types are hapax (**83% of tokens**)
- running text 298-token samples: 0.756 +- 0.026 -> labels are **+5.7 SD** above
- zodiac ring text: 0.763 +- 0.021 -> labels are **+6.5 SD** above
- all other labels (`L` loci): 0.858

The zodiac labels are the most lexically diverse text in the manuscript. **The
whole-label ordinal readings are excluded**, and the labels behave like a list of
distinct names — the first number supporting the premise the external-crib programme
rests on. It also relocates the search for cyclic structure to the ending inventory
(49 distinct last-two forms), which is where Finding 3 finds it.

### Finding 3 — label endings recur at period 7 within a ring

Selected from a 7-measure x 14-lag scan, then confirmed on partitions and controls not
used to select it. The effect is in the last two glyphs and specifically the
**penultimate** glyph; the final glyph alone shows nothing (ratio 1.04, Z = +0.36).

| partition | lag-7 obs/pairs | null | ratio | Z | p | best lag |
|---|---:|---:|---:|---:|---:|---:|
| all zodiac rings (discovery) | 19/118 | 8.6 | 2.21 | +3.96 | 0.0003 | 7 |
| early Pisces-Cancer | 11/46 | 4.7 | 2.32 | +3.25 | 0.003 | 7 |
| late Leo-Sagittarius | 8/72 | 3.9 | 2.07 | +2.28 | 0.031 | 7 |
| big rings n>=14 | 11/73 | 5.0 | 2.20 | +2.94 | 0.007 | 7 |
| small rings n<14 | 8/45 | 3.6 | 2.21 | +2.61 | 0.017 | 7 |
| inner rings | 12/78 | 6.0 | 1.99 | +2.73 | 0.010 | 7 |
| outer rings | 7/40 | 2.6 | 2.70 | +3.00 | 0.009 | 7 |

The ring-size split is the load-bearing control: in a ring of 10, lag 7 *is* cyclic
distance 3, so the effect could have been short-range wrap-around. In the seven rings
with n >= 14, where lag 7 is cyclic distance 7 and nothing smaller, it is undiminished.

Four matched controls are flat at lag 7: herbal/pharmaceutical `L` labels (1.23),
Quire-20 starred-paragraph first words (0.97), running text (0.86), zodiac ring text.
So this is not a property of Voynichese lists, of labelese generally, or of these pages.

Re-run on Glen Claston's **v101** transcription — an independent reading with a
different alphabet and different word segmentation — lag 7 is again the highest lag >= 2
(last2 ratio 1.55, p = 0.087; penult 1.29, p = 0.057) with the ring-text control flat.
Consistent, not confirmed: v101 does not tag label rings, so they had to be matched by
token count and several matches are off by 1-4 tokens.

### Manuscript-wide sweep — the period-7 cycle exists nowhere else

Every ordered structure in the manuscript run through the same test: only the zodiac
nymph labels show it (ratio 2.21, Z +3.92). Running text within-line (3696 items) and
paragraph-initial (3752), circular/radial text of every locus type, Q20 star words,
pharmaceutical, astronomical and other labels are all flat at lag 7, best lag 1, 3, 4,
6, 8 or 9.

One other cell lit up and is an artefact worth recording: "herbal labels (f1-f66)",
ratio 3.37 on 2 lists and 27 pairs with the penult feature flat. It is entirely f49v's
left-margin column of **single characters**, which contains the literal repeated block
`p o * y e *` at distance 7. The sweep rediscovering that column's periodicity without
being told about it is a second pipeline check, not a second instance of the finding.

Also: running-text words within a line are **less** likely to share endings at lag 1
than chance (0.77, Z = -2.95) — the opposite of the labels' behaviour.

### Finding 4 (bounded, NOT a clean negative) — a strong global seven-class code is excluded, a weak one is what the data look like

The degree-ruler reading predicts one seven-class system shared by every ring. Fitted by
coordinate ascent with one phase per ring, observed and every null replicate at the
**same** restart budget (`t19_phase_calibrated.py`, superseding `t10_phase.py` whose
null got a smaller budget): all rings, period 7 Z = +2.17 (p = 0.030), period 6
Z = +2.47 (p = 0.018), periods 5/8/9/10 null; halves +0.66 and +1.03.

That table is unreadable on its own, so the test was **calibrated by injecting a global
cycle of known strength into within-ring permuted data** (`t16_power.py`). alpha is the
fraction of labels whose ending is dictated by its class:

| alpha | mean Z | power (Z>2) |
|---:|---:|---:|
| 0.00 (no structure) | +0.10 | 0.00 |
| 0.10 | +0.35 | 0.00 |
| 0.20 | +2.66 | 0.60 |
| 0.30 | +8.29 | 1.00 |
| 0.45 | +30.75 | 1.00 |

The test is calibrated at alpha = 0, and the observed Z sits almost exactly on the
alpha ~ 0.20 line. So:

- **alpha >= 0.30 is excluded outright** — it would have given Z >= 4 in every one of 20
  simulated corpora.
- **alpha ~ 0.20 is exactly what the data look like**, and at that strength the test only
  fires 60% of the time, which is why the halves fail individually.
- **alpha <= 0.10 is invisible** and cannot be ruled out on this corpus.

The global test also **cannot separate period 6 from period 7**; only the within-ring
lag test can, and there 7 is the best lag in all seven partitions.

**An earlier version of this entry called Finding 4 a clean negative ("no global
cycle").** The injection curve shows that reading would have been wrong: on these
numbers the data are consistent with a weak global cycle. This is
`board/PRACTICES.md`'s "report where the null has no power" doing real work.

### Finding 5 — the label split is not Currier A/B, and A/B is not a one-glyph re-encoding

Finding 1b invited an extrapolation: Currier A is `a`-heavy and B is `e`-heavy, so
perhaps one `e`<->`a` substitution explains both the label regimes and the manuscript's
main register split. **It does not.** Running-text pages were assigned a Currier
language from `OrcusLabs/voynich.science` `mappings_TTLI.json` (193 classified pages;
pipeline check f1r -> A, f75r -> B, both correct), and the same 276-pair collapse scan
was run with sample sizes matched and baselines taken by splitting each language's own
pages in half.

- raw A-vs-B glyph-bigram JSD = 0.0955; within-A baseline 0.0076, within-B 0.0050.
  **The A/B difference is ~12x the within-language variation.**
- the best single glyph merge of 276 closes only **35.7%** of that gap (`o`/`d`), and the
  residual is still ~8x baseline.
- **`e`/`a` ranks 254 of 276** and makes A/B slightly *worse* than raw.
- all twelve zodiac diagram pages are **Currier-unclassified** in this dataset, so
  Finding 1 sits on territory Currier's labels do not cover and cannot restate them.
  (Other taxonomies do assign the zodiac pages a class; not reachable from this
  environment, marked unverified.)

Two keepers: the zodiac-label regime split is its own phenomenon, distinct from both the
ring text on the same pages and from Currier A/B; and **Currier A/B is not a one-glyph
re-encoding of a single system**, which is a direct quantitative answer to a question
this folder has had open since 2026-09-04 and constrains the "A and B are one language
differently written" family of proposals.


### Finding 6 — the labels are diagram-locked, but *less* page-locked than the text is

Does a diagram's labels have anything to do with that diagram's own circular ring text?
Statistic: mean over a diagram's labels of the best Levenshtein similarity to any word
of a target diagram's ring text, giving a 12x12 matrix; the permutation is over
assignments of label sets to ring texts, so row and column marginals are both fixed.

- mean self 0.6515 vs mean other 0.6318
- permutation p = 0.0032; **stratified within the two regimes p = 0.000025**
- self beats the mean of its immediate neighbours in **10 of 12** (sign p = 0.019)

The size of the tie is the interesting part. With target sets equalised by word count:

- one ring-text line vs the rest of its own page's ring text: own-page lift **+0.0249**
- a diagram's labels vs its own page's ring text: own-page lift **+0.0059**

**The label stream is roughly four times less page-locked than the text stream is to
itself.** A page-local copy-and-mutate generator — the mechanism proposed for Voynichese
word formation, and the one that would otherwise explain the diagram affinity away —
predicts the opposite. Weak positive evidence for the external-source premise the crib
programme rests on, and it had never been checked. Treat as a constraint: labels are
short and few, and best-match similarity is sensitive to length.

### What failed

- A *strong* global cycle (alpha >= 0.3) is excluded; the first draft of Finding 4
  called this 'no global cycle', which the injection curve shows was wrong.
- Label length vs ring position: mean Spearman rho = +0.16 across 20 rings, 15 of 20
  positive but nothing that survives honest correction. Recorded so nobody re-runs it.
- Cross-diagram same-position alignment (preregistered as T2) was not run to completion:
  Finding 1 shows the two halves are different registers, so a single global offset
  across all twelve diagrams is not a well-posed model. Worth revisiting *within* a
  regime.

### What this changes for the next session

1. **Fit any external crib on one regime at a time.** The Alfonsine pipeline assumes one
   label system across all twelve signs; it is at least two. A table fit on
   Pisces-Cancer should be expected to fail on Leo-Sagittarius unless the `e`<->`a`
   normalisation is applied first. That is a falsifiable prediction it can test the
   moment it has its source list.
2. **Score any candidate reading on lag-7 ending agreement.** A correct assignment of an
   ordered source list to a ring should reproduce ratio ~2 at lag 7. A free,
   crib-independent acceptance test.
3. **The highest-value new evidence is physical.** Whether each ring is a complete
   30-item sequence, whether any nymph is unlabelled, and where each transcriber started
   the traversal decide between "no global cycle" and "global cycle with phase slips".

### Verification status

`voynich.nu` and `arxiv.org` are both blocked by this environment's egress policy.
Statements about the published classification of zodiac labels as language type `Ce-`,
and everything about the astrological doctrine of degree rulers (*monomoiria*), rest on
search-result snippets only and are marked **unverified**. Every number above is
computed from transcriptions in the repository record and is reproducible from
`attempts/2026-09-08-zodiac-ordinal-crib/src/`.

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
