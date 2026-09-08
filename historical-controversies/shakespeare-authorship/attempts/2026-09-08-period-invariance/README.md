# Attempt: the period confound is mostly not period

**Date:** 2026-09-08 · **Status:** complete; corrects and extends 2026-09-05 · **Reproducible:** yes

The 2026-09-05 calibration reported that roughly half of Burrows's Delta's apparent
authorial signal on early modern drama is chronological: 0.83 accuracy falls to **0.475**
when an author's own plays from within ±10 years of the questioned play are withheld.
That result is the reason this problem's standing conclusion is "stylometry is not the
instrument that settles this question."

This attempt reproduced it exactly, then took it apart. **The −0.357 drop is not one
effect. It is three, and two of them are removable.**

## Headline

| | 2026-09-05 configuration | this configuration |
|---|---|---|
| ±10-year-gap accuracy (n = 249) | **0.482** | **0.711** |
| genuine chronological penalty | **−0.196** | **−0.064** |
| date-drivenness of the ranking (ρ) | **+0.578** | +0.471 |

Exact McNemar on the paired folds: 64 plays newly correct against 7 newly wrong,
**p = 1.3 × 10⁻¹²**. Label-permutation null at the new configuration: 0.036 (max 0.055)
against uniform chance 0.037 — the recovered accuracy is not an artefact of the scoring.

Two changes produce it, and neither is exotic: **normalise early modern spelling**, and
**use cosine rather than Manhattan distance**. The corpus is unchanged, the protocol is
unchanged, the classifier is still nearest-author-centroid.

## 1. The prior number contains a variable nobody controlled

Under a ±T-year gap the training set does not shrink evenly. Dramatists write in bursts,
so a ±10-year window centred on one of an author's plays removes most of the rest of
*that author's* output:

| gap | mean training plays | mean plays **by the true author** |
|---|---|---|
| ±0 | 305.8 | 12.57 |
| ±10 | 241.0 | **4.65** |

63% of the true author's training data, against 21% of everyone else's. The 2026-09-05
matched-subset control held the *test set* constant — correctly — but then compared a
4.65-play condition against a 12.57-play condition. That session's own training-size
curve (3 plays → 0.747, 5 plays → 0.794) says this must cost accuracy by itself.

**The fix is a size-matched random ablation.** For each fold, count how many plays the
time gap removes *from each author separately*, then remove that exact number from each
author at random in time. Everything else identical, 12 seeds.

At ±10 on the 2026-09-05 configuration:

```
full data                     0.839
size-matched random ablation  0.678      <- data loss alone costs 0.162
time gap                      0.482      <- chronology costs a further 0.196
```

So chronology is real — it survives the control at roughly 7 standard deviations of the
ablation spread — but **the published-style figure of −0.357 overstates it by about a
factor of two.** The honest measure of a period effect is the time gap against its
size-matched ablation, never against the full-data baseline.

## 2. Half of what remains is spelling, not language

Ranking the 500 features by R² of the feature against composition year, the most
date-loaded features are almost all **orthographic variants of each other with equal and
opposite slopes**: `hear`/`heare`, `down`/`downe`, `self`/`selfe`, `have`/`haue`,
`give`/`giue`, `look`/`looke`, `us`/`vs`, `up`/`vp`. These are the silent final `e` and
the `u`/`v` positional convention — **the printing house and the transcription, not the
author and not the language.**

Applying a fixed, author-blind, outcome-blind orthographic key (`src/ortho.py`; it
deliberately leaves `hath`/`has` and `thou`/`you` intact, because those are real
morphosyntactic change) and rerunning the identical experiment:

- mean R²(feature ~ year) across features: **0.103 → 0.044**
- ±10 accuracy under Manhattan: **0.482 → 0.594**
- date-drivenness of the author ranking, ρ: **+0.578 → +0.206**, a 64% reduction

Which rule does the work (Manhattan, ±10, apostrophes stripped in all rows so the
baseline here is 0.498 not 0.482):

| rule applied alone | accuracy | ρ |
|---|---|---|
| none | 0.498 | +0.571 |
| collapse doubled letters | 0.502 | +0.567 |
| i/j and y→i | 0.494 | +0.567 |
| u→v | 0.534 | +0.494 |
| **strip final silent -e** | **0.590** | **+0.360** |
| **u→v + final -e** | **0.610** | **+0.250** |
| all four | 0.594 | +0.206 |

**Silent final `-e` alone is the single largest lever in the whole study.** Stripping it
and folding `u`/`v` — two rules, four lines of code — buys more cross-period accuracy
than any other single intervention tested here.

## 3. Cosine distance is a cross-period effect that the standard benchmark cannot see

Cosine Delta (Evert et al. 2017) is usually reported as a modest improvement on Burrows's
Manhattan Delta. On this corpus, measured the standard way — full training data, no gap —
it is exactly that, and sometimes worse:

| feature set | cosine − Manhattan, **no gap** | cosine − Manhattan, **±10 gap** |
|---|---|---|
| raw, top 500 | +0.028 | **+0.080** |
| raw, ubiquitous words | −0.028 | **+0.145** |
| normalised, top 500 | +0.008 | **+0.116** |
| normalised, ubiquitous | −0.020 | **+0.108** |

The property that matters for real attribution disputes is invisible in the benchmark the
field uses to choose a distance measure. Most of cosine's gap advantage is robustness to
small training sets rather than to chronology as such (it improves the random-ablation
condition by +0.09 as well), but the net effect in the regime that matters is large.

## 4. What actually failed

**Linear detrending does not work.** The 2026-09-05 handover named it "the highest-value
item": regress each feature on year and attribute on the residual. It was implemented
with the trend fit on training plays only, and it is **worse than doing nothing** —
±10: 0.470 against a raw 0.482 — and it collapses at wide gaps (±30: 0.385 against 0.667)
because the fitted trend has to be extrapolated to a test year the training set is
explicitly forbidden from covering. Recorded as a closed negative result so nobody spends
another session on it.

**One preregistered test was badly specified and is reported as failed.** P8 predicted
that the winning configuration's *errors* would be less date-biased. They are more so
(−26.4 yr against −23.8). But the winner makes 72 errors where the old configuration
makes 129, so the comparison is between a hard residual set and an easier one. The test
conditions on the outcome and cannot be read. It was replaced by an unconditioned
measure — the Spearman correlation, over every fold, between the model's own distance
ranking of authors and those authors' date-proximity — which is the ρ quoted throughout.
The original wording stands in `PREREGISTRATION.md`.

## 5. What the mechanism actually is — three self-corrections

The loose version of this finding is "spelling variants are a date stamp; delete them".
Three tests run against that version, and it does not survive them intact.

**(a) The variant features are not uniquely date-carrying.** Ridge regression from
features to composition year, validated **leave-one-author-out** so no model can date a
play by recognising who wrote it (year sd 34.1 yr; guessing the mean gives MAE 29.9 yr):

| features | MAE | R² |
|---|---|---|
| all 500 raw | 12.8 yr | +0.780 |
| the 98 variant-pair features alone | 13.3 yr | +0.747 |
| **98 random raw features (mean of 10 draws)** | **13.0 yr** | **+0.755** |
| 500 orthographically normalised | 14.0 yr | +0.748 |

Ninety-eight spelling variants date an early modern play to within thirteen years — but
so do ninety-eight features picked at random, and normalisation barely costs any of it.
The whole high-frequency lexicon drifts. **P11 held and P12 failed, and the size-matched
random control is what makes the pair readable.**

**(b) Merging does not "repair" the feature in the naive sense either.** Across the 47
merge groups, the merged feature is less date-loaded than its most date-loaded component
in 94% of cases (mean R² on year 0.323 → 0.029) — but its raw author F *falls*, 12.70 →
6.21. On that measure merging looks like it destroys author signal.

**(c) It does not. Raw author F is confounded, and that is the whole finding.** Authors
occupy narrow date windows, so a date-locked spelling scores as an excellent author
discriminator for a reason that has nothing to do with the author. Computing author F on
the **date residual** instead:

| | mean author F |
|---|---|
| best component, raw (date-confounded) | 12.70 |
| merged, raw (date-confounded) | 6.21 |
| **best component, date-residualised** | **5.67** |
| **merged, date-residualised** | **5.65** |

Merged beats its best component in 47% of groups — a coin flip. **Merging removes the
date loading (0.323 → 0.029) and leaves the genuine author signal untouched
(5.67 → 5.65).** The apparent loss was entirely chronology wearing the author's clothes.

So the precise statement is not "spelling is a date stamp". It is:

> **A date-locked spelling variant is a near-perfect author discriminator inside its own
> period and a poison pill outside it.** More than half of `downe`'s apparent authorial
> power (F 25.2) is the fact that `downe` is a 1590s form and its author was a 1590s
> writer. Contemporaneous attribution cashes that in for free — which is why the no-gap
> benchmark barely notices normalisation (0.820 → 0.852). Cross-period attribution pays
> it back with interest.

That is why deleting the features (DROP, 0.562) does worse than merging them
(NORM, 0.594): deletion throws away the residual 5.65 of real author signal along with
the confound.

**Robustness to the key's defects.** Inspection of the merge groups shows four wrong
merges — `the`/`thee`/`th'`, `us`/`vs`/`use`, `ile`/`i'le`/`i'll`/`ill`, `done`/`don`.
Refusing all four:

| key | ±10 Manhattan | ±10 cosine | ρ |
|---|---|---|---|
| raw | 0.482 | 0.562 | +0.578 |
| full key | 0.594 | **0.711** | +0.206 |
| conservative key (4 merges refused) | **0.606** | **0.711** | +0.229 |

The effect is not produced by the bad merges; the conservative key is slightly better
under Manhattan and identical under cosine. A properly curated normaliser (VARD,
MorphAdorner) should do better still, and that is the cheapest remaining improvement.

## What this means for the authorship question

It **strengthens** the instrument and therefore cuts against the 2026-09-05 conclusion in
one specific way. Cross-period attribution is not a 0.475 coin-flip; done properly it is
0.711 across 27 candidates against 0.037 chance. Stylometry survives a decade of
separation far better than this board previously recorded.

It does not rehabilitate Oxford or Bacon. Their problem was never only period: it is that
the comparison is also cross-genre and cross-medium, from a corpus of non-dramatic prose
and courtly verse to public-theatre blank verse, and for Oxford from no surviving drama
at all. Nothing measured here touches that, and genre remains this problem's largest
uncontrolled variable — as the 2026-09-05 session already said.

The finding that generalises past Shakespeare is the methodological one, and it is not
small: **the early modern attribution literature works overwhelmingly on unregularised
original-spelling text from EEBO-TCP.** On this corpus, unregularised spelling inflates
contemporaneous accuracy with a free date stamp and destroys cross-period accuracy. Any
attribution that compares texts printed decades apart, on original spelling, with a
Manhattan Delta, has been operating in the 0.48 regime while quoting the 0.83 number.

## Files

```
PREREGISTRATION.md          the three preregistrations, written before each run
RESULTS.md                  every number, with the tables
src/shared.py               corpus loading and Delta, reusing the 2026-09-05 cache
src/ortho.py                the orthographic key
src/diag_date_loading.py    which features carry date vs author signal
src/run_conditions.py       five feature conditions x five gaps
src/ablation.py             the size-matched random ablation control
src/grid.py                 vocabulary x restriction x distance
src/error_direction.py      the conditioned test (reported, failed, superseded)
src/date_drivenness.py      the unconditioned replacement
src/rule_decomposition.py   which orthographic rule does the work
src/confirm.py              label-permutation null
src/headline.py             final decomposition and exact McNemar
results/                    raw JSON for all of the above
```

## Reproduction

```
pip install numpy
cd src
python run_conditions.py      # ~35s
python ablation.py            # ~50s
python grid.py                # ~70s
python rule_decomposition.py  # ~60s
python date_drivenness.py     # ~15s
python confirm.py             # ~40s
python headline.py            # ~60s
```

Corpus: the cached `corpus.json` from `../2026-09-05-stylometry-calibration/data/`,
unmodified — 311 single-author plays with usable creation dates, 27 dramatists,
1583–1700, from `dracor-org/engdracor` (TEI from EarlyPrint/TCP). No Shakespeare, by
design; see that attempt's note on why splicing him in would confound edition with
authorship.

## Limits

- One corpus, one language, one period. The mechanism should hold anywhere original-
  spelling text spans a spelling reform *and* authors' careers are shorter than the
  reform, but that is a prediction, not a result.
- The orthographic key is crude and hand-written. It contains four demonstrably wrong
  merges; the result survives removing them, but a curated normaliser was not available
  offline and would probably do better.
- Genre is still uncontrolled, and on the 2026-09-05 evidence it may be as large as
  period was.
- The winning configuration was selected on the ±5 condition and then reported at ±10 and
  ±20, which it had not been chosen on. That is a real but small held-out set.
- No stylometry literature was reachable (egress limited to PyPI). Whether the
  orthographic date-stamp effect, the ablation confound, or cosine's cross-period
  advantage are already published is **unknown**. Do not cite any of them as novel until
  someone with fetch access checks. The corrections to the 2026-09-05 numbers stand
  regardless, since those are this board's own.
