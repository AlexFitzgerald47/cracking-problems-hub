# HCA 686 cracking results — 2026-09-05

## Bottom line

This session did **not** recover a defensible plaintext. It did materially narrow the inscription.

The best current structural model is:

> **medieval/scholastic ogham + probable Norse rune + a likely secondary/non-phonetic fifth mark**, rather than five ordinary linguistic letters.

Under the lowest-assumption published orientation, the first three positions are most simply `ALU`; sign 4 is plausibly the Younger-Futhark `ʀ`/later `y` rune; sign 5 is better treated as a terminal/secondary mark than as phonetic `P`. This yields a minimum-assumption *graphic* sequence approximately `ALUʀ + MARK` (or the reverse if reading direction is opposite), **not a solved lexical reading**.

The crucial result is that the geometry-favoured `ALUʀ` branch fails the strongest obvious lexical explanations. That failure is evidence against the assumption that the whole string is an ordinary word.

## Evidence actually used

### Primary/public object evidence

1. Hunt Museum Sketchfab model, **Penannular Ring-Brooch Mould**, UID `360532e622024d008b885a843c6cc423`, CC0. Public metadata gives HCA 686, soapstone, c. 6.1 × 5.9 cm, and records the inscription on one edge. The model page reports 63.9k triangles / 33.2k vertices.
2. Hunt Museum photographs reproduced in David Stifter, **Og(h)am of the Month: June 2025**, OG(H)AM. The page includes an overall object photograph and paired photographs of the inscription in both orientations.

### Access limitation

The research environment could resolve the published image URLs and model metadata but could not obtain the JPG/mesh binary for local rendering (image fetch/cache/DNS/403 restrictions; Sketchfab download also normally requires authenticated API access). Therefore this session does **not** pretend to have made new pixel-level or mesh-level observations. All groove geometry below is frozen from the specialist photographs/audit and then reasoned from independently.

## Sign inventory

| pos. | published geometry / visual fact | serious linguistic values | non-linguistic possibility | working confidence |
|---|---|---|---|---|
| 1 | One of the first three signs classed as standard ogham; slight rightward inclination is the source of ambiguity. | `A` most simply; `M` if inclination is structurally significant. | Low: shape participates cleanly in ogham system. | High that it is ogham; medium A vs M. |
| 2 | Standard ogham sign on the drawn stem-line. | `L` in published orientation; `D` when the object is upended. | Low. | High. |
| 3 | Standard ogham sign; like sign 1, slight rightward inclination matters. | `U` most simply; `Gʷ/NG` if angle is significant. | Low. | High that it is ogham; medium U vs NG. |
| 4 | Not an ordinary ogham character. Published form resembles the inverted-algiz/ýr shape used in Younger Futhark. | Norse `ʀ` in the earlier use; `y` after c. 1050. | Could be an idiosyncratic/technical mark, but the runic parallel is materially better than an ordinary-ogham one. | Medium-high for rune, pending direct groove/mesh audit. |
| 5 | Smaller than the others, slightly wider gap before it, and crosses the stem-line; small-cap-y-like form. | Weak `P` hypothesis via Bern Burgerbibliothek MS 207. | Terminal mark, separator, feather-like direction mark, craftsman/technical mark, or later addition. | Low for phonetic P; medium for secondary/non-phonetic role. |

### Why the `P` hypothesis was downgraded

A specialist discussion of ogham P notes that the y-like form in the ninth-century Bern MS 207 is used twice there but is **not attested elsewhere** (citing Sims-Williams 1992). The later learned `P` tradition uses a different supplementary form. Therefore resemblance to Bern is a one-manuscript analogue, not a normal letter-form. On HCA 686, where the mark is also smaller and separated, treating it as phonetic `P` consumes too many special assumptions.

## Orientation constraint

The object is physically ambiguous about top/bottom. There is nevertheless a conditional preference:

- In the published orientation, sign 4 has the **Younger-Futhark ʀ/ýr-type orientation** identified by Stifter, which fits a Norse/Viking-age context.
- The first three signs also require fewer reinterpretations in that orientation (`ALU` is the minimum-assumption ogham core).
- Therefore **if sign 4 is genuinely runic**, the published orientation is preferred over the upended `UDA/NGDM...` family.

This does **not** yet determine reading direction. Sign 5 could be terminal or initial if it has a feather/direction role, and its exact form does not match a standard feather mark.

## Chronological/register constraint: this looks scholastic, not classical

A full stem-line is deliberately incised along the narrow side. Standard Ogham references distinguish classical monumental ogham using a natural stone edge from later **scholastic** ogham written on an artificial stem-line. Unicode's current core specification explicitly calls stem-line inscriptions on a face later/post-seventh-century.

That is independently consistent with the object's probable Norse/Viking context and inconsistent with accepting the museum's old fifth-century label at face value.

Consequences:

1. Primitive-Irish memorial formulae should receive a low prior.
2. Manuscript-influenced/reformed/scholastic letter behaviour should receive a higher prior.
3. Script-switching is historically credible rather than intrinsically anomalous.

## Mixed ogham + rune parallels

### Killaloe, Co. Clare

The strongest Irish parallel is the Killaloe cross. It carries an Old Norse runic text and a scholastic ogham text that belong to the same monument: the runes name Þorgrímr and the ogham gives a blessing on him (`BENDACHT ... TOROQRIM`). Modern scholarship places it around the early twelfth century / campaign of 1102–1103.

This proves that in medieval Ireland a writer/community could deliberately coordinate **Norse runes and manuscript-based Irish ogham**.

### Maughold, Isle of Man

Maughold 2 juxtaposes a Younger-Futhark inscription/alphabet with the first part of the ogham alphabet on an artificial stem-line. Whatever the precise dating of the separate carving phases, it is strong evidence for a learned environment in the Irish Sea where the two scripts were consciously compared/displayed.

### Irish learned tradition

`In Lebor Ogaim` preserves Younger Futharks under labels such as *Gallogam* ('foreigner-ogham') and *Ogam lochlannach* ('Scandinavian ogham'). The surviving manuscripts are later than the mould, so this is contextual rather than direct proof, but it shows that Irish learned culture could conceptually absorb runes into an ogham framework.

## Object-type parallel: inscriptions on soapstone moulds are real

Norse Greenland provides a particularly useful function parallel. At Garðar, multiple soapstone moulds for casting spindle whorls carry inscriptions; five are runic and one uses Latin letters. Published discussion says legible examples contain names or ownership statements. The inscriptions are in negative because they were intended to transfer to the casting.

HCA 686 is not identical: its signs are on an edge rather than as a negative casting legend. But this comparison materially raises the prior for a **maker/owner/workshop mark** on a soapstone mould and lowers the need to invoke magic merely because the object is a mould.

## Explicit branch space

`analysis/candidates.csv` records **64 unique phonetic candidates** generated from:

- published vs upended orientation;
- four independently retained ogham cores (`ALU`, `ALNG`, `MLU`, `MLNG`) and their upended counterparts (`UDA`, `NGDA`, `UDM`, `NGDM`);
- sign 4 as `R` (= ʀ) or later `Y`;
- both reading directions;
- sign 5 as non-phonetic vs weak `P`.

The enumerator is `code/enumerate_candidates.py`.

The branch set deliberately includes `MLU`, although it was not highlighted in the short published prose, because sign 1 and sign 3 ambiguities must not be silently coupled.

## Corpus control: ordinary ogham does not rescue the cores

The public `ogi-ogham/ogham-datav1` readings CSV (CISP/Ogham-in-3D-derived data) was used as an empirical control.

Search results:

- `ALU`: no occurrence found.
- `ALNG`: no occurrence found.
- `MLNG`: no occurrence found.
- `UDA`: no occurrence found.
- `NGDA`: no occurrence found.
- `NGDM`: no occurrence found.
- `UDM`: no occurrence found.
- `ALUR`: no occurrence found.
- `MLU`: one substring occurs inside `ATUCMLU`, but that is Macalister's disputed old reading of the **Ennis bead**, itself an ambiguous portable-ogham inscription; it is not independent lexical confirmation.

This is not a proof against a later scholastic/foreign/abbreviated reading. It is strong negative evidence against claiming that a familiar ordinary-ogham word/name has simply been overlooked.

## Null model: why a short dictionary hit is not a crack

The 64 branches contain 32 four-phonetic-sign candidates and 32 five-sign candidates. `analysis/null_model.csv` gives an illustrative uniform-string null in which the same search budget is applied to random strings.

For an effective 20-symbol alphabet:

- against 1,000 entries at each length, probability of **at least one exact hit** somewhere in the branch set is about **18.9%**;
- against 5,000 entries, it rises to about **65.0%**.

This null is intentionally simple and is not a model of Old Irish or Old Norse phonotactics. Its role is to quantify the multiple-testing warning: after generating dozens of branches, a four-letter dictionary match is not remotely enough.

## Competing explanations

| hypothesis | result | reason |
|---|---|---|
| Ordinary/classical ogham, Primitive Irish | **Strongly downgraded** | Artificial stem-line is later/scholastic; sign 4 is not ordinary ogham; candidate cores lack corpus support. |
| Old/Middle Irish personal name/formula | **Downgraded** | No clean name/formula appears; four/five signs are unusually short and sign 4 does not fit ordinary ogham. |
| Owner/maker/workshop mark | **Still viable; ranked #2** | Strong object-class parallels for names/ownership on soapstone moulds; short/abbreviated mark plausible, but no name recovered. |
| Object/function label | **Low** | No candidate gives a securely historical word for mould/brooch/casting. |
| Abbreviation / initials | **Viable** | Short length and workshop context fit; intrinsically difficult to prove without parallels. |
| Cryptic/scholastic ogham | **Viable; part of ranked #1 family** | Artificial stem-line and learned rune/ogham parallels support the register. No specific cryptic key yet yields text. |
| Pure runic | **Very low** | First three signs are well-formed stem-line ogham, not a natural runic sequence. |
| Mixed ogham + runic | **Preferred script model** | Fits first three + sign 4 with fewer exceptions and has strong Irish/Irish-Sea parallels. |
| Old Norse / Norse-Gaelic plaintext | **Possible but no surviving lexical candidate** | Context fits; actual branches do not produce a historically clean form. |
| Magical/protective `ALU` | **Strongly downgraded** | `alu` is an early Elder-Futhark formula (chiefly Migration-period evidence); Hunt would require it to survive much later, be written in ogham, and then be followed by a Younger-Futhark rune plus unexplained fifth mark. |
| Practice / script-display marks | **Viable; ranked #3** | Maughold gives direct runic+ogham alphabet/display behaviour. Hunt's `ALU` is not itself an alphabet fragment, so this cannot be made more specific yet. |
| Pseudo-writing | **Possible but not preferred** | Three coherent ogham signs plus a contextually credible rune suggest real script knowledge. Non-lexical literate play/marking remains plausible. |
| Technical/numerical notation | **Low for whole sequence** | Strong script-shaped structure, no identified metrological/casting notation. Sign 5 alone could still be technical. |
| Later/secondary inscription | **Viable** | Provenance is poor and edge inscription could post-date manufacture. Needs tool-mark/patina sequencing. |
| Modern/antiquarian addition | **Not excluded, currently low-medium** | Art-market provenance raises the question, but the learned ogham+rune combination is historically possible; no physical evidence of modern cutting was obtained. |

## Failed bold hypothesis: `ALUʀ` = Old Norse *alur* 'awl'

This was worth pursuing because it would be a compact craft-related label. Modern Icelandic **alur** 'awl' descends from Old Norse **alr** 'awl'. At first glance, `ALUʀ` looked remarkably close.

It breaks chronologically:

- Old Norse is **alr**, not *alur*.
- The `u` in forms such as Modern Icelandic *alur* is the later svarabhakti/epenthetic vowel that begins to appear near the **end of the thirteenth century / around 1300**.
- But the distinctive Younger-Futhark ʀ rune had already changed/reassigned value by around the mid-eleventh century in the account used for HCA 686.

So the exact spelling `ALUʀ` combines features whose ordinary historical windows do not line up. It is a classic attractive short-string false positive and is rejected.

## Ranked explanation set after this session

1. **Medieval scholastic mixed-script mark/graffito, probably 3 ogham signs + one Younger-Futhark rune + a secondary fifth mark.** It may be abbreviated, literate play, identity/workshop marking, or otherwise non-lexical. This best explains the graphic system while accepting the lexical failure instead of forcing a word.
2. **Owner/maker/workshop abbreviation or short name in a mixed-script register.** Object-type parallels make the function plausible, but no candidate name currently earns acceptance.
3. **Learned practice/script-display sequence.** Strong cultural parallels exist for deliberate rune-ogham juxtaposition; Hunt's sequence is not an alphabet fragment, so this remains broader 'literate exercise/display' rather than a specific alphabet exercise.
4. **Secondary/later addition of uncertain date.** Physical incision sequencing could move this sharply up or down.
5. **Everything else** (ordinary Irish word/name, pure runic, magical `alu`, technical numerical sequence) is currently substantially weaker.

## Current preferred orientation/read inventory

Conditional, not claimed as decipherment:

- orientation: **published orientation preferred** if sign 4 is runic;
- signs 1–3: **A – L – U** is minimum-assumption, with `M` and/or `NG` retained as live alternatives;
- sign 4: **Younger-Futhark ʀ** is preferred over ordinary-ogham or random-mark explanations; post-c.1050 `y` remains chronological alternative;
- sign 5: **non-phonetic/secondary mark preferred**, phonetic `P` strongly downgraded;
- direction: **unresolved**;
- lexical status: **no defensible ordinary-language reading**.

This is a tighter result than `ALUʀ P`: the `P` should not currently be treated as a fifth letter, and the apparent `ALUʀ` should not be promoted to plaintext merely because it resembles later Icelandic *alur* or early Germanic `alu`.
