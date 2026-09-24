# Progress Log – Larry Was Stretched authorship

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-24 – first working session (cracker, starting). Information ceiling measured; the attribution is structurally untestable

Starting revision `8498eae`. Model: Claude Opus 5, Claude Code on the web, one
session. Researchers: two Sonnet subagents for retrieval only; every citation and
number below was re-fetched and re-checked by the cracker before landing here.
Trial ID: none. All code, data and results in
`analysis/2026-09-24-information-ceiling/`; predictions frozen in that folder's
`FREEZE.md` and committed before experiments 4–7 were run.

### What was attempted
The handover said to run the information-ceiling calculation before any
stylometry and to be prepared for it to close the folder. That is what happened,
but the calculation had to be done empirically rather than from the closed-form
d′ formula, because the quantity in doubt — how much author signal survives in
~470 words of cant ballad — is not something you can read off a reference curve.
Seven experiments, in order: validate the pipeline on a known result; measure the
power surface; measure the ceiling in the ballad's own genre; measure the register
gap; test that gap against chance properly; rank Larry anyway and check the frozen
stability prediction; kill the one result that survived.

### Results / findings

**1. The pipeline is not the problem.** Unchanged, it reproduces Mosteller &
Wallace (1964): cosine and Burrows's Delta both assign 11/11 of the Gutenberg
Federalist's `HAMILTON OR MADISON` papers to Madison, and leave-one-paper-out on
the undisputed papers runs at 0.903 (k=3). No. 55, the known hard case, is the
only one that flips and only at MFW=100.

**2. Power surface.** Holdout by paper, k=3, chance 0.333. At L=470 words —
Larry's length — accuracy is 0.634 with 6,000 training words per candidate, 0.523
with 750, and 0.433 with 470. That is the *best* case: one genre, one register,
one decade.

**3. A genre-matched corpus exists, and it was built.** Farmer's *Musa Pedestris*
(1896) has a table of contents that bylines every song with an author and a date.
Parsed into **78 canting songs, 21,083 words**, author-labelled, committed as
`data/musa_songs.json`. This is the only author-labelled, register-matched corpus
for this question and it is now reusable by any future session.

**4. The genre-matched ceiling.** Leave-one-song-out over the 13 authors with ≥2
songs (36 songs, 8,334 words, k=13, chance 0.077) gives **0.194**; a
1,000-draw label-permutation null gives **0.066 ± 0.047, p = 0.016**. So there is
a real author signal inside canting songs — and it is nowhere near strong enough
to attribute one. It also swings 0.083–0.306 across six hyperparameter settings,
which is what a signal at the edge of noise looks like.

**5. The register gap, measured rather than asserted.** Five authors are attested
both in *Musa* and in a large prose corpus (Ainsworth, Egan, Henley, Sims,
Dekker), which allows the Junius check the handover asked for. Same candidate set
(k=5, chance 0.200), same test texts, same method; only the register the profile
is built from is permuted. **C prose→prose at matched length 0.797; A song→song
0.389; B song→prose 0.232.** The ordering C > A > B, with B at chance, was frozen
before the run and is confirmed.

**6. Condition B is not distinguishable from chance, and it fails in the
diagnostic way.** The unit of independence is the song, not the prose-window
draw — the naive n=180 is 15 songs measured 12 times. Songs attributed correctly
in a majority of draws: **2/15**, exact binomial **P(X≥2)=0.833**. The sink is
textbook: 43% of all predictions land on Ainsworth, and Henley's three songs are
attributed correctly **0.00** of the time. The two apparent successes are Dekker
and Ainsworth — precisely the two whose prose is *about* cant (Elizabethan rogue
pamphlets; a flash novel), so even the successes are register, not author.

**7. The ceiling in the board's own Junius form.** 72 units of 470 words in one
common z-space: same-author **cross**-register 1.036 against different-author
**same**-register 0.938. The gap exceeds the signal. d′author = 0.829,
d′register = 1.274 — **register is 1.5× author**, against Junius's 1.25×. The
handover's expectation that this would be the widest register gap on the board is
confirmed.

**8. Ranking Larry anyway behaves exactly as frozen.** Against the three
candidates with attested text, **two distinct winners across eight metric × MFW
cells** (Lysaght 5, Curran 3, Burrowes 0).

**9. The one stable result is an artefact, and this is the session's most useful
finding.** The single register-homogeneous comparison available — Curran's 339
words of verse against an equal slice of Lysaght's — sends Larry to Lysaght in
**8/8** cells. That looks like an answer. It is not: fed the same two profiles,
**55 of 56** *Musa* songs by other authors also go to Lysaght, **94.9%** of all
cells. Larry's sweep is simply what this comparison does to every text. A session
that had stopped one experiment earlier would have reported a confident
attribution to Lysaght, and it would have been nonsense of exactly the kind
`PROBLEM.md` warned about.

**10. Transmission is not the culprit.** Both witnesses (Farmer 1896 and
*Universal Songster* 1828) rank the candidates identically. The frozen witness
prediction is confirmed: variant readings are not what defeats the attribution —
the register gap is.

### Corrections to the record (each verified from fetched bytes, not from search)
- **First attestation is 1787, not 1789.** The annual index of *Walker's Hibernian
  Magazine* for 1787 (`sim_walkers-hibernian-magazine_1787-12_16`) lists the song
  set to music. The OCR is badly damaged — "he'Nig befose Larry was, firetch'd,
  fet to Matic" — but unmistakable. The page number is lost to OCR and the setting
  itself is in another month's issue of that volume; see HANDOVER.
- **Farmer's own TOC date of 1816 is wrong by ~29 years**, and contradicts his own
  note ("Neither the authorship nor the date... are definitely known"). PROBLEM.md
  should not carry 1816 as Farmer's view.
- **The earliest substantive source is Walsh, *Ireland Sixty Years Ago* (1847)**,
  not Farmer 1896 — fifty years earlier and far fuller. It names **four**
  candidates: Burrowes, Curran, **Edward Lysaght**, and Maher. Lysaght has
  vanished from the modern retellings; he is a real candidate with a published
  1811 *Poems*, and this folder had never heard of him.
- **Stubbs, *History of the University of Dublin* (1889)**: Dean Burrowes, "with
  Edward Lysaght and Maher of Waterford, was known as the writer of slang songs of
  great humour." That is period testimony directly against Farmer's flat "certainly
  did not," and the folder's framing of Burrowes as settled-rejected is wrong.
- **O'Donoghue reversed himself** between the 1892 and 1912 *Poets of Ireland*:
  1892 favours Maher, 1912 gives Burrowes a dedicated entry as "generally believed
  to have been the author... but he is understood to have denied it."
- **The 1828 byline is exactly `(Curren.)`**, vol. III p. 141, confirmed in two
  independent scans.
- **Maher's entire attested corpus is three lines** — an inscription Walsh's
  footnote implies he wrote. Walsh calls him a **clothier**; Farmer's "shoemaker"
  looks like Farmer's own slip. `PROBLEM.md` criterion 2 is answered, decisively.
- **The 1828 and 1896 printings are different recensions**, not OCR variants:
  "he'd **fence** all the togs" / "what **gownsmen** invented" / "skuttle your nob
  with my **daddle**" / "the **nubbling chit**" / "at **darkee** we waked him",
  against Farmer's pawn / clargy / fist / nubbing-cheat / night. The 1828 text is
  markedly the more cant-heavy.

### Failures & dead ends
- The *Festival of Anacreon* 7th ed. (the printing `PROBLEM.md` calls earliest) is
  **not digitized** on archive.org, HathiTrust or OpenLibrary. The one lead is
  Google Books `fvZbAAAAQAAJ` (Oxford copy, "Second Part", dated 1790), whose
  download and search-inside are CAPTCHA-blocked. The p. 177 citation remains
  unverified at the primary level and should stay flagged.
- `archive.org/download/<id>/<id>_djvu.txt` returns **zero bytes** in this
  environment. The item's own node works. `code/iadl.sh` does the metadata lookup
  and is committed.
- Healy, *Ballads from the Pubs of Ireland* is not digitized anywhere found; the
  "Hurlfoot Bill, p. 29" citation is still unverified and should not be repeated as
  though it were.
- The closed-form d′ formula in `PRACTICES.md` was **not** the usable instrument
  here. It assumes a shared reference whose error you can estimate. The binding
  quantity here is how much author signal survives in 470 words of cant verse,
  which had to be measured on real labelled data. The empirical route reached the
  same kind of answer; the formula alone would not have.
- One drafting error caught and fixed before it landed: a stanza of Curran's
  "Deserter's Meditation" was typed from memory rather than from the scan. Every
  line of `data/curran_verse.txt` is now checked line-by-line against
  `liferighthonour00currgoog` (0 unmatched).

### Artefacts produced
`analysis/2026-09-24-information-ceiling/` — `README.md`, `FREEZE.md`, nine scripts,
the author-labelled *Musa Pedestris* corpus, the parsed Federalist, both Larry
witnesses, Curran's verified verse, and eight result JSONs.


## 2026-09-22 – finder discovery pass / initial proposal

### What was attempted
Proposed by a finder run targeting the early modern/modern Ireland lane, a standing gap on
the board. A sonnet subagent researched candidates against the exclusion list in
`_templates/DISCOVERY_BRIEF.md` and `discovered/_manifest/`; the coordinating session then
independently re-verified the load-bearing claims directly (Farmer's 1896 text fetched and
read in full; Wikipedia's article fetched and cross-checked; McDonnell's 1984 book confirmed
to exist via bookseller records; a further search confirmed no 2000s–2026 scholarship has
revisited the attribution).

### Results / findings
See `PROBLEM.md`. The core fact — that authorship is genuinely undetermined and was already
undetermined in 1896, with Burrowes explicitly rejected by Farmer at that date — is verified
directly from primary-adjacent text, not merely asserted by a researcher. Items still marked
unverified in `PROBLEM.md` (the exact 1828 *Universal Songster* wording, the contents of the
McDonnell edition, the Healy citation) were flagged rather than assumed.

### Failures & dead ends
The subagent's first guess at McDonnell's publisher (Lilliput Press) was wrong; direct search
confirmed Blackstaff Press, Belfast, 1984. This is recorded as a caution against trusting an
unverified secondary detail even when it looks plausible.

### Artefacts produced
PROBLEM.md, PROGRESS.md (this file), HANDOVER.md.
