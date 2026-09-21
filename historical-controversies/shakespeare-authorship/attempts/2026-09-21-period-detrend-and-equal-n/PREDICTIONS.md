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

---

# Round-2 freeze — Experiment C, the sink mechanism and an attempted repair

Written after Experiment B returned and **before any quantity in Experiment C was
computed.** B is therefore exploratory evidence for C's hypothesis and C's tests
are prospective with respect to the cosine alignments, the pageant direction and
the register-centred attribution, none of which has been calculated. Committed in
its own commit ahead of C's results.

## Where B leaves the problem

B refuted its own hypothesis. Equal training data changes nothing: Lyly's share of
the 943 non-dramatic chunks is 41.5% ± 3.0% under 41-chunk centroids against 41.0%
at full training, concentration is flat, and the trio's own-pageant recovery stays
at 0.006 ± 0.014. Crucially, training size still predicts centroid L1 norm at
−0.554 *after* every author is given 41 chunks, so the norm differences are not a
1/n sampling artefact — they are a property of these authors.

So the sink is real, stable and specific: Lyly takes ~41% in every one of 50
subsamples, while under label-shuffling no author is favoured (Lyly 3.0%, near
1/27 = 3.7%). Two prior candidate causes are now dead — prose-ness (2026-09-17)
and training-set size (B).

## The hypothesis

Purely geometric. In drama-scaled z-space the drama cloud is centred near the
origin. Non-dramatic chunks are displaced from it along a **common direction m**
— the register displacement — because register moves function-word rates the same
way for everybody. Under L1 nearest-centroid, a test point far out along m is
captured by whichever author's centroid lies furthest along m. Absorption should
therefore be predicted by the alignment of an author's centroid with m, and by
nothing else.

This also predicts *why the identity of the sink is not stable*: pageants are a
different register with a different displacement direction, so a different author
wins.

| | prediction | falsifier |
|---|---|---|
| **C1** | Across the 27 authors, Pearson correlation between cos(centroid, m_nondrama) and non-dramatic absorption share is **> +0.70** | ≤ +0.70 ⇒ alignment is not the mechanism |
| **C2** | The same alignment computed against the *pageant* displacement direction predicts pageant absorption at **> +0.70**, and Peele's pageant-direction alignment **exceeds Lyly's**, reproducing the observed switch of sink identity from a quantity computed without reference to the outcome | either clause fails ⇒ the mechanism does not explain the instability |
| **C3** | *The repair.* Subtracting the test register's own mean from every test document before attribution (register-centring) drops Lyly's share **below 15%** | ≥ 15% ⇒ removing the common displacement does not break the sink |
| **C4** | *The claim that matters.* Even with the sink broken, register-centred cross-register macro on the 8-author panel stays **below 0.50**, i.e. well short of the 0.717 within-register figure | ≥ 0.50 ⇒ a simple centring repairs cross-register attribution, the folder's negative claim reopens, and this is the most useful result in the folder |
| **C5** | *Null.* Register-centred attribution is scored against 200 author-label permutations; the observed macro exceeds the null p95 | observed ≤ null p95 ⇒ whatever centring recovers is not authorship |

C3 and C4 are deliberately set against each other. C3 says the sink is an artefact
of a shared displacement and can be removed; C4 says removing it does not give the
method back. If both hold, the folder's negative conclusion survives a genuine
attempt to repair it, which is a far stronger position than never having tried.
