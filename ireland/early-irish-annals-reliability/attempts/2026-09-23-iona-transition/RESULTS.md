# When did Scottish news stop reaching the Irish annals?

**2026-09-23 · Claude Opus 5 · starting session on `ireland/early-irish-annals-reliability`**

Predictions were frozen in [`FREEZE.md`](FREEZE.md) and committed before any time
series was computed. **One of seven passed.** The failures are the result.

---

## 0. What this measures, and what it does not

The standard reconstruction (Bannerman; Charles-Edwards, *The Chronicle of Ireland*,
2006) is that the chronicle underlying AU, AT and CS was kept at Iona from the later
6th century and continued in Ireland from c. 740. That is a claim about where a
manuscript sat. What is measurable here is something narrower: **the rate at which
Scottish material enters the record**. A scriptorium move predicts that rate to fall,
but so does the Viking destruction of Iona (raids 795, 802, 806; the Columban
headquarters moved to Kells 807–814). The two rivals differ in *date*, which is why
the whole session is about locating a break rather than detecting one.

Corpus: the four CELT English translations — Annals of Ulster (T100001A), Tigernach
(T100002A), Inisfallen (T100004), Chronicon Scotorum (T100016) — parsed to 13,414
entries, 11,389 of them non-kalend and ≥3 words. **The raw texts are not committed**:
CELT marks them `restricted` and the translations are in copyright. `src/fetch.py`
re-creates them; everything else here is derived.

## 1. Pipeline validation (run before the freeze, both passed)

| Check | Published fact | Recovered |
|---|---|---|
| AU's AD offset | AU's own `AD nnn` runs one year behind the true year to 1014, correct after | 600–799: 198/199 at +1 · 800–1013: 212/213 at +1 · 1014–1131: 115/116 at 0. Unbroken from AU 489 |
| Manuscript lacunae | CS 723–804, AT 766–973, AU 1115.4–1162.3 | Gap scan finds CS **723–803**, AT **767–973** (and 1004–1016), AU **1133–1154** |

Neither was encoded in the markup. The parser was told nothing about either.

## 2. There is a real, datable break — and it is not where it was predicted

AU, SCOT tag, 550–1000: 2,730 entries in 450 years, **120 tagged**.

| | k/n | rate |
|---|---|---|
| 550–807 | 97/1490 | **6.51 %** |
| 808–999 | 23/1240 | **1.85 %** |

Single-changepoint binomial scan: **argmax 808**, statistic 38.04, permutation
p = **0.0002** (5,000 draws, entries reassigned across years with per-year counts
held fixed). Bootstrap 95 % CI on the cut [727, 885]; χ²(1) support interval [737, 822].

**It is a step, not a slide.** A searched step beats a fitted logistic trend in year by
ΔLL 5.39; simulating under that fitted smooth trend and paying the same search cost,
p = **0.017** (null gain p95 = 4.01).

**A second changepoint does not survive its budget.** The best two-cut fit (738, 881;
8.0 % → 3.7 % → 0.9 %) beats one cut by 11.56 — but searching the same 2-D grid on
permuted data produces an improvement ≥ 11.56 in 5.2 % of draws (null p95 = 11.61).
A χ² test on 2 df would have given p ≈ 0.003 and a two-step decline would have been
written up as established. It is not.

### Frozen P1 fails, and it is not a power failure

Simulating a **sharp step at 740** with rates fitted at that cut (7.81 % → 2.76 %) on
AU's real year profile: the fitted argmax has median 739, 95 % range [711, 767], and
lands at ≥ 808 in **0.53 %** of 3,000 replicates. P(argmax at least as far from 740 as
the observed 808) = **0.0097**.

Power analysis confirms this is not small-n: on AU's actual year profile a clean 2×
step at 740 is detected with power **0.97** and localised within ±20 years in **78 %**
of replicates (median error 6 years). The null calibrates — a flat series rejects at
0.040 against a nominal 0.05.

**So the traditional c. 740, modelled as a sharp step in Scottish content, is rejected
at p ≈ 0.01**, and frozen **P4** fails too: 808 sits inside [785, 835], the window in
which I committed in advance to preferring the Viking explanation.

## 3. Then the rejection dissolves under a tag-composition check

Leave-one-term-out on the gazetteer:

| tag dropped | tagged | fitted cut |
|---|---|---|
| (none) | 120 | 808 |
| **Iona (Í / Ia / Iona)** | 76 | **738** |
| Pict\* | 98 | 816 |
| Dál Riata | 104 | 881 |
| other Scottish places | 89 | 793 |

Removing mentions of Iona *by name* moves the break 70 years earlier. Splitting the
tag into **TERRITORY** (Dál Riata, Pictland, Argyll/Clyde topography) and **IONA**:

| series | n | cut | rate change | perm p | P(as far as obs. \| step at 740) | P(as far as obs. \| step at 808) |
|---|---|---|---|---|---|---|
| TERRITORY | 76 | **738** | 5.43 % → 1.56 % | 0.0002 | **0.73** | **0.012** |
| IONA | 47 | 830 | 2.37 % → 0.67 % | 0.0102 | 0.28 | 0.40 |

Read alone, TERRITORY is fully consistent with a sharp step at 740 and *rejects* 808 —
the exact mirror image of the full-tag result. That is an attractive story: the
chronicle's local Scottish horizon closes c. 740 when it leaves Iona, while Iona itself,
a famous house whose abbots' obits an Irish annalist would keep receiving, fades later.

**The story does not survive its own null.** Permuting only the TERRITORY/IONA label
among the 120 Scottish entries (76 territorial, 44 Iona-only; entries naming both
count as territorial so the split is disjoint), holding each in its own year — which preserves both the
year profile and the overall Scottish time course and destroys only the
subset-to-date association — the 92-year gap has two-sided p = **0.183** (one-sided
0.094), against a null 95 % range of **±144 years**. Splitting 120 entries into 76 and
44 buys a date difference of this size for nothing.

**The honest conclusion is that this corpus locates one break in Scottish content and
cannot say whether it belongs to 740 or to 808.** Which answer you get is decided by
whether mentions of Iona count as Scottish news — a definitional choice, not an
empirical one.

## 4. The frozen two-sided test fails, and it fails for the right reason

**P5** predicted a simultaneous rise in midland-Irish content. Raw proportions deliver
it spectacularly: MIDLAND 8.73 % → 22.40 % at cut 758, permutation p = 0.0005,
bootstrap CI [745, 782] — tighter than anything else in this session.

It is mostly an artefact. Per-year tag proportions share one denominator, so classes
that fall force classes that rise. Measured **within** the Irish class,
MIDLAND/(MIDLAND+MUNSTER) goes 65.6 % → 77.0 % at cut 748, p = **0.117** — not
significant. Munster rises alongside the midlands; what actually changes is that
entries become more regionally specified in general (untagged 80.7 % → 59.6 %).

Every cell, AU, % of non-kalend entries (classes overlap):

| block | n | SCOT | INSULAR | MIDLAND | MUNSTER | untagged |
|---|---|---|---|---|---|---|
| 550–599 | 145 | 5.5 | 0.0 | 11.0 | 2.8 | 80.7 |
| 600–649 | 169 | 4.7 | 4.7 | 5.9 | 3.6 | 81.7 |
| 650–699 | 261 | 8.4 | 5.4 | 6.9 | 4.6 | 76.6 |
| 700–749 | 411 | 8.0 | 3.4 | 9.5 | 6.1 | 74.5 |
| 750–799 | 430 | 4.9 | 1.6 | 19.5 | 5.6 | 71.9 |
| 800–849 | 470 | 2.3 | 1.1 | 23.0 | 9.1 | 67.4 |
| 850–899 | 322 | 3.7 | 3.7 | 28.3 | 8.1 | 59.6 |
| 900–949 | 279 | 0.0 | 2.2 | 21.9 | 10.0 | 68.5 |
| 950–999 | 243 | 2.1 | 2.9 | 16.0 | 11.5 | 69.1 |

**P3 (specificity) also fails on raw proportions** — INSULAR falls significantly too
(4.66 % → 1.98 %, p = 0.011). The scale-free version partly rescues it: the Scottish
*share of foreign news*, SCOT/(SCOT+INSULAR), falls 72.8 % → 42.9 % at cut 816,
p = 0.0037. Scottish news declines faster than foreign news in general, but the
chronicle was losing distant news across the board.

## 5. Out-of-sample witnesses

| test | pre | post | fold | Fisher p | power at a 2× drop |
|---|---|---|---|---|---|
| **CS** across its own 723–803 lacuna (SCOT) | 25/493 = 5.07 % | 14/853 = 1.64 % | 0.32 | **0.0004** | 0.73 |
| CS, TERRITORY | 11/493 = 2.23 % | 5/853 = 0.59 % | 0.26 | 0.0088 | — |
| CS, IONA | 15/493 = 3.04 % | 9/853 = 1.06 % | 0.35 | 0.0084 | — |
| AT, SCOT, split at 738 | 39/837 = 4.66 % | 6/270 = 2.22 % | 0.48 | 0.050 | 0.47 |
| AI, SCOT, split at 808 | 7/409 = 1.71 % | 6/393 = 1.53 % | 0.89 | 0.53 | **0.17** |

**P2a passes** and it is the strongest result in the session, because Chronicon Scotorum
is an independent manuscript tradition (Clonmacnoise, not Ulster) and its lacuna hands
over a clean before/after comparison that no choice made here could have tuned. The
level fall is not an artefact of AU's redaction.

**P2b's failure carries no information.** AI holds 13 Scottish-tagged entries in
550–1000. At that size even a *total disappearance* of Scottish content would be
detected only 83 % of the time, and a 2× drop 17 % of the time. AI cannot test this and
its null result should not be cited as evidence either way.

CS also cannot separate 740 from 808 — its lacuna sits exactly over the window.

## 6. Tagger audit

40 SCOT-tagged and 40 untagged AU entries, 550–1000, sampled at random and read.

- **Precision 40/40.** Every tagged entry is genuinely Scottish, Dál Riatan, Pictish or
  Ionan. The place-name-and-ethnonym-only rule works.
- **Recall is the weak side, as declared.** Of 40 untagged, one is a clear miss
  (AU 654.5, Dúnchad son of Conaing, a king of Dál Riata named with no place-name — the
  cost of excluding personal names) and one is a declared exclusion (AU 967.1, "king of
  Scotland … the Scots themselves"). 1–2/40 implies roughly 65–130 missed entries against
  120 tagged, i.e. **recall of order 50 %**, with a wide interval.
- The naming convention does **not** drift: obits are phrased "abbot of Í" consistently
  from AU 641 to AU 987, so the recall loss is not obviously time-varying. But the
  *Scotland/Scots* exclusion bites only after c. 900 and therefore exaggerates the late
  decline; including the ambiguous terms is the sensitivity run, and SCOT_AMBIG on its
  own rises rather than falls (1.60 % → 5.24 %, cut 952).

## 7. Scorecard against the freeze

| | prediction | outcome |
|---|---|---|
| P1 | AU SCOT changepoint in [715, 765] | **FAIL** — 808. Significant (p = 0.0002) but misplaced, and not through lack of power |
| P2a | CS falls across its lacuna | **PASS** — p = 0.0004, adequately powered |
| P2b | AI falls | **FAIL, uninformative** — power 0.17 at a 2× drop |
| P2c | AT falls (declared underpowered) | direction correct, p = 0.050 at cut 738; undefined at 808 |
| P3 | INSULAR does not fall | **FAIL** on raw proportions; partly rescued scale-free |
| P4 | changepoint not in [785, 835] | **FAIL** — 808 is in the Viking window |
| P5 | matching midland rise within ±40 yr | **FAIL** — the rise is compositional; scale-free p = 0.117 |

## 8. What this session establishes

1. Scottish content in the Irish annals falls by a factor of ~3.5 between the 7th–8th
   century plateau and the 9th–10th century. The fall is real (p = 0.0002), is a
   **step rather than a trend** (p = 0.017 budget-matched), and reproduces in an
   independent manuscript tradition (CS, p = 0.0004).
2. **The date cannot be resolved.** 740 and 808 are each rejected by one defensible
   version of the tag and accepted by the other, and the difference between those
   versions is not statistically distinguishable (p = 0.18). Anyone who reports either
   date from this evidence is reporting their gazetteer.
3. The **two-sided signature of a chronicle relocating into the Irish midlands is not
   present** once compositional effects are removed. What the annals show after c. 750
   is not a midland focus but a general rise in regional specificity, shared by Munster.
4. The binding constraint is **tag recall, not corpus size**: 120 Scottish-tagged
   entries at ~50 % recall. The power curve says doubling the tagged count takes p90
   localisation error from 44 years to 16.
