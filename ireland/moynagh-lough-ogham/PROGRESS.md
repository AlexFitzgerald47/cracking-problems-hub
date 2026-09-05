# Progress

## 2026-09-05 — GPT-5.6 Sol — starting session

### Evidence secured

Read the April 2025 OG(H)AM object treatment and David Stifter’s 2026 preprint discussion in full-text form. Fixed the archaeological and inscription constraints before pursuing words:

- red-deer antler leather-working beveller/burnisher, NMI RIA 1889:13;
- archaeological horizon roughly AD 625–810;
- two inscribed sides, one natural ridge and one drawn stem-line;
- published preferred readings `COLORRS` and `PIBANSNAVQE`;
- side order/continuity unknown;
- initial side-2 sign can be P/PH, forfid or start mark; final sign damaged;
- side-1 adjacent Rs may include a correction;
- crucially, Stifter reports the last two side-1 letters as apparently cut with a finer blade, perhaps the same tool as side 2.

Built the explicit branch generator `code/enumerate_candidates.py`: 5 side-1 models × 8 side-2 models × 3 side-relationship models = **120 structural hypotheses**. This is the search budget future lexical work must respect.

### New finding 1 — `PIBAN` has an independently dated personal-name reading

A live biographical source records Fáilbe (d. 679), eighth abbot of Iona, as the son of **Pípán**; historical lists also transmit *Failbe mac Pipan*. This is directly inside the tine’s date window.

This matters because Stifter’s tentative translation begins by taking `PIBAN` as the common noun *pípán* “small tube”. The same form is therefore not uniquely lexical: it is also a genuine early-medieval Irish personal name. Portable ogham artefacts can bear owners’/persons’ names, so an owner/maker/name model now has a strong independent prior.

**Limit:** `SNAVQE` is not solved, and the initial side-2 sign might still be non-phonetic. This is a component reading, not a full decipherment.

### New finding 2 — a physically motivated `COLOR` phase

Stifter’s tool observation independently suggests a carving boundary before the last two signs of `COLORRS`. If the reported finer `RS` belongs to a later episode, the first carving phase is exactly:

`COLOR`

which is Latin *color* “colour / appearance”. Because the proposed boundary comes from groove/tool morphology rather than arbitrary substring selection, this is worth testing.

**Limit:** no independent functional reason has yet been found for Latin *color* on the leather-working tine, and this session did not directly measure the RTI/3D grooves. The hypothesis stands or falls on physical tool-profile clustering.

### Reverse-side control

The public Ogham Data v1 readings include `DUGENNGG[I] MAQI RODDOS`; `RODDOS` is independently recognised as an ogham personal-name form. This gives reverse `CRRODOS` a real comparator but not a match. Even collapsing one R as a correction leaves additional discrepancies. Retained as a low-ranked image-audit lead.

### Published `PIBAN SNAVQE = “tube of bark”` reassessed

Downgraded, not eliminated. It requires a common-noun reading of `PIBAN`, hypothetical `*snamchae`, several special orthographic values, and then must explain why “tube of bark” occurs on solid antler. Discovery of period-correct Pípán removes the uniqueness of the first step.

### Failed lead preserved

A 2026 internet proposal linked Old Irish bark terminology to late English/Scots `snob/snab` “cobbler” and read the text as a leatherworker’s tool label. Rejected as evidence: the cobbler sense is late (18th/19th century) and its origin is not established. See `FAILED_READINGS.md`.

### Current ranking

1. `PIBAN` = personal name Pípán/Pipan; `SNAVQE` remains qualifier/name/independent text.
2. First side-1 carving phase = `COLOR`, with finer `RS` added later.
3. Stifter’s “tube of bark” phrase — possible but assumption-heavy and object-semantically weak.
4. Reverse `CRRODOS` / attested `RODDOS` connection — weak but physically testable.

No solve claim made.
