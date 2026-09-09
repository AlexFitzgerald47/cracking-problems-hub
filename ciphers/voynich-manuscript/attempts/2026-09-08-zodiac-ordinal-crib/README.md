# What the Voynich zodiac labels are, from the manuscript alone

**Date:** 2026-09-08
**Session:** Claude (Opus 5), remote
**Status:** five positive findings, one bounded negative, one clean negative. **No decipherment, no reading of any label.**
**Preregistration:** `PREREGISTRATION.md`, written before any statistic was computed.

---

## The model this session arrived at

Everything below is derived from the transcription alone, with no external source list
and no assumed reading. Taken together it is a structural description of the label
system that did not exist before:

> The 298 zodiac nymph labels are **near-unique items** — 83% hapax, the most lexically
> diverse text in the manuscript — so they are a list of *distinct things*, not an
> ordinal code. They are **tied to their own diagram** but *less* bound to their page
> than the ring text is to itself, which is what an externally sourced list looks like
> and not what page-local generation looks like. They are written in **two register
> regimes** that break between Cancer and Leo, differing partly by an `e`↔`a`
> substitution that is *not* the one separating Currier A from B. And while the labels
> themselves do not repeat, their **endings do**, at period 7 within a ring — an effect
> absent from four matched control corpora including the circular text on the same
> pages.

So: a list of distinct externally-sourced names, each carrying a suffix drawn from a
small inventory that cycles with period 7, written in two successive register regimes.
Each clause of that sentence is a number in the sections below, and each is falsifiable.

**What it does for the blocked crib programme.** That programme assumes the labels are
an ordered list of ~30 distinct names per sign and is stuck waiting for a medieval
source to match them against. Finding 2 is the first evidence that its premise is right.
Findings 1 and 5 say it must fit one regime at a time. Finding 3 hands it a free
acceptance test it can run on any candidate alignment before the source arrives.

---

## Why this attempt exists

The zodiac section (f70v2–f73v) carries ~298 short labels attached to nymphs arranged
in rings around twelve zodiac medallions, ~30 per sign. Every serious attack on this
section — including this folder's own `2026-09-07-alfonsine-myriogenesis` attempt, and
the published external-crib programme it responds to — assumes the labels are an
**ordered list of ~30 items per sign** and tries to match that list against an external
medieval source. All of them are blocked on obtaining the external source.

That programme has an untested prerequisite. **If the labels carry positional
information at all, that information is detectable from the manuscript alone**, because
position is the one semantic variable already known. Nobody had checked. This attempt
checks it.

## Data

`results/zodiac_labels.csv` — all **298** zodiac labels with sign, folio, ring, and
position in ring, parsed from the Takahashi transcription
(`alephmembeth/voynich`, `analysis/takahashi_original.txt`). Parser: `src/vmsparse.py`,
`src/labels.py`.

**The reading order of the twelve diagrams is derived, not assumed.** Four diagrams
carry 15 labels and eight carry 29–30. The four 15-label diagrams are the split signs
(two Aries halves, two Taurus halves) and must therefore be *contiguous* and sit between
Pisces (29) and Gemini (29). Only one ordering of the foldout panels satisfies that,
and it is the one in which the verso panels of f70 and f72 run outward-to-spine:

| # | sign | folio | labels |
|---|---|---|---|
| 1 | Pisces | f70v2 | 29 |
| 2 | Aries-1 | f70v1 | 15 |
| 3 | Aries-2 | f71r | 15 |
| 4 | Taurus-1 | f71v | 15 |
| 5 | Taurus-2 | f72r1 | 15 |
| 6 | Gemini | f72r2 | 29 |
| 7 | Cancer | f72r3 | 30 |
| 8 | Leo | f72v3 | 30 |
| 9 | Virgo | f72v2 | 30 |
| 10 | Libra | f72v1 | 30 |
| 11 | Scorpio | f73r | 30 |
| 12 | Sagittarius | f73v | 30 |

The total, 298, matches the published nymph count exactly, and the panel-reversal it
forces agrees with the accepted assignment. This is a pipeline check in the sense of
`board/PRACTICES.md`: the parser recovers a known fact it was not told.

---

## Finding 1 — the label register is not one system; it drifts along the zodiac, and the text on the same pages does not

Zandbergen's classification treats the zodiac labels as a single language type (`Ce-`:
high `eo`, low initial `qo`), distinct from both running text and the pharmaceutical
labels. **They are not one type.** Measured per diagram in the derived order:

| statistic | Spearman rho vs zodiac index | permutation p |
|---|---:|---:|
| **LABELS** `a/(a+e)` | **-0.783** | **0.004** |
| RING TEXT `a/(a+e)`, same pages | +0.084 | 0.800 |
| LABELS `eo`-rate | +0.564 | 0.060 |
| RING TEXT `eo`-rate, same pages | **-0.678** | 0.019 |
| **paired label − ring difference** | **-0.804** | **0.003** |

The labels run from `a`-based (Pisces `a/(a+e)` = 0.88) to `e`/`eo`-based
(Libra 0.19). The circular ring text written on the same pages, by the same hand, does
not move at all on the same statistic — and on `eo` it moves in the *opposite*
direction. The paired test removes any page-level effect and the drift survives it.

A changepoint scan over all eleven possible splits puts the break **between Cancer and
Leo** (gap 0.550, max-over-splits permutation p = 0.0026); i.e. exactly at the
seventh diagram, with 148 labels before and 150 after.

**This is the load-bearing part.** A scribal or temporal drift would move the ring text
too. Something that changes only in the labels, monotonically, along the astronomical
order, is a property of the *label system*, not of the page.

Caveat stated plainly: astronomical order and physical foliation order coincide here, so
this attempt cannot separate "position in the zodiac" from "position in the quire". The
ring-text control is what makes the result informative either way — whatever drifts,
drifts only in the labels.

### Finding 1b — the two regimes are partly, not wholly, one substitution

Collapsing each of the 276 possible glyph pairs in turn and re-measuring the
early-vs-late bigram divergence, **`e`→`a` is the single best of all 276** at closing the
gap (JSD 0.185 → 0.145). It does not close it to the within-regime baseline (0.110), so
this is not a pure key change. Independently: normalising `eo`/`ee`/`e` → `a` roughly
doubles the rate at which a late label is exactly an early label type (6.0% → 12.7%),
while the identical normalisation applied to ring-text words from the same pages does
not move (6.8% late, 6.6% early).

---

## Finding 2 — the labels are not an ordinal code, and this is decidable in one line

Every ordinal reading of the zodiac labels makes the same prediction. Day of month,
degree 1..30, planetary ruler, decan — each is a **small closed inventory repeating
across all twelve signs**: 30, 7, or 36 items for 298 slots. That is a type/token
statement, and it needs no crib and no model.

| corpus | 298-token type/token ratio |
|---|---:|
| **zodiac nymph labels** | **0.903** (269 types / 298 tokens) |
| running text (`P` loci) | 0.756 ± 0.026 — labels are **+5.7 SD** above |
| all other labels (`L` loci) | 0.858 — labels are above |
| zodiac ring text (`R` loci) | 0.763 ± 0.021 — labels are **+6.5 SD** above |

Repeat spectrum across the entire zodiac section: **248 types occur once**, 15 twice, 4
three times, 2 four times. **83% of the labels are hapax.**

An ordinal code would need ≤ 36 types. There are 269, and the labels are the most
lexically diverse text in the manuscript, more diverse than the running text and more
diverse than the manuscript's other labels.

**The whole-label ordinal readings are excluded.** The labels behave like a list of
distinct items — names — which is exactly what the external-crib programme assumes and
had never verified. This is the first number that supports its premise.

It also tells you where to look for cyclic structure: not in the label, but in the
**ending** inventory, which is small (49 distinct last-two-glyph forms for 298 labels).
Finding 3 is that test.

---

## Finding 3 — label endings recur at period 7 within a ring

Selected from a 7-measure × 14-lag scan over all zodiac rings (`src/t8_period.py`), then
confirmed on partitions and controls that were not used to select it
(`src/t12_final.py`). Statistic: pooled count of position pairs *d* apart sharing a
feature, null = permutation of labels within each ring, 40,000 draws.

The effect is in the **last two glyphs**, and specifically the **penultimate** glyph —
the final glyph alone shows nothing (lag-7 ratio 1.04, Z = +0.36).

| partition | rings | lag-7 obs/pairs | null | ratio | Z | p | best lag |
|---|---:|---:|---:|---:|---:|---:|---:|
| all zodiac rings (discovery) | 20 | 19/118 | 8.6 | **2.21** | +3.96 | 0.0003 | 7 |
| early, Pisces–Cancer | 10 | 11/46 | 4.7 | 2.32 | +3.25 | 0.003 | 7 |
| late, Leo–Sagittarius | 10 | 8/72 | 3.9 | 2.07 | +2.28 | 0.031 | 7 |
| big rings n ≥ 14 | 7 | 11/73 | 5.0 | 2.20 | +2.94 | 0.007 | 7 |
| small rings n < 14 | 13 | 8/45 | 3.6 | 2.21 | +2.61 | 0.017 | 7 |
| inner rings | — | 12/78 | 6.0 | 1.99 | +2.73 | 0.010 | 7 |
| outer rings | — | 7/40 | 2.6 | 2.70 | +3.00 | 0.009 | 7 |

Seven partitions, four of them disjoint pairs, all peaking at the same lag.

**The ring-size stratification matters and is not cosmetic.** In a ring of 10 labels,
lag 7 is the same thing as cyclic distance 3, so the whole effect could have been
short-range adjacency wrapping round the ring. It is not: in the seven rings with
n ≥ 14, where lag 7 is cyclic distance 7 and nothing smaller, the effect is undiminished.

### Controls

Four control sequence sets, cut to the same ring-size profile:

| control (matched ring-size profile) | last-2 ratio | Z | penult ratio | Z | best lag |
|---|---:|---:|---:|---:|---:|
| herbal / pharmaceutical `L` labels | 1.23 | +0.68 | 0.83 | -1.12 | 5 |
| Quire-20 starred-paragraph first words | 0.97 | -0.04 | 0.64 | -0.71 | 4 |
| running text (`P` loci) | 0.86 | -0.55 | 1.12 | +0.63 | 8 / 3 |
| **zodiac ring text, same pages** | **1.24** | +0.90 | **1.04** | +0.25 | 5 |

Compare the zodiac labels' 2.21 / 1.69. Full table: `results/t12_final.txt`.

The effect is not a property of Voynichese lists, of the label register generally, or of
the zodiac pages. It is a property of *these* labels in *this* order.

### Manuscript-wide sweep — the effect exists nowhere else

Every ordered structure in the manuscript was cut into lists and run through the same
pooled test (`src/t15_sweep.py`, full table `results/t15_sweep.txt`):

| structure | lists | items | lag-7 last-2 ratio | Z | best lag |
|---|---:|---:|---:|---:|---:|
| **zodiac nymph labels** | 20 | 258 | **2.21** | **+3.92** | **7** |
| running text, paragraph-first words | 182 | 3752 | 0.98 | −0.42 | 1 |
| running text, within-line words | 400 | 3696 | 0.77 | −2.98 | 1 |
| circular / radial text (`R`) | 7 | 135 | 0.55 | −1.14 | 1 |
| Quire-20 starred-paragraph first words | 4 | 73 | 1.42 | +0.96 | 4 |
| circular / radial text (`X`, `Y`, `C`) | 10 | 120 | 0.68–1.05 | <+0.1 | 6–9 |
| pharmaceutical labels (f88–f102) | 4 | 38 | 0.00 | −0.51 | 8 |
| astronomical labels (f67–f73) | 1 | 28 | 0.80 | −0.38 | 4 |
| other labels (f74+) | 4 | 49 | 0.59 | −0.58 | 3 |

The zodiac labels are the only structure in the manuscript that shows it.

**One other cell lit up, and it is an artefact worth recording.** "Herbal labels
(f1–f66)" gave ratio 3.37, Z = +4.01 — on 2 lists and 27 pairs, and with the penult
feature flat (0.99) where the zodiac moves on both. Inspecting it: the hit is entirely
f49v's left-margin column of **single characters**,
`f o r y e * k s p o * y e * * p o * y e * d y s k y`, which contains the literal
repeated block `p o * y e *` at distance 7. For single-character "labels" the last-two
feature is the whole character, so this is a verbatim repeat, not an ending cycle. The
sweep rediscovering the f49v marginal column's periodicity without being told about it
is a second pipeline check; it is not a second instance of Finding 3.

Also worth one line: running-text words *within a line* are **less** likely to share
endings at lag 1 than chance (0.77, Z = −2.98). Whatever governs Voynichese line
composition actively avoids adjacent ending repetition, which is the opposite of the
zodiac labels' behaviour and further separates the two.

### Independent transcription

Re-run on Glen Claston's **v101** transcription (`musyoku/voynich-transcription`) — a
different reading of the same pages with a different alphabet *and different word
segmentation*. The test needs only symbol identity, so it runs on v101 strings directly.

| v101 set | lag-7 last2 ratio | Z | p | lag-7 penult ratio | Z | p |
|---|---:|---:|---:|---:|---:|---:|
| zodiac label rings | 1.55 | +1.59 | 0.087 | 1.29 | +1.78 | 0.057 |
| zodiac ring text | 1.01 | +0.10 | 0.48 | 1.06 | +0.90 | 0.20 |

Lag 7 is the highest lag ≥ 2 in both features, and the ring-text control stays flat, but
neither reaches significance on its own. v101 does not tag label rings separately, so
they had to be matched to the Takahashi label rings by token count
(`src/t13_v101.py` prints the assignment); several matches are off by 1–4 tokens, which
attenuates any positional effect. **Call this consistent, not confirmed.**

---

## Finding 4 — a *strong* global seven-class code is excluded; a weak one is exactly what the data look like

The obvious reading of Finding 3 is a degree-ruler / *monomoiria* cycle: in a
30-per-sign degree list, a repeating seven-planet assignment puts the same ruler on
degrees seven apart. That predicts more than local periodicity — it predicts **one**
seven-class system shared by every ring, so that after aligning each ring by a phase,
labels in the same class agree on their endings *across* rings.

Fitted by coordinate ascent with one phase per ring, **with the observed fit and every
null replicate given the same restart budget** (`src/t19_phase_calibrated.py`; this
supersedes the numbers in `src/t10_phase.py`, whose null got a smaller budget):

| set | period 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|
| all rings (Z) | +0.25 | **+2.47** | **+2.17** | −0.36 | −1.30 | −0.03 |
| early only | +0.53 | +0.56 | +0.66 | −0.04 | −0.80 | +0.31 |
| late only | −0.42 | +1.05 | +1.03 | −0.10 | +0.14 | +0.77 |

On its own that table is unreadable: is +2.17 a weak signal or no signal? So the test
was calibrated by **injecting a global cycle of known strength into within-ring
permuted data** and re-running it (`src/t16_power.py`). α is the fraction of labels
whose ending is dictated by its class:

| α | mean Z | sd | power (Z > 2) |
|---:|---:|---:|---:|
| 0.00 (no structure) | **+0.10** | 0.98 | 0.00 |
| 0.10 | +0.35 | 0.82 | 0.00 |
| 0.20 | +2.66 | 1.65 | 0.60 |
| 0.30 | +8.29 | 2.80 | 1.00 |
| 0.45 | +30.75 | 6.51 | 1.00 |
| 0.60 | +57.49 | 9.43 | 1.00 |

The test is properly calibrated at α = 0, and the observed **Z = +2.17 sits almost
exactly on the α ≈ 0.20 line**. So the honest conclusion is a bound, not an absence:

- **α ≥ 0.30 is excluded outright.** A regular, manuscript-wide seven-class code in
  which a third or more of labels carry the class ending would have produced Z ≥ 4 in
  every one of 20 simulated corpora. It did not.
- **α ≈ 0.20 is exactly what the data look like** — and at that strength this test only
  detects it 60% of the time, which is why the halves (Z = +0.66, +1.03) fail
  individually.
- **α ≤ 0.10 is invisible** to this test and cannot be ruled out by any amount of
  further analysis on this corpus.

Two further limits worth stating. The global test **cannot separate period 6 from
period 7** (+2.47 vs +2.17); only the within-ring lag test of Finding 3 can, and there
period 7 is the best lag in all seven partitions while period 6 replicates in the early
half only. And a single skipped or damaged nymph inside a ring breaks the phase from
that point on while leaving local period-7 similarity intact, which would depress the
global statistic without there being anything wrong with the cycle.

**This is the practice from `board/PRACTICES.md` — run the null and report where it has
no power — doing real work.** Without the injection curve this section would have read
"no global cycle found", which on these numbers would have been wrong.

---

## Finding 5 — the label regime split is not Currier A/B, and Currier A/B is not a one-glyph re-encoding

Finding 1b invited an obvious extrapolation: Currier A is `a`-heavy and B is `e`-heavy,
so perhaps one `e`↔`a` substitution explains both the label regimes *and* the
manuscript's main register split — which would be a claim about the writing system
rather than about two languages. **It does not.**

Running-text pages were assigned a Currier language from
`OrcusLabs/voynich.science` `mappings_TTLI.json` (193 classified pages; pipeline check:
f1r → A, f75r → B, both correct). Same collapse-scan as Finding 1b, sample sizes
matched by subsampling, baselines taken by splitting each language's own **pages** in
half:

| quantity | value |
|---|---:|
| raw A-vs-B glyph-bigram JSD | 0.0955 |
| within-A baseline (random page halves) | 0.0076 |
| within-B baseline | 0.0050 |
| **excess over baseline** | **0.0892** |

The A/B difference is roughly **12× the within-language variation**. The best single
glyph merge of all 276 closes only 35.7% of that gap (`o`/`d`), and the residual is
still ~8× baseline:

| collapse | A-vs-B JSD | gap closed |
|---|---:|---:|
| `o`/`d` | 0.0637 | 35.7% |
| `o`/`e` | 0.0678 | 31.0% |
| `d`/`y` | 0.0727 | 25.5% |
| `e`/`y` | 0.0754 | 22.5% |
| **`e`/`a`** | **0.0962** | **worse than raw — rank 254 of 276** |

Two conclusions, both worth keeping:

1. **The zodiac-label regime split is a different phenomenon from Currier A/B.** The
   substitution that best closes the label split is the 254th-best for A/B, i.e. it
   makes A/B slightly *worse*. Independently, all twelve zodiac diagram pages are
   **Currier-unclassified** in this dataset, so Finding 1 is on territory Currier's
   labels do not cover at all and cannot be a restatement of them. (Other taxonomies do
   assign the zodiac pages a class; that assignment was not reachable from this
   environment and is **unverified**.)
2. **Currier A/B is not a one-glyph re-encoding of a single system.** No single glyph
   identification brings A and B within reach of their own internal variation. This is a
   direct, quantitative answer to a question this folder has had open since 2026-09-04,
   and it constrains the "A and B are one language differently written" family of
   proposals.

---

## Finding 6 — the labels are diagram-locked, but *less* page-locked than the text is

Does a diagram's nymph labels have anything to do with that diagram's own circular ring
text, or could any label sit on any diagram? Statistic: mean over a diagram's labels of
the best Levenshtein similarity to any word of a target diagram's ring text, giving a
12 × 12 matrix (`results/t17_labeltext.json`). The permutation is over assignments of
label sets to ring texts, so both row and column marginals are held fixed.

| test | result |
|---|---:|
| mean self | 0.6515 |
| mean other | 0.6318 |
| permutation p, all 12 diagrams | 0.0032 |
| **permutation p, stratified within the two regimes** | **0.000025** |
| self beats the mean of its immediate neighbours | 10 of 12 (sign p = 0.019) |

So the labels are tied to their own diagram. **But the size of that tie is the
interesting part.** Repeating the comparison with target sets equalised by word count:

| stream | lift of own-page over size-matched other-page |
|---|---:|
| one ring-text line vs the rest of its own page's ring text | **+0.0249** |
| a diagram's labels vs its own page's ring text | **+0.0059** |

**The label stream is roughly four times less page-locked than the text stream is to
itself.** A page-local copy-and-mutate generator — the mechanism proposed for
Voynichese word formation, and the one that would otherwise explain the diagram
affinity away — predicts the opposite: labels drawn from the page's local pool would be
*at least* as page-locked as the text. They are not.

That is weak positive evidence for the premise the whole external-crib programme rests
on: that the labels come from somewhere other than the page. It had never been checked.
Treat it as a constraint, not a result: labels are short and few, the two streams have
different length distributions, and best-match similarity is sensitive to both.

---

## What this changes for the next attempt

1. **Fit any external crib on one regime at a time.** The `2026-09-07-alfonsine-myriogenesis`
   pipeline assumes one label system across all twelve signs. Findings 1/1b say it is at
   least two. A code table fit on Pisces–Cancer should be expected to *fail* on
   Leo–Sagittarius unless the `e`↔`a` normalisation is applied first — and that is a
   falsifiable prediction the pipeline can test the moment it has its source list.
2. **Score any candidate reading on lag-7 ending agreement.** A correct assignment of an
   ordered source list to a ring should reproduce ratio ≈ 2 at lag 7. This is a free,
   crib-independent acceptance test that every proposed reading must pass, and it costs
   nothing to run.
3. **The highest-value new evidence is physical, not textual.** Whether the rings are
   complete 30-item sequences, whether any nymph is unlabelled or lost, and where each
   transcriber started the traversal, decide between "no global cycle" and "global cycle
   with phase slips". That is a look at the folios, not another statistic.

## Reproducing

```
pip install numpy
git clone --depth 1 https://github.com/alephmembeth/voynich.git
git clone --depth 1 https://github.com/musyoku/voynich-transcription.git
export VMS_TAKAHASHI=.../voynich/analysis/takahashi_original.txt
export VMS_V101=.../voynich-transcription/voynich.txt
cd src
python3 labels.py        # dump the 298 labels by ring
python3 t6_regime.py     # Finding 1
python3 t7_substitution.py  # Finding 1b
python3 t8_period.py     # discovery scan
python3 t9_controls.py   # stratification + controls
python3 t11_pooled.py    # nested ending features
python3 t12_final.py     # Finding 3, definitive
python3 t18_diversity.py # Finding 2
python3 t17_labeltext.py # Finding 6
python3 t14_currier.py   # Finding 5
python3 t19_phase_calibrated.py # Finding 4, budget-matched
python3 t16_power.py     # Finding 4 power curve
python3 t15_sweep.py     # manuscript-wide sweep
python3 t13_v101.py      # independent transcription
```

## Honest limits

- No label is read. No plaintext. No claim about language.
- Finding 3 was *selected* on the Takahashi corpus; the partitions confirm it but are
  not a fresh corpus. v101 is the only genuinely independent check and it is
  suggestive, not significant.
- The `a/(a+e)` drift and the physical order of the manuscript are perfectly
  collinear here and cannot be separated by any test on this data.
- Sources on the astrological doctrine of degree rulers were reached through search
  snippets only: `voynich.nu` and `arxiv.org` are blocked by this environment's egress
  policy. Every claim about *monomoiria* in this document is offered as an
  interpretation to be checked, and is marked **unverified**.
