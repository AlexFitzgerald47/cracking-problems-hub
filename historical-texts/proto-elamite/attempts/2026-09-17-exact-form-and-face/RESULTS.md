# Face confound, exact-form audit, and the per-sign self-match test

**Session:** 2026-09-17, Claude Opus 5 cracker (advancing)
**Corpus:** SFU `pe-sign-value-data` at the pinned commit
[`538949cca949a176400b144ef49c2036e9dc82a6`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6)
**Predictions frozen before running:** [`PREDICTIONS.md`](PREDICTIONS.md), committed in
`2e2668d`, one commit before any result file.
**Code:** `face_and_form.py`, `power_floor.py`, `rotate_holdout.py`,
`matched_selfmatch.py`; 14 unit tests in `test_face_and_form.py`.

---

## Result in one sentence

Seven of the 2026-09-04 constraint set's eight numeral associations survive a null that
blocks on physical face as well as tablet, the eighth (M288–N45) is untestable on the
20% holdout rather than refuted, the M297 family merge survives an exact-form audit, and
the corpus-wide face gap is 0.41× the between-sign signal — but the sign carrying the
folder's strongest constraint is the single most face-sensitive sign in the corpus, so
the corpus-average self-match test would have given false reassurance.

---

## 0. Reproduction, and a correction to the recorded corpus digest

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pinned commit. All
fifteen result rows reproduce: every contingency cell, odds ratio and q-value is
identical to the published `results/associations.csv` (p-values differ only in the ~16th
decimal place, from platform floating-point summation order). Corpus audit figures match
exactly: 1,467 files, 10 without numbered lines, 1,457 tablets, 11,013 lines, 4,869
eligible, 3,819 train / 1,050 validation.

**One recorded value does not reproduce, and it is benign.** `results/associations.json`
records the corpus digest as `ee4fa7ba…c083d6a`; a Linux checkout gives
`8849716c…8bf2b2dcf`. The digest hashes raw file bytes, and the 2026-09-04 session ran
on Windows (its README uses PowerShell, and it reports a Windows checkout failure in a
sibling repository), so git had converted the corpus to CRLF. Converting the LF bytes to
CRLF and re-hashing returns `ee4fa7ba…c083d6a` **exactly**.

So the pin is sound, but the recorded digest is not line-ending-neutral and will look
like corpus drift to every future session on Linux. Both digests are now recorded:

| checkout | digest |
|---|---|
| LF (Linux/macOS) | `8849716c6afbf963e5ee02535da013c87c931c61e88e2c05ced9cd58bf2b2dcf` |
| CRLF (Windows, as recorded 2026-09-04) | `ee4fa7bacbc534ba211f95d7101c3f3498d9c4a5ea7ba4e233f58f9c1c083d6a` |

The new test suite's load-bearing test (`test_tablet_block_reproduces_published_p_values`)
requires the re-parameterised randomization to return the eight published validation
p-values to within 1e-12 when given the tablet block key. It passes. Every face-blocked
number below comes from that same function with a different block key, so the comparison
is like-for-like by construction.

---

## 1. Test A — the face-blocked null

### Why this test and not the one the handover proposed

The handover's recommended experiment 4 was a provenience/metadata control. Running it
would have been largely wasted effort, and the reason is worth recording: **the
2026-09-04 validation already controls for provenience.** Its exact test permutes the
target *within tablet*, so any confound that is constant across a tablet — site, period,
scribe, publication, tablet type — cannot produce a significant result. The corpus is in
any case 1,334/1,467 MDP (Susa), so a provenience stratification would have had almost
no power to offer.

What the within-tablet permutation does **not** control is position within the tablet. A
Proto-Elamite obverse carries itemised entries and the reverse carries totals, and the
two use numerals differently. Shuffling a target freely across a tablet's lines lets it
move between faces, which is exactly the freedom a face confound would exploit. So the
live confound is face, and the test is the same exact test with blocks keyed on
`(tablet, face)`.

### Result (bucket-0 holdout, 1,050 lines, 229 tablets → 290 tablet-faces)

| pair | direction | OR | q, tablet-blocked (2026-09-04) | q, face-blocked | p-floor, face-blocked |
|---|---|---:|---:|---:|---:|
| M297–N39B | enriched | 12.89 | 0.0002 | **0.0058** | 0.0000 |
| M297–N24 | enriched | 5.83 | 0.0055 | **0.0321** | 0.0002 |
| M297–N01 | depleted | 0.21 | 0.0055 | **0.0168** | 0.0000 |
| M263–N30C | depleted | 0.15 | 0.0166 | **0.0253** | 0.0190 |
| M263–N01 | enriched | 1.85 | 0.0189 | **0.0023** | 0.0000 |
| M243–N39B | enriched | 8.61 | 0.0222 | **0.0082** | 0.0000 |
| M106–N24 | enriched | 3.57 | 0.0390 | **0.0187** | 0.0004 |
| M288–N45 | enriched | 16.29 | 0.0480 | 0.4700 | **0.1200** |

Predictions A1 (M297–N39B survives) and A3 (at least six survive; seven did) are
confirmed. Prediction A2 said M288–N45 would not survive. It did not — **but my stated
reason was wrong, and the power floor is what caught it.**

### The power floor, and why M288–N45 is not refuted

A blocked exact test can only reach the p-value its block marginals permit. The
right-hand column above is the smallest p-value each test could return *if every block
showed the maximum overlap its marginals allow* — the p-value of a perfect result.

For M288–N45 under face blocking that floor is **0.12**. The test could not have
returned a significant answer whatever the data said. Only 4 of 290 tablet-faces were
informative (had any freedom to vary), and the observed overlap was 15 of a maximum
possible 16 — i.e. the data were nearly perfect and still could not clear 0.05.

**M288–N45's failure is an absence of power, not evidence of a face artefact.** Every
other pair has a floor below 0.02, so for those seven the survival is meaningful.

This is `board/PRACTICES.md`'s Kryptos lesson — "report where the test has no power, not
only where it fired" — arriving in a new form. Without the floor computation this session
would have published "the face block kills the weakest constraint", which is a clean,
attractive, *wrong* headline.

### Is there a face confound at all for M288–N45?

There is a real shared skew, which is why the prediction was tempting. Against a corpus
baseline of 86.5% obverse:

| | n | obverse | reverse |
|---|---:|---:|---:|
| all eligible lines | 4,869 | 86.5% | 13.5% |
| lines with N45 | 91 | 69.2% | **30.8%** |
| lines with M288 | 557 | 80.1% | 19.9% |
| lines with both | 56 | 62.5% | **37.5%** |

N45 is the most reverse-skewed N-sign in the top-15 vocabulary, at 2.3× the baseline
reverse rate. So M288 and N45 do share a face preference — but on the **full corpus**,
where the face-blocked test has 16 informative blocks and a floor of 0, the pair passes
at p = 1.0×10⁻⁴. The shared skew is not sufficient to explain the co-occurrence.

That full-corpus figure is a *power* demonstration, not independent confirmation: it
includes the tablets the candidate was selected on. The honest verdict is that at
holdout scale M288–N45 is **neither confirmed nor refuted against the face confound**,
and the corpus is large enough to settle it under a better split.

---

## 2. Holdout rotation — which constraints are actually stable

The candidate list is fixed, so the five hash buckets can each be used as a holdout in
turn. This is a stability and power check, **not** five independent confirmations:
buckets 1–4 were pooled as the 2026-09-04 training set, so they are in-sample for
selection. Direction agreement is reported separately because it is far less
power-dependent than a per-bucket p-value.

| pair | buckets with power | passes among powered | direction agrees (obverse OR) |
|---|---|---|---|
| M297–N39B | 5/5 | **5/5** | 5/5 |
| M263–N01 | 5/5 | **5/5** | 5/5 |
| M263–N30C | 4/5 | **4/4** | 5/5 |
| M297–N01 | 5/5 | 3/5 | 5/5 |
| M106–N24 | 3/5 | 2/3 | 5/5 |
| M288–N45 | 3/5 | 2/3 | 5/5 |
| M297–N24 | 5/5 | 2/5 | 5/5 |
| M243–N39B | 2/5 | 1/2 | 4/5 |

**The constraint set is not one tier.** Three pairs — M297–N39B, M263–N01, M263–N30C —
pass the face-blocked null in every bucket where the test has power. The rest are
power-limited, and M243–N39B is barely testable at this corpus size (powered in 2 of 5
buckets, direction flips in bucket 1, which has zero informative blocks). Future work
should treat the top three as the load-bearing results and the rest as leads.

---

## 3. Test B — exact-form audit of M297

### The handover's three-way split is not available in this corpus

Recommended experiment 1 asked for M297 lines separated into standalone M297,
read-value annotations, and compound membership. Of 370 M297 tokens corpus-wide:

- **363 (98.1%)** carry the SFU value annotation `ri2<M297<…`.
- **5 (1.4%)** are compound members (`M297+X` ×2, `M297+M296` ×2, `M297~B+M388` ×1).
- Annotation is therefore not a variable here, and compound membership cannot be tested.

The variation that *does* exist is graphical form. Eligible-line counts:
M297 175, M297~B 62, M297~D 10, M297~C 3, M297~BC 2.

### Are M297 and M297~B the same sign, functionally?

Proto-Elamite scholarship does not agree that `~` variants are allographs, and the
2026-09-04 design merges them. This tests the merge directly, on the whole eligible
corpus (the question is within-family homogeneity, not confirmation, and M297~B has only
62 eligible lines).

| target | base rate (non-M297 lines) | M297 (n=175) | M297~B (n=62) | homogeneity p |
|---|---:|---|---|---:|
| N39B | 0.105 | 0.491, OR 8.21 | 0.629, OR 14.27 | 0.0757 |
| N24 | 0.050 | 0.177, OR 4.13 | 0.145, OR 3.36 | 0.6941 |
| N01 | 0.751 | 0.417, OR 0.24 | 0.532, OR 0.38 | 0.1377 |

**Predictions B1 and B2 both confirmed.** No target separates the two forms at 0.05, and
both forms carry all three associations in the same direction with large effects. The
family merge is defensible, and the published M297 constraints are not an artefact of
collapsing two functionally different signs.

One caveat worth passing on: the N39B homogeneity p of 0.0757 is not far from
threshold, and the direction is consistent across all three targets — M297~B is *more*
enriched with N39B and *less* depleted with N01 than plain M297. At n=62 this is not a
finding, but it is the specific thing that more M297~B attestations would resolve.

---

## 4. Test C — cross-class self-match, and why the corpus average misleads

This is the 2026-09-17 handover instruction: take a class attested in two conditions,
score it against itself across the boundary, and put that number beside the association
statistics. The class boundary is face; the score is the distance between numeral-context
profiles (presence probabilities over the 15 commonest N-signs, mean absolute
difference).

### Sample-size-matched comparison, 25 signs

The naive comparison is confounded by sample size: a self-distance splits a sign's lines
across two faces, so each profile is noisier than the full-face profiles used for
between-sign distances. Every number below is therefore computed from two **disjoint**
samples of exactly *k* lines, *k* chosen per sign as the largest both groups supply,
averaged over 400 draws.

| quantity | value | above noise |
|---|---:|---:|
| NOISE — same sign, same face, disjoint halves | 0.0255 | — |
| FACE — same sign, obverse vs reverse | 0.0346 | **+0.0090** |
| SIGN — different signs, same face | 0.0477 | **+0.0222** |

**Ratio face-effect / sign-effect = 0.408, bootstrap 95% CI [0.191, 0.656],
P(ratio ≥ 1) = 0.0000** (5,000 resamples over signs and over sign pairs).

**Prediction C1 is refuted.** I predicted the class gap would be large, as it is on
Junius (register > author) and Shakespeare (register > author). In this corpus it is
real — a face-permutation null confirms the face effect is not noise, p = 0.005 for M297
— but it is decisively *smaller* than the signal. On the board's own framing this
"cheaply buys the right to generalise" across the obverse/reverse boundary, and that was
worth the test.

### But the corpus average is the wrong unit, and this is the session's most transferable finding

Ranking the 25 signs by their individual face effect:

| rank | sign | face effect above noise | vs mean sign effect (0.0222) |
|---:|---|---:|---:|
| 1 | **M297** | +0.0457 | **2.06×** |
| 2 | **M243** | +0.0270 | 1.22× |
| 3 | M362 | +0.0261 | 1.18× |
| 4 | **M288** | +0.0238 | 1.07× |
| … | (21 others) | ≤ +0.0218 | < 1 |

Exactly four of 25 signs have a face effect exceeding the mean between-sign signal —
and **three of them (M297, M243, M288) carry five of the eight confirmed constraints**,
including the strongest one. M297, the sign behind the folder's headline result, is the
single most face-sensitive sign in the corpus.

So the corpus-level self-match test passes comfortably (0.41, CI excluding 1) while the
units the claims are actually about sit in the tail of the very distribution that test
summarises. A corpus-average self-match would have returned "class gap is well under the
signal, proceed" — reassurance that does not apply to any of the signs being ranked.

This cuts both ways, and the second way is the good news: because Test A blocked on face
and seven pairs survived anyway, the M297 constraints are robust **despite** M297 being
the most face-skewed sign in the corpus. That is a stronger statement than the
2026-09-04 result made, and it is only available because the two tests were run together.

---

## 5. What this session did not establish

- **No semantic, phonetic or metrological value is assigned to any sign.** Everything
  here is structural association, as in 2026-09-04.
- The holdout rotation is not five independent replications; buckets 1–4 are in-sample
  for candidate selection. It measures stability and power, not novelty.
- The full-corpus face-blocked p-values in §1 include selection data and are reported
  only to establish that the corpus *can* answer the M288–N45 question.
- Novelty against specialist sign-by-sign literature remains unestablished, exactly as
  the 2026-09-04 write-up said. Nothing in this session changes that.
- The self-match test was run on face only. Provenience was not tested because the
  within-tablet permutation already controls it and the corpus is 91% one publication
  group; that is a reasoned skip, not a completed test.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
echo /abs/path/to/pe-sign-value-data/corpus > corpus_path.txt
python3 -m unittest -v test_face_and_form      # 14 tests, all must pass
python3 face_and_form.py "$(cat corpus_path.txt)" --json results/face_and_form.json
python3 power_floor.py
python3 rotate_holdout.py
python3 matched_selfmatch.py
```

No third-party packages. `corpus_path.txt` is the only machine-specific input and is
deliberately not committed.
