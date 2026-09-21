# Frozen predictions — 2026-09-21 session

Written **before** any new distance, centroid or attribution was computed, and
committed in its own commit ahead of the results commit so the freeze is checkable
in `git log`. The only things run before this file was written were
`build_corpus.py`, `analysis.py` and `wide_panel.py` **unchanged**, as a
reproduction check on the 2026-09-17 pipeline (see `REPRODUCTION.md`).

This session runs HANDOVER items 1 and 2.

---

## Reproduction gate (run first, reported in `REPRODUCTION.md`)

**R0.** Rebuilding the corpus from `fetch_tcp.py` + `build_corpus.py` on a fresh
container reproduces `data/manifest.json` byte-identically, and `analysis.py` and
`wide_panel.py` reproduce every number quoted in
`../2026-09-17-register-self-match/RESULTS.md` to the printed precision.

*Status at freeze time: **held**. 74 non-dramatic texts kept, 943 non-dramatic and
3,062 drama chunks; cells 415.80 / 447.92 / 470.52 / 486.20; within-register macro
0.717; cross-register macro 0.337; null mean 0.119, p95 0.222, max 0.315; Lyly
41.0%; Spearman +0.039. Identical.*

---

## Experiment A — regress period out (HANDOVER item 1)

**Method.** For each of the 500 vocabulary features, fit ordinary least squares of
relative frequency on document year over a reference set, subtract the fitted value
from every document, then z-score the residuals on the same reference set and
recompute the four distance cells and the attribution experiments. Primary
reference = drama chunks only (the real scenario: you hold a body of plays);
sensitivity = pooled corpus. A quadratic-in-year variant is run as a second
sensitivity because the corpus spans 1578–1691 and a linear trend may be
mis-specified.

**Nonparametric companion.** Year-matched pairing: recompute the four cells using
only document pairs whose years differ by at most W years, for W in {5, 10, 20}.
This holds period constant without assuming any functional form. Same-work pairs
stay excluded throughout.

The quantity of interest throughout is the **P1 margin**

    margin = mean(same author, cross register) − mean(different author, same register)

which is **+22.60** undetrended (470.52 − 447.92).

| | prediction | falsifier |
|---|---|---|
| **A1** | Under drama-fit linear detrending the margin stays positive and retains at least half its undetrended value, i.e. **≥ +11.3** | margin < +11.3 ⇒ period and register are substantially the same effect |
| **A2** | Under year-matched pairing at W = 5 the margin is still **> 0** | margin ≤ 0 at W = 5 ⇒ the register gap is a period artefact |
| **A3** | Cross-register attribution macro on the 8-author panel after detrending stays **< 0.50** (it is 0.337 now) | ≥ 0.50 ⇒ detrending materially rescues cross-register attribution |
| **A4** | *Sanity control.* Within-register leave-one-work-out macro after detrending stays **≥ 0.60** (0.717 now) | < 0.60 ⇒ the detrend is destroying authorial signal generally, and A1/A3 say nothing about register |

**A5 (decomposition, no threshold — reported, not scored).** Using year-matched
pairs, quote in one table what each variable costs in Delta units on this corpus:
changing author within a register; changing register within an author; and widening
the year gap from ≤5 to ≥20 within an author and register. The board has two
confounds measured on different scales in this folder; this puts all three on one.

---

## Experiment B — equal-N training sets (HANDOVER item 2)

**Method.** On the 27-author panel, subsample every author's drama chunks to a
common N = the smallest author's count, rebuild centroids from the subsample only,
attribute all 943 non-dramatic chunks, and repeat over 50 independent subsamples
with a fixed seed. Report the mean and spread of every statistic.

Full-training baselines to beat, read off `wide_panel.json` at freeze time and
fixed here so no threshold can move afterwards: Lyly's share **41.0%**; authors
absorbing **exactly** zero **12 of 27**; Herfindahl concentration of the 27
non-dramatic prediction shares **0.2324**.

*Audit note made at freeze time, before any new computation.*
`../2026-09-17-register-self-match/RESULTS.md` says "fourteen of the twenty-seven
dramatists absorb nothing at all". The stored shares say **twelve** absorb exactly
nothing; Dryden and Lee each absorb one chunk of 943 and print as 0.1%. The
argument is unaffected but the number is wrong by two, and the corrected figure is
used as the B2 baseline.

| | prediction | falsifier |
|---|---|---|
| **B1** | Lyly's mean share of non-dramatic chunks under equal-N falls **< 25%** | ≥ 25% ⇒ the sink is not mainly a training-size artefact |
| **B2** | The mean number of authors absorbing zero non-dramatic chunks falls **< 12** | ≥ 12 ⇒ ditto |
| **B3** | Mean concentration falls by at least a third, i.e. **< 0.1550** | ≥ 0.1550 ⇒ ditto |
| **B4** | *The load-bearing one.* Cross-register macro on the 8-author panel under equal-N stays **< 0.50** | ≥ 0.50 ⇒ equal-N rescues cross-register attribution and `RESULTS.md` needs rewriting, not amending |
| **B5** | *Null.* With author labels shuffled among drama chunks and equal-N centroids, mean concentration is **lower** than the observed equal-N concentration | null ≥ observed ⇒ even the residual sink is centroid noise |

**Standing commitment.** If B1–B3 hold, the 41% / 0% figures in
`../2026-09-17-register-self-match/RESULTS.md` are a training-size artefact and
this session says so plainly in `PROGRESS.md` and amends that file's status —
without deleting it. If B4 fails, the folder's negative claim reopens.

**Note on what B can and cannot overturn.** B is about the *sink*, which is a
property of the centroids. It cannot touch the four distance cells (A1/A2), which
involve no centroids at all, nor the held-out pageant zeros, which were computed
against the same full-training centroids and will be re-run under equal-N as B6.

**B6.** Re-run the held-out civic-pageant arm under equal-N centroids. Prediction:
Middleton, Heywood and Jonson jointly recover **< 25%** of their own 25 pageant
chunks (they recover 0 of 25 at full training; the power analysis bounds the true
rate at about ≤10%, so 25% is a genuine risk line, not a safe one).
