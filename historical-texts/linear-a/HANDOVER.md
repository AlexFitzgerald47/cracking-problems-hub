# Handover Notes – Linear A

**Current frontier:** 2026-09-08, GPT-5.6 Sol  
**Status:** functional/historical solve candidate; not a phonetic decipherment or language-family solve.

## Read these first

1. `analysis/2026-09-08-scribe9-dossier-functional-reconstruction.md`
2. `analysis/scribe9_dossier.csv`
3. `analysis/2026-09-07-haghia-triada-labor-control-functional-solve.md`
4. `analysis/haghia_triada_functional_decode.csv`
5. `analysis/2026-09-07-kiro-unified-residual-grammar.md`
6. `analysis/2026-09-07-obligation-circuit-post-award.md`
7. `PROGRESS.md`

## Current solve candidate

The strongest current reading is:

> **A substantial Haghia Triada / Casa del Lebete Linear A dossier written by HT Scribe 9 records an integrated labor-liability administration linking accountable units, personnel assessments, standardized work groups, assignment, roster checking, KI-RO exception reporting, census-linked provisioning/resources, and hierarchical control totals.**

This is stronger than a one-word KI-RO result because the same hand, same institutional environment, repeated names and repeated header vocabulary form a coherent dossier.

## Strong anchors

### KU-RO

Closing total / summation marker. Arithmetic support is strong and independent of language choice.

### PO-TO-KU-RO

Higher-order / grand total. On HT122:

`KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97`.

### KI-RO

Best functional nucleus:

**DUE-BUT-UNFULFILLED / OUTSTANDING / MISSING.**

Two constructions remain the best grammar:

- `KI-RO + numeral` -> scalar residual;
- `KI-RO •` -> forward-scoping outstanding / missing list.

For personnel records, the strongest interpretation is an expected labor/service obligation that failed to materialize at muster or reconciliation.

### A-DU

Best current type, still provisional:

**ASSESSED / ACTIVATED OBLIGATION / ACCOUNT-STATE HEADING.**

Reason: it occurs across manpower and grain/assessment records and behaves more like a generic administrative operator than a normal name/place. Do not force the exact polarity yet.

### MA-KA-RI-TE

Best current type:

**SERVICE / DUTY / INSTITUTIONAL ACCOUNT.**

This comes mainly from the HT87/HT117 pairing. Do not claim a literal lexical translation.

### U-MI-NA-SI / SA-TA / QI-TU-NE

Best current type:

**ACCOUNTABLE / SUPPLYING UNIT OR INSTITUTION.**

U-MI-NA-SI should no longer be treated confidently as a verb meaning `owes`. In HT117 it occupies the same subgroup-header slot as SA-TA and QI-TU-NE.

## Main new result: the Scribe-9 dossier

Secure Scribe-9 tablets identified in the current dossier:

### Casa Room 7

- HT85 — personnel mobilisation / gang formation;
- HT87 — ordinary personnel roster;
- HT94 — personnel account + KI-RO exception list;
- HT112 — fragmentary livestock/resource account.

### Casa Room 9

- HT117 — large KI-RO exception roster grouped by units;
- HT119 — personnel/resource ratio account.

### Casa del Lebete

- HT122 — master personnel liability/control register;
- HT128 — grain/resource allocation linked in prior scholarship to a census of people;
- HT132 — person/resource responsibility, including 27 sheep with QA-RE-TO;
- HT135 — fragmentary account.

Treat findspots as administrative clustering, not proven chronology.

## HT87 -> HT117: strongest query-grammar result

Both are Scribe 9.

HT87 begins:

`QI-TU-NE • MA-KA-RI-TE •`

followed by ordinary personnel, including DI-KI-SE.

HT117 begins:

`MA-KA-RI-TE • KI-RO • U-MI-NA-SI •`

followed by ten one-unit personnel entries and `KU-RO 10`, then further personnel blocks under SA-TA and QI-TU-NE. DI-KI-SE occurs again in the QI-TU-NE block.

Best functional reconstruction:

```text
HT87
FILTER unit = QI-TU-NE
FILTER duty/account = MA-KA-RI-TE
SHOW ordinary roster

HT117
FILTER duty/account = MA-KA-RI-TE
FILTER status = KI-RO
GROUP BY accountable unit
SHOW exceptions
```

This makes DI-KI-SE the strongest status-switch control in the dossier.

## HT85 — dispatch / mobilisation sheet candidate

HT85 totals exactly 66 personnel.

`66 = 11 x 6`.

Existing structural work identifies eleven receiving/responsibility entries on the reverse. Best functional reading:

> **Eleven standardized six-person work gangs assembled from personnel supplied by several accountable source units and assigned onward.**

Do not claim the exact source->destination mapping yet.

## HT122 — master liability/control register candidate

HT122 uses repeated personnel contributions and hierarchical totals:

- first block -> KU-RO 31;
- KU-DA 1;
- second block -> KU-RO 65;
- PO-TO-KU-RO 97.

It also contains ordinary one-unit entries such as KU-PA3-NU and PA-TA-NE, both of which occur in KI-RO exception contexts elsewhere in the Scribe-9 dossier/wider personnel archive.

Best functional reading:

**master personnel liability / contribution register over the same administrative population that appears in exception and mobilisation records.**

### Intriguing but unproven bridge

HT85 total = 66.

HT122 contains `KU-RO 65` plus `KU-DA 1`.

Because both are Scribe-9 manpower records, test whether `65 + 1 = 66` is a real cross-tablet reconciliation. Do **not** claim it until entity-level composition aligns.

## HT119 — fixed manpower ratio clue

HT119 records:

`*327 34`

`VIR 68`

an exact 1:2 relationship.

The identity of *327 is unresolved. Preserve only the structural result: two men per counted unit in this line.

Together with HT85's six-person groups, Scribe 9 repeatedly encodes fixed manpower ratios.

## Unified administrative architecture

```text
ACCOUNTABLE LOCAL UNITS
        |
        v
ASSESS / ACTIVATE LIABILITY (A-DU?)
        |
        v
MOBILISE PERSONNEL / GOODS
        |
        v
FORM / ASSIGN WORK GROUPS
        |
        v
ORDINARY ROSTER / DUTY ACCOUNT
     /                 \
REALISED             KI-RO
                     OUTSTANDING /
                     MISSING
                        |
                  NAMED EXCEPTIONS
                        |
              KU-RO / PO-TO-KU-RO
                  CONTROL TOTALS
                        |
                 CENSUS-LINKED
             PROVISIONING / RESOURCES
```

## Why this matters

If the model survives adversarial testing, the archive shows Minoan administration doing more than inventory counting:

- maintaining stable accountable units;
- levying personnel obligations;
- pooling and redistributing labor;
- organizing standardized gangs;
- assigning duties/accounts;
- checking named personnel against expected rosters;
- flagging unfulfilled service under KI-RO;
- linking people to food, livestock and productive resources;
- using local and higher-order arithmetic controls.

The recoverable object is therefore an **operating system of labor administration** despite the language remaining undeciphered.

## Do not regress to these old paths

- Do not restart generic candidate-language dictionary fishing.
- Do not spend another session proving KU-RO is a total.
- Do not spend another session asking whether KI-RO can vaguely mean deficit.
- Do not force A-DU = payment.
- Do not force U-MI-NA-SI = owes/debt; test its entity/header behavior first.
- Do not force MA-KA-RI-TE = former year or a reason-for-absence without explaining the HT87/HT117 structural pair.
- Do not trust the transaction parser's sender/recipient labels as deciphered semantics; they are heuristic assignments.
- Do not infer chronological sequence from room findspots.
- Do not claim `Linear A deciphered`.

## Highest-value next experiments

1. **Build the complete Scribe-9 relational table**: tablet, findspot, header fields, entities, quantities, resources, status terms, totals, repeated names and circuit positions.
2. **Test the HT87/HT117 query grammar** on HT85, HT94, HT119 and HT122. Ask whether `account / status / unit / person` predicts unseen structures.
3. **Resolve MA-KA-RI-TE** by enumerating every occurrence and classifying duty/account vs place/unit vs temporal vs explanatory uses.
4. **Resolve U-MI-NA-SI** with the same held-out type test. A clean operator/verb use would falsify the current unit interpretation.
5. **Resolve A-DU polarity** across HT85/HT88 and HT86/HT95 without importing candidate-language etymology.
6. **Test HT85 66 vs HT122 65 + KU-DA 1** at the entity level.
7. **Build the directed labor network**: source unit -> duty/account -> assigned personnel -> KI-RO exceptions. DI-KI-SE is the first anchor edge.
8. Only after the functional graph stabilizes should phonetics/language-family hypotheses return as weak priors.

## Falsifiers

- U-MI-NA-SI behaving cleanly as an operator rather than an entity/header.
- MA-KA-RI-TE failing in a held-out duty/account context.
- A-DU requiring incompatible meanings across labor and assessment records.
- The HT87/HT117 pairing disappearing once tablet segmentation is re-audited against facsimiles/GORILA.
- The 66 vs 65+1 bridge failing entity-level reconciliation (expected possibility; this would only kill that sub-hypothesis).

## Claim discipline

Use:

> **functional solve candidate / historical reconstruction of a Scribe-9 labor-liability dossier**

Do not use:

> **Linear A deciphered**

The claim worth specialist attention is narrower and stronger:

> **A coherent Scribe-9 Haghia Triada/Casa del Lebete tablet cluster can be read as different administrative views over one labor-obligation system, including personnel liability, gang formation, duty/account assignment, named KI-RO exception reporting, repeated roster states, census-linked resources, and hierarchical control totals.**
