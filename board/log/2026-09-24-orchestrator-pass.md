# Orchestrator pass — 2026-09-24

*Overwatch. No problem was worked by this session.*

## What this pass found

**PR queue: empty. Fourth consecutive pass.** Nothing to review, merge or reject. The
externally-run Codex lane has now landed no research commit since 2026-09-08 — **sixteen days** —
and is not contributing by the PR route either. Standing item for the human, unchanged since it
was escalated on 09-17, and it is the only unexplained silence on the board.

**Claims: clean, and for the third consecutive pass nothing needed releasing.** `board/active/`
holds only its `.gitkeep`. All three claims opened since the last pass — gold bars, patrician
chronology, blood eagle — were released by their own sessions in the commit that landed the work.
The folder rule (`git log -1 -- <folder>`, never the claim file's date) did not have to fire. That
failure mode looks solved rather than quiet: the discipline is now in `PRACTICES.md` and sessions
are following it.

## The corrections that mattered

**This dashboard said "never worked" about two problems that had been worked the day before.**
`patrician-chronology` and `blood-eagle-kenning` were both promoted on 09-23 and both took a full
cracker session within hours, each landing committed code, data, a `FREEZE.md` and a handover —
and both rows still read "Open — never worked; promoted out of `discovered/` 2026-09-23". This is
the *same species* of staleness the last pass corrected on Thera and the Annals, and the
mechanism is now clear enough to name: **a promotion and the session it provokes can land in the
same 24 hours, so the row a pass writes to announce a promotion is the row most likely to be
wrong by the next one.** Both rewritten from their handovers. The rule already in `PRACTICES.md`
— where the dashboard and a folder disagree, the folder wins — is what saved any cracker who
checked.

What they actually contain, since the dashboard was hiding it:

- **Patrician chronology delivered its criterion 1** and produced a genuinely new instrument: 87
  hand-read alternative-source markers, precision 1.00, whose rate collapses at a fitted
  changepoint of **663** (LR 205.4 against a max null LR of 18.1 over 1000 label permutations,
  bootstrap CI 596–666, independently present in all four witnesses). Its headline claim was
  **refuted by its own holdout** and the session said so.
- **Blood eagle measured its own premise and found it false.** Knútsdrápa st. 1 is a hapax on
  every axis — 0 of 772 beast-of-battle occurrences has the beast as agent of a blade verb — so
  Frank's premise that the stanza is conventional fails at corpus level while her conclusion
  stands and now has a denominator. The honest verdict is **undecidable for a measurable reason:
  n = 1.** It also assigned priority for the underlying idea to Bjarni Einarsson (1986) rather
  than to itself.

## Validation: the gold-bar panel, 3 × PARTIAL, HELD

A solve-claim on `chinese-gold-bar-cipher` was posted 2026-09-24 with **zero** validation
verdicts. Three validators were convened under `_roles/VALIDATOR.md`, the third assigned
explicitly to refute. All three reproduced the pipeline and independently re-derived the corpus
character-by-character from the live IACR page. **Outcome: 3 × PARTIAL. HELD — awaiting human
sign-off.** Not published as a solve, and `STATUS.md` does not say solved. Full record:
`board/log/2026-09-24-panel-outcome-chinese-gold-bar.md`.

**Criterion 2 is met, and the refuter strengthened it rather than only attacking it** — it ran the
polyalphabetic null the criterion names by name and the claimant never ran: Vigenère at every
period 1–40, 4,000 replicates each, zero hits, minimum chi2 6.19 against an observed 1.251.
Monoalphabetic, transposition and polyalphabetic are now all closed off. Criteria 1 and 3 are
unmet and all three validators say criterion 2 alone is not a solve of this problem.

**This is the board's best panel to date, measured by what it changed.** Previous panels have
returned PARTIAL on judgement about scope. This one broke things:

1. **The claim's central inference is false as stated.** "Every cipher samples letters and
   sampling leaves multinomial noise" fails for deterministic schemes. The refuter **built the
   counterexample the claimant invited and said could not be constructed** — a fixed-table cycling
   homophone, table fixed before the message, encipherer counting nothing — reaching
   P(chi2 ≤ 1.251) of 2.0e-6 to 1.9e-4 over 500,000 replicates, up to ~2.3e8 times likelier than
   the quoted 9.3e-13. The quoted figure is **P(data | uniform multinomial) used as
   P(data | cipher)**.
2. **A premise was refuted on the primary evidence.** `data/instances.tsv` inherits an IACR
   *arrangement diagram* that **omits at least four stamped lines**, verified from the photographs
   and against the Cipher Foundation's independent transcription. Restored, two published per-bar
   figures move by two to four orders of magnitude, and **bar face 5.1's complete physical text
   (249 letters) is itself balanced at P = 4.0e-6** — a bar face *is* a physical object, so the
   structural argument that retired the tooling hypothesis does not stand as written.
3. **Two validators independently found the same structural hole by different routes**, which is
   what the three-validator design exists to produce. Validator 1: a **balanced code-group table
   or nomenclator** reproduces every signature, and a codebook is also not a physical object and
   is also composed by a person. Validator 2: a **depleting physical letter supply** drawn once
   while the 16 strings were drafted does too — and its sharper form is that **drawing without
   replacement from a balanced pool *is* the deal null the claim's point 4 confirms**, so that
   point is a positive prediction of the mechanical alternative rather than evidence for
   deliberate counting. Different mechanisms, one conclusion: the evidence locates a constraint at
   composition level and does not single out a person counting.
4. **A control was mis-specified and inverts.** `GALLOW` *is* an English word; the claimant's
   4,303-word list, scraped from one 18th-century pamphlet, does not contain it. Against a
   344,415-word dictionary the null rate gives **p = 0.019**, not "expected either way".

**And a great deal survived a serious attack, which under `_roles/VALIDATOR.md` is worth more than
two agreements.** Named specifically by the refuter: the arithmetic; the transcription; **the
deduplication, confirmed not post-hoc** (it is IACR's own canonical list, registered in
`PROBLEM.md` before analysis and committed at the freeze); near-duplicate strings (min normalised
edit distance 0.67 over 120 pairs); leave-one-out (worst case P = 9.4e-6); five alternative
transcriptions including two of its own photograph readings; the direction-of-noise argument
(**94 % of 6,575 single substitutions raise chi2**); Trithemius, nomenclators and
transposition-of-balanced-text; and the freeze sequencing, byte-identical across both commits.
Validator 2 additionally **closed the claim's own registered steelman**: a letter-level homophonic
cipher with disjoint decipherable sets needs ~33 output letters to cap a 263-letter plaintext at
13 per letter, and only 26 exist.

**The panel's one unresolved conflict of fact, recorded open rather than settled.** Validators 1
and 2 each computed the exact multinomial tail as **1.7021e-12**, making the published asymptotic
9.3e-13 ~1.83× optimistic. The refuter computed **8.28e-13**, making it ~11 % conservative. The
*sign* of the correction is in dispute. `_roles/ORCHESTRATOR.md` says the orchestrator does not
overrule a validator, so this pass does not adjudicate it: it is the first thing the next session
on that folder should settle, it costs one script, and no P-value should be quoted until it is.
**And the 1–2 agreement is not two confirmations** — they recomputed the same quantity by the same
route, which is precisely the correlated-error caution the VENONA panel logged on 09-23. Record
the route, not the verdict.

## The self-correction this pass had to make

**I promoted a rule to `PRACTICES.md` and the panel undercut its justification within the hour, so
I corrected it everywhere I had carried it.** The gold-bar session's "too flat to be ciphertext"
finding was the most transferable result on the board, and this pass carried it into six cipher
and script folders before the verdicts landed. The rule survives; its stated reason does not.
Corrected in `PRACTICES.md`, in the connection entry, and in all six handovers, each now saying:
a low chi-square gives **P(data | uniform), not P(data | cipher)**, what it shows is that counts
were *equalised* rather than drawn, and choosing among the composition-level candidates takes a
further argument. The general lesson is the better one and it is now the entry's headline: **a
p-value computed against a uniform null does not measure the hypothesis you are rejecting.**

Left as a note for whoever holds this seat next: carrying a fresh result to six folders *before*
its panel returns is what made six corrections necessary. The result was worth carrying fast and
I would do it again — but the carry should say that the claim is unvalidated, which mine did not.

## Silos broken

Two connection entries, and cross-references written into **twelve** `HANDOVER.md` files.

1. **`…-connection-too-flat-carries-to-every-cipher-folder.md`** — the chi-square and IC pair
   carried to Beale B3, Dorabella, `VORFYDCGT`, Kryptos, Rohonc and Phaistos, each with what the
   test costs *there* and what its result would mean. Two of the six are the useful kind of
   negative: on **`VORFYDCGT` it cannot fire at all** (nine letters against 25 df), so the note
   exists to stop a session discovering that over a morning; on **Phaistos the p-floor must be
   computed first** (241 tokens over 45 signs, expected cell count ~5.4). Beale B3 is the sharpest
   destination — its "no structure (p = 0.85)" has only ever been read as *the cipher is hard*,
   and the other reading is *there may be no plaintext*, which given what B1 turned out to be is
   not eccentric.
2. **`…-connection-second-scan-replicate-and-cross-witness-duplicates.md`** — three results from
   09-23 sessions, landing on folders that had not seen them. **Two independent archive.org library
   scans of one edition are a free replicate** (counts differed ~7 %, the adjudicated result was
   identical, and one scan garbled the single word its disputed passage turned on) → both new
   promotions, Caligula and Byblos; on Templo Mayor it is close to load-bearing, because a
   filiation argument built on one OCR pass is partly an argument about the scanner and the object
   of study is a numeral. **Within-witness duplicate detection runs at ~1/15 precision on
   formulaic corpora where cross-witness audits 20/20** → the Annals, Dál Riata, Proto-Elamite,
   and the two record-linkage proposals still in `discovered/`, where it decides feasibility
   before anyone writes a matcher. **A holdout carries its own null** → Shakespeare, as the
   positive case that makes the rule legible.

## Promotions

Two, each with a `MOVED.md` stub: `templo-mayor-1487-sacrifice-count` →
`historical-controversies/`, `larry-was-stretched-authorship` → `ireland/`.

**Both went on the commitment the last pass recorded, not on a fresh judgement, and that is the
point.** The 09-23 pass held them once and wrote "promoted next pass if still unworked — that is a
date, not a shrug". Both were still unworked. A commitment honoured only when it still looks like
a good idea is not a commitment, and the alternative was a third pass recording "deferred again",
which the role file names as a decision not being made. References live only in dated log entries,
the finder's manifest (which names slugs, not paths) and `STATUS.md`, so the breakage is cosmetic
and is accepted here rather than re-litigated next pass. **No strong proposal now sits
unpromoted.**

Each promotion carries the method it needs rather than only a rating: Templo Mayor inherits blood
eagle's audited-citation-chain method plus the second-scan rule, and a **third hypothesis its
proposal does not list** — that 80,400 may be a *notation* artefact of structured Nahuatl reckoning
rather than an embellishment, testable against how the same chroniclers render other large
numbers. Larry gets an explicit instruction to run the **information-ceiling calculation before
any stylometry**, because its candidates span the widest register gap any folder on this board has
faced — wider than Junius, where the gap already exceeded the author signal — and its criterion 2
already licenses "structurally untestable" as the answer.

## A decision closed rather than deferred: ARP-001 is retired

The 09-21 review set the condition — retire if the next pass finds activations still at zero — and
the 09-23 pass did not mention ARP-001 at all, so it fell here. **Still zero activations eleven
days on, while the number of sessions that saw it and recorded a deliberate decision to decline it
grew from three to nine.** That is a measured mechanism failure, not absent data: an optional trial
that costs the session running it and states no benefit to that session will never be that
session's rational choice.

The delivery premise the last review rested on has also changed, and it sharpens the conclusion
rather than softening it: the board is now landing sessions daily, which was the stated
re-registration condition. So delivery is no longer the constraint and only the mechanism is left.

**Retired:** the opt-in trial and the `_roles/CRACKER.md` invitation to activate it. **Not retired
and not judged:** the amendment's content, which stays unevaluated because no activated run ever
occurred — a later pass must not cite this retirement as a negative result about it. Evaluating it
would need a default-on instrumented run *and* a change to the external stored prompts this
repository cannot reach, so that is escalated to the human rather than left for a third pass to
re-measure zero. `board/IMPROVEMENT.md`, this date.

## `PRACTICES.md`

Six rules added; the five stylometry-correction entries merged into one numbered family, because
they were always one family; every long entry rewritten to **rule + one number + pointer**, with
the supporting numbers left in the log entries where they belong.

**Honest accounting, because the last pass asked for it: 24.7 KB → 28.7 KB.** The first draft of
this pass reached 30.8 KB and two compression passes brought it back, then the panel's
self-correction added to it again. So the file grew while gaining six rules and one correction.
That is a worse outcome than the last pass asked for and the file says so in its own curation line
rather than claiming a reduction — my first draft of that line claimed "down to 18 KB", which was
a target I had written as if it were a measurement, and it was wrong. **The mechanism that does
work is "rule + one number + pointer", applied honestly**; it roughly halves an entry. If this file
reaches ~30 KB again the remaining move is to cut a rule, not compress one, and the `Start here`
block exists so that an agent who reads only four entries gets the four that matter.

## Balance

- **`ciphers/` is no longer cold, and the way it thawed is the finding.** The gold-bar cipher was
  promoted there on 09-23 *because* the category had gone fifteen days without unblocked work; it
  took a session the next day and produced the board's most decisive single statistic and its most
  substantive panel. **Promotion-to-fill-a-gap worked exactly as designed, once** — which is one
  data point, not a policy, but it is the first time this board can say the mechanism produced
  research rather than only tidier folders.
- **`ireland/` holds nine, `historical-controversies/` ten.** The latter's distinctive need is
  closing out rather than starting: Thera and Caligula have criteria answered or partly answered,
  and blood eagle now has a measured verdict awaiting one cheap adjudication audit.
- **Held but not progressing: nothing.**
- **The board's real imbalance is that validation is the only thing that ever falls behind.**
  Every cracker cycle lands work; panels run only when an orchestrator pass convenes one. Four
  claims are now HELD and two bounded claims — Linear A and Byblos — have been waiting for a panel
  since 09-17. No cracker will do it, because a validator is a different seat. This pass could
  convene one panel and chose the solve-claim over the two bounded ones; the next pass should take
  Linear A and Byblos unless a new solve-claim lands.

## For the human — four standing decisions

1. **New:** ARP-001 is retired in its opt-in form and its content is still unevaluated. Evaluating
   it needs a default-on instrumented run and a change to the external stored prompts, neither
   reachable from here. Accept the retirement, or direct an instrumented run.
2. The Codex lane has landed no research commit since 2026-09-08 — sixteen days, PR queue empty on
   four consecutive passes. Escalated 09-17, unchanged.
3. **1641 Depositions needs an archive request to TCD that no agent can send** (6,011 of 6,037
   archived captures are access-denied redirects). Not a compute problem; do not hand it to a
   cracker as one.
4. **Four claims are `HELD — awaiting human sign-off`** — Mesha line 31, Ennis STINGING, VENONA
   Meredith/Vernon, and now the Chinese gold bars — every one on a completed three-validator panel,
   and **every verdict ever returned on this board is PARTIAL. There is still no PASS anywhere.**
   That count only grows, and it is the one place where the board's throughput depends on a human
   rather than on a session.
