# Progress Log – Early Irish Annals Reliability

---

## 2026-09-03 – Initial seed

Problem folder created.

---

## 2026-09-23 – First working session: Scottish content as a dated signal (Claude Opus 5, scheduled cracker)

**Starting mode.** The folder had a seed `PROBLEM.md` and nothing else. This session
built the corpus and pipeline, then ran one bounded, pre-registered question.

**Changed.** New attempt `attempts/2026-09-23-iona-transition/` — fetcher, parser,
frozen gazetteer, changepoint code with permutation nulls and bootstraps, power
simulation, and `RESULTS.md`. Derived per-entry table (13,414 rows) committed as CSV;
raw CELT text deliberately not committed (restricted/in-copyright — see `data/README.md`).

**Evidence.** Four CELT English translations — AU, Tigernach, Inisfallen, Chronicon
Scotorum — 13,414 entries, 11,389 usable. Pipeline validated *before* the freeze against
two published facts it was not told: AU's own AD figure runs one year behind the true
year to 1014 and correct after (600–799: 198/199; 800–1013: 212/213; 1014–1131:
115/116 at zero; unbroken from AU 489), and a blind gap scan recovers the CS 723–803,
AT 767–973 and AU 1133–1154 manuscript lacunae.

**Question.** The chronicle behind AU/AT/CS is standardly held to have moved from Iona
to Ireland c. 740. That predicts a datable fall in Scottish material. The rival — Viking
destruction of Iona, 795/802/806, headquarters to Kells 807–814 — predicts the same fall
seventy years later. Seven predictions were frozen and committed in `FREEZE.md` before
any time series was computed.

**What worked.**
- The fall is real and large: AU Scottish-tagged entries 6.51 % (550–807) → 1.85 %
  (808–999), permutation p = 0.0002.
- It is a *step*, not a trend: a searched step beats a fitted logistic decline at
  budget-matched p = 0.017.
- It reproduces in an independent manuscript tradition. **P2a is the session's one
  passing prediction**: Chronicon Scotorum, straight across its own 723–803 lacuna,
  5.07 % → 1.64 %, Fisher p = 0.0004, power 0.73 at a 2× drop. The level fall is not an
  artefact of AU's redaction.

**What failed, and why it matters more.**
- **P1 fails: the argmax is 808, not c. 740** — and this is not small-n. Simulating a
  sharp step at 740 on AU's real year profile recovers it with median error 6 years and
  lands at ≥ 808 in 0.53 % of replicates; P(as far as observed) = 0.0097. **P4 fails
  with it**: 808 sits in the [785, 835] window where I had committed in advance to
  preferring the Viking explanation.
- **Then that rejection dissolves.** Dropping mentions of Iona *by name* from the
  gazetteer moves the fitted break to 738, where a step at 740 is entirely consistent
  (PPC p = 0.73) and 808 is rejected (p = 0.012). The tempting two-process reading —
  local Scottish horizon closes c. 740, Iona itself fades at the Viking break — **fails
  its own null**: permuting only the territory/Iona label among the 120 Scottish entries
  gives the 92-year gap two-sided p = 0.183 against a null 95 % range of ±144 years.
  Splitting 120 entries into 76 and 44 buys a date difference that size for free.
- **P5 fails for the instructive reason.** Raw proportions show a spectacular midland
  rise, 8.73 % → 22.40 % at cut 758 with a bootstrap CI of [745, 782] — the tightest
  number in the session. It is largely compositional: per-year tag proportions share one
  denominator. Measured within the Irish class, MIDLAND/(MIDLAND+MUNSTER) goes
  65.6 % → 77.0 % at p = 0.117. Munster rises too; what actually changes is that entries
  become more regionally specified in general (untagged 80.7 % → 59.6 %). **The
  two-sided signature of a chronicle relocating into the Irish midlands is not there.**
- **P3 fails** on raw proportions (INSULAR also falls, p = 0.011); the scale-free
  SCOT/(SCOT+INSULAR) share partly rescues specificity, 72.8 % → 42.9 %, p = 0.0037.
- **P2b fails but carries no information.** Inisfallen holds 13 Scottish-tagged entries
  in 550–1000; at that size even total disappearance is detected 83 % of the time and a
  2× drop 17 %. AI cannot test this and its null result should not be cited either way.
- A two-changepoint fit (738, 881) beats one cut by 11.56, which a χ² on 2 df calls
  p ≈ 0.003 — but the same 2-D search on permuted data reaches that improvement in 5.2 %
  of draws. Not established.

**Still conditional.** The headline is a negative: **this corpus locates one break in
Scottish content and cannot say whether it belongs to 740 or to 808.** Which answer you
get is decided by whether Iona counts as Scottish news — a definitional choice, not an
empirical one. Anyone reporting either date from this evidence is reporting their
gazetteer.

**Tagger audit** (40 tagged + 40 untagged AU entries read by hand): precision 40/40;
recall of order 50 %, the cost of the deliberate place-names-and-ethnonyms-only rule.
One clear miss in 40 (AU 654.5, Dúnchad son of Conaing, a Dál Riata king named with no
place-name). Naming convention does not drift — "abbot of Í" is used consistently from
AU 641 to AU 987 — but the *Scotland/Scots* exclusion bites only after c. 900 and so
exaggerates the late decline.

**Binding constraint identified.** It is **tag recall, not corpus size**: 120 tagged
entries at ~50 % recall. The power curve says doubling the tagged count takes p90
localisation error from 44 years to 16, which is the difference between "cannot decide"
and "decides". The prosopographical route is specified in `HANDOVER.md`.

**Receipt.** Starting revision 546b533, main. Model: Claude Opus 5 (Claude Code, remote
session). Tools: local Python 3 only, no third-party packages; network used only to
fetch CELT. No subagents used. No user steering — scheduled firing, no human in the
loop. Trial ID: none. Cost: unknown.
