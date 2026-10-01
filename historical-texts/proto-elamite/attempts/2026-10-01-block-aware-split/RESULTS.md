# The block-aware split, the correction base, and 130 new tablets

**Session:** 2026-10-01, Claude Opus 5 Breaker (advancing). Drawn: stream B, pick
`historical-texts/proto-elamite`, next move "settle M288–N45 with a block-aware split".
**Corpus (pinned):** SFU `pe-sign-value-data` at
[`538949cc`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6),
LF digest `8849716c…8bf2b2dcf`.
**Corpus (live):** CDLI bulk ATF export, fetched 2026-10-01T18:43:20Z, 1,597
Proto-Elamite inscriptions.
**Predictions frozen before results:** [`PREDICTIONS.md`](PREDICTIONS.md) (commit
`53271e7`) and [`REPLICATION_PREDICTIONS.md`](REPLICATION_PREDICTIONS.md) (commit
`4669385`), both one or more commits before any file in `results/`.
**Code:** `marginal_survey.py`, `block_split.py`, `coinflip_and_base.py`, `nulls.py`,
`complexity.py`, `cdli_fetch.py`, `cdli_compat.py`, `cdli_replicate.py`,
`exact_form_audit.py`; tests in `test_block_split.py`.

---

## Result in one sentence

M288–N45 is a real line-level association that survives face blocking in a properly
powered design, survives adjustment for line numeral complexity, and rests on eight
two-line faces that are exact fair coins under the null **all eight of which came up
heads (p = 0.0039)** — but it does **not** clear the folder's own confirmation rule,
because under the published design's own multiple-testing base face blocking confirms
only **two** of the eight published pairs, not seven; and the three load-bearing
constraints pass their published falsification test in direction on 130 genuinely new
CDLI tablets, which are far too few (0 of 8 pairs have any power) to confirm anything.

---

## 0. Reproduction

The 2026-09-04 pipeline was re-run unchanged on a fresh clone at the pinned commit.
**All fifteen published rows reproduce with zero mismatches** — every contingency cell,
odds ratio, p-value and q-value agrees to within 1e-9 relative. Corpus audit figures
match exactly (1,467 files, 10 without numbered lines, 1,457 tablets, 11,013 lines,
4,869 eligible, 3,819 train / 1,050 validation). The LF digest is as the 2026-09-17
session recorded; the CRLF trap in the handover is confirmed and was not re-triggered.

The exact-form generalisation in §5 is gated on reproducing the 2026-09-17 M297
homogeneity p-values (0.0757 / 0.6941 / 0.1377) before its new output is read. It does,
to four decimals.

`test_block_split.py` carries 20 tests, all passing. The load-bearing one requires the
re-parameterised exact test to return the eight published validation p-values when handed
the *tablet* block key, so that every face-blocked number here is the same statistic with
one argument changed. **It earned its keep immediately:** the first version of that test
carried the published constants typed in by hand, and it failed — I had written
4.44 × 10⁻¹⁶ for M297–N39B where the CSV says 4.39 × 10⁻⁶. The constants are now read
programmatically out of `analysis/results/associations.csv`. A reproduction gate that
can only be satisfied by hand-entered numbers is not a gate.

---

## 1. The split, and why selecting on marginals is legitimate

The bucket-0 holdout left M288–N45 with 4 informative `(tablet, face)` blocks and a
p-value floor of 0.12 — it could not have returned a significant answer. The fix is to
stratify the tablet-level split on **block marginals only**: block size, how many lines
carry the M-sign, how many carry the target. A block is *informative* when
`hi = min(s, t)` strictly exceeds `lo = max(0, s − (total − t))`, and both are functions
of those marginals.

This matters because the exact conditional test **conditions on exactly those
marginals**. Selecting blocks on them is selection on an ancillary statistic and cannot
disturb the null distribution. The within-block overlap — the quantity under test — is
never read by the split. `nulls.py` checks the claim by brute force rather than asserting
it: under 60 replicates of a null that permutes the target within each face (preserving
all marginals), **the split came out identical 60/60 times**.

The split: tablets contributing ≥1 informative block form stratum I, are ordered by
`sha256(tablet)`, and are added to validation until validation holds ≥10 informative
blocks; the rest go to train. All other tablets use the published rule (hash bucket 0 →
validation).

| | pinned design (bucket 0) | this design |
|---|---:|---:|
| validation tablets | 297 | 235 |
| validation lines | 1,050 | 1,084 |
| M288–N45 informative blocks in validation | **4** | **10** |
| M288–N45 face-blocked p-floor | **0.12** | **0.0022** |

**Prediction P2 confirmed.** The design bought two orders of magnitude of power.

**Prediction P1 confirmed.** Train alone, with ten of the fifteen informative tablets
removed, still re-screens the pair under the published rule: OR 11.02, BH
q = 5.2 × 10⁻¹⁶, cells (35, 390, 27, 3333). So the validation test is a genuine test of a
screened candidate, not of a pair smuggled in by hand.

### The answer, and the surprise

| | value |
|---|---:|
| validation face-blocked p | **0.0216** |
| p-floor | 0.0022 |
| informative blocks | 10 |
| observed / forced / max overlap | 21 / 12 / 22 |
| BH q over the 54 re-screened candidates | **0.1516** |
| confirmed under the published rule? | **no** |

**Prediction P3 refuted.** The raw p-value clears 0.05 comfortably. The *corrected*
q-value does not, because the published screening rule selects **54** candidates and the
published confirmation rule BH-corrects across all of them. Which brings us to the thing
this session did not set out to find.

---

## 2. The correction base is part of the test

The 2026-09-17 session reported that seven of the eight published pairs survive the
face-blocked null, with q-values from 0.0023 to 0.0321, and wrote: *"Every face-blocked
number below comes from that same function with a different block key, so the comparison
is like-for-like by construction."*

**That is true of the p-values and not of the q-values.** The face-blocked q-column was
BH-adjusted across the 8 already-published pairs. The 2026-09-04 column beside it was
BH-adjusted across the 54 candidates its own screen selected. Re-running the face-blocked
test on the identical bucket-0 holdout and correcting over the published base gives:

| pair | p (face-blocked) | floor | q over 8 (as published 2026-09-17) | q over 54 (published design's base) | confirmed at base 54 |
|---|---:|---:|---:|---:|:--|
| M263–N01 | 0.00029 | 0.0000 | 0.00229 | **0.01547** | **yes** |
| M297–N39B | 0.00145 | 0.0000 | 0.00581 | **0.03919** | **yes** |
| M243–N39B | 0.00306 | 0.0000 | 0.00817 | 0.05515 | no (boundary) |
| M297–N01 | 0.00839 | 0.0000 | 0.01678 | 0.11327 | no |
| M106–N24 | 0.01168 | 0.0004 | 0.01870 | 0.12619 | no |
| M263–N30C | 0.01900 | 0.0190 | 0.02534 | 0.15160 | no |
| M297–N24 | 0.02807 | 0.0002 | 0.03208 | 0.15160 | no |
| M288–N45 | 0.47000 | 0.1200 | 0.47000 | 1.00000 | no (no power) |

Under the published design's own correction base, **face blocking leaves two confirmed
constraints, not seven**: M263–N01 and M297–N39B. M243–N39B sits on the boundary at
0.0552.

The 2026-09-17 rotation table is a third base again: `rotate_holdout.py` compares raw
per-bucket p-values to 0.05 with **no correction at all**, so the "passes among powered"
column — the evidence for the three-tier reading — is uncorrected throughout.

**This is not a claim that BH-over-8 is wrong.** Correcting over a pre-registered set of
8 is a defensible confirmatory choice, and arguably the right one for a re-test of
already-published pairs. What is not defensible is printing it in a column beside a
BH-over-54 number and describing the comparison as like-for-like. The tiering claim the
folder now runs on depends on which base you pick, and no previous write-up says so.
The fair summary of the face-blocked evidence is:

- **Load-bearing on any base:** M297–N39B, M263–N01.
- **Load-bearing on a confirmatory base, not on the design's own base:** M263–N30C,
  M297–N01, M297–N24, M106–N24, M243–N39B.
- **M288–N45:** see §3.

---

## 3. Forced, free, and fair coins — what the evidence actually is

A blocked exact test's p-value hides how much of the observed overlap was **mandatory**
given the block marginals. Decomposing it (`coinflip_and_base.py`) changes how the whole
constraint set reads. Full corpus, face blocks:

| pair | observed | forced | free | free used | informative blocks | fair-coin faces | heads | binomial p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| M297–N39B | 135 | 73 | 84 | 62 | 64 | 10 | 6 | 0.3770 |
| M297–N24 | 44 | 20 | 46 | 24 | 34 | 4 | 3 | 0.3125 |
| M297–N01 | 117 | 91 | 80 | 26 | 61 | 8 | 3 | 0.8555 |
| M263–N30C | 0 | 0 | 41 | 0 | 27 | 2 | 0 | 1.0000 |
| M263–N01 | 176 | 96 | 84 | 80 | 55 | 7 | 6 | 0.0625 |
| M243–N39B | 22 | 8 | 17 | 14 | 12 | 5 | 4 | 0.1875 |
| M106–N24 | 14 | 0 | 19 | 14 | 12 | 1 | 1 | 0.5000 |
| **M288–N45** | 56 | **38** | 21 | 18 | 16 | **8** | **8** | **0.0039** |

A *fair-coin face* is a block whose marginals are exactly `total = 2, s = 1, t = 1`: a
face with two eligible lines, one carrying the M-sign and one carrying the target, where
the null is a 50/50 coin with no asymptotics and no modelling.

**For M288–N45 all eight came up heads.** Exact binomial p = 0.0039; Bonferroni over the
eight pairs reported here, 0.031. This was prediction **P6**, frozen before computing —
with one error I have to own: I wrote "**eleven** such blocks corpus-wide" and predicted
≥ 9 of 11. The true count is **eight**; I miscounted the `total = 2` rows in the marginal
survey printout. The threshold I set (p-value of the stated tail, 0.0327) is nonetheless
cleared by a wider margin than I predicted, and the denominator was fixed by the data,
not chosen after seeing the heads. **P7 confirmed**: freedom used 18 of 21, against a
predicted ≥ 15.

Two cautions, because this cuts both ways:

1. **The coin statistic is only the right lens where coin faces are a large share of a
   pair's evidence.** For M288–N45 they are 8 of 16 informative blocks. For M297–N39B
   they are 10 of 64, so its 6/10 is a thin and noisy slice and emphatically **does not**
   demote the folder's headline constraint, which uses 62 of its 84 free units.
2. **38 of M288–N45's 56 co-occurrences are forced** by face marginals. Any future
   statement about this pair should quote the free-unit count, not the odds ratio of
   16.29 / 13.50, which is inflated by overlap the test never had the option to refuse.

---

## 4. Null models and the complexity question

| null | prediction | result |
|---|---|---|
| **N1** split invariance under within-face target permutation | — | split identical **60/60** |
| **N2** validation p under the null (P4) | fraction ≤ 0.05 should be ≈ 0.05 | **0.024** over 500 replicates; conservative from discreteness. Observed p = 0.0216 sits at the **2.4th percentile** of the null |
| **N3** alternative splits meeting the ≥10-block constraint (P5) | median p ≤ 0.05 | 2,000 splits: median **0.0021**, 96.3% ≤ 0.05; the hash-chosen split sits at the **88th percentile** — *less* significant than most, so it was not a lucky draw |
| **N4** block on `(tablet, face, numerals on the line)` | — | full corpus **p = 0.0575**, floor 0.00056, 8 informative blocks, 6 of 8 free units used |

**P4 and P5 confirmed.** The design does not manufacture significance; it is if anything
conservative, and the particular split chosen is one of the worse ones available.

N4 is the interesting one. Face blocking does not control **line complexity**: a line
carrying more accounting numerals picks up any given numeral more readily. Under the
triple block M288–N45 lands at p = 0.058 while M297–N39B and M263–N01 stay below 10⁻⁵
(40 and 47 informative blocks). That looks like a refutation. It is not, and
`complexity.py` shows why — the question is whether numeral count is a **confound** or a
**mediator**:

- M288 lines do carry more numerals: mean 1.838 vs 1.292.
- But stratifying by numeral count, the N45 rate on M288 lines exceeds the rate on other
  lines **in every single stratum**: 0.018 vs 0.002 (k = 1), 0.099 vs 0.014 (k = 2),
  0.195 vs 0.058 (k = 3), 0.440 vs 0.128 (k = 4), 0.375 vs 0.125 (k = 5).
- **Mantel–Haenszel OR holding line numeral count fixed: 5.87.**
- Of the eight fair-coin faces, the M288 line was the longer of the two in only 4. On the
  **4 equal-length faces, where complexity cannot explain anything, N45 landed on the
  M288 line 4/4** (binomial p = 0.0625).

So the association survives complexity adjustment at OR ≈ 5.9, down from an unadjusted
13–16: complexity accounts for a substantial part of the raw effect size and **none** of
the association. The triple block fails not because the signal dies but because
conditioning on `(tablet, face, numeral count)` forces 50 of 58 co-occurrences and leaves
8 informative blocks — it conditions on a consequence of the association. **Report the
Mantel–Haenszel figure, not the triple-blocked p-value.**

---

## 5. Exact-form audit of M263 and M288 (folder item 3)

The 2026-09-17 handover said "same script, change the `family` argument in `test_b`";
`family` is a hardcoded local there, so `exact_form_audit.py` generalises it and is gated
on reproducing M297's published numbers, which it does exactly.

**M263 — merge upheld, more strongly than M297's.** Four graphical forms reach the
15-line bar (M263 93, M263~A 34, M263~B1 27, M263~1 23).

| target | base rate | M263 | M263~A | M263~B1 | M263~1 | homogeneity p |
|---|---:|---:|---:|---:|---:|---:|
| N30C | 0.063 | **0.000** | **0.000** | **0.000** | **0.000** | 1.0000 |
| N01 | 0.729 | 0.903 | 1.000 | 0.926 | 0.870 | 0.1114 |

The N30C absence is **total in every one of the four variants separately** — a
considerably stronger statement than the family-level absence the folder published, and
it is now the best-supported constraint in the set on this axis. N01 enrichment holds in
all four.

**M288 — the merge question does not arise.** Of 559 form-bearing eligible lines, 538 are
plain M288; no variant reaches 15 lines. There is effectively nothing merged, so the
M288–N45 constraint cannot be a merge artefact. That answers item 3 for both families and
it should not be re-run.

---

## 6. Replication on 130 genuinely new tablets (folder item 4)

The folder has wanted this since 2026-09-04 and called it "the strongest falsification
test". It is now runnable. **The stale mirror is a trap worth recording:**
`github.com/cdli-gh/data` advertises itself as a daily dump but its README says "Last
update was August 2022" and its newest commit (2023-10-11) only edits that README. The
live site is current:

```
https://cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions&limit=3000
```
→ HTTP 200, `text/x-c-atf`, 508,015 bytes, **1,597** `&P` blocks. (`robots.txt` asks for
a 60-second crawl delay; this is one request.)

**The pin is a strict subset.** All 1,467 pinned P-numbers are present; **130 are new**;
none has been withdrawn. 115 of the 130 are *PETF 1*, the rest Louvre and Shahdad items.

**Parser compatibility was established, not assumed** (`cdli_compat.py`). On the 1,467
overlapping tablets the 2026-09-04 parser reads 4,869 eligible lines from the SFU
serialisation and 4,868 from the live CDLI one; 11 tablets differ on eligible-line count
and per-sign counts differ by 1–2 (M288 557/558, M263 191/190, N39B 621/620, N01
3585/3587). Those are CDLI's own curation edits since 2022. **One systematic renaming:
pinned `N08` is live `N08A`** — it touches no pair under test here, but it will silently
break any future N08 result that mixes serialisations.

### The new tablets, alone

| pair | published direction | a | b | c | d | OR | direction | informative blocks | p-floor |
|---|---|---:|---:|---:|---:|---:|:--|---:|---:|
| M297–N39B | enriched | 2 | 2 | 17 | 88 | 5.06 | **holds** | 0 | 1.00 |
| M263–N01 | enriched | 3 | 2 | 50 | 54 | 1.51 | **holds** | 1 | 0.167 |
| M263–N30C | depleted | 0 | 5 | 12 | 92 | 0.67 | **holds** | 0 | 1.00 |
| M243–N39B | enriched | 0 | 0 | 19 | 90 | 4.64 | holds | 0 | 1.00 |
| M106–N24 | enriched | 0 | 1 | 3 | 105 | 10.05 | holds | 0 | 1.00 |
| M297–N24 | enriched | 0 | 4 | 3 | 102 | 3.25 | holds | 0 | 1.00 |
| M288–N45 | enriched | 1 | 8 | 1 | 99 | 11.71 | holds | 1 | 0.333 |
| M297–N01 | depleted | 2 | 2 | 51 | 54 | 1.06 | **fails** | 0 | 1.00 |

**R1 confirmed.** All three load-bearing pairs hold in the direction they were published
under. This is the falsification test the constraints were staked on, and they passed it.

**R2 confirmed, more sharply than predicted.** I predicted at most two of eight would
have power at 0.05 on the new tablets. **Zero do.** 130 tablets give 576 numbered lines
and only 109 eligible ones. The new material can test *direction* and nothing else, and
any future session must not read a p-value off it.

**R3 confirmed.** M288–N45 gets 1 informative block from the new tablets, floor 0.333 —
untestable, as predicted. The one new co-occurrence went in the predicted direction.

**R4 confirmed vacuously.** No new fair-coin face appeared, so the pooled count stays 8/8
(p = 0.0039).

**The one direction failure is uninformative, not a reversal.** M297–N01 comes in at
OR 1.06 — dead neutral — on 4 M297 lines. Calling that "fails" is my rule being strict
about a cell with no information in it. It does not weaken the pair; it says the new
tablets have nothing to say about it. Honest framing: **of the eight pairs, seven hold in
direction, one is neutral, none reverses.**

**Pooled corpus (1,597 tablets), face-blocked, for the record:** all eight pairs pass with
a p-floor of 0, M288–N45 at p = 4 × 10⁻⁵ (OR 13.50, 57/38/60, 17 informative blocks).
**This includes selection data and is a power demonstration, not confirmation** — the same
caveat the 2026-09-17 session attached to its full-corpus figure.

---

## 7. Verdict on M288–N45

Neither of the two outcomes the handover anticipated. Precisely:

- It is **not** a face artefact. The properly powered face-blocked test returns
  p = 0.0216 at a floor of 0.0022, the null is conservative, and the chosen split is
  one of the less favourable ones available.
- It is **not** explained by line complexity: Mantel–Haenszel OR 5.87 with numeral count
  held fixed, and 4/4 on the equal-length fair-coin faces.
- It is **not** a graphical-merge artefact: 538 of 559 M288 form-lines are the plain form.
- Its effect size is **inflated** by forced overlap: 38 of 56 co-occurrences are mandatory
  given face marginals. The honest effect size is the complexity-adjusted OR ≈ 5.9, not 16.
- Its cleanest evidence is **eight fair coins, eight heads, p = 0.0039** — which is
  stronger and far more legible than the aggregate it was previously judged on.
- And it still **does not clear the folder's own confirmation rule**, because that rule
  BH-corrects over 54 screened candidates and face blocking clears only two of them.

So: **a real association, under-powered for the bar this folder sets, and the bar is the
binding constraint rather than the evidence.** The 130 new tablets do not move it and no
plausible near-term corpus growth will: the pair would need roughly four times the
current informative-block count to clear q = 0.05 at base 54. That is a power analysis,
and it is a negative result about the method, not about the pair.

---

## 8. What this session did not establish

- **No semantic, phonetic or metrological value for any sign.** Nothing here says what
  M288, M263, M297, N45, N39B or N01 mean. §3's fair coins say that M288 and N45 belong on
  the same *line* more often than the face's marginals require; they do not say why.
- Novelty against specialist sign-by-sign literature remains unestablished, exactly as the
  two previous write-ups said. This session did no literature search and claims no priority.
- The pooled 1,597-tablet figures in §6 include selection data.
- The 130 new tablets' proveniences were read only from their `&P… = publication` headers;
  no catalogue metadata was joined.
- N4's triple block was run only for M288–N45, M297–N39B and M263–N01, not all eight.
- The `N08`→`N08A` renaming was noted, not investigated.

## Reproducing

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data
git -C pe-sign-value-data checkout 538949cca949a176400b144ef49c2036e9dc82a6
echo /abs/path/to/pe-sign-value-data/corpus > corpus_path.txt
python3 -m unittest -v test_block_split      # must pass before any result is read
python3 marginal_survey.py
python3 block_split.py --pair M288-N45
python3 coinflip_and_base.py
python3 nulls.py                             # ~3 min, seeded (20261001)
python3 complexity.py
python3 exact_form_audit.py

# live replication
curl -sS 'https://cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions&limit=3000' -o pe_all.atf
python3 cdli_fetch.py pe_all.atf /abs/path/to/cdli-corpus
python3 cdli_compat.py /abs/path/to/pe-sign-value-data/corpus /abs/path/to/cdli-corpus
python3 cdli_replicate.py /abs/path/to/pe-sign-value-data/corpus /abs/path/to/cdli-corpus
```

No third-party packages. `corpus_path.txt` is the only machine-specific input and is not
committed. The live export is not committed either — it is 508 KB of CDLI's data, and the
route plus the fetch timestamp plus `cdli_compat.py` are what make the run repeatable.
