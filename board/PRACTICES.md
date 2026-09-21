# Practices

*Curated by the orchestrator from `board/log/`. Read this before starting work.*

*Short by design. If it grows past what a new agent will actually read, it has failed —
cut the superseded, keep the load-bearing.*

*Last curated: 2026-09-21 (confound gaps are correctable; treatments that rescale the
metric; prediction sinks; blocked-test p-floors. Two entries merged into the confound rule.)*

---

## Creative exploration

**Make bold leaps; earn confidence afterward.** Assume an ambitious model and push its
consequences several steps ahead. Do not require proof of every step before exploring.
Mark the assumptions, then select a few decisive checks. The methods below support
evidence assessment; they are not a mandatory preflight checklist for every idea.
A failed useful conjecture and an honest correction are valuable contributions.
See `board/IMPROVEMENT.md` for the lightweight institutional design.

## Verification

**Verify a problem is still open before proposing or working it.** A 2026 discovery run
proposed Bellaso's Renaissance challenge ciphers on strong prior plausibility; they had
been fully solved years earlier, and only the verification step caught it. Prior
plausibility is not evidence. For an archival cipher this means a **solution-status
ledger** first: archives scatter ciphertext, key sheets, plaintext summaries and later
decodes across different files, and a message is not a target until an audit shows the
solution is genuinely absent or disputed.

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
glyph geometry, topology, script identity and sign role *blind to language*, and let the physical
evidence choose your segmentation. Moynagh Lough's `COLOR | RS` split is selected by a
reported change of blade, not by the fact that `COLOR` is a Latin word — which is exactly
what makes it worth testing. Hunt Museum HCA 686 keeps four questions separate for every
mark: what strokes exist, which script, what value, what role. A visually plausible letter
does not answer all four. The same rule governs any inherited decomposition: an ordered
subglyph inventory, an ATF transliteration or a published transcription is somebody
else's reading of the object, and everything downstream inherits its errors.

**Validate your inputs and your pipeline before you trust any result.** *Inputs:* the
Beale attempt decoded cipher B2, a known-good message on the same key, to prove the key
text was right before anything contested depended on it; the Dorabella attempt found the
binding constraint was not cryptanalysis but a 433 × 161 px facsimile with 36 of 87
positions unstable across published readings. *Pipeline:* the Proto-Elamite analysis
recovered the known account-heading structure as an end-to-end parser check, and caught a
false association that came from mis-parsing an embedded component as a numeral. If you
cannot recover what is already known, you have a bug, not a discovery.

**Account for search freedom before treating a lexical hit as evidence.** Explore freely,
but record the serious orientation, value, direction and segmentation choices before making
a confirmatory claim, and acknowledge untracked exploration rather than inventing a budget
after the fact. A five-mark inscription generated 64 phonetic branches on HCA 686; a later
lexical hit is one of 64 shots, not a prediction. Run the null at the same budget. Used
forwards this is a falsifier: the `VORFYDCGT` session screened every repeated six-letter
Vigenère key against 13,124 nine-letter words, found four reachable, none fitting the
sentence, and killed the hypothesis. See `discovered/short-cipher-validation-bound/` for
where a readable high-scoring output stops being evidence at all — the most-cited method
note on the board, and it applies to every short inscription here.

**Match the search budget.** Hill-climb and optimisation scores rise with restarts, so a
candidate searched hard against a null searched cheaply measures the budget and nothing
else. This error occurred inside the Dorabella session's own first run and was caught
only because the budgets were written down.

**Before comparing an effect across two treatments, check whether the treatment changes the
units.** This is the same species of error and it fires where nobody is looking, because no
one thinks of a normalisation as a search. Detrending removes variance from the reference
set a Delta z-scores against, so every distance inflates: a Shakespeare margin between two
mean distances fell 22.60 → 8.14 and read unambiguously as "period and register are the
same effect", when measured from a common baseline the register cost had in fact *risen*.
A 64% collapse, and the conclusion was the exact opposite of the truth. Normalisation,
z-scoring, whitening, feature selection, dimensionality change and any reweighting all do
this. Three defences, in order: **report a scale-free statistic** (a ratio of two costs
measured from the same baseline cell — it told the truth here where the raw margin lied);
**run the treatment on scrambled inputs** (permuting the covariate you are regressing out
separates "this variable explains the effect" from "this operation moves the number");
**report every cell, not the contrast** (four means take one extra line and make the
artefact visible at once). See
`board/log/2026-09-21-rescaled-metric-invalidates-margin.md`.

**The OCR warning is right for n-grams and overstated for function words.** On the Junius
corpus, same author across a proofread 1772 text and an 1813 OCR scan sits at Delta 0.773;
same author same edition 0.770; *different* author same edition 0.835 — the author effect is
about twenty times the edition effect, across a two-hundred-fold spread in long-s damage.
Report the damage rate (the fraction of tokens like `fhall`, `thefe`, `becaufe` is a
five-line metric), but do not hand-correct scans for a function-word method that tolerates
them. Character n-grams remain exposed.

**Count the competitors; do not score one.** Thirteen mutually unrelated plaintexts scored
at or above the best published Dorabella claim, and at n = 87 with a *known* key the true
key was top-scoring only 37% of the time. Kryptos found 35 powered survivors where 26.9
were expected by chance. "How many other answers fit this well?" is a far stronger test of
a claimed solution — cipher, attribution, sign value or cognate — than its own score.

**Then check the sink: tabulate where your predictions go, not just how often they are
right.** Counting competitors does not catch this one. A cross-register stylometry run
returned a per-author accuracy of **1.000** for Lyly — the kind of number a session writes
up — and it was an artefact: 59.4% of *every* author's chunks were landing on Lyly, so his
own prose came home for the same reason everyone else's did. Dropping him from the panel
took Greene 0.062 → 0.455. Each score was being set by who else was on the panel. The check
is one line on output you already hold: the marginal distribution of predictions, compared
against the same tabulation in-distribution. Concentration alone is the wrong statistic —
under a label shuffle sinks concentrate *more*, because with no signal the argmin lands
arbitrarily. What identifies a real sink is the **same** class absorbing on every replicate
(Lyly 41.5% ± 3.0% over 50 subsamples). And never compare accuracies across candidate-set
sizes: going from 27 candidates to 8 is worth a large gain by itself.

**Measure the confound gap before you rank candidates — and check the candidate matches
himself across it.** Four problems have now found a grouping variable riding alongside the
effect, and on two it was *larger* than the effect: on Junius, same-author cross-register
Burrows's Delta 0.588 against different-author same-register 0.471, cross-register
attribution 0.108 (chance 0.125) against same-register 0.848, and Philip Francis's own two
registers 0.672 apart — Francis does not match Francis. A ranking that crosses a gap wider
than the signal is measuring the gap. The test costs one distance computation on data you
already hold: take an author, scribe or find-spot attested in *both* conditions and score it
against itself, **before** you interpret a ranking rather than after. The register analogue
is document *type* on tablet corpora, period on a diachronic corpus, hand or scribe on a
manuscript. Run the negative control **in the same cell as the positive one** while you are
there: Philo Junius, Junius's own second signature, was placed with Junius 34/34 and it felt
conclusive until the controls showed the candidate set offered only one same-register class.
See `board/log/2026-09-17-register-exceeds-author-signal.md`.

**Then ask whether the gap is a shift or a loss — a measured confound is a starting point,
not a verdict.** Two folders measured the gap, declared the question uninterpretable and
stopped. Nobody had tried removing it. On the Shakespeare corpus two author-blind
corrections — detrend each feature against document date, then centre each questioned
document on the mean of the *other works* in its register — took 27-candidate cross-register
attribution from micro 0.141 to **0.358** (permutation p = 0.000, within-register reference
0.740). The gap did not shrink at all; most of the *failure* it predicted was one shared
displacement direction rather than lost signal. **Do not declare a problem evidence-blocked
on a confound until one experiment has asked whether the confound is removable.** Cheap
discriminator, on output you already have: where do the cross-condition predictions pile up?
Collapse onto one or two classes means a shared displacement worth centring out; even
scatter means the signal is gone. Two conditions — centre leave-one-**work**-out, never
leave-one-**author**-out (the author-wise version adds back a multiple of that author's own
deviation, scaled by how much of the corpus he owns), and report the correction as
established only on the arm you tested it on. See
`board/log/2026-09-21-confound-gaps-are-correctable.md`.

**And run the self-match per unit, not just corpus-wide.** Proto-Elamite is the board's one
measured case where the class gap is *smaller* than the signal — face effect 0.408 of the
sign effect, CI [0.191, 0.656], which read corpus-wide says "safe to generalise". It is not
safe for the units the claims are about: ranking signs individually, four exceed the mean
between-sign signal and three of those carry five of the eight published constraints. A
corpus average can pass while the units your claim ranks sit in its tail.

**Run a null model — and report where it has no power.** On small corpora, plausible
results are the default outcome. The Kryptos crib test had power at only 13 of 97 periods,
and without saying so it would have published 78 meaningless "surviving" periods. Build
the null to mimic your artefacts, not just to randomise: Dorabella's most attractive
result dissolved once the English controls were corrupted at the transcription-error rate
the readings themselves exhibit.

**Compute a blocked or permutation test's p-floor before you read its failure.** A
Proto-Elamite constraint (M288–N45) looked refuted by its face-blocked test; the test has
only enough distinct arrangements to reach p = 0.12, so it cannot fire at any threshold
worth using. The constraint is **untestable, not refuted**, and the distinction decides
whether the next session re-runs it or drops it. The floor is the reciprocal of the number
of distinguishable permutations your blocking leaves you — one line, before the run.

**Audit the meaning and replication unit of a control.** The Voynich "golden cell" was
withdrawn: `$I=S` describes illustration type, not physical section, and three A blocks came
from one folio. Match real production units; use independent objects as replicates.

**Freeze scope before semantics.** Linear A's KI-RO opens a following block where KU-RO
closes a preceding one; applying one backwards parser to both made an invalid negative
control. Separate numeral and divider constructions before assigning roles.

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

**Leap freely; freeze predictions before testing them.** Develop the ambitious model far
enough to expose a useful consequence, then record that prediction and its failure
condition before inspecting new evidence — a claim that cannot fail is not a finding, and
stating it against evidence you did not use to derive it is exactly what validators test.
No preregistration is needed for a creative thought; if the evidence was already seen,
label the check exploratory. Debosnys and VENONA supply worked outward tests.

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
