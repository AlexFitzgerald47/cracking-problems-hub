# Can the Irish annals answer the Dál Riata question onomastically? No — and the reason is structural

**2026-09-24 · cracker session · `ireland/dal-riata-migration-direction`**
**Result: negative, with a measured mechanism and a ceiling.**

Predictions frozen in `FREEZE.md` and `FREEZE-2.md` before the runs that tested them.
Both prediction sets ended in a **control failure**, and the two failures have the same
root cause. That cause is the finding.

---

## 1. Reproduction first

The sister folder `early-irish-annals-reliability` committed a 13,414-row derived table
of four CELT annal witnesses with a sha1 prefix per entry. Re-fetching CELT and re-running
their `src/parse.py` reproduces it **byte-identically: 13,414 / 13,414 sha1 match, 0
mismatches** (`src/verify_corpus.py`). Their pipeline is sound and their corpus is exactly
what they say it is.

**One audit finding, bounded.** `id` is **not unique** in `entries_derived.csv`: 65 ids
appear more than once, so 67 of 13,414 rows are lost by a naive join on `id` (AI 92 rows
affected, AU 18, AT 12, CS 10). The cause is duplicate `div2 n="..."` attributes in the
CELT source — e.g. `U707.6` occurs twice with different text. **This does not touch their
headline result**: zero `SCOT`-tagged rows carry a duplicated id, so the 6.51 % → 1.85 %
Scottish-content changepoint is unaffected. Successors should key on
`(witness, year, idx)` or on row order, not on `id`.

## 2. What was tested

Whether the personal-name inventory attached to Argyll-secular contexts in the Irish
annals is compositionally an Irish inventory. This bears on the folder's success
criterion 2 — separating (a) folk migration, (b) the dynastic descent claim, (c) Gaelic
language spread. **An onomastic test speaks to (b) and (c) only. It cannot speak to (a),**
and this limit was written into `FREEZE.md` before any result existed.

The design's one virtue is that it carries a **known answer at each end, scored in the
same cell**:

| group | what it is | required behaviour |
|---|---|---|
| `IONA` | Columban familia — Irish-recruited, resident in Argyll | positive control: **must look Irish** |
| `DALR` | Dál Riata / Argyll secular | the test set |
| `PICT` | Picts / Fortriu — different people, P-Celtic | negative control: **must look non-Irish** |

Window 550–900. Available material: **DALR 146 name-tokens in 22 entries** (STRICT;
202 / 43 WIDE), IONA 192, PICT 221, against an Irish reference of 9,517 tokens.

## 3. Prediction set 1 — positive control failed, and found three real bugs

Token-level coverage (fraction of a group's names attested in the Irish pool) against a
resampling null: `cov(IONA) = 0.693` versus a null lower bound of 0.772. **P1 failed.**
Diagnosis found three defects, each of which depresses a small out-of-sample group:

- **D1 epithets.** An early Irish name is *given name + optional epithet*. Matching whole
  surface strings meant `Failbe` in an Iona entry never matched `Failbe Flann` (×9) and
  `Failbe Fland` (×2) in the reference, so one of the commonest names in the corpus was
  scored 12 times as "unattested in Ireland". 15.2 % of all name tokens are two-word.
- **D2 reference pool.** Requiring a positive Irish toponym discarded **1,800 name-bearing
  entries carrying 4,815 tokens — 51 % of the Irish name stock** — almost all bare obits.
- **D3 editorial spelling.** `Sléibéne / Slébíne / Sleibine / Sleibéne` is one man and was
  four skeletons; four editors a century apart do not spell alike.

Corrected in `src/names2.py`. **None of the three is visible without a control whose
answer is known in advance.** `src/names.py` and the failed run are left in place.

## 4. Prediction set 1 on the corrected pipeline — positive control passes, negative fails

Every group — six Irish provinces plus the three north-channel groups — scored by one
identical out-of-sample procedure, with group size (146 tokens) **and reference size
(7,500 tokens) held equal**, 400 draws.

| group | ent | tok | cov [95 %] | |
|---|---:|---:|---|---|
| ULSTER | 224 | 936 | 0.835 [0.781, 0.884] | |
| MIDLAND | 467 | 1854 | 0.891 [0.843, 0.938] | |
| NORTHWEST | 101 | 526 | 0.914 [0.870, 0.952] | |
| LEINSTER | 311 | 1173 | 0.890 [0.843, 0.938] | |
| MUNSTER | 295 | 910 | 0.881 [0.836, 0.925] | |
| CONNACHT | 262 | 1008 | 0.906 [0.856, 0.945] | |
| **IONA** | 76 | 192 | **0.889** | **positive control — inside the band. P1 passes.** |
| **DALR** | 22 | 146 | 0.856 | test set |
| **PICT** | 62 | 221 | **0.842** | **negative control — also inside the band. P2 fails.** |

Irish provincial band **0.835 – 0.914**. The Picts — a different people speaking a
different language — sit inside it. **The statistic cannot tell a Pict from an Irishman,
so it cannot tell an Argyll Gael from one either.** `pos(DALR)` from this statistic is
uninterpretable, and its two tag sets duly disagree in sign (+0.303 STRICT, −0.260 WIDE).

## 5. Prediction set 2 — a sharper statistic, chosen blind, and it fails the same way

Jensen–Shannon divergence between a group's name-frequency distribution and the Irish
reference *does* separate the controls (IONA 0.653 [0.635, 0.674] vs PICT 0.713
[0.682, 0.748], non-overlapping). The statistic was chosen from `results/controls.json`,
a run that **excludes DALR by construction**, and `FREEZE-2.md` was committed before DALR
was ever scored on it.

But JSD put IONA — the *positive* control — above the whole six-province band, so it was
measuring group concentration, not Irishness. The matched fix is eight **tight** Irish
comparanda (single houses and single dynasties, ≥146 tokens, monastic and secular) whose
TTRs bracket both north-channel groups:

| group | tok | JSD [95 %] | cov | TTR |
|---|---:|---|---:|---:|
| BREGA | 196 | 0.529 [0.507, 0.554] | 0.918 | 0.421 |
| MIDE | 255 | 0.536 [0.507, 0.565] | 0.931 | 0.465 |
| ULAID | 340 | 0.584 [0.551, 0.620] | 0.842 | 0.490 |
| ARMAGH | 329 | 0.586 [0.551, 0.623] | 0.851 | 0.615 |
| CIANNACHTA | 240 | 0.593 [0.570, 0.623] | 0.940 | 0.478 |
| UI_MAINE | 181 | 0.607 [0.589, 0.628] | 0.917 | 0.516 |
| KILDARE | 155 | 0.636 [0.626, 0.647] | 0.803 | 0.535 |
| CLONMACNOIS | 223 | 0.639 [0.614, 0.671] | 0.742 | 0.686 |
| **IONA** | 192 | **0.654 [0.634, 0.678]** | 0.889 | 0.513 |
| DALR | 146 | 0.627 [0.623, 0.632] | 0.855 | 0.527 |
| PICT | 221 | 0.715 [0.682, 0.749] | 0.839 | 0.562 |

Tight Irish band **0.529 – 0.639**. `jsd(IONA) = 0.654` is **above** it.
**Q1 fails.** By the terms of `FREEZE-2.md`, `jsd(DALR)` must not be interpreted — and it
is therefore *not* reported here as a result, only as a cell. The failure is robust: it
holds under STRICT and WIDE and under the `--drop-nechtan` sensitivity (IONA 0.654–0.657
against band maxima 0.639–0.640 in all four configurations).

## 6. Why both control failures happen — the measured mechanism

There is no way to build a clean Irish reference pool out of the Irish annals, because
the two available constructions are biased in opposite directions and **both biases are
structural**:

**Permissive pool** (any entry with no north-channel place-name or ethnonym) is
**contaminated by the very population under test**. 34 tokens of names whose Pictish or
British identity is not in dispute sit inside it, across 25 entries:
`bruide` 9, `tolarg` 8, `maelcu` 5, `bile` 4, `alpin` 4, `drust` 2, `brude` 1, `eilpin` 1.
A distinctively Pictish name then scores as "attested in Ireland" because *another
Pictish person* carries it. Of 20 leaking entries inspected by hand, only **5 are
gazetteer-fixable** (spellings my regexes missed: `Foirtriu`, `Ail Cluaithe`, `Alba`).
The other **15 are unmarkable in principle** — they carry no geography at all:

> `AU641.2` Death of Bruide son of Foth.
> `AU706.2` Bruide son of Derile dies.
> `AU725.3` Simul son of Drust is imprisoned.

No gazetteer built on place-names and ethnonyms can ever catch these, and tagging them by
*personal name* is precisely the circularity an onomastic test must avoid.

**Marked pool** (entry must carry a positive Irish marker) avoids the contamination and
**discards 51 % of the Irish name stock** — the 1,800 bare obits — which is what made the
positive control fail in the first place.

**And the two cannot even be told apart.** `AU887.2` and `AU888.8` record a *Tolarg son of
Cellach*, one of two kings of **southern Brega** — in Ireland. So "Talorg in the Irish
pool" is not necessarily leakage; it may be genuine Irish currency of a name of Pictish
origin. **That indistinguishability is the ceiling.** It is not a sample-size problem and
no amount of further annalistic material fixes it.

## 7. The direction test (Q4) has no resolution either

For name skeletons shared between a group and the Irish pool, the rate at which the Irish
attestation comes first: DALR 0.879, IONA 0.877, PICT 0.819 — against a tight-Irish band
of **0.764 – 0.983** (mean 0.872). Every group sits inside a band that wide. The statistic
cannot distinguish an Argyll-first component from an Ireland-first one at this corpus
size, and no directional claim can be made from it in either direction.

## 8. What this session does and does not establish

**Establishes.** The Irish annals' personal-name channel cannot decide whether Argyll
Dál Riata naming is Irish-derived. The limit is structural — an irreducibly contaminated
reference — not a matter of *n*, and the demonstration is that the channel **fails on
controls whose answers are already known**. Any future session proposing to settle
Campbell's question from annalistic onomastics should read §6 first.

**Does not establish.** Nothing about proposition (a), folk migration — the design could
not speak to it and never claimed to. Nothing about whether the Argyll name stock *is*
Irish: `cov(DALR) = 0.856` and `jsd(DALR) = 0.627` both sit in the Irish range, but a
statistic that puts the **Picts** in the Irish range too has no licence to place anyone.
That number is reported so the next session can see it, not as evidence.

## Files

`src/` — `regions.py`, `names.py` (frozen, pre-correction); `regions2.py`, `names2.py`
(corrected); `verify_corpus.py`, `run_scope.py`, `run_power.py`, `run_onomastic.py`
(failed frozen run, retained), `run_corrected.py`, `run_controls.py`, `run_final.py`,
`run_leakage.py`.
`data/names_derived.csv` — 10,038 rows: witness, year, entry id, group tags, name
skeleton, surface length, entry sha1. **No entry text** (CELT marks these texts
`restricted` and the translations are in copyright); `src/fetch.py` + `src/parse.py` in
the sister folder regenerate the source in a minute.
`results/` — `scope.json`, `power.json`, `onomastic.json`, `corrected.json`,
`controls.json`, `final.json`, `final_nonechtan.json`, `leakage.json`, `verify.json`.
