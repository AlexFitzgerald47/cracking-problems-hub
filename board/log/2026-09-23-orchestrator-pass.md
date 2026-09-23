# Orchestrator pass — 2026-09-23

*Overwatch. No problem was worked by this session.*

## What this pass found

**The delivery problem did not recur, and that is the headline.** Four consecutive passes
recorded scheduled sessions firing and landing nothing. Since 2026-09-21 the repository has
taken **six distinct research sessions in 48 hours** — Junius (09-21 evening), Thera (09-22),
Caligula (09-22), a finder gap-fill run (09-22), Early Irish Annals (09-23) and Shakespeare
(09-23) — each with committed code, committed data, a `FREEZE.md` where predictions were
frozen before testing, and an updated handover. Three produced results general enough to
change how other folders work. The gap is not re-litigated here because it did not happen.

What it leaves is a different problem, and it is the one this pass existed to solve: **six
sessions of method in two days, most of it stranded in the folder that produced it.**

**PR queue: empty.** Third consecutive pass. Nothing to review, merge or reject. The
externally-run Codex lane has still landed no research commit since 2026-09-08 — fifteen
days — and is not contributing by the PR route either. Standing item for the human,
unchanged since it was escalated on 09-17.

**Claims: clean, and left alone.** `board/active/` is empty and correct. Every claim opened
since 09-17 was released by its own session in the commit that landed the work, including
the three opened since the last pass. **No claim was released by this pass because none
needed releasing** — the folder rule (`git log -1 -- <folder>`, never the claim file's date)
did not have to fire. Second consecutive pass that can say so.

## The correction that mattered most

**This dashboard was wrong about the board's own top priority for two days.** The 09-21 pass
named Junius "the cheapest high-value item on the board" and recommended a compute route past
its archival block. The Junius session ran that route to completion **the same evening** and
closed it, with committed evidence under `attempts/2026-09-21-shift-or-loss/`. The
recommendation then sat at the top of `STATUS.md` while three cracker cycles fired. Any
cracker who read the dashboard and not the handover would have spent a full session
re-running a closed experiment.

The general lesson is now a standing rule in `PRACTICES.md`: **`STATUS.md` is written once a
pass and a folder can close a route the same evening the dashboard recommends it. Where the
two disagree, the folder wins.** The orchestrator role file already says reality beats the
dashboard; what it did not say is that the dashboard's own *recommendations* go stale the
same way its status fields do, and faster, because a recommendation is exactly what a good
session acts on immediately.

Two more of the same species, both fixed: Thera and Early Irish Annals were both listed
**"never worked"** while both had been worked, and both had committed reusable pipelines
their successors are explicitly told not to rebuild.

## Validation

**Two panels were incomplete and this page claimed one of them was finished.** The 09-21 pass
recorded "the Ennis panel is now complete" — it had two verdicts. VENONA had one. Both were
completed this pass under `_roles/VALIDATOR.md`, refuter assigned explicitly in each case.
Both returned **3 × PARTIAL**, and every verdict on this board is now PARTIAL — there is no
PASS anywhere.

**VENONA BROWN/BRAUN: 3 × PARTIAL. HELD — awaiting human sign-off.** Not published as a solve
anywhere and `STATUS.md` is not updated to say solved. The panel's finding is sharper than
"unproven": Meredith is **unevidenced rather than contradicted**, and the reason is a process
failure the project's own files document — the candidate field was **closed by written
instruction, not exhausted**. `fraser-residence-kill-test.md` ends "BLOCKED / UNRESOLVED —
not passed" and Fraser was demoted the next day with no new evidence; the Barnard file's own
prescribed program was dropped; and constraint-ledger Q2 and Q3, the two *small and
enumerable* populations the cables actually name, were never run. The Smiths → Henry Hughes
bridge establishes only employment somewhere in the S. Smith & Sons group, which every
Hainault shop-floor employee satisfies better — and No. 976 points at the production line.

Three things the panel added that belong to the problem rather than to the verdict, and that
the folder's owner should carry into `PROBLEM.md` and `constraint-ledger.md`:

1. **A new primary constraint nobody had logged.** London No. 798 §4 has STANLEY "looking for
   work on an agricultural farm near the MUSIC" to defer call-up, so BROWN's July 1940 radio
   flat sat within working distance of farmland — the outer fringe, not inner London. Hainault
   in 1940 *was* farmland with the Hughes works in it. This points the search back at the
   Essex end that the Meredith detour abandoned.
2. **Two settled textual corrections**, independently recovered: "illicit **link**" (not
   "ink"), and the leak-reading of "a MUSIC from BROWN". Both *raise* the W/T bar rather than
   lowering it.
3. **Covernames in this corpus carry no identifying information.** An inventory of all 45
   glossed covernames found every resolved personal-name covername unrelated to the true name
   (BARCh = Kremer, ZhEROM = Labarthe, BAUER = Lieut. Hein). BRAUN is a null label. Separately,
   BROWN signs at No. 256 *inside* the residency officers' outgoing sequence
   (255 BARCh → **256 BROWN** → 259 BARCh) — a hypothesis class the claim never enumerated.

What survived the refuter and should stand as the project's real result: **the STANLEY/BROWN
role separation**, confirmed from the raw cable text.

**A methodological finding from validator 2's dissent, which is about the panel and not the
claim.** Two validators independently recovered the same two textual corrections from the
same two sources by near-identical routes, and validator 2 flags that this agreement must
**not** be counted as independent confirmation. That is precisely the correlated-error failure
`_roles/VALIDATOR.md` exists to prevent, and it is the first time a validator on this board
has caught it in their own panel. Recorded in `STATUS.md`: **agreement between validators
drawn from similar models is evidence only to the extent their routes differed — record the
route, not just the verdict.**

**Ennis STINGING: 3 × PARTIAL, and the panel is worth more than its verdict.** Three things
it produced that change what the folder should do next:

1. **The headline null figure is wrong by more than an order of magnitude, and must stop
   being quoted.** "0.406 %, about 1 in 246" is the most favourable of **four** values now in
   the repo, and it does not reproduce — the committed script returns a different figure on a
   current `cmudict`. It is also frozen-path, English-only, and conditional on the very
   deletion at issue. By exact enumeration over all 64,000,000 six-sign sequences under the
   12-reading cycle budget with an English ∪ Irish lexicon, the defensible figure is **7.2 %,
   about one in fourteen** — and 31.5 % charged for the affine family.
2. **The falsifier the board has been carrying as its cheap kill test is discharged, and it
   resolved in the claim's favour.** The refuter fetched the live OG(H)AM EpiDoc record and
   decomposed the editors' own ogham edition to code points: exactly one FEARN+AILM pair, so
   "the ogham letters VA repeated" means "VA, repeated from DMVA", not `VAVA` on the branch.
   `STATUS.md` had this as an open item. It is closed — stop carrying it.
3. **New evidence against the historical bridge, out of the claim's own cited source.** The
   refuter read all 45 pages of Hayden & Stifter 2025, which neither co-validator had gone
   past the abstract of. The attested nineteenth-century ogham ciphers — *ogam craobh*, *ogam
   coll*, *ogam consaine* — contain **no positional rotation**; the Minchin charms are plain
   ogham with no superimposed cipher; and the eye-charms are Irish prayers under `ar x`
   headings, a comparator predicting specifically *against* a bare English participle.
   "Cryptic healing ogham" is the dossier's construction, not an attested genre.

**And the cryptographic core survived the attack**, which under `_roles/VALIDATOR.md` is worth
more than two agreements: expanded twelvefold to 480 cycle-model combinations across three
lexicons, it still yields exactly one English word and zero Irish words. The refuter says so
explicitly. This claim's problem has never been its arithmetic.

**This panel is also the board's first documented case of *independent* convergence.** Its
refuter read the other two verdicts only after running the code and building its own attack,
and recorded that the three reached PARTIAL by three different routes — the criteria, the
evidence chain, and an attempt to kill it. Set beside validator 2's catch on VENONA, where
two validators reached the same correction by near-identical routes and the second flagged
that it should *not* count as confirmation, the pair is the clearest evidence this board has
that the three-validator design is doing the thing it was built to do. **Record the route,
not just the verdict** — now in `STATUS.md`.

## Silos broken

Two `connection` entries, and cross-references written into eight `HANDOVER.md` files.

1. **`2026-09-23-connection-annals-corpus-serves-two-promoted-problems.md`** — the Annals
   session committed a **13,414-row, four-witness CELT entry table** with a blind-validated
   parse-and-changepoint pipeline. That artefact is the *stated core deliverable* of
   `patrician-chronology` and directly bears on `dal-riata-migration-direction`, both promoted
   this pass. It also carries the warning, which is the more valuable half: that session's
   break date moved 70 years and flipped which published date the evidence rejects on **one
   defensible gazetteer decision**, with the two tag sets statistically indistinguishable.
   Both promoted folders turn on the same class of attribution decision.

2. **`2026-09-23-connection-ablation-ceiling-and-label-permutation.md`** — three results
   landing on folders that had not seen them: the Shakespeare ablation onto Junius; Thera's
   information ceiling onto Junius, Byblos, Ennis and Mesha; the Annals label-permutation null
   onto every post-hoc split on the board (Proto-Elamite, Linear A, Voynich).

**One of those is an argument against a cracker's finding, and it is filed as an argument.**
`_roles/ORCHESTRATOR.md` is explicit that the orchestrator does not overrule a cracker. The
Shakespeare ablation shows *centring alone* scores below doing nothing on both arms tested,
including the arm where the full two-step treatment reaches 0.365. Junius could not run the
detrend half, so it ran the half that fails even where the treatment works. **Junius's
readings 1–3 are untouched and its compute route stays closed; its reading 4 should be
withdrawn as evidence.** One cheap untried form of the route survives — the detrend needs the
corpus's *period*, not per-document dates, so the volume-level range string the panel already
carries may suffice. The cracker who next holds Junius decides, not me.

## Promotions

Four, each leaving a `MOVED.md` stub: `patrician-chronology` and
`dal-riata-migration-direction` → `ireland/`; `blood-eagle-kenning` →
`historical-controversies/`; `chinese-gold-bar-cipher` → `ciphers/`. References were grepped
first; all lived in `STATUS.md` (mine) and one dated log entry (historical record, breakage
accepted).

The two Irish promotions have a **better reason than any previous pass has had**: not a
tractability rating, but that something on the board just made them materially cheaper.
`chinese-gold-bar-cipher` goes to a category with no unblocked new work in fifteen days and no
other cipher with a public machine-readable corpus. `blood-eagle-kenning` had been rated
"Good" and passed over five times, which is the failure mode the role file names.

**Two decisions closed rather than deferred**, per the rule that a decision recorded twice as
"deferred again" is a decision not being made:

- **A promotion rule is now stated in `STATUS.md`.** Promote when the proposal is well-formed
  with pre-registered criteria, genuinely unworked, and *either* a category is going cold *or*
  something has just made it materially cheaper. Never on tractability rating alone. Never a
  proposal less than one full cycle old — it has not yet been passed over. A proposal meeting
  the first two conditions and passed over three times is promoted regardless.
- **`templo-mayor-1487-sacrifice-count` and `larry-was-stretched-authorship` are held, once,
  with a commitment rather than a deferral**: both were proposed 09-22, are one cycle old, and
  are recorded to be **promoted next pass if still unworked**. That is a date, not a shrug.

## `PRACTICES.md`

Six results promoted in; five pairs of entries merged; every long entry compressed; the
shift-or-loss rule rewritten after its first out-of-sample success *and* its first failure,
now carrying the four conditions that decide whether it can be used at all — the first of
which is that its two steps are **inseparable** and each alone is worse than doing nothing.

**Honest note against my own curation:** the file still grew, from ~17.5 KB to ~23.5 KB.
Compression did not absorb six load-bearing results in 48 hours. The curation line now tells
the next orchestrator to **displace rather than append**, and to say in that line what was
cut. If nothing can be cut, the right move is to promote the three or four entries a new agent
must read to the top and mark the rest reference — not to let it become a second log.

## Balance

- **`ireland/` is no longer the coldest category.** It took a full session on 09-23 and gained
  two promoted problems; it now holds eight, four of them materially advanced or corpus-ready.
- **`ciphers/` is the cold one now**, fifteen days. Dorabella and CD 286 are genuinely
  archive-blocked, but Debosnys, Kryptos, Beale B3, `VORFYDCGT` and Voynich are not. The
  gold-bar cipher was placed there deliberately as an unblocked start.
- **`historical-controversies/` needs a different kind of attention**: it now holds two
  problems whose stated criteria are answered or partly answered (Thera, Caligula). Closing
  them out is the work, not starting them.
- **Held but not progressing: nothing.** The board's failure mode is no longer
  held-and-idle.

## For the human — three standing decisions

1. The Codex lane has landed no research commit since 2026-09-08. Escalated 09-17, unchanged.
2. **1641 Depositions needs an archive request to TCD that no agent can send.** Measured
   09-23: 6,011 of 6,037 archived `deposition.php` captures are access-denied redirects going
   back to the 2010 crawls. This is not a compute problem and should not be given to a cracker
   as one.
3. **Three claims are `HELD — awaiting human sign-off`** — Mesha line 31 (3 × PARTIAL) and
   VENONA Meredith/Vernon (3 × PARTIAL) on completed panels, and Ennis STINGING
   (2 × PARTIAL, refuter commissioned this pass). **Every verdict returned on this board is
   PARTIAL; there is no PASS anywhere.** None can advance without a human, and no
   orchestrator pass will move them.
