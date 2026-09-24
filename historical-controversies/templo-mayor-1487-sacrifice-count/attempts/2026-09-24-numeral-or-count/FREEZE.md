# FREEZE — predictions registered before the evidence that tests them was examined

Session: 2026-09-24, cracker (Claude Opus 5), problem `templo-mayor-1487-sacrifice-count`.
Repo revision at freeze: see `git log` for the commit that introduces this file.

This file separates **what I had already seen when I formed the hypothesis** (derivation
evidence, which cannot confirm it) from **what I had not seen** (prospective tests). It is
written and committed *before* the extraction pipeline in `code/` was run and before the
researcher's corpus-gathering results were read.

---

## Already seen at the moment of freezing — DERIVATION evidence, not confirmation

Located by direct grep of downloaded `_djvu.txt` full texts (archive.org), read in context:

1. **Durán**, *Historia de las Indias de Nueva España*, ed. Ramírez 1867, vol. I, cap. on the
   dedication (printed pp. 353–359): "ochenta mili y quatrocientos" appears **three times** —
   (a) the captives counted in rows by province before the killing, (b) those who died over
   four days, (c) "las ochenta mili calauernas y quatrocientas mas" mounted on the renewed
   skull-rack. Durán names twelve provinces of origin and gives **no breakdown of the number**.
   He states he is translating "la historia" and that he would not have dared write the figure
   had the source not forced him.
2. **Ixtlilxóchitl**, *Historia de la nación chichimeca* cap. LX (*Obras históricas*, ed.
   Chavero, vol. II p. 273): "ochenta mil y cuatrocientos hombres en este modo" **with a
   four-nation itemisation**: tzapoteca 16,000; tlapaneca 24,000; huexotzinca+atlixca 16,000;
   Tizauhcoac/Xiuhcoac 24,400. He dates the dedication to 1487 (8 Acatl) and explicitly says he
   is setting aside "varias opiniones de autores" and harmonising authors who "exceden en el
   número".
3. **Mendieta**, *Historia eclesiástica indiana*: "se sacrificaron ochenta mil y cuatrocientas
   personas", dated to **1485**, the year of Cortés's birth, inside an explicit Cortés–Luther
   providential typology, sourced to "la cuenta de las antiguallas de los indios". No breakdown,
   no province list.
4. **Torquemada**, *Monarquía Indiana* (1723), lib. II: "fueron los facrificados, en elta
   Diabolica Dedicacion, fetenta y dos mil y trecientos y quarenta y quatro Captivos" =
   **72,344**.
5. **Tezozómoc**, *Crónica Mexicana*, narrates the same dedication at the same length and gives
   **no total for it**. Two separate skull-rack counts attributed to Spanish soldiers appear
   elsewhere in his text, and the two editions consulted disagree: 62,000 (modern critical ed.)
   vs 72,000 (Orozco y Berra 1878) in the Ahuitzotl chapter, and 62,000 in a Motecuhzoma I
   chapter in both.
6. **Nahuatl numeral idiom in Tezozómoc** (grep hits, read in context at two of them):
   `cempoalxiquipilli` (20x8,000), `matlacxiquipilli` glossed "ochenta mill",
   `macuilxiquipilli` (5x8,000), `macuilxiquipilli ypan macuiltzontli` glossed 42,000,
   `nauhxiquipilli`, "beinte y cinco xiquipilli de a ocho mil cada xiquipil".
7. **Ramírez's 1867 footnote** to Durán reports the *Codex Telleriano-Remensis* gives 20,000 in
   native numerals for this event and the *Codex Vaticanus* 400 fewer; **Orozco y Berra's 1878
   note** reads the glyphs himself: two bags (8,000 each) plus ten feathers (400 each) =
   20,000, over glyphs naming Tzapoteca, Tlapaneca, Xiuhcoac, Ocelotla.

## The hypothesis these led to

**H-N (notation).** 80,400 is not a tally. It is a **vigesimal unit-expression** —
*matlacxiquipilli ipan centzontli*, "ten xiquipilli and one tzontli" (10 x 8,000 + 1 x 400) —
of exactly the form attested elsewhere in this chronicle tradition as a conventional large
quantity. Its spurious decimal *precision* (the odd "400") is what makes modern readers treat
it as a real count, and is in fact the signature of the opposite.

## PROSPECTIVE predictions — evidence NOT examined at freeze time

The extraction pipeline had not been written or run; the researcher's corpus results had not
been read. Frozen now.

- **P1.** Define VIG\DEC = {n : n >= 400, n = 0 mod 400, n != 0 mod 1000} — numbers that are
  round in vigesimal but *not* round in decimal, so a Spanish author rounding decimally will
  essentially never land there. Among all quantities >= 400 extracted mechanically from the
  full texts, the **proportion falling in VIG\DEC will be strictly greater in the Nahua-derived
  texts (Durán, Tezozómoc) than in Torquemada's *Monarquía Indiana***.
- **P2.** VIG\DEC will be **rare** in the corpus overall: fewer than 10 % of all extracted
  quantities >= 10,000 will fall in it. (Rarity is what makes 80,400's membership diagnostic
  rather than generic; if VIG\DEC turns out common, H-N loses its force and I will say so.)
- **P3.** **Motolinía** (*Historia de los indios* / *Memoriales*) does **not** contain the
  80,400 figure for the temple dedication. If he does, Mendieta's figure descends through the
  Franciscan line and my reading of Mendieta as a borrowed token needs revision.
- **P4.** **Acosta** (*Historia natural y moral*, 1590) does **not** give 80,400 for the
  dedication.
- **P5.** Under a null in which Ixtlilxóchitl's four components are drawn independently from the
  **empirical distribution of person-quantities extracted from the rest of the corpus** (i.e.
  from how these chroniclers actually report numbers of people, not from a uniform), the
  probability that all four are = 0 mod 400 *and* at least three are = 0 mod 8,000 will be
  **< 1e-4**.
- **P6.** Torquemada's 72,344 is **not** = 0 mod 400 and not = 0 mod 20; it will be the only
  dedication figure in the corpus outside VIG, i.e. the only one with the arithmetic shape of a
  tally rather than of a unit-expression.

## Registered failure conditions

- If P1 fails (Torquemada as vigesimal-looking as Durán), the mod-400 signature is an artefact
  of how large numbers are printed or extracted, not of Nahuatl notation, and H-N is not
  supported by it.
- If P2 fails (VIG\DEC common), 80,400's form is unremarkable and carries no information.
- If P3 fails, the Mendieta arm of the transmission map is wrong as drawn.
