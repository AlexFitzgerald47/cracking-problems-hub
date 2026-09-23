# Frozen predictions — 2026-09-23 third-register holdout

**Frozen at:** corpus built, `expH_holdout.py` written, **no attribution run on the
holdout arm and no result seen**. Committed before the first execution of
`expH_holdout.py`; the commit that adds this file adds the runner too, and the
results commit comes after.

## What has been seen at freeze time

The holdout arm's *composition* only: 496 chunks from 56 texts by 11 panel
dramatists (Behn 171, Settle 100, Dryden 68, D'Urfey 66, Crowne 51, Shirley 13,
Ford 9, Glapthorne 7, Otway 4, Shadwell 4, Peele 3), 1589–1700, none of whom
contributed any of the 943 non-dramatic chunks the 2026-09-21 correction was
developed on. Also seen: the drop ledger (24 performance texts by markup, 83
under the 3,000-word floor, 9 posthumous, 2 miscellanies, 1 translation) and the
two within-author 8-gram overlaps that sit under the inherited 0.30 duplicate
threshold (Behn A27315/A27316 0.214; Settle A59344/A59303 0.204). **No distance,
no attribution and no accuracy has been computed on these chunks.**

## The claim under test

2026-09-21 established, on 943 non-dramatic chunks by eight dramatists, that
detrending against document date plus author-blind leave-one-work-out centring
takes 27-candidate cross-register attribution from micro 0.141 to 0.358
(permutation p = 0.000, within-register reference 0.740). It is unvalidated
anywhere else. The handover's reopening condition is this arm.

## Predictions

| # | Prediction | Fails if |
|---|---|---|
| **P1** | **Primary.** On the 27-author panel, `detrend + centre` reaches micro **≥ 0.25** on the holdout arm, with work-blocked permutation **p < 0.05**. | micro < 0.25, or p ≥ 0.05 |
| **P2** | The uncorrected cross-register failure reproduces on new authors: uncorrected micro **< 0.20**. | ≥ 0.20 |
| **P3** | The sink reproduces and the correction breaks it: uncorrected `max_share` **≥ 0.25**, and corrected `max_share` < uncorrected. | either half fails |
| **P4** | The correction's absolute gain is **≥ 0.15** micro. | < 0.15 |
| **P5** | It still fails for some authors: **≥ 2** of the 11 present authors score < 0.10 corrected per-author accuracy. | ≤ 1 |
| **P6** | Recovery is not simply training mass: Spearman(per-author chunk count, corrected per-author accuracy) **< +0.5**. | ≥ +0.5 |
| **P7** | **Decomposition.** Centring carries more of the gain than detrending: `centre only` micro − uncorrected > `detrend only` micro − uncorrected. | the reverse |
| **P8** | **Control.** Permuting the test chunks' years before detrending costs accuracy: permuted-year `detrend + centre` micro is **≥ 0.02 lower** than with true years. | permuted ≥ true − 0.02 |
| **P9** | **Robustness.** The result does not rest on the weakly attributed texts: on the `named_on_title` subset, `detrend + centre` micro is within **0.10** of the full-arm figure. | differs by more than 0.10 |
| **P10** | **Handover item 2, tested out of sample.** Pooling these 11 authors with the original 8 (n = 19), the register **date gap** \|mean year(non-drama) − mean year(drama)\| predicts corrected per-author accuracy better than the log ratio of non-dramatic to drama chunks: rho(date gap, accuracy) < 0 **and** \|rho(date gap)\| > \|rho(log ratio)\|. | either half fails |

## What a failure means

P1 failing is the answer the folder asked for: the 0.358 gain would be
corpus-specific, developed and validated on the same eight authors, and the
Junius cross-reference built on it in `board/log/2026-09-21-confound-gaps-are-correctable.md`
would have to be narrowed. P1 passing with P5 also passing is the expected
shape: a real but partial correction that some authors do not get back.
