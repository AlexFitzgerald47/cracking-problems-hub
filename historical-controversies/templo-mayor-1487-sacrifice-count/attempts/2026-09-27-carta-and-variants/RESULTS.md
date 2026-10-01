# The *Carta*, the variant, 72,344 and the folio: Templo Mayor 1487, second working session

**Session:** 2026-09-27, cracker, remote session (configured model `claude-opus-5-5`). **Mode:** advancing.
**Starting revision:** `c6b6027`. **Predictions frozen before looking:** `FREEZE.md`, commit `8742b52`.
**Evidence:** `data/` (six tables), `images/` (public-domain crops), `code/fetch_and_crop.py` (rebuilds
every source and crop). Graded predictions: `data/predictions_graded.tsv`.

---

## What failed, read first

1. **The 2026-09-24 session's P3 failed.** Motolinía has the figure. His *Carta al Emperador*
   (Tlaxcala, 2 January 1555) reads "ochenta mill i quatrocientos hombres" (Icazbalceta,
   *Colección* I, 1858, p. 254). **The handover's reopening condition fired**, and the transmission
   map is redrawn below.
2. **A second 2026-09-24 claim is withdrawn: "the odd 400 is the system's smallest counter, not a tally
   residue."** The first half is false as a statement about the system: Nahuatl counts in 20s
   (*pohualli*) and units too. The second half is no longer supported. Chimalpahin's Nahuatl annal
   gives this same count itemised by nation, and his last item carries a 20s-place tail
   (*exiquipilli … ipan centzontli ipan matlacpohualli* = 24,600).
3. **F1.5 failed.** I predicted that Mendieta shares some phrase, qualifier, or the one-temple or
   three-or-four-days framing with the *Carta*. He shares none of them. The only thing the two
   passages have in common besides the number is the providential argument.
4. **F2.4 failed.** I predicted that Tezozómoc's 72,000 predates Orozco y Berra. It does not.
   Kingsborough's 1848 printing reads *sesenta y dos mil*. The 72,000 belongs to the 1878 edition
   alone.
5. **F3.4 failed, narrowly.** I predicted that Torquemada's own dedication narrative is not in the
   *Crónica X* family (content-test z < 2 against both Durán and Tezozómoc). Against Durán it gives
   **z = 2.045, p = 0.036** under the frozen 500-draw null. An exploratory 5,000-draw null gives
   z = 1.95, p = 0.041. Against Tezozómoc it gives z = 0.31.
6. **F4.2 failed.** I predicted that the Telleriano's Spanish gloss would agree with its glyphs. The
   gloss says ***quatro mil*** **(4,000)**. The glyphs say **20,000**.

Of the other prospective predictions, **twelve passed** and **one partly failed**. That was the
F2 classification: "not OCR" and "no harmonisation" held, but "inherited through the 19th-century
copy text" did not. Two predictions were contaminated by my own memory of the *Carta* (F1.1, F1.6).
Both passed, and neither is credited.

## Disposition

**The 2026-09-24 verdict is not confirmed.** Its "(b), chronicler-side" label is refuted, and its
"smallest counter" argument is withdrawn. **The problem closes on a corrected verdict**, because the
correction rests entirely on primary text read this session. No reachable source would move it
further (the reasons are given below).

> **Corrected verdict on criterion 3.** 80,400 is **(a) as to transmission.** It is a Nahua figure
> relayed to the chroniclers, not a chronicler's invention. It is **(c) as to whether it was ever a
> count.** Three pieces of evidence give the origin:
>
> - It is in Spanish by January 1555, inside the event-specific staging of the Mexica narrative.
> - Durán says the Nahuatl history forced it on him.
> - It survives in Nahuatl numerals, itemised by nation, in Chimalpahin's annal.
>
> The native record contradicts itself on size, and nothing that survives can say which figure, if
> any, counted anything:
>
> | Native record | Figure |
> |---|---|
> | narrative and itemised tradition | 80,400 (80,600 in Chimalpahin's version) |
> | pictorial annal (Telleriano-Remensis) | 20,000 |
> | its sister (Vaticanus A) | 19,600 |
> | the Telleriano's glossator | 4,000 |
> | Torquemada's untraced figure | 72,344 |
>
> The notation reading survives in a narrower form: 80,400 is *matlacxiquipilli ipan centzontli*. The
> modern inference that its "400" betrays a real tally is **neither supported nor excluded**.

---

## 1. Item 1: Motolinía's *Carta al Emperador* (1555)

**Found in the first place checked.** Icazbalceta's *Colección de documentos para la historia de
México* I (1858) prints the letter at pp. 251–277. Its text comes from the Muñoz copy of the Simancas
original (RAH, Col. Muñoz, Indias 1554–55, T. 87, ff. 213–32). The passage is on p. 254 and was read
from the page image. Two independent scans (`coleccindedocum01motogoog`, `bub_gb_WJk6nlChEKYC`) agree:

> Sepa V. M. que quando el Marques del Valle entró en esta tierra, Dios nuestro Señor era mui ofendido
> … porque el antecesor de Motecçuma señor de México, llámado Abiçoçi (Ahuizotl), ofresció á los
> Indios (sic) en un solo templo i en un sacrificio que duró tres ó quatro dias **ochenta mill i
> quatrocientos hombres**, los quales traian á sacrificar **por quatro calles en quatro ileras** hasta
> llegar delante de los ídolos **al sacrificadero**

The letter is signed "De Taxcala, 2 de Enero de 1555 años … Motolinía, Fr. Toribio". It gives no year
for the sacrifice, no breakdown and no source for the figure (F1.2–F1.4 passed). Bellini's 1988
introduction, which the prior session flagged, quotes this letter explicitly. The line after the hit
reads "escribe el fraile al emperador".

**What it changes.** The earliest attestation moves from Durán (c. 1581) to **2 January 1555**, 68
years after the event. The writer is a first-generation, Nahuatl-literate Franciscan, and his
*Memoriales* define *xiquipilli* = 8,000.

**The staging.** The *Carta* does not carry a bare number. It carries the number together with a
specific staging: captives brought "by four streets in four rows" to the sacrificial stone over three
or four days. The base rate of that staging decides how much weight it bears:

- **In Durán**, rows of captives are generic. At least ten sacrifice episodes put captives "en
  renglera". But *quatro rengleras* running along the causeways to *quatro sacrificaderos* occurs
  once in the whole work: at the 1487 dedication (Ramírez ed. I, pp. 356–357; `data/staging_matrix.tsv`).
- **In Motolinía's own writing** (*Historia* in two editions, *Memoriales*), "quatro calles" and
  "quatro ileras" occur nowhere except this sentence. The staging is borrowed, not his idiom.

So by 1555 the number was travelling inside the event-specific staging of the narrative that later
fed Durán. That contradicts the prior session's claim that it "does not travel with the prose around
it" (RESULTS 2026-09-24 §3), at least for this pair.

**But the staging is the stable element and the number is not.** The same staging recurs in
**Tezozómoc** and in **Torquemada**:

- Tezozómoc places captives in rows at three causeway points, with four sacrificers at four stones
  and four days, and **gives no number**.
- Torquemada, lib. II cap. 63, has rows along the San Antón causeway "desde Malcuitlapilco" and a
  second row on the west, four days, and **72,344**.

Across the four narrative witnesses the staging is constant, and the number reads 80,400 / 80,400 /
none / 72,344. **Within the narrative family the number is the least stable element.** The prior
session inferred from Tezozómoc's silence alone that the common source "did not force the number".
That now reads as one translator's omission inside a family where the number varies. It is not
evidence that the family lacked a number.

**Mendieta and the *Carta*.** Mendieta's sentence says *personas*, not *hombres*. It gives "largos
ochavarios" instead of three or four days, dates the event 1485, has no rows and names no ruler. What
it shares with the *Carta* is the argument: the 80,400 as the evil that Cortés's coming remedied.
Mendieta is Motolinía's institutional heir, and he sources the figure to "la cuenta de las antiguallas
de los indios". The *Carta* itself cites Motolinía's own "relación de los ritus i antiguallas" to the
Conde de Benavente, though for the dynastic history, not for the figure. **The link is probable and
not demonstrated** (F1.5 failed on wording).

**No independent edition of the *Carta* was reached.** García Pimentel's 1903 printing (pp. 403–423
per Aldao 2022) is not in any archive.org scan of the 1903 volume, and the UPSA PDF failed (TLS, then
503). The quote rests on one edition in two scans, which agree, plus Bellini's quotation. The edition
was made from a copy of the original. Nothing suggests the number was touched on the way: it stands
in the letter's own orthography ("ochenta mill i quatrocientos"), and Icazbalceta printed it in 1858,
before Durán or Mendieta was in print.

## 2. Item 2: Tezozómoc 62,000 vs 72,000, resolved

All printed texts descend from **Kraus MS 117** (Library of Congress, early 17th century). The 1997
edition "reproduce escrupulosamente y por primera vez" that manuscript and identifies it as the
exemplar Veytia copied in 1755. Every branch of that stemma was read (`data/tezozomoc_skull_variant.tsv`):

| witness | branch | reading |
|---|---|---|
| Kraus MS fol. [97v] (1997 ed. p. 304, **page image**) | the exemplar | **sesenta y dos mill** |
| Ternaux-Compans 1853 (French) | Veytia-line copy (Madrid or BnF) | **soixante-deux mille** |
| Kingsborough IX, 1848 | copy of the AGN 1792 copy | **sesenta y dos mil** |
| Orozco y Berra 1878 p. 517 (**page image**) | new copy made from the AGN copy | **setenta y dos mil** |

The parallel "eight soldiers" passage (Motecuhzoma I) reads 62,000 in the Kraus MS, in Kingsborough
and in Orozco y Berra. Ternaux's OCR at that point is illegible. **The 72,000 is an error of the 1878
edition alone.** It entered either in that edition's own transcription from the AGN copy or at
composition; the evidence cannot separate the two.

- **Not OCR:** the printed page reads *setenta*.
- **No evidence of a harmonising emendation**, though that cannot be proved:
  - the editor declares "No hemos tocado el texto … Ninguna superchería en cambios, aumentos o mutilaciones";
  - there is no note at the sentence;
  - the parallel 62,000 is left untouched;
  - his own dedication note (pp. 518–519) discusses Ixtlilxóchitl's 80,400 and the Telleriano's
    20,000 and never mentions Torquemada's 72,344.

The resemblance to 72,344 is coincidence. It could not be a source for Torquemada in any case, who
printed in 1615.

## 3. Item 3: Torquemada's 72,344, traced as far as the evidence goes, and untraced

- **Page image, 1723 vol. I p. 186:** "…fueron los sacrificados, en esta Diabolica Dedicacion,
  setenta y dos mil y trecientos y quarenta y quatro Captivos. Durò esta Fiesta quatro dias". The
  chapter names no source and the page has no marginal note (F3.1). Torquemada prints 80,400
  elsewhere as "según otros", so he knew it and preferred 72,344.
- **Unique:** it appears in no other text reached, of 30 files searched
  (`data/torquemada_72344_search.tsv`). The 1877 *Anales del Museo Nacional* report it as
  Torquemada's, without a source.
- **Not derivable** from any attested figure by the operations frozen in advance
  (`code/arith_check.py`). Every reachable value is a multiple of 20, and 72,344 ≡ 4 (mod 20).
  Adding Chimalpahin's figures afterwards changes nothing.
- **In Nahuatl orders** it is 9 xiquipilli, 0 tzontli, 17 pohualli and 4 units. Chimalpahin's
  24,600 also has a non-zero 20s digit, but 72,344 is the only figure for this event with units.
- **Its narrative** carries the family staging. It has a weak content link to Durán (z = 2.045,
  p = 0.036) and none to Tezozómoc on the instrument (z = 0.31). By inspection it shares two rare
  items with Tezozómoc that the instrument's windows miss: the colonial locator "casas de Alonso de
  Ávila" for the temple site, and the toponym Malcuitlapilco. Orozco y Berra (1878) held that
  Torquemada "tuvo á la vista el Códice Anónimo". That is plausible and unproven.

**Status: untraced (F3.5).** The figure is tally-shaped, attributed to no one, and carried by an
author who knew the rival figure. The previous calibration anchored Torquemada on the chapter he
copies from Mendieta, so his own dedication narrative was never tested before this session.

## 4. Item 4: the Telleriano-Remensis folio, counted

Both reproductions were counted independently: the BnF original (Gallica digitisation
`btv1b8458267s`, via its archive.org mirror, since Gallica returned 403) and the 1899 Hamy/Loubat
photochromographic facsimile. They agree (`data/pictorial_counts.tsv`, `images/telleriano_*`):

- **Fol. 39r, 8 Acatl 1487:** 2 xiquipilli bags and 10 tzontli signs in two ruled rows of five,
  = **20,000**. Orozco y Berra's reading is correct (F4.1).
- **Codex Vaticanus A, same year:** 2 bags and 9 tzontli in rows of five and four, = **19,600**.
  Ramírez's report is correct.
- **The Spanish gloss** on fol. 39r: "dizen los viejos que se sacrificaron en este año **quatro mil
  onbres** tray[d]os de las provincias que havian sujetado por guerra…". It then explains that each
  of "estos negritos" counts four hundred. It counted the ten tzontli and left out the two bags.
  **The one 16th-century reading of this cell we can check was wrong, by a factor of five.**
- **The victims' name glyphs** are a zapote tree, a red paint vessel, a turquoise serpent and a
  jaguar head. These are the signs Orozco y Berra read as Tzapoteca, Tlapaneca, Xiuhcoac and
  Ocelotla. The phonetic readings are his; I checked only the sign identities.

## 5. A witness the folder did not have: Chimalpahin

Chimalpahin's *Séptima Relación*, year VIII acatl 1487 (Siméon 1889, pp. 157–159; page image):

> yn quincenpouhque onxiquipilli Tzapoteca, exiquipilli yn Tlahpaneca, onxiquipilli yn Huexotzinca,
> auh exiquipilli Tziuhcohuaca **ipan centzontli ipan matlacpohualli**

In figures: 16,000 + 24,000 + 16,000 + **24,600**. Siméon's note already gives the sum: "Ce sacrifice
comprit donc **80,600** victimes". The sum is his (1889), not mine.

This is Ixtlilxóchitl's four-nation itemisation, **in Nahuatl numerals**, with a different tail.
Ixtlilxóchitl has 24,400 for the same group, which makes his parts sum to 80,400. In both versions the
non-xiquipilli remainder belongs to the Tziuhcoac/Xiuhcoac captives. The *Anales de Tlatelolco* also
single that group out as the dedication's victims, and the *Códice Aubin* names them with no figure.

Neither itemisation has the other's circumstantial detail, so they look like two draws on one itemised
record, not a copy. It is still not established which way the tail moved. Two readings fit:

- Ixtlilxóchitl, who says he is harmonising "varias opiniones de autores", trimmed 24,600 to 24,400.
- Chimalpahin's text altered it.

Chimalpahin's papers are reported to include copies of Ixtlilxóchitl's writings (the *Codex
Chimalpahin*; I did not verify this), so dependence remains possible.

## 6. Transmission map, redrawn (the reopening condition fired)

```
  NAHUA RECORD of the 8 Acatl dedication — at least three strands, which disagree on size
  │
  ├─ narrative strand (the "Crónica X" family, staging: captives in rows along the causeways, ~4 days)
  │    ├─ MOTOLINÍA, Carta, Tlaxcala 2.i.1555 ....... 80,400 "hombres"; Ahuitzotl; 4 streets, 4 rows
  │    ├─ DURÁN c. 1581 ............................. 80,400 ×3; 4 rows, 4 sacrificaderos;
  │    │                                               "la historia me forçara … escrito y pintado"
  │    ├─ TEZOZÓMOC c. 1598 ......................... NO NUMBER (staging intact)
  │    └─ TORQUEMADA lib. II cap. 63, 1615 .......... 72,344 (staging intact; source untraced)
  │         [Tovar → Acosta: the whole episode omitted — Orozco y Berra 1878]
  │
  ├─ itemised strand (by nation, in xiquipilli)
  │    ├─ IXTLILXÓCHITL c. 1610–40 .................. 16,000/24,000/16,000/24,400 = 80,400 (harmonising)
  │    └─ CHIMALPAHIN c. 1620s (Nahuatl) ............ 16,000/24,000/16,000/24,600 = 80,600 (Siméon)
  │
  └─ pictorial annal strand
       ├─ TELLERIANO-REMENSIS fol. 39r .............. 2 xiquipilli + 10 tzontli = 20,000
       │     └─ its Spanish gloss ................... "quatro mil" (bags not counted)
       └─ VATICANUS A ............................... 2 xiquipilli + 9 tzontli = 19,600

  FRANCISCAN providential line (bare token, reframed)
       MOTOLINÍA 1555 ──(probable, not demonstrated)──> MENDIETA c. 1596: 80,400 "personas", 1485,
       Cortés–Moses ──(verbatim)──> TORQUEMADA 1615: 80,400 "según otros"

  19th-century print: Tezozómoc's 62,000 skulls → "72,000" in Orozco y Berra 1878 only
```

## 7. The verdict, re-examined against the rule frozen before looking

| component (2026-09-24) | status now | why |
|---|---|---|
| 80,400 = 10 xiquipilli + 1 tzontli, a Nahuatl unit-expression | **stands, strengthened** | the itemised count exists in Nahuatl numerals (Chimalpahin) |
| **V2: "(b) chronicler-side"** | **refuted** | Spanish by 1555 inside the native staging; Durán's own testimony; Chimalpahin's Nahuatl itemisation |
| "copied thereafter as a token, not re-derived" | **partly** | true of the Franciscan line; in the narrative family the number rides with the staging and varies across it |
| "the odd 400 is the system's smallest counter, not a tally residue" | **withdrawn** | the system has 20s and units; in the itemised record the 400 is the tail of one nation's figure |
| V1 as frozen (refuted only by an earlier non-round, non-vigesimally itemised, or named-counter attestation) | **survives the frozen test** | no such attestation exists; the Telleriano victims are in xiquipilli and tzontli |

Under the rule frozen before looking, the problem closes. A corrected V2 is reported as a failed prior
claim, not absorbed. The correction rests on text read this session. The residual unknowns are the
source of 72,344, the direction between Chimalpahin and Ixtlilxóchitl, and Motolinía's own source.
All three sit inside the **(c)** half of the verdict and cannot move its **(a)** half. Only a
Spanish-side origin for the *Carta*'s figure would move it: a pre-1555 Spanish source, or proof that
Motolinía took the number from one. None is known.

## 8. What this does not establish

- **How many died.** That is not the target, and this session adds two more incompatible figures to
  the question: Chimalpahin's 80,600 and the glossator's 4,000.
- **That any figure was a tally.** 72,344 has the arithmetic shape of one; its provenance is unknown.
- **That 20,000 is "the real number".** The pictorial annal is one Nahua strand among three. Its own
  glossator misread it.
- **A mechanism turning 20,000 into 80,400.** None is proposed. The two figures differ by a factor of
  about four, and the glossator's 4,000 shows how readily this very cell was misread. That is a reason
  to distrust reconstructions, not a licence for one.

## 9. Limits and debts

- *Carta*: one edition, two scans. An independent edition was not reached (García Pimentel 1903; UPSA
  PDF: TLS, then 503).
- Sources that could not be reached: Gallica (403, worked around through the archive.org mirror), INAH
  *Anales* (403 at origin) and web.archive.org (connection reset).
- The 1997 Tezozómoc edition is in copyright, and the Vaticanus A image rights are unclear. Their
  crops are generated by the script and not committed.
- **Reproducibility defect in the 2026-09-24 corpus script, found and worked around.**
  `fetch_corpus.sh` silently saves a 146-byte 404 page for `motolinia_historia.txt`, because
  archive.org stores that filename with a decomposed "ñ". `code/fetch_and_crop.py` resolves names
  through the metadata API and size-checks every download. The recovered file matches the 2026-09-24
  sha256. `sahagun.txt` is in the old manifest but not in the old script, and its source item was not
  identified. No claim in either session rests on it.
