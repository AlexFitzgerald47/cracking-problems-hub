# Validation — Ennis ogham amber bead, `STINGING` (validator 2)

claim: The Ennis ogham amber bead (I-CLA-003 / CIIC 53) inscription decodes to the English plaintext **STINGING**, via the six signs `DMVAVA` under a uniform 3-position backward cyclic shift in the traditional learned 20-letter ogham order `B L V S N | H D T C Q | M G NG Z R | A O U E I`, giving `S T I NG I NG`.

problem: `ireland/ennis-ogham-amber-bead/`

criteria applied: `PROBLEM.md` has no section headed "Success criteria". Its pre-registered standard is the **Crack target**, quoted verbatim:

> Establish what the inscription says or encodes while explaining the anomalous marks, direction and circular/closure geometry rather than merely fitting an inherited transcription.

(Note on the criterion itself: `git log` shows this sentence was edited on 2026-09-08 — *after* the 2026-09-07 solve claim — from "...the anomalous marks, direction and **split stemline**..." to "...**circular/closure geometry**...", in commit `8a9f5ae`. The edit tracks the claimants' own revised physical model. It does not lower the bar — it still demands that the anomalous marks, the direction and the geometry be *explained* — so I apply the current wording as instructed, and note that the claim fails both wordings identically.)

validator role: 2 (physical and historical evidence chain)

reproduced: **partially** — the arithmetic reproduces exactly; the evidence chain that supplies its input does not.

- Ran `code/decode_stinging.py`: prints `S T I NG I NG` → `STINGING`, assertions pass.
- Ran `code/caesar_affine_null.py` in full (both lexicons present locally). Reproduces the published result: of the 20 cyclic shifts of `dmfafa`, exactly one is an English word (`stinging`, shift +17 ≡ −3); `DMLOVA`, `ATATML`, `ATODML` give no hit; the sole affine hit is `(a,b) = (1,17)`, i.e. the Caesar shift itself. My CMUdict counts differ trivially from the writeup (13,486 six-token sequences / 13,450 orbits / 0.4203% vs. their 13,932 / 13,893 / 0.4342%) — a dictionary-version difference, not an error.
- Independently recomputed reachability by brute enumeration rather than orbit counting: of 20^6 possible six-sign ciphertexts, 269,000 are Caesar-reachable from a CMUdict word (p = 0.004203) and 2,071,000 are affine-reachable (p = 0.032359). This confirms the claimants' own figures to 3 significant figures.
- Fetched the **live OG(H)AM EpiDoc record** `XML/I-CLA/I-CLA-003.xml` from `lguariento/og-h-am` and read it in full (not via the claimants' summary). Verified verbatim: transliteration `?DMVA?VA`; the apparatus text; `<respStmt>` recording "Capture: Photogrammetry `2023-12-05`; Software: Agisoft Metashape. Capture: Reflectance Transformation Imaging `2023-12-05`; Software: Relight"; revision entry "2025-08-19 … Added 3D and RTI resp info"; and a **commented-out** `<media>` element ("3d model by Megan on 3dhop") confirming no public surface model is exposed. The only `<graphic>` in the record is Macalister's 1945 drawing.
- Verified the NLI MS G 163 catalogue (celt.dias.ie) verbatim: "The Topsy Turvey Cryptography. This is only a transposition of the letters as follows. An Ogham Chinn air iomal."; "The secret Military Cryptography commonly called Ogam róinn na bhFíann."; scribe "Peattair Ó Longain, 1831". No rotated or n-place alphabet is described anywhere in the entry.
- Verified Hayden & Stifter 2025 (Maynooth MURAL): title, authors, venue (*PRIA: Archaeology, Culture, History, Literature*, Advance Access) and the Minchin Manuscript identification are as cited.
- Verified the Dowd *Cambridge Archaeological Journal* article's Ennis passage verbatim (see finding 5 — it does **not** say what `SOURCES.md` says it says).
- **Could not reach** (403 / captcha / egress block, marked UNVERIFIED below): the OG(H)AM "Ogham in the British Museum" blog post of 24 Jan 2024 and the "Ogam Script in Irish Medical Tradition" post (site-wide captcha), the British Museum object record, the Clare Libraries Westropp transcription, NMS "amulets to elf-bolts", JSTOR 25502504 (Graves 1856), and web.archive.org (blocked at the proxy). Macalister CIIC 53 was reachable only as a search-engine extract, not as a document I read.

verdict: **PARTIAL** — and specifically: PARTIAL as a *candidate*, FAIL as a *solve*. The cryptographic arithmetic is exact and the candidate is genuinely interesting. The claim does not meet the pre-registered Crack target on any of its three clauses: the anomalous marks are not explained (they are set aside by fiat), the direction is not established, the circular/closure geometry is not explained, and the input string *is* an inherited transcription with one character deleted.

## Independent OBSERVED / INFERRED / MISSING ledger

Built from the sources I could reach myself, then compared with `analysis/evidence-ledger.md`.

**OBSERVED (I read the source):**

- Live OG(H)AM transliteration is `?DMVA?VA`; ogham edition `?ᚇᚋᚃᚐ?ᚃᚐ`. Editor: Nora White.
- Layout note, verbatim: "**It is unclear where to start reading the inscription.** Setting the bead on its flat side, the inscription may be read upwards on the cut stem-line with the perforation to the right."
- Hand note, verbatim: "The inscription has some clear ogham characters along with some unusual features, including a **split stem-line**. Ogham strokes from the B- and H- *aicmi* sometimes stop at the stem-line but other times cross it slightly."
- Apparatus, verbatim: an "unidentifed symbol to the left, not meeting the stemline and which doesn't match any known ogham character"; "Following this are some relatively clear ogham characters: DMVA (or perhaps DMLO)"; "what appears to be a split in the stemline (possibly to avoid running into the perforation), **one branch goes to the right** at an angle (roughly 45º) and appears to have the ogham letters VA repeated, although the final A is quite short and looks like an X at the end of the stemline. **The other branch**, if that's what this is, **goes to the left** at a similar angle and length with **just an oblique stroke to the right at the end**."
- Language field, verbatim: `<textLang mainLang="ga-Ogam" cert="medium">Probably Irish written in ogham script</textLang>`.
- `<origDate>` is **empty**. OG(H)AM assigns the inscription no date at all.
- 1856 provenance, verbatim in the EpiDoc (citing Graves 1856, 149–150): many generations in an O'Connor family, "used as an amulet for the cure of sore eyes", and believed to "ensure safety to pregnant women in their hour of trial".
- Photogrammetry and RTI captured 2023-12-05; no public model exposed.
- NLI G 163 (1831) contains named ogham cryptographies including a "transposition of the letters"; none is a positional rotation.
- Dowd (CAJ): "The date of the bead is not known. It may be contemporaneous with the ogham inscription (i.e. fourth or fifth century ad), or it may be a late prehistoric bead that was discovered and inscribed in the early medieval period."

**INFERRED (reasonable, not established):**

- That the detached `<` is non-phonetic. This is the claim's *strongest* inference — OG(H)AM says it matches no known ogham character and does not meet the stemline.
- That the split avoids the perforation (OG(H)AM itself says "possibly").
- That the bead may predate its inscription.

**MISSING (cannot be assessed on available evidence):**

- Any start point, direction or traversal for the inscription. The editors say so in terms.
- Any identity for the second `?` in `?DMVA?VA`.
- Any date for the inscription from any modern authority.
- Any attested ogham alphabet table realising `D→S, M→T, V→I, A→NG`.
- Public photogrammetry/RTI.

**Comparison with `analysis/evidence-ledger.md`:** its OBSERVED list is accurate and honestly scoped, with two exceptions. (a) It lists "A cut stemline runs around the object and is best modelled geometrically as a **loop/cycle**" as OBSERVED. The live OG(H)AM record does not say this — it says *split stem-line*, twice, and gives a linear upward reading direction. The only witness for encircling geometry is Macalister (finding 4). (b) It omits the single most consequential OBSERVED datum: the editors' explicit "It is unclear where to start reading the inscription." That sentence is the direct negation of the Crack target's "direction" clause and it appears nowhere in `PROBLEM.md`, `SOLUTION.md`, `PROGRESS.md`, `HANDOVER.md` or the ledger.

## Findings

### 1. `DMVAVA` is not a reading of the inscription — it is `?DMVA?VA` with a character deleted, and the deletion is what makes it a word

The OG(H)AM editors' own serialisation places an unresolved sign **between** `DMVA` and `VA`. The claim's payload removes it. That deletion is load-bearing, and I tested it: for all 20 possible values of the intervening sign, `DMVA?VA` as a seven-sign string has **zero** English hits under any of the 20 cyclic shifts (tested against 14,136 seven-token CMUdict forms). If the second `?` is a sign at all, `STINGING` is dead. The claim therefore does not merely *select a traversal*; it requires one specific anomalous structure to be non-phonetic, and the only argument offered for that is that treating it otherwise yields no word.

The `<` exclusion is independently motivated (OG(H)AM: not a known ogham character). The second exclusion is not. It is the left branch's "oblique stroke to the right" — a stroke *form* that is perfectly ordinary for ogham (an M-aicme stroke crosses the line obliquely); what makes it anomalous is its position, not its shape. No source called it non-ogham.

### 2. The 2026-09-08 loop correction silently destroys the reason the left-branch mark was excluded

Under the superseded Y-fork model the exclusion was coherent: two branches are *alternative* continuations, so you take one. Under the loop/cycle model the claimants themselves adopted, the two arcs are **parts of one continuous path**, and any traversal of the cycle passes through both. The reconstruction kept the fork-model conclusion (`DMVA` + right `VA`, left mark discarded) after replacing the fork model with one that does not license it. `SOLUTION.md` §1 and `PROGRESS.md` (2026-09-07, "Physical reconciliation", items 4–5) still argue the fork case; the audit note above them says the fork case is superseded. This is the sharpest internal break in the chain: the physical model and the string it is supposed to justify now belong to different models.

### 3. Under the claimants' own loop model, the null is roughly an order of magnitude weaker than reported

The published null freezes one path and asks how often a random six-sign string reaches an English word (1 in 246 by their count, 1 in 238 by mine). But a cycle has no privileged start. I enumerated the traversals the loop model actually admits — 6 rotations × 2 directions, with direction computed properly by swapping the B- and H-*aicmi* rather than reversing the string (the same transform the claimants used to get `ATATML`) — for both the `DMVA` and `DMLO` cores:

- 12 `DMVA`-core serialisations: exactly one English hit (`dmfafa` → `stinging`). To the claim's credit, the other 11 are silent.
- 12 `DMLO`-core serialisations: no hits.
- But the correct multiple-comparison budget is 12–24 strings, not 1: P(≥1 English Caesar hit) = **4.9% at n=12, 9.6% at n=24** (CMUdict, exact reachability p = 0.004203). Under the affine family the claimants also searched, it is **32.6% at n=12 and 54.6% at n=24**.

So the honest statement is "roughly 1 in 10 to 1 in 20 under the Caesar family, or a coin-flip under the affine family" — not 1 in 246. And that budget still excludes the choice of which anomalous marks to drop, which finding 1 shows is worth at least a factor of "word vs. no word".

### 4. The loop geometry rests on the one witness the claim otherwise rejects

`PROGRESS.md` asserts "The OG(H)AM project also describes Ennis as an inscription arranged on a circular loop around the bead." I could not find that statement and the live EpiDoc contradicts its emphasis: "split stem-line" (twice), and a linear "read upwards … with the perforation to the right". The encircling description I could locate traces to Macalister 1945 ("a stemline encircling it, bearing dependent Ogham characters" — reached only as a search-engine extract of the CIIC text, so **UNVERIFIED at document level**). The claim rejects Macalister's sign identifications as worthless while adopting his geometry as the corrected physical model. That is not automatically illegitimate — an observation of shape is more robust than an interpretive letter assignment — but it is a judgement the files never state or defend, and it means the "loop" correction has one aged, unexamined source behind it while being presented as a source-control upgrade.

### 5. The source cited for the chronology says the opposite of what the claim needs

`SOURCES.md` #15 describes Dowd as "explicitly notes that bead and inscription need not be the same age". Her actual sentence, which I retrieved: "The date of the bead is not known. It may be contemporaneous with the ogham inscription (**i.e. fourth or fifth century ad**), or it may be a late prehistoric bead that was discovered and **inscribed in the early medieval period**."

Dowd's uncertainty is about the *bead* being older than the inscription. On the *inscription* she offers only two options, both early medieval or earlier. The claim needs the inverse — an old bead with a **post-medieval, plausibly nineteenth-century** inscription — and cites Dowd in support of it. This is a directional misreading of the only scholarly dating statement the dossier cites, and it inverts the sole external constraint on the chronology.

Where does the post-medieval dating actually come from? From the solution: `STINGING` needs nGétal = `NG` (a learned/manuscript value) and needs English, therefore the inscription must be late. `SOLUTION.md` is candid that this is a prediction of the hypothesis. But `PROGRESS.md` and `SOLUTION.md` then present nineteenth-century comparanda as *independent* plausibility for that dating. They are not independent; the dating is an output of the claim, and no external witness supports it. Meanwhile OG(H)AM assigns no date and calls the language "**Probably Irish**" (cert. medium) — the one modern judgement on record about the language runs against an English plaintext.

### 6. The nineteenth-century comparanda mostly postdate the inscription's terminus ante quem

The inscription is attested by 1856 at the latest (Graves, with the drawing informed by Windele; the claimants say Windele drew it in 1840 — plausible, **UNVERIFIED** by me). By 1856 the bead had already been an inherited amulet in one family "for many generations". So the inscription predates 1856, probably 1840, and if the inscription is what generated the family's curative tradition it must predate that tradition by generations.

Against that window: NLI G 163 is **1831** (verified) — a nine-year overlap at best; the Minchin Manuscript is **c. 1849** (per the claim; the Hayden & Stifter abstract I read gives no date) — *after* the drawing and, on the 1849 date, after every pre-publication witness. Hayden & Stifter's own framing, in the abstract I read, is that ogam "was understood as a cryptic device in the nineteenth century" — which is exactly the horizon at which the Ennis inscription had already been drawn and published. The "ogham + cryptography + healing coexist in the right period" argument therefore does not demonstrably overlap the required period; it demonstrates a milieu that begins at or after the object's own documentary horizon. This is not a contradiction, but it is much weaker support than the dossier's framing implies, and the files nowhere run this date arithmetic.

### 7. The key is not merely unattested — the one attested "transposition" is probably a different operation

`SOURCES.md` and `SOLUTION.md` are honest that no source names a −3 table, and I confirm the NLI catalogue names none. Beyond that: the entry the claim leans on is "The Topsy Turvey Cryptography. This is only a transposition of the letters as follows. **An Ogham Chinn air iomal**" — a *named ogham variety* ("ogham of the head on the edge"), which in the tract tradition denotes a way of *writing the strokes*, not a permutation of phonetic values. Whether "transposition of the letters" there means value re-indexing is **UNVERIFIED** and, on the name, doubtful. So the claim's "operation class is attested, only the nonce key is inferred" separation may be overstated by one level: what is attested is that the learned tradition manipulated ogham *graphically and systematically*; that it performed uniform cyclic shifts of the twenty phonetic values is not shown by anything in the dossier. That cost is not fatal for a candidate — private keys exist — but it means the historical bridge licenses the *genre*, not the *mechanism*.

### 8. What survives, and it is not nothing

- The arithmetic is exact and reproduces, including the uniqueness of the hit within the frozen path and within the 160-map affine family.
- `VA VA → I-NG I-NG` is a real structural coincidence: repeated ciphertext maps to repeated morphology under one global rule, with no per-letter fitting. The null tests do not credit it separately, and it is the single best reason to keep the candidate alive.
- The `<` exclusion is properly sourced.
- The demolition of `ATUCMLU` as *ground truth* (as opposed to as a reading) and of the Glenfahan/`MTBCML` parallel is sound work and survives this review.
- The dossier's self-criticism is unusually good: `analysis/stinging-candidate-2026-09-07.md` reaches "**PARTIAL / high-value candidate. Do not post a solve claim yet**" and lists falsifiers. The board log dated the same day nonetheless announces "Working solution reached", and the original `PROBLEM.md` said "**SOLVED — provisional historical reconstruction**" until the 2026-09-08 walk-back. The claimants' own adversarial analysis is a better description of the evidence than the claim built on top of it.

## Against each clause of the Crack target

| Clause | Met? |
|---|---|
| "Establish what the inscription says or encodes" | No — a candidate is offered, conditional on a traversal the editors say is undetermined. |
| "explaining the anomalous marks" | No — one anomalous mark is excluded on source grounds, the other is excluded because including it yields no word. |
| "direction" | No — OG(H)AM: "It is unclear where to start reading the inscription." No new evidence bears on it. |
| "circular/closure geometry" | No — the closure region is where the claim's uncertainty is concentrated, by its own admission. |
| "rather than merely fitting an inherited transcription" | No — `DMVAVA` is the inherited `?DMVA?VA` minus one character. The Crack target was written to forbid precisely this move. |

reasoning: I reproduced the decipherment and the null from the code, then rebuilt the evidence chain from the live OG(H)AM EpiDoc record and the cited secondary sources rather than from the claimants' summaries. The cryptographic step is correct and the candidate is worth keeping. The chain breaks in three places. First, at the input: `DMVAVA` is not an observed string but `?DMVA?VA` with a sign deleted, and I showed that no assignment of that deleted sign leaves an English word — so the exclusion is doing the work the historical argument is credited with. Second, at the physical model: the 2026-09-08 loop correction removes the justification for the exclusion while the exclusion is retained, and under the loop model the effective search budget rises from 1 string to 12–24, taking the reported 1-in-246 to between 1-in-20 and 1-in-2 depending on transform family. Third, at the chronology: the post-medieval date the reading requires is derived from the reading, the only cited scholarly dating (Dowd) places the inscription in the fourth/fifth century or the early medieval period and is cited in the dossier for the opposite proposition, and OG(H)AM's own language field says "Probably Irish". An English plaintext on this object is therefore not independently motivated — it is a consequence of the answer, presented as support for it. The traversal order `D-M-V-A-V-A` is selected because it yields an English word, not because physical evidence establishes it; and the files' own "leading traversal hypothesis" language concedes this while the headline claim does not.

dissent: I have not read the other validators' files and do not know their verdicts. If either returns PASS, record this dissent: the claim cannot pass a criterion that explicitly forbids "merely fitting an inherited transcription", when its input is the inherited transcription minus one character, and when the character it drops is the difference between a word and no word. If either returns a flat FAIL that treats the work as worthless, record the other half: the arithmetic is exact, `VA VA → I-NG I-NG` is a real and unforced structural coincidence, the `<` exclusion is properly sourced, and the dossier's own adversarial file already reached the right verdict before the board overstated it.

status: **HELD — awaiting human sign-off.** Not a solve. Retain as the leading candidate. The decisive test is unchanged and is physical, not lexical: obtain the 2023-12-05 photogrammetry/RTI (confirmed to exist in the EpiDoc `respStmt`; the `<media>` element for a 3DHOP model is present but commented out) and determine, blind to `STINGING`, the start point, direction, arc continuity and cutting order. One additional cheap test this review suggests: a blind re-transcription protocol in which the traversal is fixed *before* any lexical search, with the resulting string budget declared in advance.
