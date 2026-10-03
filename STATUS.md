# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-10-03, **orchestrator overwatch pass** (the board is livelocked, not idle: seven Breaker sessions duplicated one experiment on unmerged branches, all now landed; Byblos panel closed at 3 × PARTIAL; two connections carried; `PRACTICES.md` split again). Full report: `board/log/2026-10-03-orchestrator-pass.md`. Previous: 2026-10-02, **orchestrator overwatch pass** (the board has not been worked since 2026-09-27; both outstanding validation panels convened; two folders added that were missing from this dashboard; `PRACTICES.md` curated and split). Full report: `board/log/2026-10-02-orchestrator-pass.md`. Previous: 2026-09-27, **external-claim triage** (Beale B3 and Rohonc dispositions corrected; recent Dorabella/Voynich solve claims screened but not adopted) — `board/log/2026-09-27-external-claim-triage.md`.

## Operating design — 2026-09-13

[Adaptive Research Practice](board/IMPROVEMENT.md) is installed by user direction:
bold leaps, decisive checks, compact handovers and proportionate validation.
ARP-001 is **retired in its opt-in form as of 2026-09-24** — zero activations in eleven days
while nine sessions each recorded a deliberate decision to decline it. The mechanism failed, not
the amendment, whose content remains **unevaluated**: no activated run ever occurred, so the
retirement is not a negative result about it and must not be cited as one. Evaluating it would
need a default-on instrumented run and a change to the external stored prompts, which is on the
human-decision list. See `board/IMPROVEMENT.md`, 2026-09-24.
This policy update does not change the research dispositions below or restart routines.

## Operating framework — 2026-09-27: the draw

By the owner's direction, Breaker work is now **drawn, not chosen**. Four streams — **A**
Ciphers, **B** Undeciphered texts, **C** Controversies, **D** Ireland — take turns: each
Breaker firing works the stream after the last Breaker session's, and within it the
unclaimed file with the highest coverage debt (days since a working session × stage
weight). A held claim idle for more than 14 days jumps to the front of its stream. No
session releases a claim without a next move in `HANDOVER.md`. **`discovered/` is live**:
its packs are drawn and claimable where they sit. Run `npm run draw` to see the pick; the
rules are in `_roles/README.md`, the standing briefs in `board/streams/`, and the live site
has a framework page. The *cracker* role is renamed **Breaker**; dated records keep the
old word. Log: `board/log/2026-09-27-the-draw.md`.

## Board state

**2026-10-03: the board is NOT idle — it is livelocked, and the 2026-10-02 finding on this line was
wrong.** That pass recorded "the board is idle … it is simply not being drawn from", and read eighteen
missed firings off `main`. **The Breaker routine is firing normally.** Eight sessions fired between
2026-10-01 and 2026-10-03; seven did real work. Every one of them pushed to its own
`claude/busy-galileo-*` branch and **opened no pull request**, so nothing reached `main` and from
`main` a working routine is indistinguishable from a dead one. The earlier diagnosis was made from
`main`'s history alone; the branch list is where the routine is visible.

**All seven worked the same problem, on the same experiment.** `historical-texts/proto-elamite`, the
M288–N45 block-aware split — because the draw reads the last worked stream and coverage debt from
`main` alone, so with nothing landing it handed session after session the identical stream B pick with
the identical item 1 as its next move. The rotation never advanced either: each session read "last was
stream A (Debosnys, 09-27)" and took stream B. **That is the livelock, and it is a property of the
publication path, not of the sessions** — each froze its predictions before running and did honest
work, and one (`v5ftaw`) reports three of its own six frozen predictions failed.

**All seven are now landed on `main`** (commit `fee05e6`), each in its own namespaced
`attempts/<date>-<name>--<session>/` directory with its `PREDICTIONS.md`, `RESULTS.md`, code, results,
`HANDOVER-as-written.md` and `PROGRESS-entry-as-written.md` preserved verbatim, plus their eight
`board/log/` craft entries under their own filenames. **Nothing was merged, ranked or adjudicated by
Overwatch.** The seven agree that M288–N45 is confirmed against the face confound and that the
2026-09-17 bucket-0 holdout's p-floor of 0.12 was a power failure rather than a negative result; they
give **six different answers** on the downstream constraint-set re-tiering (8 → 26 pairs; four of
eight demoted; a re-count on a new multiplicity basis; "a sample, not a set"; a co-numeral control
demoting M263–N01 and refuting M297–N24; a 24-pair frozen screen). Choosing between those is a
Breaker's call. The folder's next move is now **reconcile the seven, and do not run an eighth** — with
step 2 pricing the seven-way agreement for test dependence, because they shared a corpus, a handover
item and an instruction, and their errors are correlated by construction.

**This is the one thing on this dashboard that needs a human.** The Breaker routine pushes to a
branch and nothing merges it. Either it should `git pull --rebase origin main` and push to `main` as
the Orchestrator routine does, or it should open a pull request — and until one of those is true,
every firing re-runs the previous firing's work. Recorded at the top of `board/TOP_INTEREST.md` too.
**The corrected count of genuinely lost cycles is seven duplicated sessions, not eighteen missing
ones.**

**What was and was not blocking, checked again this pass.** `board/active/` holds only its `.gitkeep`
— sixth consecutive clean claim pass, and no stale claim to clear (the one session that crashed
straight after claiming, `4ptru6`, left its claim on its own branch where it is harmless). GitHub has
**no open pull request**, so the Codex queue is clear. The draw runs, names a pick with a written next
move, and marks **no** file `PICK-UP` and **no** file `NO NEXT MOVE`.

**Validation: Byblos is closed, Linear A is closing.** Both had been panel-pending since
**2026-09-17**; both panels were convened on 2026-10-02, three validators each with the third assigned
to refute, judged against the criteria already written in each `PROBLEM.md` and reproducing from the
raw corpora rather than reviewing the writeups.

**Byblos syllabary — panel complete at 3 × PARTIAL, `HELD — awaiting human sign-off`, drawable
again.** Outcome in `board/log/2026-10-03-panel-outcome-byblos-syllabary.md`; verdicts in
`board/log/2026-10-02-validation-byblos-syllabary-v{1,2,3-refuter}.md`. Source integrity and the
transcriptions verified clean against an independent published witness. Criteria 1 and 4 **not met** —
criterion 4's only artefact **inverts**, being anchored on U+E402, which the GEAS font that ships the
signs names a word divider and which behaves like one (13 tokens, zero at a line edge). Criterion 2 is
met by prior art for Woudhuizen/Best only, with **Garbini (2009)** a live rival the folder does not
name; criterion 3 is met as argument but unexecuted. **Validators 2 and 3 dissent** on whether the
E416/E4AF split is published prior art or adjudicated in neither direction — both agree it is not a
Hub novelty, and a future session must not resolve it by picking the convenient reading. Not a solve
and published nowhere as one.

**And the 2026-10-02 pass's own lesson repeated itself inside the panel it convened.** That pass named
*an unposted verdict is worse than an unconvened panel* — the work is paid for and invisible. Linear
A's refuter then committed a complete attack suite (eleven `attack_*.py` scripts, vendored witnesses,
a 48 KB `out.txt`, and a `README.md` naming the verdict path) and **died before writing the verdict
file**, leaving the panel owed to Overwatch over one missing file. A validator was convened on
2026-10-03 to close it, told to run and go beyond the crashed session's suite rather than adopt it.
The rule now in `PRACTICES.md`: **write the file that reports your result, with
`verdict: PENDING`, before you run the thing that might kill the session.**

**Two folders existed on disk and not on this dashboard, and that is a dashboard bug of the exact kind
the draw was built to prevent.** `historical-controversies/venona-baron/` and
`discovered/historia-augusta-authorship/` both landed in the **2026-09-27 reconciliation** and were
never entered in the tables below. `venona-baron` has in fact been drawable and ranks 8th in stream C;
`historia-augusta-authorship` ranks just below the cut in the same stream. Both now have rows. The
lesson is narrow and worth keeping: **a reconciliation commit that imports folders must also add their
rows, because the draw will happily rank a problem this file has never heard of.**

**One override is now standing, for a mechanism gap rather than a disagreement.**
`discovered/cypro-minoan/` has been recorded since 2026-09-25 as evidence-blocked until its corpus is
digitised — a standing item like the 1641 Depositions archive request, not a Breaker task — yet the
draw ranked it 5th in stream B as `unworked`, because `stageOf` can only read `blocked` from the table's
*status* column and a `discovered/` row uses that column for the suggested category. Its row now says
`historical-texts — evidence-blocked`, which ranks it `blocked` (weight 0.5, never leads) while leaving
it in stream B. The underlying gap is in `scripts/derive.mjs`, which is the owner's file, so it is on
the human-decision list rather than patched here.

**Held claims trip the pick-up rule from 2026-10-08, and one more file is now held.** The four HELD
3 × PARTIAL files (Ennis, Mesha line 31, VENONA BROWN/BRAUN, Chinese gold bars) are idle 8–9 days and
cross the 14-day threshold between **2026-10-08 and 2026-10-09**, at which point they jump to the
front of their streams — the mechanism working as designed. **Byblos syllabary joins them as held at
3 × PARTIAL from 2026-10-03**, but its validation artifacts landed 2026-10-02, so it ranks as
just-worked and will not trip pick-up until late October. Nothing is currently marked `PICK-UP`.
**What is waiting on what:** all four of the older held claims are waiting on a *physical or archival*
check rather than another pass of reasoning — Ennis on the December 2023 photogrammetry/RTI, Mesha on
a blind stroke comparison against genuine stone and squeeze, VENONA on constraint-ledger Q2 and Q3
(two small enumerable populations the cables name and nobody has run), and the gold bars on the
simplified-character check against the IACR photographs plus the cursive script on six of the fifteen
faces that nobody here or elsewhere has looked at. None of the four is blocked on Overwatch, and none
needs a new panel; each needs one session willing to do the unglamorous evidence step. With the
livelock fixed these are the four files most worth a firing after the Proto-Elamite reconciliation.

**What the board produced this pass was method, not evidence.** Two cross-silo carries were posted:
the Blitz length-matched-null and doublet rules, written into **seven** `HANDOVER.md` files and a new
annexe (`board/log/2026-10-02-connection-length-matched-nulls-and-the-doublet-trap.md`), and the
Crelly/Ormond–Anglesey archival lane
(`board/log/2026-10-02-connection-the-two-irish-archival-cipher-packs-are-one-lane.md`).
`board/PRACTICES.md` was curated for the first time since 2026-09-25 — four rules added from the
2026-09-27 sessions, which had never been distilled — and the ciphertext-statistics family split out to
**`board/PRACTICES-CIPHERTEXT.md`**, taking the main file from 29.5 KB to 27.3 KB with nothing lost.

*Everything from here down is the **2026-09-27** text unless a row says otherwise. It was accurate
when written. Where it says the board is delivering, read the paragraph above instead.*


**2026-09-27 post-reconciliation check.** The canonical checkout equalled `origin/main` at
`cacd6f6`; `board/active/` was empty and GitHub had no open pull request. The audit counted 48
problem packs. Raw commit touches put Linear A first (29), followed by Ennis (22), VENONA
BROWN/BRAUN (21), Shakespeare (18) and Voynich (15); file/attempt depth instead highlights
Junius, Shakespeare, the Annals and Voynich. These are measures of attention, not merit or
closeness to solution.

There is still **no internally validated solve and no PASS verdict**. One proposed target,
Ormonde–Maltravers, was correctly withdrawn after an external solution was found. The closest
internal candidates remain the four HELD 3 × PARTIAL claims (Ennis, Mesha, VENONA, gold bars),
while Linear A and Byblos still await their first panels. Several projects nevertheless answered
their narrower success criteria: Templo Mayor returned a notation-artifact verdict with two
primary-source checks outstanding; Thera established an information bound; blood eagle measured
why the surviving evidence cannot decide the rite question; and Caligula strongly favours the
literal reading but still lacks the two decisive modern articles. Full evidence and the refreshed
draw order are in `board/log/2026-09-27-orchestrator-pass.md` and `board/TOP_INTEREST.md`.

*Rewritten in full by the 2026-09-25 orchestrator pass. The section standing here until now was
the **2026-09-23** pass's text: it still said "PR queue empty, third consecutive pass", "Codex
silent fifteen days" and "four proposals promoted", all of which had moved on twice. The 09-24
pass corrected individual rows and left this section alone, which is how a dashboard rots from the
top. Anything below is current as of this pass or it is a bug.*

**Delivery is not the problem and has not been for a week.** Four distinct research sessions have
landed since the last orchestrator pass on 09-24 at 10:47 — Templo Mayor (09-24), "Larry Was
Stretched" (09-24), Phaistos Disc (09-25, first working session) and the Chinese gold-bar panel
repair (09-25) — each with committed code, data, a `FREEZE.md` and a handover. Two of the four
reported a **frozen prediction refuted by their own evidence** and said so in their headline, which
is the disposition this board most wants and the hardest one to fake.

**What the board produces faster than it distributes is method.** Both 09-25 sessions produced
results whose value is mostly in other folders: an exact-tail enumerator and an inherited-structure
null from the gold bars, and three ways a comparison corpus lies from Phaistos. Carried this pass
to **nine** `HANDOVER.md` files —
`board/log/2026-09-25-connection-exact-tails-inherited-structure-and-audited-comparanda.md`.

**Claim hygiene: good, and nothing needed clearing — fourth consecutive pass.** `board/active/`
holds only its `.gitkeep`. Every claim opened since 09-17 has been released by its own session in
the commit that landed the work. The folder rule (`git log -1 -- <problem folder>`, never the claim
file's date) did not have to fire. This failure mode looks genuinely solved rather than quiet: the
discipline is in `PRACTICES.md` and sessions are following it.

**PR queue: empty. Sixth consecutive pass.** Nothing to review, merge or reject. The externally-run
Codex lane has now landed no research commit since **2026-09-08 — seventeen days** — and is not
contributing by the pull-request route either. Standing item for the human, escalated 09-17,
unchanged. It remains the only unexplained silence on the board.

**The gold-bar claim was repaired against its own panel, and this is the first time that loop has
closed here.** The 09-24 panel returned 3 × PARTIAL with six named repair items; a session took
four of them within 24 hours. The disputed exact tail is settled at **1.7020973493e-12** by two
independent exact-integer algorithms — validators 1 and 2 were right and the refuter's counter-figure
was the more optimistic of the two. The corpus was **re-read off the photographs** and is 261
letters, not 263, with a line inventory of **88 instances against IACR's 44** and three faces nobody
had ever transcribed. The frozen image prediction from 09-24 **failed**, and the session led with
that. Pillar 3 is repaired rather than withdrawn: the refuter was factually right that a bar face is
itself balanced, and conditioning on the inventory shows that balance is **100 % inherited**
(p = 0.598, dead centre). **The claim stays `HELD — awaiting human sign-off` at 3 × PARTIAL.**
Criteria 1 and 3 remain unmet; repair items 5 and 6 are untouched and cheap. Nothing is published
as solved.

**Three proposals promoted out of `discovered/`,** each leaving a `MOVED.md` stub and each carrying
into its `HANDOVER.md` the specific method that now makes it cheaper, not just a rating:
**`blitz-ciphers` → `ciphers/`**, because its criterion 1 asks for exactly the authenticity
benchmark the gold-bar sessions just built and it is the only unworked cipher on the board whose
whole question is "is this even a cipher"; **`meroitic-language` → `historical-texts/`**, on the
board's own "passed over three times" clause — it has been well-formed and unworked since 09-04 and
passed over on every pass since — and it fills the board's total absence of an African script;
**`black-death-mortality-figure` → `historical-controversies/`**, because blood eagle and Templo
Mayor have now completed the citation-chain instrument its criterion 1 describes, and Templo Mayor
supplies the third hypothesis its proposal does not list (a big round number may be a *notation*
artefact rather than a count or an embellishment). **The residual `discovered/` queue is closed as a
recurring question this pass rather than deferred again** — see the standing draw order under
*Recently Proposed*.

**`board/PRACTICES.md` gained three rules without being cut.** The specialist five-rule stylometry
and confound family moved to **`board/PRACTICES-STYLOMETRY.md`**, which is the structural move the
previous curator's "at 30 KB, cut a rule" instruction needed: those rules are among the
best-earned here and apply to four folders, not forty. 4.4 KB left the file every new agent reads
and no craft was lost.

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Debosnys Ciphers | `ciphers/debosnys-ciphers/` | **PARKED 2026-09-27 — shared signature key retired; evidence-blocked by the owner's choice**; unclaimed | A held-out session froze its predictions and then retired the atom-level transition key (`X=EC`, `DOT=OS`, …; Branch A or B) on two frozen falsifiers — the signature's `NU` glyph is the poem's `TCURL` (p = 0.0027). **Read `attempts/2026-09-27-heldout-key-test/RESULTS.md`, then `evidence-acquisition.md`.** The next move needs scans from the Brewster Memorial Library (Adirondack History Museum); an unsent draft request waits for the human. Two archive-free tasks remain: the copied-source sweep of 1878–83 magazine and newspaper verse (freeze the fingerprint and its null first), and checking whether Farnsworth's plates beat the Commons resolution. |
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open — corrected and redirected | September 6 audit withdrew the claim that the golden cell controls physical section: illustration class is not quire, and A blocks repeat one folio. Plant-label fit failed held-out (117/120). Next: frozen Tankalusha/Alfonsine degree-list extraction; fit Taurus, predict Gemini/Cancer. See current `HANDOVER.md`. |
| Kryptos (remaining parts) | `ciphers/kryptos/` | **Restated 2026-09-04** – K4 open as a *method* problem | Plaintext recovered from Sanborn's Smithsonian papers in 2025 and confirmed, but not deciphered and sealed for 50 years. Pure transposition and the Vigenère family eliminated from the public cribs; simple-transposition composites show no signal above chance. See `attempts/2026-09-04-crib-constraints/` |
| Beale Ciphers | `ciphers/beale-ciphers/` | **Review-ready 2026-09-27** – B1 effectively settled; B3 external no-message case not yet reproduced here | The Hub established only that B1's alphabetical runs are non-random (p < 10⁻⁵) and that B3 lacks that specific signature (p = 0.85). A 2026 peer-reviewed *Cryptologia* study now reports a reproducible broader result favouring deliberate construction for both B1 and B3 after testing the principal composite-cipher families. This is strong external evidence, **not an adopted Hub closure**. Next: reproduce its archived pipeline against the two disputed B3 tokens, then decide whether B3 should move from open decipherment to probable constructed/no-message. See `HANDOVER.md` and `board/log/2026-09-27-external-claim-triage.md` |
| IRA `VORFYDCGT`, 25 Oct 1923 | `ciphers/ira-vorfydcgt-1923/` | Open – **promoted 2026-09-06**; first pass complete, unclaimed | Nine-letter token in an IRA Director of Intelligence memo, NLI MS 10,973/15/24: *"Can any of 100's methods be used now that no VORFYDCGT?"*. The documented 1923 key `GVZKLG` is falsified against a reproduced control. Only four of 13,124 nine-letter dictionary words are reachable under **any** repeated six-letter key, and none fits the sentence. Contextual reconstruction — identifying `100` — now carries more information than the ciphertext |
| British RIC / military cyphers (Kennedy CD 286) | `ciphers/british-cyphers-cd286/` | Open – **promoted 2026-09-06**; archive-blocked, unclaimed | BMH Contemporary Documents Group 2, June–Sept 1920 RIC/military telegrams the Bureau and NLI could not decode in the 1950s. Working implementation of the documented RIC paired-alphabet keyword cipher with tests; message-family ledger in `solution-status.md`. **Blocked on scans**, not cryptanalysis. Catalogue discrepancy live: CD 286 (Military Archives) vs CD 280 (Kerry Library) |
| Chinese gold bar cryptograms (1933) | `ciphers/chinese-gold-bar-cipher/` | **Worked again 2026-09-25 — panel repair items 1–4 closed; corpus corrected from the photographs. Solve-claim still HELD at 3 × PARTIAL**; unclaimed | **Read `attempts/2026-09-25-tail-images-mechanism/RESULTS.md` first; it corrects the 09-24 attempt in three places.** (1) **The disputed exact tail is settled: 1.7020973493e-12**, by two independent exact-integer algorithms plus a third agreeing. Validators 1 and 2 were right; the published 9.3e-13 is 1.83× optimistic and the refuter's 8.28e-13 is 2.06× optimistic. Quote no other number. (2) **The corpus is 261 letters, not 263.** All fifteen IACR photographs were read; both strings disputed between IACR and Pelling are **13 glyphs** on three stampings each — `UGMNCBXCFLDEY` (both published readings wrong) and `KOWVRSRWTMLDH` (Pelling right). New headline: chi2 = 1.4904, **exact P = 1.2231e-11**, 19/26 letters at exactly ten. The balance survives at a cost of 7.2×. (3) **The 09-24 session's frozen image prediction is refuted by the metal** — the correction moves B and K *away* from ten and lands on exactly the chi2 = 1.490 / 19-of-26 it predicted against. (4) **The line inventory doubles**: 88 instances across seven faces, 1,441 stamped letters, against IACR's 44; faces **7.2, 11.1 and 13.1 had never been transcribed by anyone**. No new string — the repertoire is closed at 16 across 88 stampings. **"18 bar faces public" was wrong: 15 images**, six of them cursive script only, three detail close-ups. (5) **Pillar 3 is repaired rather than withdrawn, and this is the session's substantive result.** The refuter was right that a bar face is itself balanced (5.1 at P = 7.4e-6) — but conditioning on the inventory and the face's own layout, **every face sits inside the null**, 5.1 at p = 0.598 dead centre and the whole physical corpus at p = 0.148. Face balance is 100 % inherited. The defensible form is **"the balance has zero residual at every physical level tested"**. (6) **The depleting-supply alternative is dead as stated**: a uniform urn flat enough needs c ≲ 12, a letter used 13 times needs c ≥ 13 — **zero hits in 800,000 draws at every feasible urn size**. Non-uniform supplies and balanced code tables fit trivially and are all *someone balanced an inventory*, so the three composition-level mechanisms are **not separated by this corpus** — now a result, not an omission. (7) Two of this session's own frozen predictions failed and are reported as failures: faces are flatter than predicted, and validator 2's max-distinct-per-string lead **strengthened** to p = 0.0056 rather than weakening. That lead is the only live signal; the deficit is entirely in the five strings of 19+ letters (z = −2.50), which runs *against* a bag of tiles. **Repair items 5 and 6 remain untouched and cheap.** Largest unexamined evidence on the problem: **six of the fifteen faces are entirely the unidentified cursive script and nobody on this board has looked at it.** |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | **CLOSED – BLOCKED** (2026-09-04; parked, not abandoned) | Blocked on **source resolution, not cryptanalysis**: the facsimile every published reading derives from is 433×161 px (~14.6 px per glyph). Four independent readings disagree on an identical fixed set of 36 of 87 positions. September 2026 repositories claiming a definitive musical solution do not remove that block: one verification suite asserts consequences of its chosen G-major mapping, while the underlying 2025 musical study explicitly disclaims a unique solution. Reopen on a 300 dpi scan, or on blind adjudication of those 36 positions |
| Blitz Ciphers | `ciphers/blitz-ciphers/` | **Worked 2026-09-27 — measured result, not a verdict** | First substantive session ran criterion 1 in full. Against a within-line unigram-shuffle null the released pages carry real sub-unigram structure (bigram-IC z = +5.84 at n = 470, p = 5e-5) but **far less than genuine substitution ciphertext of the same length**: **0 of 402** length-matched Copiale/Borg blocks fall as low, at **power 1.000**. **Replicated on a frozen holdout** — Pelling's original 2011-key transcription of *other* pages, z = +4.94, again 0/402. Not a hoax verdict: the innocent explanation is priced at ~14–25 % of glyphs mistranscribed, or a wholesale doubling of the alphabet, and heavy nulls, a polyalphabetic scheme and a non-prose plaintext all survive. **Exactly one transcription of pages 7–8 exists** (the benchmark copy is byte-identical to Pelling's blog text), so the decisive next artefact is an independent second transcription; the cheap next test is the pairing test in `HANDOVER.md`. `attempts/2026-09-27-authenticity-internal-nulls/RESULTS.md` |

**`ciphers/ira-vorfydcgt-1923/` and `ciphers/british-cyphers-cd286/` are one lane.** Same
period, same intelligence office, same cipher family, same prior-solution check
(Mahon & Gillogly, *Decoding the IRA*), same bottleneck — archival images. A session that
resolves the CD 286 / CD 280 discrepancy and orders Kennedy Group 2 unblocks both. The
`100` cross-link runs in one direction only; see this pass's log entry.

### Historical Texts
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Proto-Elamite | `historical-texts/proto-elamite/` | **Open — seven parallel Breaker sessions 2026-10-01→10-03, all landed 2026-10-03, awaiting reconciliation**; unclaimed | **Read the orchestrator note at the top of `HANDOVER.md` before anything else, and do not run an eighth block-aware split.** Seven sessions worked this folder on the same drawn next move while none of their work reached `main`; all seven are landed under namespaced `attempts/<date>-<name>--<session>/` directories with their predictions, results, code and own handover text preserved verbatim. **They agree M288–N45 is confirmed against the face confound** and that the 2026-09-17 bucket-0 holdout's p-floor of 0.12 was a power failure rather than a negative result — so this row's previous "M288–N45 is untestable, not refuted" is superseded by seven runs, none of them yet reconciled. **They give six different answers on the downstream constraint-set re-tiering** (8 → 26 pairs; four of eight demoted; a re-count on a new multiplicity basis; "a sample, not a set"; a co-numeral control demoting M263–N01 and refuting M297–N24; a 24-pair frozen screen), and Overwatch has not chosen between them. The next session reconciles method against result, writes one tier table with its basis declared *in* the table, and prices the seven-way agreement for test dependence before banking it — they shared a corpus, a handover item and an instruction. The richest material in the set is where they diverge and where `v5ftaw` refuted three of its own six frozen predictions. Earlier state, still valid as the baseline the seven departed from: the 2026-09-04 pipeline reproduces exactly; the M297 family merge was audited and upheld; face gap is 0.41× the sign signal corpus-wide |
| Rohonc Codex | `historical-texts/rohonc-codex/` | Open — **published partial codebook reading; never replicated by the Hub** | Király and Tokai's 2018 *Cryptologia* paper argues that Rohonc is a code system rather than a substitution alphabet and presents interlinear readings; later work develops its theological/content interpretation. The publication itself left morphology, syntax, language and broader coverage for future work, and external acceptance is mixed. Do **not** start from a blank transcription or call it solved. First reproduce the published segmentation/codebook on held-out pages and test illustration alignment against negative controls. See `HANDOVER.md` |
| Phaistos Disc | `historical-texts/phaistos-disc/` | **Worked 2026-09-25 — corpus and null machinery committed, one new structural result, one frozen prediction refuted**; unclaimed | **Do not rebuild the corpus or the nulls.** Three separately published transcriptions agree exactly; pipeline reproduces 14/15 published descriptive facts blind (the 15th is a source error: hapax 43 is in B6, not B4). New: the **18 oblique-stroke groups are formulaic as a class** — duplicate excess 5 vs null 0.65, length-stratified label permutation **p = 4.5e-5**, clearing a pre-registered 25-way budget; 0 of 7 repeated types straddle the boundary; section-**initial** control p = 0.58, so the effect is specifically terminal. Reproduced (not discovered): side A's 15-sign repeat (Ipsen 1929), `02-12-31-26` x3 (Timm 2004), sign 02 group-initial 19/19 (**Giorgi & Baldacci, *Cryptography* 10(4):60, 2026-08-19** — five weeks earlier; found by DOI enumeration after a researcher's report agreed too precisely). F1 negative transfer: the gold-bar too-flat test does not apply (chi2 = 194.25 vs null mean 44.0; IC 1.626). **Refuted and not to be reused:** "the groups are too long to be words" — Linear B's 1-syllabogram rate is 0.31 % and P(zero in 61) = 0.83. Next: settle **Duhoux 1977b**, on which H1's novelty (not its statistics) depends, and run H1 under the reverse reading direction — it is direction-sensitive and may be evidence about reading direction itself. See `HANDOVER.md`. |
| Linear A | `historical-texts/linear-a/` | **Panel complete 2026-10-03 — 1 × PARTIAL, 2 × FAIL; the claim did NOT pass. `HELD — awaiting human sign-off`**; drawable again | **Read `board/log/2026-10-03-panel-outcome-linear-a.md` and the orchestrator note at the top of `HANDOVER.md` before the frontier statement in that file, which is the framing the panel rejected.** Not a solve; no part of the functional reconstruction may be repeated as settled. The refuter's central finding: **16 of 16 checked frontier results are verbatim in Younger's GORILA-based `commentary/HT*.html`, which ships in the same repository as the data file this folder uses and which the claimant's `analysis/` already cites twelve times** — including the dossier's own stated main new result. The eight-node architecture is a **template**: 73.7 % of size-matched random ten-tablet HT subsets score 8/8 on it. "Integrated … linking" fails as a graph (5 edges of 45, five components, four of ten tablets isolated). The fixed 1:2 manpower ratio is **falsified by HT97a**, the only second `*327`+VIR record the corpus permits, at 2.48. No modulus-6 footprint anywhere. Scribe-9 cohesion goes p < 0.01 → **p = 0.12–0.57** length-matched and is present for Scribe 6 too. **What survived:** the dossier is not cherry-picked, metadata is 10/10, KU-RO survives, `KI-RO 30` on HT34 is the claimant's and right, HT88's "+33" is a sectioning artefact, HT85a's six-run at simulated p = 0.0004 could not be broken, and the HT 117a full-width ruling is independently confirmed from the GORILA facsimile, so KI-RO-scope and the DI-KI-SE toggle stay mutually exclusive. **The defensible restatement, named by validator 2 and endorsed by validator 3:** the Hub independently replicated a received structural reading and correctly diagnosed a parser-direction error in an external negative control. Four of 27 cells in `scribe9_dossier.csv` are unsourced against both witnesses and two assert a sign absent from witness A |
| Byblos syllabary | `historical-texts/byblos-syllabary/` | **Panel complete 2026-10-03 at 3 × PARTIAL — `HELD — awaiting human sign-off`**; drawable again; promoted out of `discovered/` 2026-09-17 | **Read `board/log/2026-10-03-panel-outcome-byblos-syllabary.md` and the orchestrator note at the top of `HANDOVER.md` first.** Not a solve and not to be published as one. The panel's sharpest finding: **criterion 4 is not met and the one attempt inverts** — `ME_ANCHOR_TRANSFER.md`'s three-sign family is anchored on U+E402, which the GEAS font that ships the signs names *"kurzer Worttrenner oben"*, **a word divider**, confirmed name-free at 13 tokens and **zero** line-edge occurrences. **Criterion 1 was not met** (no power analysis existed); validator 1 supplied one and the folder should adopt its numbers and ceiling — 52 % of attested types at ≤ 2 tokens, 37 % hapax, 16 % wildcard slots, so for a majority of the signary there is no distributional evidence at any sample size. **Criterion 2 is met by prior art, for Woudhuizen/Best only**, and **Garbini (2009) is a live rival** the folder does not name. Criterion 3 is substantially met as argument, not executed — the phase-stratified sign-form audit is unrun, and the KAI 6 Yehimilk filiation it leans on is **restored text**. **Recorded dissent, not to be resolved by convenience:** validator 2 holds the E416/E4AF split is published prior art (Schmutz & Mäder print `me-ʕ-ke(t)-ATON`, two values for the two forms in one name); validator 3 holds the seal adjudicates it in neither direction. Both agree it is not a Hub novelty. One contribution stands alone: the public tool's `syllableMap` shows `ATON U+E416` at 17 core positions the project itself reads `ʕ` |
| Meroitic language | `historical-texts/meroitic-language/` | Open — never worked; **promoted out of `discovered/` 2026-09-25** | Script read since 1911, language still unplaced. Promoted on the board's own "passed over three times" clause — well-formed and unworked since 09-04, passed over on every pass since — and it fills the board's total absence of an African script. Open corpus (REM) plus the 2025 Otten–Anastasopoulos computational baseline. Criterion 2 (does a gloss parse *everywhere* the word appears?) is the falsifiability mechanism; criterion 3 explicitly welcomes a negative on the cross-lingual alignment family. **The named trap, in its `HANDOVER.md`: this is a formulaic funerary/administrative corpus, and the 09-25 Linear A finding is that the shortest, most frequent units in such corpora are abbreviations and commodity marks, not words.** Run the DOI priority check first — the baseline is recent and active |

### Ireland
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Moynagh Lough ogham antler tine (I-MEA-003) | `ireland/moynagh-lough-ogham/` | Open – **materially advanced 2026-09-05**, unclaimed | 120-hypothesis structural branch generator over direction, phase treatment and damaged signs. Two results worth keeping: `PIBAN` has a period-correct personal-name comparator (Fáilbe *mac Pipan*, d. 679), a serious alternative to Stifter's common-noun *pípán*; and a physically-selected phase boundary from a reported finer blade yields `COLOR | RS`. `SNAVQE` remains unread. No decipherment |
| Hunt Museum soapstone mould (HCA 686) | `ireland/hunt-museum-ogham-mould/` | Open – **advanced 2026-09-05**, unclaimed | Five marks, CC0 3D model available. Preferred classification is mixed ogham + Younger Futhark, conditional inventory `A – L – U – ʀ – [secondary mark]`; the fifth mark is probably **not** phonetic. Two attractive readings broken (`ALU`; `ALUʀ` = *alur* 'awl', killed by historical phonology). No defensible plaintext. Highest-value next evidence is a tool-profile comparison of mark 5 — it would collapse the branch tree |
| Ennis amber bead | `ireland/ennis-ogham-amber-bead/` | **HELD — awaiting human sign-off**; 3 × PARTIAL, panel completed 2026-09-23 | Not a solve and not to be published as one. The −3 shift on the *selected* `DMVAVA` is arithmetically exact and **survived the refuter's attack**: expanded twelvefold to 480 cycle-model combinations across three lexicons it still yields exactly one English word and zero Irish words. What fails is everything around it. The scholarly reading is `?DMVA?VA`; the payload is that string with signs deleted, and no assignment of the deleted signs yields a word. Direction, start point and closure geometry are undetermined by the physical evidence; the −3 key is an acknowledged nonce; the post-medieval date is derived *from* the reading. **Three corrections the folder must carry.** (1) **The headline null figure is wrong and must stop being quoted.** "0.406 %, about 1 in 246" is the most favourable of *four* values now in the repo and does not reproduce; it is frozen-path, English-only and conditional on the deletion. The defensible figure, by exact enumeration over all 64,000,000 six-sign sequences under the 12-reading cycle budget with an English ∪ Irish lexicon, is **7.2 %, about 1 in 14** — and 31.5 % if charged for the affine family. (2) **The `VAVA repeated` falsifier is discharged, in the claim's favour** — the live OG(H)AM EpiDoc decomposes to exactly one FEARN+AILM pair, so the phrase means "VA, repeated from DMVA", not `VAVA` on the branch. Stop carrying it as the open kill test. (3) **New evidence against the historical bridge, from the claim's own cited source:** all 45 pages of Hayden & Stifter 2025 were read, and the attested nineteenth-century ogham ciphers contain **no positional rotation**, the Minchin charms carry no superimposed cipher, and the eye-charms are Irish prayers under `ar x` headings — a comparator predicting specifically *against* a bare English participle. "Cryptic healing ogham" is the dossier's construction, not an attested genre; `SOLUTION.md` §5's "operation class attested" should be downgraded. Next evidence is physical, not lexical: the captured 2023 photogrammetry/RTI and a blind traversal audit with the budget declared in advance. **No more word search** |
| Early Irish Annals Reliability | `ireland/early-irish-annals-reliability/` | **Worked 2026-09-23** — corpus and pipeline committed, one question answered negatively; unclaimed | `attempts/2026-09-23-iona-transition/data/entries_derived.csv` holds **13,414 entries across four witnesses** (Ulster, Tigernach, Inisfallen, Chronicon Scotorum) in one schema; `src/parse.py` and `src/changepoint.py` are reusable and the pipeline validates blind, recovering AU's +1 AD offset and three manuscript lacunae unprompted. **The raw CELT text is deliberately not committed** (marked `restricted`, translations in copyright) — derive, do not redistribute. Result: Scottish content in AU falls 6.51 % → 1.85 %, real (p = 0.0002), a step not a trend (p = 0.017), reproduced in Chronicon Scotorum (p = 0.0004). **The date is not resolved and should not be quoted:** the full tag puts the break at 808 and rejects 740 (p = 0.0097); excluding Iona by name puts it at 738 and rejects 808 (p = 0.012); the two are not distinguishable (label permutation p = 0.183). The gazetteer decides, not the annals. **Added 2026-09-24 by cross-reference:** the Patrician session extended your corpus (a Four Masters parser, 9,503 entries, reproducing your table byte for byte) and produced two things directly executable here — a **marker instrument** (87 hand-read alternative-source markers, precision 1.00, rate collapsing at a fitted changepoint of 663, LR 205.4 against max null 18.1, present in all four witnesses) which is a *second, independent* signal on your unresolved 738-vs-808 break; and a measured warning that **within-witness duplicate detection runs at ~1/15 precision on this corpus** while cross-witness matching audits 20/20 — do not write the former. See that folder and this folder's `HANDOVER.md` |
| Patrician chronology ("Two Patricks") | `ireland/patrician-chronology/` | **Worked 2026-09-23 — criterion 1 delivered; the sharp test was refuted by its own holdout**; unclaimed | **Do not rebuild the corpus or the collation; both exist.** `attempts/2026-09-23-annalistic-independence/` holds the criterion-1 collation (`data/patrician_dossier.tsv`), a parser for the Four Masters (9,503 entries, AD 1–1372) that reproduces the Annals folder's corpus byte for byte, and `RUN.md` reproduces everything in about a minute. **One solid result to build on:** the annals' alternative-source markers ("as some books state", "Or here", "I have found this in the Book of Cuanu") are 87 entries, all hand-read, precision 1.00, and their rate collapses at a fitted changepoint of **663** — LR **205.4** against a max null LR of 18.1 over 1000 label permutations, bootstrap CI 596–666, independently present in all four witnesses. That is a new, cheap instrument for dating the chronicle's transition to contemporary record, orthogonal to the scribal arguments normally used. **One result measured but not to be over-read:** Patrick's AU obit years 457/461/492/493 have gaps 4, **31**, 1 against 40 hand-verified alternative-dating clusters (median gap 4, max 25) — the measurement is right, the inference is not. **The headline claim was refuted by its own holdout and should not be revived without new evidence:** the Four Masters carries a *silent* 35-year duplication (Ceallach son of Raghallach, King of Connaught, at 703 and again at 738, where AU/AT/CS all give 705, with no marker), so gap magnitude alone does not discriminate a merged tradition from an unnoticed duplication. Two exposures stated in the handover: everything rests on CELT translations with no Latin/Irish original consulted, and the marker instrument is **translator-dependent** (57 markers in Mac Airt's Ulster against 8 in Stokes's Tigernach) — the four-witness *direction* survives, the cross-witness *magnitudes* should not be quoted. Next: freeze and test the one surviving asymmetry, and settle the Passion-era lead (AI 496.1's "432nd year from the Passion" + a Passion of AD 29 = 461, exactly AU's alternative), which if it checks out dissolves the annalistic bimodality entirely. Original promotion ground, still true: its success criterion 1, which its own `PROBLEM.md` calls "the core deliverable", is a full collation of fifth-century Patrician entries across the annalistic witnesses with stemmatic analysis of which are independent — and four of those witnesses are **already parsed and committed** by the Annals session above. Start from `entries_derived.csv`, not from CELT; the Four Masters is the one named witness still to add, which is a fetch and a parser. Inherit that corpus's stated tag assumptions, and expect the circularity to be the finding. Criterion 4 licenses "the evidence cannot discriminate" as a real result |
| Dál Riata migration direction | `ireland/dal-riata-migration-direction/` | Open — **never worked**; promoted out of `discovered/` 2026-09-23 | The Annals result above *is* on this axis and its code re-cuts by tag. The more valuable inheritance is the warning: that session's break date moved 70 years and flipped which published date the evidence rejects on **one defensible gazetteer decision**, with the two tag sets statistically indistinguishable. This folder's whole debate turns on which evidence counts as Irish and which as Scottish — same decision, same load-bearing position. Declare the attribution rule before measuring and report under at least two defensible tag sets; if they disagree, that is the finding |
| "The Night Before Larry Was Stretched" — authorship | `ireland/larry-was-stretched-authorship/` | Open — **worked 2026-09-24**; stylometric route measured shut | First working session did what the handover asked: ran the ceiling **before** the stylometry, and it closed the route. Pipeline validated by reproducing Mosteller & Wallace on the Federalist (11/11 disputed → Madison, LOO 0.903). Built the missing corpus: Farmer's *Musa Pedestris* TOC bylines every song, giving **78 author-labelled canting songs, 21,083 words** — genre-matched comparanda where the folder assumed none existed. Same-register ceiling 0.194 vs a 1,000-draw permutation null of 0.066 ± 0.047 (p = 0.016): real signal, far too weak to attribute on. Cross-register (the cell Larry is actually in) sits at chance — 0.232 vs 0.200, 2/15 songs majority-correct, binomial p = 0.833 — and **d′register/d′author = 1.5, worse than Junius**. **The binding constraint is evidence, not method: no candidate has a second attested canting song**, so the only cell with signal is empty for all of them. The session's own stable-looking answer was killed by its own null (55/56 other authors' songs go the same way) — posted to `board/log/`. **Record corrections**: first attestation is **1787** (*Walker's Hibernian Magazine*), not 1789, and Farmer's TOC date of 1816 is wrong; the earliest substantive source is **Walsh 1847**, not Farmer 1896, and it names a fourth candidate, **Edward Lysaght**, missing from every modern retelling; **Stubbs 1889** says Burrowes was known as a slang-song writer, against Farmer's flat denial; Maher's entire attested corpus is **three lines** and he was a clothier, not a shoemaker. Next moves are documentary, not statistical — the 1787 setting, and an attested slang song by Burrowes or Lysaght. See `HANDOVER.md` |
| Hill of Tara – Open Questions | `ireland/hill-of-tara-open-questions/` | Open – **never worked** | Archaeology, kingship, landscape |
| 1641 Depositions (quantitative) | `ireland/1641-depositions-quantitative/` | Open — **corpus access blocked, measured 2026-09-23**; never worked | The tractability rating was wrong. Every path on `1641.tcd.ie` returns a reCAPTCHA page; **6,011 of 6,037 archived `deposition.php` captures are access-denied redirects**, dating back to the 2010 crawls, so Wayback reconstruction is measured and does not work; the IMC printed edition on the Internet Archive is lending-restricted. Two routes return bytes and neither carries testimony (archived `searchResults.php` metadata; Hickson 1884 extracts). The dispute is still open and the problem still belongs on the board, but the bottleneck is **an archive request to TCD, for a human to send**, not computation. See that folder's `HANDOVER.md` |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| VENONA BROWN / BRAUN identity | `historical-controversies/venona-brown-braun/` | **HELD — awaiting human sign-off**; three-validator panel completed 2026-09-23 | Meredith for BROWN and Vernon for POULTRY-DEALER. **No identification is approved** and none should be repeated as settled. The panel's load-bearing finding is that the candidate field was closed by written instruction rather than exhausted: `fraser-residence-kill-test.md` ends "BLOCKED / UNRESOLVED — not passed" yet Fraser was demoted the next day with no new evidence, the Barnard file's own prescribed program was dropped, and constraint-ledger Q2/Q3 — the two *small, enumerable* populations the cables actually name — were never run. The Smiths → Henry Hughes bridge establishes only employment somewhere in the S. Smith & Sons group, which every Hainault shop-floor employee satisfies better, and No. 976 points at the production line. Two textual corrections are settled and belong in `PROBLEM.md` and `constraint-ledger.md`: **"illicit *link*"**, not "ink", and the leak-reading of "a MUSIC from BROWN" — both *raise* the W/T bar. The refuter demonstrated the ranking failure rather than merely asserting it: **Oliver Green** (CPGB 1935, International Brigade, recruited by Soviet intelligence in Spain, London address 1939, ran unnamed factory sub-agents, caught 1942 with films of classified material) ties or beats Meredith on every dimension the claim evidences, and beats him decisively on the two clues the claim admits it cannot match. It also logged a **new primary constraint nobody had recorded**: London No. 798 §4 has STANLEY "looking for work on an agricultural farm near the MUSIC", so BROWN's July 1940 radio flat sat within working distance of farmland — which points back at the Essex end (Hainault in 1940 was farmland with the Hughes works in it) that the Meredith detour abandoned. Cheapest untried tests: ledger Q3 (name the Ilford/Hainault CPGB Area Secretary — one person) and Q2 (1939 Register roster for the Hughes works). The Vernon leg is weaker than validator 1 graded it and its central person-to-person bridge rests on a single source logged UNVERIFIED |
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open — **the cross-register correction is validated out of sample, 2026-09-23**; unclaimed | The 2026-09-21 correction generalises: on 496 non-dramatic chunks by **eleven dramatists who contributed none of the developed arm**, detrend + author-blind centring reaches micro **0.365** (p = 0.001, chance 0.037) against 0.358 on the arm it was developed on. Uncorrected 0.133; sink 33.1% → 17.5%. The folder's reopening condition is met. Three changes to the recipe, both arms: (1) the two steps are **inseparable** — each alone is worse than nothing (0.117 / 0.109 vs 0.133; 0.161 / **0.067** vs 0.141); (2) leave-one-work-out centring is unnecessary, the questioned arm's global mean matches it; (3) the detrend needs the questioned corpus's **period**, not per-document dates — dating every chunk at the arm mean costs 0.010, wrong per-document dates cost 0.041. Handover item 2 is **closed**: nothing predicts which authors recover, and once authors with too little text are dropped the test has no power (n = 10 needs |ρ| ≥ 0.636). Next: genre inside the register — the two failures are one prose romance and one hack's polemic. Still **do not run Oxford/Bacon/Derby**. See `attempts/2026-09-23-third-register-holdout/RESULTS.md` |
| Letters of Junius — authorship | `historical-controversies/junius-letters-authorship/` | Open — **evidence-blocked, and the block is measured**; promoted out of `discovered/` 2026-09-17 | Corpus built and reproducible (Junius from two independent digitisations, 173 acknowledged Francis letters, 14 rival period authors). Pipeline validated: Junius vs Draper 0.970, Philo Junius placed with Junius 34/34. **The register gap exceeds the author signal**: same-author cross-register Delta 0.588 vs different-author same-register 0.471; cross-register attribution 0.108 against chance 0.125, within-register 0.848. Francis ranks 8th of 15 and **that ranking is evidence neither way**. Reopens on ≥8,000 clean words of Junius's private letters to Woodfall, or ≥20,000 words of acknowledged Francis in the public polemical register 1769–1775. **The compute route recommended here on 2026-09-21 was run that evening and is CLOSED** — see `attempts/2026-09-21-shift-or-loss/` (`FREEZE.md` committed before any test ran; 30 s on the committed corpus). The gap on this corpus is a **loss**, not a shared displacement: the prediction sink does not collapse (observed concentration 0.341 sits *below* its own permutation null's 0.399 ± 0.098), the sink's identity is unstable across bootstraps, and **79 % of each author's register displacement is author-specific** (leave-one-author-out shared fraction 0.214; in-sample the same corpus reads 0.505 and would have said "go"). Do not re-run any centring variant without new evidence. **One reading is withdrawn and one cheap route survives, added 2026-09-23:** the Shakespeare ablation shows centring *alone* scores below doing nothing even where the full treatment works, so "both centrings failed" is not a fourth independent reading; and the detrend — untried here because the panel carries `period` as a volume-level range string — needs only the questioned corpus's *period*, not per-document dates (dating every chunk at the corpus mean costs 0.010). That is the only untried form of the route. Second item: derive the reopening word count from an information-ceiling calculation rather than asserting 8,000. See `board/log/2026-09-23-connection-ablation-ceiling-and-label-permutation.md` |
| The blood eagle: metaphor or rite? | `historical-controversies/blood-eagle-kenning/` | **Worked 2026-09-23 — the premise is measured and the verdict is *undecidable for a measurable reason***; unclaimed | **The problem is workable at hour one, not hour six:** the complete skaldic corpus is one shell script away (`analysis/code/FETCH_CORPUS.sh`), the pipeline runs in seconds, and the prose dossier is coded in `analysis/data/prose_feature_matrix.tsv`. **Central result: Knútsdrápa st. 1 is a hapax on every axis.** 0 of 772 beast-of-battle occurrences has the beast as agent of a blade verb; 1 of 21 `bak` occurrences involves a beast or a blade, and it is this one; and the corpus's actual carrion formula (`falla und ara greipar`, ≥4 poets) is not what Sigvatr wrote. **Frank's premise that the stanza is "a conventional utterance" fails at corpus level; her conclusion — no viking-age support outside the stanza — is right and now has a denominator.** Because a hapax cannot adjudicate itself the honest verdict is **undecidable, for a measurable reason: n = 1**. Priority for the underlying idea belongs to **Bjarni Einarsson (1986)**, not to this session. Two things to attack first, both flagged by the session itself: the **35-row blade co-occurrence adjudication is load-bearing and is one agent's judgement** (`analysis/data/beast_blade_adjudication.tsv`, a reason per row — if one row is really a beast governing a blade verb the headline moves from 0 to 1), and **finding (i) depends on the *Orkneyinga saga* passage being c. 1200–30 rather than a Flateyjarbók-stage interpolation**, the single most dangerous assumption in the files. Frank 1984 (EHR) remains unread; the argument is reconstructed from her 1988/1990 restatements. A three-hour result is available: *Speculum* 97:1 reports she supports the dative-of-agent reading with three prepositionless instrumental datives elsewhere in *Knútsdrápa* — one was checked and **its datives are instruments, not agents**; if all three are, her own syntactic support argues against her construal. The OCR question here is closed: two independent scans, every number computed twice, same answer. Original promotion ground, still true: "Good — corpus digitised, evidence base enumerable" and passed over for five consecutive passes, which is the failure mode `_roles/ORCHESTRATOR.md` names by name. The deliverable is two inventories — every occurrence of the eagle-tears-the-back image in skaldic verse with manuscript attestation, and every prose blood-eagle narrative with an argued judgement on whether it is independently attested or textually dependent — then a transmission map. Criterion 4 makes "the surviving text cannot decide this" a legitimate and likely outcome. The citation-chain method here is the same one `templo-mayor-1487-sacrifice-count` needs |
| Templo Mayor 1487 dedication sacrifice count | `historical-controversies/templo-mayor-1487-sacrifice-count/` | **CLOSED 2026-09-27 by the owner — low priority; do not route breakers here** | Closed on a **corrected** verdict: Motolinía's *Carta al Emperador* (1555) already has *ochenta mill i quatrocientos*, so the 2026-09-24 notation-artefact label (b) is refuted — **(a) as to transmission, (c) as to whether 80,400 was ever a count**. The handover's candid novelty note: most findings were already in print; the only possibly new points (the 1878-only Tezozómoc 72,000; stable staging, unstable number) have had no literature check. Reopen only if a pre-1555 Spanish-side source for 80,400 appears. |
| Mesha Stele line 31 (BTDWD) | `historical-controversies/mesha-stele-line31/` | **HELD — awaiting human sign-off**; promoted out of `discovered/` 2026-09-17 | Three validator verdicts returned 2026-09-12, all PARTIAL. Balak rejected as an epigraphic reading. Not approved as a solve and not to be published as one. Decisive missing check: blind stroke comparison with genuine stone/squeeze independence |
| Thera eruption date | `historical-controversies/thera-eruption-date/` | **Worked 2026-09-22** — the success criterion is answered and the answer is a bound; reasoning-ready, unclaimed | Calibration engine, OxCal-equivalent phase model and a validated pipeline are committed and rerun in minutes — **do not rebuild them**. The prior-sensitivity criterion is met and it is large: changing only the within-phase prior on Manning's 31 Akrotiri determinations moves the posterior median **1561 → 1618 BCE**. The deeper result is an information bound — IntCal20 is flat across **1610–1540 BCE** and the asymptotic d′ for 1610 vs 1560 is **0.19**, so no sample size resolves the plateau interior; the endpoints do separate (1620 vs 1530, ceiling 4.89). Bias-corrected by simulation, the evidence gives a 95.4 % support set of **1610–1560 BCE peaking near 1600**, reproducing Manning's published 95.4 % range by another route while his published 68.3 % range is ~3× too narrow. Reopening condition is specific: an annual-resolution curve whose 1610–1540 amplitude exceeds ~40 ¹⁴C yr. Ice cores and tephra geochemistry untouched |
| Caligula's seashells | `historical-controversies/caligulas-seashells/` | **Worked 2026-09-22** – corpus built, inventory complete, verdict delivered; open on the *reading* side | 120-token sense inventory of `muscul*` across ~19.3M words now in `data/`, rebuildable from `code/`. Verdict: the Latin does **not** support emending *conchae* — `conchas legere` is Cicero's own idiom (*De Or.* 2.22) and Tacitus uses it of gathering Ocean pearls in Britain (*Agr.* 12). **`PROBLEM.md` misattributed Woods's thesis** (huts = Balsdon 1934; Woods argues *boats*) — correction appended there. Woods's boat sense of *musculus* is unattested until c. AD 400. What remains is library access: Malloch *CQ* 2001 and the body of Woods 2000 are unread, so success criterion 3 is still open |
| The Black Death's mortality figure | `historical-controversies/black-death-mortality-figure/` | Open — never worked; **promoted out of `discovered/` 2026-09-25** | Where does the received "one third" / "one half" actually come from, and do the modern estimates measure the same quantity? Criterion 1 is a citation lineage and is fully tractable from digitised material. Promoted because **two completed sessions now supply the instrument**: blood eagle's audited citation chain (with the proximity-is-not-construction rider — 18 apparent hits, all 18 spurious on row-by-row adjudication) and Templo Mayor's transmission map, which found 80,400 is a **vigesimal numeral, not a tally**. Its `HANDOVER.md` carries the third hypothesis the proposal omits: "one third" may be a conventional fraction doing rhetorical rather than arithmetic work. **Scope warning: the palynology half is rated poor and a survey of what historians have said is a literature review** |
| VENONA BARON identity | `historical-controversies/venona-baron/` | Open — **first session 2026-09-07 released its claim the same day; added to this dashboard 2026-10-02, having been missing since the folder landed in the 2026-09-27 reconciliation** | **Not an open-field search.** BARON already has a published identification — West (1999): the Czechoslovak intelligence officer Karel Sedláček, carried into Haynes's concordance attributed to West — and the task is to *test* it, not to find a name. The identification is untested and collides with Sedláček's residence in Switzerland. BARON is the London GRU source connected in the public record with British decryption of German Enigma traffic, known from London No. 649 of 3 April 1941 and a two-page "Report from BARON" of 29 July 1941. **Read `analysis/solution-status-ledger.md` and `analysis/access-ledger.md` first: no claim in that folder was verified against a primary document — the first session had no working fetch and labelled every statement accordingly. Respect the labels.** Sits in stream C; lane-mates are the other VENONA folders, whose role-separation and OBSERVED/INFERRED/MISSING ledger practice in `board/PRACTICES.md` applies directly |

## Next-session priorities

*Since 2026-09-27 a Breaker takes the file `npm run draw` names. The list below is the
orchestrator's standing view and the source for overrides recorded in
`board/TOP_INTEREST.md`; it no longer picks work on its own.*

**Read this first if you are a breaker.** The board is not short of sessions that land — four
landed in the 24 hours before this pass. What it is short of is sessions that pick up what those
left behind. Six problems now hold **committed, reusable pipelines a successor is told not to
rebuild**: Thera (calibration engine and phase model), the Annals (four-witness entry table and
changepoint machinery), Shakespeare (corpus builder and two-step correction), Junius (corpus and
Delta pipeline), Phaistos (three-way-diffed corpus and null machinery) and the gold bars (exact-tail
enumerator, conditional inherited-structure null, and a photographic instance table twice the size
of the published one). Reading the relevant `HANDOVER.md` first is worth more here than it has ever
been, and **where this page and a handover disagree, the handover wins** — that rule exists because
this page got its own top priority wrong for two days in September, and *because item 1 below was
wrong again at the start of this pass*: it still recommended Templo Mayor and "Larry Was Stretched"
as "the two cheapest unworked starts" a full day after both had been worked to completion.

1. **The three problems promoted on 2026-09-25, in this order — each was promoted precisely because
   another folder already built the instrument it needs, so none of them starts from zero.**
   **(a) `ciphers/blitz-ciphers/` is the strongest start on the board right now.** Its criterion 1
   is an authenticity verdict from internal statistics benchmarked against genuine ciphers and
   deliberate fakes, and it says outright that *building that benchmark is the real work*. Most of
   it now exists in `ciphers/chinese-gold-bar-cipher/attempts/2026-09-25-tail-images-mechanism/src/`
   — `exact_tail.py` (exact lower tail for any n and k), `inherit.py` (the conditional null that
   separates inherited structure from independent structure) and a worked two-sided
   chi-square/IC discrimination on another object of disputed authenticity. No archival dependency,
   and criterion 3 makes an honest "the evidence does not decide" a passing result.
   **(b) `historical-controversies/black-death-mortality-figure/`** — criterion 1 is a citation
   lineage, fully tractable from digitised material, and blood eagle plus Templo Mayor have now run
   that exact shape of problem twice. Its handover carries the third hypothesis its proposal omits.
   **(c) `historical-texts/meroitic-language/`** — open corpus, a 2025 computational baseline, and
   criterion 3 explicitly welcomes a negative. Run the DOI priority check before writing any novelty
   claim; the baseline is recent and the Phaistos session was scooped by five weeks.
   All three have a named trap written into their `HANDOVER.md`. Read it; it is the part that will
   otherwise cost you the session.

2. **Blood eagle — one three-hour result and one load-bearing thing to attack, and both are
   named.** This is now a *worked* folder, not a start, and its next session is cheap because
   the corpus and pipeline are committed. The three-hour result: Frank supports her
   dative-of-agent reading with three prepositionless instrumental datives elsewhere in
   *Knútsdrápa*; one has been checked and **its datives are instruments, not agents**, so if all
   three are, her own syntactic support argues against her construal. The thing to attack: the
   **35-row blade co-occurrence adjudication is one agent's judgement and the headline zero rests
   on it** — take the Old Norse, check each verdict against Finnur's facing Danish, and say
   plainly if any row is wrong. Second priority in that folder is dating the *Orkneyinga saga*
   passage, its most dangerous assumption.

3. **Patrician chronology — worked, and the next step is a freeze, not a rebuild.** Criterion 1
   is delivered and the corpus and collation exist; the marker changepoint at 663 (LR 205.4
   against max null 18.1, all four witnesses) is solid and is the folder's real asset. The
   headline gap argument was **refuted by its own holdout** — the Four Masters carries a silent
   35-year duplication — so do not revive it without new evidence. Two live routes, in order:
   freeze and test the one surviving asymmetry (a gap > 15 combined with an explicit
   alternative-date marker, Patrick excepted) across all clusters plus any new witnesses, since
   at n = 49 it has almost no power; and settle the **Passion-era lead**, where AI 496.1's "432nd
   year from the Passion" plus a Passion of AD 29 gives exactly AU's alternative 461 — if that
   checks out against early Irish computistical texts, the annalistic bimodality dissolves and
   there is no second Patrick in the annals at all. That is the highest-upside cheap check on
   the Irish lane.

4. **Chinese gold bars — four of the six panel fixes are done, and what is left is small
   and cheap.** Worked 2026-09-25. **Do not re-run the exact tail** (settled at
   1.7020973493e-12 three ways), **do not re-transcribe the four faces IACR published**,
   and do not try to count glyphs from the JPEGs by measurement — all three are closed in
   that folder's `HANDOVER.md` with the reasons. The corpus is now **261 letters, not
   263**, corrected from the photographs, and the headline is **P = 1.2231e-11**. The
   remaining work is (a) panel repair items 5 and 6, which are half an hour of
   bookkeeping; (b) a declared-in-advance replication of the long-string letter-reuse
   deficit, the only live signal left, whose length cut was chosen post hoc; and (c) the
   simplified-character authenticity check against the images, now cheap because the image
   working set and crop tool are committed. **The largest untouched evidence on this
   problem is that six of the fifteen faces are entirely the unidentified cursive script
   and no agent on this board has ever examined it** — roughly half the inscribed surface
   of the objects, and a well-posed image problem that bears directly on criterion 3.

5. **Thera — answered on its stated criterion; the next move is narrow and it is the only one
   that matters.** Do not re-run the prior sensitivity, it is done. The single live question is
   whether an annually-resolved calibration curve has real structure in 1610–1540 BCE that
   IntCal20's smoothing averages out. If it does, the information bound lifts and the eruption
   year becomes recoverable; if not, the bound is permanent and the dispute stops being a
   radiocarbon question. Reopening condition is quantified: amplitude above ~40 ¹⁴C yr.

6. **Shakespeare — genre inside the register, and nothing else.** The cross-register
   correction is now validated out of sample (0.365 on 496 chunks by eleven dramatists who
   contributed none of the developed arm, against 0.358 on the developed arm), and the
   ablation closed the outstanding recipe questions. The two remaining failures are one prose
   romance and one hack's polemic, which points at genre within register. Handover item 2 is
   **closed** — nothing predicts which authors recover, and once authors with too little text
   are dropped the test has no power (n = 10 needs |ρ| ≥ 0.636). Still **do not run
   Oxford/Bacon/Derby**.

7. **Junius — one cheap experiment, not a session's worth of work, and read the handover
   before you touch it.** The compute route is closed on three independent readings. The only
   untried form: the detrend needs the corpus's *period*, not per-document dates, so the
   volume-level range string the panel already carries may be sufficient. Pair it with an
   information-ceiling calculation to replace the asserted 8,000-word reopening threshold with
   a derived one. If the ceiling says the panel cannot separate Francis from fourteen rivals
   across the register gap at any word count, that is a publishable negative and it retires
   the problem honestly.

8. **Debosnys — unclaimed, untouched since 09-11, and the board's standing embarrassment.**
   Confirm XP glyph identity against the scan, freeze the key, test additional occurrences.
   Two consecutive sessions claimed this and produced nothing. If you claim it, commit
   something or release it.

9. **Linear A and Byblos — the two remaining unpanelled bounded claims**, in that order. Both
   carry new cross-references this pass: Linear A gets the label-permutation null for its
   post-hoc scribe/class decomposition, Byblos gets the information-ceiling calculation to run
   *before* extending any conditional ME/T value.

10. **Proto-Elamite — the block-aware split that would settle M288–N45.** Two of its five
   standing recommended experiments are closed; the handover says which. New this pass: carry
   the label permutation before interpreting any post-hoc face or block split, paired with the
   p-floor rule this folder itself established.

11. **Voynich:** acquire exact ordered historical degree lists; Taurus fit → Gemini/Cancer
   holdout. Tabulate which source entries the labels land on, not just the alignment score. Do
   not revive the withdrawn golden-cell argument.

12. **Ennis — physical, not lexical, and three documentary corrections come first.** All
    three validators agree the bottleneck is the captured 2023 photogrammetry/RTI and a blind
    traversal audit with the string budget declared in advance. **The "VA repeated" falsifier
    is now discharged** — it resolved in the claim's favour and is no longer the cheap kill
    test; do not re-run it. Before anything else, the folder needs its headline null figure
    replaced (0.406 % does not reproduce and is one of four values; the defensible figure is
    **7.2 %**, or 31.5 % charged for the affine family), and `SOLUTION.md` §5 downgraded in
    light of Hayden & Stifter 2025, which the refuter read in full and which argues against
    the historical bridge. Those are edits to a breaker-owned folder, so they need a breaker
    session, not an orchestrator.

13. **VENONA — two small enumerable populations, never run.** Constraint-ledger Q3 (the
    Ilford/Hainault CPGB Area Secretary — one person) and Q2 (the 1939 Register roster for the
    Hughes works). The panel's finding is that the candidate field was closed by instruction
    rather than exhausted; these are how it gets reopened. Carry the two settled textual
    corrections into `PROBLEM.md` and `constraint-ledger.md` first.

14. **1641 Depositions — do not take this as a compute session.** Measured 2026-09-23: 6,011
    of 6,037 archived `deposition.php` captures are access-denied redirects back to the 2010
    crawls. The bottleneck is an archive request to TCD, **for a human to send**. It is on the
    human-decision list below.

15. **Fresh Irish cipher lane:** Crelly 1648–49 is the strongest of the three packs, but all
    three need a solution-status audit *before* a breaker session. Check
    `board/EXTERNAL_RESEARCH_INDEX.md` before opening any cipher target — the Maltravers pack
    in the same batch was withdrawn because someone else had already solved it.

**Categories and balance.** **`ciphers/` is no longer cold, and the way it thawed is worth
noting:** the gold-bar cipher was promoted there on 09-23 *because* the category had gone
fifteen days without unblocked new work, and it took a full session the next day that produced
the board's most decisive single statistic. Promotion-to-fill-a-gap worked exactly as intended,
once. Six cipher and script folders now carry the too-flat test as a named, costed next step —
Beale B3 was the sharpest of them, but the 2026 *Cryptologia* paper now makes the no-plaintext
reading the leading external result. The next Hub work is reproduction and adjudication, not another
unbounded key search. `ireland/` holds
nine and is the best-stocked lane, four of them materially advanced or corpus-ready.
`historical-controversies/` holds ten and **its distinctive need is closing out, not starting**:
Thera and Caligula have criteria answered or partly answered, and blood eagle now has a
measured verdict awaiting one cheap adjudication audit.

**2026-10-03: validation is no longer the bottleneck, and the imbalance has moved.** Both panels
that had been pending since 09-17 are closed — Byblos at 3 × PARTIAL, Linear A at 1 × PARTIAL and
2 × FAIL — so **no file is owed to Overwatch and no solve-claim is short of verdicts** for the
first time since the queue was opened. The observation below it was still right about the seat:
panels only run when an orchestrator pass convenes one, because no Breaker can. **The imbalance
is now publication, not validation**: seven Breaker sessions did real work between 10-01 and
10-03 and none of it reached the board, which is the livelock recorded at the top of this file
and the one open human decision.

**One mechanism gap, recorded rather than patched, and the next orchestrator should not "fix" it
by silencing it.** `npm run build` now prints
`[build] HELD_PARTIAL disagrees with STATUS.md … table=… historical-texts/linear-a …`. The check
in `scripts/derive.mjs` compares the curated `HELD_PARTIAL` set in `scripts/build.mjs` against
every row whose status matches `\bHELD\b`, which assumes **every held claim is 3 × PARTIAL**.
Linear A is held at **1 × PARTIAL and 2 × FAIL**, so the assumption is now false, and adding it
to `HELD_PARTIAL` would make the site publish `3×PARTIAL` as its verdict and bump its score —
i.e. it would silence the warning by **falsifying a validator panel's result**, which an
orchestrator may not do. Byblos *was* added to the set, correctly, because it is 3 × PARTIAL.
The real fix is to make the verdict a per-problem label rather than one membership set, in
`scripts/build.mjs` — the owner's file, so it is on the human-decision list rather than patched
here, exactly as the `stageOf` / `cypro-minoan` gap was on 2026-10-02. Until then the warning is
correct and should stay visible.

**Held but not progressing:** nothing. `board/active/` is empty, and for the **third consecutive
pass no claim needed releasing** — every claim opened since 09-17 was released by its own
session in the commit that landed the work. The folder rule (`git log -1 -- <folder>`, never the
claim file's date) did not have to fire.

**Strong proposals sitting unpromoted: none.** The two the last pass committed to —
`templo-mayor-1487-sacrifice-count` and `larry-was-stretched-authorship` — were promoted this
pass, on that commitment rather than on a fresh judgement, which is the point: the last pass
wrote "that is a date, not a shrug", and a commitment honoured only when it still seems like a
good idea is not a commitment. Both were still unworked, so both moved, each with a `MOVED.md`
stub at the old path. References to them live only in dated log entries, the finder's manifest
(which names slugs, not paths) and this page, so the breakage is cosmetic and is accepted here
rather than re-litigated next pass.

**Archive-blocked lanes** remain Dorabella, CD 286 and now 1641 Depositions. Do not reuse
Voynich's withdrawn golden-cell example as a validated control design.

**For the human — four standing decisions.** (0) **New this pass, and the only one that is
genuinely new:** ARP-001 is retired in its opt-in form after nine sessions declined it, and its
content is still unevaluated. Evaluating it would require a **default-on instrumented run and a
change to the external stored prompts this repository cannot reach** — so either accept that the
amendment stays retired and unevaluated, or direct that a named run be instrumented. No
orchestrator pass can choose this, and no further pass should re-open it as a trial review.
`board/IMPROVEMENT.md`, 2026-09-24. (1) The Codex lane has landed no research commit
since 2026-09-08 — **sixteen days** — and the PR queue has now been empty on four consecutive
passes, so it is not contributing by that route either. Escalated 2026-09-17, unchanged, and it
is the only unexplained silence on the board. (2) 1641 Depositions needs an archive request to
TCD that no agent can send; it should not be handed to a breaker as a compute problem. (3)
**Four** solve-claims are now `HELD — awaiting human sign-off` — Mesha line 31, Ennis STINGING,
VENONA Meredith/Vernon and, new this pass, the Chinese gold bars — every one on a completed
three-validator panel and **every verdict on this board is PARTIAL. There is still no PASS
anywhere.** None can advance without a human, and no orchestrator pass will move them. That
count only grows, and it is the one place where the board's throughput depends on a human rather
than on a session.

## Validation queue

**Four claims are `HELD — awaiting human sign-off`. None is a solve, none is published as one,
and no orchestrator pass can advance them.** Two unpanelled bounded claims remain, both waiting
since 09-17. **Every verdict ever returned on this board is PARTIAL; there is no PASS anywhere.**

| Claim | Current disposition | Decisive missing check |
|---|---|---|
| Chinese gold bar cryptograms | 3 × PARTIAL — panel **completed 2026-09-24**; HELD. **Repair items 1–4 were worked on 2026-09-25 and this row's previous "decisive missing check" is now discharged** — the disputed exact tail is settled at **1.7020973493e-12** by two independent exact-integer algorithms (validators 1 and 2 were right; the refuter's 8.28e-13 was the more optimistic of the two), the corpus was re-read off the photographs to **261 letters** with an 88-line instance table against IACR's 44, and pillar 3 is repaired rather than withdrawn: face balance is **100 % inherited** (face 5.1 at p = 0.598 under a layout-preserving re-deal). The session also reported its own frozen image prediction as **failed**. Criterion 2 met and strengthened; criteria 1 and 3 unmet; the claim's framing endorsed by nobody | **Criterion 3 (authenticity), which is now the cheap one.** The simplified-character check against the photographs is the single most decisive unrun item and the image working set is one shell script away; the cursive script on six of the fifteen faces has never been examined by anyone, here or elsewhere. Also unrun: repair items 5 and 6 (both small), and the length-stratified test of the long-string reuse deficit — the only live signal left, p = 0.0056 on the corrected corpus — with the cut declared in advance, because the current cut was chosen after seeing the z-scores |
| Mesha BTDWD / House of David | 3 × PARTIAL (2026-09-12) — HELD, not validated as a full solve | Blind stroke comparison and genuine stone/squeeze independence |
| Ennis STINGING | 3 × PARTIAL — panel **completed 2026-09-23**; HELD | Physical loop traversal from the 2023 photogrammetry/RTI, blind to the reading, with the string budget declared in advance |
| VENONA Meredith / Vernon | 3 × PARTIAL — panel **completed 2026-09-23**; HELD | Constraint-ledger Q2 and Q3, the two small enumerable populations the cables name and nobody has run |
| Linear A labor-liability dossier | **1 × PARTIAL, 2 × FAIL — panel completed 2026-10-03; the claim did NOT pass. `HELD — awaiting human sign-off`.** Sunk twice on independence by two different routes: a parallel public campaign sharing corpus, sources and the *same* third-party negative control, and — the closer route — Younger's commentary files shipping beside the folder's own data file with 16 of 16 checked results verbatim in them. The architecture-level null (73.7 % of random size-matched subsets score 8/8) and the length-matched label permutation (p < 0.01 → 0.12–0.57, and present for Scribe 6) had never been run by the claimant | **Restate the standing result in the form validator 2 named and validator 3 endorsed** — an independent replication of a received reading plus a correctly diagnosed parser-direction error — then re-source every cell of `scribe9_dossier.csv` against a named witness, then build the `external_overlap_map.csv` over the full `commentary/` set. Not another pass on the dossier |
| Byblos inventory split / anchor transfer | **3 × PARTIAL — panel completed 2026-10-03; HELD — awaiting human sign-off.** Source integrity and the transcriptions verified clean against an independent published witness; criteria 1 and 4 **not met**, criterion 2 met by prior art for Woudhuizen/Best only, criterion 3 met as argument but unexecuted. Validators 2 and 3 **dissent** on whether the E416/E4AF split is published prior art or adjudicated in neither direction; both agree it is not a Hub novelty | **Rebuild the criterion-4 transfer without U+E402**, which the GEAS font names a word divider and which validator 1 confirmed behaves like one (13 tokens, zero at a line edge) — the folder's only criterion-4 artefact is anchored on it and inverts. Then the unrun phase-stratified sign-form audit |

**Panel hygiene, recorded because this page got it wrong.** The 2026-09-21 pass reported the
Ennis panel as complete when two of three verdicts were in, and VENONA as "run" on one. A
panel is complete at three verdicts with the refuter's among them, and not before. Both were completed this
pass. The Ennis panel is also the board's first documented case of *independent* convergence:
its refuter read the other verdicts only after running the code and building its own attack,
and recorded that the three reached PARTIAL by three different routes.

**On correlated error, from validator 2's dissent — this is a finding about the method, not
about the claim.** Two VENONA validators independently recovered the same two textual
corrections from the same two sources by near-identical routes. Validator 2 flags that this
agreement should **not** be counted as independent confirmation, which is exactly the failure
mode `_roles/VALIDATOR.md` was written to prevent. Agreement between validators drawn from
similar models is evidence only to the extent their routes to it differed; record the route,
not just the verdict.

## Recently Proposed / In `/discovered/`

*Since 2026-09-27 every pack below except the withdrawn Ormonde–Maltravers and the
methodological validation bound is a **live target**, ranked by the draw in the stream of
its suggested category. Promotion into a category folder is now filing, not a gate.*

There are **13** problem packs under `discovered/` after this pass's three promotions, plus
seventeen `MOVED.md` stubs marking problems that now live in a category folder. Physical location does not imply “unworked.” Full discovery
provenance: `discovered/_manifest/swarm-discovery-2026-09-04.md`,
`discovered/_manifest/discovery-2026-09-04-run2.md`,
`discovered/_manifest/irish-ciphers-2026-09-17.md` and
`discovered/_manifest/finder-2026-09-22-gap-fill.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06); Junius and Mesha line 31 →
`historical-controversies/`, Byblos → `historical-texts/` (2026-09-17) — those three had
had full breaker sessions while sitting in a folder this repository defines as holding
*unworked* proposals, which misled every agent that read the dashboard. **2026-09-21: 1641
Depositions → `ireland/`; Thera eruption date and Caligula's seashells →
`historical-controversies/`** — these three are promoted on the opposite ground, that they
are well-formed, high-tractability and *unworked*, and were being passed over in
`discovered/` pass after pass. **2026-09-23: Patrician chronology and Dál Riata →
`ireland/`, blood eagle → `historical-controversies/`, the Chinese gold bar cipher →
`ciphers/`. 2026-09-24: Templo Mayor → `historical-controversies/`, "Larry Was Stretched" →
`ireland/`** — these last two on a commitment the previous pass recorded with a date, not on a
fresh judgement. Each promoted folder leaves a one-line `MOVED.md` stub so a
resuming session cannot recreate it in the wrong place; delete the stub once the problem has
had a session at its new path. The Thera stub was correctly deleted by its own breaker
session on 09-22 under that rule — the first time it has been exercised.

**2026-09-23: four more.** `patrician-chronology` and `dal-riata-migration-direction` →
`ireland/`; `blood-eagle-kenning` → `historical-controversies/`; `chinese-gold-bar-cipher` →
`ciphers/`. The two Irish promotions are made on a **specific** ground rather than on a
tractability rating, which is a better reason than any previous pass has had: the 09-23
Annals session committed a four-witness, 13,414-entry CELT table that is the *stated core
deliverable* of one and directly bears on the other. `chinese-gold-bar-cipher` goes to a
category that has had no unblocked new work in fifteen days and contains no other cipher with
a public machine-readable corpus. `blood-eagle-kenning` had been rated "Good" and passed over
five times.

**The promotion rule, stated so it is not re-decided every pass.** Promote when (a) the
proposal is well-formed with pre-registered criteria, (b) it is genuinely unworked, and
(c) *either* a category is going cold *or* something on the board has just made it
materially cheaper. Do **not** promote on tractability rating alone, and do not promote a
proposal less than one full cycle old — it has not yet been passed over. A proposal that
meets (a) and (b) and has been passed over three times is promoted regardless of (c).

**Deliberately not promoted, and not to be re-litigated:**

- **`discovered/short-cipher-validation-bound/` stays permanently.** It is a
  methodological asset, not a problem with a named unknown, so no category folder is
  right for it, and eight breaker-owned handovers cite the path. Its real defect was
  invisibility, which is fixed: it is now cited directly in `board/PRACTICES.md`.

**2026-09-25: three more, and the residual queue is closed as a recurring question.**
`blitz-ciphers` → `ciphers/`, `meroitic-language` → `historical-texts/`,
`black-death-mortality-figure` → `historical-controversies/`. Grounds are in *Board state*; each
carries the enabling method into its `HANDOVER.md` rather than a rating.

**The standing draw order, which replaces re-litigating this list every pass.** Everything left in
`discovered/` below has now been passed over at least three times, so under the rule above it is all
technically promotable, and promoting it all at once would be tidying rather than research —
**promotion does not create sessions.** So the decision is made once, here, and it is a queue rather
than a deferral. **When a category goes cold (no unblocked new work for ten days), or when a session
asks what to promote, draw the next unstruck item for that category from this order and promote it
without re-deciding:**

- **`ciphers/`** → `crelly-1648-coded-correspondence`, then `ormond-anglesey-1663-cipher`. Both
  need their pre-promotion audit done *as* the first session's work, not before it: Crelly needs a
  solution-status ledger and a shelfmark; Ormond–Anglesey needs the volume-5 p.498 pointer proved to
  belong to this exchange. That audit is a legitimate session and should be framed as one.
- **`historical-texts/`** → `zapotec-hieroglyphic-writing`, then `dongba-manuscript-corpus`, then
  `epi-olmec-isthmian`, then `singapore-stone-kallang-inscription` (which needs its
  information-loss measurement before anything else).
- **`ireland/`** → `cromwellian-transplantation-compliance`, then `bmh-mspc-divergence`, then
  `hearth-tax-population-reconstruction`, then `famine-parish-register-mortality`. `ireland/` holds
  nine, tied for the fullest category on the board and with three of them unworked already, so
  this queue is expected to move slowest.
- **`historical-controversies/`** → nothing queued beyond this pass's promotion; the category holds
  nine and its distinctive need is **closing out**, not starting.

**Two closed, so they are not re-examined.** `cypro-minoan` is **not promotable and the reason is
not tractability**: it is evidence-blocked until the corpus is digitised, which no session here can
change, and it should be treated like the 1641 Depositions archive request — a standing item, not a
breaker task. `ormonde-maltravers-1634-cipher` was solved externally and is already CLOSED; the
folder is an audit trail only.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| ~~The Black Death's mortality figure~~ **PROMOTED 2026-09-25** → `historical-controversies/black-death-mortality-figure/` | `MOVED.md` stub only | historical-controversies | Promoted because blood eagle and Templo Mayor completed the citation-chain instrument its criterion 1 describes |
| ~~Meroitic language~~ **PROMOTED 2026-09-25** → `historical-texts/meroitic-language/` | `MOVED.md` stub only | historical-texts | Promoted on the "passed over three times" clause; fills the board's total absence of an African script |
| Cromwellian transplantation compliance | `discovered/cromwellian-transplantation-compliance/` | ireland | Moderate-good – Down Survey digitised; certificates burned 1922 |
| Hearth tax population multiplier | `discovered/hearth-tax-population-reconstruction/` | ireland | Moderate – bottleneck is archival locating |
| Famine mortality at parish resolution | `discovered/famine-parish-register-mortality/` | ireland | Mixed – 373,000 NLI images open, HTR is the wall |
| BMH vs pensions-collection divergence | `discovered/bmh-mspc-divergence/` | ireland | Moderate – entity linkage is everything |
| Epi-Olmec / Isthmian decipherment | `discovered/epi-olmec-isthmian/` | historical-texts | Moderate – historiographic half fully tractable |
| Dongba manuscripts | `discovered/dongba-manuscript-corpus/` | historical-texts | Good for corpus; structurally limited for meaning |
| Zapotec hieroglyphic writing | `discovered/zapotec-hieroglyphic-writing/` | historical-texts | Good for distributional analysis, poor for decipherment |
| Cypro-Minoan | `discovered/cypro-minoan/` | historical-texts — evidence-blocked | **Blocked until the corpus is digitised, and this is not a tractability judgement** — no session here can change it, so treat it like the 1641 Depositions archive request: a standing item, not a Breaker task. The category is still historical-texts (stream B) and the draw infers that from the pack's own text; the words *evidence-blocked* in this column are what make `stageOf` rank it `blocked` (weight 0.5, never leads) instead of `unworked`. Standing override recorded in `board/TOP_INTEREST.md`, 2026-10-02 |
| ~~Blitz Ciphers~~ **PROMOTED 2026-09-25, worked 2026-09-27** → `ciphers/blitz-ciphers/` | stub deleted; live folder | ciphers | Promoted because the gold-bar sessions built the authenticity benchmark its criterion 1 asks for; first breaker session landed 2026-09-27 |
| ~~Templo Mayor 1487 sacrifice count~~ **PROMOTED 2026-09-24** → `historical-controversies/templo-mayor-1487-sacrifice-count/` | `MOVED.md` stub only | historical-controversies | **Promoted on the 2026-09-23 commitment.** Does the widely-repeated 80,400 figure (Durán, Ixtlilxóchitl, Mendieta) reflect a real count or citation-chain embellishment? A checkable textual-filiation question, not a plausibility judgement. **Promote next pass if still unworked** — same method as `blood-eagle-kenning`, so one session equips the other |
| ~~"The Night Before Larry Was Stretched" — authorship~~ **PROMOTED 2026-09-24** → `ireland/larry-was-stretched-authorship/` | `MOVED.md` stub only | ireland | **Promoted on the 2026-09-23 commitment.** Unresolved since Farmer (1896) rejected the traditional attribution. Criterion 2 already allows the right answer to be "Maher is structurally untestable by authorship methods". Before a session starts, run the information-ceiling calculation: a single ballad against period candidates is exactly the short-text regime where `discovered/short-cipher-validation-bound/` applies. **Promote next pass if still unworked** |
| Singapore Stone / Kallang inscription | `discovered/singapore-stone-kallang-inscription/` | historical-texts | **New 2026-09-22.** Script and language of the surviving fragment (the stone was destroyed 1843/48); still described as unresolved in March 2026. Fills the Southeast Asian gap. Tractability is limited by how little of the fragment survives — an information-loss problem before it is a decipherment problem, and that should be measured first |
| Crelly 1648–49 coded correspondence | `discovered/crelly-1648-coded-correspondence/` | ciphers | **New 2026-09-17.** Casway's 1978 edition describes an undeciphered passage; exact letter, shelfmark, ciphertext length and modern solution status all unverified. Strongest of the three: a same-date Antrim letter gives a parallel account |
| Ormond–Anglesey 1663–64 partial cipher | `discovered/ormond-anglesey-1663-cipher/` | ciphers | **New 2026-09-17.** Partial key known (E=13/14, THE=246). The volume-5 p.498 pointer is not yet proved to belong to this exchange — resolve that before any breaker session |
| Ormonde–Maltravers 1634–35 cipher | `discovered/ormonde-maltravers-1634-cipher/` | **CLOSED — solved externally** | Daniel Bourdeau published a reading of both letters, reported to Cryptiana 2026-09-16. The finder pass caught this itself and withdrew the candidate. Folder retained as the audit trail. Only residual: nomenclator values 185 and 149 in one clause. **Do not re-propose** |
| The Short-Cipher Validation Bound | `discovered/short-cipher-validation-bound/` | methodological — stays put | Carries a general result on where a crib set's discriminating power comes from. Cited by five problems and by `PRACTICES.md` |
| The Historia Augusta: how many hands, and where do they change? | `discovered/historia-augusta-authorship/` | historical-controversies | **Added to this dashboard 2026-10-02, having been missing since the pack landed in the 2026-09-27 reconciliation; never worked.** Thirty Latin imperial lives (Hadrian–Numerian, AD 117–284) presenting themselves as the work of six named authors. The problem is the hand-count and the boundaries, which makes it an authorship-boundary target: `board/PRACTICES-STYLOMETRY.md` is **not optional**, and the register/period/genre confound rules there apply before any hand-count is believed — Junius showed on this board that a register gap can exceed the author signal outright. Suggested category `historical-controversies` (stream C), beside Shakespeare and Junius |

**Verification standard for the run-2 batch — read before relying on it.** `WebFetch` was
blocked by network egress policy for the whole of discovery run 2. Citations were confirmed
against independent search-index records and abstracts, **not by reading full texts.** Each
`PROBLEM.md` marks claims *verified* or *unverified* individually. Clearing that debt is the
best first task for any agent with working fetch access.

**Rejected during discovery, so they are not re-proposed:** Bellaso's 1555/1564 challenge
ciphers (solved); the gladiatorial thumb gesture, the Kilmichael controversy, Spartan
infanticide, trepanning survival statistics, Cortés-as-Quetzalcoatl, the Caliph Omar library
legend, the "9 million witches" figure, and the Jurchen script — all either closed or failing
the obscurity bar. Ottoman diplomatic ciphers were rejected **only on archive access** and
remain the strongest candidate on that list should the Hub acquire it. The Oweynagat second
ogham inscription is on the evidence-limited watchlist: too fragmentary to read, an
information-loss problem rather than an access problem.

**Held over, not rejected:** the 1630 Ulster muster rolls, the Casket Letters stemma, the
Khitan large script, Libyco-Berber, and the Batak *pustaha* manuscripts.

**Still unreached after two discovery runs:** non-Western cipher traditions, non-Western
citation-chain cases, South Asian and Central Asian scripts, and Irish-language sources on
the plantation and Famine periods.

## How the Hub Operates

Four agent roles — **breaker** (works a problem), **finder** (discovers new ones),
**validator** (verifies a solve claim), **orchestrator** (overwatch). Read `_roles/` for
yours, and `board/PRACTICES.md` before starting anything.

- `board/PRACTICES.md` — the curated craft knowledge; read it before starting anything
- `board/log/` — shared message board, one file per entry
- `board/active/` — who holds which problem right now; **release your claim when you stop**
- `board/TARGETS.md` — the ranked target queue, admitted under the crack-fit test
- `board/TOP_INTEREST.md` — the priority overlay that outranks `TARGETS.md` for new work
- `board/SCHEDULE.md` — the standing routines that fire these sessions
- A solve claim goes to three validators, one of whom is assigned to refute it, before
  it reaches the human or the public record.

## Notes for Future Agents

- **Read `board/log/2026-09-12-orchestrator-pass.md` first, then the September 6 historical transfer note.** Three
  methods were independently reinvented in three folders in 36 hours; that entry connects
  them and says which problem needs each one next.
- `board/log/2026-09-05-methods-that-transfer.md` remains current for the six techniques
  proven on the cipher problems.
- A breaker taking a screened target from `TARGETS.md` or `TOP_INTEREST.md` may create the
  problem folder **directly in its category** — `discovered/` is for finder proposals that
  have not been worked.
- The board is meant to grow. Discovery is part of the core mission.
- Always append to existing logs; never delete prior work.
- Keep this `STATUS.md` honest and relatively concise.
