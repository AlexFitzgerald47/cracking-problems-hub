# Orchestrator pass — 2026-10-03

**Previous pass:** 2026-10-02 (`2026-10-02-orchestrator-pass.md`). No evidence was analysed in this
pass. Where this entry states a research fact it is quoting a folder, a session or a validator.

---

## 1. The finding: the board is livelocked, not idle — and the last pass was wrong about it

The 2026-10-02 pass led with *"the board is idle, and that is the only finding that matters this
pass"*, counted about eighteen consecutive missed Breaker firings, and recorded it at the top of
`STATUS.md`, at the top of `board/TOP_INTEREST.md` and in a push to the owner. **That diagnosis was
wrong, and the way it was wrong is the lesson.**

**The Breaker routine is firing normally.** Eight sessions fired between 2026-10-01 and 2026-10-03;
seven did real work. Every one pushed to its own `claude/busy-galileo-*` branch and **opened no pull
request**, so nothing reached `main`. The previous pass read activity off `main`'s history alone,
where a working routine and a dead one are indistinguishable. One `git for-each-ref
--sort=-committerdate refs/remotes/origin` shows the difference immediately. **Every pass should now
read the remote branch list before concluding anything about whether the board is being worked**, and
that instruction is written into `board/TOP_INTEREST.md` rather than only here.

**And all seven worked the same file on the same experiment**: `historical-texts/proto-elamite`, the
M288–N45 block-aware split. The mechanism is the draw itself. It reads the last worked stream and the
coverage debt from `main`, so with nothing landing it re-issued the identical stream B pick with the
identical item 1 to session after session, and the rotation never advanced past stream B either —
every session read "last was stream A (Debosnys, 09-27)". **That is a livelock, and it is a property
of the publication path, not of the sessions**, each of which froze its predictions before running and
did honest work. One (`v5ftaw`) reports three of its own six frozen predictions failed, which is the
most informative single thing in the set.

| | 2026-10-02 pass | corrected 2026-10-03 |
|---|---|---|
| routine | not firing | **firing normally** |
| cost | ~18 missed firings | **7 duplicated sessions** |
| cause | unknown, outside the repo | **work not reaching `main`; the draw can only see `main`** |
| fixable from inside the repo | no | **no — but diagnosable, and the damage is recoverable** |

The honest limit of the previous observation stands — a session cannot see the routine's logs — but it
could have seen the branches. **The diagnosis was limited by where it looked, not by what it could
know**, which is a different and more correctable failure.

## 2. The seven sessions are landed, and nothing was adjudicated

All seven are on `main` (commit `fee05e6`), each in its own
`attempts/<date>-<name>--<session>/` directory holding that session's `PREDICTIONS.md`, `RESULTS.md`,
code and results exactly as committed, plus `HANDOVER-as-written.md` and
`PROGRESS-entry-as-written.md`. Their eight `board/log/` craft entries land under their own filenames.
About 85,000 lines of research that the board could not see.

**Why namespaced rather than merged.** Three of the seven wrote into the *same*
`attempts/2026-10-01-block-aware-split/` path, and all seven rewrote `HANDOVER.md` and `PROGRESS.md`.
Seven divergent versions of one file cannot be merged without deciding between them, and **that
decision is a Breaker's, not Overwatch's** — the role is explicit that the orchestrator's authority is
over the board's shape, not over anyone's conclusions. So `PROGRESS.md` and every pre-existing section
of `HANDOVER.md` are untouched: the folder still reads as of 2026-09-17 below the new note, and the
seven accounts sit in their own directories until a Breaker reconciles them.

**What they agree on, and what they do not.** All seven: M288–N45 is confirmed against the face
confound, and the 2026-09-17 bucket-0 holdout's p-floor of 0.12 was a power failure rather than a
negative result. That supersedes the folder's standing "untestable, not refuted", and the `STATUS.md`
row says so. On the downstream constraint-set re-tiering they give **six different answers**: 8 → 26
pairs; four of eight demoted; a re-count on a new multiplicity basis; "a sample, not a set"; a
co-numeral control demoting M263–N01 and refuting M297–N24; a 24-pair frozen screen. Overwatch has not
chosen, and the next move says not to pick the most recent or average them.

**The note's step 2 is the part that matters.** Seven agreeing runs is *not* seven replications — see
§5(a). They shared a corpus, a handover item and an instruction, so their errors are correlated by
construction. The draw now reads: **"Reconcile the seven parallel runs of the M288–N45 block-aware
split, and do not run an eighth."**

## 3. PR queue, claims and draw defects

| check | result |
|---|---|
| open pull requests | **none** — the Codex queue is clear; nothing merged or commented |
| `board/active/` | only `.gitkeep` — **sixth consecutive clean claim pass** |
| stale claims to release | **none.** The one session that crashed straight after claiming (`4ptru6`) left its claim file on its own branch, where it is harmless and was not landed |
| `npm run draw` | runs; names a pick with a written next move |
| `PICK-UP` marks | none |
| `NO NEXT MOVE` marks | **none** |
| panels owed to Overwatch | **none, for the first time since the queue was opened** |
| solve-claims short of three verdicts | **none** |

`discovered/` audited again: thirteen live packs, every one with a suggested category and a startable
next move under a heading the draw can read. The two expected exceptions are unchanged — `_manifest/`
is a finder directory, and `short-cipher-validation-bound` is the methodological asset settled
permanently on 2026-09-06.

**No promotions out of `discovered/`, and the reason is now different and better.** The standing draw
order's trigger is a category going cold — no unblocked new work for ten days. The 2026-10-02 pass
found every category cold and correctly declined to promote, because the cause was a board nothing was
reading. **This pass can say something stronger: the categories were never cold.** Seven sessions ran
in three days; the work was invisible, not absent. The trigger was never actually met, so there is
nothing to draw from the queue, and the standing order in `STATUS.md` stands unchanged and
un-relitigated. **Promotion is not the board's problem; publication is.**

## 4. Both panels closed — and the 10-02 pass's own lesson repeated inside them

**Byblos syllabary: 3 × PARTIAL.** `2026-10-03-panel-outcome-byblos-syllabary.md`. Source integrity
and transcriptions verified clean against an independent published witness — validator 2 names that as
the part it expected to break and could not. Criteria 1 and 4 **not met**, and criterion 4's only
artefact **inverts**: it is anchored on U+E402, which the GEAS font that ships the signs names
*"kurzer Worttrenner oben"*, a word divider, and which behaves like one at 13 tokens with zero
line-edge occurrences. Criterion 2 is met by prior art for Woudhuizen/Best only, with Garbini (2009) a
live rival the folder does not name. **Validators 2 and 3 dissent** on whether the E416/E4AF split is
published prior art or adjudicated in neither direction; both agree it is not a Hub novelty, and the
dissent is carried into the folder with an instruction not to resolve it by convenience.

**Linear A: 1 × PARTIAL, 2 × FAIL — the claim did not pass.**
`2026-10-03-panel-outcome-linear-a.md`. The refuter's central finding is a prior-art route nobody had
checked: **Younger's GORILA-based `commentary/HT*.html` files ship in the same repository as the
`LinearAInscriptions.js` the folder uses, the claimant's `analysis/` already cites twelve of them, and
16 of 16 checked frontier results are verbatim inside them** — including the dossier's own stated main
new result. Beyond that: the eight-node architecture is a template (73.7 % of size-matched random
ten-tablet subsets score 8/8); "integrated … linking" fails as a graph (5 edges of 45, five
components, four of ten tablets isolated); the fixed 1:2 manpower ratio is falsified at 2.48 by HT97a,
the only second data point the corpus permits; and there is no modulus-6 footprint anywhere.

**What survived is recorded as carefully as what failed**, because the refuter reported its failed
refutations instead of burying them: the dossier is not cherry-picked, metadata is 10/10, KU-RO
survives everything, `KI-RO 30` on HT34 is the claimant's reading and is right, HT88's "+33" is a
sectioning artefact rather than an error, HT85a's six-run at simulated p = 0.0004 could not be broken,
and the HT 117a full-width ruling is independently confirmed from the GORILA facsimile. **The
defensible restatement, named by validator 2 and endorsed by validator 3** — *the Hub independently
replicated a received structural reading and correctly diagnosed a parser-direction error in an
external negative control* — is now item 1 of the folder's next move, because leaving the rejected
2026-09-08 framing as the first thing a session reads is how a failed claim gets inherited as settled.

**Both claims are `HELD — awaiting human sign-off`, published nowhere as solved.** Byblos joins the
3 × PARTIAL set; **Linear A does not, and must not** — see §7.

**The 10-02 pass named *an unposted verdict is worse than an unconvened panel*, and it then happened
inside the panel that pass convened.** Byblos's three verdicts landed on 10-02. Linear A's refuter
committed its entire attack suite — eleven `attack_*.py` scripts, vendored witnesses, a 48 KB
`out.txt`, and a `README.md` naming the verdict path — and **died before writing the verdict file**,
leaving the panel owed to Overwatch for a further day over one missing file while finished work sat
unreadable. A validator was convened on 2026-10-03 to close it, instructed to run and go beyond the
crashed suite rather than adopt it. It reproduces (exit 0; 29 differing lines, all sort ties among
equal-frequency items, no numeric result changed, nulls seeded), `out.txt` was restored byte-for-byte,
and none of its conclusions were taken on its word. **That is how an inherited suite should be
handled, and the rule that prevents the next one is now in `PRACTICES.md`: write the file that reports
your result, with `verdict: PENDING`, before you run the thing that might kill the session.**

## 5. Silos broken — two connections, both written into handovers

**(a) A shared source and a shared trigger make agreement worthless as replication.**
`2026-10-03-connection-a-shared-trigger-is-not-an-independent-replication.md`. Measured by Linear A's
validator 2 against `dbourdeau/cyphersolver`: corpus overlap effectively total, source overlap
near-total, and on the flagship KI-RO result **test dependence total** — both projects pushed to the
same reading by the *same* third-party negative control, which that project's own notes label
"replication, not discovery". The transferable artifact is its **`external_overlap_map.csv`**: one row
per proposition → *published elsewhere* / *Hub result* / *cannot assess*, with a reason per row so it
can be attacked. It is now the live question on Proto-Elamite, where seven runs agreed from one
instruction, and it is carried into stream briefs A, B and C with the folders that need it named
(Voynich, Beale, Kryptos, Rohonc, Phaistos, the gold bars, and the two archival packs).

**(b) Match the permutation on the confound, then test the classes you did not hypothesise.**
`2026-10-03-connection-match-the-null-on-the-confound-and-test-the-other-classes.md`. Linear A's
Scribe-9 cohesion was p < 0.01 under a free label permutation, **p = 0.12–0.57** permuted within
strata of tablet size (the scribe label is confounded with it), and **present for Scribe 6 too**. It
was the absence of the across-class comparison, not the p-value, that sank the criterion — and that
half needs no new data, because you already hold the other classes. Carried into **five** handovers
with a folder-specific reason each: `shakespeare-authorship` (run the discriminator against the other
dramatists of the same decade), `larry-was-stretched-authorship` (length confounded with source
collection), `historia-augusta-authorship` (lives differ systematically in length and subject period),
`early-irish-annals-reliability` (early strata terse, late strata discursive), `bmh-mspc-divergence`
(collection label confounded with when a statement was taken, by whom and at what length). Folded into
the existing *Permute the label before believing a post-hoc split* rule rather than added beside it,
and explicitly distinguished from the 2026-10-02 length-calibration rule: that one is about comparing
documents of different lengths, this one bites when every unit is the same length.

**And the 2026-10-02 pass's deferred carry is discharged.** That pass deliberately withheld the
length-matched-null connection from Byblos's and Linear A's handovers while their panels were live, and
left a specific instruction for this pass to land it. **Both are now carried**, with the Byblos version
tied to its criterion-1 power analysis and the Linear A version tied to the architecture-level null.
The pending-carry note is removed from the stream B brief.

## 6. `PRACTICES.md`: four rules added, one family split out

Four added. *Agreement is evidence only if you could have disagreed* — promoted straight into **entry
6 of Start here**, because it is the newest way this board has gone wrong at scale. The
confound-matched permutation, **folded** into the existing label-permutation rule. *Charge the
transcription-variant budget before counting anchors*, from the Byblos refuter — in a corpus with
multiple published readings per witness, "the two names share a sign" is a statement about which
reading was chosen, with validator 2's rider that a variant selection which is the editor's own
published choice is attributable to them. And two operations rules from this pass's own failures:
write the result file before the run that might kill the session, and **land your work on `main`, or
the draw will send the next session to repeat it.**

The additions took the file past the 32 KB threshold again, so **the archival/identity family — the
candidate the previous curator named as next — is split out to `board/PRACTICES-ARCHIVAL.md`** rather
than deferred a third time, per the standing rule that a decision recorded twice as deferred is a
decision being failed. Moved: role separation before identity constraint, the OBSERVED / INFERRED /
MISSING ledger, the proximity trap with row-by-row adjudication, and the second-scan replicate.
Flagged **not optional for streams C and D and for the stream A archival packs**, and listed in
*Start here*. **28.5 KB → 31.6 KB plus a 4.8 KB annexe; four rules added, four moved, none lost.** The
file is still above where the last curator wanted it; the remaining split candidate is the
corpus-and-pipeline-audit family, and a curator who adds two more rules should take it.

## 7. The mechanism gap, recorded rather than patched

`npm run build` now warns that `HELD_PARTIAL` disagrees with `STATUS.md` over
`historical-texts/linear-a`. The check compares the curated set in `scripts/build.mjs` against every
row matching `\bHELD\b`, which **assumes every held claim is 3 × PARTIAL**. Linear A is held at
1 × PARTIAL and 2 × FAIL, so the assumption is now false for the first time.

**Adding Linear A to `HELD_PARTIAL` would silence the warning by publishing `3×PARTIAL` as its verdict
and bumping its score — it would falsify a validator panel's result, and an orchestrator may not do
that.** Byblos *was* added, correctly, being 3 × PARTIAL. The real fix is a per-problem verdict label
instead of one membership set, in the owner's `scripts/build.mjs`, so it goes on the human-decision
list exactly as the `stageOf` / `cypro-minoan` gap did on 2026-10-02. **The warning is correct and
should stay visible; the next orchestrator should not "fix" it by silencing it**, which is why this
section exists.

## 8. What the board looks like leaving this pass

- **No file is owed to Overwatch and no solve-claim is short of verdicts** — first time since the
  validation queue was opened. Validation has stopped being the bottleneck.
- **The bottleneck is now publication.** One human decision: the Breaker routine must
  `git pull --rebase origin main` and push to `main` as the Orchestrator routine does, or open a pull
  request. Until then every firing re-runs the previous firing's work.
- **Five claims held, none published as solved.** Byblos joins Ennis, Mesha line 31, VENONA
  BROWN/BRAUN and the gold bars at 3 × PARTIAL; Linear A is held having not passed. `STATUS.md` now
  says what each of the four older ones is waiting for, per the draw rule — and all four wait on a
  *physical or archival* step rather than another pass of reasoning, none on Overwatch and none on a
  new panel. They trip the 14-day pick-up rule between **2026-10-08 and 2026-10-09**.
- **The next pick is the Proto-Elamite reconciliation**, and after it the four held files are the
  most valuable firings on the board.
