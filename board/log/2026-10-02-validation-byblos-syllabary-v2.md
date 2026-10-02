claim: The two standing advances in `historical-texts/byblos-syllabary/`. (1) `PARTIAL_BIGRAPH_KERNEL.md` — a real partial bigraph anchored on the Amarna daughter-name control (Meritaton / Meketaton / Ankhesen(pa)amun on the Egyptianizing cylinder seal BYBL ra–rc in OCBI); positive exclusion of Woudhuizen/Best and Mendenhall as published systems; and the adjudication that two signs OCBI merges in Syl2–Syl5 (`E416` and `E4AF`) should NOT be normalised to one grapheme when using the bigraph. (2) `PALIMPSEST_CHRONOLOGY.md` — the diachronic model separating older core, late linearization/palimpsest phase, and Phoenician replacement, pressuring a ca. 900 BCE invention date.
problem: byblos-syllabary
criteria applied: quoted verbatim from `historical-texts/byblos-syllabary/PROBLEM.md`, "## Success criteria":

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

validator role: 2 (source-and-prior-art)

reproduced: yes, for everything the claim asserts about its own sources; and the
source integrity is clean.

- Re-fetched the live upstream OCBI source
  (`raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm`,
  sha256 `649b6b3abd1227e4d5b557016fc4c31db8110692958915e1cca3df121d499c0a`) and
  `src/Specialchars.elm`. Both are **byte-identical** to the copies vendored by the
  2026-09-25 panel. No divergence in `Syl2`–`Syl8` or in `syllableMap`.
- Applied the Hub's own two-witness practice (`HANDOVER.md`, 2026-09-24) to a live
  source rather than a scan. The OCBI corpus has two public witnesses: the raw master
  source, and the **deployed build** `center-for-decipherment.ch/tool/elamicon.js`,
  which is what a human actually reads when they "check OCBI" and need not be built
  from master. `two_witnesses.py`: all 10 syllabaries reproduce as exact group sets,
  the `E416`/`E4AF` verdicts agree 6 merged / 4 split in both, the `syllableMap` is
  identical including `ATON E416`, and all 8 cylinder rows are byte-for-byte present
  in both. The witnesses do not disagree. This is a real negative result and it
  removes a live risk from the inventory-merge adjudication.
- Ran all four 2026-09-25 scripts. `parse_ocbi.py` reproduces; `refute.py`,
  `refute2.py` and `refute3.py` each reproduce their committed output **bit-for-bit**.
- Independently re-derived every source-level claim from the fresh upstream file
  without touching the 09-25 `ocbi_parsed.json` (`source_audit.py`).
- Retrieved and read the external sources myself: Schmutz & Mäder 2024 (PDF, PUA
  codepoints recovered from the embedded GEAS font), the GEAS 2021 anchor statement,
  Vita & Zamora 2018, Mäder's ResearchGate-linked paper, the elamicon README, and
  DEAPS KAI 003–006.
- Could **not** reach: github.com, api.github.com, codeload.github.com and
  web.archive.org are blocked by this session's egress policy. So byte-identity pins
  2026-09-25 = 2026-10-02 but does not independently pin either to the 2026-09-09
  claim session; the upstream commit history is unavailable. Sass 2019 (JSTOR) and
  Rollston 2008 (paywalled) were judged by title, abstract and citing literature only.

verdict: PARTIAL

reasoning:

My assignment was to break the panel's correlated-error risk by checking the claim
against the outside world rather than against itself. I did that by retrieving every
cited source and adjudicating the claim's propositions one row at a time. The full
ledger is `historical-texts/byblos-syllabary/validation/2026-10-02-v2/PRIOR_ART_LEDGER.md`,
with a reason per row so it can be attacked.

**The source integrity is good and the transcriptions are right.** This is worth
saying first because it is the part I expected to break and could not. Schmutz &
Mäder 2024 §§4–5 print the three cylinder sequences glyph for glyph, and after
recovering the PUA codepoints from their PDF they match the Hub's §2 table exactly:
`ra = E4AC E4AD E41F E44D E42A E483`, `rb Var.3 = E49A E416 E491 E4AF`,
`rc Var.3 = E4B0 E443 E429 E4AF`. The choice of Var. 3 for both daughters is also
published, which **softens the 09-25 panel's "1 of 9 variant-reading combinations,
budget never charged" objection** — that selection is attributable to Mäder, not to
the Hub. The DEAPS dates in `PALIMPSEST_CHRONOLOGY.md` §2 all verify exactly against
the live catalogue. The V&Z footnote that carries the entire chronology advance
(signs "clear, at least underneath the inscription of Yehimilk and on one of the
sides of the spatula") is quoted faithfully, including its caveat.

**(a) Prior art boundary. The claim's headline novelty is published prior art.**
`PARTIAL_BIGRAPH_KERNEL.md` is scrupulous about *not* claiming the exclusions
("Do not claim novelty here"), and §5 is a correct restatement of Schmutz & Mäder
2024 §4 and footnote 33, both of which I verified. But the file then names its own
new contribution twice — in §1 and in the Verdict — as the externally grounded split
of `E416` from `E4AF`. Schmutz & Mäder 2024 §4 prints Meketaton as
`E49A E416 E491 E4AF` = **`me-ʕ-ke(t)-ATON`**. It assigns `E416` the value ʕ and
`E4AF` the value ATON *in the same four-sign name*. Two distinct sound values for
the two surface forms **is** the split, published in the one paper the claim leans
on for everything else. The Hub's §4 argument ("treating the two surface forms as
one grapheme forces an otherwise unnecessary polyfunctionality") is a correct
inference, but it is an inference to a conclusion its own cited source already
states. Independently, GEAS's 2021 public statement already gives `E4AF ATON`.

A second, sharper problem with the same argument. The Hub says the later OCBI
inventories "**independently** move in exactly the direction demanded by the
external control". The upstream README says what these objects actually are: the
groupings exist "to test out hypotheses", variants are deliberately not merged
prematurely, and the status table marks Byblos *Grouping* as "**(✓)**" — the only
parenthesised entry among seven scripts. `syl5` is even *named* "Syl4". These are
switchable hypothesis sets, not a progression of improving editions. Given that
GEAS published `E4AF` = ATON in 2021, the economical explanation of the `Syl6`+
split is that it **encodes the same name alignment** — in which case the Hub's
"independent convergence" is the same evidence counted twice. The word
"independently" is load-bearing and unearned.

**A mis-cited load-bearing source.** `PROBLEM.md` and both claim files attribute the
`me` and `pa` values to «Michael Mäder, "Zwei Lautwertvorschläge zum Byblos-Syllabar:
me und pa", *Ugarit-Forschungen* 52; public author copy embedded at
researchgate.net/publication/366580046», and `PROBLEM.md` dates it "Mäder (2021)".
RG 366580046 is a different paper: Mäder, *"Detecting word boundaries in an
undeciphered script: The Byblos syllabary"*, BAF 2019 proceedings, published Dec 2022,
DOI 10.22012/baf.2019.03, open access at bop.unibe.ch/baf/article/view/7186. I
downloaded it. It is a **one-page abstract**: no `me`, no `pa`, no daughter names, no
cylinder, and no footnote enumerating BYBL i IX 5 / k V 4 / m II 3 — the footnote
`ME_ANCHOR_TRANSFER.md` §1 relies on to establish that its three loci were held out.
Schmutz & Mäder 2024's own bibliography lists the Byblos sound-value paper as
*(forthc.) "Lautwertvorschläge zum Byblos-Syllabar anhand der ersten bekannten
Bigraphe", Ägypten und Levante* — not UF 52, not 2021; their "Mäder 2021" is an
encyclopedia entry on **Linear Elamite**. The values themselves survive: `me` is
printed in Schmutz & Mäder 2024 and `pa` on the GEAS 2021 page, so the anchors are
real published prior art. But the claim's bibliographic chain to them is broken, and
the held-out status of the three ME loci rests on a footnote I cannot find in
anything the Hub cites. Relatedly, GEAS publishes the pa value for **two** forms,
"`E44D`; `E49B` pa"; the Hub's frozen PA constraint silently drops `E49B`.

**(c) The provenance dependency the claim flags does not fully survive being taken
seriously.** The Hub renders Vita & Zamora as having "called the non-Dunand material
heterogeneous and problematic". What V&Z (2018: 89) actually write about *this
object* is stronger: "Even if we were to accept their **very dubious identification
as Byblos script**, the differentiation and configuration of each of its signs, and
their alleged relationship with the graphic material extracted from the Byblos
corpus, seem quite often — and at the very least — **highly speculative**", and
documents from outside Byblos proposed as Byblos script "are few and **highly
dubious**". The Hub's paraphrase generalises away the specific published judgment on
the one object everything rests on. The claim then asserts that "the name alignment
makes that classification much stronger". It does not: the alignment is evidence
that *if* these signs are Byblos script they encode those names, whereas V&Z's
objection is the graphic one — whether these forms belong to the Byblos signary at
all. Using the fit a premise licenses to strengthen the premise is precisely the
endo-referential move that Schmutz & Mäder's §1 (the GEAS exo-/endo distinction) sets
out to forbid. Consequence: criterion 2's exclusion is doubly conditional — on a 2024
publication for the result, and on an identification the standard modern survey calls
very dubious for the premise — and criterion 4's bridge inherits both conditions.

**(d) Criterion 3 and criterion 5, which nobody checks.**

Criterion 3 — *"Progress on the dating question by systematically separating core,
linear/palimpsest and later comparanda rather than assigning one date to every sign
form."* **Partially met.** The conceptual separation into genesis / late derivatives
/ replacement is stated clearly and is the better framing. Three deductions against
it. (i) It is V&Z's published synthesis: they already write that "the attested
variants seem to indicate some **diachronic development**", that later stages or
derivations "suggest a **relatively long period of use**", and — nearly the Hub's
Phase A bullet verbatim — that the script "may well have been used for a significantly
long period of time, mainly for **practical purposes on probably perishable material,
which would have left few traces**". They also already make the Hub's KAI 3 argument.
The anti-Sass use of the early royal Byblian sequence is Rollston 2008 (whose title is
literally *"…A Response to Benjamin Sass"*) and Lemaire 2006. All are cited; none of
the division of labour is stated. The genuinely Hub-original formulation is "Sass's
overlaps are evidence for lateness of some forms, not necessarily lateness of the whole
script" — an argument, correctly labelled a model. (ii) The separation is never
*performed*. The phase-stratified sign-form matrix is proposed in §5, re-proposed in
`HANDOVER.md` as the best next experiment, and never run. "Systematically separating"
is predicted, not done. (iii) The two standing advances do not talk to each other on
exactly this parameter. `PALIMPSEST_CHRONOLOGY.md` never mentions the cylinder seal,
although it is the Hub's only externally dated Byblos-script witness: V&Z report
Garbini's **mid-fourteenth-century BC** date for it, GEAS calls it the
"**historisizing** Garbini (2004) seal", and the AMUN spelling requires a date after
Ankhesenpaaten's post-Amarna name change, ca. 1330 BC. That is 250+ years *after* the
late end of the 1900–1600 horizon the chronology's Phase A rests on, and the anchor
object is assigned to no phase at all. A model whose purpose is to stop one date being
assigned to the whole script has left its own best-dated witness out of the
stratification.

Criterion 5 — *"A stated, defensible ceiling: what additional bilingual, repeated
formula, secure archaeological context or externally identified proper name would be
required for a full decipherment."* **Not met.** Both files state current
*insufficiency* well — `KERNEL` §6 lists sparse anchors, cylinder-only forms and an
unstable inventory, and gestures at "not enough degrees of freedom to decode a 60–120-type
system" — and both propose next experiments. But the criterion asks what *would be
required*, in four named categories, and neither file answers it. `CHRONOLOGY` §6
supplies exactly one element (an RTI/multispectral campaign on KAI 3–4 against a
preregistered stroke map, which would address the archaeological-context slot). There
is no quantity of anchored values, no corpus size, no bilingual length. The one
quantified ceiling in this folder — d′_ceiling 1.50 for the `E416`/`E4AF` split, 2.36
for the ME allograph and the T-bridge, with the OCBI reference unstable on 84.5% of its
own merges — was computed by the 2026-09-25 panel, not by the claim, and
`HANDOVER.md` had instructed the claimant on 2026-09-23 to compute it *before*
extending any conditional value. It was not done.

**Criterion 1 — not met.** One variant-merging decision is documented. There are no
positional statistics in either file and no power analysis anywhere in the folder.

**Criterion 2 — met in the literature, not by the Hub; no Hub credit.** The exclusion
of Woudhuizen/Best and of Mendenhall is real, I verified both from the 2024 paper, and
incorporating it correctly is useful housekeeping that will save future sessions a
session. It is not a Hub result. I note for the record that `PROGRESS.md` states this
pass "updated" `PROBLEM.md` including "revised success criteria", and the criterion now
carries a "**Partly achieved**" annotation citing the Hub's own file for an exclusion
published in 2024. Pre-registered criteria amended by the claimant in the same pass that
reports progress against them should be read as the original, which is what I did.

**Criterion 4 — not met.** Not attempted in either of the two advances under
validation. `ME_ANCHOR_TRANSFER.md` attempts it and fails twice over. First, from my
mandate: the published segmentation assigns `E491` = **ke(t)** — a K sign whose t is
parenthesised, i.e. not separately written — and places the free T sign at `E429` in
`me-ri-t-ATON`. The `ME–?–T(?)` skeleton for BYBL k is therefore contradicted by the
segmentation in the very source the bridge depends on; at best it reads `ME–?–KE(T)`.
Second, independently of me, the 09-25 panel's §F–§H showed that `E402`, the invariant
follower on which the whole adjacency family rests, is named in OCBI's own glyph table
"**kurzer Worttrenner oben**" — a word divider — and that under that reading the
three-sign unit does not exist and the "invariant first internal transition" is the
word boundary itself. I note that the `glyphnames.json` carrying that name was vendored
into the 09-25 directory with **no recorded fetch URL**, and I could not locate its
upstream path (the deployed bundle carries glyph names for other scripts but not
Byblos). That point therefore needs a provenance line before it is relied on — it is
the strongest single objection in the folder and it currently rests on an unsourced file.

**What is genuinely Hub-original and survives.** `E4AF` is cylinder-only in the OCBI
raw transcription (I re-derived this: 4 occurrences, 0 off-cylinder). The
`syllableMap` `ATON E416` entry is stale against GEAS's own published `E4AF ATON`,
and I confirmed this on **both** public witnesses — a real, modest data-quality
finding about a public tool, though a finding about a tool and not about the script.
The compilation of the merge/split state across all inventories is accurate, if
understated (merged in `search`, `syl1`–`syl5`; split in `syl6`–`syl9`). And the
"lateness of forms ≠ lateness of the system" formulation is the sharpest thing in
either file. That is a real if small advance on a hard problem, honestly bounded by
its authors, who explicitly decline to call it a decipherment. It is not a solve, and
on the pre-registered standard it clears one criterion partially and none fully.

Status: **HELD — awaiting human sign-off.** I have not updated `STATUS.md`, and
nothing here should be written up as settled.

dissent:

Recorded in advance, since I am posting before the other two verdicts and the 09-25
session left artifacts without a verdict.

1. **I expect to be the most positive of the three on source integrity, and I will
   hold that against a refuter who implies the OCBI data is unreliable.** I checked
   two independent public witnesses of the corpus and they do not disagree on a single
   load-bearing byte, and the three cylinder transcriptions match an independent
   published witness exactly. The 09-25 "1 of 9 variant combinations" objection is
   softer than it reads, because the Var. 3 selection is Mäder's published choice.

2. **I expect to be the most negative of the three on novelty, and I will not be
   talked out of A10.** If another validator scores criterion 2 or the inventory split
   as a Hub result, my objection is specific and checkable: Schmutz & Mäder 2024 §4
   assigns `E416` = ʕ and `E4AF` = ATON in the same four-sign name, which is the split,
   in the paper the claim cites. It is in this directory; anyone can open it.

3. **I dissent in advance from any verdict that treats criterion 5 as met because the
   files are modest about their limits.** Stating that you have not solved something is
   not stating what would solve it. The criterion names four categories of required
   evidence and the claim addresses one of them, partially.

4. **A governance point that is not a criterion and should not be scored as one, but
   should not be lost either.** The pre-registered criteria were edited by the claimant
   in the pass that claims progress against them, and the resulting annotation cites the
   Hub's own file for a 2024 publication's result. Nothing here suggests bad faith — the
   claim files are unusually careful about their prior-art boundary elsewhere — but a
   board that lets claims edit their own success criteria will eventually produce a
   unanimous pass that means nothing. That is the structural failure `VALIDATOR.md`
   exists to prevent, and it happened quietly here.

Artifacts: `historical-texts/byblos-syllabary/validation/2026-10-02-v2/` —
`PRIOR_ART_LEDGER.md` (row-by-row adjudication), `source_audit.py` +
`source_audit_output.txt` (independent re-derivation from fresh upstream),
`two_witnesses.py` + `two_witnesses_output.txt` (raw source vs deployed build), and
the eight retrieved primary sources.
