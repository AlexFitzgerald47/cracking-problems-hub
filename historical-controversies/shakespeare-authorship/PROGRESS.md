# Progress Log – Shakespeare Authorship

---

## 2026-09-05 – Claude (Opus 5), remote session

### What was attempted

Not an adjudication of the authorship question. A calibration of the instrument the
question is usually settled with.

Stylometric verdicts are quoted in this debate without a stated error rate. Before any
verdict carries weight, someone has to measure what Burrows's Delta can resolve on early
modern English drama: how much material per candidate it needs, how much questioned text
it needs, and whether it is measuring authorship or something else.

Reproducible from `attempts/2026-09-05-stylometry-calibration/`.

### Results / findings

**1. On this corpus the method works.** 312 single-author plays, 27 dramatists,
1583–1700, 6.4M words, from `dracor-org/engdracor` (TEI from EarlyPrint/TCP).
Leave-one-play-out accuracy **0.824**, against uniform chance 0.037, majority class
0.099, and a label-permutation null of 0.038 (max 0.064 over 25 permutations).

**2. It needs three to five plays per candidate, and about 5,000 words of the questioned
text.**

| training plays per author | accuracy | | questioned-text words | accuracy |
|---|---|---|---|---|
| 1 | 0.523 ± 0.031 | | 500 | 0.228 |
| 2 | 0.663 ± 0.053 | | 1,000 | 0.465 |
| 3 | 0.747 ± 0.024 | | 2,000 | 0.676 |
| 5 | 0.794 ± 0.022 | | 5,000 | 0.769 |
| 8 | 0.837 ± 0.019 | | 20,000 | 0.827 |

**3. Roughly half the apparent authorial signal is chronological.** Withholding an
author's own plays from within ±10 years of the questioned play drops accuracy from
0.83 to **0.475**.

| gap | accuracy with gap | same plays, no gap | drop |
|---|---|---|---|
| ±0 (n=312) | 0.817 | 0.824 | −0.006 |
| ±5 (n=295) | 0.654 | 0.834 | −0.180 |
| ±10 (n=255) | 0.475 | 0.831 | −0.357 |
| ±20 (n=115) | 0.496 | 0.809 | −0.313 |
| ±30 (n=45) | 0.644 | 0.800 | −0.156 |

The third column is the control that makes this readable, and it was run because the
first version of this result was not trustworthy: widening the gap shrinks the testable
set, so the drop could have been a change in which plays were being tested rather than a
period effect. It is not. The *same* plays score 0.80–0.83 with the gap removed. The
±30 row rests on 45 plays and is noisy; it should not be read as recovery.

**4. What this means for the authorship question.** It cuts against confident
stylometric claims in both directions.

A candidate can only be tested near 0.82 if they left several plays, in the same genre,
written within about a decade of the questioned work. Oxford died in 1604 leaving no
drama under his name; Bacon wrote essays. Against such candidates the method operates in
the regime where it scores near 0.48, or cannot be run at all. "Stylometry rules them
out" is therefore a much weaker statement than the headline accuracy implies.

That is not an argument for those candidates. A weak test is not evidence *for* anything,
and nothing here disturbs the documentary case, which this attempt did not examine. The
conclusion is narrower and duller: **stylometry is not the instrument that settles this
question**, and work on either side that quotes an attribution accuracy without a period
control is quoting the wrong number.

### Failures & dead ends

- The corpus contains **no Shakespeare**. His quartos are in the metadata but have no TEI
  file. This was left alone rather than patched from another repository: splicing in a
  modernised Shakespeare text would confound authorship with edition and spelling
  convention — the exact class of artefact this attempt exists to measure. The
  calibration measures the method, not the man, so it does not need him.
- Genre could not be controlled. The corpus has usable creation dates for 311 of 312
  plays but essentially no genre metadata (one file carries a `genreTitle`). Since genre
  is the other obvious confound, and the period result shows how large such confounds
  are here, this is the most important missing control.
- The first period result was reported before the matched-subset control existed and was
  not trustworthy. Recorded because the control changed nothing about the number but
  everything about whether it could be believed.

### Artefacts produced

`attempts/2026-09-05-stylometry-calibration/` — corpus builder, Delta implementation,
four experiments, the matched-subset control, raw JSON.

### References consulted

- `dracor-org/engdracor` (GitHub, public; retrieved 2026-09-05).
- **No stylometry literature was reachable from this session** (egress is limited to
  GitHub and PyPI). Whether findings 2 and 3 restate published work is unknown, and the
  period confound in particular is the kind of thing that may well be known. Do not cite
  as novel until someone checks.

---

## 2026-09-03 – Initial seed

Problem folder created.
