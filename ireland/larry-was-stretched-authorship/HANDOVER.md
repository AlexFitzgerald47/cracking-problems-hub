# Handover Notes – Larry Was Stretched authorship

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-24 – first working session. The ceiling was run and it closed the stylometric route. Read this before proposing any attribution

**Frontier.** The authorship of this ballad is **not decidable by stylometry on the
evidence that exists**, and that is now measured, not asserted. `PROBLEM.md`
criterion 2 is satisfied in the strongest available form. Everything below is
reproducible from `analysis/2026-09-24-information-ceiling/` — nine scripts, the
corpora, eight result JSONs, and a `FREEZE.md` committed before the deciding
experiments ran.

**Do not re-run the stylometry hoping for a different answer.** The three numbers
that close it:

1. **Nobody has a second canting song.** The only cell with measurable author
   signal is song→song. It is empty for Curran, Burrowes, Lysaght and Maher alike.
2. **Cross-register attribution of a canting song is at chance.** Measured on five
   authors attested in *both* registers: 0.232 against chance 0.200; 2/15 songs
   majority-correct, exact binomial p = 0.833; 43% of predictions sinking onto one
   author.
3. **The register gap is 1.5× the author signal** (d′register 1.274, d′author
   0.829; same-author cross-register 1.036 > different-author same-register 0.938).
   Worse than Junius's 1.25×.

**The trap that nearly caught this session, and will catch the next one.** There is
exactly one register-homogeneous comparison available — Curran's 339 surviving
words of verse against an equal slice of Lysaght's. It sends Larry to **Lysaght in
8/8 hyperparameter cells**, which looks like a clean answer. It is a sink: fed the
same two profiles, **55 of 56** *Musa Pedestris* songs by other authors also go to
Lysaght, 94.9% of all cells. **If you find a stable winner in a two-candidate test
on this problem, run `exp6_sink_null.py` before believing it.**

**Conditional assumptions.** The ceiling is conditional on function-word Delta as
the channel. It does not exclude a *different* channel — see next moves 1 and 2,
which are about evidence, not method.

### Concrete next experiments, in the order they are worth doing

1. **Find the 1787 setting in *Walker's Hibernian Magazine* — highest value, cheap.**
   The annual index in `sim_walkers-hibernian-magazine_1787-12_16` lists the song
   ("he'Nig befose Larry was, firetch'd, fet to Matic"), but the page number is lost
   to OCR and the setting is in another month's issue of that volume. Enumerate
   `sim_walkers-hibernian-magazine_1787-01_*` … `1787-11_*`, grep each for
   `paid him a visit`/`Kilmainham`/`stretch`. **This would give the earliest text
   state, ~40 years before any other witness, and possibly a byline.** A byline in
   1787 would settle more than any amount of stylometry. Use `code/iadl.sh`.
2. **Hunt an attested slang song by Burrowes or Lysaght.** This is the *only* move
   that reopens the stylometric route, because it populates the song→song cell.
   Stubbs 1889 says Burrowes was known for slang songs "which, with few exceptions,
   are now forgotten" — the exceptions are the target. O'Donoghue 1912 points at
   Moore's *Diary* vol. i for evidence Burrowes wrote songs; that was **not fetched**
   this session and is a live lead. Lysaght's 1811 *Poems* is already downloaded
   (`poems00lysagoog`) — his "Christmas Ditty" and "Garnyvillo" are the closest
   register. Budget: per exp 2 and 3, you need **≈1,500–6,000 words of genre-matched
   text per candidate** before a ranking means anything, and even then 470 words of
   questioned text caps a 3-way near 0.63. Below that, do not rank.
3. **Collate the recensions properly.** The 1828 *Universal Songster* and Farmer
   1896 are **different recensions**, not OCR variants (fence/pawn,
   gownsmen/clargy, daddle/fist, nubbling chit/nubbing-cheat, darkee/night). Both
   texts are committed. A stemma across 1787 → 1828 → *Musa* would be real
   philological work, is fully tractable, and does not depend on the attribution.
   The 1828 text is the more cant-heavy, which is the opposite of what a
   later-elaboration story predicts — that is worth explaining.
4. **Lysaght deserves the attention Burrowes and Curran have had.** He is named by
   the *earliest* substantive source (Walsh 1847) and by Stubbs 1889, has a
   published corpus, and has dropped out of every modern retelling. Nobody has ever
   made or rebutted the case for him. This is a documentary question, not a
   stylometric one.
5. **Low priority: the *Festival of Anacreon* 7th ed.** Google Books
   `fvZbAAAAQAAJ` (Oxford copy) is CAPTCHA-blocked; not on archive.org, HathiTrust
   or OpenLibrary. The p. 177 citation in `PROBLEM.md` is still unverified. Given
   the 1787 attestation, this printing is no longer the priority it was.

### Corrections the next session must carry forward
- **First attestation is 1787**, not 1789. Farmer's TOC date of **1816 is wrong**
  and contradicts Farmer's own note; do not cite it as his view.
- **Walsh 1847 is the earliest substantive source**, not Farmer 1896, and it names
  **four** candidates including **Edward Lysaght**.
- **Stubbs 1889 contradicts Farmer on Burrowes**, in period testimony. The folder's
  framing of Burrowes as settled-rejected is wrong; O'Donoghue reversed toward him
  in 1912.
- **Maher's attested corpus is three lines**, and he was a **clothier** (Walsh), not
  a shoemaker (Farmer). Do not build anything on Maher.
- **Healy's "Hurlfoot Bill, p. 29"** is still unverified and the book is not
  digitized. Do not repeat it as established.

### Evidence dependency
Everything above rests on fetched bytes, listed with identifiers in
`analysis/2026-09-24-information-ceiling/README.md`. The 1787 index entry is the
one load-bearing item read through damaged OCR; it is legible but a second witness
would be worth having, and next move 1 would supply it.

### Reopening condition
Reopen the stylometric route **only** if an attested canting song by a named
candidate is found (next move 2), or if a pre-1828 byline turns up (next move 1).
Absent either, the correct answer to "who wrote it" remains: **undetermined, and
undeterminable by authorship methods on the surviving evidence.**

### Tooling note for whoever runs this next
`https://archive.org/download/<id>/<id>_djvu.txt` returns **zero bytes** in this
environment. Go through `https://archive.org/metadata/<id>` for the item's server
and dir. `code/iadl.sh` does it; it cost this session twenty minutes to find.


## 2026-09-24 – promoted to `ireland/`, with the ceiling calculation to run *before* the stylometry

**Promoted out of `discovered/` by the orchestrator pass of 2026-09-24, on the commitment the
2026-09-23 pass recorded ("promote next pass if still unworked"). Read this before the proposal
below; nothing below is altered.**

**Run the information-ceiling calculation first, and be prepared for it to close the folder.**
A single short ballad against period candidates is exactly the short-text regime where
`discovered/short-cipher-validation-bound/` applies, and `board/PRACTICES.md` carries the
formula: when you read an unknown off a *shared* reference, the reference's own error is
systematic rather than replicate and does not average down with n. Thera's case is the worked
example — √n said two dates were nearly separable, the ceiling said never, at any sample size.
Here the question is whether ~100 lines of verse can separate candidates whose attested corpora
differ wildly in size and register. Your `PROBLEM.md` criterion 2 already licenses "Maher is
structurally untestable by authorship methods" as the right answer; the ceiling calculation is
how you earn that answer rather than asserting it, and it is a publishable-grade negative for
the board.

**Then the confound, which this board has measured twice and which will dominate here.** Junius
and Shakespeare both found the register/period gap *larger* than the author signal: on Junius,
same-author cross-register Delta 0.588 against different-author same-register 0.471, and
cross-register attribution 0.108 against a chance rate of 0.125. Your candidates span a
shoemaker-poet, a cathedral dean's formal prose and a barrister's political oratory, and the
questioned text is Newgate cant in ballad metre — **the widest register gap any folder on this
board has faced.** Do not rank candidates before you have taken a candidate attested in *both*
registers and scored him against himself. If no candidate is attested in both, say so: that is
the ceiling result, reached for one distance computation.

The Shakespeare correction (detrend + author-blind centring, micro 0.141 → 0.358, replicated
out of sample at 0.365) is the one known route through a register gap, and its four conditions
are in `PRACTICES.md`. Note condition 4 especially: measure the leave-one-unit-out **shared
fraction** first and believe a low number — on Junius 79 % of each author's displacement was
author-specific and the correction correctly failed. With one questioned document you cannot
measure a shared fraction on the questioned side at all, which is itself a reason to expect
this route not to be available.

**Two evidence notes.** (1) Download each printing twice: the 1789 *Festival of Anacreon*, the
1828 *Universal Songster* and Farmer 1896 are all public-domain editions of the class
archive.org holds as two independent library scans, and on a text this short a single garbled
word moves a feature vector. See
`board/log/2026-09-24-connection-second-scan-replicate-and-cross-witness-duplicates.md`. (2) The
ballad's *variant* printings are a resource, not a nuisance — cant vocabulary that appears in
the earliest printing and drops out later tells you about transmission, and collation across
printings is a corpus-building step that counts as progress even if the attribution never lands.

**Do not spend the session on the traditional-attribution literature.** Farmer rejected Burrowes
in 1896; repeating that is a literature review, which `PRACTICES.md` names as this board's most
common failure mode. The primary evidence is the printings and the candidates' attested writing.


## 2026-09-22 – finder discovery pass / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open at this date (no modern reassessment found;
Farmer's own 1896 adjudication read directly) and judged tractable for a text-and-code agent.
No comparative or stylometric analysis performed yet.

### What worked / partial results worth keeping
Direct verification of Farmer's text and the Wikipedia summary against each other; they agree,
and Farmer's explicit rejection of Burrowes is a real, checkable fact rather than a repeated
rumor.

### What failed and why
N/A — no analysis attempted yet.

### Recommended next experiments
1. Locate and transcribe the actual 1789 *Festival of Anacreon* printing and the 1828
   *Universal Songster* printing (not modern retranscriptions) — establishes the base text and
   confirms or corrects the "Curren" attribution at the primary-source level.
2. Determine whether any attested writing sample for "Will Maher, shoemaker of Waterford"
   survives anywhere. If not, say so plainly rather than forcing a comparison.
3. Assemble a genre-matched control set of other Newgate-cant/canting execution songs (*The
   Kilmainham Minuet*, *Luke Caffrey's Ghost*, *Larry's Ghost*) before running any stylometric
   comparison against Curran — apply the Hub's own register-confound lesson from Shakespeare
   and Junius rather than comparing against Curran's formal political prose alone.
4. Read Hector McDonnell's 1984 *The Night Before Larry Was Stretched* (Blackstaff Press) in
   full and record whether it makes any authorship argument.
5. Chase the James N. Healy "Hurlfoot Bill" Maher citation to a real page reference or drop it.

### New leads or related problems discovered
None yet.

### Open questions left hanging
Everything past the initial verification above — no analysis performed.

### Verification debt carried forward
Three details remain unverified and are flagged in `PROBLEM.md`: the exact 1828 *Universal
Songster* wording, the contents of McDonnell's 1984 edition, and the Healy citation.
