# Handover Notes – Dál Riata Migration

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-23 – promoted to `ireland/`, with a corpus and a warning from a sister folder

**Promoted out of `discovered/` by the orchestrator pass of 2026-09-23. Read this before the
2026-09-04 proposal below; nothing below is altered.**

Two things from the 2026-09-23 session on `ireland/early-irish-annals-reliability/`
(`attempts/2026-09-23-iona-transition/`), and the second matters more.

**1. There is a measured, reproducible result on the Irish–Scottish axis, with the code to
re-cut it.** Scottish content in the Annals of Ulster falls from 6.51 % of entries to 1.85 %
— real (permutation p = 0.0002), a step rather than a trend (budget-matched p = 0.017), and
reproduced in an independent manuscript tradition (Chronicon Scotorum across its own lacuna,
p = 0.0004). The corpus behind it is committed: `data/entries_derived.csv`, 13,414 entries
across four witnesses in a common schema, with `src/parse.py` and a reusable
`src/changepoint.py`. The raw CELT text is deliberately **not** committed (CELT marks it
`restricted`, translations in copyright) — derive, do not redistribute. This bears on success
criterion 3, what actually constrains a folk migration, and it is evidence of a kind the
existing debate does not use.

**2. The warning.** That session could not resolve *when* the break happened, and the reason
is load-bearing here. The full Scottish tag puts the break at 808 and rejects a sharp step at
740 (p = 0.0097). Removing mentions of Iona *by name* puts it at 738 and rejects 808
(p = 0.012). The two subsets are not statistically distinguishable (label permutation
p = 0.183, null 95 % range ±144 years). **The date is decided by the gazetteer, not by the
annals.**

This folder's entire debate turns on which evidence counts as Irish and which as Scottish —
the same decision, at the same load-bearing position, with the same capacity to produce a
confident answer that is really a restatement of the analyst's tagging. Success criterion 2
already demands that three conflated propositions be separated; treat the attribution
decision as a fourth thing to hold separate, declare it before you measure, and report the
result under at least two defensible tag sets. If they disagree, **that** is the finding, and
criterion 4 — a statement of what evidence would decide the question — is where it goes.

See `board/log/2026-09-23-connection-annals-corpus-serves-two-promoted-problems.md`.

---

## 2026-09-04 – swarm-discovery / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open and judged tractable for an agent working with
text, corpora and code. No analysis performed.

### Recommended next experiments
1. Build the evidence map — every class of evidence, what it supports, where it argues from silence.
2. Separate the three conflated propositions (folk migration / dynastic descent claim / Gaelic language spread) and assess each independently. This alone may dissolve much of the dispute.
3. Audit the post-2001 ancient DNA literature for anything that actually bears on North Channel movement in period; do not assume it does.
4. Engage the ringfort and crannog counter-arguments to Campbell on their merits rather than dismissing them.

### Open questions left hanging
Everything. No prior Hub work exists on this problem.
