# FREEZE — 2026-09-24, onomastic composition of the north-channel material

Written **after** the scoping run (`results/scope.json`, sample sizes only) and the power
run (`results/power.json`, Irish reference pool only), and **before** any group's outcome
statistic was computed. Neither prior run touches IONA / DALR / PICT outcome values.

Frozen at commit: see the commit that adds this file. `src/regions.py`, `src/names.py`,
`src/run_scope.py`, `src/run_power.py` are frozen with it.

## What is being tested, and what it can and cannot support

**Tested:** whether the personal-name inventory attached to Argyll-secular ("Dál Riata")
contexts in the Irish annals is compositionally an Irish inventory.

**This bears on success criterion 2 — the separation of the three conflated propositions:**

- (a) a substantial **folk migration** Ireland → Argyll
- (b) a ruling dynasty **claiming Irish descent**
- (c) **Gaelic spreading** from Ireland to Argyll

An onomastic test speaks to (b) and (c). **It does not speak to (a)** and no result here
should be read as doing so: elite names are not a population sample, and a name stock can
be adopted without anybody moving. This limit is stated here, before the result, so it
cannot be quietly relaxed afterwards.

## Design

Three-way split of the north-channel material with a **known-answer control at each end**,
scored in the same cell, per `PRACTICES.md`:

| group | what it is | expected |
|---|---|---|
| `IONA` | Columban familia — Irish-recruited, resident in Argyll | **positive control: must look Irish** |
| `DALR` | Dál Riata / Argyll secular | **the test set** |
| `PICT` | Picts / Fortriu — different people, P-Celtic | **negative control: must look non-Irish** |

Outcome statistic **cov(G)** = fraction of G's name-tokens whose normalised skeleton is
attested at least once in the period-matched Irish reference pool. Window 550–900.
Coverage for a pool draw is computed **held-out** (the drawn entries are removed from the
reference first), because without that the statistic is ~1.0 by construction.

Scale-free position between the controls:
`pos(G) = (cov(G) − cov(PICT)) / (cov(IONA) − cov(PICT))`. 1 = Iona-like, 0 = Pict-like.
Every cell is reported, not only the contrast.

Null: 2,000 period-matched size-matched draws from the Irish reference pool.
Measured null (from `results/power.json`, STRICT): mean cov 0.841, and for the group sizes
actually available the 95 % interval is **[0.766, 0.906] at n = 192** and
**[0.775, 0.901] at n = 221**. The test can therefore detect a coverage drop of about
**0.07–0.08** and no smaller. Anything subtler than that is below this corpus's resolution
and will be reported as untestable, not as absent.

Every headline number is reported under **two tag sets** (STRICT, WIDE), because the sister
folder established that on this corpus the gazetteer can decide the answer. **If STRICT and
WIDE disagree, that disagreement is the finding.**

## Frozen predictions

**P1 — positive control.** `cov(IONA)` lies **inside** the Irish null 95 % interval for its
own n (STRICT: ≥ 0.766). *Fails if* it falls below the 2.5 % tail. A failure means the
extractor or the gazetteer is broken and **no other result in this attempt may be believed**.

**P2 — negative control.** `cov(PICT)` falls **below** the Irish null 2.5 % tail for its own
n (STRICT n = 221: < 0.775). *Fails if* PICT sits inside the null. A failure means the
statistic has no power on this axis and P3 is uninterpretable.

**P3 — the test.** `pos(DALR) > 0.5`: the Argyll-secular name stock sits **closer to the
Columban (Irish-recruited) end than to the Pictish end**. *Fails if* `pos(DALR) ≤ 0.5`, or
if `cov(DALR)` sits at or below `cov(PICT)`.

**P4 — founder effect.** Rarefied type/token ratio of `DALR` at matched n is **not** below
the Irish null 2.5 % tail — i.e. no detectable founder bottleneck in the Argyll inventory.
*Fails if* TTR(DALR) falls below that tail. (A founder bottleneck is what a small migrating
elite founding a dynasty c. 500 would leave; its absence is informative against the
*strong* form of that model, not against migration as such.)

**P5 — direction.** For name skeletons attested in **both** DALR and IRISH, the Irish
first-attestation is earlier than the Argyll one more often than chance. The relevant
comparison is **not** 50 % — the corpus is Irish-dense, so Irish-first is expected by
sampling alone. The control is `IONA`, an Irish-derived population resident in Argyll:
predict **asymmetry(DALR) ≈ asymmetry(IONA)**, both Irish-first. *Fails if* DALR's
Irish-first rate is significantly **below** IONA's, which would be the signature of an
Argyll-first (reverse-flow) component in the secular material that the Columban material
lacks.

## Pre-registered interpretation

- P3 passes, P4 passes → Argyll-secular naming is an Irish provincial inventory with no
  bottleneck. Consistent with (b) and (c); silent on (a).
- P3 passes but `cov(DALR)` is nevertheless below the Irish null → a **mixed** inventory:
  Irish-derived stock carrying a real non-Irish component. Supports a contact/mixed
  picture over a clean colonial one.
- P3 fails → the Argyll secular name stock is not Irish-derived, which would be a
  substantive point against (b)/(c) as usually stated.
