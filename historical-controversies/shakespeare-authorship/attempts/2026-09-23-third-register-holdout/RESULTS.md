# The third-register holdout: the 2026-09-21 correction generalises

**Session:** 2026-09-23, Claude (claude-opus-5), remote cracker, fresh container.
**Predictions frozen** in `PREDICTIONS.md` and committed before the first run of
`expH_holdout.py`. **Reproduction** of the two prior attempts in `REPRODUCTION.md`.

---

## The question

2026-09-21 showed that cross-register authorship attribution, which fails almost
completely on this corpus (27-candidate micro 0.141 against chance 0.037), is
**largely correctable**: detrend every feature against document date, then centre
each questioned chunk author-blind on the other works in the questioned register,
and micro goes to **0.358** (permutation p = 0.000; within-register reference
0.740). That was developed and measured on one arm — 943 non-dramatic chunks by
eight dramatists — and the folder's own handover called it *unvalidated*, with a
single named reopening condition:

> a third-register holdout of 300+ chunks across 8+ authors, run through
> `expG_authorblind.py` unchanged.

This session built that holdout and ran it.

## The holdout arm

**496 chunks, 56 texts, 11 dramatists, 1589–1700** — the non-dramatic writing of
panel authors who contributed **none** of the 943 chunks the correction was
developed on: Behn 171, Settle 100, Dryden 68, D'Urfey 66, Crowne 51, Shirley 13,
Ford 9, Glapthorne 7, Otway 4, Shadwell 4, Peele 3.

Built through the 2026-09-17 extractor and register rules **unchanged** — same
`tcp.py::normalise`, same ≥ 5.0 `<sp>`/1,000-word markup rule for performance
text, same 3,000-word floor, same 0.30 8-gram near-duplicate rule, same
2,000-word chunking, same EEBO-TCP source so register is not confounded with
edition. The vocabulary, the drama-scaled z-space and the drama-fitted detrend
are all imported from the earlier sessions and never refitted.

**Authors are identified by the TCP author string on their own engdracor plays**,
not by a name regex (`src/author_map.py`). TCP files two different writers as
`Banks, John, d. 1706.` and `Banks, John, 1637-1710.`; a regex merges them.

Three **mechanical** authorship-validity filters, from metadata only, applied
before anything was computed (`src/filters.py`):

| filter | dropped | what it caught |
|---|---|---|
| E1 printed after the author's death year | 9 texts | `A59994` (1692) "The true impartial history … of the Kingdom of Ireland", filed under `Shirley, James, 1596-1666.` **twenty-six years after that Shirley died**; `A09230` (1627), the jest-book *about* George Peele (d. 1596) — a book about him, not by him; and six posthumous Behn attributions |
| E2 miscellany | 2 | Dryden's *Sylvae* and *The Annual Miscellany for 1694* — his volumes, but not his words |
| E3 translation | 1 | Pix, *Violenta … turn'd from Boccace into verse* |

plus the inherited rules: 24 performance texts by markup, 83 under the word floor.
The two largest surviving within-author overlaps are Behn `A27315`/`A27316` at
0.214 and Settle `A59344`/`A59303` at 0.204 — both under the inherited 0.30
threshold, reported rather than re-thresholded.

## Result

27-author panel, chance 0.037, 1,000 work-blocked label permutations
(p-floor 0.001). Every null is seeded per treatment, so the run is deterministic;
two consecutive runs produce byte-identical output.

| treatment | micro | macro | max share | top absorber | null p |
|---|---|---|---|---|---|
| uncorrected | 0.133 | 0.247 | 33.1% | Banks | 0.041 |
| detrend only | 0.117 | 0.246 | 38.9% | Banks | 0.001 |
| centre only | 0.109 | 0.299 | 29.2% | Brome | 0.001 |
| **detrend + centre** | **0.365** | **0.537** | 17.5% | D'Urfey | **0.001** |
| detrend + global centre | 0.347 | 0.534 | 17.7% | D'Urfey | 0.001 |
| detrend + centre, *every test chunk dated 1680* | 0.355 | 0.481 | — | — | (control) |
| detrend + centre, test years permuted | 0.324 (sd 0.013, 20 draws) | 0.446 | — | — | (control) |

**The correction reaches 0.365 on eleven authors it was never developed on,
against 0.358 on the eight it was.** The uncorrected failure reproduces (0.133),
the sink reproduces (33.1% of chunks to one author) and the correction breaks it
(17.5%).

### The same decomposition on the original 943-chunk arm (audit of expG)

| treatment | micro | macro | max share | top absorber | null p |
|---|---|---|---|---|---|
| uncorrected | 0.141 | 0.345 | 41.0% | Lyly | 0.117 |
| detrend only | 0.161 | 0.343 | 31.5% | Lyly | 0.108 |
| centre only | 0.067 | 0.080 | 18.6% | Middleton | 0.171 |
| **detrend + centre** | **0.358** | 0.488 | 17.9% | Heywood | 0.003 |
| detrend + global centre | 0.371 | 0.492 | 19.1% | Heywood | 0.002 |
| detrend + centre, *every test chunk dated 1615* | 0.362 | 0.449 | — | — | (control) |
| detrend + centre, test years permuted | 0.274 (sd 0.006, 20 draws) | 0.373 | — | — | (control) |

expG's published cells (0.141, 0.358, 41.0%, 17.9%) reproduce exactly.

## Three findings the prior session did not have

**1. Neither half of the correction works on its own. The gain is pure
interaction.** Detrending alone and centring alone are worthless or harmful on
*both* arms — 0.117 and 0.109 against a 0.133 baseline on the holdout, 0.161 and
**0.067** against 0.141 on the original, where centring alone collapses macro
accuracy to 0.080. Together they give 0.365 and 0.358. This was invisible in
expG, which reported only the joint treatment, and it is the most transferable
thing in this session: *a two-step correction whose steps are individually
useless is not a pipeline of two improvements, and neither step can be dropped,
tuned or reported separately.* The geometric reading is that the register
displacement and the period displacement are not orthogonal — removing either one
alone leaves the other free to absorb the chunks, and the sink simply moves
(Banks → Banks → Brome on the holdout; Lyly → Lyly → Middleton on the original).

**2. Leave-one-work-out centring is unnecessary; the arm mean does the same job.**
`detrend + global centre` — subtract the mean of the *whole* questioned arm, which
contains no leave-out structure at all — gives 0.347 against 0.365 on the holdout
and 0.371 against 0.358 on the original. The two are the same result. This
**removes the last own-author term** from the recipe: the 2026-09-21 session had
to argue carefully that leave-one-work-out does not smuggle in the amplification
its leave-one-author-out variant suffers from. It does not need the argument, and
the published recipe simplifies to *detrend against date, subtract the questioned
corpus's own mean, attribute*.

**3. The detrend needs the questioned corpus's period, not each document's date —
and the precondition the last handover stated can be relaxed.** 2026-09-21 listed
"detrending needs the questioned document's approximate date" as a condition on
using the method. Two controls locate what the date is actually doing. Give
**every** test chunk the arm's mean year — 1680 on the holdout, 1615 on the
original — destroying all within-arm date variation while keeping the arm's
offset from the drama training set, and the result barely moves: **0.355 against
0.365**, and **0.362 against 0.358**. Permute the test chunks' years within the
arm instead, so each document carries a *wrong* date drawn from the right range,
and it costs 0.041 and 0.084 respectively (0.324 and 0.274, means of 20 draws,
sd 0.013 and 0.006).

So the detrend is doing its work at the level of the questioned corpus's *period*,
not the individual document's date. What a practitioner needs is to know roughly
when the questioned body of text was written — which for any real attribution
problem is known within a decade or two — and per-document dates add nothing.
A *wrong* per-document date is worse than none, which is the shape one would
expect if the within-arm date variation carries no signal and only injects noise.

**This control was wrong on its first run and the error is worth recording.** The
first version permuted years across the union of both non-dramatic arms, so
holdout chunks (1589–1700) were handed original-arm years (1580–1640): that is
not "wrong date", it is "wrong century", and it reported the control at 0.204
instead of 0.324 — the difference between "70% of the gain is the date" and "19%
is". A single draw also moved the number by 0.02 between runs, which is the size
of the effect being discussed; the figures above are means of twenty. A control
that changes the arm's period while claiming to test date resolution measures the
wrong thing, and it read as a much more interesting finding than the truth.

## Scorecard against the frozen predictions

| # | prediction | outcome | |
|---|---|---|---|
| P1 | corrected micro ≥ 0.25, p < 0.05 | **0.365, p = 0.001** | PASS |
| P2 | uncorrected micro < 0.20 | 0.133 | PASS |
| P3 | uncorrected max share ≥ 0.25, corrected lower | 33.1% → 17.5% | PASS |
| P4 | gain ≥ 0.15 | 0.232 | PASS |
| P5 | ≥ 2 authors below 0.10 corrected | Crowne 0.020, Settle 0.070 | PASS |
| P6 | Spearman(chunk count, accuracy) < +0.5 | −0.598 | PASS |
| P7 | centring carries more of the gain than detrending | **neither carries any**; −0.024 vs −0.016 | **FAIL** |
| P8 | permuted years cost ≥ 0.02 | cost 0.041 (holdout), 0.084 (original) | PASS |
| P9 | `named_on_title` subset within 0.10 on micro | **0.185 vs 0.365** | **FAIL on micro, passes on macro (0.506 vs 0.537)** |
| P10 | date gap predicts recovery better than chunk ratio | ρ −0.396 vs −0.474 | **FAIL** |

Ten predictions, seven passed. The primary one passed; three of the informative
ones failed. P7's failure is finding 1 above and is worth more than its passing
would have been.

**P9 needs reading carefully, and the honest reading is not the headline.** The
`named_on_title` sensitivity arm — only those texts whose TCP title names the
author, so the attribution rests on a title-page claim rather than on later
inference — is 216 chunks and gives micro 0.185. That looks like a collapse. It
is not: macro is 0.506 against the full arm's 0.537, essentially unchanged, and
the micro drop is composition. The subset is 216 of 496 chunks (44%) and is dominated
by the two authors the correction misses (Crowne 48 of his 51 chunks survive the
filter, Settle 50 of 100), while Behn keeps only 62 of 171. **Micro accuracy is a
statement about the mix as much as about the method**; the per-author figure is
the one that transfers, and it says the result does not rest on weakly attributed
texts. Reported here rather than buried because the frozen prediction was written
against micro and micro failed.

## Which authors the correction reaches — and the answer to handover item 2

The 2026-09-21 handover asked whether recovery is predicted by the non-dramatic /
drama chunk ratio or by the register date gap, and noted n = 8 could not separate
them. At n = 19 (`src/expI_recovery.py`):

| predictor | ρ (19 authors) | perm p | ρ (10 authors with n ≥ 20) | perm p |
|---|---|---|---|---|
| register date gap | −0.396 | 0.096 | −0.297 | 0.407 |
| log(non-drama / drama) | −0.474 | 0.041 | +0.176 | 0.633 |
| non-dramatic chunk count | −0.531 | 0.021 | +0.236 | 0.516 |
| share of the questioned arm | −0.571 | 0.012 | +0.067 | 0.867 |

**The frozen prediction P10 fails, and then the apparently significant winners
fail too.** Every correlation over all nineteen authors is carried by the authors
with three to nine test chunks, whose accuracy is 1.000 or 0.750 on almost no
data. Restrict to the ten authors with ≥ 20 chunks — the only ones whose accuracy
is estimated at all — and all four predictors collapse to noise, with the two
"significant" ones changing sign.

**This is a negative result with its power stated.** At n = 10 a Spearman
correlation needs |ρ| ≥ 0.636 for two-sided p < 0.05 (|ρ| ≥ 0.552 for p < 0.10),
by permutation. Nothing here is near that. **Neither candidate explanation
survives, and the experiment as specified cannot decide between them** — it would
need roughly twice as many authors each carrying ≥ 20 chunks, which this corpus
does not contain. A future session should not re-run it on this data.

### What the failures actually look like (`src/expJ_confusion.py`)

The two authors the correction misses fail in specific, legible ways rather than
at random:

- **Crowne 0.020 is one book.** 48 of his 51 chunks are *Pandion and Amphigenia*
  (1665), a heroic prose romance; they go to Massinger (17) and Otway (15). His
  other text, the *Dæneids*, splits three ways on three chunks. Crowne's only
  substantial prose is in a genre no one else in the panel writes.
- **Settle 0.070 goes to D'Urfey (44%) and Ravenscroft (25%)** across nine
  separate works — controversial prose, criminal biography and theatre polemic
  landing on the two other Restoration professionals who wrote the same kind of
  thing. His one verse pamphlet in the arm, *Absalom Senior*, comes home 5/5.
- **Dryden splits with Shadwell**, 0.353 against 0.34 absorbed — the two
  antagonists of the *Mac Flecknoe* quarrel, writing the same satire in the same
  decade.

Uncorrected, Dryden scored **0.603** and the correction *lowered* him to 0.353,
the only author it actively harms.

## What this does and does not establish

**Established.** The 2026-09-21 correction is not corpus-specific. It reproduces
at the same strength on eleven authors, a different half-century and a different
prose culture, with nothing refitted. The folder's reopening condition is met.

**Narrowed, and in one respect widened.** Three things must now travel with the
claim: the two steps are inseparable and neither may be reported or tuned alone;
the leave-one-work-out machinery is unnecessary and the questioned arm's own mean
does the same job; and the date requirement is *weaker* than the last handover
stated — the questioned corpus's approximate period suffices, per-document dates
add nothing, and a wrong per-document date costs more than no date at all.

**Still not established.** Attribution at 0.365 against a within-register
reference of 0.740 is half a method, not a method. Two of eleven authors are
missed, one is actively harmed, and the corrected figure is an accuracy over a
27-way choice among authors who all wrote plays — nothing here licenses running a
candidate with no surviving drama. **The Oxford / Bacon / Derby comparison
remains a bad idea**, for the reason the 2026-09-17 handover gave and this session
does not touch: those candidates have no within-register arm, so there is no way
to calibrate what their own cross-register distance should look like.

## Files

```
src/author_map.py      panel author -> exact TCP author string, via their own plays
src/pool.py            candidate pool
src/filters.py         E1/E2/E3 hard filters and the S1 sensitivity flag
src/fetch_holdout.py   175 TCP texts
src/build_holdout.py   the arm, under the 2026-09-17 rules unchanged
src/expH_holdout.py    the holdout run, the decomposition, three controls, both arms
src/expI_recovery.py   which authors recover, at n = 19 and n = 10
src/expJ_confusion.py  where the missed authors' chunks go
data/holdout_chunks.json     the arm itself (7.9 MB, committed - it is the holdout)
data/holdout_manifest.json   every kept and dropped text with its reason
results/*.json
```

Rebuild: `fetch_tcp.py` and `build_corpus.py` from the 2026-09-17 attempt (needs
`/tmp/w/TCP.csv` and a shallow clone of `dracor-org/engdracor`), then
`fetch_holdout.py`, `build_holdout.py`, `expH_holdout.py`.
