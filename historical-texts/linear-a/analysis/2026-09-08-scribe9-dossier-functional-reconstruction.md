# 2026-09-08 — HT Scribe 9 dossier: functional reconstruction

## Status

This note records the strongest new result of the 2026-09-08 cracking pass. It is a **functional/historical decipherment candidate**, not a phonetic decipherment of Linear A and not a language-family claim.

The key move was to stop treating HT85, HT87, HT94, HT117 and HT122 as isolated tablets and instead treat the securely identified **HT Scribe 9** tablets as one administrative dossier.

## Core result

The most economical model is that Scribe 9 handled a labor-and-dependent-resource control system linking:

1. accountable source units / communities;
2. personnel liabilities or assessments;
3. mobilisation into standardized work groups;
4. assignment / responsibility;
5. muster or roster checking;
6. KI-RO exception / shortfall lists;
7. KU-RO and PO-TO-KU-RO control totals;
8. census-linked provisioning and productive assets.

The working state-machine is:

```text
OUTLYING ACCOUNTABLE UNITS
           |
           v
    PERSONNEL LIABILITY
           |
           v
       A-DU ACCOUNT
  assessed / activated state
           |
           v
   STANDARD WORK GANGS
           |
           v
    ASSIGN / DISPATCH
           |
           v
      ORDINARY ROSTER
        /         \
 REALISED         KI-RO
                  UNFULFILLED /
                  ABSENT
                    |
               EXCEPTION ROLL
                    |
                  KU-RO
               subtotal/total
                    |
             PO-TO-KU-RO
               grand total
```

## Secure anchors retained from prior work

### KU-RO

Closing summation marker / total. Strong arithmetic support.

### PO-TO-KU-RO

Higher-order / grand total. HT122 gives:

`KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97`.

### KI-RO

Best functional nucleus remains:

**UNFULFILLED / MISSING / OUTSTANDING**.

Two constructions:

- `KI-RO + numeral` -> scalar residual;
- `KI-RO •` -> forward-scoping residual / exception block.

Personnel uses are best read as missing or unfulfilled labor/service obligations, not as a permanent class of people.

## New result 1 — HT87 and HT117 are two views over the same administrative relation

Both tablets are by Scribe 9.

HT87 begins with the paired heading:

`QI-TU-NE • MA-KA-RI-TE •`

and then lists personnel, including `DI-KI-SE`.

HT117 begins:

`MA-KA-RI-TE • KI-RO • U-MI-NA-SI •`

then gives ten one-unit personnel entries and `KU-RO 10`, followed by further blocks under `SA-TA` and `QI-TU-NE`. `DI-KI-SE` appears again in the QI-TU-NE block.

The strongest functional parse is therefore:

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

This is a **query-grammar hypothesis**: the tablets appear to be different administrative projections of the same personnel relation.

The DI-KI-SE recurrence is the best quasi-experimental control because the same person/designation occurs in the same QI-TU-NE / MA-KA-RI-TE institutional environment with KI-RO toggled on only in HT117.

## New result 2 — U-MI-NA-SI is probably an entity/unit, not a verb meaning `owes`

Older glossing traditions sometimes treat U-MI-NA-SI as debt/owing vocabulary. The HT117 layout argues against that as the primary functional type.

In HT117, U-MI-NA-SI occupies the same structural slot as SA-TA and QI-TU-NE, each heading a personnel subgroup. That makes the cleaner ontology:

- U-MI-NA-SI = accountable / supplying unit or institution;
- SA-TA = accountable / supplying unit or institution;
- QI-TU-NE = accountable / supplying unit / personnel group.

This is a type inference, not a literal translation.

## New result 3 — MA-KA-RI-TE is more likely a duty/account than a reason-for-absence or calendar word

HT87 and HT117 together make `MA-KA-RI-TE` look like the stable institutional/duty dimension across an ordinary roster and an exception roster.

Working functional value:

**SERVICE / DUTY / INSTITUTIONAL ACCOUNT**.

Do not claim a literal lexical translation yet.

Old proposals such as `former year` or a reason-for-absence reading are less economical under the three-subgroup structure of HT117, especially because QI-TU-NE independently behaves as an entity/personnel-group label.

## New result 4 — A-DU is best treated as an obligation/account-state heading

A-DU occurs across labor and grain/assessment contexts. The strongest cross-domain compression is not `worker`, `place`, or `payment`, but an administrative state such as:

**ASSESSED / ACTIVATED OBLIGATION / ON-BOOK LIABILITY**.

Evidence used in this pass:

- HT85: A-DU heads the 66-person mobilisation sheet;
- HT88: A-DU heads the accounted personnel/resources block immediately before a KI-RO exception list;
- HT95/HT86: A-DU occurs in assessment-style grain records.

Treat exact polarity as unresolved. The important result is that A-DU behaves like a generic administrative operator/state rather than a normal entity name.

## New result 5 — Scribe 9 dossier and findspot structure

Secure Scribe-9 tablets identified in this pass:

### Casa Room 7

- HT85 — personnel mobilisation / gang formation;
- HT87 — ordinary roster in QI-TU-NE / MA-KA-RI-TE context;
- HT94 — personnel account plus KI-RO exception list;
- HT112 — fragmentary livestock/resource record.

### Casa Room 9

- HT117 — large KI-RO exception roster grouped by units;
- HT119 — personnel/resource counts, including an exact `*327 34 : VIR 68` 1:2 relation.

### Casa del Lebete

- HT122 — master personnel contribution/control register with KU-RO / PO-TO-KU-RO hierarchy;
- HT128 — grain distribution interpreted in the literature as linked to a census of people;
- HT132 — person/resource responsibility record, including 27 sheep assigned to QA-RE-TO;
- HT135 — fragmentary account.

The distribution is therefore 4 / 2 / 4 across the three deposits.

Do not overstate the room-level sequence as chronology. The useful claim is narrower: the same hand handled a coherent set of people/resource obligation records across the Casa del Lebete administrative complex.

## New result 6 — master-register to exception-register cross-links

HT122 contains ordinary personnel entries such as:

- KU-PA3-NU 1;
- PA-TA-NE 1.

Those same labels occur in KI-RO exception contexts elsewhere in the Scribe-9 dossier:

- KU-PA3-NU -> KI-RO context in HT117 (and also HT88 in the wider archive);
- PA-TA-NE -> KI-RO context in HT94.

This is exactly the relationship predicted between a master liability roster and later/parallel exception/muster records.

Chronology is not proven. The cross-link is structural, not temporal.

## New result 7 — standardized manpower ratios

Two Scribe-9 records show fixed ratios:

### HT85

Total manpower `66 = 11 x 6`.

Existing structural work identifies eleven receiving/responsibility entries on the reverse. Best functional interpretation: eleven standardized six-person work gangs.

### HT119

`*327 34` and `VIR 68`, an exact 1:2 relation.

The identity of *327 is unresolved, so preserve only the structural claim: this tablet encodes two men per counted unit in that line.

Together these suggest the administration used fixed manpower grouping/ratio rules.

## Intriguing but unproven numerical bridge

HT85 totals 66 workers.

HT122 contains a second `KU-RO 65` with an intervening `KU-DA 1`, and the grand control arithmetic is compatible with `65 + 1 = 66`.

Because both are Scribe-9 manpower records this deserves direct testing, but the entity composition is not yet strong enough to call the equality a cross-tablet reconciliation rather than coincidence.

Next agent should test whether KU-DA 1 belongs logically to the 65-person section and whether the contributing nodes align with the 66-person HT85 mobilisation pool.

## Strongest historical reconstruction now justified

> A substantial Scribe-9 Haghia Triada/Casa del Lebete tablet dossier can be read as a labor-liability administration in which accountable units supplied personnel obligations; personnel could be pooled into standardized work groups, assigned onward, provisioned according to census, checked in roster/muster records, and entered under KI-RO when expected service was unfulfilled. KU-RO and PO-TO-KU-RO provide local and higher-order controls.

This is a **functional solve candidate**, not `Linear A deciphered`.

## Falsifiers / danger points

1. If U-MI-NA-SI is shown in a clean held-out context to function syntactically as an operator rather than an entity/header, downgrade the unit interpretation.
2. If MA-KA-RI-TE is found in a clean non-personnel context where a duty/account reading fails, reopen its semantic type.
3. If A-DU cannot be modeled consistently across manpower and grain/assessment records, split it into narrower functions rather than forcing one gloss.
4. Do not infer chronological order from findspots.
5. Do not derive phonetic/language-family claims from these functional types.
6. Do not treat the 66 = 65 + 1 equality as a discovery until entity-level reconciliation is demonstrated.

## Highest-value next experiments

1. **Build the full Scribe-9 dossier table**: tablet, findspot, header fields, entities, personnel quantities, resources, KI-RO/KU-RO status, repeated names, circuit positions.
2. **Test the HT87/HT117 query grammar** against HT85, HT94, HT119 and HT122. Ask whether the same field order (`account / status / unit / person`) predicts unseen structures.
3. **Resolve MA-KA-RI-TE** by enumerating every occurrence and classifying whether it behaves as duty/account, place/unit, temporal term, or reason clause.
4. **Resolve U-MI-NA-SI** by the same held-out type test; specifically test the claim that it is an accountable entity rather than `owes`.
5. **Resolve A-DU polarity** using paired assessment/realization records such as HT86/HT95 and personnel records HT85/HT88.
6. **Test HT85 66 vs HT122 65+KU-DA1** at the entity level.
7. **Build a directed network** of source units -> assigned duty/account -> personnel -> KI-RO exceptions. DI-KI-SE is the first anchor edge.
8. Only after the functional graph is stable should phonetic values or candidate languages be reintroduced as weak priors.

## External / corpus sources used during this pass

- `mwenge/lineara.xyz` item, commentary and transaction files for HT85, HT87, HT88, HT94, HT95, HT112, HT117, HT119, HT122, HT128, HT132, HT135.
- Existing Davis & Valério contextual work on Haghia Triada personnel and circuit ordering, already cited elsewhere in this project.
- Existing Hub analyses listed in HANDOVER.md.

The transaction parser's sender/recipient labels were explicitly audited and **not treated as deciphered truth**: they are heuristic assignments. Directional claims in this note are therefore structural inferences, not imported parser semantics.
