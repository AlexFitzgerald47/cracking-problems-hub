# Results — every number

All accuracies are leave-one-play-out on 311 single-author plays, 27 dramatists,
1583–1700. Features are relative frequencies of the 500 commonest word types unless
stated; z-scoring uses training statistics only. Corpus and Delta implementation are
inherited unchanged from `../2026-09-05-stylometry-calibration/`.

## 0. Replication anchor

`python ../2026-09-05-stylometry-calibration/src/calibrate.py --control` reproduces the
prior session exactly: baseline 0.824, and the matched period control

```
gap  n    with-gap  same plays, no gap   drop
  0  312   0.817       0.824            -0.006
  5  295   0.654       0.834            -0.180
 10  255   0.475       0.831            -0.357
 20  115   0.496       0.809            -0.313
 30   45   0.644       0.800            -0.156
```

This attempt drops the one play with no usable creation date, so n is 311 and the gap
counts are 311/289/249/109/39. That is the only difference; the raw ±10 figure moves
0.475 → 0.482.

## 1. Feature-level date loading (`results/date_loading.json`)

R² of each z-scored feature regressed on composition year; author F computed on the
date residual. Top of the ranking:

| word | R²(year) | F(author) | slope | word | R²(year) | F(author) | slope |
|---|---|---|---|---|---|---|---|
| hear | 0.634 | 3.24 | +0.80 | haue | 0.497 | 5.28 | −0.70 |
| down | 0.575 | 5.07 | +0.76 | poore | 0.484 | 1.87 | −0.70 |
| just | 0.573 | 4.41 | +0.76 | selfe | 0.474 | 4.72 | −0.69 |
| self | 0.533 | 3.24 | +0.73 | feare | 0.464 | 2.61 | −0.68 |
| speak | 0.478 | 4.30 | +0.69 | downe | 0.464 | 6.07 | −0.68 |
| think | 0.477 | 4.22 | +0.69 | goe | 0.457 | 2.78 | −0.68 |
| dear | 0.465 | 5.88 | +0.68 | neuer | 0.457 | 5.59 | −0.68 |
| mean | 0.449 | 3.01 | +0.67 | heare | 0.455 | 1.81 | −0.67 |
| fear | 0.448 | 3.05 | +0.67 | giue | 0.455 | 4.74 | −0.67 |
| has | 0.442 | **13.16** | +0.66 | vs | 0.443 | 5.63 | −0.67 |
| | | | | hath | 0.416 | **16.80** | −0.64 |

Mean R²(year) over all 500 features: **0.1032**. Over the normalised feature set:
**0.0439**.

Features with essentially no date loading but high author F: `ye` (F 29.0), `enter`
(15.5), `now` (13.4), `breath` (11.8), `therefore` (10.4).

## 2. Training-set shrinkage under the gap

| gap | n tested | mean training plays | mean plays by the true author | authors available |
|---|---|---|---|---|
| ±0 | 311 | 305.8 | 12.57 | 27.0 |
| ±5 | 289 | 270.3 | 7.78 | 26.7 |
| ±10 | 249 | 241.0 | 4.65 | 25.9 |
| ±20 | 109 | 199.5 | 3.39 | 22.3 |
| ±30 | 39 | 151.7 | 3.08 | 18.5 |

## 3. Five feature conditions × five gaps (`results/conditions.json`)

Accuracy with the gap; matched no-gap accuracy on exactly the same plays in brackets.

| gap | RAW | DETREND | DROP | NORM | NORM+DETREND |
|---|---|---|---|---|---|
| ±0 (311) | 0.814 [0.820] | 0.820 [0.826] | 0.826 [0.842] | 0.839 [0.852] | 0.823 [0.839] |
| ±5 (289) | 0.668 [0.841] | 0.685 [0.848] | 0.706 [0.865] | **0.740** [0.875] | 0.716 [0.862] |
| ±10 (249) | 0.482 [0.839] | 0.470 [0.847] | 0.562 [0.867] | **0.594** [0.880] | 0.566 [0.863] |
| ±20 (109) | 0.514 [0.826] | 0.422 [0.826] | 0.541 [0.853] | 0.505 [0.872] | 0.505 [0.862] |
| ±30 (39) | 0.667 [0.846] | 0.385 [0.846] | 0.615 [0.872] | 0.590 [0.923] | 0.538 [0.897] |

DETREND = per-feature linear regression on year, fit on training plays only, residuals
attributed. DROP = the 51 most date-loaded raw features deleted, date loading measured
per fold on training plays only, 51 matched to the number of raw features the
orthographic merge absorbs. Both are pre-specified controls, not proposals.

**DETREND fails.** It is the 2026-09-05 handover's proposal 3 and it is worse than
nothing at ±10 and catastrophic at ±20/±30, where the fitted trend must be extrapolated
into a decade the training set is forbidden from covering.

**DROP (0.562) versus NORM (0.594)** separates the two available explanations. Deleting
date-loaded features recovers most of the gain, merging the variant pairs recovers a
further 0.032. So the finding is mostly "these features carry a date stamp" with a real
but smaller "and merging them recovers information rather than discarding it".

## 4. Size-matched random ablation (`results/ablation.json`, 12 seeds)

| features | gap | time gap | random ablation (sd) | full data | data-loss effect | chronology effect |
|---|---|---|---|---|---|---|
| RAW | ±0 | 0.814 | 0.816 (0.005) | 0.820 | −0.004 | −0.002 |
| RAW | ±5 | 0.668 | 0.781 (0.012) | 0.841 | −0.060 | **−0.113** |
| RAW | ±10 | 0.482 | 0.670 (0.028) | 0.839 | −0.169 | **−0.188** |
| RAW | ±20 | 0.514 | 0.628 (0.032) | 0.826 | −0.198 | −0.114 |
| RAW | ±30 | 0.667 | 0.690 (0.085) | 0.846 | −0.156 | −0.023 |
| NORM | ±0 | 0.839 | 0.845 (0.004) | 0.852 | −0.007 | −0.006 |
| NORM | ±5 | 0.740 | 0.795 (0.015) | 0.875 | −0.080 | −0.055 |
| NORM | ±10 | 0.594 | 0.686 (0.024) | 0.880 | −0.194 | **−0.092** |
| NORM | ±20 | 0.505 | 0.592 (0.028) | 0.872 | −0.280 | −0.087 |
| NORM | ±30 | 0.590 | 0.675 (0.046) | 0.923 | −0.248 | −0.085 |

The ±30 row rests on 39 plays and should not be read.

At ±10 the 2026-09-05 headline of −0.357 splits into −0.169 data loss and −0.188
chronology. Orthographic normalisation halves the chronological half.

## 5. Grid: vocabulary × restriction × distance (`results/grid.json`, 8 seeds)

`ubiq` = features present in ≥95% of plays (author-blind, date-blind, and it removes
period-locked spellings as a side effect). Entries are full / time-gap / random-ablation.

| cell | k | ±5 | ±10 | ±20 |
|---|---|---|---|---|
| raw + top500 + Manhattan | 500 | 0.841/0.668/0.780 | 0.839/0.482/0.671 | 0.826/0.514/0.631 |
| raw + top500 + cosine | 500 | 0.865/0.699/0.817 | 0.867/0.562/0.728 | 0.844/0.633/0.734 |
| raw + ubiq + Manhattan | 240 | 0.869/0.720/0.782 | 0.867/0.566/0.684 | 0.844/0.422/0.533 |
| raw + ubiq + cosine | 240 | 0.844/0.751/0.814 | 0.839/0.711/0.761 | 0.826/0.670/0.753 |
| norm + top500 + Manhattan | 500 | 0.875/0.740/0.794 | 0.880/0.594/0.689 | 0.872/0.505/0.586 |
| **norm + top500 + cosine** | 500 | **0.882/0.758/0.829** | **0.888/0.711/0.780** | **0.881/0.706/0.765** |
| norm + ubiq + Manhattan | 304 | 0.869/0.716/0.781 | 0.871/0.590/0.684 | 0.862/0.440/0.553 |
| norm + ubiq + cosine | 304 | 0.851/0.730/0.819 | 0.851/0.699/0.768 | 0.853/0.670/0.774 |

Selection was made on the **±5 column alone**. It picks `norm + top500 + cosine`, which
is then best or tied-best at ±10 and ±20 — columns it was not chosen on.

Cosine minus Manhattan, same feature set, at ±10:

| feature set | no gap | random ablation | time gap |
|---|---|---|---|
| raw + top500 | +0.028 | +0.057 | **+0.080** |
| raw + ubiq | −0.028 | +0.076 | **+0.145** |
| norm + top500 | +0.008 | +0.091 | **+0.116** |
| norm + ubiq | −0.020 | +0.083 | **+0.108** |

## 6. Date-drivenness of the ranking (`results/date_drivenness.json`)

Unconditioned. For each fold, Spearman ρ between the model's distance ranking of the
available authors and those authors' date-proximity to the questioned play. ±10 gap,
249 folds.

| configuration | ρ | se | top-ranked author is the date-nearest |
|---|---|---|---|
| raw + Manhattan (2026-09-05) | **+0.578** | 0.017 | 11% |
| norm + Manhattan | **+0.206** | 0.015 | 11% |
| raw + cosine | +0.669 | 0.017 | 16% |
| norm + cosine (winner) | +0.471 | 0.013 | 17% |

Orthographic normalisation removes 64% of the date-drivenness under Manhattan and 30%
under cosine. Cosine *raises* ρ while raising accuracy: date-correlated style is
genuinely informative, and cosine exploits more of it. What normalisation removes is the
part that is not informative.

## 7. Which orthographic rule (`results/rule_decomposition.json`)

Manhattan, ±10, n=249. Apostrophes are stripped in every row including "none", so the
baseline here is 0.498 rather than the true raw 0.482 — apostrophe stripping alone is
worth +0.016 and is itself an orthographic normalisation.

| rule | accuracy | ρ |
|---|---|---|
| none (apostrophes stripped) | 0.498 | +0.571 |
| collapse doubled letters | 0.502 | +0.567 |
| i/j and y→i | 0.494 | +0.567 |
| u→v | 0.534 | +0.494 |
| strip final silent -e | **0.590** | +0.360 |
| u→v + final -e | **0.610** | +0.250 |
| all four | 0.594 | **+0.206** |

Final silent `-e` is the single largest lever. The two-rule combination is the accuracy
optimum; adding the other two rules trades 0.016 accuracy for a further 0.044 of ρ.

## 8. Confirmation (`results/confirm.json`, `results/headline.json`)

Label-permutation null at the winning configuration, ±10: **0.036** mean, 0.055 max over
25 permutations, against uniform chance 0.037 and the recovered 0.711.

Exact McNemar, paired over the 249 folds, 2026-09-05 configuration against this one:
64 newly correct, 7 newly wrong, **p = 1.26 × 10⁻¹²**.

Final decomposition (12 ablation seeds):

| configuration | gap | full | random ablation | time gap | data loss | chronology |
|---|---|---|---|---|---|---|
| 2026-09-05 | ±5 | 0.841 | 0.777 | 0.668 | −0.064 | −0.109 |
| 2026-09-05 | ±10 | 0.839 | 0.678 | 0.482 | −0.162 | **−0.196** |
| 2026-09-05 | ±20 | 0.826 | 0.642 | 0.514 | −0.183 | −0.128 |
| 2026-09-08 | ±5 | 0.882 | 0.827 | 0.758 | −0.055 | −0.069 |
| 2026-09-08 | ±10 | 0.888 | 0.774 | 0.711 | −0.113 | **−0.064** |
| 2026-09-08 | ±20 | 0.881 | 0.746 | 0.706 | −0.135 | **−0.040** |

## 9. The one test that failed as written (`results/error_direction.json`)

P8 predicted the winner's *errors* would be less date-biased. Measured mean date bias of
errors at ±10: raw + Manhattan −23.82 yr (CI −26.07, −21.35; 94% date-proximate;
n = 129); norm + Manhattan −18.78 yr (CI −21.73, −15.59; 91%; n = 101); norm + cosine
−26.39 yr (CI −29.37, −22.98; 97%; n = 72).

The norm-versus-raw comparison under the same distance measure is readable and supports
the mechanism (−23.8 → −18.8 at ±10, and −23.9 → −13.7 at ±20, non-overlapping CIs). The
winner comparison is not readable: 72 errors against 129 means the residual set is
harder, and the statistic conditions on the outcome. Section 6 is the unconditioned
replacement. Reported here rather than dropped.

## 10. Dating (`results/dating.json`)

Ridge regression (λ = 1) from features to composition year. Leave-one-author-out is the
honest fold structure: authors cluster in time, so leave-one-play-out lets a model date
a play by recognising its author. Year sd 34.1 yr; always guessing the mean gives
MAE 29.9 yr.

| features | MAE (author-out) | R² | MAE (play-out) | R² |
|---|---|---|---|---|
| raw, all 500 | 12.8 yr | +0.780 | 11.3 yr | +0.830 |
| variant-pair features only (98) | 13.3 yr | +0.747 | 10.9 yr | +0.827 |
| raw minus variant features (402) | 12.6 yr | +0.781 | 12.2 yr | +0.797 |
| orthographically normalised, 500 | 14.0 yr | +0.748 | 11.2 yr | +0.829 |
| **random 98 raw features (mean of 10)** | **13.0 yr** | **+0.755** | — | — |

P11 held; **P12 failed**; and the random-98 control shows why the pair has to be read
together. Variant features date a play well, but not distinctively so — the entire
high-frequency lexicon drifts, and normalisation costs only 1.2 yr of dating accuracy.
"Spelling is the date stamp" is therefore too narrow, and section 11 gives the version
that survives.

## 11. Merge groups: what merging does to a feature (`results/repair_test.json`, `results/mechanism.json`)

47 merge groups covering 98 of the 500 raw features.

| statistic | best component | merged |
|---|---|---|
| mean R²(year) | 0.323 | **0.029** |
| mean author F, raw | 12.70 | 6.21 |
| **mean author F, on the date residual** | **5.67** | **5.65** |
| merged less date-loaded than best component | — | 94% of groups |
| merged higher raw author F than best component | — | 11% of groups |
| merged higher **residualised** author F | — | 47% of groups |

Selected groups:

| key | members | R²(year) best→merged | raw F best→merged |
|---|---|---|---|
| down | down / downe | 0.575 → 0.001 | 25.21 → 8.11 |
| vs | us / vs / use ✗ | 0.443 → 0.002 | 17.66 → 4.51 |
| ben | been / beene | 0.436 → 0.121 | 12.96 → 6.17 |
| again | again / againe | 0.375 → 0.012 | 14.15 → 9.41 |
| ever | ever / euer | 0.358 → 0.010 | 14.06 → 8.65 |
| il | ile / i'le / i'll / ill ✗ | 0.311 → 0.047 | 10.46 → 4.56 |
| do | do / doe | 0.281 → 0.014 | 11.22 → 8.69 |
| be | be / bee | 0.219 → 0.014 | 9.25 → 10.20 |
| th | the / thee / th' ✗ | 0.154 → 0.017 | 6.92 → 6.40 |
| don | done / don ✗ | 0.044 → 0.047 | 4.29 → 1.42 |

✗ marks a merge the inspection rejects as wrong.

## 12. Robustness to the key's known defects (`results/mechanism.json`)

| key | ±10 Manhattan | ±10 cosine | ρ |
|---|---|---|---|
| raw | 0.482 | 0.562 | +0.578 |
| full key | 0.594 | 0.711 | +0.206 |
| conservative key (the four ✗ merges refused) | **0.606** | **0.711** | +0.229 |
