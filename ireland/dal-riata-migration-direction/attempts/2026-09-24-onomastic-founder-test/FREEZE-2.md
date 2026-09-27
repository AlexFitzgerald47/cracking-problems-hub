# FREEZE-2 — 2026-09-24, second frozen prediction set

`FREEZE.md` stands unaltered. Its P1 failed on the first run (pipeline defects D1–D3,
diagnosed in `src/names2.py`); on the corrected pipeline **P1 passes** and **P2 fails** —
token coverage puts the Picts inside the Irish provincial band, so the frozen statistic
has no demonstrated power on the Irish/non-Irish axis and `pos(DALR)` computed from it is
uninterpretable. Its two tag sets also disagree in sign (+0.303 STRICT, −0.260 WIDE),
which by the freeze's own terms is the finding, not a number to quote.

This file freezes a **second** prediction set before the replacement statistic is ever
applied to the test set. It is written from `results/controls.json`, a run that
**excludes DALR by construction**, so the statistic was chosen without seeing the answer.

## Why the statistic changed

Jensen–Shannon divergence between a group's name-frequency distribution and the Irish
reference does separate the known controls — IONA 0.653 [0.635, 0.674] vs PICT 0.713
[0.682, 0.748], non-overlapping — where coverage does not.

But **JSD is confounded by group concentration**, and this must not be waved past: both
north-channel groups sit above the whole six-province Irish band, and IONA is the
*positive* control, so the band is measuring how tight a group is and not how Irish it
is. A province is a heterogeneous aggregate; Iona is one house with the same abbots
recurring (rarefied TTR 0.512 against 0.571–0.662 for provinces).

The fix is matched comparanda: **eight tight Irish groups** of ≥146 name-tokens, single
houses and single dynasties, monastic *and* secular — ARMAGH, CLONMACNOIS, KILDARE,
ULAID, MIDE, CIANNACHTA, BREGA, UI_MAINE — whose all-token TTRs (0.326–0.592) bracket
both IONA (0.443) and DALR. Like is then compared with like.

## Frozen predictions

**Q1 — positive control, matched.** `jsd(IONA)` falls **inside** the tight-Irish band.
*Fails if* it is above the band maximum. A failure refutes the concentration explanation,
and JSD is then unusable — DALR's value must not be interpreted at all.

**Q2 — negative control.** `jsd(PICT)` falls **above** the tight-Irish band maximum.
*Fails if* PICT sits inside the band. A failure means this axis has no power on either
statistic tried, and the honest output of the session is the ceiling result.

**Q3 — the test (only interpretable if Q1 and Q2 both pass).** `jsd(DALR)` falls
**inside** the tight-Irish band — the Argyll secular name stock is compositionally an
Irish dynasty's name stock. *Fails if* `jsd(DALR)` is above the band maximum, or at or
above `jsd(PICT)`'s lower 95 % bound.

**Q4 — direction (unchanged in substance from P5).** Predict
`pool_first_rate(DALR) ≈ pool_first_rate(IONA)`, both above the tight-Irish band's own
rate, since both are Argyll-resident groups drawing on a shared pool attested earlier in
the larger Irish record. *Fails if* DALR's rate is significantly **below** IONA's, which
would be the signature of an Argyll-first component in the secular material that the
Columban material lacks.

Reported under both tag sets. **If STRICT and WIDE disagree, the disagreement is the
finding.** Note for the record: the WIDE Pictish set violates this attempt's own
place-names-and-ethnonyms-only rule by including `Nechtan`, a personal name; a sensitivity
run drops it.

## Standing limit, restated

This measures onomastic composition. It bears on propositions (b) and (c). **It cannot
speak to (a), folk migration**, and no result below may be read as doing so.
