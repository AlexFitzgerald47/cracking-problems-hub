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

The 2023 direct examination reports:

- a detached `<`-like shape that does not meet the stemline and is not a known ogham character;
- a relatively clear middle `DMVA`, with `DMLO` retained as an alternative;
- a **split stemline** close to the perforation;
- a right branch apparently containing `VA`;
- a left branch ending in a separate oblique stroke.

That topology matters. A serialized text such as `?DMVA?VA` hides a choice about how a reader traverses a physical fork. The conservative upward-orientation graph already has four path serialisations (`?DMVAVA`, `?DMVA?`, `?DMLOVA`, `?DMLO?`). Allowing the opposite reading direction gives a lower bound of **8 structural cases** before assigning values to either anomalous mark. See `analysis/evidence-ledger.md` and `code/branch_model.py`.

### Result 2 — Macalister's `ATUCMLU` is falsified as a frozen transcription

Macalister's reading requires treating two anomalous V-shaped structures as the U-forfid. He explicitly said there was “little justification” for doing so. The modern object examination instead identifies the first as detached/non-standard and the later structure as part of a fork.

Therefore `ATUCMLU` remains a historical interpretive branch, but it is **not sufficiently secure to be the ciphertext/plaintext target**. Searching dictionaries or cryptic-ogham tables for meanings of `ATUCMLU` without first resolving the marks is downstream of an unstable input.

### Result 3 — the old Ennis ↔ Glenfahan “same secret formula” argument does not reproduce on the modern transcription

Arntz reports Glenfahan `LMCBDV`, Ennis `MTBCML`, and the reverse-Ennis resemblance that prompted Marstrander's *rúnogam* proposal. The December-2023 Ennis examination does not reproduce that skeleton, so the cross-object match is transcription-dependent rather than independent semantic evidence.

### Result 4 — probable attribution/transmission error in Westropp's published comparison

The Clare Libraries transcription of Westropp 1911 says Ennis=`LMCBDV` and Fahan=`LMCBTM`, conflicting with Arntz and the later corpus tradition. Do not count it as independent support until the original publication is adjudicated.

---

## 2026-09-07 — second cracker pass — `STINGING` hypothesis and null test

### Discovery

Take only the modern specialist's relatively defensible upward/right path `DMVAVA` and index the six signs in the canonical 20-sign ogham order:

`B L V S N | H D T C Q | M G NG Z R | A O U E I`

Apply one uniform cyclic displacement of **−3 positions** (equivalently +17 mod 20):

| observed sign | D | M | V | A | V | A |
|---|---:|---:|---:|---:|---:|---:|
| ogham index (0-based) | 6 | 10 | 2 | 15 | 2 | 15 |
| −3 | 3 | 7 | 19 | 12 | 19 | 12 |
| traditional value | S | T | I | NG | I | NG |

Result: **`STINGING`** (six ogham tokens: `S T I NG I NG`).

This is notable because the bead is independently documented since 1856 as an amulet used to cure **sore eyes**. “Stinging” is therefore semantically related to the specific traditional ailment, not merely a generic English word.

### Exhaustive shift check

All 20 cyclic shifts of `DMVAVA` were generated. Under the same traditional ogham token values, the outputs are:

`DMVAVA, TGSOSO, CNGNUNU, QZHEHE, MRDIDI, GATBTB, NGOCLCL, ZUQVQV, REMSMS, AIGNGN, OBNGHNGH, ULZDZD, EVRTRT, ISACAC, BNOQOQ, LHUMUM, VDEGEG, STINGING, NCBZBZ, HQLRLR`.

Against the local CMU English pronunciation dictionary (~126k raw entries), **STINGING was the only exact lexical hit** among the 20 shifts.

### Null model

A stronger null was run over the dictionary rather than merely noting the hit.

Method:

1. Normalize dictionary entries to alphabetic forms.
2. Tokenize `NG` as one ogham sign and map English F to the same traditional fern slot represented epigraphically as V.
3. Retain words occupying exactly six ogham tokens.
4. Canonicalize each six-token word under all 20 global cyclic shifts of the ogham alphabet.
5. Ask what fraction of the `20^5 = 3,200,000` distinct shift-orbits contain at least one dictionary word.

Result:

- six-token dictionary forms: 13,108
- distinct shift-orbits represented: 13,005
- random six-token shift-orbit lexical-hit rate: **13,005 / 3,200,000 = 0.004064 = 0.4064%**

So under this deliberately simple null, obtaining *some* English dictionary word from a random six-token ogham sequence after trying all 20 cyclic shifts is about **1 in 246**. This is interesting but nowhere near enough by itself to establish decipherment.

The repeated geometry gives a second useful constraint: `DMVAVA` has token pattern `A B C D C D`, with the first four tokens distinct. Only 22 six-token CMU entries matched that repetition pattern in the filtered dictionary; examples include `STINGING`, `SLINGING`, `CRINGING`, `BRINGING`, `CLINGING`, `FLINGING`, `CRISIS`, `THESES` and several proper names. Crucially, **only `STINGING` occupies the exact cyclic-shift orbit of `DMVAVA`**.

### Historical plausibility update

The cipher mechanism is no longer generically anachronistic. `In Lebor Ogaim` preserves over 100 cryptic ogham systems involving substitution, reordering and positional manipulation. The OG(H)AM project specifically documents `Ogam Féniusa`, where letters are paired with following letters within an aicme, and other substitution/reordering systems. This establishes that ogham-alphabet positional manipulation is historically real.

However, **no source has yet been found for this exact global Caesar −3 transformation**. That is the largest cryptographic weakness in the `STINGING` proposal.

A major contextual update strengthens the *late healing-charm* prior independently of the wordplay: Hayden & Stifter (2025) document the Minchin Manuscript, a 66-page Irish notebook probably written in Kerry around 1849 containing at least 59 healing charms and prayers, almost entirely in ogham. This demonstrates that ogham was genuinely being used for healing charms in nineteenth-century Ireland, not merely by modern revivalists. The Ennis bead was published as a healing amulet in 1856. This does **not** prove that its inscription is nineteenth-century, but it makes a late antiquarian/healing-ogham inscription a serious competing date model.

### Important transliteration caveat

The `STINGING` reading uses **traditional manuscript values** for two signs:

- fern as V/F occupies the third alphabet slot;
- nGétal as `NG` occupies the thirteenth.

Modern historical-linguistic reconstruction gives nGétal an earlier value approximately /gʷ/ and straif approximately /st/, while the medieval tradition labels them NG and Z/ST in different conventions. Therefore `STINGING` specifically predicts an inscription/cipher maker operating from the **later learned/manuscript ogham tradition**, not a classical Primitive-Irish stone-carver's phonemic system. This is a useful falsifiable dating prediction.

### Current verdict on `STINGING`

**Promoted from curiosity to serious solve candidate, but NOT declared solved.**

Reasons for promotion:

1. exact output from one uniform operation on the best modern six-sign path;
2. unique English lexical hit across all 20 shifts;
3. simple null lexical-hit rate only ~0.4%;
4. output has unusually specific semantic fit to the independently recorded sore-eye function;
5. nineteenth-century Irish healing charms written in ogham are now independently attested;
6. learned ogham traditions demonstrably contain positional/substitution ciphers.

Reasons not to declare victory:

1. exact Caesar −3 key is not yet historically attested;
2. the six-sign `DMVAVA` path is still physically uncertain because of the fork;
3. the semantic fit was evaluated post hoc, so 0.4064% is **not** a valid final p-value for the whole discovery process;
4. `STINGING` implies later learned values and likely English, hence a late inscription; that needs independent material/palaeographic support;
5. anomalous detached `<` and left fork remain unexplained under this solution.

### Highest-value falsification tests now

1. Search the complete *In Lebor Ogaim* keys for an exact ±3/global positional substitution, or a rule that produces the same mapping `D→S, M→T, V→I, A→NG`.
2. Test the same 20-shift procedure across **all** defensible Ennis path/orientation serialisations, with a predeclared dictionary/corpus and correction for the full branch budget.
3. Compare Ennis ductus with nineteenth-century antiquarian/healing ogham, especially the 1849 Minchin Manuscript, versus medieval portable ogham.
4. Resolve whether the detached `<` and terminal fork can be read as delimiters/feather marks or whether they falsify the six-token path.
5. Obtain the project's 3D/photogrammetric surface record if published and use intersections/tool profiles to select the true path.

### Frontier position

The strongest live hypothesis is now concrete and falsifiable:

> **A later learned-ogham charm maker wrote `DMVAVA`; applying a uniform −3 displacement in the traditional 20-letter ogham order yields `STINGING`, a word specifically matching the bead's documented sore-eye healing function.**

This is substantially stronger than the inherited `ATUCMLU`/Glenfahan formula because it starts from the modern direct examination and has a measurable null. It remains provisional until the cipher rule and physical path receive independent support.
