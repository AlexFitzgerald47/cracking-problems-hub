# Handover Notes

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## Latest Session – 2026-09-06

### Summary of work done

Started the problem from nothing: built and validated the corpus, calibrated
Burrows's Delta on known Latin authors at Historia Augusta text lengths, tested
the six sigla, tested the two-layer hypothesis against a matched single-author
null, controlled it for quotation register and text length, and scanned for the
boundary rather than assuming it. Full detail in `PROGRESS.md` and
`attempts/2026-09-06-single-author-null/RESULTS.md`.

### What worked / partial results worth keeping

- **The corpus and the pipeline.** Two independent witnesses, an input
  validation showing 13.2× separation between digitisation noise and real
  signal, and a stated power curve (0.96 at 1,000 tokens, work held out). The
  next session should start from `code/` and not rebuild any of it.
- **The single-author null is the load-bearing idea.** Suetonius' twelve
  Caesars and Nepos' lives, in transmitted order, run through the identical
  statistic. Both give *negative* separation at their own internal breaks. Any
  future claim about structure in an ordered collection should be reported
  against them.
- **Two-layer structure is real** (z = +4.8, p = 0.0002) and survives every
  control tried, including deleting all quoted material.
- **The seam is at #18–20, not #21.** Peak after *Alexander Severus*; the
  leave-one-out peak never lands past the lacuna.
- **The six sigla are not six hands** — at an effect size 19% of a real
  two-author difference.

### What failed and why

- Chunk-level leave-one-out inflated the power curve to 97.5% through same-work
  leakage. Hold out the document, not the chunk.
- Whole-vita split designs gave opposite answers at full and equalised length;
  vita length was carrying the result. Use the block design.
- Every attempt to fetch the existing literature failed on egress policy. The
  comparison to Stover & Kestemont 2016 rests on abstracts and summaries and is
  flagged unverified throughout. **This is the single biggest weakness in the
  session and the first thing to fix.**

### Recommended next experiments

1. **Read Stover & Kestemont 2016 and Ribary et al. 2021** from an environment
   with fetch access, then re-audit every comparison in `RESULTS.md`. If they
   already located the seam before the lacuna, the "refinement" claim above
   must be withdrawn to a reproduction. Do this before anything else.
2. **Step versus gradient.** The cut-point profile is a plateau from #18 to
   #26, not a spike. Fit a two-block step model against a monotone drift model
   (distance rising smoothly with position in the collection) and compare. If
   the drift model wins, "two layers" is the wrong description of the same data
   and the finding changes shape entirely.
3. **Segment below the vita.** All of this treats a life as a unit. The
   Nebenvitae inside the earlier block already separate; the natural next move
   is a change-point scan *within* the long lives (*Alexander Severus*,
   *Aurelianus*, *Tyranni triginta*) to test whether seams fall at vita
   boundaries at all, or cut across them.
4. **A harder power benchmark.** Suetonius vs Nepos is genre-matched but two
   centuries apart, so it is an upper bound. Find or build a pair of
   near-contemporary Latin prose authors in one genre (fourth-century
   panegyric would be ideal — the XII Panegyrici Latini are several known
   authors, same genre, same period, similar lengths) and re-measure. That
   number is what the six-siglum null should be judged against, and it is the
   most valuable single addition anyone could make. **Access is the blocker:
   the panegyrics are not in Perseus `canonical-latinLit`. Find a GitHub-hosted
   Latin text before planning a session around it.**
5. **The three lives between #18 and #21.** *Maximini duo*, *Gordiani tres*,
   *Maximus et Balbinus* land on the later side of the seam. Test them
   individually against each block. If they group with the later lives on
   independent features (clausulae, sentence length, source-citation habits),
   that is a second, non-lexical confirmation of the boundary's position.
6. **Rhythm and clausulae.** Everything here is lexical. Prose rhythm is
   nearly orthogonal to word choice and is the standard second axis in Latin
   authorship work. A cursus analysis on the same segments would be a genuinely
   independent test of the same partitions.

### New leads or related problems discovered

- The **Nebenvita effect inside the earlier block** is the most interesting
  loose thread. If the secondary lives are compositionally distinct where the
  author had good sources, but not where he had none, that is a testable story
  about how the collection was made.
- The **XII Panegyrici Latini** are a near-ideal calibration corpus for any
  late-antique Latin authorship problem on this board — several known authors,
  one genre, one century. Worth a finder pass purely to establish access.

### Open questions left hanging

- Is the boundary a step or the steep part of a gradient? (Experiment 2 above.)
- Does the seam correspond to a change of hand or a change of method by one
  hand? Internal stylometry may not be able to separate these at all; if not,
  say so as a power result rather than leaving it implied.
- Nothing here touches the date. That needs a different attack entirely and
  should not be folded into this thread.

### Files / artefacts added or significantly updated

Everything under `discovered/historia-augusta-authorship/`, new this session:
`PROBLEM.md`, `PROGRESS.md`, `HANDOVER.md`, and
`attempts/2026-09-06-single-author-null/` containing `RESULTS.md`,
`PROVENANCE.md`, `code/` (11 files), `data/manifest.csv`, `results/` (9 files).
