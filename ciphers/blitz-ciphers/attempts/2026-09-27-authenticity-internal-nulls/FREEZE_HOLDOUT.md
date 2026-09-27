# FREEZE 2 — holdout prediction, 2026-09-27

Written **after** the pages 7/8 results and the length-matched calibration, and **before**
any statistic was computed on the holdout. The holdout is evidence that played no part in
developing anything above.

## The holdout

Nick Pelling's **original (2011/2013) provisional transcription** of "part of the text",
`https://ciphermysteries.com/other-ciphers/blitz-ciphers`, mirrored identically at
`cipherfoundation.org`. `data/holdout_2011key.txt`. It is independent of pages 7/8 in three
ways that matter: **different pages** of the manuscript, a **different transcription key**
(the original ~50-glyph key, not the expanded one Pelling built for pages 7/8), and a
**different transcription session** three years earlier.

581 tokens in 11 paragraphs. **Paragraph 3 (113 tokens) is excluded before any test**, on a
ground stated in the data file and fixed before the test was run: its opening lines read
`ABCDEFGHIJKL...` and `PQR.k.E.G.ST.j.UCVBWXAYZ`, i.e. its glyph sequence coincides with the
order of Pelling's own transcription key, so any structure it shows is the key's ordering
rather than the document's. That leaves **468 tokens, 47 types** — within 0.5 % of page 7's
470 tokens, so the `@470` calibration applies directly.

## What has already been established (development set, pages 7 and 8)

- Bigram-IC z, within-line unigram shuffle: p7 **+5.84** (n=470), p8 **+2.42** (n=159),
  pooled **+6.81** (n=629). All positive; p7 and pooled at p = 5e-5.
- Genuine length-matched reference, 5th percentile: Copiale@470 **+9.31**, Borg@470 **+9.18**;
  Copiale@629 **+12.63**, Borg@629 **+12.41**. Power at 470 tokens is **1.000** in both.
- Doublet z: p7 **-0.42**, pooled **-1.19**, against genuine medians of **-2.70** (Copiale@470)
  and **-3.21** (Borg@470).

## Frozen predictions

If the Blitz corpus is one kind of thing, the holdout must behave like pages 7 and 8, not like
the genuine comparanda:

- **H1.** Holdout bigram-IC z > 0 at p < 0.05. *(Replicates that there is real sub-unigram
  structure.)*
- **H2.** Holdout bigram-IC z falls **below the genuine 5th percentile for n≈470, i.e. below
  +9.18**. Point prediction: **z between +3 and +9**. *(This is the discriminating one. The
  genuine reference has power 1.000 at this length and 0 of 402 genuine blocks at @470 are
  expected this low; a holdout landing in the genuine range would refute the development-set
  finding outright.)*
- **H3.** Holdout doublet z is **greater than -2.0**, i.e. materially less negative than both
  genuine medians at this length.

H2 is the prediction I would most expect to fail if pages 7 and 8 are unrepresentative, if the
180° rotation of page 7 corrupted its transcription, or if the effect is an artifact of the
expanded 2014 key. The holdout shares none of those.

## Confound recorded in advance

The original key is known to merge at least two distinct glyphs: Tim T, comment of 5 Dec 2013
on that same page, identified a second `m`-like glyph "with a tail to the left" that the key
did not distinguish, and Pelling accepted the correction. Merging two glyphs into one code can
only **raise** apparent repetition, so it biases the holdout **towards** the genuine range and
**against** H2. H2 surviving that bias is stronger than H2 surviving nothing.
