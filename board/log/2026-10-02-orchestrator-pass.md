# Orchestrator pass — 2026-10-02

**Previous pass:** 2026-09-27 (`2026-09-27-orchestrator-pass.md`, plus the same day's
`2026-09-27-external-claim-triage.md` and `2026-09-27-reconciliation.md`).
No evidence was analysed in this pass. Where this entry states a research fact it is quoting a folder
or a validator.

---

## 1. The finding: the board is idle, and nothing is blocking it

The last Breaker session closed `ciphers/debosnys-ciphers` at **2026-09-27 20:30 UTC**. At the
routine's six-hour cadence, the gap to this pass is about **eighteen consecutive missed firings**. The
only commits to `main` in those four and a half days are the owner's site and visual work (#21–#28);
there is not one research commit. Every problem folder reads idle 7–9 days in the draw.

What makes this the finding rather than a symptom is everything that is *not* wrong:

| check | result |
|---|---|
| open pull requests | **none** — the Codex queue is clear, nothing waiting on review |
| `board/active/` | only `.gitkeep` — **no stale claim to clear, fifth consecutive clean pass** |
| `npm run draw` | runs, names a pick with a written next move (`historical-texts/proto-elamite`) |
| `PICK-UP` marks | none; no held claim is yet past 14 days |
| `NO NEXT MOVE` marks | two, both filing defects, both fixed in this pass |
| solve-claims short of verdicts | none — mesha, ennis, VENONA and the gold bars each carry three |

So the board is not jammed, not under-specified, and not waiting on Overwatch for anything except the
two panels this pass convened. **It is simply not being drawn from.** That is a fact about the Breaker
routine — firing, failing, or switched off — and no promotion, re-ranking or priority overlay written
by an orchestrator addresses it. It is recorded at the top of `STATUS.md`, at the top of
`board/TOP_INTEREST.md`, and pushed to the owner.

**Honest limit on this observation.** A session is not a process and I cannot see the routine's own
logs. What I can establish from inside the repository is that no Breaker session committed anything,
and that nothing in the repository would have stopped one. If the routine fired and the sessions died
before their first commit, that is indistinguishable from here.

## 2. Panels, which were the standing constraint

Linear A and Byblos had been panel-pending since **2026-09-17**. The 2026-09-25 pass convened both and
committed in-progress artifacts — `historical-texts/linear-a/validation/2026-09-25/` holds a working
two-witness reproduction harness (GORILA-via-Douros and SigLA) with recorded output, and
`historical-texts/byblos-syllabary/validation/2026-09-25/` holds four OCBI parsing and refutation
scripts with theirs — **and never posted a verdict.** For a week the board therefore showed two panels
as owed to Overwatch while two substantially complete refutation sessions sat unread in the folders.

That is worth naming as a failure mode distinct from "validation falls behind": **an unposted verdict
is worse than an unconvened panel**, because the work is paid for and invisible, and the next session
cannot tell the difference. Both panels were convened on 2026-10-02 — three validators each, the third
explicitly assigned to refute, judged against the criteria already in each `PROBLEM.md`, reproducing
from the raw corpora rather than reviewing the writeups, and told that the 09-25 artifacts are prior
panel material to run and go beyond rather than to adopt.

Outcomes are recorded in §7 below and in each folder.

## 3. Draw defects fixed

**Both `NO NEXT MOVE` marks were filing defects, not empty folders.**
`discovered/crelly-1648-coded-correspondence/` and `discovered/ormond-anglesey-1663-cipher/` each had a
concrete move from their 2026-09-17 finder session — but as a `- Best next move:` **bullet inside a
session block**, and as *First bounded experiment* in `PROBLEM.md`. `readNextMove` in
`scripts/derive.mjs` matches on a **heading**, so neither the draw nor the site could see it. Each now
carries an additive orchestrator note restating the move under a heading the draw reads, with the
source and the sibling pack cited.

**Generalisable lesson for every role:** a next move that is not under a heading does not exist as far
as the board is concerned. The heading pattern the draw accepts is `## … next experiments / next move /
next tests / next task / next order / do this next / best next …`. Writing the move in `PROBLEM.md`
instead does not count.

**No `PICK-UP` marks**, but the four HELD 3 × PARTIAL files are idle 7–8 days and cross the 14-day
threshold between **2026-10-08 and 2026-10-09** if nothing runs. Said so in `STATUS.md`. Worth noting
what that means on an idle board: pick-up is designed to stop promising work drifting, but with nothing
drawing at all it will simply re-present the oldest unfinished business ahead of the most tractable
work. The rule is not wrong; it is being asked to do a job it was not designed for.

## 4. Dashboard versus reality

**Two folders existed on disk and not on `STATUS.md`.** `historical-controversies/venona-baron/` and
`discovered/historia-augusta-authorship/` both landed in the **2026-09-27 reconciliation commit** and
were never entered in the tables. `venona-baron` has been *drawable the whole time* and ranks 8th in
stream C; `historia-augusta-authorship` ranks just below the top-8 cut in the same stream. Both now
have rows, and both are named in the stream C brief.

**The narrow lesson, which is the one worth keeping:** a reconciliation commit that imports folders
must add their rows in the same commit, because the draw scans the filesystem and will happily rank a
problem this dashboard has never heard of. The failure is not that a session was sent somewhere wrong
— it is that an orchestrator reading only `STATUS.md` would not have known either folder existed.

**One standing override, for a mechanism gap rather than a disagreement.**
`discovered/cypro-minoan/` has been recorded since 2026-09-25 as evidence-blocked until its corpus is
digitised — explicitly *not* a tractability judgement, and to be treated like the 1641 Depositions
archive request — yet the draw ranked it 5th in stream B as `unworked`, debt 10, so it would eventually
have been drawn. The cause: `stageOf` can only reach `blocked` through the `STATUS.md` table's *status*
column, and `parseStatusRows` gives a `discovered/` row's third column to the **suggested category**
instead, so the status string for such a row is always empty. Its row now reads
`historical-texts — evidence-blocked`, which ranks it `blocked` (weight 0.5, never leads) while
`inferDomain` keeps it in stream B from the pack's own text. **The underlying gap is in
`scripts/derive.mjs`, which is the owner's file, so it is recorded for a human decision rather than
patched here.** The override is written into `board/TOP_INTEREST.md` with this reason, per the rule
that an override with no reason is drift with extra steps.

## 5. Silos broken

Two connection entries were posted, and in both cases the knowledge was written into the handovers
rather than only into the log. That distinction is the whole point of the role: **this board has
already measured that promotion does not create sessions, and a log entry is the same — a Breaker
arriving at Voynich in three weeks reads `HANDOVER.md` and the stream brief, not a five-week-old log
file.**

**(a) Calibrate every shuffle null at the target's own token count, and stop reading a doublet deficit
as a hoax signature.** From the 2026-09-27 `ciphers/blitz-ciphers/` session. A z-score scales with
√length, so cut each genuine comparandum into non-overlapping blocks of *exactly* the target's token
count and report a percentile — "0 of 402 genuine blocks at 470 tokens fall this low" — and the same
blocks give the power curve free. And a doublet deficit is what genuine ciphertext looks like (Borg
z = -47.3, Copiale z = -33.0, against Σpᵢ² of 4–7 % versus real rates of 1–2 %), so the anomalous
document is the one sitting *near* Σpᵢ². Carried into **seven** `HANDOVER.md` files with a
folder-specific reason each — Voynich, Kryptos, Beale, the gold bars, Debosnys, Rohonc, Proto-Elamite —
together with the `matthewdgreen/cipher_benchmark` comparandum corpus and its committed fetch script.
`2026-10-02-connection-length-matched-nulls-and-the-doublet-trap.md`.

**Deliberately not carried into Byblos or Linear A**, whose handovers the live panels were reading;
editing them mid-panel risks confusing a verdict about what the claimant wrote. **The next pass carries
it into both** — Byblos's criterion 1 demands a power analysis and this is the cheapest way to produce
one. That is a specific instruction to the next orchestrator, not a deferral of a decision.

**(b) Crelly 1648 and Ormond–Anglesey 1663 are one archival lane.** Same period, cipher class,
archival route (HMC calendars, archive.org scans of the same series, JSTOR-held Irish journals) and the
same unverified-solution-status question — the seventeenth-century counterpart of the existing
VORFYDCGT/CD 286 arrangement, with `ciphers/british-cyphers-cd286/` as the lane's live folder, which
neither pack cited. Two consequences a session should act on: pull the other pack's shelfmark while in
the same catalogue, and measure the passage against
`discovered/short-cipher-validation-bound/` as soon as a verbatim ciphertext exists, because partially
enciphered letters of this period hide only names, numbers and a clause or two — the regime where a
readable high-scoring decryption is not evidence. This board has already lost
`discovered/ormonde-maltravers-1634-cipher/` to an external solve published days before it was
proposed, which is why the solution-status ledger **is** the session rather than preliminary work.
`2026-10-02-connection-the-two-irish-archival-cipher-packs-are-one-lane.md`.

## 6. `PRACTICES.md`: curated, and split

Last curated **2026-09-25**, so the four craft lessons from the 2026-09-27 sessions had never been
distilled. Added: the shuffle-null length-calibration rule; the doublet deficit; sign identity across
two transcription systems when a key is fitted in one and tested in the other (Debosnys, p = 0.0027 on
a comparison sheet nobody had made in four days of building on the key); and a figure being the least
stable element of its own narrative, with Templo Mayor's constant staging against its varying number
(80,400 / 80,400 / none / 72,344) and `black-death-mortality-figure` named as next in line for the
instrument. Folded in rather than added: price a confound with the error model the transcriber
*declared*, not a generic one.

That took the file to **35 KB**, past the ~32 KB threshold at which the previous curator named two
families as candidates for the annexe treatment. **The split was done in this pass rather than
bequeathed again**, per the standing rule that a decision recorded twice as deferred is a decision
being failed: the **ciphertext and unknown-script statistics** family — five rules — moved to
**`board/PRACTICES-CIPHERTEXT.md`**, flagged not-optional for streams A and B. The general statistical
craft (nulls, power, p-floors, the information ceiling, search freedom, frozen predictions) deliberately
stayed in the main file, because it applies to every stream; only the rules about what genuine
ciphertext *looks like* moved. **29.5 KB → 27.3 KB plus a 9.6 KB annexe, four rules added, none lost.**
The predecessor's accounting block was cut, as the predecessor cut theirs — by this file's own standard
an accounting block is about a pass, not about craft, and it belongs here. The remaining candidate for
the same treatment is the archival/identity-chain family.

## 7. Panel outcomes

*Recorded below as the verdicts landed. Every claim stays* `HELD — awaiting human sign-off` *whatever
the verdicts say; three passes publish nothing, and an orchestrator does not overrule a validator.*

**To be completed in this pass.**

## 8. Filing, and what was deliberately not done

**No promotions out of `discovered/` this pass, and this is a decision rather than a deferral.** The
2026-09-25 pass closed the residual queue as a standing draw order precisely so this would not be
re-litigated every pass, and its promotion trigger is a category going cold — *no unblocked new work
for ten days*. By that test every category is now cold, but the cause is that nothing is being drawn at
all, not an imbalance between categories, and `discovered/` packs are claimable where they sit under
the 2026-09-27 framework. **Promoting a dozen folders onto a board that nothing is reading would be
tidying presented as progress, and this board already has a measurement saying promotion does not
create sessions** (Dál Riata: promoted on the strongest available ground, still never worked). The
standing order in `STATUS.md` stands unchanged; the next pass draws from it when a category is cold for
a reason other than a stopped routine.

**Audited instead:** every live pack has a suggested category and a startable next move. Fourteen live
packs, sixteen `MOVED.md` stubs, one finder manifest directory and one methodological asset
(`short-cipher-validation-bound`, which stays permanently and is cited from `PRACTICES.md`). Two packs
were missing a readable next move and are fixed; one pack was missing from the dashboard and is added.

**Stream briefs** (`board/streams/A–D`) were all updated: the new annexe and the length-calibration
rule into A and B, the panel status and the pending carry into B, the staging-versus-figure rule and the
two invisible folders into C, and the Crelly/Ormond lane cross-reference into D so a session looking
for Irish archival work knows those two packs are ranked in stream A and why.
