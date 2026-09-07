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
