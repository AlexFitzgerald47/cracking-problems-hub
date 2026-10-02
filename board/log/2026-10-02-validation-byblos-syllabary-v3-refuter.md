# Validation — Byblos syllabary, validator 3 (the refuter)

```
claim: The two standing advances in `historical-texts/byblos-syllabary/`.
       (1) `PARTIAL_BIGRAPH_KERNEL.md` — that a real partial bigraph exists, anchored on
       the Amarna daughter-name control (Meritaton / Meketaton / Ankhesen(pa)amun on the
       Egyptianizing cylinder seal BYBL ra–rc in OCBI); that this control positively
       excludes Woudhuizen/Best and Mendenhall as published systems; and that two signs
       OCBI merges in Syl2–Syl5 (U+E416 `offener Ring`, U+E4AF `Sonnenaufgang /
       Rechts-Schlaufe`) must NOT be normalised to one grapheme when the bigraph is used.
       (2) `PALIMPSEST_CHRONOLOGY.md` — the diachronic model separating an older core, a
       late linearization/palimpsest phase and Phoenician replacement, pressuring a
       ca. 900 BCE invention.
problem: byblos-syllabary
criteria applied: quoted verbatim from `historical-texts/byblos-syllabary/PROBLEM.md`,
       "## Success criteria":

> 1. A reproducible structural audit: sign inventory with documented variant-merging
>    decisions, positional statistics, and an explicit power analysis stating what a
>    corpus of this size can and cannot support.
> 2. Positive exclusion of one or more published decipherments by a held-out or otherwise
>    externally grounded test. **Partly achieved:** the Amarna daughter-name control
>    excludes Woudhuizen/Best and Mendenhall as published systems; see
>    `PARTIAL_BIGRAPH_KERNEL.md` for the Hub audit and prior-art boundary.
> 3. Progress on the dating question by systematically separating core, linear/palimpsest
>    and later comparanda rather than assigning one date to every sign form.
> 4. Convert the partial bigraph into cross-text predictions that are tested on the Dunand
>    core **with the cylinder left out**. This is the critical bridge from a few external
>    anchors to a genuine decipherment.
> 5. A stated, defensible ceiling: what additional bilingual, repeated formula, secure
>    archaeological context or externally identified proper name would be required for a
>    full decipherment.

validator role: 3 (refuter)

reproduced: yes for the claim's own machine-checkable content and for the prior session's
       scripts; the inferential step the kernel offers as its own contribution does not
       survive, and the missing power analysis, once run, does not favour the anchors.
verdict: PARTIAL
```

All my scripts, outputs and saved sources are in
`historical-texts/byblos-syllabary/validation/2026-10-02-v3/`.
`r0_reproduce_prior.sh` re-runs everything from scratch.

## Reproduction

* Re-fetched `src/Scripts/Byblos.elm` and `src/Specialchars.elm` from
  `raw.githubusercontent.com/elamicon/elamicon/master` on 2026-10-02. Both are
  **byte-identical** (md5 `bbfb29fd2605d33999d9a7dc43c55797`,
  `da866ec156a6ccf134f05d6e0d8de563`) to the copies vendored on 2026-09-25.
* Ran the 2026-09-25 session's `parse_ocbi.py`, `refute.py`, `refute2.py`, `refute3.py`
  in a scratch copy. All execute; all three outputs are **diff-identical** to the recorded
  `*_output.txt`. Their numbers are theirs, not mine; I say where we converge.
* Wrote my own parser (`lib_ocbi.py`) from the primary source, with two deliberate
  differences from the 2026-09-25 one: runs of spaces inside a transcription line become
  an explicit segment break, so adjacency is never asserted across a visible gap
  (fragment `c`'s last line has one); and variant readings of a witness are de-duplicated,
  giving 1302 canonical off-seal sign tokens rather than 1343. Neither change alters any
  result below.
* Fetched the external anchors: the GEAS 2021 news page, Schmutz & Mäder 2024 (11 pp.,
  text dump saved), Colless 2019 (`cryptcracker.blogspot.com`), DEAPS KAI 003/004.

## Attacks I ran, and which landed

**(a) OCR / PUA normalisation artefact — did NOT land.** The marker encoding is exactly
what the source documents in its own comment (`'s'` guessmark → U+E7E1, zero-width,
attaching to the *preceding* glyph; `'a'` → fracture; `'x'` → wildcard). Every PUA
codepoint in the file lies in U+E400–U+E4FF plus the four Specialchars; there is no
stray normalisation, no case-folding, no composed/decomposed hazard. The prior session's
handling is correct. There is no transcription artefact here.

**(b) The cylinder's own standing — did NOT land, with one caveat
(`r7_cylinder_standing.py`).** I tested whether the seal actually uses the Byblos signary:
of its 21 distinct forms, 13 occur on other witnesses. That is low (4th lowest of 32
witnesses) but **not an outlier for its size** — 3 of the 24 witnesses with ≤25 distinct
forms score lower. On this test the seal's classification as Byblos-script survives, and
I record that as a negative result in the claim's favour. The caveat is which forms are
seal-only: U+E4AF, U+E4AE and U+E4FD — i.e. *all three* candidate terminals of the two
sister names. The shared `-Aton` terminal that kernel §2 constraint (3) rests on is a
form attested nowhere else in the corpus, so that constraint is uncheckable in principle.

**(c) Power / overfit — LANDED (`r4_power_null.py`).** Criterion 1 demands an explicit
power analysis. `r9` greps the whole claim set: the phrase occurs only where the criterion
or a 2026-09-04 recommendation says one *should* be run. There is no null model, no
permutation test, no p-value, no stated ceiling. `ME_ANCHOR_TRANSFER.md` §5 explicitly
declines one. So I built it.

Kernel §2 lists five "external constraints". Two (the texts' positions in the composition,
and orientation following the figures) are iconographic; I grant them. Three are testable
statements about sign strings: two short names vs one longer; both sisters share a ME-family
onset *and* "the exact same terminal sign" U+E4AF; the long name has U+E44D (`pa`) in its
4th position. Monte Carlo over the seal — re-draw four columns of the observed lengths
(6,4,4,3) from off-seal sign frequencies, draw three alternative readings each for rb and
rc exactly as OCBI offers, and ask whether *any* admissible combination yields the pattern:

| configuration | per-seal P | family-wise over the budget actually spent |
|---|---|---|
| two-sister pattern, free mirror licence | 0.108 | 0.51 |
| two-sister pattern, OCBI-class licence | 0.0029 | 0.027 |
| + `pa` at position 4 exactly, free licence | 0.00094 | — |
| + `pa` anywhere internal, free licence | 0.0036 | 0.021 |

Read that carefully: **the two-sister pattern on its own is inside chance.** It appears in
about one in nine randomly generated seals once the nine OCBI variant readings are charged.
Empirically the same template is abundant in the Dunand core itself — 3,764 pairs of 4-sign
windows share an exact terminal with distinct initials (`r4` K2).

What carries the kernel's statistical weight is one thing only: U+E44D at position 4 of
`ra`. That survives at p ≈ 1e-3 per trial, and it degrades to ≈ 2e-2 if `pa` need only be
*internal* rather than 4th — and "4th" is fixed only by one chosen segmentation of
Ankhesen-pa-amun. `pa` also has an independent, non-corpus argument (the Egyptian p3
cross-shape), which the power analysis cannot score and which I do not dismiss.

Two further budget items the kernel never charges: OCBI transcribes **four** columns on the
seal (ra, rb, rc, rd), not three — rd is simply left unaccounted for; and two of the three
"constraints" in §2(3) are properties of *Egyptian onomastics* (two of the six Amarna
daughters begin `Me-`, three end `-aten`), fixed before any Byblos sign is looked at.

**(d) The `me` anchor's mirror claim — LANDED, as unsupported assertion
(`r6_mirror_shape_test.py`).** The anchor covers *both* sisters only because U+E49A (rb)
and U+E4B0 (rc) are asserted to be "mirrored/allographic forms". That is a testable claim
about two vector outlines, and OCBI ships the outlines.

* OCBI's own taxonomy denies it. U+E49A is named `das Z gerundet` — a rounded variant of
  `das Z` (U+E400). U+E4B0 is named `Die Zwei gespiegelt` — the mirror of `die Zwei`, which
  is U+E47D. On the source's own naming they are variants of two *different* base signs and
  nothing calls them mirrors of each other.
* Geometry, calibrated. I mirrored each outline about a vertical axis (the transformation
  Mäder's argument actually invokes: Egyptian scribes flip signs to face the person named),
  normalised translation and scale, and measured a symmetric Chamfer distance, with OCBI's
  ten explicitly declared `gespiegelt` pairs as positive controls and 4,000 random pairs as
  negative controls. Positive controls: median 0.098. Random pairs: median 0.348. **The
  claim scores 0.343 — the 52.5th percentile of random pairs.** Under a horizontal flip,
  the two `me` forms are no more alike than two Byblos glyphs picked at random.
* I then gave the claim its best possible shot, letting the mirrored shape rotate freely to
  whatever angle minimises the distance. It improves to 0.226 (80th percentile of random
  pairs, and equal to OCBI's own U+E4B0/U+E47D pairing), but 8 of the 10 genuine mirror
  pairs still score better. So: not a flat contradiction, but the strong wording
  ("mirrored/allographic") is unsupported by the only graphical evidence available.

Brian Colless, who has looked at the object, says the same thing independently: "I would
have to say that these '2' letters are not the same; and the one on the left is actually the
second letter in the sequence" — and, on the terminal, "the signs at the bottom of the
cartouches are similar but not the same". OCBI itself encodes that disagreement: its
**rc Var. 2 terminates in U+E4FD, not U+E4AF**, which makes kernel §2 constraint (3)
simply false under that reading.

**(e) Circularity in the inventory merge — LANDED. This is my central finding
(`r5_merge_circularity.py`).** The kernel's one claimed *new* result is that the name
alignment gives "a non-circular reason to split the old U+E416 / U+E4AF variant group",
because rb Var.3 puts both in one four-sign name and a merge would force "an otherwise
unnecessary polyfunctionality". Three independent problems:

1. **Not identified by the evidence.** Apply the kernel's own inference to the *other* OCBI
   readings of the same two columns. rb Var. 1 and Var. 2 read `U+E4FF U+E49A U+E4AE
   U+E4AF` — which puts U+E4AE and U+E4AF, two members of the *same* merged group, in one
   four-sign name. The identical argument would then demand `U+E4AE ≠ U+E4AF`, a *different*
   split, and one cutting across OCBI's own motif naming (both are `Sonnenaufgang`). Under
   rc Var. 2 the premise disappears entirely. Which grapheme pair gets split is decided by
   which of nine readings is adopted, and the kernel adopts Var.3/Var.3 without argument.
2. **The premise is not supported by the corpus.** "Two forms of one grapheme class inside
   a four-sign stretch" is not an anomaly in this corpus — it is the ordinary case:
   **24.6 % of off-seal 4-sign windows under the `search`/`syl1` inventory, 26–29 % under
   `syl2`–`syl5`, 33 % under `syl7`–`syl8`**; 11.3 % even repeat an *identical* form.
   Nothing needs explaining, so nothing is forced. Mixed logographic + phonetic use of one
   sign inside one name is also standard in the Egyptian system the script imitates, so
   "polyfunctionality" is not a cost that excludes.
3. **The kernel breaks its own rule two columns away.** Inside the six-sign name `ra` it
   accepts U+E42A as the first half of the logogram AMUN, while OCBI's `syllableMap` gives
   that same sign the single value `i` and it is one of the most frequent forms in the
   corpus (23 off-seal tokens). The polyfunctionality refused in `rb` is granted in `ra`.

And the split's downstream effect is the opposite of progress: it strips the one
well-attested form (U+E416, 17 off-seal tokens) out of the ATON class, leaving a class with
**3** off-seal tokens under `syl6`–`syl8` instead of 20. It makes the ATON anchor *less*
testable off the seal, and generates no cross-text prediction at all.

I want to be precise about what this does and does not show. The split may well be *right*
— OCBI's glyph names already distinguish `offener Ring` from `Sonnenaufgang`, and `Syl6`–
`Syl8` already split them, which the kernel states. What fails is the claim that **the
bigraph supplies a non-circular external reason** for it. The adjudication is
under-determined; it is a preference presented as an external constraint.

The related "stale `ATON U+E416` mapping" point stands as reporting: GEAS's 2021 page does
give `U+E4AF ATON`, so the public tool contradicts its own project's statement. But note the
direction of the conflict. U+E416 is `offener Ring` — an open circle, a perfectly plausible
sun disc; Colless identifies the sun sign on this seal as yet a third form, "a circle with a
dot in it" in the long column's second position. If `ATON = U+E416`, rb Var.3 reads
`me-ATON-?-?` and the kernel's alignment fails. The kernel resolves a conflict between its
alignment and the only machine-readable sound map in its primary source by declaring the
source stale. That is an assertion, not an adjudication.

**(f) Leakage / criterion 4 — LANDED (`r8_criterion4_pa.py`).** All five "external
constraints" in §2 except the Egyptian p3 shape comparison are properties *of the seal*, so
the anchors are confirmed on the material that established them. The kernel is honest about
this: its §7 places the leave-the-cylinder-out test in the future ("Then run **leave-the-
cylinder-out** searches… We finally have something that can lose"). So the kernel does not
claim criterion 4, and criterion 4 is the criterion `PROBLEM.md` calls "the critical bridge".

The folder's only attempt at it is `ME_ANCHOR_TRANSFER.md`. The 2026-09-25 session already
inverted it, and I reproduce that bit-for-bit: the invariant follower U+E402 is named by the
OCBI font `kurzer Worttrenner oben` — short word divider — it never occupies a line edge
(0 of 13, p = 0.022), and under a divider reading the claimed three-sign unit
`U+E49A U+E402 U+E48F` does not exist; the "invariant first internal transition" *is* the
word boundary. Validator 1 reports the same.

So I ran the held-out test on the anchor the kernel itself calls strongest — `pa` =
U+E44D, "the best externally grounded syllabic value in the current corpus", with 11
off-seal tokens, four times ME's. Result: nothing. Its line-edge rate is ordinary
(4 of 11, expected 2.8, p = 0.30); among the 21 signs with 8–16 off-seal tokens it ranks
8th for left-neighbour concentration and 13th for right-neighbour concentration, with no
invariant or even dominant neighbour on either side; it is adjacent to a divider 0 times,
so it carries no divider confound either. And U+E4AF has **zero** off-seal tokens, so no
held-out prediction can ever involve the ATON anchor at all.

Criterion 4 is not met, for any anchor, and for U+E4AF it cannot be met from this corpus.

**(g) Chronology falsifiability — PARTIALLY landed, partly inability to assess
(`r9_audit_and_chronology.py`).** `PALIMPSEST_CHRONOLOGY.md`'s factual reporting checks out:
DEAPS gives KAI 003 "Gregorian −1000 to −975" and KAI 004 "−950 to −920" exactly as
tabulated, and both records do state the Phoenician-over-pseudohieroglyphic relation. The
three-parameter reframing (genesis / terminal phase / replacement) is a real conceptual
advance and §4 is appropriately careful not to declare Dunand victorious.

But the model's §5 "prediction that can kill the model" requires every sign to be labelled
core / Linear Pseudo-Hieroglyphic / secure palimpsest. The machine-readable corpus carries
**no** period, phase, medium or palimpsest field — only `source`/`group` ∈ {BYBL, BYBL?}
and a writing direction — and no witness is labelled Linear Pseudo-Hieroglyphic. The
nominated kill-test cannot be run from the available evidence and was not run. That is
inability to assess, not refutation. As an exploratory substitute I used the OCBI glyph
outlines' path length as a crude complexity proxy: per-witness means lie on a continuum
from 280 to 746 with no gap and no bimodality, which is consistent with the two-phase model
*and* with a single-phase model, and so discriminates nothing.

The deeper problem is logical. §3 argues: *if* the conventional/DEAPS royal chronology is
approximately right, a Byblos-script layer beneath KAI 3/4 predates the tenth century, so a
ca. 900 invention is impossible. But "the early royal Byblian inscriptions are tenth-century"
is precisely what Sass (2005) disputes; his ca. 900 invention is a package that includes
lowering that series. Conditioning on the contested premise is not a falsification, and the
document's own text concedes it ("None of those moves is individually impossible. The
problem is cumulative") before resting on parsimony. Its "moderate confidence" grading is
honest about this. What the document is *not* is new evidence: every element of the chain is
cited literature, assembled rather than tested.

**(h) Source and citation integrity — one defect found.** `PROBLEM.md`,
`PARTIAL_BIGRAPH_KERNEL.md` and `ME_ANCHOR_TRANSFER.md` all attach ResearchGate publication
`366580046` to Mäder, "Zwei Lautwertvorschläge zum Byblos-Syllabar: me und pa",
*Ugarit-Forschungen* 52. That id is in fact Mäder, "Detecting word boundaries in an
undeciphered script: The Byblos syllabary", BAF-Online (also at
`bop.unibe.ch/baf/article/view/7186`). ResearchGate returns 403 to automated fetch, so I
flag this as probable rather than certain. Its consequence is real: the `me`/`pa` paper is
cited but never located, nothing in the claim set quotes it, and the operative wording of
the mirror argument reaches the Hub only through Schmutz & Mäder 2024 and a GEAS news page.
The paper actually at that id is Mäder's *word-boundary* paper — the one that bears on
whether U+E402 is a divider.

Three things about the seal that the claim set does not record and should. Its only primary
publication is Garbini, Luiselli & Devoto 2004, *Rendiconti dell'Accademia Nazionale dei
Lincei* 9/15, 377–390 — cited nowhere in the folder. Its provenance is "apparently emanating
from somewhere in Phoenicia, possibly Byblos": not merely "not a stratified Dunand find" but
an unexcavated object whose attribution to Byblos is itself an inference. And GEAS's own
anchor page calls it "the historisizing Garbini (2004) seal".

## Criterion-by-criterion

| criterion | verdict |
|---|---|
| 1 — structural audit incl. explicit power analysis | **NOT met.** No power analysis, no null, no p-value, no positional statistics anywhere in the claim set; one adjudicated merge is not an inventory. Supplied here, and it does not favour the anchors. |
| 2 — positive exclusion of a published decipherment | **Met for Woudhuizen/Best, by prior art, correctly attributed.** The kernel explicitly disclaims novelty, which is right. Not met for Mendenhall: Schmutz & Mäder handle him in footnote 33 only, by asserting that Colless explains the mismatch away with "diversen schlecht verständlichen Hilfshypothesen"; they never show his values applied to the three names. |
| 3 — progress on dating by separating core / linear / later | **Partially met in argument, nowhere performed on the signs.** Reporting verified; the separation is proposed and the kill-test is unrunnable from the available corpus. |
| 4 — cross-text predictions tested with the cylinder left out | **NOT met.** The kernel places it in the future; the one attempt inverts into a word-divider artefact; the strongest anchor predicts nothing; the ATON anchor has zero off-seal tokens and cannot be tested at all. |
| 5 — a stated, defensible ceiling | **Partially met.** Both documents state limits and name what would lift them (multispectral/RTI on KAI 3–4, independent confirmation of U+E412 ~ U+E491, better imaging of U+E4B0's follower). But without a power analysis the ceiling is qualitative. |

## What survived my attacks

So that the record is not all demolition:

* The corpus-premise correction is correct and valuable. A machine-readable corpus exists
  and the Hub's old "no corpus" premise was stale.
* The source integrity is clean: no OCR artefact, no doctored vendoring, correct marker
  semantics, byte-identical refetch.
* The seal is not disqualified as a Byblos-script witness by its signary; that attack failed.
* The `pa` = U+E44D anchor is the one piece with genuine weight — the only element that
  survives my null, and it has an independent non-corpus argument.
* The Woudhuizen/Best exclusion survives even if the seal falls, because Schmutz & Mäder's
  first argument (Fuls's phoneticisation degree: ~20–30 logograms expected, 5 postulated)
  does not use the seal at all. The kernel does not make this point and it strengthens it.
* `PALIMPSEST_CHRONOLOGY.md`'s three-parameter reframing is a real advance and its
  confidence gradings are honest.
* Both documents refuse the available overclaims. That restraint is the best thing in the
  folder and should be said plainly.

## dissent

Validators 1 and 2 both returned PARTIAL and I return PARTIAL, so there is no disagreement
on the verdict word. I differ on three substantive points and record them.

1. **The U+E416 ≠ U+E4AF adjudication should be struck, not merely "not carried forward".**
   Validator 1 says the inferential step "did not survive". I go further: it is
   *under-determined*, and demonstrably so — the same inference run on rb Var. 1/2 yields a
   different split (U+E4AE ≠ U+E4AF), and on rc Var. 2 the premise vanishes. Combined with
   24–33 % of ordinary four-sign windows already containing two tokens of one class, and
   with the kernel granting the refused polyfunctionality to U+E42A one column away, this is
   not a result awaiting confirmation. It should not appear in any Hub summary as an
   externally adjudicated inventory decision, in either direction. Whether the split is
   *correct* is a separate, still-open question that `Syl6`–`Syl8` and OCBI's glyph naming
   already bear on without the seal.

2. **The `me` anchor should be narrowed to U+E49A alone.** The mirror link to U+E4B0 fails
   OCBI's own taxonomy and sits at the 52.5th percentile of random glyph pairs under the
   very transformation the argument invokes. Kernel §2 constraint (3) — "a `me` onset in
   mirrored/allographic forms" in *both* sisters — is therefore an unsupported assertion,
   and with it the strongest-looking of the three string constraints. Any downstream use
   should read `rc` as having **no** anchored onset.

3. **Criterion 2 should be recorded as met for Woudhuizen/Best only, and the folder should
   name Garbini (2009) as a live rival.** Schmutz & Mäder's footnote 2 states that the one
   Byblos decipherment attempt they consider methodologically acceptable is Garbini 2009,
   with evaluation deferred to a later paper. The kernel's §5 "what is already dead" reads
   as if the field had been cleared. It has not.

I also want one methodological point on the record, since it is transferable to Phaistos and
Dorabella. The thing that made this claim feel strong is that its five "external
constraints" were counted as five pieces of evidence. Two are iconographic and untestable
from the text; two are facts about Egyptian onomastics that were fixed before any Byblos
sign was inspected; one, the shared terminal, is at chance once the nine variant readings
the source itself offers are charged. One constraint — `pa` in position 4 — is doing all the
work. **The right discipline is to charge the transcription-variant budget before counting
anchors**, because in a corpus with multiple published readings per witness, "the two names
share a sign" is a statement about which reading was chosen.

Status: `HELD — awaiting human sign-off`. Nothing here is solved.
