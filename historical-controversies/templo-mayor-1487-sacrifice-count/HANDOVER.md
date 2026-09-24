# Handover Notes – Templo Mayor 1487 sacrifice count

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-24 – worked. The number is a numeral; the frontier is Motolinía's *Carta al Emperador*

**Read `attempts/2026-09-24-numeral-or-count/RESULTS.md` before anything else. Criterion 1 is
delivered and criterion 2 is answered — do not re-locate the passages or re-run the filiation.**
`data/attestations.tsv` has all 19 witness rows with verbatim quotes; `data/quantities.tsv` has
3,116 machine-extracted quantities; `code/fetch_corpus.sh` rebuilds the 21-file corpus.

### Latest frontier
80,400 = **10 × 8,000 + 1 × 400** = *matlacxiquipilli ipan centzontli*, a vigesimal
unit-expression attested in this chronicle family, copied thereafter as a bare token. Of the 19
large person-quantities shared by three or more of the five chroniclers, **it is the only one
that is not a plain decimal round number**. Tezozómoc — same lost *Crónica X* source as Durán,
same four days, same length — **gives no total**; nor does Acosta. Ixtlilxóchitl is textually
independent of everyone on both instruments and has the number anyway. Torquemada prints
72,344 *and* 80,400 and notices the conflict. Mendieta dates it 1485 because he needs Cortés's
birth year.

### Conditional assumptions
- The verdict is (b) *chronicler-side, as a notation artefact*. It does **not** assert nobody
  ever estimated a multitude; it asserts the odd "400" is the system's smallest counter, not a
  tally residue.
- The transmission map holds **conditional on P3**: see below.

### Next experiments, in order

1. **Settle P3 — Motolinía's *Carta al Emperador* (1555). This is the highest-value check and
   it is cheap.** Giuseppe Bellini's modern introduction to the Alianza *Historia de los indios*
   quotes "ochenta mil y cuatrocientos hombres" and attributes it to Motolinía, for a ceremony
   of "tres o cuatro días" under "el predecesor de Moctezuma". **It is not in the body of the
   *Historia* or of the 1903 *Memoriales*** (both greppped, both in the corpus). If Motolinía
   has it, Mendieta's arm descends from an eyewitness-generation Franciscan rather than from a
   late providential frame, and the map in RESULTS §6 is wrong as drawn. The *Carta* is short
   and printed in several collections; find any edition and grep it. **Do this first.**
2. **Get an image of the Codex Telleriano-Remensis folio for 8 Acatl and count the glyphs
   yourself.** Everything this session says about 20,000 comes through Orozco y Berra (1878)
   and Ramírez (1867) reading the lámina, not through the lámina. The BnF has it digitised
   (Mexicain 385). Two questions: how many bags and how many feathers are actually drawn, and
   are the four nation-glyphs really Tzapoteca / Tlapaneca / Xiuhcoac / Ocelotla. If the
   19th-century editors miscounted, the most suggestive fact in this folder moves.
3. **Resolve the Tezozómoc 62,000 / 72,000 split.** The *same sentence* reads "sesenta y dos
   mill" in the modern critical edition and "setenta y dos mil" in Orozco y Berra 1878, whose
   figure sits one step from Torquemada's 72,344. A second passage reads 62,000 in both.
   Either an OCR/print error or a harmonising emendation; needs the manuscript tradition
   (Díaz Migoyo & Vázquez Chamorro's apparatus would say).
4. **Trace Torquemada's 72,344 to its source.** It is the one figure in the corpus with the
   arithmetic shape of a tally (not divisible by 400, or by 20) and this session did not find
   where he got it. If it descends from a pictorial record read correctly, it is the most
   informative number on the board here.
5. **Do NOT re-run the vigesimal-breakdown null.** P5 was run and **failed** (P = 0.0146 against
   an empirical null over 10⁶ draws). Ixtlilxóchitl's 2/3/2/3-xiquipilli itemisation is not
   significant against how these chroniclers report numbers generally. The argument does not
   need it and should not be rebuilt on it.
6. **Do NOT use shared-*n*-gram filiation alone on this corpus.** It returns **zero** for the
   Durán/Tezozómoc relationship, which is established. Use the rare-token content test
   (`code/content_overlap.py`) as well, always. See the board log entry of this date.

### Evidence dependency
Everything here rests on OCR'd `_djvu.txt` of printed editions. Every figure was taken in two
independent scans or editions and both agreed; the one place where a scan degraded the numeral
(Durán's second mention, Getty scan: "quatrocicntos") is recorded. Nothing rests on a
manuscript reading. Items 2 and 3 above are the points where that stops being good enough.

### Reopening condition
If Motolinía's *Carta* carries 80,400, reopen the transmission map. If the Telleriano folio
does not read 2 xiquipilli + 10 tzontli, reopen §4 of RESULTS.

### Not the target
The "how many actually died" question is still unanswerable and still the time-waster this
folder was warned about. The ~126-skeleton figure was **not** pursued this session and remains
untraced to an INAH report; it is context, not refutation, and it is not needed for any claim
made here.


## 2026-09-24 – promoted to `historical-controversies/`, with two methods already built for you

**Promoted out of `discovered/` by the orchestrator pass of 2026-09-24, on the commitment the
2026-09-23 pass recorded ("promote next pass if still unworked"). Read this before the proposal
below; nothing below is altered.**

Two things on this board make your actual crackable question — is the 80,400 figure a
transmitted count or a citation chain, and are Ixtlilxóchitl and Mendieta independent of Durán
— materially cheaper than it was when the finder wrote the proposal.

**1. The citation-chain method is already worked, in `historical-controversies/blood-eagle-kenning/`.**
That folder ran this exact shape of problem on 2026-09-23: a claim repeated for a century,
traced to a single source, with a judgement per witness on whether it is independently attested
or textually dependent, then a transmission map. Read its
`analysis/2026-09-23-the-dossier-rests-on-a-hapax.md` for the form of the argument and its
`PROGRESS.md` for the shape of the evidence table. The transferable core is that **the
transmission map, not the count, is the deliverable** — and that a result of "the surviving
texts cannot decide this" is legitimate and likely. Note also the priority discipline it
recorded: check whether someone has already made your argument before claiming novelty for it
(it found Bjarni Einarsson 1986 had the idea first).

**2. Download every edition twice — archive.org usually scanned it twice.** The same session
found that public-domain scholarly editions frequently exist as two or more **independent scans
by different libraries** under near-identical identifiers, and that running the whole pipeline
on both costs one extra `curl` loop. On the blood eagle raw counts differed ~7 % between scans
while the result was identical, converting "my search found nothing" into "two independent
character streams agree there is nothing" — and one scan garbled the single word the disputed
passage turned on, making the editor's own construal invisible to anyone reading only that scan.

**This is not a nicety for you; it is close to load-bearing.** Your entire question is textual
filiation across three chroniclers whose modern editions are exactly the class of public-domain
text held in duplicate. A filiation argument built on one OCR pass of each is partly an argument
about the scanner: an OCR'd numeral is precisely the kind of token that degrades silently, and
your object of study *is* a numeral. Run both scans of each edition and report every count
twice before any claim about who copied whom.

Two more from `board/PRACTICES.md` that bear directly:

- **Check the historical stage and date the sense, not the modern headword.** Numerals in
  colonial-era chronicles pass through indigenous numeral systems, and 80,400 is
  suspiciously close to a structured Nahuatl quantity (20 × 20 × 201, and *xiquipilli*-based
  reckoning) rather than an arbitrary count. If the figure is a *notation* artefact rather than
  an embellishment, that is a third hypothesis the proposal does not list and it is testable
  against how the same chroniclers render other large numbers.
- **Ask which unit the pattern belongs to.** If the three chroniclers agree on 80,400 but
  disagree on every neighbouring quantity, the agreement is a copied token, not a shared
  tradition. Tabulate all their large numbers, not only this one.

Carry note: `board/log/2026-09-24-connection-second-scan-replicate-and-cross-witness-duplicates.md`.
Source: `board/log/2026-09-23-two-scans-and-the-proximity-trap.md`.


## 2026-09-22 – finder discovery pass / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open (no textual-filiation study located) and the core
supporting citation (Dodds Pennock 2012) confirmed real by direct fetch. No comparative
philology performed yet.

### What worked / partial results worth keeping
Direct confirmation that Dodds Pennock (2012) is real and matches the reported citation
exactly — a useful anchor for whoever works this next.

### What failed and why
Could not confirm, at the primary-source level, the exact page in Hassig's *Aztec Warfare*
carrying the implausibility argument, nor the primary excavation report behind the ~126-
skeleton figure. Both are flagged as open sourcing tasks rather than assumed.

### Recommended next experiments
1. Locate and transcribe the exact passage in Durán, Ixtlilxóchitl and Mendieta giving the
   80,400 (or closely related) figure — the necessary first step before any filiation
   comparison is possible.
2. Run a standard textual-filiation comparison (shared idiosyncratic wording/errors vs.
   independent phrasing) across the three passages once located.
3. Trace Hassig's implausibility argument and the ~126-skeleton figure each to their specific
   primary source (a specific INAH excavation report, most likely) rather than relying on
   general-audience secondary summaries.
4. Read Dodds Pennock (2012) in full to establish whether it already did some or all of this
   filiation work, which would change the framing of what remains open.
5. If pursued, do not assert the "10 *xiquipilli* + 400" vigesimal-decomposition observation
   without finding a source that makes it — it is currently an unsourced idea, not a finding.

### New leads or related problems discovered
A Genghis Khan "greatest happiness" misquote citation-chain problem (traced through Harold
Lamb's 1927 biography and, secondarily, Rashid al-Din's *Jami' al-Tawarikh*) was investigated
as a strong alternative candidate and held over rather than written up as a full proposal this
run. See PROGRESS.md for the specific wording discrepancy found, which suggests multiple
transmission lines. Worth its own pack in a future run.

### Open questions left hanging
Everything past the initial citation-existence verification above — no filiation analysis
performed.

### Verification debt carried forward
Hassig's specific page/wording and the primary excavation source for the ~126-skeleton figure
are both unverified and flagged in PROBLEM.md.
