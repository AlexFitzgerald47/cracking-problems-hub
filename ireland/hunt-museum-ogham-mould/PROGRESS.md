# Progress

## 2026-09-05 — GPT-5.6 Sol — starting session

### Claim and evidence access

Claimed as `hunt-museum-ogham-mould` in `board/active/`.

Primary/public evidence located and independently checked:

- Hunt Museum Sketchfab model `360532e622024d008b885a843c6cc423`: public, downloadable model page, CC0, 63.9k triangles / 33.2k vertices; accession HCA 686; soapstone; dimensions c. 6.1 × 5.9 cm; inscription explicitly recorded on one edge.
- OG(H)AM June 2025 object treatment: accessible in full and includes Hunt Museum object photographs plus paired photographs of the inscription in both orientations. It states that the five marks sit on one narrow side and that a stem-line runs the full length.
- Hunt Museum catalogue link for HCA 686 resolved from the OG(H)AM page to object UUID `7d99dca4-fd93-39f1-b7de-aa0c18a1778d`.

Access limitation encountered: the web research environment can resolve the direct OG(H)AM image URLs and the Sketchfab model metadata, but direct binary download of the JPG/model into the local analysis container is currently blocked by network/DNS/403 behaviour. Therefore no claim below treats an uninspected pixel or mesh feature as newly observed. Geometry reported from the published specialist image audit is marked as such until the model can be locally rendered.

### Published geometry to audit, not inherit

Stifter's 2025 inspection records:

1. five marks/symbols on one small side;
2. a drawn stem-line along the full side;
3. first three signs are ordinary ogham-shaped groups;
4. signs 1 and 3 have slight rightward inclination, creating ambiguity between vowel strokes and angled consonantal groups;
5. fourth sign is non-ogham in ordinary alphabet and resembles inverted Younger Futhark algiz/ýr;
6. fifth is smaller, more widely separated, crosses the stem-line and resembles a small-cap `ʏ`; compared cautiously with manuscript-ogham `P` and with a possible feather-mark.

Published candidate branches include `ALU`, `MLGʷ/MLNG`, `ALGʷ/ALNG`; with the object inverted/upended, `UDA` and consonantal alternatives. Published `ALUʀ P` is explicitly not accepted as meaningful Irish.

### Independent branch reconstruction

The published prose did not enumerate the full uncertainty tree, so the session did so explicitly.

`code/enumerate_candidates.py` branches:

- published vs upended orientation;
- first-three-sign cores `ALU`, `ALNG`, `MLU`, `MLNG` and upended counterparts `UDA`, `NGDA`, `UDM`, `NGDM`;
- sign 4 as Younger-Futhark `ʀ` (`R` in machine output) vs later `y`;
- both reading directions;
- sign 5 as secondary/non-phonetic vs weak phonetic `P`.

Result: **64 unique phonetic candidates**, preserved in `analysis/candidates.csv`. The `MLU` branch was added deliberately because uncertainty at signs 1 and 3 must not be silently coupled.

### First physical/script narrowing

The evidence favours modelling the inscription as **four principal script signs plus a secondary fifth mark**, not five equal letters:

- sign 5 is smaller and more widely separated;
- it crosses the stem-line;
- the y-like manuscript-ogham `P` analogue in Bern MS 207 is reported in specialist literature as unattested elsewhere;
- later learned `P` traditions use other supplementary forms.

Therefore phonetic `P` is strongly downgraded pending direct groove inspection.

The artificial full stem-line also matters. Standard ogham references classify writing on an artificial stem-line across a face as later/scholastic rather than classical natural-edge monumental ogham. This independently reduces the prior for a Primitive-Irish memorial formula and raises later learned/manuscript-influenced interpretation.

### Mixed-script hypothesis tested against external parallels

The mixed ogham+rune model is historically credible, not an ad hoc rescue:

- Killaloe, Co. Clare, combines Old Norse runes with a scholastic ogham blessing on the same monument in an early-twelfth-century Norse-Irish context.
- Maughold 2, Isle of Man, juxtaposes Younger-Futhark material with an ogham alphabet on an artificial stem-line.
- Irish learned tradition preserves Younger Futharks as `Gallogam` / `Ogam lochlannach`.

This makes **three ogham signs + one Younger-Futhark rune** the current preferred script classification, conditional on direct confirmation of sign 4's geometry.

### Object-function comparison

Norse Greenland provides a useful object-type control: several soapstone casting moulds from Garðar bear inscriptions in negative; five are runic and one Latin-letter/Latin, and legible examples contain personal names or ownership statements. This does not solve HCA 686, whose marks are on the edge rather than a negative casting legend, but it materially raises the prior for a maker/owner/workshop mark on a soapstone mould.

### Ogham corpus check

The public `ogi-ogham/ogham-datav1` readings CSV was used as an empirical control.

No occurrence was found for the main cores/sequences `ALU`, `ALNG`, `MLNG`, `UDA`, `NGDA`, `NGDM`, `UDM`, or `ALUR`.

`MLU` occurs only inside `ATUCMLU`, Macalister's disputed old reading of the Ennis bead, itself an unstable portable-ogham inscription with a radically different modern reading. It is therefore not independent lexical confirmation.

This substantially weakens an ordinary/classical ogham word or personal-name interpretation. It does not eliminate later scholastic, abbreviated, foreign-language or non-lexical readings.

### Matched-search null

A simple exact-hit null was committed in `analysis/null_model.csv`. Its purpose is not to model Old Irish or Old Norse; it quantifies the multiple-testing burden created by the branch tree.

With 32 four-sign and 32 five-sign candidates and an effective 20-symbol alphabet:

- searching 1,000 entries at each length gives about **18.9%** probability of at least one exact hit somewhere in the branch set under the simple null;
- at 5,000 entries the chance rises to about **65.0%**.

Therefore a four-character dictionary hit cannot count as a crack unless it also explains chronology, object function, script choice and physical orientation.

### Bold readings pursued and broken

#### `ALU` as the early Germanic magical formula

Rejected/downgraded. The famous runic `alu` belongs to the much earlier Elder-Futhark/Migration-period horizon. Hunt would require the formula to survive much later, be transliterated into ogham, and then be followed by a Younger-Futhark-like rune and a fifth unexplained mark.

#### `ALUʀ` = Old Norse/Icelandic *alur* 'awl'

Rejected after historical-form checking. Modern Icelandic `alur` descends from Old Norse `alr`; the epenthetic/svarabhakti `u` in forms such as `alur` develops only around the late thirteenth century/around 1300. That does not share a normal chronological window with the earlier `ʀ` value. This was an attractive short-string false positive, not a solution.

### Current ranked explanation set

1. **Medieval scholastic mixed-script mark/graffito**: minimum-assumption core `A-L-U` + probable Younger-Futhark `ʀ`, plus a secondary/non-phonetic fifth mark; could be abbreviated, identity/workshop marking or literate/non-lexical play.
2. **Maker/owner/workshop abbreviation or short name** in a mixed-script register; object-function parallels support this, but no name has earned acceptance.
3. **Learned practice/script display**; strong cultural parallels exist, though Hunt is not a literal alphabet fragment.
4. **Secondary/later inscription**; poor provenance keeps this live and physical incision sequencing can decide it.
5. Ordinary Irish word/name, pure runic, magical `alu`, and technical/numerical whole-sequence interpretations are currently substantially weaker.

### Preferred inventory at close of session

Conditional, not a decipherment:

- orientation: **published orientation preferred if sign 4 is genuinely runic**;
- sign 1: `A` preferred over `M`, both live;
- sign 2: `L` in preferred orientation;
- sign 3: `U` preferred over `NG/Gʷ`, both live;
- sign 4: **Younger-Futhark `ʀ` preferred**, later `y` a chronological alternative;
- sign 5: **secondary/non-phonetic preferred**, `P` strongly downgraded;
- reading direction: unresolved;
- lexical status: **no defensible ordinary-language reading**.

The tightest shorthand is therefore approximately **`ALUʀ + MARK`**, with the warning that this describes the preferred graphic classification, not recovered plaintext.

### Highest-value next observation

Determine whether sign 5 was cut with the **same tool profile, depth, patina and operation** as signs 1–4. If not, the problem immediately simplifies from a five-sign decipherment to a four-sign mixed-script mark. Next priorities are metric adjudication of signs 1 and 3 and incision/stem-line sequencing.

Full reasoning: `analysis/RESULTS.md`. Dead ends: `FAILED_READINGS.md`. Exact sources: `SOURCES.md`. Next experiments: `HANDOVER.md`.
