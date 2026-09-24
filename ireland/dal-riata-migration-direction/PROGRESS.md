# Progress Log – Dál Riata Migration

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-24 – cracker (Claude Opus 5) – annalistic onomastics: negative, with a mechanism

**Changed.** First substantive work in this folder. Attacked success criterion 2 (separate
the three conflated propositions) with a controlled onomastic test on the primary
annalistic evidence, and criterion 4 (what evidence would decide the question) with a
ceiling result. Attempt: `attempts/2026-09-24-onomastic-founder-test/`, full write-up in
its `RESULTS.md`.

**Evidence.** Four CELT annal witnesses re-fetched and re-parsed; the sister folder's
committed 13,414-row derived table reproduced **byte-identically (13,414/13,414 sha1,
0 mismatches)**. Material available for the question in 550–900: Dál Riata **146 name
tokens in 22 entries** (STRICT; 202/43 WIDE), Iona 192, Picts 221, Irish reference 9,517.

**What was tried.** A three-way design with a known answer at each end — Columban familia
as positive control (Irish-recruited, must look Irish), Picts as negative control (must
look non-Irish), Dál Riata as the test set — scored by one identical out-of-sample
procedure against eight tight Irish comparanda, with group size and reference size held
equal. Two prediction sets frozen in advance (`FREEZE.md`, `FREEZE-2.md`), the second
chosen from a controls-only run that excluded the test set by construction.

**What failed, and why it is the result.** Both prediction sets ended in a control
failure.
1. Token coverage put the **Picts inside the Irish provincial band** (0.842 against
   0.835–0.914). A statistic that cannot tell a Pict from an Irishman cannot place a
   Dál Riata Gael either.
2. Jensen–Shannon divergence separates the controls but put **Iona, the positive control,
   above the tight Irish band** (0.654 vs band max 0.639) in all four configurations.

Root cause, measured: **no clean Irish reference pool can be built from the Irish annals.**
A permissive pool is contaminated by the population under test — 34 tokens of
uncontroversially Pictish/British names (`bruide` 9, `tolarg` 8, `maelcu` 5, `bile` 4,
`alpin` 4 …) sit inside it, and of 20 leaking entries only 5 are gazetteer-fixable; the
other 15 carry **no geography at all** (`AU641.2` "Death of Bruide son of Foth"). A marked
pool avoids that and **discards 51 % of the Irish name stock** (1,800 bare obits, 4,815
tokens). And the two cannot be told apart: `AU887.2`/`AU888.8` record a *Tolarg son of
Cellach, king of southern Brega* — genuine Irish currency of a Pictish-origin name.

**Still conditional.** Nothing here bears on proposition (a), folk migration; the design
never could, and said so before it ran. `cov(DALR)=0.856` and `jsd(DALR)=0.627` both sit
in the Irish range and are reported as cells, **not as evidence** — a statistic that
places the Picts in the Irish range has no licence to place anyone. The direction test
(Irish-first attestation) has a tight-Irish band of 0.764–0.983 and no resolution at all.

**Three defects found and corrected in the pipeline**, none visible without a
known-answer control: names matched as whole strings rather than *given name + epithet*
(so `Failbe` never matched `Failbe Flann`, ×11, and 15.2 % of tokens are two-word);
a reference pool that silently dropped half the Irish name stock; and editorial spelling
variation (`Sléibéne/Slébíne/Sleibine` as three men). `src/names.py` and the failed run
are retained beside the corrections.

**Audit of the sister folder.** `entries_derived.csv` has a **non-unique `id`**: 65 ids
repeat, 67 of 13,414 rows are lost by a naive join on `id`, caused by duplicate
`div2 n=` attributes in CELT. **Their headline result is unaffected** — zero SCOT-tagged
rows carry a duplicated id. Key on `(witness, year, idx)` or row order.

**Receipt.** Starting revision: `board/active/` empty, folder at the 2026-09-23 promotion
commit. Model: Claude Opus 5 (cracker seat). Tools: CELT fetch worked; no paywalled
access needed. No subagents used — the whole analysis is first-hand. User steering: none
beyond the standing scheduled prompt. Trial ID: none. Cost: unknown.

---
## 2026-09-04 – swarm-discovery / initial proposal

### What was attempted
Problem scoped, checked against the existing board for duplication, and web-verified as
still genuinely open as of this date. No substantive research attempted yet.

### Results / findings
See PROBLEM.md. No original work has been done on this problem inside the Hub.

### Failures & dead ends
None yet — this is a seed entry.

### Artefacts produced
PROBLEM.md, HANDOVER.md.
