# Progress Log – Templo Mayor 1487 sacrifice count

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-24 – first working session (cracker, Claude Opus 5): the number is a numeral

### What was attempted
Criterion 1 (locate the passages) and criterion 2 (filiation), from full-text scans rather
than from the literature. Twenty-one `_djvu.txt` files fetched from archive.org
(`attempts/2026-09-24-numeral-or-count/code/fetch_corpus.sh`, sha256 manifest in `data/`),
every named edition taken in **two independent scans or two independent editions** per the
carry note from `blood-eagle-kenning`. Predictions frozen in `FREEZE.md` and committed before
the tests were run.

### Results / findings
Full write-up: `attempts/2026-09-24-numeral-or-count/RESULTS.md`.

1. **All three named passages located and transcribed verbatim**, plus four witnesses the
   proposal did not name and two decisive absences (`data/attestations.tsv`, 19 rows).
   Ixtlilxóchitl itemises 80,400 across **four** nations (16,000 / 24,000 / 16,000 / 24,400);
   Durán names **twelve** provinces and gives no breakdown; Mendieta dates it to **1485**, not
   1487, because he needs it to be Cortés's birth year for a Cortés–Luther typology; Torquemada
   gives **72,344** in his own narrative *and* 80,400 "según otros" in a chapter he lifts from
   Mendieta verbatim.
2. **Tezozómoc — who translates the same lost *Crónica X* as Durán, narrates the same four days
   at the same length — gives no total at all.** Nor does Acosta, the third descendant of that
   family. The number does not descend the line it is supposed to have descended.
3. **Method calibrated on two relationships already established in the literature, and one of
   the instruments broke.** Shared-5-gram filiation recovers Torquemada-copies-Mendieta at
   z = 39.4 (158 shared 5-grams) but recovers the Durán/Tezozómoc *Crónica X* relationship
   **not at all — zero shared 5-grams** under a deliberately OCR-tolerant normalisation. A
   rare-token (name-level) test recovers it at z = 3.7, p = 0.006. Two independent translations
   of one lost original share episodes and names but no phrasing. See the board log entry.
4. **Ixtlilxóchitl is textually independent of every other witness on both instruments**
   (all |z| < 2.6) and carries the identical number to the last 400.
5. **The filiation result.** 3,116 quantities ≥ 400 extracted mechanically from the corpus.
   Of the **19 distinct large person-quantities attested in three or more of the five
   chroniclers, every one except 80,400 is a plain decimal round number** (2,000 … 1,000,000).
   80,400 is the only shared non-generic value, and four of the five have it. It is transmitted
   as a **bare token, detached from the prose that carries it**.
6. **What the number is.** 80,400 = 10 × 8,000 + 1 × 400 = *matlacxiquipilli ipan centzontli*.
   Not a reconstruction: the construction is attested in the *Crónica Mexicana* itself, whose
   editors gloss `macuilxiquipilli ypan macuiltzontli` as 42,000 and print "ochenta mill
   tarascos (`matlacxiquipilli`)" for a *different* 80,000 in the same text. Motolinía's
   *Memoriales* defines *xiquipilli* = 8,000; his *Historia* gives a New Fire sacrifice as
   "cuatrocientos hombres" — one *centzontli*. The Telleriano-Remensis annal for the same event
   is **2 xiquipilli + 10 tzontli = 20,000**, over four nation-glyphs, **three of which are
   three of Ixtlilxóchitl's four nations**. The odd "400" that makes 80,400 read as a tally is
   the system's *smallest counter*.
7. **Verdict on criterion 3: (b) — chronicler-side, by a specific mechanism.** A vigesimal
   unit-expression that entered Spanish prose looking decimal and was thereafter copied. The
   route by which it became 80,400 rather than another xiquipilli-round value is **not**
   established, and no specific misreading of the 20,000 is proposed.

### Failures & dead ends
- **P5 failed outright.** The vigesimal shape of Ixtlilxóchitl's breakdown (three exact
  multiples of 8,000, the fourth absorbing the whole 400 residue) is **not** significant:
  against an empirical null drawn from the 545 person-quantities these chroniclers actually
  report in [2,000, 40,000], P = **0.0146**, about one in 68. Their numbers are already 74.5 %
  divisible by 400 and 18.2 % by 8,000. The breakdown is suggestive and nothing more, and this
  is why the argument in §3 of RESULTS rests on the shared-token result instead.
- **P1 passed on the broad cut and inverted on the narrow one** (person-quantities ≥ 2,000:
  Tezozómoc 0.0 %, Torquemada 1.0 %). Small-*n*; the passing half is not claimed.
- **P3 is unresolved and is a live verification debt.** Motolinía's *Historia* and *Memoriales*
  do not contain 80,400 in their body text — but **Giuseppe Bellini's modern introduction to
  the Alianza edition quotes it and attributes it to Motolinía**, for a ceremony of "tres o
  cuatro días" under "el predecesor de Moctezuma". I could not locate it in either work. If
  Motolinía has it, the Mendieta arm of the transmission map is wrong.
- **A cross-edition discrepancy found and left open.** Tezozómoc's skull-rack aside reads
  "sesenta y dos mill" (62,000) in the modern critical edition and "setenta y dos mil" (72,000)
  in Orozco y Berra 1878 — the *same sentence*. A second, earlier passage reads 62,000 in both.
  Orozco y Berra's 72,000 sits suspiciously close to Torquemada's 72,344; possible harmonising
  emendation, not demonstrated. Not resolvable without the manuscript.
- The extractor is deliberately strict and **drops OCR-damaged numerals**: it misses
  Torquemada's own "fetenta y dos mil y trecientosty quarenta y quatro" because OCR fused two
  tokens. That figure is in `data/attestations.tsv` by hand-transcription from the 1723 folio.
  Recall is not complete and the tables should be read as lower bounds.

### The second-scan rule earned its keep, twice
Durán's second mention of the figure is invisible to a numeral parser in the Getty scan
("quatrocicntos") and clean in the other — the very failure mode the carry note predicted for a
numeral. And the 80,400/Motolinía hit that nearly entered this session as a finding turned out
on inspection to sit in a **20th-century editor's introduction**, not in the chronicler.

### Artefacts produced
`attempts/2026-09-24-numeral-or-count/`: `FREEZE.md`, `RESULTS.md`, `code/` (6 scripts:
corpus fetch, numeral extractor, lattice test, sharing + null, 5-gram filiation, content
filiation), `data/` (corpus manifest with sha256, 3,116-row `quantities.tsv`, hand-verified
19-row `attestations.tsv`, four saved analysis outputs).


## 2026-09-22 – finder discovery pass / initial proposal

### What was attempted
Proposed by a finder run targeting "claims propagated through a century of citation without
anyone re-checking the source," a standing gap named explicitly in this run's brief, with a
deliberate preference for a non-Western example. A sonnet subagent researched two candidates
(this one, and a Genghis Khan "greatest happiness" misquote traced through Harold Lamb's 1927
popular biography) plus one it investigated and rejected itself (Mansa Musa's gold allegedly
"crashing Cairo's economy for 12 years," already closed by Warren Schultz's 2001 *Mamluk
Studies Review* reappraisal). The coordinating session independently fetched the Dodds Pennock
(2012) paper's abstract page directly to confirm it is a real, existing publication rather than
an invented citation, and ran independent searches on the Aztec vigesimal counting system and
the Durán/Hassig claims before writing this proposal.

### Results / findings
Dodds Pennock (2012) confirmed real: full citation matches exactly
(*Historical Social Research* 37:3, 276–302). The general shape of the Hassig implausibility
argument and the ~126-skeleton archaeological figure are consistently reported across secondary
sources but neither has been traced to its primary citation by this run — both are flagged
unverified-at-the-primary-source-level in PROBLEM.md rather than asserted as confirmed.

### Failures & dead ends
An interesting numerical observation — that 80,400 decomposes cleanly in Aztec vigesimal
notation as 10 *xiquipilli* (8,000-count units) plus 400 — was investigated as a possible lead
toward "this may reflect a genuine indigenous numerical record" but no source was found making
this specific argument about the Templo Mayor figure. It is recorded here as an idea for a
future session to test properly, not as a finding, since asserting it without a source would
violate the no-fabrication rule.

The Genghis Khan "greatest happiness" quote candidate was not written up as a full proposal
this run (one citation-chain slot was needed) but is a strong backup: the popular wording
("to vanquish your enemies... clasp to your bosom their wives and daughters") traces through
Harold Lamb's 1927 popular biography *Genghis Khan: The Emperor of All Men*, itself claiming
descent from Rashid al-Din's 14th-century *Jami' al-Tawarikh*. An independent search by the
coordinating session found Lamb's actual 1927 wording — "to crush your enemies, to see them
fall at your feet – to take their horses and goods and hear the lamentations of their women" —
which differs noticeably from the most common modern internet wording, suggesting at least two
divergent transmission lines rather than one, a detail worth investigating in a future pack.
Scholarly translations of Rashid al-Din (Thackston) and Juvaini (Boyle) exist and would let a
future session compare wording directly rather than relying on secondary paraphrase.

### Artefacts produced
PROBLEM.md, PROGRESS.md (this file), HANDOVER.md.
