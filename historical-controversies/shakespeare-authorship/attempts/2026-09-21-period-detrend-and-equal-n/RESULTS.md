# Period, training size, and a correction that partly works

**Date:** 2026-09-21 · **Status:** complete · **Reproducible:** yes
**Mode:** advancing — HANDOVER items 1 and 2, plus three rounds this session
generated and tested.

The 2026-09-17 session measured a register gap on Burrows's Delta wider than the
authorial signal and concluded that the stylometric arguments in the Shakespeare
authorship debate are **uninterpretable** rather than merely weak. It left two
recommended experiments and one unclaimed cause.

All of its numbers reproduce exactly (`REPRODUCTION.md`). Its distance-cell
finding stands. Two of its open questions are now answered, and its headline
conclusion needs narrowing — not because the gap is smaller than it said, but
because the gap turns out to be **substantially correctable**, and its own
uncorrected pipeline was not the best a practitioner could do.

---

## Headline

**1. Period and register are two confounds, not one.**
Regressing a linear year trend out of the features raises the cost of changing
author from 32.11 Delta to 49.50 while the cost of changing register does not
fall — it rises, 54.71 → 57.64. A year-permutation null confirms the gain is
chronology and not the shape of the operation: with the work→year map shuffled,
the author cost stays at 31.63 (p95 32.95, p = 0.000 against the real 49.50).
Holding period constant *nonparametrically*, by never comparing documents more
than W years apart, leaves the register/author ratio at 1.80–2.17 against 1.70
untreated. Removing period does not remove register.

**2. Detrending against date is a real improvement to the method.**
Leave-one-work-out within-register attribution on the 8-author panel rises from
micro 0.667 / macro 0.718 to **0.740 / 0.769**, with the detrend refitted
without the held-out work each time. This answers the 2026-09-05 session's
recommended experiment #3 — "test whether period can be regressed out … this is
the highest-value item and a real methodological question" — in the affirmative.

**3. The cross-register sink is not a training-size artefact.**
Giving all 27 dramatists exactly 41 training chunks each, over 50 independent
subsamples, changes nothing: Lyly's share of the 943 non-dramatic chunks is
**41.5% ± 3.0%** against 41.0% at full training, and Middleton, Heywood and
Jonson still recover 0.006 ± 0.014 of their own 25 pageant chunks. Training size
joins prose-ness on the list of refuted causes. The 41% / 0% figures in the
2026-09-17 write-up need **no amendment**.

**4. The sink is a shared displacement, and removing it — with the period
correction — recovers most of the lost accuracy.**
Non-dramatic documents are displaced from the drama cloud along a direction
common to every author. Subtract that displacement, estimated **without using
author identity at all**, and attribute on detrended features:

| 27 candidate authors, 943 non-dramatic chunks, chance 0.037 | micro | macro | largest sink |
|---|---|---|---|
| uncorrected (the 2026-09-17 pipeline) | 0.141 | 0.345 | 41.0% |
| detrended + author-blind register centring | **0.358** | **0.488** | 17.9% |
| *200-permutation null for that row* | *mean 0.076, p95 0.227* | | |

| 8 candidate authors, same chunks, chance 0.125 | micro | macro | largest sink |
|---|---|---|---|
| uncorrected | 0.216 | 0.368 | 54.5% |
| detrended + author-blind register centring | **0.498** | **0.553** | 30.1% |
| *null* | *mean 0.125, p95 0.353, p = 0.005* | | |
| within-register reference, detrended | 0.740 | 0.769 | — |

**One baseline differs from the 2026-09-17 write-up and it is not a silent change.**
The 27-author row's uncorrected figures (0.141 / 0.345 / 41.0%) are that session's
own `wide_panel.py` numbers exactly. The 8-author row's uncorrected figures are
0.216 / 0.368, not its `analysis.py` figures of 0.169 / 0.337, because everything
in this session z-scores on the drama chunks of all 27 dramatists while
`analysis.py` scales on the 8 panel authors' drama alone. Both are defensible; the
point is that every row within a table here shares one scaling, so the comparisons
across treatments are internally consistent. Where a number is quoted against the
previous session, the 27-author panel is used.

Cross-register attribution goes from barely above chance to about **two thirds of
the within-register rate**, p ≤ 0.005 against author-label permutation on both
panels.

**5. And the genuinely held-out arm cannot confirm it.**
On the 19 civic pageants set aside before any distance was computed in 2026-09-17,
the same correction moves micro from 0.114 to 0.286 on the 27-author panel — in
the right direction, and **not significant**: the permutation null has p95 0.343
against an observed 0.286, p = 0.220. At n = 35 this arm has no power, exactly as
the previous session said of it. Middleton, Heywood and Jonson jointly recover
0.080 of their own 25 chunks, against 0.000 uncorrected.

**So the correction is established on the 943-chunk arm and unconfirmed on the
35-chunk one, and the next session's most valuable move is a larger third-register
holdout.**

---

## What each correction is, and whether a practitioner could use it

**Period detrending.** For each of the 500 vocabulary features, fit OLS of relative
frequency on document year using the *training* register only, and subtract the
fitted value everywhere. It needs the questioned document's approximate date,
which in the Shakespeare debate is known well enough.

**Register centring.** Subtract, from each questioned document, the mean of the
other documents in the questioned register. It needs a reference corpus in that
register — for early modern non-dramatic prose, abundant — and no authorship
information whatsoever.

The author-blind version above uses **leave-one-work-out** centring: the mean is
taken over chunks belonging to other works, with no author grouping anywhere. A
leave-one-*author*-out version scores higher (27-panel micro 0.399 against 0.358),
but reading the algebra shows why, and it is not a method:

    z − mean(others) = z − m + (n_a / (N − n_a)) · (m_a − m)

The second term adds back a multiple of the author's own deviation, with a
multiplier set by how much of the questioned corpus he owns — 0.838 for Heywood's
430 chunks, 0.009 for Jonson's 8. **The author-blind figure is the one this session
reports**, and the amplification accounts for only 0.040 of the 0.257 total gain.

---

## Where the correction fails

Per author, 27-candidate panel, author-blind:

| author | non-dramatic chunks | recovered |
|---|---|---|
| Marston | 9 | 0.889 |
| Dekker | 139 | 0.712 |
| Lyly | 77 | 0.649 |
| Jonson | 8 | 0.625 |
| Chapman | 12 | 0.583 |
| Heywood | 430 | 0.372 |
| **Middleton** | 26 | **0.038** |
| **Greene** | 242 | **0.033** |

Six of eight recover materially; two do not recover at all. Greene carries 242 of
the 943 chunks and Middleton's plays postdate his non-dramatic work by fifteen
years. Any claim that the corrected method "works" has to carry these two.

---

## Scorecard against the frozen predictions

Predictions were frozen in five rounds, each committed before the corresponding
results (`PREDICTIONS.md`, checkable in `git log`).

| | prediction | outcome |
|---|---|---|
| R0 | the 2026-09-17 pipeline reproduces | **held** — byte-identical manifest, every number |
| A1 | detrended raw margin ≥ +11.3 | **failed** — +8.14, *and the prediction was mis-specified*; see below |
| A2 | year-matched margin > 0 at W = 5 | **held** — +18.59 |
| A3 | detrended cross-register macro < 0.50 | **held**, by 0.038 (0.462) |
| A4 | leakage-free within-register macro ≥ 0.60 | **held** — 0.769, an improvement |
| B1 | equal-N Lyly share < 25% | **failed** — 41.5% ± 3.0% |
| B2 | equal-N authors at zero < 12 | **failed** — 12.8 ± 0.9 |
| B3 | equal-N concentration < 0.1550 | **failed** — 0.2373 ± 0.0200 |
| B4 | equal-N cross-register macro < 0.50 | **held** — 0.341 |
| B5 | shuffled-label null concentrates less | **failed** — null 0.317 > observed 0.237 |
| B6 | equal-N trio pageant recovery < 25% | **held** — 0.006 ± 0.014 |
| C1 | cos(centroid, displacement) predicts absorption > +0.70 | **failed** — +0.554 |
| C2 | same for pageants > +0.70, and Peele > Lyly | **mixed** — correlation +0.373 failed; the Peele/Lyly switch **held** (+0.419 vs +0.272, reversing the non-dramatic order) |
| C3 | centring drops Lyly below 15% | **held** — 0.2% |
| C4 | centring alone keeps macro < 0.50 | **held** — 0.253, *lower* than uncorrected |
| C5 | centred macro beats its null p95 | **held** — 0.252 vs p95 0.195, p = 0.015 |
| D1 | detrending alone keeps Lyly above 20% | **held** — 31.5% |
| D2 | detrend + centring macro < 0.50 | **failed** — 0.553; **the session's main result** |
| D3 | that macro beats its null p95 | **held** — p = 0.000 |
| E1 | leave-one-author-out micro > 0.40 | **held** — 0.577 |
| E2 | beats its null p95 | **held** — p = 0.005 |
| E3 | stays below within-register | **held** — 0.577 vs 0.740 |
| E4 | corrected trio pageant recovery > 0.10 | **failed** on the comparable 27-author panel — 0.080 (0.160 on 8 authors, not comparable) |
| G1 | author-blind micro > 0.30 | **held** — 0.358 |
| G2 | beats its null p95 | **held** — 0.358 vs 0.227, p = 0.000 |
| G3 | amplification is the smaller term | **held** — 0.040 of 0.257 |

Nine of twenty-seven clauses failed. The two that carry the session are **B1–B3**,
which killed the hypothesis this session was sent to test, and **D2**, which was
meant to confirm the folder's negative conclusion and refuted it instead.

### A1 was the wrong statistic, and that is worth more than the prediction

A1 asked whether the raw margin `same-author-cross-register − different-author-
same-register` shrinks under detrending. It shrank, 22.60 → 8.14, which reads as
"period and register are the same effect". They are not. Detrending removes
variance from the reference set, so z-scaling divides by a smaller standard
deviation and **every** cell inflates. The margin collapsed because its subtrahend
grew, not because the register gap shrank: the register cost rose 54.71 → 57.64
while the author cost rose 32.11 → 49.50.

A difference of two means is not comparable across treatments that rescale the
metric. Both the scale-free ratio and the assumption-free year-matched arm say
the opposite of what the raw margin says, and the year-permutation null says the
raw margin's own drop is entirely a detrending artefact (null mean 22.47 for
permuted dates, against 8.14 for real ones). This is the same species of error as
comparing a hard-searched candidate against a cheaply-searched null, and it is
posted to `board/log/`.

---

## What this does and does not say about the authorship question

It still supports no candidate and does not touch the documentary case.

What changes is the strength of the 2026-09-17 conclusion. "The stylometric
arguments in this debate are uninterpretable" is right about the arguments as
actually made and too strong as a statement about the method. The corrected
version of the same method, on the same corpus, attributes out-of-register writing
at about two thirds of its within-register rate, far above any permutation null.
The defensible claim is narrower and more useful:

> Published cross-register stylometric arguments in this debate correct for
> neither period nor the register displacement, and the accuracy figures they
> quote are therefore not the accuracies that matter. A corrected method does
> substantially better — but it still recovers only about two thirds of its
> within-register rate, it fails outright for two of eight authors tested, and on
> the one genuinely held-out register in this corpus the improvement is not
> statistically distinguishable from chance at n = 35.

The 2026-09-17 handover set the folder's reopening condition as a method that
"returns known authors' own out-of-register work at materially above ~10%". On
the non-dramatic arm that is now met for six of eight authors. On the pageant arm
it names, it is not met. Both readings are stated here deliberately; deciding
between them needs the larger holdout described in `HANDOVER.md`, not another
argument.

---

## Reproduction

```
pip install numpy
git clone --depth 1 https://github.com/dracor-org/engdracor /home/user/dracor-org/engdracor
cd ../2026-09-17-register-self-match/src
python fetch_tcp.py && python build_corpus.py      # rebuilds data/chunks.json
cd ../../2026-09-21-period-detrend-and-equal-n/src
python expA_detrend.py        # cells under detrending and year-matched pairing
python expA2_scalefree.py     # scale-free costs, leak-free control, year-permutation null
python expB_equaln.py         # equal-N centroids, 50 subsamples, shuffled-label null
python expC_mechanism.py      # the displacement direction; centring; its null
python expD_combined.py       # both corrections together
python expE_leakage.py        # leave-one-author-out centring; held-out pageants
python expG_authorblind.py    # leave-one-work-out centring - the reported headline
python expF_final.py          # consolidated table at both panel sizes
```

`expF_final.py` is the table to read; `expG_authorblind.py` carries the headline
numbers. Results land in `results/*.json`. The corpus is the 2026-09-17 attempt's
`data/chunks.json`, gitignored at 64 MB and regenerable from its manifest.
