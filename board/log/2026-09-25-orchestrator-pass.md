# Orchestrator pass — 2026-09-25

*Overwatch. No problem was worked by this session.*

## PR queue: empty, sixth consecutive pass

Nothing to review, merge or reject. The externally-run Codex lane has now landed no research
commit since **2026-09-08 — seventeen days** — and is not contributing by the pull-request route
either. Escalated to the human on 09-17 and unchanged since. It remains the only unexplained
silence on the board, and it is the one item on this page that no orchestrator pass can move.

## Claims: clean, fourth consecutive pass

`board/active/` holds only its `.gitkeep`. All four sessions since the last pass — Templo Mayor,
Larry, Phaistos and the gold-bar repair — released their own claim in the commit that landed the
work. The folder rule (`git log -1 --date=iso -- <problem folder>`, never the claim file's date)
was run against every category folder and did not have to fire. Nothing was released, because
nothing needed releasing.

This failure mode now looks genuinely solved rather than quietly absent: the discipline is in
`PRACTICES.md`, four consecutive passes have found nothing to clear, and the sessions are doing it
unprompted.

## The correction that mattered: the board state was two passes stale

**`STATUS.md`'s entire "Board state" section was still the 2026-09-23 pass's text.** It said "PR
queue empty, third consecutive pass" (it was the fifth), "Codex silent fifteen days" (seventeen),
and "four proposals promoted" (nine by then). The 09-24 pass corrected individual problem rows —
correctly, and that was the right call under time — and left the narrative section alone.

**That is a distinct rot from the one the last two passes caught, and it is worth naming.** The
09-24 failure was *a row saying "never worked" about a problem worked the day before*: a fact
going stale. This one is *a whole section describing a board that no longer exists*, and it is
more dangerous, because a row is read by whoever is about to work that problem and gets checked
against the folder, while the board-state section is read by everyone and checked against nothing.
Rewritten in full, with a dated note at the top saying it was rewritten and why, so the next pass
can tell at a glance whether it has happened again.

**And it had already caused the exact harm the file warns about.** Priority 1 under *Next-session
priorities* still read "Templo Mayor and Larry Was Stretched — the two cheapest unworked starts",
a full day after both were worked to completion. That is the *second* time this page has
recommended a closed route as its top priority; the first, Junius on 09-21, is memorialised in
`PRACTICES.md` as "where this page and a handover disagree, the folder wins". The rule worked —
neither problem was re-run — but the rule exists to catch a mistake, not to excuse repeating it.
Priority 1 is rewritten, and it now names the failure in its own preamble.

## The gold-bar repair loop closed, and that is a first for this board

The 09-24 panel returned 3 × PARTIAL on `chinese-gold-bar-cipher` with six named repair items. A
session took four of them **within 24 hours**, and the board has never before had a claim repaired
against its own validation panel. What came back:

- **The panel's one unresolved conflict of fact is settled.** The 09-24 pass declined to
  adjudicate it — three validators had produced three numbers and disagreed about the *sign* of
  the correction — and made it repair item 1. The exact multinomial tail is **1.7020973493e-12**,
  by two independent exact-integer algorithms with a third slower one agreeing. Validators 1 and 2
  were right; the refuter's 8.28e-13 was the more optimistic of the two figures. **Declining to
  adjudicate was the correct call and it cost nothing** — the folder settled it in one script,
  which an orchestrator ruling would have pre-empted with a coin flip.
- **A premise was repaired by going back to the object.** The corpus was re-read off the
  photographs: **261 letters, not 263**, both disputed strings read as 13 glyphs on three
  stampings each, and an instance table of **88 stamped lines against IACR's published 44**, with
  three faces nobody — IACR included — had ever transcribed.
- **The session's own frozen prediction failed and it led with that.** The 09-24 attempt predicted
  a corrected reading would move the deviant letters *toward* ten; the metal moves two of them
  away. Reported as the headline of its own repair.
- **Pillar 3 is repaired rather than withdrawn, and the repair is the transferable result.** The
  refuter was factually right that a bar face is itself balanced (P = 7.4e-6). Conditioning on the
  inventory and the face's own layout, every face sits inside the null and face 5.1 lands at
  **p = 0.598 — dead centre**. The balance is 100 % inherited.

**The claim stays `HELD — awaiting human sign-off` at 3 × PARTIAL.** Criteria 1 and 3 are still
unmet, repair items 5 and 6 are untouched, and nothing is published as solved anywhere. What the
repair changed is the quality of the held claim, not its status — and `STATUS.md`'s validation-queue
row, whose "decisive missing check" column had been discharged in full, now names criterion 3 and
the length-stratified reuse test instead.

## Silos broken: nine handovers, one connection entry

`board/log/2026-09-25-connection-exact-tails-inherited-structure-and-audited-comparanda.md`. Three
results from the two 09-25 sessions, each landing on folders that had not seen them.

1. **A balance p-value is a counting problem, not an integration problem.** chi2 is a strictly
   increasing function of an integer, so the lower tail is a finite enumeration. **The most useful
   destination is a negative**: `ciphers/ira-vorfydcgt-1923/` was told on 09-24 that the flatness
   test cannot fire there (nine letters against 25 df). That was right as an asymptotic, and at
   n = 9 the *entire* distribution is enumerable, so the folder can now state the minimum
   attainable chi-square and its exact probability — a closed-form bound on what any flatness
   argument could ever establish there, replacing a hunch with a documented dead end for one
   function call. Also to Phaistos (its p-floor is exact, not simulated), Beale B3 and Blitz.
   Carried with it: **a 20,000-draw Monte Carlo cannot resolve anything below 5e-5**, so any
   headline below that is an approximation somebody must name.
2. **A structured sub-object is not independent evidence until you condition on the level above
   it.** The generalisation of the pillar-3 repair, and it has a textual form that matters more
   here than the statistical one: **a witness that looks independent because it reproduces a
   pattern may be copying the pattern.** Carried to Phaistos pre-emptively (its next obvious move
   is to report that some side or spiral arm is also formulaic — that number would be inherited),
   to Proto-Elamite (which already does this, blocking on `(tablet, face)`, and should say so), and
   to `ireland/patrician-chronology/` and `ireland/early-irish-annals-reliability/`, where the
   four-witness independence the changepoint rests on is exactly the assumption at risk, and where
   the 09-23 holdout already caught one instance in the Four Masters' silent 35-year duplication.
3. **The comparandum is the least-audited object in a session.** The Phaistos session's first
   three numbers all pointed the way its frozen prediction wanted and all three were artifacts of
   its comparison corpora. Carried to Dorabella — whose strongest and most-cited result *is* a
   comparandum, thirteen unrelated plaintexts scoring at or above the best published claim — and
   to Shakespeare and Junius, where the reference corpus is now the most plausible place for a
   strong result to be wrong.

**One thing this pass deliberately did not do.** The 09-24 pass carried a fresh result to six
folders before its panel returned and had to issue six corrections; its note to the next holder was
that the carry should say the claim is unvalidated. Everything carried this pass is either
post-panel (items 1 and 2, from the repair that answered the panel) or a methodological finding
with no claim attached (item 3). Nothing here is waiting on a verdict.

## Promotions: three, and the residual queue is closed rather than deferred

Each with a `MOVED.md` stub, and each carrying into its `HANDOVER.md` the specific method that
makes it cheaper rather than a tractability rating.

- **`blitz-ciphers` → `ciphers/`.** The strongest promotion available this pass. Its criterion 1
  asks for an authenticity verdict from internal statistics benchmarked against genuine ciphers
  and deliberate fakes, and says outright that *building that benchmark is the real work*. The
  gold-bar sessions just built most of it. This is the (c) limb of the promotion rule — something
  on the board has made it materially cheaper — and it is the cleanest instance the board has had.
- **`meroitic-language` → `historical-texts/`.** On the "passed over three times" clause: it has
  been well-formed and unworked since 2026-09-04 and passed over on every pass since. It also
  fills the board's total absence of an African script. Its handover carries the trap that will
  otherwise eat its criterion 2 — the 09-25 Linear A finding that the shortest, most frequent
  units in a formulaic administrative corpus are abbreviations and commodity marks, not words.
- **`black-death-mortality-figure` → `historical-controversies/`.** Blood eagle and Templo Mayor
  have now run its criterion 1 twice between them, and Templo Mayor supplies the hypothesis its
  proposal omits: a big round number may be a **notation** artefact rather than a count or an
  embellishment. Its handover also carries the scope warning this problem invites, because a
  survey of what historians have said about the Black Death is a literature review.

References to all three lived only in dated log entries and `STATUS.md`, so the breakage is
cosmetic and is accepted here rather than re-litigated.

**And the decision the last three passes kept postponing is made.** Every remaining pack in
`discovered/` has been passed over more than three times, which under the board's own rule makes
them all promotable — and promoting them all would be tidying, because **promotion does not create
sessions**. So `STATUS.md` now carries a **standing per-category draw order** with a named trigger
(a category with no unblocked new work for ten days), explicitly a default rather than a lock: a
specific enabling reason always outranks it. Two items are closed outright rather than queued —
`cypro-minoan` is **evidence-blocked, not low-tractability**, and belongs with the 1641 Depositions
archive request as a standing item no cracker can discharge; `ormonde-maltravers` was solved
externally and is an audit trail. Recorded in `board/IMPROVEMENT.md` with the condition under which
the queue should be deleted: **two consecutive passes promoting out of order.**

## `PRACTICES.md`: three rules added, none cut, and a mechanism to replace cutting

The previous curator left an instruction with teeth: compression is exhausted, so at ~30 KB **cut a
rule rather than compress one**. Three rules earned promotion this pass and no rule in the file was
untrue, so the instruction as written required destroying something correct.

**The move instead: a specialist family gets its own annexe.** The five-rule stylometry and
confound family — the largest block in the file, and specialist rather than general — is now
`board/PRACTICES-STYLOMETRY.md`, pointed at from `Start here` and from the four folders it serves.
4.4 KB left the file every new agent reads and not a word of craft was lost. Those rules are among
the best-earned on this board; two of the four problems that produced them found the confound
*larger* than the signal, and deleting them to hit a number would have been vandalism.

**Honest accounting: 28.6 KB → 30.2 KB, plus a 5.6 KB annexe.** It grew by 1.6 KB while gaining
three rules, two fold-ins and a longer `Start here`. Also cut: the previous curator's
two-paragraph accounting block, which was about a pass rather than about craft; the
paywalled-footnote technique, the narrowest item in the file; and the too-flat entry's same-day
self-correction, which is settled fact now and reads as one rule rather than a rule plus its
retraction.

**The contrary case, recorded because it is real:** this is how a second unreadable log gets
started, which `_roles/ORCHESTRATOR.md` names as the failure mode of `PRACTICES.md` itself. The
mechanism is safe only while annexes are few, named in `Start here`, and addressed to identifiable
folders. Cost limit set at **three annexes ever**; failure condition recorded in
`board/IMPROVEMENT.md`.

Added: the exact-tail rule; the inherited-structure rule; and *audit your source corpora*, which is
now entry 5 of `Start here` because it is the newest way sessions here go wrong. Folded in rather
than added: the DOI resolution of a too-precise citation — the completion of the 09-24 fabrication
tell, and the useful half of it, since **the same single call distinguishes "invented" from "you
have been scooped"** and both are worth knowing before writing a novelty claim; and validating a
measurement instrument on answers you already know, which killed a pixel-measurement approach in
ten minutes.

## Policy

**No policy trial is active, and none is opened.** ARP-001 stays retired in its opt-in form and its
content stays unevaluated; that is a human decision and this pass does not re-open it. The two
mechanisms installed above are changes to the shape of files the orchestrator already owns, not
trials, and neither asks any session to do anything extra. Both are recorded in
`board/IMPROVEMENT.md` with supporting case, contrary case, cost limit and failure condition.
