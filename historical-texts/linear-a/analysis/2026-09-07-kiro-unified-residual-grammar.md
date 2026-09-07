# KI-RO unified residual grammar: from loose gloss to testable administrative operator

**Session:** 2026-09-07, GPT-5.6 Sol  
**Status:** significant structural advance; not a linguistic decipherment

## Executive result

The previous pass narrowed KI-RO to an "outstanding residual/status" marker. This pass pushes that result further into a small, falsifiable administrative grammar.

The best current model is:

> **KI-RO marks an UNFULFILLED / MISSING / OUTSTANDING state.**
>
> It can apply either to a scalar quantity or to a set/list of entities. When a detailed residual list follows, KU-RO can close that list by giving its arithmetic total/cardinality.

This is deliberately a *functional* representation. It does not claim that the underlying Minoan lexeme literally meant one English word, nor does it identify a language or etymology.

A useful formalisation is:

- scalar accounts: `R = EXPECTED - REALISED`; KI-RO labels `R`;
- personnel/roster accounts: `M = EXPECTED_SET \\ REALISED_SET`; KI-RO labels the members of `M`;
- if the residual set is itemised, `KU-RO N` can give `|M| = N`.

This unifies commodity deficits and missing-personnel lists without changing KI-RO's semantic type.

## Same-day correction: HT117 is not good evidence for a binary X–KI-RO–Y relation

The prior analysis treated the visible opening sequence of HT117 — `MA-KA-RI-TE • KI-RO • U-MI-NA-SI •` — too readily as a single three-term relational header. That made a directional reading such as `X owes Y` look tempting.

Davis & Valério's contextual analysis is a better segmentation for semantic work: they treat `MA-KA-RI-TE • KI-RO •` as the main heading, and the following personnel material as three 1-lists under subheadings including `U-MI-NA-SI`, `SA-TA`, and `QI-TU-NE`. They explicitly note that KI-RO, normally interpreted in the deficit/owing family, may in these personnel lists mean something like "missing/absent".

Source: Brent Davis & Miguel Valério, "Names and Designations of People in Linear A: A Contextual Study of Tablets HT 85 and 117," *Neôteros* (2020), pp. 23–32, DOI 10.2307/j.ctv1q26kwq.9. Public author copy indexed at:
https://www.researchgate.net/publication/352343395_Names_and_designations_of_people_in_Linear_A_A_contextual_study_of_tablets_HT_85_and_117

This does **not** undo the previous scope finding. KI-RO still scopes over material that follows. It does remove the main reason to hunt a debtor→creditor direction inside KI-RO itself.

## Discovery 1: a two-construction grammar predicted by the token immediately after KI-RO

I hand-audited every clean exact KI-RO context located in the current Haghia Triada working set and froze the immediate construction independently of whether the arithmetic later "worked".

There are two constructions:

### Construction A — scalar residual

`... KI-RO N`

where a numeral/measure follows KI-RO directly.

Observed clean cases:

- HT1 — `KI-RO 197`
- HT15 — `KI-RO 400`
- HT34 — `KI-RO 30`
- HT123+124 — row-level KI-RO quantities/fractions

### Construction B — detailed residual block

`... KI-RO • ITEM q ... [KU-RO N]`

where a divider follows KI-RO and the marker scopes forward over a list/block.

Observed clean cases:

- HT30
- HT37
- HT88
- HT94b
- HT117

### Frozen result

**9/9 clean exact KI-RO contexts obey this construction rule; 0 clean contradictions were found.**

HT93b has damaged `KI-RO[` and is deliberately excluded from the construction count. ARKH4 `A-KI-RO` and HT85b `KI-KI-RA-JA` are near-forms, not silently merged into the KI-RO family.

This is descriptive rather than a p-value claim: the background rate of divider placement has not yet been measured corpus-wide. The important advance is that the rule is explicit enough to run blind on unseen records.

Machine-readable ledger: `analysis/kiro_construction_grammar.csv`  
Executable assertions: `analysis/kiro_construction_grammar.py`

## Discovery 2: the two constructions share one residual semantics

The split above is not merely formatting. Independent arithmetic and list structure show the same negative-state semantics in both modes.

### HT34 — scalar residual is exact

The account gives 100, a fulfilled/removed amount 70, and `KI-RO 30`:

`100 - 70 = 30`

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT34.html

### HT123+124 — scalar make-up residual is exact

For the DA-TU row, OLIV is 15; the target *308 relation is one third, i.e. 5. The booked amount is `4 E` = 4 1/4 and KI-RO is `J E` = 3/4:

`5 - 4 1/4 = 3/4 = KI-RO`

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT123%2B124.html

### HT88 — residual personnel block has exact cardinality

`KI-RO •` opens six named entries, each 1, and the block closes with `KU-RO 6`.

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT88.html

### HT94b — independent residual personnel block has exact cardinality

`KI-RO •` opens five named entries, each 1, and the block closes with `KU-RO 5`. Younger's commentary independently calls it a list of personnel deficits.

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT94.html

### HT117 — personnel residual/status under a main heading

The first 1-list contains ten unit entries and is closed by `KU-RO 10`. Davis & Valério's segmentation places KI-RO in the main heading over the personnel material rather than between a debtor and creditor.

Sources:
- Davis & Valério 2020, DOI above
- https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT117.html

### Held-out semantic discriminator: HT15 — HIT

Before reading the HT15 commentary in this pass, I froze the prediction that `KI-RO 400` should be an unresolved/residual amount tied to the account above it, rather than a total or arbitrary label.

HT15 gives visible quantities 684 and 570, which sum to 1,254. The source commentary independently describes `KI-RO 400` as a deficit/amount owed against an expected total of 1,254.

`684 + 570 = 1254`

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT15.html

The semantic prediction therefore hit on a tablet not used to derive the unified model.

## Discovery 3: KI-RO behaves like a status applied to ordinary entities, not the name of a special class

A strong alternative model would be that KI-RO names some fixed category of workers or recipients. That predicts that the names under KI-RO should be characteristic of that category.

Instead, at least five entities/designations recur both in KI-RO contexts and in ordinary non-KI-RO lists:

1. **DI-KI-SE** — HT117 under the KI-RO personnel heading, but also HT87 in a comparable `QI-TU-NE • MA-KA-RI-TE` personnel context with no KI-RO.
2. **KU-PA3-NU** — in KI-RO lists on HT88/HT117 (and also on HT1), but in an ordinary personnel list on HT122.
3. **PA-TA-NE** — in the HT94b KI-RO list and in the ordinary HT122 personnel list.
4. **PA-JA-RE** — in the HT88 KI-RO list and in non-KI-RO contexts on HT8, HT29 and ZA10.
5. **SA-RU** — in the HT94b KI-RO list and in non-KI-RO records such as HT86/HT95.

The strongest control is DI-KI-SE because the surrounding institutional pair is conserved: HT87 has `QI-TU-NE • MA-KA-RI-TE` with DI-KI-SE 1, while HT117 has the same contextual terms plus KI-RO and again DI-KI-SE 1. This is close to a natural status-toggle experiment.

That pattern is expected if KI-RO says that otherwise ordinary roster members are in a negative/outstanding state. It is not expected if KI-RO is itself a fixed occupational, ethnic, or personnel-class label.

## The resulting mini-grammar

The smallest model that covers the clean evidence is:

### Scalar form

`ACCOUNT_CONTEXT ... KI-RO N`

Functional reading:

`ACCOUNT_CONTEXT ... OUTSTANDING N`

### List form

`ACCOUNT_CONTEXT ... KI-RO • X1 n1 X2 n2 ... [KU-RO N]`

Functional reading:

`ACCOUNT_CONTEXT ... MISSING/OUTSTANDING: X1 n1, X2 n2, ... [TOTAL N]`

The English words are placeholders for a semantic operator, not a translation claim.

## Why this is stronger than "KI-RO = deficit"

"Deficit" has long been proposed in Linear A scholarship, and Davis & Valério already floated "missing/absent" for the 1-lists. The advance here is therefore **not** the English gloss.

The new contribution is the combination of five independently testable pieces:

1. **construction grammar:** divider-after-KI-RO predicts forward list scope; numeral-after-KI-RO predicts scalar residual — 9/9 clean cases;
2. **cross-domain semantics:** one residual operator covers both scalar quantities and sets of personnel;
3. **arithmetic/cardinality controls:** HT34, HT123, HT88, HT94b and HT117 all instantiate the predicted residual/aggregation structure;
4. **held-out confirmation:** HT15 was predicted as a residual account before its commentary was opened and matched;
5. **status-switch controls:** recurring entities occur both inside and outside KI-RO contexts, with DI-KI-SE preserving unusually close surrounding context.

Together these turn a traditional gloss into a falsifiable administrative model.

## Adversarial audit / awkward cases

### HT1

The signs KI and RO are both marked certain in the published digital reading, immediately followed by 197. Some scholarship has proposed alternative interpretations of the record, including treating the form as a scribal issue or interpreting the large integers as cumulative absences. Those are semantic hypotheses, not transcription uncertainty in the two signs themselves.

HT1 therefore supports the scalar construction syntactically but is **medium-grade semantic evidence**. It should not be used to prove "days absent" or any other unit.

Primary/digital object page:
https://github.com/mwenge/lineara.xyz/blob/master/items/HT1.html

### HT37

`KI-RO •` is clean enough to support the forward-construction classification, but surrounding material is damaged. Count it for scope, not for a fine semantic equation.

### HT93b

`KI-RO[` is damaged on the reverse. The visible account appears to leave a numerical gap, which is compatible with residual semantics, but the record is excluded from the 9-case construction test.

### ARKH4 A-KI-RO

`A-KI-RO 3` is a tempting morphological relative but occurs as an ordinary numbered word in a damaged Arkhanes tablet. Similar spelling is not sufficient evidence of semantic identity. It is retained as a **near-form negative control**, not counted as KI-RO.

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/ARKH4.html

### HT85b KI-KI-RA-JA

This heading introduces an 11-entry one-list, and older scholarship has connected it morphologically with KI-RO. Its structure is compatible with a derived administrative heading, especially beside HT85's 66-person arithmetic, but semantic identity is not demonstrated. Keep it as a candidate extension, not part of the solved KI-RO grammar.

## Correction to the recent computational negative control

The 2026 corpus-validation project tests KI-RO with the same backwards-looking routine used for KU-RO: it takes numbers before the marker and compares their sum with a number after it.

That is now demonstrably the wrong grammar for the unquantified `KI-RO •` construction. Those cases scope forward. The 0/7 local-total result is therefore not evidence against the deficit/missing semantic family; it is a parser-direction mismatch.

Source code:
https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a/blob/main/src/kuro_test.py

A corrected automated test should first classify KI-RO occurrences by immediate construction without looking at arithmetic outcomes, then test scalar and forward-list cases separately.

## Frozen falsifiers

The unified model should be weakened if any of the following is found in a clean, well-segmented record:

1. `KI-RO •` followed by material that demonstrably belongs to the preceding account rather than a new residual/status block;
2. `KI-RO N` where `N` can independently be shown to be a neutral total or fulfilled amount rather than a residual/outstanding quantity;
3. a corpus-wide analysis showing that KI-RO personnel names form a stable special class and do not behave like ordinary roster entities switching status;
4. a securely segmented binary construction `ENTITY_A • KI-RO • ENTITY_B` in which independent evidence forces an A→B or B→A relation;
5. failure of the 9/9 construction rule when tested blind on an unseen clean KI-RO attestation.

## Reproducibility and next step

Files:

- `analysis/kiro_construction_grammar.csv` — frozen hand-audited evidence ledger;
- `analysis/kiro_construction_grammar.py` — construction, arithmetic/cardinality, and status-switch assertions.

Current frozen results:

- construction grammar: **9/9** clean exact KI-RO contexts;
- arithmetic/cardinality controls: **6/6 pass** (HT34, HT123, HT88, HT94b, HT117, plus HT15's visible 1,254 expected-account invariant);
- independently recurring entities with both KI-RO and non-KI-RO contexts: **5** hand-confirmed controls.

The highest-value next experiment is a true corpus-wide parser over `corpus_v1.json` that classifies KI-RO by punctuation/next-token form *before* any semantic outcome is inspected, then tests the frozen grammar on all remaining attestations and matched non-KI-RO controls.
