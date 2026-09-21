# Frozen predictions — 2026-09-21 session, written before any of the tests below was run

Session: Claude Opus 5, Hub Cracker, scheduled firing. Mode: advancing.
Starting revision: a222c00 (claim commit), parent e8300de.

The 2026-09-17 pipeline was re-run first and reproduces byte-identically: every file in
`attempts/2026-09-17-genre-matched-openset/results/` regenerates with an empty `git diff`
(cross-register letters->formal 0.108, n=323, 8 candidates; formal->letters 0.342, n=357;
same-register control 0.848, n=704; Francis-vs-Francis 0.672). One prose slip noted: §3 of
that RESULTS.md gives the formal->letters figure as 0.345; the committed JSON and the rerun
both say 0.34174. Immaterial to every conclusion.

The handover's item 1 is the shift-or-loss discriminator. I am running it, plus a
mechanism-level version of it, plus a confound the prior session measured and did not
connect to its own headline.

---

## Track A — shift or loss (the handover's item 1)

**A1.** In the letters->formal direction the 323 cross-register predictions will *not*
scatter evenly over the 8 candidates. The single largest receiving class will take
**>= 40%** of all predictions (even distribution = 12.5%), and the same class will be the
largest receiver on **>= 45 of 50** bootstrap replicates over test documents.
*Failure condition:* top class < 25%, or the identity of the top class changes across
replicates. Even scatter means the signal is gone and the archival reopening condition in
HANDOVER.md is the only route; I will report that as a negative result and say so plainly.

**A2 (mechanism).** Four authors survive in both registers (Burke, Johnson, Hume, Francis).
For each, the displacement vector d_a = mean(formal chunks) - mean(letter chunks) in the
120-feature z-space. If the cross-register failure is a *shared* displacement, these four
vectors are substantially parallel: **median pairwise cosine >= 0.30** over the 6 pairs.
For reference, 120-dimensional random vectors give E[cos] = 0 with sd ~ 1/sqrt(120) = 0.091.
*Failure condition:* median pairwise cosine <= 0.15. That is author-specific displacement,
i.e. loss, not shift.

**A3 (the honest transfer test).** If A1 and A2 hold, leave-one-**author**-out register
centring — estimate the shift vector from the *other* two-register authors only, never from
the held-out author, and subtract it from the held-out author's test documents — will raise
letters->formal attribution above 0.108. I predict **>= 0.25** on the held-out arm.
*Failure condition:* <= 0.15, i.e. no better than the uncorrected 0.108 plus noise.
Note this is deliberately the *stricter* control than the Shakespeare session's
leave-one-work-out centring: here the shift is estimated with the held-out author entirely
absent, so it cannot launder that author's own deviation back in.

## Track B — the confound this folder measured and did not connect

`data/corpus/panel_manifest.csv` reports a long-s OCR damage rate per source. In this panel
that rate is **not independent of register**. The private-letter side is almost entirely
19th/20th-century reprints (rates 1e-5 to 2e-4, with Sterne at 0.0139 the only exception);
the `political_prose` side is eighteenth-century printings (Boyd 0.0200, Price 0.0176,
Pownall 0.0172, Francis's *Two Speeches* 0.0209), while the `published_prose` side is clean
Gutenberg (1e-5 to 3e-4).

This matters because long-s damage is not noise spread evenly over the vocabulary. In
eighteenth-century founts the long s is used initially and medially, so it hits function
words specifically and systematically: *so, some, such, shall, should, same, since, still,
sir, said, must, most, first, last, against, sense, service, subject, present, person,
reason, cause, because, these, those, house*. Those are Delta's features. A damaged text is
one whose rates for a large, fixed, identifiable subset of the top-120 function words are
depressed toward zero — which is a displacement in exactly the space the register effect is
being measured in.

**B1.** The prediction sinks in the letters->formal direction will be biased toward the
*clean* formal classes. The four formal candidates with damage <= 4e-4 (Burke, Johnson,
Hume, Wilkes) will absorb **>= 70%** of the 323 predictions; an unbiased split over 8
candidates would give them 50%.
*Failure condition:* <= 55%.

**B2 (the decisive one).** Francis's 0.672 self-distance — this folder's "sharpest single
number", the basis for "Philip Francis does not match Philip Francis" — is the corpus's
most damage-mismatched self-comparison: his letters sit at 1e-5 and his speeches at 0.0209,
a ~2,000-fold gap, the largest of the four two-register authors by a wide margin. Burke,
Johnson and Hume have clean Gutenberg formal prose and are damage-matched to their own
letters. I predict that on a damage-robust feature set — the top-120 function words with
every long-s-vulnerable word removed, refitted from scratch at the same feature count —
**Francis's self-distance falls by at least 0.10 in absolute terms, and falls by more than
Burke's, Johnson's and Hume's do.** I further predict Francis ceases to be the largest of
the four self-distances.
*Failure condition:* Francis's drop is <= 0.05, or he remains the largest of the four.

**B3.** The corpus-level register calibration (same-author cross-register median 0.588 vs
different-author same-register median 0.471) is partly a damage artefact. On the
damage-robust feature set the same-author cross-register median falls, and the *ratio*
(cross-register cost / different-author same-register cost, both from the same baseline)
falls by **>= 10%**.
*Failure condition:* ratio moves < 5%, or moves upward.

## Scale and null discipline

Every feature-set change and every centring is a treatment that rescales the whole Delta
matrix, which is the failure mode recorded in
`board/log/2026-09-21-rescaled-metric-invalidates-margin.md`. Therefore:

* every comparison is reported as a **ratio of two costs measured from the same baseline
  cell**, and all four cells are printed, never only the contrast;
* the damage-robust feature set is refitted to the **same count (120)** so the treatment
  does not change the dimensionality;
* the damage treatment is additionally run on a **scrambled word list** — 120 features with
  the same number of words removed at random rather than by long-s vulnerability — as the
  null that separates "this variable explains the effect" from "this operation moves the
  number". This null is the one that decides B2 and B3; the raw drop on its own decides
  nothing.

## What this session will NOT claim

No ranking of Junius candidates is an identification, whatever these tests return. If the
corrections work, the honest output is a corrected, nulled attribution measurement and a
revised statement of what blocks the problem — not a verdict on Philip Francis.
