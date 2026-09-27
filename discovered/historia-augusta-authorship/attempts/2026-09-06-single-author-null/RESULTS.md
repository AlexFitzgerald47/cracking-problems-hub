# The six sigla are not six hands; the seam is earlier than the lacuna

**Session:** 2026-09-06 · Claude Code (Opus 5) · cracker, starting
**Corpus:** 30 Historia Augusta lives (Perseus/Loeb), 108,112 tokens, with
Suetonius (12 lives) and Nepos (25 lives) as single-author controls.
**All output files:** `results/e1..e9_*.txt`. All code in `code/`.

## Summary

| Question | Answer | Evidence |
|---|---|---|
| Are the features real, or digitisation noise? | Real | Same vita across two independent digitisations is **13.2× closer** than two different vitae in one digitisation, with zero overlap (E1) |
| Can the instrument identify authors at these lengths? | Yes | Work-held-out Delta attribution of known Latin authors: **0.96 at 1,000 tokens, 1.00 at ≥1,500** (E2) |
| Do the six sigla mark six hands? | **No** | Separation p = 0.065, and only **19% of the magnitude** of a genuine two-author difference in the same genre (E3) |
| Is there a two-layer structure? | **Yes** | Split at the lacuna: z = +4.8, p = 0.0002, stable across 50–400 features (E5); a single author's ordered collection of lives produces **negative** separation at its own equivalent break (E5) |
| Is it just the forged documents? | **No** | Survives deleting every `<q>`: p = 0.0006. Survives quote-density matching: p = 0.0012 (E6) |
| Where is the seam? | **Before the lacuna, at #18–20, not #21** | Peak after Alexander Severus (#18), z = +5.6; leave-one-out puts the peak before the lacuna in **30/30** runs on all text and 28/30 narrative-only (E8, E9) |
| More than two layers? | No evidence | Pollio vs Vopiscus inside the later block: p = 0.53–0.84. Four sigla inside the earlier block: p = 0.24–0.42 (E7) |
| Any other real partition? | One, weaker | Hauptvitae vs Nebenvitae **within the earlier block only**: p = 0.006–0.023, surviving quote removal (p = 0.013–0.027). Not significant across all 30 (E7) |

## What is new here

Two things, neither of which is a restatement of the existing literature.

**1. A matched single-author null for "layers in an ordered collection".** The
published two-layer result is a claim that a collection of lives read in order
changes at a point. Any such collection has a best cut. The control that makes
the claim mean something is the same statistic run on a collection of lives
that is certainly by one hand — and it had not, as far as this session could
establish, been reported. Suetonius' twelve Caesars, split at his own sharpest
internal break (Nero | Galba, where his sources visibly thin), give a
**negative** separation of −0.20 to −0.44 across every feature-set size: his
two halves are *more* alike than a random regrouping of the same lives. Nepos
likewise. Against that, the Historia Augusta's +0.58 is a real discontinuity,
not an artefact of the procedure.

**2. The seam is located earlier than the manuscript lacuna.** Scanning every
cut point rather than testing the hypothesised one puts the maximum after
**vita #18, Alexander Severus** — the end of the stretch for which the author
had Marius Maximus to work from — not after #21, where the Palatine manuscripts
break. Leave-one-vita-out never moves the peak later than the lacuna: it sits
at #18, #19 or #20 in every one of the 30 all-text runs. The three lives
between (*Maximini duo*, *Gordiani tres*, *Maximus et Balbinus*) fall on the
**later** side of the seam.

This is a refinement, not a contradiction: it locates a boundary that the
two-layer reading places at the manuscript gap two to three lives earlier, at
a point that corresponds to a known change in the author's source material
rather than to an accident of transmission.

## Effect sizes, in one place

The statistic throughout is (mean between-group Delta − mean within-group
Delta) / sd, on 1,000-token blocks, with a text-level permutation null.

| Partition | Separation | p |
|---|---:|---:|
| Suetonius vs Nepos (two real authors, same genre) | **+1.83** | 0.0002 |
| Historia Augusta, at the lacuna | +0.58 | 0.0002 |
| Historia Augusta, at the strongest cut (#18) | +0.46 to +0.65 | — |
| Historia Augusta, Hauptvita vs Nebenvita, earlier block only | +0.40 | 0.013 |
| Historia Augusta, six sigla (whole-vita design) | +0.24 | 0.065 |
| Historia Augusta, Pollio vs Vopiscus | +0.12 | 0.53 |
| Suetonius, at his own source break | **−0.22** | 0.98 |
| Nepos, at his midpoint | **−0.42** | 0.98 |

The Historia Augusta's internal discontinuity is about **a third** of the size
of the difference between two genuinely different authors writing the same
genre. That is the number to argue about. It is far too large to be nothing
and too small to be read, without further argument, as two unrelated hands.

## What this does not show

- **It cannot date anything.** Internal stylometry counts strata and locates
  seams. The Theodosian-date question is untouched by everything here.
- **A seam is not necessarily a second author.** A single writer who changes
  sources, changes pace, and starts padding with invented documents will move
  in feature space. The controls rule out *quotation register* and *vita
  length* as sufficient causes; they do not rule out a change of working method
  by one person. That the strongest cut falls exactly where the Marius Maximus
  material runs out is, if anything, evidence for the change-of-method reading
  rather than the second-hand reading.
- **The Nebenvita result is suggestive, not established.** Eight to eleven
  blocks on the small side is thin, and it is significant only inside the
  earlier block.
- **The six-siglum null is a null, not a proof of unity.** E2 establishes that
  the instrument would catch a difference the size of Suetonius-vs-Nepos at
  these lengths. Two contemporaries collaborating on one project, imitating one
  model, could be far more similar than that and would not be caught. The
  honest statement is: *the sigla do not mark authorial differences as large as
  those between two independent authors of the same genre.*
- **Stover & Kestemont 2016 could not be read.** The paper is egress-blocked
  from this environment. Its claims are known here only from published
  abstracts and secondary summaries, and the comparisons above are made against
  that second-hand characterisation. **A future session with fetch access must
  check it before any of this is described as confirming or refining their
  result.**

## Reproducing

```
sh code/fetch_sources.sh                 # clones the two GitHub text mirrors
HA_SCRATCH=./sources python3 code/build_corpus.py
cd code && for e in e1_witness_check e2_power_curve e3_sigla e4_split \
    e5_chunks e6_quote_control e7_within_layer e8_boundary_scan e9_jackknife; \
    do python3 $e.py; done
```

Runtime: about three minutes total, no GPU, numpy only. Every permutation null
is seeded (`20260906`); Monte Carlo error moves p-values in the fourth decimal
between runs, which is why the tables above quote ranges where a result was
re-run.

## A trap worth recording

The first version of E2 reported 97.5% attribution accuracy at 1,000 tokens.
That was leakage: the nearest neighbour of a chunk was usually another chunk of
the same work, so the number measured work-recognition, not
author-recognition. Holding the whole work out drops the honest figure to
0.960 — which happens to be similar, but only because these authors are also
separated by four centuries. The lesson generalises to any chunked corpus:
**leave out the document, not the chunk.**

Likewise, E4's whole-vita design gave contradictory answers at full length
(p = 0.50) and at equalised length (p = 0.012). The contradiction was the
finding: vita length was carrying the result. E5 removes length from the design
entirely by making every data point a 1,000-token block, and it is E5's numbers,
not E4's, that are reported above. E4 is kept in `results/` because the
discrepancy is the reason to distrust whole-vita designs on this corpus.
