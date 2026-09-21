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

---

# Round-3 freeze — Experiment D, the two corrections together

Written after A and C returned, before anything in D was computed.

## Where A and C leave it

A's year-permutation null is unambiguous. Detrending against the **true** dates
raises the author cost A from 32.11 to 49.50, while detrending against **permuted**
dates leaves it at 31.63 (p95 32.95). Real chronology was masking authorial signal
and removing it helps: leave-one-work-out within-register macro 0.718 → 0.769
(leakage-free), cross-register micro 0.169 → 0.356. But the register cost R does
not fall — it rises, 54.71 → 57.64 — and year-matched pairing, which assumes no
functional form, puts R/A at 1.80–2.17 against 1.70 untreated. **Period and
register are two confounds, not one.**

C showed the sink is a shared displacement direction and that subtracting it wipes
the sink out (Lyly 41.0% → 0.2%) while *lowering* apparent accuracy, leaving a
weak signal marginally above its null.

Two things are now untested and one of them could hollow out A's result.

| | prediction | falsifier |
|---|---|---|
| **D1** | Under linear detrending, Lyly's share of the 943 non-dramatic chunks on 27 centroids stays **above 20%** — i.e. detrending does *not* break the sink, so A's cross-register gain is a real gain and not the sink being redistributed | ≤ 20% ⇒ detrending works partly by breaking the sink, and A's cross-register numbers must be re-read as a sink effect |
| **D2** | The two corrections combined (detrend, then register-centre) give an 8-author cross-register macro **below 0.50**, and below the detrended within-register figure of 0.769 | ≥ 0.50 ⇒ the pair of corrections substantially repairs cross-register attribution |
| **D3** | The combined treatment's macro **exceeds** its own author-label permutation p95 | ≤ p95 ⇒ nothing survives that is distinguishable from chance |

**Exploratory, labelled as such, no threshold.** C1 and C2 failed on the cosine
statistic while C2's discriminating clause held. A post-hoc diagnostic — rank
authors by the plain L1 distance from their centroid to the register's centre of
mass, which is what `argmin` actually computes — is reported alongside, explicitly
as a statistic chosen after seeing that cosine underperformed. It is a description
of the sink, not a test of it.

---

# Round-4 freeze — Experiment E, does the repair leak?

Written after D returned, before E was computed.

D2 **failed**, which is the strongest result of the session: detrending and
register-centring together take 8-author cross-register accuracy from micro 0.169
(chance 0.125) to **micro 0.499, macro 0.553**, against a 200-permutation null of
mean 0.134 / p95 0.273. That is a threefold gain on the arm this folder declared
uninterpretable.

**It is worth nothing until one thing is checked.** The centring subtracts the mean
of the *pooled* non-dramatic corpus — which contains the very chunks being
attributed. If most of that gain comes from each author's own chunks contributing
to the mean that is subtracted from them, the method is transductive leakage and
cannot be used on a real questioned document.

The honest version: estimate the register displacement from **other authors only**.
For every author a, centre a's non-dramatic chunks on the mean of the non-dramatic
chunks of the other seven. This is exactly what a practitioner can do — hold a
reference corpus of other writers in the questioned register — and it cannot see
the questioned author at all.

| | prediction | falsifier |
|---|---|---|
| **E1** | Leave-one-author-out centring keeps 8-author cross-register micro **above 0.40** (pooled centring 0.499; uncorrected 0.169) | ≤ 0.40 ⇒ a large part of D's gain is transductive and the honest figure is lower |
| **E2** | It stays **above its own 200-permutation null p95** | ≤ p95 ⇒ nothing survives |
| **E3** | It stays **below** the detrended within-register figure computed on the 8-author panel alone | ≥ ⇒ cross-register is as good as within-register, which would be extraordinary and almost certainly a bug |
| **E4** | *Held-out arm.* On the 19 civic pageants set aside by the 2026-09-17 session, the combined correction with leave-one-author-out centring raises Middleton + Heywood + Jonson's joint recovery of their own 25 chunks **above 0.10**, the upper bound that session's power analysis placed on the uncorrected rate | ≤ 0.10 ⇒ the repair does not transfer to the third register and its scope is narrower than the non-dramatic arm suggests |

**Known bug to fix before E is reported**, found while reading D's output: D's
within-register line passed the 27-author document set with the 8-author label
list, so its `micro` of 0.234 is diluted by nineteen authors who cannot be
correct. The macro (0.791) is over the panel and is unaffected. E recomputes the
within-register comparison on panel documents only.

---

# Round-5 freeze — Experiment G, the centring must be author-blind

Written after F returned, before G was computed.

E1 held and leave-one-author-out centring beat pooled centring (micro 0.577 against
0.499 on the 8-author panel). Reading the algebra rather than the number explains
why, and the explanation is a problem. Writing `m` for the pooled non-dramatic
mean, `m_a` for author a's own mean and `n_a` for his chunk count out of N, the
shift subtracted from a's chunks is

    mean(others) = (N·m − n_a·m_a) / (N − n_a)

so centring subtracts it and leaves

    z − m + (n_a / (N − n_a)) · (m_a − m).

The second term **adds back a multiple of the author's own deviation**, and the
multiplier grows with how much of the questioned corpus he owns. That is not
leakage of the training labels, but it does use knowledge of which test chunks
share an author, and it amplifies by an amount set by corpus arithmetic rather
than by style. Heywood owns 430 of 943 chunks and gets a multiplier of 0.84;
Jonson owns 8 and gets 0.009. A method whose strength depends on that is not a
method.

The author-blind version subtracts, from each chunk, the mean of every
non-dramatic chunk belonging to a **different work** — no author grouping used
anywhere, and available to any practitioner holding a reference corpus in the
questioned register. Leave-one-work-out, not leave-one-author-out.

| | prediction | falsifier |
|---|---|---|
| **G1** | Author-blind leave-one-work-out centring keeps 27-author non-dramatic micro **above 0.30** (uncorrected 0.141; LOAO 0.399) | ≤ 0.30 ⇒ most of the gain needed author grouping, and the honest headline is much smaller |
| **G2** | It stays **above its own 200-permutation null p95** | ≤ p95 ⇒ nothing survives that is distinguishable from chance |
| **G3** | The gap between author-blind and leave-one-author-out centring is **smaller** than the gap between author-blind and uncorrected — i.e. most of the correction's value comes from removing the shared displacement, not from the amplification term | ⇒ the amplification, not the centring, was doing the work |

Whichever way G falls, the **author-blind** figure, not the leave-one-author-out
figure, is the one this session reports as its headline.
