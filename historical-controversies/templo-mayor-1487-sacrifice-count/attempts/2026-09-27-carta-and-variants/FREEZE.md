# FREEZE — 2026-09-27, before any new evidence was fetched

Session: 2026-09-27, cracker (Claude, remote session; configured model `claude-opus-5-5`).
Mode: advancing. Starting revision: `c6b6027` (main), claim commit `59256bd`.
Committed and pushed **before** any edition of the *Carta*, any page image, any Kingsborough
text, the full Torquemada chapter or any secondary literature on these items was opened.

## What I had already seen at freeze time (derivation evidence — cannot confirm anything)

Only the prior session's files: `HANDOVER.md`, `RESULTS.md`, `FREEZE.md`, `PROGRESS.md`,
`data/attestations.tsv`. In particular: Bellini's paraphrase ("el predecesor de Moctezuma
habría sacrificado, en una ceremonia durada tres o cuatro días, en un solo templo, «ochenta
mil y cuatrocientos hombres»"); the Tezozómoc rows T1 (1997 ed., "sesenta y dos mill"),
T1b (1878 ed., "setenta y dos mil"), T2 (62,000 in both); Torquemada's one sentence (Q1).

## Contamination disclosure — read this before crediting item 1

The *Carta al Emperador* is printed in widely digitised 19th-century collections and is very
likely in my training data. **I have a partial recollection** that it contains "ochenta mil y
cuatrocientos hombres", offered by Moteczuma's predecessor "en un solo templo" over "tres o
cuatro días", and — less confidently — a detail about victims entering "por cuatro calles en
cuatro hileras". That last detail may be an echo of Durán's rows of captives that I read an
hour ago. **So F1.1 is not a clean prospective test.** The sub-predictions marked (P) below
concern details I do not recall and are prospective; those marked (D) are derivation-contaminated
and are recorded only so that a failure is visible. I have no recollection of the Tezozómoc
manuscript reading, of Kingsborough's text, or of any source for 72,344.

## Item 1 — Motolinía, *Carta al Emperador* (Tlaxcala, 2 Jan 1555)

- **F1.1 (D, p = 0.8).** The *Carta* contains 80,400 ("ochenta mil y cuatrocientos"), for a
  sacrifice under Moteczuma's predecessor, in one temple, over three or four days.
- **F1.2 (P, p = 0.75).** The *Carta* gives **no calendar year** for it — neither 1485 nor
  1487. Mendieta's 1485 is Mendieta's own typological move.
- **F1.3 (P, p = 0.85).** **No itemisation** by nation or province.
- **F1.4 (P, p = 0.6).** **No explicit source claim** for the figure (no "según sus libros",
  "pinturas", "cuenta").
- **F1.5 (P, p = 0.6).** Mendieta's sentence shares with the *Carta* at least one element
  beyond the number that is not in Durán or Ixtlilxóchitl (a phrase, a qualifier, the
  one-temple or three-or-four-days framing).
- **F1.6 (D, p = 0.5).** The *Carta* mentions victims entering in four rows / by four streets.

**Consequence rule, frozen.** If F1.1 passes, the handover's reopening condition fires and the
transmission map (RESULTS §6) is wrong as drawn; I redraw it this session. The verdict is split
for adjudication into **V1 (form)** — 80,400 is a vigesimal round expression, not a tally
residue — and **V2 (locus)** — the figure is chronicler-side rather than an indigenous figure
relayed. V1 is refuted only by an earlier attestation that is non-round, itemised in
non-vigesimal parts, or framed as a count by named counters. V2 is **re-examined, not
presumed**, if a Nahuatl-literate friar writing in 1555 already has the number; if V2 fails I
say so as a failed prior claim. If F1.1 fails, Bellini's attribution is an editor's error and I
try to find where he got it.

## Item 2 — Tezozómoc 62,000 vs 72,000 (same sentence, two editions)

- **F2.1 (P, p = 0.85).** The **1878 printed page** reads "setenta y dos mil": 72,000 is in the
  print, not an OCR artefact of the scan.
- **F2.2 (P, p = 0.9).** The **1997 printed page** reads "sesenta y dos mill".
- **F2.3 (P, p = 0.8).** 62,000 is the manuscript reading; 72,000 is a 19th-century
  transmission error.
- **F2.4 (P, p = 0.5).** 72,000 **predates** Orozco y Berra: Kingsborough's 1848 printing
  (*Antiquities of Mexico* IX) reads 72,000 at this sentence. This is the discriminating test
  between "inherited" and "Orozco y Berra's own".
- **F2.5 (P, p = 0.7).** Orozco y Berra has **no note** at this sentence citing Torquemada or
  defending 72,000. A note of that kind would prove a harmonising emendation.
- **Classification (P, p = 0.55):** copy/print error inherited through the 19th-century copy
  text — not OCR, not a deliberate harmonisation.

## Item 3 — Torquemada's 72,344

- **F3.1 (P, p = 0.55).** Torquemada's dedication chapter names **no written source** for
  72,344 (no "según X", no marginal citation attached to it).
- **F3.2 (P, p = 0.9).** 72,344 appears in **no other text in the corpus**, the *Códice
  Ramírez* (inside `tezozomoc_scanA.txt`) and Sahagún included.
- **F3.3 (P, p = 0.7).** 72,344 is **not derivable** from the other figures for this event by
  the operations allowed here, fixed in advance to bound the search: sums of any subset, or
  differences of any two, of {80,400; 20,000; 19,600; 16,000; 24,000; 16,000; 24,400; 62,000;
  72,000}; and a single unit confusion between adjacent vigesimal orders (1↔20, 20↔400,
  400↔8,000) applied to one component of 80,400 or 20,000. Anything outside this set found
  later is exploratory and will be labelled so.
- **F3.4 (P, p = 0.55).** On the prior session's content instrument (`content_overlap.py`,
  unchanged), Torquemada's dedication narrative is **not** in the *Crónica X* family:
  z < 2 against both Durán and Tezozómoc. I.e. 72,344 arrives with a different narrative.
- **F3.5 (P, p = 0.55).** The source of 72,344 **cannot be established** from what is
  reachable this session.

## Item 4 — Codex Telleriano-Remensis, 8 Acatl (only if time; frozen now because it is cheap)

- **F4.1 (P, p = 0.6).** A count from the BnF image gives **2 bags + 10 feather signs** for the
  victims, as Orozco y Berra read it (20,000).
- **F4.2 (P, p = 0.5).** A Spanish gloss on the folio, if present, gives a figure consistent with
  the glyphs.

## Disposition rule, frozen

**Closed, verdict confirmed** if V1 survives all items, any map change can be redrawn from
evidence in hand, and no final claim depends on evidence not obtained. **Reopened** if an
earlier attestation is tally-shaped or itemised in non-vigesimal parts, if the Telleriano
victims are not in xiquipilli/tzontli at all, or if the final statement needs a check this
session could not make. A corrected V2 label is reported as a **failed prior claim**, not
absorbed silently; whether the problem can close with it corrected depends on whether the
correction rests entirely on evidence in hand.
