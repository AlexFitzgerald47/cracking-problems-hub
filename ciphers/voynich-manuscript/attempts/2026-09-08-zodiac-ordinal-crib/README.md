# The Voynich zodiac labels are two register regimes, and their endings repeat at period 7

**Date:** 2026-09-08
**Session:** Claude (Opus 5), remote
**Status:** two structural findings, one clean negative. **No decipherment, no reading of any label.**
**Preregistration:** `PREREGISTRATION.md`, written before any statistic was computed.

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

## Finding 2 — label endings recur at period 7 within a ring

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

## Finding 3 (negative) — there is no global seven-class code table

The obvious reading of Finding 2 is a degree-ruler / *monomoiria* cycle: in a
30-per-sign degree list, a repeating seven-planet assignment puts the same ruler on
degrees seven apart. That reading predicts more than local periodicity — it predicts
**one** seven-class system shared by every ring, so that after aligning each ring by a
phase, labels in the same class agree on their endings *across* rings.

Tested by fitting one phase per ring by coordinate ascent, scoring cross-ring agreement,
with the identical fitting procedure applied to permuted rings (matched search budget):

| set | period 6 | period 7 | period 8 |
|---|---:|---:|---:|
| all rings | Z = +2.32 | Z = +2.05 | Z = −0.18 |
| early only | +0.48 | +0.54 | −0.11 |
| late only | +0.98 | +1.03 | −0.10 |

Period 7 does not beat period 6, and neither replicates in the halves. **The periodicity
is local to each ring; it is not a manuscript-wide class system.** Report this as a real
result: it kills the strongest version of the degree-ruler hypothesis, and any future
attempt to read the labels as a global cyclic code has to explain this table first.

(It does not kill a weaker version. A single skipped or damaged nymph inside a ring
breaks the phase from that point on while leaving local period-7 similarity intact.
Distinguishing "no global system" from "global system with phase slips" needs the
nymph-by-nymph physical evidence, not more statistics on this transcription.)

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
python3 t12_final.py     # Finding 2, definitive
python3 t10_phase.py     # Finding 3 (slow, ~20 min)
python3 t13_v101.py      # independent transcription
```

## Honest limits

- No label is read. No plaintext. No claim about language.
- Finding 2 was *selected* on the Takahashi corpus; the partitions confirm it but are
  not a fresh corpus. v101 is the only genuinely independent check and it is
  suggestive, not significant.
- The `a/(a+e)` drift and the physical order of the manuscript are perfectly
  collinear here and cannot be separated by any test on this data.
- Sources on the astrological doctrine of degree rulers were reached through search
  snippets only: `voynich.nu` and `arxiv.org` are blocked by this environment's egress
  policy. Every claim about *monomoiria* in this document is offered as an
  interpretation to be checked, and is marked **unverified**.
