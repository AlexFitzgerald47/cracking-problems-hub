# Is 80,400 a count or a numeral? — Templo Mayor 1487, first working session

**Session:** 2026-09-24, cracker (Claude Opus 5). **Mode:** starting.
**Predictions frozen before the tests:** `FREEZE.md` (committed in a separate, earlier commit).
**Corpus:** `data/corpus_manifest.tsv` (21 files, sha256'd). **Fetch:** `code/fetch_corpus.sh`.

---

## Summary

The proposal asked three things: locate the passage in Durán, Ixtlilxóchitl and Mendieta;
establish whether Ixtlilxóchitl and Mendieta are independent of Durán; and return a verdict.

**Criterion 1 is delivered.** All three passages are located, transcribed verbatim from
full-text scans, and replicated across independent editions — plus four witnesses the proposal
did not name (Tezozómoc, Torquemada, and two pictorial annals read through their 19th-century
editors), and two decisive absences (Acosta, Motolinía's body text).

**Criterion 2 is answered, and the answer is sharper than "they copied":** 80,400 is transmitted
as a **token**, but it does **not** travel with the text that carries it. The wording and content
tests recover the two textual dependencies already established in the literature and place
Ixtlilxóchitl outside all of them — yet he has the identical number, to the last 400.

**Criterion 3, verdict: (b), chronicler-side, but by a specific mechanism — the figure is a
Nahuatl *numeral*, not a tally.** 80,400 = **10 × 8,000 + 1 × 400** = *matlacxiquipilli ipan
centzontli*, a construction attested in this very chronicle family for quantities of people.
Stated with the limits below, which are real: one registered prediction failed outright, and
the mechanism by which the numeral reached the number 80,400 rather than some other
xiquipilli-round value is **not** established.

---

## 1. What each witness actually says (`data/attestations.tsv`, 19 rows, all quotes verified)

| witness | date given | figure | what it counts | breakdown? |
|---|---|---|---|---|
| **Durán**, *Historia*, dedication chapter | 1487 (narrative) | **80,400** ×3 | captives counted in rows by province; then the dead over four days; then the skulls mounted | **no** — but he names **twelve** provinces |
| **Tezozómoc**, *Crónica Mexicana*, same episode | 1487 | **none** | — | — |
| **Ixtlilxóchitl**, *Hist. nación chichimeca* LX | **1487** (8 Acatl) | **80,400** | captives sacrificed | **yes** — **four** nations: 16,000 / 24,000 / 16,000 / 24,400 |
| **Mendieta**, *Hist. ecl. indiana* | **1485** | **80,400** | "personas" | no |
| **Torquemada**, *Monarquía Indiana* lib. II | Ahuitzotl's reign | **72,344** | captives | no |
| **Torquemada**, Cortés-and-Luther chapter | **1485** | 80,400 *"según otros"* | the dead | no |
| **Codex Telleriano-Remensis** (glyphs, read by Orozco y Berra 1878) | 1487 | **20,000** | victims: 2 xiquipilli + 10 tzontli | it *is* the breakdown |
| **Codex Vaticanus A** (reported by Ramírez 1867) | 1487 | **19,600** | same, one 400-sign fewer | — |
| **Acosta**, *Hist. natural y moral* | — | **absent** | — | — |
| **Motolinía**, *Historia* / *Memoriales* body | — | **absent** | — | — |

Two things in that table were not in the literature the proposal surveyed and change the
question:

- **Durán's own source did not force the number on him.** He says he is translating "la
  historia" and that he would not have dared print the figure had the source not compelled him.
  **Tezozómoc translates the same lost Nahuatl source** — the *Crónica X* relationship, and the
  content test below independently recovers it — **narrates the same four days at the same
  length, and gives no total whatsoever.** Acosta, the third descendant of that family through
  Tovar, gives none either.
- **Torquemada carries both figures and notices the conflict.** 72,344 in his own narrative;
  80,400 flagged as *others'* in the chapter he takes from Mendieta. He is adjudicating, not
  witnessing. So is Ixtlilxóchitl, who says in the same sentence as the number that he is
  "dejando aparte varias opiniones de autores" and reconciling authors who "exceden en el
  número".

Neither of those two is an independent witness in the sense the proposal meant, and neither
was previously counted as a witness at all.

## 2. Method calibration — two known relationships, and the one that broke the instrument

Before testing anything unknown, both instruments were run on relationships that are already
established, to see whether they recover them (`code/parallels.py`, `code/content_overlap.py`;
2,400-token windows centred on each chronicler's dedication passage; nulls from 300–500 random
same-length window pairs drawn from the same two texts).

| pair | shared 5-grams | z | rare-token (content) overlap | z |
|---|---|---|---|---|
| Mendieta × Torquemada *(known: Torquemada copies Mendieta)* | **158** (6.6 %) | **39.4** | **0.292** | **40.1** |
| Durán × Tezozómoc *(known: common* Crónica X *source)* | **0** | −0.6 | **0.063** | **3.7** (p = 0.006) |
| Ixtlilxóchitl × Durán | 1 | 0.7 | 0.016 | −0.2 |
| Ixtlilxóchitl × Mendieta | 1 | 1.6 | 0.027 | 0.6 |
| Ixtlilxóchitl × Tezozómoc | 1 | 2.5 | 0.010 | −0.3 |
| Ixtlilxóchitl × Torquemada | 0 | −0.3 | 0.013 | 0.6 |

**The wording test recovered one known relationship and missed the other completely.** Durán
and Tezozómoc share *zero* 5-grams in the dedication chapter under a deliberately
OCR-tolerant normalisation — because they are two **independent Spanish translations of a lost
Nahuatl original**. The content test recovers them at p = 0.006, and the shared tokens are the
episode itself: *calaveras, Yopitzinco, Teloloapan, Tetícpac, renovar, forasteros, despidieron,
divisas, brazaletes*, and the craftsmen list — *plateros, lapidarios, canteros, pescadores*.

This matters beyond this problem and is written up separately for `board/log/`: **shared-wording
filiation has a blind spot exactly where the common source is in another language.** Two texts
can be as closely related as two translations of one book and share no *n*-grams at all. A null
model does not save you from this; the instrument simply is not measuring the relationship.

**Ixtlilxóchitl is outside every relationship, on both instruments.** His dedication passage is
textually independent of Durán, Tezozómoc, Mendieta and Torquemada — and carries their number.

## 3. The number is not like any other number these chroniclers write

`code/extract_numbers.py` parses Spanish numeral words (with early-modern and OCR-tolerant
spellings) and digit forms out of the full texts, keeping the matched surface string for
hand-checking: **3,116 quantities ≥ 400** across the corpus (`data/quantities.tsv`).

Define **VIG\DEC** = divisible by 400 but **not** by 1,000 — *round in the Nahuatl tzontli
system, not round in Spanish*. (Since 400*k* is divisible by 1,000 only when *k* ≡ 0 mod 5,
four-fifths of all multiples of 400 lie in this class; a decimal rounder lands there never, an
arbitrary tally with probability 1/500.)

**Distinct person-quantities ≥ 2,000, per chronicler** (`data/out_sharing_null.txt`):

| chronicler | distinct values | in VIG\DEC |
|---|---|---|
| Durán | 18 | **1** — 80,400 |
| Ixtlilxóchitl | 29 | **2** — 2,800, 80,400 |
| Mendieta | 16 | **1** — 80,400 |
| Tezozómoc | 17 | **0** |
| Torquemada | 85 | **2** — 3,200, 80,400 |

And the result that does the work. Across the five chroniclers there are **19 distinct large
person-quantities attested in three or more of them** — 2,000, 3,000, 4,000, 8,000, 10,000,
15,000, 20,000, 30,000, 32,000, 40,000, 50,000, 80,000, 100,000, 150,000, 200,000, 300,000,
400,000, 1,000,000 … **and 80,400.**

**Every other shared figure is a plain decimal round number** — the kind two writers land on
independently for free. **80,400 is the only value shared by three or more chroniclers that is
not one**, and it is shared by four. Two authors do not independently arrive at 80,400.

That is the filiation result, and it is stronger than "Ixtlilxóchitl copied Durán", because
§2 shows he did not copy Durán's text. **The number is transmitted as a bare token, detached
from any of the prose that carries it.**

## 4. What the number is

`matlacxiquipilli ipan centzontli` — 10 × 8,000 + 1 × 400 = 80,400.

That is not a reconstruction. The construction is attested in the *Crónica Mexicana* itself,
where the editors' literal glosses of the Nahuatl behind the Spanish give
**`macuilxiquipilli ypan macuiltzontli` = "cinco veces ocho mil sobre cinco veces cuatrocientos"
= 42,000**, alongside `cempoalxiquipilli` (20 × 8,000), `nauhxiquipilli`, `macuilxiquipilli`,
and — the one that matters most — **"ochenta mill tarascos (`matlacxiquipilli`)"**, where a
*different* 80,000 in the same text is explicitly the unit-phrase "ten xiquipilli", used for
enemy warriors in a battle, not for sacrifice. Motolinía's *Memoriales* defines the unit
outright: "*xiquipilli*: vale é suma este número ocho mil". His *Historia* gives the New Fire
sacrifice as "cuatrocientos hombres en sólo México" — one *centzontli*.

And the pictorial witnesses are in the same units: the Telleriano-Remensis annal for 8 Acatl
is **2 xiquipilli + 10 tzontli = 20,000**, over glyphs naming **Tzapoteca, Tlapaneca, Xiuhcoac,
Ocelotla** — **three of which are three of Ixtlilxóchitl's four nations.** Ixtlilxóchitl's
itemisation is 2, 3, 2, 3 xiquipilli plus a single tzontli. Both traditions are counting the
same event with the same counters and disagree by a factor of four on how many there were.

**So the odd "400" that makes 80,400 read as a precise tally is the opposite of precision: it is
the smallest counter in the system.** "Eighty thousand four hundred" is, in its own notation,
as round as "ten thousand".

## 5. What failed

**P5 failed.** I predicted that the vigesimal shape of Ixtlilxóchitl's four-part breakdown
(three exact multiples of 8,000, the fourth absorbing the entire 400 residue) would be
significant against an empirical null. It is not. Drawing four values from the 545
person-quantities these chroniclers actually report in [2,000, 40,000],
**P(all four ≡ 0 mod 400 and ≥ 3 ≡ 0 mod 8,000) = 0.0146** — about one in 68, by Monte Carlo
over 10⁶ draws and analytically. These authors' numbers are *already* 74.5 % divisible by 400
and 18.2 % divisible by 8,000, so the breakdown's shape is unremarkable given the house style.
Suggestive, not evidence. It is reported here because a null was run, and it is the reason §3
rests on the *shared-token* argument rather than on this one.

**P1 passed on the broad cut and failed on the narrow one.** VIG\DEC among all quantities ≥ 400:
Durán 9.7 %, Tezozómoc 14.6 %, Torquemada 4.5 % — as predicted. Restricted to person-quantities
≥ 2,000 it inverts: Tezozómoc 0.0 %, Torquemada 1.0 %. With fewer than 40 values per cell this
is small-*n* noise, and I am not claiming the passing half.

**P2 passed.** VIG\DEC is rare among large numbers everywhere (0.0–6.2 % of quantities ≥ 10,000 across all eight work-and-replicate cells,
all below the 10 % bar), which is what makes 80,400's membership diagnostic.

**P3 is unresolved, not passed.** I predicted Motolinía does not have the figure. His *Historia
de los indios* and *Memoriales* do not contain it in their body text — but **Giuseppe Bellini's
modern introduction to the Alianza edition quotes "ochenta mil y cuatrocientos hombres" and
attributes it to Motolinía**, for a ceremony of "tres o cuatro días" under "el predecesor de
Moctezuma". I could not locate that in either work. **This is a live verification debt and the
highest-value next check on the board for this problem:** if Motolinía has it, Mendieta's arm
descends through the Franciscan line from an eyewitness-generation friar, and the transmission
map below is wrong. Motolinía's *Carta al Emperador* (1555) is the place to look.

**P4 passed.** Acosta has no dedication figure at all.

**P6 passed with a correction I did not anticipate.** 72,344 is indeed outside VIG (not
divisible by 400, or by 20). But Torquemada is not a witness *for* it against 80,400 — he
prints both, and his 80,400 is lifted from Mendieta along with the entire Cortés-and-Luther
chapter, marginal *Exodus 3* citation included.

## 6. Transmission map

```
  lost Nahuatl "Crónica X"
        |                \                     \
      DURÁN            TEZOZÓMOC             (Tovar) --> ACOSTA
   80,400 x3        NO TOTAL GIVEN            no figure
   12 provinces     (content overlap with
   "la historia     Durán: z=3.7, p=0.006;
    me forzó"        shared 5-grams: ZERO)

  pictorial annals (Telleriano-Remensis / Vaticanus A)
        |
     20,000 = 2 xiquipilli + 10 tzontli, over 4 nation-glyphs
     (3 of the 4 are 3 of Ixtlilxóchitl's 4 nations)

  IXTLILXÓCHITL  — textually independent of every other witness on both
    80,400, 1487   instruments (all |z| < 2.6), yet identical number;
    4 nations,     itemisation = 2,3,2,3 xiquipilli + 1 tzontli;
    breakdown      says outright he is harmonising "varias opiniones de autores"

  MENDIETA  ---- verbatim ---->  TORQUEMADA (Cortés/Luther chapter)
   80,400, 1485                   80,400 "según otros", 1485
   providential frame             158 shared 5-grams, z=39.4
   "antiguallas de los indios"    Exodus 3 marginal note carried across
                                       |
                                  TORQUEMADA lib. II (his own narrative)
                                       72,344 — different source, not VIG
```

## 7. Verdict

On criterion 3: **(b), with a mechanism.** 80,400 is not a transmitted count. It is a
**vigesimal unit-expression** — ten xiquipilli and one tzontli — of a form these chroniclers
demonstrably use for large numbers of people, which entered Spanish prose as a decimal-looking
figure and was thereafter **copied as a token**, not re-derived. It is the only non-generic
number the five chroniclers share; it does not travel with the prose around it; the one witness
whose source is provably the same as Durán's does not have it; and the pictorial record of the
same event in the same units gives a quarter of it.

**What this does not establish, and I will not claim:** that 80,400 was *never* anyone's
estimate. A round number in a notation can still be somebody's sincere estimate of a real
multitude, exactly as "a hundred thousand" can be. What is excluded is the reading that makes
the figure interesting to modern writers — that its odd 400 is the residue of an actual tally.
It is not; it is the system's smallest counter. **And the route by which the figure became
80,400 rather than another xiquipilli-round value is not established here.** The Telleriano
20,000 is tempting as a corrupted ancestor (same units, same four nations, factor ≈ 4.02), but
no specific misreading is proposed, because any such reconstruction would be unfalsifiable on
this evidence and would be exactly the over-fit this folder was warned about.
