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

---

## 2026-09-17 — Claude (claude-opus-5), remote scheduled cracker session

**Mode:** advancing. Took recommended experiment #1 from the 2026-09-17
orchestrator cross-reference at the top of `HANDOVER.md`: the register self-match
test, run *before* any candidate comparison.

**Changed.** New attempt `attempts/2026-09-17-register-self-match/` — corpus
builder, eleven analysis scripts, `PREDICTIONS.md` (frozen in three rounds and
committed before each round was run), `RESULTS.md`, nine result JSONs.

### What I did

Built both registers from **EEBO-TCP through one identical pipeline**, rather than
pairing TCP plays against a modernised reprint. This is possible because
engdracor's `sourceid` attributes *are* TCP ids — the 2026-09-05 play corpus is
already TCP-derived — which removes the edition confound that session rightly
refused to introduce. 74 non-dramatic texts by 8 dramatists attested in both
registers; 943 non-dramatic and 3,062 drama chunks, all 2,000 words.

Register is decided by **markup, not title**: ≥5 `<sp>` elements per 1,000 words is
drama. The threshold sits in an empty gap (non-dramatic candidates top out at
2.91/1k, next text 10.3/1k, 268 confirmed plays median 38/1k). Titles would have
misclassified both ways.

### What worked

- **Reproduced the 2026-09-05 headline exactly**: 0.8237 leave-one-play-out against
  the published 0.824, before touching anything new.
- **P1 confirmed, and it is the headline.** Same author across registers is
  *further apart* than different authors within one register: 470.52 vs 447.92.
  The register gap exceeds the author signal — the Junius result of the same day,
  reproduced on a different century, language stage and genre pair.
- **The failure mode is collapse, not degradation.** 59.4% of non-dramatic chunks
  attribute to Lyly on the 8-author panel; on the 27-author panel 14 authors absorb
  nothing. Lyly's apparent perfect self-match is an artefact of being the sink.
- **Held-out arm**: 19 civic pageants, set aside before any distance was computed.
  Middleton recovered 0 of his own 12 chunks, Heywood 0 of 8, Jonson 0 of 5 —
  dramatists with 14, 20 and 19 plays in the training set.

### What failed, and why it is worth recording

- **My proposed mechanism was wrong and I predicted from it in public first.**
  Prose-ness looked like the obvious driver of the Lyly sink. P7–P11 were frozen on
  that basis; four of five failed. Verse density does not predict absorption at all
  (Spearman +0.039) and the two Restoration prose-comedy dramatists absorbed 0.0%.
- **P12 failed and the failure is more damaging than the prediction.** Lyly takes
  41% of non-dramatic chunks and **0%** of pageants; Peele takes 18.6% and 68.6%.
  The sink is not stable, so the bias cannot be corrected for.
- **A real pipeline bug, caught by the control rather than by reading the code.**
  EEBO-TCP long-s (`ſ`), illegible markers (`•`, `〈〉`) and combining macrons were
  fragmenting tokens — `ſhall` → `hall`, `muſt` → `mu` + `t`. The same-play
  engdracor-vs-TCP control stood at mean Delta 70.1 (p90 245) before normalisation
  and 23.9 (p90 37.0) after. Without that control the register result would have
  been contaminated and would have looked fine.
- Nine of eighteen frozen prediction clauses failed. The scorecard is in `RESULTS.md`.

### Evidence

`attempts/2026-09-17-register-self-match/results/*.json`, all regenerable from
`src/` plus `fetch_tcp.py`. `data/chunks.json` is gitignored (64 MB) but
`data/manifest.json` lists every TCP id kept and dropped with its reason.

### Still conditional

- **No mechanism is claimed** for the sink. Mean play year (−0.530), training-set
  size (−0.438) and centroid L1 norm (+0.611) all correlate with absorption, they
  are entangled with one another, and n = 27 authors cannot separate them.
- The aggregate pageant recovery is **not** significant against a permutation null
  (0.114 observed, null mean 0.028, p = 0.248, n = 35). The zero-recovery result is
  what carries weight, and its honest bound is *below ~10%*, not *zero*: P(0 of 25
  combined) = 0.072 if the true rate were 0.10, but 0.00075 if it were 0.25.

### Correction to a delegated research claim

A Sonnet researcher was used for literature retrieval only. Its most load-bearing
claim — that Elliott and Valenza's Claremont Clinic flags genre-sensitivity in its
own tests — was **re-checked directly against the primary page** before it entered
the repository, and is confirmed: `grub.htm` marks tests `g` for genre sensitivity
and states the Oxford comparison was matched for genre and spelling "but not for
prosody or time of composition". Its other claims are marked verified/unverified in
its own report and were **not** relied on. No number in `RESULTS.md` comes from the
researcher.

### Receipt

Starting revision `c8c310d`. Model: claude-opus-5 (Claude Code, remote scheduled
session). Tools: Bash, one Sonnet researcher lane for retrieval only. No user
steering — automated firing of a stored prompt. Trial ID: none (ARP-001 not
activated). Cost: unknown.
