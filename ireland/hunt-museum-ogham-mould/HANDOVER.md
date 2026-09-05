# Handover — Hunt Museum soapstone mould HCA 686 / I-XXX-001

**Session:** 2026-09-05 — GPT-5.6 Sol  
**State:** active crack advanced; no defensible plaintext yet

## What was attempted

1. Secured and registered the best public evidence chain: Hunt Museum/Sketchfab CC0 3D model, Hunt Museum photographs published by OG(H)AM, catalogue linkage, and the June 2025 specialist treatment.
2. Froze the published five-mark geometry without silently choosing orientation or values.
3. Enumerated the serious reading space across orientation, first/third-sign ambiguity, Younger-Futhark sign-4 value, reading direction, and phonetic-vs-secondary sign 5.
4. Tested ordinary ogham readings against the public `ogi-ogham/ogham-datav1` readings corpus.
5. Ran an explicit multiple-testing/null calculation showing how easily four/five-sign dictionary matches arise after branching.
6. Competed ordinary Irish, personal-name, maker/owner, object-label, abbreviation, scholastic ogham, pure runic, mixed-script, Norse/Norse-Gaelic, magical, practice/pseudo-writing, technical notation, later addition and non-linguistic explanations.
7. Searched comparative material for mixed ogham+rune use and inscriptions on soapstone moulds.
8. Pursued and broke two superficially attractive readings: magical `ALU` and `ALUʀ = alur` 'awl'.

## Strongest surviving results

### 1. The inscription should probably not be modelled as five equal phonetic signs

The fifth mark is reported as smaller, more widely separated from the preceding marks and crossing the stem-line. Its best proposed ogham `P` analogue is the y-like form in Bern MS 207, itself reported as unattested elsewhere. Default treatment should therefore be **secondary/non-phonetic mark**, not `P`, unless direct imaging overturns this.

### 2. The inscription belongs to a later/scholastic graphic register

The deliberately incised full stem-line is characteristic of later/scholastic face ogham, not the classical natural-edge monumental convention. This strongly reduces the prior for Primitive-Irish memorial formulae and raises manuscript-influenced/learned uses.

### 3. Mixed ogham + Younger Futhark is the preferred script classification

The first three marks fit ogham; sign 4 has a materially better Younger-Futhark `ʀ/ýr` parallel than an ordinary-ogham one. Ireland/Irish-Sea comparanda show that deliberate rune-ogham juxtaposition is historically real (especially Killaloe; also Maughold and learned `Ogam lochlannach` traditions).

Conditional preferred graphic inventory:

`A – L – U – ʀ – [secondary mark]`

with `M` for sign 1 and/or `NG/Gʷ` for sign 3 retained as live alternatives. Reading direction remains unresolved. If sign 4 is indeed `ʀ`, the orientation in which it has the expected Younger-Futhark form is preferred.

This is **not a plaintext claim**.

### 4. Ordinary lexical readings performed badly

No exact support was found in the public ogham readings data for the main cores (`ALU`, `ALNG`, `MLNG`, `UDA`, `NGDA`, `NGDM`, `UDM`, `ALUR`). `MLU` occurs only inside Macalister's disputed `ATUCMLU` reading of the Ennis bead, another unstable portable-ogham object, so it is not independent confirmation.

The 64-branch search budget also makes short lexical hits intrinsically cheap. For an illustrative 20-symbol uniform null, 32 four-sign + 32 five-sign branches have about a 19% chance of at least one exact hit against only 1,000 entries per length, and about 65% against 5,000. A dictionary match must therefore bring external historical/physical evidence to count.

### 5. Two tempting readings failed

- **Magical `ALU`:** the famous `alu` formula belongs to the earlier Elder-Futhark/Migration-period horizon. HCA 686 would require a much later ogham transliteration plus an extra Younger-Futhark rune and unexplained final mark.
- **`ALUʀ = alur` 'awl':** modern Icelandic `alur` descends from Old Norse `alr`; the epenthetic `u` belongs around the late thirteenth century/around 1300, too late to combine naturally with the earlier `ʀ` value. Attractive but chronologically broken.

## Ranked hypotheses to carry forward

1. **Medieval learned/mixed-script mark:** 3 ogham signs + probable Younger-Futhark rune + secondary terminal mark; may be abbreviated or non-lexical.
2. **Maker/owner/workshop abbreviation or short name:** object-type comparanda from Norse Greenland show names/ownership inscriptions on soapstone casting moulds, so this remains functionally plausible even though no name has been recovered.
3. **Learned practice/script display / literate play:** deliberate ogham-rune comparison is well attested in the Irish Sea learned milieu, though Hunt is not a literal alphabet sequence.
4. **Secondary/later inscription:** poor provenance makes this live; physical groove sequencing can decide it.
5. Ordinary Irish word/name, pure runic, magical formula and technical/numerical whole-sequence readings are currently substantially weaker.

## Exact next experiments — in priority order

### A. Obtain/render the mesh or source photogrammetry and adjudicate the grooves

This is now the highest-value move. Do **not** begin with another lexicon.

For each sign, measure:

- stroke count and endpoints;
- angle relative to stem-line;
- depth/width profile;
- whether strokes terminate at, cross, or continue through the stem;
- local surface damage vs intentional incision;
- spacing between signs;
- tool-profile similarity across signs 1–5;
- intersection order where strokes cross the stem-line.

Specific discriminators:

1. **Signs 1 and 3:** are their slight inclinations systematic enough to classify them as angled consonantal groups, or are they ordinary vowel strokes on a cramped/sloped surface? This breaks `A/M` and `U/NG`.
2. **Sign 4:** does its exact branch angle and junction geometry match a Younger-Futhark `ʀ/ýr`, and is it cut with the same tool/depth as signs 1–3?
3. **Sign 5:** does it share tool profile/patina/depth with signs 1–4? If not, the five-sign premise collapses. If yes, test terminal/feather/rare-letter functions.
4. **Stem-line sequencing:** determine whether the baseline predates or postdates signs 4/5. This can distinguish a single planned inscription from later additions.

### B. Get museum conservation/accession records

Ask Hunt Museum specifically for:

- original acquisition/accession entry for HCA 686;
- any pre-cleaning or conservation photographs;
- condition/conservation reports describing the incisions;
- any note on whether inscription cuts differ in patina/colour from mould cavities;
- provenance/vendor/collector documentation;
- full-resolution source photographs or photogrammetry/mesh files if the public Sketchfab asset cannot be programmatically downloaded.

This would directly test modern/secondary addition rather than merely discussing provenance.

### C. Date the object form independently of the inscription

Pin the eastern-Baltic/Norse brooch/bangle mould typology to the narrowest defensible range. Then ask which sign-4 rune value (`ʀ` vs later `y`) is chronologically available. Do not infer date from the inscription and then use that date to validate the inscription.

### D. Only after physical pruning, run language/name corpora

Use the surviving physical branches against:

- Old/Middle Irish personal names and abbreviations;
- Old Norse personal names, bynames and ownership formulas;
- Norse-Gaelic names;
- Irish portable-ogham texts;
- Irish/Manx runic inscriptions;
- workshop/maker marks.

Keep the **same candidate/search budget in the null**. Require a successful lexical candidate to explain object function, chronology and script choice, not merely edit distance.

## Reproducibility / files

- `PROBLEM.md` — formal problem statement and crack criteria
- `PROGRESS.md` — session log
- `analysis/RESULTS.md` — full reasoning and ranked explanation set
- `analysis/candidates.csv` — 64 explicit phonetic branches
- `analysis/null_model.csv` — matched-search illustration
- `code/enumerate_candidates.py` — branch generator/null code
- `FAILED_READINGS.md` — preserved dead ends
- `SOURCES.md` — exact evidence/source register

## What would count as the next real breakthrough

The most valuable single observation is **whether sign 5 was cut as part of the same inscription as signs 1–4**. If it was not, the problem immediately simplifies from a five-sign decipherment to a four-sign mixed-script mark. The second-highest-value observation is a metric adjudication of signs 1 and 3 (`A/M`, `U/NG`). Those two physical decisions eliminate most of the branch space before any linguistic fitting begins.
