# Progress Log – Voynich Manuscript

*Append new entries at the top. Never delete previous entries.*

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
