claim: The Linear A folder's frontier (`HANDOVER.md`, 2026-09-08) — a "functional/historical
solve candidate; not a phonetic decipherment or language-family solve": that a Haghia Triada /
Casa del Lebete tablet dossier written by HT Scribe 9 records an integrated labour-liability
administration linking accountable units, personnel assessments, standardized six-person work
groups, assignment, roster checking, KI-RO exception reporting, census-linked provisioning and
hierarchical KU-RO / PO-TO-KU-RO control totals; supported by `analysis/2026-09-08-scribe9-dossier-functional-reconstruction.md`,
`analysis/2026-09-07-haghia-triada-labor-control-functional-solve.md`,
`analysis/2026-09-07-kiro-unified-residual-grammar.md`,
`analysis/2026-09-07-obligation-circuit-post-award.md` and the two CSV decode tables.

problem: linear-a

criteria applied: "A coherent linguistic decipherment that accounts for a substantial portion
of the corpus and is consistent with the known archaeological and historical context."

validator role: 1

reproduced: partially — specifics below.

verdict: PARTIAL

---

## What I did

I did not work from the claimant's `analysis/*.csv`. I fetched the raw witnesses myself on
2026-10-02:

- **witness A** — `mwenge/lineara.xyz` `LinearAInscriptions.js` (Douros's tabulation of
  Godart–Olivier GORILA; carries numerals, scribal hand and findspot), re-downloaded fresh;
- **witness B** — SigLA per-document word views (vendored from the 2026-09-25 session; SigLA
  carries sign-groups only, no numerals, so it cannot adjudicate arithmetic);
- **witness C — the primary edition itself**: I downloaded GORILA vol. I
  (`papers/GORILA-Vol1.pdf`, 372 pp. of plates, facsimiles and the editors' own
  transcriptions), rendered the pages for HT 34, HT 85, HT 117, HT 119 and HT 122, and read
  the numerals and the editorial apparatus off them. This is the only witness that is not
  downstream of Younger, and it is where three of the findings below come from.

Scripts, data and full output are at
`historical-texts/linear-a/validation/2026-10-02-v1/` (`run_all.sh`, `out.txt`,
`gorila_checks.md`). I read `validation/2026-09-25/` and ran it, but treated its output as
prior panel material; where I disagree with it I say so.

## 1. Does the arithmetic hold in the raw corpus?

**Corpus-wide, under two frozen segmentations** (walk back from the total marker to the
previous marker / face start; and the same but stopping at an administrative heading `X ·`,
which is the minimum machinery needed to respect the forward-scoping `KI-RO ·` the claim
asserts), there are **31 numeral-bearing KU-RO/PO-TO-KU-RO totals** in the corpus. **9 are
exactly reproducible** from the surviving line items. Permutation null (stated totals shuffled
among blocks, 10^5 draws): null mean 0.52, max 6, **p = 1 × 10⁻⁵**.

So **KU-RO is a summation marker — that reproduces and is not in doubt**. It is also rarely
*testable*: 22 of 31 totals cannot be checked because the entries are physically lost.

Taking the 2026-09-25 session's five reported mismatches one at a time, as instructed:

- **HT 88 (+33)** — **not real; an artefact of that session's segmentation.** HT 88 is
  `A-DU VIR+KA 20 · RE-ZA 6 · NI KI-KI-NA 7 | KI-RO · [six names ×1] KU-RO 6`. Summing
  "everything since the last marker" merges the A-DU commodity section into the KI-RO list.
  Respect the forward scope and the block is exactly 6 = 6. Three such cardinality checks
  reproduce cleanly: **HT 88 6=6, HT 94b 5=5, HT 117a 10=10.** This is a point *for* the
  claimant and against the prior session.
- **HT 119 (−1)** — **real, and it is the claimant's error of omission.** Witness A and the
  GORILA plate (p. 238) agree: entries 34, 68, 13, 10, 7, 7, 10, 2, 8 = **159**, stated
  `KU-RO 160`, on a tablet with **no damage**. `scribe9_dossier.csv` lists "KU-RO 160" among
  HT 119's strong anchors with no note that it fails.
- **HT 94a (+1)** — real (111 vs 110), on a face with damage elsewhere. Not load-bearing.
- **HT 122a (−9) and HT 122b (−50)** — **witness/physical loss, not claimant error, but they
  gut the flagship.** GORILA's own value column (pp. 243, 245) gives 22 for HT 122a against
  `KU-RO 31`, and 15 for HT 122b against `KU-RO 65`, with large breaks at the upper left of
  both faces and `.7 vacat` on b. So `KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97` is a
  relation **among three stated totals only**; 29 % of the first subtotal and 77 % of the
  second are restored from the total rather than read. The claim rates this "high" confidence
  and calls HT 122 a verified master register. It is a self-consistent set of three numbers on
  a broken tablet — a long-standing observation in the literature, not a reproduction.

**Three further arithmetic claims fail outright on the raw evidence:**

- **HT 97 "KA-RU … 82 followed by a selected breakdown summing 82"** (`haghia_triada_functional_decode.csv`,
  "new structural anchor", medium-high). The twelve following values are 33, 25, 6, 4, 4, 5,
  15, 3, 5, 2, 3, 5, summing 110. **35 distinct subsets sum to exactly 82**, and 109 of the 111
  integers in [0, 110] are reachable by some subset. A "selected breakdown" that hits the
  header is near-certain. This anchor carries essentially no information.
- **HT 2 "A-KA-RU 20 = 17 + 3"** (same table, "new structural anchor"). The *same tablet*
  states the pattern twice and contradicts it once: `KI-RE-TA-NA OLE+U 54 · OLE+A 47 · 1` gives
  47 + 1 = 48 ≠ 54. And in **2 of A-KA-RU's 3 corpus attestations** (HT 86a, HT 86b) there is no
  aggregate numeral at all — it is a bare section heading, and on HT 86a `A-DU ·` occupies the
  identical slot after a ruling. The proposed `KA-RU` (preposed) vs `KU-RO` (postposed)
  polarity does not survive its own three attestations.
- **HT 85 "66 = 11 standardized groups of six"**. The source entries are 12, 12, 6, 24, 5, 3,
  4 — **5, 3 and 4 are not multiples of six**, so nothing below the total decomposes into
  six-person units. Base rate: across HT tablet face-pairs, a stated total on one face divides
  exactly by the entry count on the other giving an integer ≥ 2 in **5 of 18 cases (28 %)**.
  HT 11, HT 117, HT 123+124 and HT 131 do it too. And the GORILA apparatus (p. 167) says the
  66 itself required an editorial ruling: *"ce qui pourrait apparaître comme une septième unité
  est en fait une marque d'ongle accidentelle."* The plate is compatible with 67.
- **HT 119 "*327 34 : VIR 68, an exact 1:2 fixed manpower ratio"**. P(some exact 2:1 pair
  among nine random integers in 1–70) = **0.39**. At chance.

**One more primary-source finding, from GORILA p. 101.** The claim's cleanest residual
demonstration is `HT 34: 100 − 70 = KI-RO 30`. GORILA prints the numeral as **`30 ⟦7⟧`** with
an apparatus note that the three unit strokes are *"gravé dans l'argile un peu plus sèche"* and
may stand over an erasure. The digital witness carried `KI-RO 37` as recently as the
2026-09-25 vendoring and now carries `KI-RO 30 [[7]]` — the file changed under us in 12
documents between 25 Sep and 2 Oct, HT 34 among them. The arithmetic works only on the reading
that deletes those strokes, and the claim does not flag this.

## 2. Two structural results that do not survive

**(a) The KI-RO "9/9 two-construction grammar" is not a test.** Corpus-wide there are **16**
KI-RO attestations: 6 numeral-next, 6 divider-next, 4 other (fractions / nothing). The
claimant's nine are a subset and miss HT 55a entirely. More seriously, the rule *classifies by
the next token and then confirms the classification* — there is no outcome under which
`KI-RO <numeral>` could be scored as a forward-scoping block. And it is not a property of
KI-RO: among HT sign-group types with ≥ 4 attestations, **19 of 49 (39 %)** show both a
numeral-following and a divider-following occurrence. The "grammar" describes Linear A list
formatting.

**(b) The DI-KI-SE status toggle — "the best quasi-experimental control in the dossier" —
contradicts the claim's own grammar.** GORILA p. 232 shows, in both photograph and facsimile,
a **full-width ruling drawn across HT 117a immediately after `KU-RO 10`**. DI-KI-SE is on
HT 117**b**, under `*21F-TU-NE ·`, two sections below that ruling. The claim needs both of
these at once and they are incompatible:

- *"`KI-RO ·` opens a list and `KU-RO N` closes it"* — the result that makes HT 88, HT 94b and
  HT 117a work; under it the KI-RO scope ends at `KU-RO 10` and DI-KI-SE is **not** marked
  KI-RO on HT 117 either, so there is no toggle;
- *"`MA-KA-RI-TE · KI-RO ·` is a main heading governing all three sublists"* — needed for the
  toggle; under it the ten-entry cardinality is not a KI-RO-block closure, and the HT 88/94b
  result loses its parallel.

Either way one of the two strongest claimed results fails. This is the single most serious
weakness I found, and it is visible on the plate.

## 3. The pre-registered label permutation (HANDOVER 2026-09-23 cross-reference)

Run on my own code, not the prior session's. Pool = 130 HT tablets; statistic = sign-group
types attested on ≥ 2 tablets of the selected set.

| statistic | observed | unmatched null | **size-matched null (±10 %)** |
|---|---|---|---|
| all sign-groups | 15 | mean 4.77, p = 0.0015 | mean 10.43, **p = 0.117** |
| admin operators dropped | 13 | mean 3.31, p = 0.0013 | mean 7.76, **p = 0.091** |
| operators + Davis–Valério circuit words dropped | 7 | mean 2.99, p = 0.0295 | mean 4.25, **p = 0.113** |

**The dossier's cohesion does not survive a size-matched null.** It is driven by the fact that
the Scribe-9 set contains the long, well-preserved tablets. Of the 15 shared types, 2 are
universal operators (KU-RO, KI-RO) and 6 are Davis–Valério circuit nodes attested on
non-Scribe-9 tablets (DA-RE on HT 7/HT 10, DA-RI-DA on HT 10/HT 93, DA-SI-*118 on HT 13/HT 99,
KU-PA₃-NU on HT 1/HT 3/HT 49/HT 88, *306-TU on HT 9, QA-*310-I on HT 8). Two more (DI, PA) are
single-syllabogram abbreviations on 11 and 6 HT tablets. The genuinely dossier-specific
repeated designations reduce to **five**: DI-KI-SE, MA-KA-RI-TE, MI-TU, PA-TA-NE, *21F-TU-NE
(and *21F-TU-NE also occurs on HT 7b, not Scribe 9).

And the split the query-grammar depends on is null: permuting the "exception" (HT 94, HT 117)
vs "ordinary" (HT 85, HT 87, HT 122) label inside Scribe 9 gives observed 6 shared types
against a null mean of 8.25, **p = 0.80**. The exception/ordinary contrast buys nothing.

## 4. Does it account for a substantial portion of the corpus?

No. Quantified against witness A (1,721 records, **1,600 distinct documents**, **2,560
sign-group tokens**, **1,070 sign-group types**):

| scope | documents | % of documents | sign-group tokens | % of tokens |
|---|---|---|---|---|
| the Scribe-9 dossier (10 tablets) | 10 | **0.62 %** | 123 | **4.8 %** |
| every document named anywhere in the four analysis notes (29) | 29 | **1.81 %** | 339 | **13.2 %** |
| Haghia Triada tablets, for reference | 137 | 8.6 % | 890 | 34.8 % |

So the dossier is 10 of the 137 Haghia Triada tablet documents (7 %), at one site, in one
LM IB horizon, out of a corpus spanning ~1800–1450 BCE across Crete, the Aegean islands and a
handful of overseas finds.

**Lexically it is thinner still.** The whole programme assigns a function to **13 sign-group
types out of 1,070 (1.2 %)**, covering **81 of 2,560 tokens (3.2 %)**. Six of those thirteen
rest on ≤ 2 attestations in the entire corpus: DA-DU-MA-TA (1), KI-KI-RA-JA (1), SA-TA (1),
KU-DA (1), MA-KA-RI-TE (2), U-MI-NA-SI (2). Of the **~1,700 records**, the claim produces a
reading for none in any language, a phonetic value for no sign, and a morpheme boundary
nowhere.

Four of the ten dossier tablets contribute nothing but scribal-hand membership: HT 112 is
`*21F | TU-PA | [lacuna]` + `CYP 6`; HT 135 is six sign-groups on two broken faces; HT 128 is a
pure grain record; HT 132 is three commodity entries. Two errors in `scribe9_dossier.csv`
follow from not checking: it gives HT 112's anchor as **"OVISf"** when the corpus has **CYP 6**
and no ovicaprid sign at all, and HT 132's as **"OVISf 27"** when the raw reading is **`*22F
27`** — an ideogram whose sheep/goat identification is exactly the one this folder's own
`PROGRESS.md` flags as subject to a systematic AB21/AB22 inversion across 14 documents.

## 5. Is it consistent with the known archaeological and historical context?

In the weak sense the criterion asks, **yes, and this clause reproduces cleanly.** The HT
Scribe 9 attribution, the three findspots (Casa Room 7: 7 faces; Casa Room 9: 3; Casa del
Lebete: 7) and the uniform LM IB context all come straight out of the corpus metadata and match
the claim exactly. A labour/personnel-and-staples administration at LM IB Haghia Triada is
consonant with mainstream Aegean archaeology; nothing in the reconstruction contradicts the
record.

Two qualifications. First, the architecture is *transferred*, not recovered: the
assess → render → outstanding state machine is lifted from the Pylos Ma series (`a-pu-do-si` /
`o-pe-ro`), a Mycenaean Greek system two to three centuries later under a different polity. The
claim is admirably explicit that it imports the slots and not the etymologies — but the
consequence is that the "operating system" is a template fitted to 10 broken tablets, and the
fit is what the subset-sum and base-rate tests above show to be cheap. Second, the one
polarity the archive could test fails: on HT 95, the only tablet placing `DA-DU-MA-TA` and
`A-DU` on opposite faces over the same entities, four values are equal, one runs the claimed
way (SA-RU 20 → 10) and one runs the wrong way (QE-RA₂-U 7 → 10). Relatedly, 8 of A-DU's 10
attestations are bulk commodity (GRA, OLE, CYP, VIN) and three are outside Haghia Triada
altogether (KH 11, KH 23, TY 3a); the personnel reading rests on two tokens.

## 6. Can a functional reconstruction satisfy this criterion?

**No, and not marginally.** The criterion's governing noun phrase is "a coherent **linguistic**
decipherment". The work under validation assigns no phonetic values, nominates no language or
family, recovers no morphology, segments no morphemes, and produces no reading of any
inscription in any language. It assigns administrative *functions* to 13 sign-group types.
Even if all thirteen were right, every clause of the criterion except the archaeological one
would be unmet, and the "substantial portion of the corpus" clause would be unmet by two orders
of magnitude. There is no version of this result that satisfies the pre-registered standard.

The claimant's own `HANDOVER.md` says exactly this ("Do not use: *Linear A deciphered*"), and
that discipline is to the folder's credit. My verdict is not that the authors overclaimed the
label; it is that the body of work, measured against the standard that was registered before
anyone knew the answer, **is not a solve and cannot become one along this route.**

## What it *is* worth as progress

Stripped of the parts that did not survive, the following stand and are worth keeping:

1. **A clean, reproducible KU-RO result with a real null.** 9/31 exact, p = 1 × 10⁻⁵ against
   shuffled totals. Independent of language, and now reproduced in this folder rather than
   cited from an external repository.
2. **The forward-scoping `KI-RO ·` construction, with three exact cardinality checks**
   (HT 88 = 6, HT 94b = 5, HT 117a = 10) that only come out right if the scope is respected.
   This also establishes that the earlier "0/7 KI-RO arithmetic failures" result from an
   external project was a parser-direction artefact — a correct and useful correction, and the
   2026-09-25 session's own HT 88 "+33 mismatch" is the same artefact recurring.
3. **The Scribe-9 roster itself**, as a verified fact about the archive: ten documents,
   seventeen faces, three deposits, one hand, LM IB. That is a legitimate object for future
   work even though it is not, on these tests, statistically more cohesive than any ten
   comparable HT tablets.
4. **A set of now-closed branches**, which is what a cracking board should bank: the 11×6 gang
   decomposition, the 1:2 ratio, the KA-RU/A-KA-RU forward aggregate, the DI-KI-SE toggle and
   the exception/ordinary query grammar should not be re-derived. Each has a number attached to
   it in `validation/2026-10-02-v1/out.txt`.

**Recommended next step, if the folder continues:** stop at the sign level. Every result above
is mediated by Younger's transliteration — note that witness A's own `translatedWords` field
already prints "total" for KU-RO and "assessment"? for A-DU, so any reading taken from this
corpus silently inherits the glosses it is meant to be testing. The corpus also moved under us
mid-panel (12 documents changed in eight days, including an arithmetic anchor). A result that
cannot be restated against GORILA's plates and SigLA's sign data is not yet a result.

**Status: HELD — awaiting human sign-off.** Nothing here is to be recorded as solved.

---

dissent: I wrote the whole of the above from my own reproduction before opening
`board/log/2026-10-02-validation-linear-a-v2.md`, to keep the panel's errors uncorrelated. I
record three places where I expect to differ from a co-validator working only from the digital
witness, and where I ask that my reading be preferred because it rests on the primary edition:

1. **HT 88 is not a mismatch.** Any audit that sums "everything since the previous total
   marker" will report HT 88 as +33 and HT 122 as catastrophic. The first is purely an artefact
   of that segmentation and should not be held against the claimant; the second is physical
   loss documented on the GORILA plate, not a claimant error either. I would resist a verdict
   that counts either as evidence of carelessness.
2. **HT 85's 66 and HT 34's 30 are editorial, not observed.** Both rest on GORILA's apparatus
   adjudicating a single stroke group (an "accidental fingernail mark" on HT 85a; three strokes
   in drier clay, possibly over an erasure, on HT 34). A validator reading only the digital
   transliteration will score both as clean hits. They are not clean, and HT 34 in particular
   changed in the digital witness between 25 September and 2 October.
3. **The decisive failure is internal, not statistical.** If a co-validator rests the verdict
   mainly on the permutation nulls, I would add that the sharpest objection needs no statistics
   at all: the ruling on HT 117a makes the KI-RO-scope result and the DI-KI-SE toggle mutually
   exclusive, so the claim's two strongest advertised results cannot both be true.

I do not dissent from a PARTIAL or a FAIL. I would dissent from any PASS, and from any verdict
that treats the functional reconstruction as satisfying the "substantial portion of the corpus"
clause: on my count that portion is 0.62 % of documents and 4.8 % of sign-group tokens.
