# Attempt: is Currier's A/B "language" separable from the scribe and the section?

**Date:** 2026-09-04 · **Status:** complete; positive result · **Reproducible:** yes

Currier's division of Voynichese into "Language A" and "Language B" is one of
the few structural facts about the manuscript that nearly everyone accepts. It
is also doubly confounded, and the confound is visible in the transliteration's
own metadata: **Hand 1 wrote 112 of the 114 Language A pages**, and Language A
is overwhelmingly the Herbal section. So "two languages", "two scribes" and
"two subject matters" are three descriptions of almost the same partition.

This attempt separates them.

## Headline

Holding the scribe and the section constant — Hand 3's Stars pages, which he
wrote in *both* languages — the A/B difference is still there and still large:
distance 12.76 against a permutation null of 5.53, p < 0.0002.

**Currier A/B is not a scribal artefact.**

| effect | comparison | distance | null | p |
|---|---|---|---|---|
| **language**, hand + section held | A/H3/Stars vs B/H3/Stars | 12.76 | 5.53 | < 0.0002 |
| language, section held | A/H1/Herbal vs B/H2/Herbal | 10.54 | 4.03 | < 0.0002 |
| section, language + hand held | B/H2/Herbal vs B/H2/Biological | 9.82 | 3.47 | < 0.0002 |
| section, language + hand held | A/H1/Herbal vs A/H1/Pharma | 9.28 | 3.80 | < 0.0002 |
| **hand**, language + section held | B/H2/Herbal vs B/H3/Herbal | 7.73 | 6.76 | 0.19 |
| **hand**, language + section held | B/H2/Herbal vs B/H5/Herbal | 8.20 | 6.79 | 0.11 |
| **hand**, language + section held | B/H3/Herbal vs B/H5/Herbal | 11.54 | 9.09 | 0.34 |

Two further things worth taking from that table:

- **No hand effect was detected** once language and section are held constant.
  But those three cells are the small ones (2–9 blocks), so this is
  "not detected at this power", not "shown to be absent".
- **Section effects are as large as language effects** (9.3–9.8 against
  10.5–12.8). If A and B were two languages, one might expect the distinction to
  dwarf a change of subject matter within one language. It does not. That is
  compatible with A/B being a register, a topic vocabulary, or a variant of one
  system, and it is a caution against reading "language" too literally.

## Method

Unit of analysis is a 250-word block. Features are the relative frequencies of
the 120 commonest EVA character bigrams (word boundaries marked), z-scored
across all blocks — Burrows-style. An effect is the Euclidean distance between
two cells' centroids.

Every distance gets a permutation null: pool the two cells' blocks, relabel at
random preserving group sizes, recompute the centroid distance, 5,000 times.
That is what makes a distance interpretable rather than merely large, and it
handles the small cells correctly, since the null is built at the same split.

```
src/vms.py          parses ZL3b into pages with hand/language/section metadata
src/confound.py     the two-axis version: language axis vs a pure scribal axis
src/decompose.py    the three-way decomposition above
results/            raw JSON
```

## Reproduction

```
pip install numpy
cd src
python confound.py     # ~1 min
python decompose.py    # ~2 min
```

## Data

ZL3b transliteration (Zandbergen–Landini, updated from the EVMT project,
version 3b of 13/05/2025), via `matthewdgreen/cipher_benchmark`
(`benchmark/unsolved/sources/voynich/`). The per-page `$H` (hand), `$L` (Currier
language) and `$I` (illustration/section type) attributes are the ZL editors'
own, and every result here inherits their judgements about hand identification —
which are themselves scholarly interpretations, not observations.
