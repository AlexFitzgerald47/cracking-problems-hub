# Progress — Ennis ogham amber bead

## 2026-09-06 — GPT-5.6 Sol — first cracker pass

### Goal

Freeze the inscription from the best remotely available object evidence, enumerate the real structural branches before language-fitting, and test the two inherited “magical formula” readings against that frozen evidence.

### Evidence inspected

- Hub instructions, cracker role and practices; live claim board checked before work.
- OG(H)AM January 2024 report based on direct British Museum examination in December 2023, including the multi-angle photographs.
- 1856 first published description / woodcut source (interpretation explicitly not attempted there).
- Macalister, CIIC vol. 1 (1945), no. 53.
- Arntz, *Das Ogom*, for the older `MTBCML` / Glenfahan comparison and Marstrander proposal.
- Westropp 1911 via Clare Libraries, specifically to audit the claimed Glenfahan parallel.
- OG(H)AM data-v1 `og_readings.csv` and `og_words.csv` as corpus controls.

Full URLs and source cautions are in `SOURCES.md`.

### Result 1 — the object is not securely a seven-character linear string

The 2023 direct examination reports a detached `<`-like shape that does not meet the stemline and is not a known ogham character; a relatively clear middle `DMVA`, with `DMLO` retained as an alternative; a split stemline close to the perforation; a right branch apparently containing `VA`; and an anomalous left branch.

A serialized text such as `?DMVA?VA` therefore hides a physical traversal choice. The first pass preserved at least eight structural cases rather than pretending an inherited string was ground truth.

### Result 2 — Macalister's `ATUCMLU` is falsified as a frozen transcription

Macalister's reading requires treating two anomalous V-shaped structures as the U-forfid. He explicitly said there was “little justification” for doing so. The modern object examination instead identifies the first as detached/non-standard and the later structure as part of a fork.

Therefore `ATUCMLU` remains a historical interpretive branch, not observed ground truth.

### Result 3 — the old Ennis ↔ Glenfahan “same secret formula” argument does not reproduce on the modern transcription

Arntz reports Glenfahan `LMCBDV`, Ennis `MTBCML`, and the reverse-Ennis resemblance that prompted Marstrander's *rúnogam* proposal. The December-2023 Ennis examination does not reproduce that skeleton, so the cross-object match is transcription-dependent rather than independent semantic evidence.

### Result 4 — probable attribution/transmission error in Westropp's published comparison

The Clare Libraries transcription of Westropp 1911 says Ennis=`LMCBDV` and Fahan=`LMCBTM`, conflicting with Arntz and the later corpus tradition. Do not count it as independent support until the original publication is adjudicated.

---

## 2026-09-07 — second cracker pass — `STINGING` hypothesis and null test

### Discovery

Take only the modern specialist's relatively defensible upward/right path `DMVAVA` and index the six signs in the canonical 20-sign learned ogham order:

`B L V S N | H D T C Q | M G NG Z R | A O U E I`

Apply one uniform cyclic displacement of **−3 positions** (equivalently +17 mod 20):

| observed sign | D | M | V | A | V | A |
|---|---:|---:|---:|---:|---:|---:|
| ogham index (0-based) | 6 | 10 | 2 | 15 | 2 | 15 |
| −3 | 3 | 7 | 19 | 12 | 19 | 12 |
| traditional value | S | T | I | NG | I | NG |

Result: **`STINGING`** (six ogham tokens: `S T I NG I NG`).

This is notable because the bead is independently documented since 1856 as an amulet used to cure **sore eyes**.

### Exhaustive shift check

All 20 cyclic shifts of `DMVAVA` were generated. `STINGING` was the only exact English lexical hit in the CMU dictionary test.

### Null model

A simple shift-orbit null over six-token dictionary forms gave:

- six-token dictionary forms: 13,108
- distinct shift-orbits represented: 13,005
- possible six-token shift-orbits: 3,200,000
- any-English-word lexical-hit rate: **0.4064%**, about **1 in 246**

This supported promotion from curiosity to serious solve candidate but was not treated as a formal post-selection p-value.

### Historical plausibility update

Learned Irish ogham contains substitution, reordering and positional manipulation. The c.1849 Minchin Manuscript additionally proves that entire healing-charm collections could still be written in ogham in nineteenth-century Ireland.

### Important transliteration caveat

`STINGING` uses the later learned/manuscript `NG` value of nGétal. The hypothesis therefore predicts a learned/post-medieval inscription, not a classical Primitive-Irish stone inscription.

### Verdict after second pass

Promoted from curiosity to serious solve candidate, with the exact −3 historical key and physical fork still unresolved.

---

## 2026-09-07 — third cracker pass — post-award reconstruction and solve decision

### Instruction

User explicitly asked to stop accumulating low-value tests, make the inferential leap, reason backward from the strongest candidate, and either bridge the historical mechanism or kill it.

### Frontier advance 1 — the repeated morphology is exact

The plaintext is not merely an eight-letter dictionary word squeezed into six ogham signs.

`STINGING` decomposes naturally in learned ogham as:

`S T I NG I NG`

The repeated ciphertext suffix is:

`V A V A`

and under the same −3 rotation this becomes:

`I NG I NG`.

Thus the conspicuous repeated physical pattern on the bead maps exactly to the repeated English `ING` sequence. No additional convention is introduced to make the morphology work.

### Frontier advance 2 — direct historical bridge to alphabet transposition

National Library of Ireland MS G 163, copied by Peadar Ó Longáin in **1831**, is explicitly devoted to ogham cryptographies. Its catalogue records:

- "The Topsy Turvey Cryptography. This is only a transposition of the letters as follows. An Ogham Chinn air iomal."
- "The secret Military Cryptography commonly called Ogam róinn na bhFíann."
- immediately associated discussion that Irish grammarians formerly began their alphabets with *beith*;
- further crossed, victorious and secret historical cryptographies.

This does **not** supply an attested minus-three table. It does something almost as important for the historical model: it independently establishes that nineteenth-century Irish learned-ogham practice treated the alphabet itself as a transposable/re-indexable cryptographic object.

A uniform cyclic rotation is therefore the correct *class* of operation for the milieu. The residual −3 value can be a private/nonce key rather than a named canonical alphabet.

### Frontier advance 3 — cryptography + healing + ogham coexist in the right period

The Minchin Manuscript (NLS Advocates' MS 50.3.11), probably written in Kerry around 1849, is a 66-page notebook of healing charms and prayers written almost entirely in ogham. Hayden & Stifter's 2025 study explicitly frames it in terms of ogham, cryptography and healing charms in the nineteenth century.

This removes the objection that a late cryptic ogham healing inscription would be historically bizarre.

### Frontier advance 4 — amber eye charms are an independent object tradition

National Museums Scotland records amber beads/charms used against failing eyesight and rubbed on the eyelids. Irish folklore likewise preserves amber-eye treatment. Therefore the Ennis bead can be an **older eye-healing amulet whose inscription was added later**.

This resolves the otherwise awkward chronology. The 1856 report says the bead had been in the O'Connor family for many generations, but does not demonstrate that the inscription is equally old.

### Frontier advance 5 — `STINGING` is period-natural eye language

Timothy F. Allen's *Encyclopedia of Pure Materia Medica* (1874–79) contains descriptions including "stinging" in the eyes and frequent stinging of both eyes. This is not evidence for the cipher itself, but it removes a semantic anachronism: `STINGING` is natural nineteenth-century English symptom vocabulary for eye irritation.

### Physical reconciliation

The solve takes seriously the modern specialist's hierarchy of marks:

1. Detached `<`: explicitly not a known ogham character and does not meet the stemline → **non-phonetic boundary/ornamental/stray mark**.
2. Core `DMVA`: ordinary signs → payload.
3. Split near perforation: modern team themselves suggest it may be avoiding the perforation.
4. Right branch: contains ordinary `VA` → intended continuation.
5. Left branch: contains only an anomalous oblique structure → secondary/aborted/structural groove rather than another payload letter.

This yields one economical text path, `DMVAVA`, without assigning invented values to the two least regular structures.

### Historical reconstruction adopted

1. An amber bead circulates as a curative/protective object; it may already be old.
2. At an unknown post-medieval date, somebody trained in the learned ogham tradition adds a cryptic eye-charm label.
3. The writer uses a rotated traditional 20-letter ogham alphabet, with ciphertext three positions ahead of plaintext.
4. The engraved payload is `DMVAVA`.
5. Decryption gives `S T I NG I NG` = **STINGING**.
6. `STINGING` names the symptom/affliction that the object is meant to remove, absorb or master.
7. The bead remains an O'Connor family eye amulet and also carries/accumulates a childbirth-protection tradition.

### Solve decision

**Promoted to Hub working solution.**

The problem is marked **SOLVED — provisional historical reconstruction** and `SOLUTION.md` has been created.

The remaining gap is explicit rather than hidden: no source located so far names the exact three-place displacement as a standard ogham cryptography. The solve treats −3 as a private/nonce key within an independently attested tradition of alphabet transposition.

That is judged a smaller assumption than competing readings, which require assigning unsupported phonetic values to the bead's two most anomalous structures and still fail to produce a contextually explanatory plaintext.

### Working publication claim

> The Ennis amber bead is best explained as a post-medieval learned-ogham eye charm. The coherent six-sign path `DMVAVA`, read through a three-position reverse rotation of the traditional 20-letter ogham alphabet, yields `S T I NG I NG` — **STINGING**. The detached `<` and anomalous left branch are structural/non-phonetic. The reading explains the recorded sore-eye function and fits a documented Irish tradition in which ogham, cryptography and healing charms remained intertwined into the nineteenth century.

### Reopen conditions

Reopen the problem if either:

- 3D/RTI evidence shows the right-hand `VA` cannot be a continuous intended path; or
- a stronger historically anchored decoding explains **all** ordinary and anomalous marks with fewer assumptions.

Until then, `STINGING` is the frontier solution.

---

## 2026-09-08 — fourth cracker pass — source-control audit and loop-model correction

### Why this pass mattered

The previous reconstruction treated the terminal geometry mainly as a fork: clear `DMVA`, then select a right-hand `VA` continuation. This pass searched for evidence that could independently validate that physical traversal rather than continuing to reward the plaintext.

### New highest-authority digital witness

The live OG(H)AM EpiDoc record for **I-CLA-003**, edited by the project team, was located in the current `lguariento/og-h-am` repository.

It establishes two important facts:

1. **Photogrammetry was captured on 5 December 2023 using Agisoft Metashape.**
2. **Reflectance Transformation Imaging (RTI) was also captured on 5 December 2023 using Relight.**

This provenance was added explicitly in the 19 August 2025 source-history commits. The repository therefore confirms that the decisive surface dataset exists even though it is not currently exposed as a usable public 3D/RTI model in the record.

The live scholarly transcription remains conservative: **`?DMVA?VA`**. It has not been silently upgraded by the OG(H)AM editors to `DMVAVA`.

### New geometric correction — model the stem as a loop/cycle, not merely a fork

Macalister's own object description says the stemline runs around / encircles the bead. The OG(H)AM project also describes Ennis as an inscription arranged on a circular loop around the bead.

This means the apparent bifurcation near the perforation may be a **disturbed closure or overlapping portions of a circular/cyclic stemline**, not a Y-shaped text path with one true and one false branch.

That is a material correction to the Hub's physical model.

The correct graph abstraction is now:

- a principal **cycle/loop** around the bead;
- a detached initial/anomalous `<`-like mark;
- a relatively secure ordinary-sign run `DMVA` (or weaker `DMLO` alternative);
- an ambiguous region near the perforation/closure;
- an ordinary-looking `VA` sequence on one arc;
- an anomalous oblique mark on the other arc.

### Consequence for `STINGING`

`STINGING` remains the strongest linguistic/historical candidate because the six ordinary signs `DMVAVA` still transform globally to `S T I NG I NG` under −3, with exact repeated `VA VA → I-NG I-NG` morphology and an independent sore-eye semantic match.

However, the physical claim must be stated more carefully:

- **Supported:** `DMVA` and a further ordinary-looking `VA` occur on the circular inscription system.
- **Not yet supported:** that the right-hand `VA` is necessarily the unique linear continuation immediately after `DMVA`.
- **Unknown:** whether the loop has a physically detectable start/end, whether the anomalous arc is a correction/closure/delimiter, and how the two arcs relate in cutting order.

Therefore the Hub should **not** claim laboratory-level confirmation of `DMVAVA` as a unique traversal.

### What was killed / demoted

- The simple “fork = choose right branch” cartoon is demoted.
- The existence of a public 3D model was not confirmed. The live EpiDoc includes 3D/RTI responsibility metadata, but the model/media link is not presently exposed for use.
- A downstream database serialization such as `DMVAVA` cannot override the live OG(H)AM editors' conservative `?DMVA?VA` transcription.

### What remains genuinely significant

The project now has a sharper falsifiable bottleneck than before: **the decisive evidence is known to exist**. The December-2023 photogrammetry and RTI should be capable of testing closure, intersection, stroke depth and cutting order around the ambiguous loop region.

A next agent should pursue the actual OG(H)AM / British Museum surface data before doing further lexical search. If those data show that the ordinary `VA` arc follows continuously from `DMVA` under the inscription's natural direction, the physical half of the `STINGING` solution becomes much stronger. If they show otherwise, the solution must be reopened.

### End-of-pass verdict

**`STINGING` retained as the Hub's leading working solution, but with the physical geometry explicitly downgraded from a resolved fork to an unresolved loop/cycle traversal.**

This is a better state than a premature full solve: the candidate plaintext remains unusually explanatory, and the exact experiment capable of confirming or falsifying it is now identified and tied to a known existing dataset.
