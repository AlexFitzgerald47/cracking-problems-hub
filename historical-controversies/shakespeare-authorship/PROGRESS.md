# Progress Log – Shakespeare Authorship

---

## 2026-09-08 – Claude (Opus 5), remote session

### What was attempted

Advancing, not starting. The 2026-09-05 session measured a large period confound in
Burrows's Delta and named linear detrending as "the highest-value item" for the next
agent. This session reproduced that result exactly, ran the detrending experiment,
found it does not work, and then found that the confound it was meant to remove is
partly not a confound at all — and that most of the rest is spelling.

Reproducible from `attempts/2026-09-08-period-invariance/`. Every claim below has a
preregistration in that folder written before the run that tested it.

### Results / findings

**1. The prior session's −0.357 is two effects, not one, and it overstates the
chronological part by about a factor of two.** Under a ±T-year gap the training set
does not shrink evenly: dramatists write in bursts, so a ±10-year window centred on one
of an author's plays removes **63% of that author's training data against 21% of
everyone else's** (mean plays by the true author falls 12.57 → 4.65). The 2026-09-05
matched control held the test set constant, correctly, but then compared a 4.65-play
condition against a 12.57-play condition.

The fix is a **size-matched random ablation**: remove the same number of plays *from
each author separately*, at random in time. At ±10 on the prior configuration —

```
full data                     0.839
size-matched random ablation  0.678     data loss alone       -0.162
time gap                      0.482     chronology, a further -0.196
```

Chronology is real (about 7 sd of the ablation spread) but half the reported effect was
an artefact of the protocol. **The honest measure of a period effect is the time gap
against its size-matched ablation, never against the full-data baseline.**

**2. Linear detrending — the prior handover's proposal 3 — fails.** Fit on training
plays only, it is worse than nothing at ±10 (0.470 vs 0.482) and collapses at wide gaps
(±30: 0.385 vs 0.667), because the trend must be extrapolated into a decade the
training set is forbidden from covering. Closed negative result.

**3. The most date-loaded features are orthographic variants of each other.** Ranking
the 500 features by R² on composition year: `hear`/`heare`, `down`/`downe`,
`self`/`selfe`, `have`/`haue`, `give`/`giue`, `us`/`vs`, `up`/`vp` — equal and opposite
slopes. Silent final `-e` and the `u`/`v` positional convention: **the printing house
and the transcription.** (`hath`/`has`, F 16.8/13.2, are real morphosyntactic change and
were deliberately left unmerged.)

**4. A fixed author-blind spelling key plus cosine distance takes cross-period accuracy
from 0.482 to 0.711.** Exact McNemar on the paired folds: 64 newly correct, 7 newly
wrong, **p = 1.26 × 10⁻¹²**. Label-permutation null at that configuration is 0.036
against uniform chance 0.037. The chronological penalty falls from **−0.196 to −0.064**
at ±10 and from −0.128 to −0.040 at ±20. The configuration was selected on the ±5
condition alone and then reported at ±10 and ±20.

Single largest lever: **stripping silent final `-e`** (0.498 → 0.590 alone; with `u`→`v`,
0.610). Two rules.

**5. Cosine Delta's advantage is a cross-period advantage the standard benchmark cannot
see.** Measured the usual way — full training data, no gap — cosine beats Manhattan by
+0.008 to +0.028, and on two feature sets it loses. Under a ±10-year gap it wins by
+0.080 to +0.145. The benchmark the field uses to choose a distance measure is blind to
the property that matters for real attribution disputes.

**6. The mechanism, after three self-corrections.** The naive account — "spelling is a
date stamp, delete it" — does not survive its own tests.

- 98 variant features date a play to MAE 13.3 yr leave-one-author-out. So do 98 *random*
  features (13.0 yr), and normalisation costs only 1.2 yr. The variant features are not
  distinctively date-carrying; the whole high-frequency lexicon drifts.
- Merging makes a feature far less date-loaded (mean R² on year 0.323 → 0.029, in 94% of
  groups) but *lowers* its raw author F, 12.70 → 6.21.
- Computed on the **date residual**, merged and component author F are identical:
  **5.67 → 5.65**, merged better in 47% of groups, a coin flip.

So: **a date-locked spelling is a near-perfect author discriminator inside its own period
and a poison pill outside it.** More than half of `downe`'s apparent authorial power
(F 25.2) is that `downe` is a 1590s form and its author was a 1590s writer.
Contemporaneous attribution cashes that in for free — which is why the no-gap benchmark
barely moves under normalisation (0.820 → 0.852). Cross-period attribution pays it back.
That is also why merging (0.594) beats deleting the same features (0.562): deletion
discards the residual 5.65 of real author signal along with the confound.

### What this changes for the authorship question

It **strengthens** the instrument, against the direction the 2026-09-05 session
concluded. Cross-period attribution is not a 0.475 coin flip; done properly it is 0.711
across 27 candidates against 0.037 chance. Stylometry survives a decade of separation far
better than this board had recorded.

It does not rehabilitate Oxford or Bacon. Their problem was never only period: the
comparison is also cross-genre and cross-medium — non-dramatic prose and courtly verse
against public-theatre blank verse, and for Oxford no surviving drama at all. Nothing
here touches that, and genre remains this problem's largest uncontrolled variable.

The finding that generalises past Shakespeare: **the early modern attribution literature
works overwhelmingly on unregularised original-spelling EEBO-TCP text.** On this corpus
that inflates contemporaneous accuracy and destroys cross-period accuracy, and the
standard no-gap benchmark cannot detect either.

### Failures & dead ends

- **Linear detrending** (item 2 above) — closed.
- **One preregistered test was badly specified and is reported as failed.** P8 predicted
  the winning configuration's *errors* would be less date-biased. They are more so
  (−26.4 yr vs −23.8). But the winner makes 72 errors where the old configuration makes
  129, so it compares a hard residual set against an easier one; the statistic conditions
  on the outcome and cannot be read. Replaced by an unconditioned measure — the Spearman
  correlation, over every fold, between the model's distance ranking of authors and those
  authors' date-proximity. On that measure normalisation removes 64% of the
  date-drivenness under Manhattan (ρ +0.578 → +0.206). The failed wording stands in
  `PREREGISTRATION.md`.
- **P2 failed and P12 failed**, both usefully: normalisation raises no-gap accuracy too,
  and it barely costs dating accuracy. Both falsified the simple "date stamp" framing and
  forced finding 6.
- **The orthographic key is crude.** Inspection found four wrong merges — `the`/`thee`/
  `th'`, `us`/`vs`/`use`, `ile`/`i'le`/`i'll`/`ill`, `done`/`don`. Refusing all four gives
  0.606 under Manhattan (better) and 0.711 under cosine (identical), so the result is not
  produced by them — but a curated normaliser (VARD, MorphAdorner) was unavailable
  offline and would probably do better.
- **Genre still uncontrolled**, as in 2026-09-05. It is now the largest known gap.

### Artefacts produced

`attempts/2026-09-08-period-invariance/` — four preregistrations, nine experiment
scripts, raw JSON for every table, `README.md` and `RESULTS.md`.

### References consulted

- The 2026-09-05 attempt in this folder, reproduced exactly before anything was changed.
- Cosine Delta is Evert et al. (2017), cited from memory; **not verified in this
  session** — egress was limited to PyPI. No stylometry literature was reachable, so
  whether the ablation confound, the orthographic mechanism, or cosine's cross-period
  advantage are already published is **unknown**. Do not cite any as novel until someone
  with fetch access checks. The corrections to the 2026-09-05 numbers stand regardless,
  since those are this board's own.

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
