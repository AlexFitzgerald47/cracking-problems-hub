# The Junius register gap is a loss, not a shift — the Shakespeare correction does not transfer

**Session:** 2026-09-21, Hub Cracker routine, Claude Opus 5. **Mode:** advancing.
**Starting revision:** `e8300de`. Predictions frozen in `FREEZE.md`, committed before any
test below was run.

This session takes item 1 of `HANDOVER.md` — the shift-or-loss discriminator the
2026-09-21 orchestrator cross-reference recommended running "before anything else" — and
then the correction it gates. It also audits the 2026-09-17 session's baseline and its
sharpest single number.

---

## Headline

**Three results, one of which reverses the folder's recommended next move.**

1. **The discriminator returns LOSS.** Cross-register predictions do not collapse onto one
   or two classes. Their concentration (top receiver 0.341) is *below* what a
   no-signal document-permutation null produces on the same geometry (0.399 ± 0.098), the
   top receiver's identity is unstable across bootstraps, and 79% of each author's register
   displacement is author-specific rather than shared.

2. **The correction fails, and fails in the direction that matters.** Author-blind register
   centring — run in the *stricter* leave-one-author-out form — takes cross-register
   attribution from 0.108 to **0.068**; global register-mean centring takes it to
   **0.043**. Both are worse than doing nothing, and the corrected figure sits at its own
   permutation null's median (0.040, p = 0.490). **The `HANDOVER.md` item "if it collapses:
   apply both corrections" is now closed out as tried and failed.** The archival reopening
   condition stands as the route.

3. **The folder's sharpest single number is partly a scanning artefact — but only partly,
   and only locally.** Philip Francis's 0.672 self-distance across his own two registers is
   the corpus's most damage-mismatched comparison (his letters measure long-s damage
   0.00001, his *Two Speeches* 0.02155 — the highest in the corpus). On a damage-robust
   feature set it falls to **0.611**, a drop of 0.061 against a rank-matched null drop of
   −0.012 [−0.026, 0.005], **z = +7.4**, and **he is no longer the largest of the four**
   (Johnson 0.618 now is). The corpus-level register ratio, however, is untouched
   (1.225 → 1.257, null band [1.193, 1.268], p = 0.885). So: correct the sentence "Philip
   Francis does not match Philip Francis"; do not correct the register finding it was
   illustrating.

Nothing here counts for or against Philip Francis's authorship. It could not: every test
below is a measurement of the evidence, not of him.

---

## 0. Reproduction first

`attempts/2026-09-17-genre-matched-openset/` was re-run before anything new was written.
Every committed file in its `results/` regenerates with an **empty `git diff`** —
cross-register letters→formal 0.108 (n = 323, 8 candidates), formal→letters 0.34174
(n = 357), same-register control 0.848 (n = 704), Francis-vs-Francis 0.672, the register
calibration verdict unchanged. `numpy` 2.4.6; the prior run's version is not recorded.

One prose slip, immaterial: §3 of that `RESULTS.md` gives the formal→letters figure as
0.345; the committed JSON and the rerun both say 0.34174.

---

## 1. Audit: the chance baseline was 1/n, and it should not have been

The 2026-09-17 headline reads the cross-register figure as "**0.108** (chance 0.125) — *at
or below chance*". That session's own limits section says baselines here should be
label-permutation rather than 1/n_classes because the classes are unbalanced. The headline
did not follow its own rule.

Corrected, with a document-level permutation null (documents reassigned among authors,
class sizes preserved; 300 draws — `src/nulls.py`):

| condition | accuracy | 1/n | permutation null median | null p95 | p |
|---|---:|---:|---:|---:|---:|
| cross-register, letters → formal | 0.108 | 0.125 | **0.102** | 0.238 | 0.467 |
| same-register control | 0.848 | 0.091 | 0.083 | 0.159 | <0.0033 |

The verdict does not change — 0.108 is at chance — but the *reading* does. Against 1/n it
looked like the classifier was performing perceptibly worse than guessing, which invites
the thought that something systematic is pushing it away from the right answer. It is not:
it is sitting exactly on the null. The sharper statement of the same fact is that the test
set's **majority-class baseline is 0.282** (Hume 91 of 323 letter chunks), so a constant
predictor that always answers "Hume" beats the cross-register classifier 2.6-fold.

Note also that permuting whole author *blocks* is not a null here: it renames the centroids
without moving them, so every geometric statistic is invariant under it. My own first pass
did exactly this and produced a "label-shuffle reference" with a standard deviation of
0.000, which is the signature of a no-op. It is recorded in `results/shift_or_loss.json`
under `label_shuffle` and should not be quoted; `src/nulls.py` is the correct version.

---

## 2. Track A — the shift-or-loss discriminator

### A1. Where the predictions go (frozen prediction: FAILED)

323 private-letter chunks from the four two-register authors, scored against 8
formal-prose centroids.

| receiving class | count | share | train chunks | long-s damage |
|---|---:|---:|---:|---:|
| John Wilkes | 110 | 0.341 | 33 | 0.00040 |
| Edmund Burke | 101 | 0.313 | 174 | 0.00004 |
| Hugh Boyd | 83 | 0.257 | 51 | 0.01992 |
| Samuel Johnson | 10 | 0.031 | 156 | 0.00027 |
| David Hume | 9 | 0.028 | 17 | 0.00018 |
| Philip Francis | 6 | 0.019 | 10 | 0.02155 |
| Thomas Pownall | 4 | 0.012 | 27 | 0.01739 |
| Richard Price | 0 | 0.000 | 13 | 0.01750 |

I predicted a single class taking ≥40% and holding that position on ≥45 of 50 bootstrap
replicates. **Both limbs fail.** The top receiver takes 34.1%, and across 50 bootstraps
over the test documents the top receiver is Wilkes 37 times, Burke 12, Boyd 1.

The decisive comparison is the one PRACTICES insists on and which I nearly skipped:
**concentration must be read against a matched no-signal null, because with no signal the
argmin lands arbitrarily and sinks concentrate *more*.** Under the document-permutation
null the top receiver takes **0.399 ± 0.098**. The observed 0.341 is *below* it. There is
no excess concentration to explain.

For reference, the in-distribution tabulation on the same candidate set (formal → formal,
accuracy 0.909) concentrates similarly: Burke 0.349, Johnson 0.306. Concentration at this
level is what an unbalanced 8-class panel does whether or not it is working.

### A2. The mechanism (frozen prediction: inconclusive as stated; resolved by repair)

Four authors survive in both registers. Their register displacement vectors
d = mean(formal) − mean(letters) in the 120-feature z-space:

| pair | cosine |
|---|---:|
| Hume, Johnson | +0.596 |
| Hume, Burke | +0.470 |
| Francis, Johnson | +0.308 |
| Hume, Francis | +0.160 |
| Burke, Johnson | +0.225 |
| Burke, Francis | +0.143 |
| **median** | **+0.267** |

All six are positive and the median is ~2.9 sd above the random-vector expectation
(0 ± 0.091 in 120 dimensions). There *is* a shared direction. My frozen thresholds were
≥0.30 pass / ≤0.15 fail and +0.267 lands between them, so the prediction as written does
not decide.

The statistic that does decide is not the cosine but the **shared fraction of displacement
energy**, computed leave-one-author-out — how much of one author's displacement lies along
the direction defined by the *others*:

| author | ‖d‖ | shared fraction | residual after perfect centring |
|---|---:|---:|---:|
| David Hume | 7.89 | 0.302 | 6.59 |
| Samuel Johnson | 8.40 | 0.299 | 7.03 |
| Edmund Burke | 5.59 | 0.129 | 5.22 |
| **Philip Francis** | **9.51** | **0.071** | 9.16 |
| median | | **0.214** | |

**79% of each author's register displacement is author-specific.** Centring can remove only
the shared part; it leaves the rest and adds the estimation error of a direction fitted on
three authors. That is the whole explanation of A3 below, and it is knowable *before*
running A3.

One methodological trap inside the diagnostic itself, worth the line: computed **in
sample** — projecting each displacement onto the mean of all four, its own included — the
common direction carries **0.505** of total displacement energy. That is 2.4× the honest
leave-one-out figure of 0.214, and 0.505 would have read as "go". The leave-one-out
discipline the Shakespeare session applied to its *centring* is equally necessary in the
*diagnostic that decides whether to centre*.

Francis is the extreme case on both axes: the largest displacement in the panel (9.51) and
the least shared (0.071). Section 3 gives a reason.

### A3. The correction (frozen prediction: FAILED)

| treatment | accuracy | permutation null |
|---|---:|---|
| uncorrected | 0.108 | median 0.102, p = 0.467 |
| paired-displacement centring, leave-one-author-out | **0.068** | — |
| global register-mean centring, author-blind, leave-one-author-out | **0.043** | median 0.040, p95 0.106, **p = 0.490** |

I predicted ≥0.25 and set ≤0.15 as the failure condition. Both corrections come in *below
the uncorrected figure*, and the corrected number sits on its own null's median.

Two things are worth separating here. Centring did not merely fail to help; it destroyed
the small amount of structure that was there. The corrected sinks concentrate harder than
the uncorrected ones (Burke 0.406 after paired centring, 0.452 after global centring,
against 0.341 uncorrected) — which is precisely the signature PRACTICES gives for an argmin
with nothing left to work with.

And the form tested was the *stricter* one. The Shakespeare session centred
leave-one-**work**-out; here the shift is estimated with the held-out author entirely
absent, so it cannot launder that author's own deviation back in. A weaker, leakier
centring would score better and would mean less.

---

## 3. Track B — an OCR confound this folder measured per source and never connected

`data/corpus/panel_manifest.csv` has carried a long-s damage rate per source since
2026-09-17. In this panel **that rate is not independent of register**:

| cell | measured long-s rate | n chunks |
|---|---:|---:|
| Philip Francis, political prose (*Two Speeches* 1784) | **0.02155** | 10 |
| Hugh Boyd, political prose | 0.01992 | 51 |
| Richard Price, political prose | 0.01750 | 13 |
| Thomas Pownall, political prose | 0.01739 | 27 |
| Laurence Sterne, private letters | 0.01387 | 25 |
| John Wilkes, political prose | 0.00040 | 33 |
| Samuel Johnson, published prose (Gutenberg) | 0.00027 | 156 |
| Edmund Burke, published prose (Gutenberg) | 0.00004 | 174 |
| **Philip Francis, private letters** | **0.00001** | 80 |

The private-letter side is 19th/20th-century reprints; the `political_prose` side is
eighteenth-century printings. This matters because **long-s damage is not uniform noise.**
In eighteenth-century founts the long s is set initially and medially and round s only
word-finally, so `s`→`f` misrecognition lands on function words specifically — the features
Burrows's Delta uses. Twelve of the baseline's top 120 features are vulnerable:
*so, some, such, should, most, those, must, shall, she, these, same, himself*.

**Treatment:** refit the feature set to the same 120 count with those twelve removed.
**Null:** refit the same way with twelve **rank-matched** non-vulnerable words removed,
200 draws. The vulnerable words are disproportionately high-frequency, so a uniform random
exclusion would be a weaker treatment for reasons having nothing to do with long s; each
excluded word is therefore replaced by a non-vulnerable word drawn from a widening band
around its own frequency rank.

### B2 — partially upheld, and it changes a sentence in the folder's headline

| author | baseline | damage-robust | drop | null drop (median [p05,p95]) | z |
|---|---:|---:|---:|---|---:|
| **Philip Francis** | 0.672 | **0.611** | **0.061** | −0.012 [−0.026, 0.005] | **+7.38** |
| Samuel Johnson | 0.614 | 0.618 | −0.005 | +0.011 [−0.007, 0.035] | −1.27 |
| David Hume | 0.563 | 0.535 | 0.028 | +0.005 [−0.007, 0.024] | +2.32 |
| Edmund Burke | 0.383 | 0.376 | 0.007 | −0.002 [−0.009, 0.008] | +1.75 |

Frozen prediction B2 had three limbs: drop ≥0.10 (**missed** — 0.061), drops by more than
the other three (**upheld**), ceases to be the largest of the four (**upheld** — Johnson
0.618 now exceeds Francis 0.611). The stated failure condition (drop ≤0.05, or remains
largest) is not met, so B2 stands as **partially upheld**: the direction and the
specificity are confirmed with a large null-relative effect, the magnitude is well under
half what I predicted.

Substantively: **"On this measure Philip Francis does not match Philip Francis" was resting
in part on a scanning artefact, and the specific claim that his is the largest self-distance
in the panel does not survive.** It is not overturned — 0.611 is still an enormous
self-distance: measured on the same damage-robust feature set it still exceeds **89.7%**
of different-author same-register pairs (the 2026-09-17 median cross-register pair, 0.588,
exceeds 85.3% of them in this pipeline, reproducing that session's "86%"). The
2026-09-17 conclusion survives; one of its illustrations does not.

### B3 — failed, cleanly, and that is the interesting half

| quantity | baseline | damage-robust | rank-matched null |
|---|---:|---:|---|
| median same-author cross-register | 0.588 | 0.573 | — |
| median different-author same-register | 0.480 | 0.456 | — |
| **ratio** | **1.225** | **1.257** | 1.234 [1.193, 1.268] |

I predicted the ratio would fall ≥10%. It **rose** 2.6%, and the robust value sits inside
the null band (p = 0.885). The corpus-level register gap is **not** a damage artefact.

Reporting the ratio rather than the raw margin is what makes this readable, per
`board/log/2026-09-21-rescaled-metric-invalidates-margin.md`: both medians fell under the
treatment (0.588→0.573 and 0.480→0.456), so a session quoting the raw cross-register
median alone would have announced a 0.015 improvement that the denominator entirely
absorbs.

The two halves of Track B are both true and they are not in tension. **The damage confound
is local to one maximally mismatched cell, not a property of the register split.** Francis
is the only author in the panel whose two registers differ ~2,000-fold in scan damage;
Burke, Johnson and Hume have clean Gutenberg formal prose, damage-matched to their letters.

### B1 — not supported, and the prediction was badly specified

`FREEZE.md` set the clean-candidate cut at damage ≤4e-4 and named Wilkes as clean on the
manifest's 0.0004. Measured per chunk, Wilkes sits almost exactly on that cut: include him
and the clean classes absorb 0.712 of predictions against a 0.500 candidate share (B1
upheld); exclude him and they absorb 0.372 against 0.375 (B1 refuted). **A threshold placed
on a data value is not a test**, and I am not entitled to pick the side. The continuous
statistic B1 should have specified:

* Spearman(candidate damage rate, share of predictions) = **−0.429**
* Spearman(candidate training size, share of predictions) = **+0.714**

At n = 8 candidates neither reaches significance (critical |ρ| ≈ 0.74), so neither is
established. But damage is the weaker of the two and has no support beyond its sign, while
training-set size is the better-supported competitor. **B1 is not supported.** Consistently,
on the damage-robust feature set cross-register accuracy *falls*, 0.108 → 0.065: removing
the damage does not recover any cross-register signal.

---

## 4. What this session changes about the problem

| claim in the folder | status after this session |
|---|---|
| The register gap exceeds the author signal | **Stands**, and survives a damage-robust refit (ratio p = 0.885) |
| Cross-register attribution runs at chance | **Stands**, with the baseline corrected from 1/n = 0.125 to a permutation null of 0.102 |
| Francis 8th of 15 is evidence neither way | **Stands** |
| "Philip Francis does not match Philip Francis" — his 0.672 is the panel's largest | **Corrected.** Damage-inflated; 0.611 robust, and Johnson's 0.618 is larger |
| Try the Shakespeare correction before waiting on archival text | **Closed out — tried, failed.** Both centrings score below doing nothing, at their own null |
| Reopening condition: ≥8,000 words Junius-private or ≥20,000 words Francis-public | **Reinstated as the only route** |

The cheaper compute route the 2026-09-21 cross-reference opened is now closed. That is a
negative result and it is worth having: it cost one session and it stops the next four from
each spending one on the same idea.

---

## 5. Reproducing

```
pip3 install numpy
python3 src/shift_or_loss.py      # Track A: sinks, displacement cosines, both centrings
python3 src/nulls.py              # corrected permutation baselines
python3 src/damage_confound.py    # Track B: damage-robust refit + rank-matched null
python3 src/diagnostics.py        # repaired B1, leave-one-out shared fraction
```

All four read the 2026-09-17 corpus unchanged from
`../2026-09-17-genre-matched-openset/data/corpus/` and reuse its tokeniser, chunker and
function-word list. Results land in `results/*.json`. Runtime is ~30s total.

## 6. Limits, stated plainly

* **n = 4.** Every displacement-geometry statistic rests on the four authors who survive in
  both registers. The shared fraction 0.214 has no confidence interval worth quoting. What
  carries the conclusion is not that number alone but its agreement with A1 (no excess
  concentration), A3 (both centrings worse than nothing, at the null) and the bootstrap
  instability of the sink — four independent readings of the same corpus, all saying loss.
* My cell-level recomputation gives the different-author same-register median as 0.480
  where `register_calibration.py` reports 0.471, and Johnson/Hume self-distances as
  0.614/0.563 where it reports 0.613/0.561. The cell inclusion rule differs slightly
  (≥8 chunks per (author, genre) cell here). Every Track B comparison is baseline-vs-
  treatment **within this pipeline**, so the offset does not touch any verdict; it does mean
  the absolute numbers in §3 should be quoted from here and the 2026-09-17 ones from there.
* The damage-robust feature set removes words that are *vulnerable* to long-s damage, not
  words *observed* to be damaged. It therefore removes real signal from the clean texts too.
  That is the correct conservative direction for B2/B3 (it biases against finding an effect)
  but it is not a repair of the damaged texts, and a session with the energy for it should
  try the other direction: restore `fhall`→`shall` etc. in the damaged cells and re-measure.
* `src/shift_or_loss.py`'s `label_shuffle` block is a no-op, kept in the output for the
  record and superseded by `src/nulls.py`. See §1.
* The Shakespeare corpus is **not committed** — `chunks.json` is gitignored and regenerable
  only from a ~500 MB TCP + dracor fetch — so the calibration comparison in
  `board/log/2026-09-21-shared-fraction-decides-whether-centring-can-work.md` could not be
  run here and is specified there instead.
