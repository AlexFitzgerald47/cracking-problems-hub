# The register self-match test

**Date:** 2026-09-17 · **Status:** complete; negative result · **Reproducible:** yes

The 2026-09-05 session on this problem calibrated Burrows's Delta on 312 early
modern plays and found that about half the apparent authorial signal was
chronology. Its recommended next step, reinforced by the Junius session of
2026-09-17, was the **register self-match test**: take an author attested in both
plays and non-dramatic writing and score him against himself across that gap,
*before* interpreting any candidate ranking.

That test is run here. It fails, and it fails in a way that matters for this
controversy, because every candidate in the Shakespeare authorship debate —
Oxford, Bacon, Derby — left non-dramatic writing and no plays, so every
stylometric comparison made about them must cross exactly this gap.

## Headline

**Same author, different register, is further apart than different authors in the
same register.**

| cell (2,000-word chunks, same-work pairs excluded) | mean Delta |
|---|---|
| same author, same register (different plays) | 415.80 |
| **different author, same register** | **447.92** |
| **same author, cross register** | **470.52** |
| different author, cross register | 486.20 |

An author's own prose sits 22.6 Delta further from his plays than a *different*
dramatist's plays do. A ranking computed across that gap is measuring the gap.

The consequences show up directly in attribution on the 8-author panel
(chance 0.125):

| | micro | macro |
|---|---|---|
| within register (plays → plays, leave-one-work-out) | 0.666 | 0.717 |
| **cross register (plays → the same authors' own prose and verse)** | **0.169** | **0.337** |
| reverse (prose → plays) | 0.268 | 0.326 |

and the macro figure is generous: it is inflated by two authors whose cross-register
scores turn out to be artefacts (below).

## The failure is not degradation, it is collapse onto a sink

Cross-register errors do not scatter. On the 8-author panel, **59.4% of all 943
non-dramatic chunks were attributed to Lyly**, against 7.0% of drama chunks.
Greene's prose went to Lyly 198 times out of 242; Heywood's went to Lyly 214 times
out of 430. **Not one non-dramatic chunk in the corpus was attributed to
Middleton.**

Lyly's apparently perfect cross-register self-match (1.000) is a consequence of
being that sink, not evidence that his prose resembles his plays. Remove Lyly from
the panel and Greene jumps from 0.062 to 0.455 while Chapman goes 0.417 → 0.500 —
each author's score is set by who *else* is on the panel, which is what an
uninterpretable ranking looks like.

Widening the panel to all 27 dramatists (chance 0.037) makes it worse: Lyly takes
41.0%, Peele 18.6%, Glapthorne 11.1%, Chapman 11.0%, and **fourteen of the
twenty-seven dramatists absorb nothing at all.**

## A mechanism was proposed, predicted from, and refuted

The obvious explanation was prose-ness: Lyly's comedies are mannered prose, and he
is by a wide margin the least verse-heavy dramatist in the corpus (11.4 verse lines
per 1,000 words, against a corpus median near 92). Predictions P7–P11 in
`PREDICTIONS.md` were frozen on that basis before the 27-author panel was run.

**Four of the five failed.**

| | prediction | outcome |
|---|---|---|
| P7 | top absorber among the three lowest-verse authors | **held** — Lyly |
| P8 | those three absorb >50% | **failed** — 41.0% |
| P9 | Shadwell + D'Urfey absorb >10% | **failed — 0.0%** |
| P10 | Spearman(verse density, absorption) < −0.45 | **failed — +0.039** |
| P11 | 27-author macro < 0.20 | **failed — 0.345** |

Verse density does not predict absorption at all, and the two Restoration
prose-comedy dramatists absorbed literally nothing. The prose-ness mechanism is
dead. Exploratory correlates of absorption are mean play year (−0.530), number of
training chunks (−0.438) and centroid L1 norm (+0.611); these three are entangled
and n = 27 authors cannot separate them, so **no mechanism is claimed**.

## The held-out arm: authors cannot recover their own work

Nineteen civic pageants, royal entries and Lord Mayor's Shows were classified and
set aside by `build_corpus.py` before any distance was computed, and predictions
P12–P15 were frozen before they were scored. They are out-of-register text of
completely undisputed authorship by dramatists who are in the training set.

| | prediction | outcome |
|---|---|---|
| P12 | Lyly again the top absorber | **failed** — Peele took 68.6%, Lyly **0.0%** |
| P13 | profile correlation > +0.60 | **failed by a hair** — exactly +0.600 |
| P14 | ≥14 of 27 authors absorb zero | **held** — 21 of 27 |
| P15 | Middleton and Heywood recover <25% of their own pageants | **held** — 0.000 and 0.000 |

P12's failure is the more damaging finding, not a disappointment: **the identity of
the sink is not even stable.** Lyly absorbs 41% of non-dramatic prose and verse and
0% of pageants; Peele absorbs 18.6% and 68.6%. The bias is severe, and it is not a
fixed property of the centroids that one could correct for.

P15 is the result that speaks to the authorship question:

| author | plays in training | own pageant chunks | recovered |
|---|---|---|---|
| Middleton | 14 | 12 | **0** |
| Heywood | 20 | 8 | **0** |
| Jonson | 19 | 5 | **0** |
| Dekker | 10 | 10 | 4 |

## Where this test has no power — and where it does

The aggregate pageant recovery (micro 0.114, n = 35) is **not** significantly above
a permutation null (null mean 0.028, p = 0.248). At n = 35 the aggregate test is weak
and it is reported as weak.

The zero-recovery result is stronger, and the power analysis says exactly how far
it goes. Probability of observing 0 hits across Middleton's 12, Heywood's 8 and
Jonson's 5 chunks combined, if the true cross-register recovery rate were:

| true rate | P(0 of 25) |
|---|---|
| 0.717 (the within-register rate) | < 10⁻⁶ |
| 0.500 | < 10⁻⁶ |
| 0.250 | 0.00075 |
| 0.100 | 0.072 |

So the data decisively exclude these authors recovering their own out-of-register
work at anything like the within-register rate, and exclude a 25% rate. They
**cannot** distinguish 0% from about 10%. Any future session tempted to quote "zero"
should quote the bound instead.

## Controls

**Pipeline (P5, held).** Both registers come from EEBO-TCP, and engdracor's own
`sourceid` attributes are TCP ids, so the play corpus is the same transcription
tradition rather than a spliced modern edition. The residual extraction difference
was measured directly: the same play taken from engdracor and from its own TCP
source sits at mean Delta 23.9 (median 22.0, n = 265) — **5.3%** of the
different-author same-register distance, against a P5 threshold of 25%.

Getting there required fixing a real bug. EEBO-TCP writes long-s as `ſ` (U+017F),
marks illegible characters with `•` and spans with `〈〉`, and uses combining
macrons for nasal abbreviations. Untreated, `ſhall` tokenises as `hall` and `muſt`
as `mu` + `t`. Before normalisation the same-play control stood at mean Delta 70.1
with a p90 of 245; after, 23.9 with a p90 of 37.0.

**Transcription damage.** TCP `<gap>` damage is heavier in the non-dramatic half
for 5 of 8 authors (Chapman 204 vs 117 per 10,000 words; Greene 156 vs 115). It is
not the explanation: on the three authors whose registers are transcribed equally
cleanly (Jonson 16.5 vs 18.2, Middleton 31.6 vs 24.8, Heywood 78.9 vs 84.5) the P1
margin is **+23.44**, against +22.60 on all eight.

**Length.** All documents in both registers are 2,000-word chunks. Delta distances
grow as documents shorten, so comparing whole plays against shorter pamphlets
would have manufactured a register gap out of arithmetic.

**Register classification is structural.** Drama is defined as ≥5 `<sp>` speech
elements per 1,000 words, not by title. The threshold sits in a wide empty gap:
non-dramatic candidates top out at 2.91/1k, the next text up is 10.3/1k, and 268
confirmed plays have a median of 38/1k. Titles would have failed — "A strange
horse-race ... the catch-poles masque" is a prose pamphlet and "Pandosto the
triumph of time" is a prose romance.

**Positive control (P3, part-held).** Within-register attribution reaches macro
0.717 (micro 0.666) against the same panel, so the pipeline works. P3 predicted
≥0.70 and is met on macro, missed on micro; both are reported.

**Permutation null.** 200 author-label shuffles of the cross-register experiment
give mean macro 0.119, p95 0.222, max 0.315 — against an observed 0.337. The
observed value is barely outside the null envelope, which is itself the point.

## Scorecard against the frozen predictions

P1 **held** · P2 mixed (micro 0.169 held, macro 0.337 failed) · P3 mixed (macro held,
micro failed) · P4 **held** (6 of 8 authors do not self-match) · P5 **held** ·
P6 **failed** (held-out macro 0.358) · P7 held · P8–P11 **failed** · P12 **failed** ·
P13 failed by a hair · P14 **held** · P15 held for Middleton, Heywood, Jonson; failed
for Dekker.

Nine of eighteen clauses failed. The headline — P1 — held, and held on the
damage-matched subset too.

## What this means for the Shakespeare authorship question

It does not support any candidate, and it does not disturb the documentary case.
It says something narrower and more corrosive: **the stylometric arguments in this
debate are not weak evidence, they are uninterpretable**, because they all cross a
gap that is wider than the signal they are reading.

This is not a charge that the practitioners were unaware of the problem. Elliott
and Valenza's Claremont Shakespeare Clinic flags it themselves. In *Of Grubs and
Butterflies: Computers and the Oxford Claimancy Revisited*
(https://www1.cmc.edu/pages/faculty/welliott/grub.htm — read in full for this
session, 2026-09-17) they mark individual tests `g` for "results can be sensitive
to differences of genre (poem verse v. play verse)", and write that "one should
also try to match for other variables: genre (whether a work is play verse, prose,
or poem), time of composition, subject matter, editorial conventions (spelling and
punctuation), and prosody". They state that for Oxford they matched "for genre
(poem v. poem, or poem v. play verse) and spelling ... **but not for prosody or
time of composition**".

Two observations follow, and they cut in different directions.

1. The single most discrepant result in their Table 1 against Oxford — modal
   distance, where the Shakespeare range is −2 to +2 and Oxford's poems score 18.4 —
   is carried on a test they themselves mark `g`, genre-sensitive, comparing
   Oxford's poems against Shakespeare poem *and/or play verse* blocks.
2. The variable they say they did **not** match, time of composition, is the one the
   2026-09-05 session on this problem measured as carrying roughly half the
   apparent authorial signal in this corpus.

So the Clinic's caution was better than its critics usually allow, and the two
uncontrolled variables identified here — register and period — are precisely the
two that this folder has now quantified. Neither is small.

## Reproduction

```
pip install numpy
git clone --depth 1 https://github.com/dracor-org/engdracor /home/user/dracor-org/engdracor
cd src
python fetch_tcp.py           # ~2 min, ~100 MB of EEBO-TCP XML
python build_corpus.py        # both registers, one pipeline
python pipeline_control.py    # P5
python analysis.py            # P1-P4, the four cells, the null
python attractor.py           # the sink
python proseness.py           # verse density from markup
python wide_panel.py          # P7-P11, 27 authors
python heldout_pageants.py    # P12-P15
python nulls_and_damage.py    # power analysis, TCP gap rates
python damage_matched.py      # is the register gap a transcription gap?
```

`data/chunks.json` (64 MB of word lists) is gitignored and regenerable;
`data/manifest.json` records every TCP id kept and dropped with the reason, so the
corpus can be rebuilt and attacked without shipping the text.
