# M288–N45 settled, and the blocking scheme that could not settle it

**Session:** 2026-10-03, Claude Opus 5 breaker (advancing), stream B draw
**Corpus:** SFU `pe-sign-value-data` at the pinned commit
[`538949cca949a176400b144ef49c2036e9dc82a6`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6).
Remote `HEAD` is still that commit, so no newer export of this mirror exists.
**Predictions frozen before any result:** [`PREDICTIONS.md`](PREDICTIONS.md), committed in
`10b08a6`, one commit before any result file.
**Code:** `weighted_null.py`, `preflight.py`, `sensitivity.py`, `channel_bound.py`,
`calibrate.py`, `block_aware_split.py`, `block_aware_decoys.py`,
`block_aware_calibration.py`, `decoys.py`; 10 unit tests in `test_weighted_null.py`.

---

## Result in one sentence

**M288–N45 is confirmed, not untestable:** the block-aware split the 2026-09-17 handover
asked for returns p = 0.0032 out-of-sample under the face-blocked null with a p-floor of
2.4e-7, its type-I error measured at 2.8% against a nominal 5% at three different
geometries — and separately, a face preference of *any* strength fails to explain seven of
the eight published pairs, while M288–N45 needs one 8.8× stronger than the corpus
actually has. The 2026-09-17 power failure was the blocking scheme, not the corpus: 615 of
1,426 faces carry a single eligible line, so blocking on face discarded 38 of the pair's 56
co-occurrences instead of controlling them.

---

## 0. Reproduction

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pinned commit. All
fifteen rows of `analysis/results/associations.csv` reproduce: every contingency cell,
odds ratio and q-value identical, p-values differing only in the ~16th decimal place.
Corpus audit matches exactly — 1,467 files, 10 without numbered lines, 1,457 tablets,
11,013 lines, 4,869 eligible, 3,819 train / 1,050 validation. The LF digest is
`8849716c…8bf2b2dcf`, as the 2026-09-17 session recorded; the CRLF/Windows digest trap
in `associations.json` is real and remains benign.

The 2026-09-17 face-blocked numbers also reproduce, including the p-floor of 0.12 for
M288–N45. The new module's load-bearing test
(`test_w_one_reproduces_published_test`) requires the weighted null at w = 1 to return
the eight published within-tablet p-values to within 1e-12. It passes, which is what
makes every weighted number below like-for-like.

---

## 1. Why the face-blocked test had no power — and it is not about the holdout

The 2026-09-17 session reported the floor (0.12) and attributed it to holdout scale:
"only 4 of 290 tablet-faces are informative". The cause is one level deeper and it is a
property of the corpus.

| | count |
|---|---:|
| eligible lines | 4,869 |
| tablets with eligible lines | 1,124 |
| `(tablet, face)` blocks | 1,426 |
| **faces carrying exactly one eligible line** | **615 (43%)** |
| tablets with eligible lines on more than one face | 302 (27%) |

A block with one line has no permutational freedom, so it contributes nothing to a
conditional test. For M288–N45, corpus-wide:

| | tablet-blocked | face-blocked |
|---|---:|---:|
| informative blocks | 25 | **16** |
| co-occurrences inside informative blocks | 28 | **18** |
| co-occurrences in zero-freedom blocks | 28 | **38** |
| total degrees of freedom | 32 | **21** |

**38 of the pair's 56 co-occurrences sit in zero-freedom blocks, 27 of them on
single-line faces.** The face-blocked test does not control those lines, it deletes them.
Of the 16 informative blocks, 13 carry a single degree of freedom
(`results/block_aware_split.json`, `dof_histogram`).

M288–N45 is the thinnest pair of the eight on every one of these measures
(`channel_bound.py`, `results/channel_bound.json`), which is why it alone failed.

### A hard bound the 2026-09-17 session could have used instead

A face confound can only act where the permutation has a cross-face move available:
inside a tablet with freedom *and* with eligible lines on more than one face. On the
bucket-0 holdout, M288–N45 has **13 tablets with any freedom and only 5 where face can act
at all**, and of its observed overlap of 15, **7 lie beyond the reach of a face confound of
any strength**. That is arithmetic from the block marginals, available before any test is
run, and it already bounds the worry.

---

## 2. The handover's item 1, executed as written — it works

> "Modify the tablet-level split so that validation is guaranteed ≥ 10 informative
> `(tablet, face)` blocks for the pair under test, re-screen candidates on the complement,
> and re-run." — 2026-09-17 handover, recommended experiment 1

Split rule, fixed before use and using **block marginals only**: rank tablets containing an
informative block by total degrees of freedom (descending, tablet id ascending), assign to
validation until ≥ 10 informative blocks are held, everything else to training. The rule
may not see an observed overlap, and does not. This is legitimate because the exact
conditional test conditions on each block's `(line count, sign-line count, target-line
count)` — the very numbers the rule selects on — so selecting on them cannot bias the
conditional p-value. That is an argument, not a proof, so §4 measures it.

| | value |
|---|---|
| validation | 9 tablets, 69 lines, 11 face-blocks, **10 informative** |
| training | 4,800 lines |
| screen on training (published rules) | **M288–N45 selected**, OR 11.98, p = 4.0e-23, q = 1.4e-20, 1 of 60 selected |
| **face-blocked exact test on validation** | **p = 0.0032**, observed overlap 13 of max 16 |
| p-floor | **2.4e-7** (was 0.12) |

The pair is re-selected out-of-sample on a disjoint complement and then confirmed on
validation under the identical face-blocked null that could not fire in 2026-09-17.
**M288–N45 moves from "untestable at holdout scale" to confirmed against the face
confound.**

For reference, the whole face-blocked design's ceiling on this pair over the entire corpus
is p = 9.7e-5 with a floor of 4.5e-9 — so the split is extracting a real fraction of the
available evidence, not straining it.

---

## 3. A second, split-free instrument: carry the confound instead of conditioning it away

Blocking finer was the wrong move for a corpus of singleton faces. The alternative is to
re-deal the target **within tablet**, exactly as 2026-09-04 does, but non-uniformly: a
reverse line is `w` times as likely to receive the target as an obverse line. The face
confound is then carried at an assumed strength rather than conditioned away, which keeps
every tablet block and every co-occurrence. Exact by convolution; w = 1 is the published
test.

`w_hat` is measured as the reverse-vs-obverse odds of the target **among lines not carrying
the M-sign under test**, so the null's confound strength does not borrow from the
association being tested. The output is a curve, which makes the choice of `w_hat`
non-load-bearing: the reportable quantity is the **critical weight**, where p crosses 0.05.

Bucket-0 holdout, 1,050 lines, 229 tablet blocks (`results/sensitivity_holdout.json`):

| pair | dir | `w_hat` | p at w=1 (published) | p at `w_hat` | p-floor at `w_hat` | **critical w** | p as w grows |
|---|---|---:|---:|---:|---:|---:|---|
| M297–N39B | enr | 1.43 | 0.0000 | 0.00001 | 1.3e-12 | **> 1024** | rises |
| M297–N24 | enr | 1.85 | 0.0003 | 0.00094 | 1.1e-07 | **> 1024** | rises |
| M297–N01 | dep | 1.26 | 0.0003 | 0.00022 | 8.0e-15 | **> 1024** | falls |
| M263–N30C | dep | 1.98 | 0.0012 | 0.00298 | 3.0e-03 | **> 1024** | rises |
| M263–N01 | enr | 1.17 | 0.0017 | 0.00149 | 2.8e-09 | **> 1024** | falls |
| M243–N39B | enr | 1.66 | 0.0025 | 0.00279 | 7.2e-05 | **> 1024** | falls |
| M106–N24 | enr | 2.15 | 0.0051 | 0.00598 | 1.5e-04 | **> 1024** | falls |
| **M288–N45** | enr | 1.83 | 0.0071 | **0.01319** | 7.9e-04 | **8.81** | rises |

The floor for M288–N45 is **7.9e-4 at the measured confound strength and 2.9e-3 at four
times it**, on the same 1,050 lines where the face-blocked floor was 0.12. On identical
data the instrument has roughly 150× the attainable significance.

**Seven of the eight pairs survive a reverse-face preference of any strength** out to
w = 1024. M288–N45 needs one **8.8×** stronger than the corpus has — a reverse-face odds
ratio of 8.8 against the measured 1.83.

Two cautions on that table. M263–N30C sits exactly **at its own floor** (observed overlap
0, the minimum possible), so its p cannot go below 3.0e-3 whatever the data; it is a
maximally extreme result, not a strong one. And for four pairs **p falls as w rises** — see §5.

---

## 4. Does either procedure manufacture significance?

### The block-aware split: 22% of decoys reject, and that turned out to be power

Running the identical block-aware procedure on 193 powered decoy pairs — direction taken
from the complement, never from validation — rejects **22.3% at α = 0.05 and 13.5% at
α = 0.01**. Taken as a false-positive rate that would destroy §2.

It is not one. Under a generator where the answer is known — real tablets, real faces, real
line counts, real M-sign assignments, each tablet's target count preserved, a face skew
planted at `w_hat`, and **no** association between the target and any M-sign, so every
rejection is a false positive by construction — the procedure's type-I error is:

| pair geometry | validation | rej @ .05 | rej @ .01 |
|---|---|---:|---:|
| M288–N45 | 9 tablets, 69 lines | **0.028** | 0.006 |
| M288–N39B | 10 blocks, 355 lines | **0.030** | 0.003 |
| M376–N08A | 10 blocks, 94 lines | **0.027** | 0.010 |

Nominal 5% and 1%. The procedure is slightly **conservative** at three different
geometries, so the 22.3% is genuine signal detected by a test with far more power, not
inflation. I suspected inflation and the generator refuted it; the decoy count alone
could not have told the two apart, in either direction.

### The weighted null on decoys

796 decoy pairs met the published support minima, 179 with power at α = 0.05. The weighted
test at each pair's own `w_hat` rejects **6.1%** of those; the published w = 1 test rejects
**8.4%** of the same set; at α = 0.01 both give 1.7%. Nominal 5% and 1%, and the decoy set
certainly contains real associations, so these are upper bounds. **Prediction P4 confirmed.**

### The face confound does inflate the published test — but about twofold, not tenfold. P5 refuted

P5 predicted the published w = 1 test would reject at **> 10%** under a confound planted at
the observed magnitude. It does not, and the size it does reach is worth stating precisely,
because the holdout and the full corpus give different-looking answers for a reason.

On the **bucket-0 holdout** (1,050 lines) the inflation is undetectable: at a planted
`w_hat` = 1.83 the w = 1 test rejects **0.3%**, the same as with no confound planted, and
only reaches 4.0% at a planted 2×`w_hat`. That is §1's bound showing through — face can act
in only 5 holdout tablets for this pair, so there is almost no channel.

On the **full corpus** (4,869 lines, 1,124 blocks, 1,500 replicates,
`results/calibration_corpus.json`) there is enough channel to measure it:

| planted confound | w = 1 (published test) | weighted at `w_hat` |
|---|---:|---:|
| none (w = 1) | 0.027 | 0.011 |
| **`w_hat` = 1.83 (measured)** | **0.059** | **0.026** |
| 2×`w_hat` | 0.157 | 0.092 |
| 4×`w_hat` | 0.327 | 0.187 |

Nominal is 0.05. So at the confound's **measured** strength the published test's
false-positive rate is **0.059** — a little over twice its own no-confound baseline of 0.027,
and only just at nominal. The weighted test, correctly specified, returns 0.026.

**The face confound is therefore real and measurable, roughly doubles the published test's
false-positive rate, and is nowhere near large enough to have produced p = 0.0071.** The
2026-09-17 session was right that face was the live uncontrolled confound and right to test
it; the prediction that it would be a *tenfold* threat was wrong.

Two riders. The inflation grows steeply — 6× the nominal rate by 4×`w_hat` — so this is a
confound worth controlling in any future pass, not one to dismiss. And the weighted test is
only calibrated at the confound's true strength: specified at `w_hat` while the truth is
2×`w_hat`, it rejects at 0.092. **Under-specifying `w` inflates it too**, which is the real
argument for reporting the critical weight rather than a single p at a single `w`.

---

## 5. The face confound has a sign, and for four pairs it is protective — P6 refuted

P6 predicted M243–N39B would be the second most fragile pair. It is not fragile at all:
its p **falls** from 0.0025 to 0.0009 as w rises to 1024. The same holds for M297–N01,
M263–N01 and M106–N24 (non-monotone, rising to 0.0086 at w = 16 then falling to 0.0008).

The mechanism is straightforward once stated. Weighting the target towards the reverse
lowers the null's expected overlap whenever the M-sign is *obverse*-concentrated relative
to the target, which makes the observed overlap more extreme, not less. **A face confound
helps an association only when both members lean the same way**; where they lean opposite,
assuming a stronger confound strengthens the result.

So "N45 is the most reverse-skewed N-sign, M288 is also reverse-skewed, therefore the
association may be a face artefact" was the correct worry for this pair and would have been
the wrong worry for half the constraint set. The sign of the lean is checkable in one line
and should be checked before a confound is treated as a threat.

One further number worth recording: the 2026-09-17 write-up quotes N45 at 30.8% reverse
against a 13.5% baseline, a 2.3× skew. Measured off the lines that are not M288 — which is
the quantity a null needs — the odds ratio is **1.83**. Part of N45's apparent reverse skew
is carried by the M288 lines themselves, so estimating confound strength from the whole
corpus overstates it.

---

## 6. Prediction scorecard

| | prediction | outcome |
|---|---|---|
| **P1** | M288–N45 has the lowest critical weight of the eight | **confirmed** (8.81; all others > 1024) |
| **P2** | its critical weight falls in (1.83, 10) | **confirmed** (8.81) |
| **P3** | the three load-bearing pairs clear p < 0.05 at 4×`w_hat` | **confirmed** (1e-4, 3e-4, 9.7e-3) |
| **P4** | weighted test rejects ≤ 8% of decoys | **confirmed** (6.1%) |
| **P5** | w = 1 inflated > 10% under a confound at observed magnitude | **refuted** (0.059 on the corpus, 0.003 on the holdout; real but ~2× its own baseline, not 10%) |
| **P6** | M243–N39B second most fragile | **refuted** (its p falls with w; §5) |
| I1 | M288–N45 clears 0.05 at `w_hat` *(informed)* | confirmed (p = 0.0132) |
| I2 | block-aware split feasible but a dead end *(informed)* | **refuted** — feasible and it fires, calibration verified |

Three of six prospective predictions failed, and two of the three failures (P5, P6) are
this session's more useful findings.

---

## 7. A screen worth confirming, not a result

Because the block-aware split is a general power amplifier with verified calibration, it can
be run across the whole candidate grid. On 193 powered decoy pairs, **24 survive BH at
q ≤ 0.05** against 5.4 expected false positives at the measured 2.8% type-I rate
(`results/block_aware_decoys_bh.json`). The strongest are M288–N39B (p = 5.1e-27),
M288–N24 (4.2e-17), M376–N08A (4.5e-11), M002–N30C (9.8e-7) and M370–N39B (3.9e-6).

**This is a screen, not a confirmation, and it is exploratory — no part of it was frozen.**
Each pair's direction came from its own complement and each test from its own validation
split, so the shape is right, but the grid was searched after the method was known to work,
and the candidate space was not budgeted in advance. Treated properly it means the published
constraint set of eight is **power-limited, not complete** — which is the folder's largest
open lead and §8's first item.

---

## 8. What this session did not establish

- **No lexical, phonetic or metrological value is assigned to any sign.** Everything here
  is structural association and the calibration of tests for it.
- **Nothing here is a blind holdout for M288–N45.** I enumerated the pair's per-block
  observed overlaps while diagnosing the power failure, before designing either test, so its
  outcome was foreseeable; `PREDICTIONS.md` says so and marks the affected predictions
  *informed*. The session's prospective evidence is the calibration work and §5.
- The 24 screen hits in §7 are unfrozen and uncorrected for the search that produced them.
- Novelty against specialist sign-by-sign literature remains unestablished, as in both prior
  sessions. Nothing here changes that.
- The weighted null models the face confound as a single multiplicative weight shared by all
  tablets. A confound that varies by tablet type or scribe is not captured, and was not
  tested. It is also calibrated only at the confound's true strength: under-specifying `w`
  inflates it (0.092 at a planted 2×`w_hat`), which is why the critical weight rather than a
  single p is the reportable quantity.
- Replication on an independent CDLI export is still unrun. The SFU mirror's remote `HEAD`
  is unchanged at the pinned commit, so that test needs CDLI directly.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
echo /abs/path/to/pe-sign-value-data/corpus > corpus_path.txt
python3 -m unittest -v test_weighted_null   # 10 tests, all must pass
python3 preflight.py                        # marginals and p-floors only
python3 sensitivity.py --scope holdout      # the p(w) curves and critical weights
python3 channel_bound.py                    # the marginal bound of §1
python3 block_aware_split.py                # the handover's item 1
python3 block_aware_decoys.py               # 193 powered decoys
python3 block_aware_calibration.py          # type-I error under a known-answer generator
python3 decoys.py                           # weighted-test decoy calibration
python3 calibrate.py --replicates 400 --scope holdout
```

No third-party packages. `corpus_path.txt` is the only machine-specific input and is
deliberately not committed.
