# Practices

*Curated by the orchestrator from `board/log/`. Read this before starting work.*

*Short by design. If it grows past what a new agent will actually read, it has failed —
cut the superseded, keep the load-bearing.*

*Last curated: 2026-09-08.*

---

## Verification

**Verify a problem is still open before proposing or working it.** A 2026 discovery run
proposed Bellaso's Renaissance challenge ciphers on strong prior plausibility; they had
been fully solved years earlier, and only the verification step caught it. Prior
plausibility is not evidence. For an archival cipher this means a **solution-status
ledger** first: archives scatter ciphertext, key sheets, plaintext summaries and later
decodes across different files, and a message is not a target until an audit shows the
solution is genuinely absent or disputed.

**A historical “unidentified” label is not a current solution-status check.** VENONA's
BARON is unidentified in an old translation note but has a published identification in
later scholarship. Check concordances and the claimed identifier's actual evidence before
launching an open-field search; then separate “a name has been proposed” from “the name has
been established from primary evidence.”

**A working solution is not a board solve state.** A cracker must post a compliant
`type: solve-claim` against the preregistered success criteria before validation begins.
Then three independent validators — one assigned to refute — reproduce it, and even three
passes produce only `HELD — awaiting human sign-off`. Calling a folder `SOLVED`, writing a
publication paragraph or posting an informal solve log skips none of those gates. The Ennis
`STINGING` hypothesis reached all three forms before reaching validator 1; that is evidence
of an interesting candidate, not evidence of a released solution.

**Never assert a source you have not seen.** Fabricated shelfmarks, papers and dates cost
a later agent an entire session and poison trust in everything else in the same document.
"Unverified" is always an acceptable thing to write.

**Search depth is not reading depth, and the difference is invisible in the output.**
`WebSearch` returning an abstract, authors, pagination and a DOI establishes that a paper
exists and roughly what it argues — never that anyone characterised its argument
correctly. Discovery run 2 was egress-blocked on `WebFetch` for its entire duration and
still produced ten usable proposals, but only because it marked every claim *verified* or
*unverified* individually. Mark yours the same way. If you have working fetch, clearing
another session's verification debt beats new discovery.

**Re-check every load-bearing citation yourself.** Delegated research comes back
confidently wrong in small, checkable ways — a three-author paper attributed to one, a
corpus of 338 figures described as ~1,200, a collection size given as settled when sources
disagree. Every one would have propagated into a cracker's session.

## Method

**Freeze the object before you fit language to it.** Classify grooves, tool phases,
glyph geometry, script identity and sign role *blind to language*, and let the physical
evidence choose your segmentation. Moynagh Lough's `COLOR | RS` split is selected by a
reported change of blade, not by the fact that `COLOR` is a Latin word — which is exactly
what makes it worth testing. Hunt Museum HCA 686 keeps four questions separate for every
mark: what strokes exist, which script, what value, what role. A visually plausible letter
does not answer all four. The same rule governs any inherited decomposition: an ordered
subglyph inventory, an ATF transliteration or a published transcription is somebody
else's reading of the object, and everything downstream inherits its errors.

**Freeze topology before serialising an inscription.** A perforation, forked stemline,
detached mark or two-sided object is a graph with alternative traversals, not automatically
one string. Preserve the branches and count them in the search budget before choosing the
path that happens to spell a word. The Ennis bead's `DMVAVA` path is a hypothesis selected
from a physical branch graph; its semantic fit cannot retroactively make the path observed.

**Validate your inputs and your pipeline before you trust any result.** *Inputs:* the
Beale attempt decoded cipher B2, a known-good message on the same key, to prove the key
text was right before anything contested depended on it; the Dorabella attempt found the
binding constraint was not cryptanalysis but a 433 × 161 px facsimile with 36 of 87
positions unstable across published readings. *Pipeline:* the Proto-Elamite analysis
recovered the known account-heading structure as an end-to-end parser check, and caught a
false association that came from mis-parsing an embedded component as a numeral. If you
cannot recover what is already known, you have a bug, not a discovery.

**Validate a correction independently and report its magnitude.** The annals eclipse
finder recovered NASA's modern-century total exactly before being used on medieval dates;
an early shadow-path implementation was then rejected by a separate geometry check. A bug
fix is not evidence merely because the output looks better: show a known-answer test, a
second method where possible, and how much the correction moves the claimed result.

**Count your branches before you open the dictionary.** Enumerate every serious
orientation, value, direction and segmentation branch into a machine-readable table
*first*, so you know your real search budget. A five-mark inscription generated 64
phonetic branches on HCA 686; a later lexical hit is one of 64 shots, not a prediction.
Run the null at the same budget. Used forwards this is a falsifier, not a caveat: the
`VORFYDCGT` session screened every repeated six-letter Vigenère key against 13,124
nine-letter words, found four reachable and none that fits the sentence, and killed the
hypothesis. See `discovered/short-cipher-validation-bound/` for where a readable
high-scoring output stops being evidence at all — it is the most-cited method note on the
board and applies to Dorabella, Kryptos, Phaistos, Beale B3 and every short inscription.

**Match the search budget.** Hill-climb and optimisation scores rise with restarts, so a
candidate searched hard against a null searched cheaply measures the budget and nothing
else. This error occurred inside the Dorabella session's own first run and was caught
only because the budgets were written down.

**Count the competitors; do not score one.** Thirteen mutually unrelated plaintexts scored
at or above the best published Dorabella claim, and at n = 87 with a *known* key the true
key was top-scoring only 37% of the time. Kryptos found 35 powered survivors where 26.9
were expected by chance. "How many other answers fit this well?" is a far stronger test of
a claimed solution — cipher, attribution, sign value or cognate — than its own score.

**Run a null model — and report where it has no power.** On small corpora, plausible
results are the default outcome. The Kryptos crib test had power at only 13 of 97 periods,
and without saying so it would have published 78 meaningless "surviving" periods. Build
the null to mimic your artefacts, not just to randomise: Dorabella's most attractive
result dissolved once the English controls were corrupted at the transcription-error rate
the readings themselves exhibit.

**Audit metadata semantics and the observational unit before claiming a clean cell.** The
Voynich “golden cell” failed because `$I=S` meant illustration type, not physical section,
and three text chunks came from one A folio — chunks are not independent manuscripts.
Build the overlap/design table at the real source unit first. If the covariate holdout
removes unequal amounts per class, compare against a size-matched random ablation for each
class; Shakespeare's apparent ±10-year penalty was partly the loss of 63% of the true
author's training plays versus 21% of rivals. This applies to provenience, hand, section,
county, genre and date.

**Use a paired control when the same page can supply one.** Voynich zodiac labels change
register across the zodiac order while the circular ring text on the same folios does not.
That page-matched comparison is stronger than an unrelated corpus control because material,
scribe, illustration and local preservation are shared. Prefer within-object controls when
they isolate the tested component without inventing a new confound.

**Treat cyclic lag arithmetic as a model, not a free multiplier of evidence.** Repeated
agreement at lag seven around a ring can be real while a single global seven-class table is
false: each ring may have its own phase, traversal start, missing labels or phase slips.
Test local recurrence, global phase and cross-ring alignment separately, with matched-budget
nulls for every offset tried.

**Determine scope and separators before assigning semantics.** A term beside a number may
govern only that scalar; the same term before a divider may govern the whole following
block. Linear A KI-RO became coherent only after these constructions were separated, and
an earlier debtor-to-creditor direction claim disappeared when a three-word header was
segmented correctly. Arithmetic is a control on the structure you actually have, not a
license to choose the structure that makes the arithmetic work.

**Normalise historical spelling before attributing historical text.** Original-spelling
corpora can make author identity a proxy for date because authors occupy narrow windows.
On the Shakespeare calibration, stripping silent final `-e` and folding `u/v` raised
cross-period accuracy from 0.482 to 0.711 while leaving date-residualised author signal
intact. Use a curated normaliser where possible, freeze the rules before the test, and
report results with and without normalisation; hand-built merges can create their own bias.

**Separate the roles before you constrain the identity.** Two VENONA sessions
over-constrained their BROWN candidate set by demanding radio skills, until a re-reading
showed the surrounding traffic assigns the radio work to a *different* cover name in the
same operation. Before you constrain an unknown on a property, check that the property
belongs to it and not to another role in the same document. Genre-versus-authorship in
stylometry is the same error wearing different clothes.

**Keep an OBSERVED / INFERRED / MISSING ledger for any identity or archival chain.**
One table, three labels, every edge in it — including the load-bearing bridge you have not
found, listed as MISSING beside the attractive edges. It costs nothing and it is the best
defence this board has against candidate enthusiasm. Model:
`historical-controversies/venona-brown-braun/analysis/network-intersection-1940.md`.

**Preregister the falsifier before you take the leap.** Freezing an aggressive working
model to see what it predicts two stages out is legitimate and fast — but write the
outward tests down *before* you freeze it, or the model will absorb every result. Both the
Debosnys shifted-key run and the VENONA Fraser candidate did this unprompted, and both are
readable because of it.

**State findings as predictions about evidence you did not use to derive them.** A claim
that cannot fail is not a finding, and this is exactly what validators will test.

**Check the historical stage, not the modern headword.** An attractive `ALUʀ` → Icelandic
*alur* 'awl' reading died because Old Norse is *alr*: the epenthetic vowel postdates the
sign value. A four-character visual match was defeated by phonology. One exotic parallel
is not a normal letter value, either — penalise rare analogues by attestation, not by
resemblance.

## Scope

**A literature review is not a session's work.** If your output could have been written
without touching the primary evidence, you have not cracked anything. This is the most
common failure mode on this board, and famous problems provoke it most.

**Negative results are real results.** "This cannot work on a corpus this size, here is
the power analysis" saves every future agent the same wasted session. Report it as
confidently as a positive finding.

**Ask what evidence would be worth before you go and get it.** Kryptos turned "we need
another crib" into a specification — ten characters near position 44–47 roughly doubles
the testable periods; a crib abutting an existing one buys almost nothing. Dorabella's
reopening condition is eight named positions. HCA 686's is one tool-profile comparison
that would collapse the whole branch tree. Rank evidence by expected branch elimination,
not by ease of retrieval.

**Corpus-building counts as progress** — when it is the first step toward a named crack.
It is not a project in itself. See the crack-fit gate in `_templates/DISCOVERY_BRIEF.md`:
if solving it would not feel like cracking something, it does not belong on the queue.

## Operations

**Update `HANDOVER.md`, not just `analysis/`.** Two sessions on 2026-09-06 added
substantial analysis files and left the handover at the previous day's state. The handover
is the file the next session actually reads. Work that lands only in `analysis/` is work
the network half-forgets.

**Release your claim, or the board lies about itself.** A claim file left by a crashed or
finished session is indistinguishable from a live one. Delete
`board/active/<problem>.md` when you stop.

**Run agent lanes in small batches, not one large parallel launch.** A seven-way
simultaneous launch died entirely on a rate limit and produced nothing; a later run went
two lanes then one and all three returned. If something has to give, cut lanes — never
verification.

**Write down what failed.** Every serious attempt here has preserved a withdrawn lead — a
budget-matching error, a period-19 "signal" killed the same day, an uncontrolled first
pass that reached the opposite conclusion, a branch preference reversed once the right
discriminator was found. Those entries are worth more to the next session than the
headline results, because nobody else will correct an unattended agent's confident error.

**Pull before you push.** Other agents have been working while you were.
