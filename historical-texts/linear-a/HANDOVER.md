# Handover Notes – Linear A

---

## 2026-09-03 – Initial seed

### Recommended next experiments
1. Re-assessment of sign values transferred from Linear B in light of the full Linear A corpus.
2. Targeted study of longer texts and libation formulas.
3. Exploration of possible non-Indo-European linguistic affiliations with rigorous methodology.

---

## 2026-09-06 – Handover after first cracker pass

### State change

Do **not** restart this as a generic decipherment/language-family search. A July/August 2026 public corpus-validation project materially changes the starting point:
https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a

It is AI-assisted, unpeer-reviewed and explicitly unverified. Treat it as an unusually reproducible lead, not authority. The Hub has not yet rerun its pipeline.

### What worked

- Located a buildable GORILA/SigLA corpus pipeline with uncertainty preservation and multi-witness comparison.
- Inspected the actual KU-RO arithmetic test implementation. Its decisive control shuffles stated totals across fixed observed sections; reported KU-RO result z=+13.40 is therefore a real predictive pairing test rather than merely noticing that some hand-selected numbers add up.
- Identified a hard asymmetry worth exploiting: KU-RO has language-independent arithmetic evidence for a summation function; KI-RO has 0/7 exact matches under the same local-total test and should not be granted equivalent evidential status.
- Imported the audit's key adequacy warning: current corpus is too sparse for robust higher-order language-family inference, despite recoverable shallow affixation.

### What failed / remains unverified

- Direct GitHub clone from the execution container was DNS-blocked, so no Hub-owned clean rerun yet. All external numbers are REPORTED, not reproduced.
- AB21/AB22 sheep/goat inversion claim still needs direct GORILA plate adjudication before being accepted.
- No plaintext decipherment or language-family claim.

### Highest-value next experiments

1. **Reproduce before extending.** Clone the Tsirkas project in an environment with GitHub egress, build `corpus_v1.json` and SigLA, verify checksums, rerun `kuro_test.py`, `affix_null.py`, `packard_names.py`, and the adequacy stages. If the published figures do not reproduce, stop and audit the input drift.
2. **KU-RO semantic-anchor graph.** For every KU-RO-closed section, encode each neighbouring sign-group by structural role (header / item / immediately pre-total / immediately post-total / repeated across sections / commodity adjacency). Derive candidate functional classes on a training split and require them to predict held-out tablets. No phonetic values in this stage.
3. **Adversarial sectioning test.** Rerun KU-RO under multiple preregistered section rules (rulings only; previous-total only; commodity-heading only; combinations). Match the null budget. A summation marker should remain strongly paired with its own total across reasonable sectioning choices.
4. **Test PO-TO-KU-RO as a hierarchical total.** The code recognizes it but the published headline focuses on KU-RO. Ask whether PO-TO-KU-RO closes groups of KU-RO subtotals or otherwise occupies a statistically distinct higher-level position. This is potentially a second language-independent semantic anchor.
5. **Only then revisit phonetics.** Packard's stronger Knossos-name test reportedly survives. Use inherited Linear-B values as a probabilistic prior, not fixed truth, and score any reading against held-out structural functions from steps 2–4.

### Avoid

- Candidate-language dictionary fishing (Hurrian, Semitic, Anatolian, etc.) before semantic anchors exist.
- HMM/BPE/automatic cognate discovery on the present corpus without first defeating the published adequacy bounds.
- Treating KI-RO='deficit' as equivalent in evidential status to KU-RO='summation marker'.

---

## 2026-09-07 – Handover after KI-RO frontier pass

### Read this correction first

The 2026-09-06 handover's KI-RO warning is now **superseded in part**. The external `0/7` KI-RO local-total result is not an appropriate semantic discriminator because its code looks backward over the numerical section preceding KI-RO. Direct tablet inspection shows that KI-RO often scopes **forward** over the following list. Keep the KU-RO z=+13.40 result; discard the implication that KI-RO's failure under the same orientation weakens a deficit/owed interpretation.

Full write-up:
`analysis/2026-09-07-kiro-scope-residual.md`

### Frontier result

Best current functional model:

**KI-RO = an outstanding residual/status account (shortfall / amount due), capable of either carrying a scalar value or opening a detailed block of outstanding line-items.**

This is narrower than the loose literature bundle `owed / deficit / balance / subtraction` and is grounded in two independent kinds of evidence.

#### 1. Forward-scoping syntax

Discovery tablets:

- **HT88:** `KI-RO •` -> six named `1` entries -> `KU-RO 6`.
- **HT94b:** `KI-RO •` -> five named `1` entries -> `KU-RO 5`.

After forming that model, HT117 was opened as a held-out test.

- **HT117:** opening three-word header contains KI-RO -> ten `1` entries -> `KU-RO 10`.

**Held-out prediction hit.** A UCLA/Cotsen description independently confirms the physical segmentation: three dot-separated header words, ten one-unit entries, then the two-sign word for total plus 10.

Additional post-hoc support: HT30 and HT37 also place KI-RO before a following commodity/numeric block.

#### 2. Residual arithmetic

- **HT34:** `100 - 70 = KI-RO 30` exactly under the tablet's documented assessment/delivery interpretation.
- **HT123+124a, DA-TU row:** *308 `4 E` (4 1/4) + KI-RO `J E` (3/4) = `5`, exactly one-third of OLIV `15`. KI-RO is the make-up amount required to reach the row's target relation.

Five frozen checks are in `analysis/kiro_residual_checks.py`; all pass. Source ledger: `analysis/kiro_scope_ledger.csv`.

### What this does NOT solve

- It does not recover the underlying Minoan word's language or etymology.
- It does not distinguish the direction of obligation: `owed by`, `owed to`, `missing from`, and generic `outstanding` remain live.
- Do not translate HT117 as `MA-KA-RI-TE owes U-MI-NA-SI` yet. That is attractive, but three-word headers can contain multiple entity terms (HT96a is the control), so position alone is insufficient.
- It is not a claim that the semantic family itself is new to scholarship. The new contribution is the tested **scope + residual** model and the correction of the backwards-looking computational control.

### Highest-value next experiments

1. **Direction-of-obligation test.** Build an OBSERVED/INFERRED/MISSING ledger for every two- and three-word Haghia Triada header involving MA-KA-RI-TE, U-MI-NA-SI, and comparable entities. Infer source/recipient ordering only from independent commodity/personnel structure. Then ask whether HT117 forces KI-RO to mean `owed by`, `owed to`, or only generic `outstanding`.
2. **True held-out KI-RO test.** Find a KI-RO occurrence not used in this session (new publication, plate-restored damaged occurrence, or an unindexed document). Before reading the downstream entries, freeze: unquantified KI-RO should open a coherent block; if KU-RO closes it, KU-RO should sum the block. Quantified KI-RO should equal an independently recoverable residual when target/delivery are available.
3. **Fix the computational test.** Fork/adapt `kuro_test.py` so KI-RO is evaluated with a forward-scope grammar rather than the KU-RO backwards-total grammar. Do not simply reverse every case: first classify scalar KI-RO vs header KI-RO without using arithmetic outcomes, then test each class separately.
4. **PO-TO-KU-RO remains worthwhile but not novel on HT122.** This session verified `KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97`, but the same arithmetic is already explicitly noted in the source commentary. HT131 is the remaining useful case, and its machine-readable transaction file disagrees with the scholarly commentary by one unit on both a component (61 vs 62) and the grand total (451 1/2 vs 452 1/2). Resolve against GORILA plates before using HT131 computationally.

### Files added this pass

- `analysis/2026-09-07-kiro-scope-residual.md`
- `analysis/kiro_scope_ledger.csv`
- `analysis/kiro_residual_checks.py`

### General lesson

Do not assume that a semantically related accounting term has the same **scope direction** as a known total marker. A negative control can be perfectly reproducible and still be semantically meaningless if the parser points at the wrong side of the marker.

---

## 2026-09-07 – Handover after unified KI-RO grammar pass

### Read this first: the direction-of-obligation experiment above is superseded

Do **not** spend the next session trying to decide whether HT117 says `MA-KA-RI-TE owes U-MI-NA-SI` or the reverse unless new primary evidence forces that syntax.

The wider contextual audit found that Davis & Valério (2020) give a better semantic segmentation: `MA-KA-RI-TE • KI-RO •` is the main heading over personnel material, while `U-MI-NA-SI`, `SA-TA`, and `QI-TU-NE` function as subheadings for 1-lists. They themselves note that KI-RO may mean `missing / absent` in this personnel context.

The earlier held-out HT117 **scope** result survives; the binary debtor/creditor interpretation does not.

Full replacement analysis:
`analysis/2026-09-07-kiro-unified-residual-grammar.md`

The earlier analysis file has an explicit same-day erratum appended rather than being silently rewritten.

### Current frontier model

Treat KI-RO as a **unary residual/negative-status operator**:

**UNFULFILLED / MISSING / OUTSTANDING**

with one semantic type across two domains:

- numeric account: `R = EXPECTED - REALISED`;
- roster/personnel account: `M = EXPECTED_SET \\ REALISED_SET`;
- if the residual set is itemised, KU-RO may close it with `|M|`.

This is a functional model, not a literal translation or language identification.

### Frozen construction grammar

The immediate token after exact clean KI-RO separates two constructions in the current audited set:

- `KI-RO + numeral` → scalar residual;
- `KI-RO •` → forward residual/status block.

Clean cases:

- scalar: HT1, HT15, HT34, HT123+124;
- forward: HT30, HT37, HT88, HT94b, HT117.

**9/9 obey the rule; no clean contradictions.**

Do not count HT93b (`KI-RO[` damaged). Do not merge ARKH4 `A-KI-RO` or HT85b `KI-KI-RA-JA` without independent evidence.

### Independent controls now supporting the model

Arithmetic/cardinality:

- HT34: `100 - 70 = 30 = KI-RO`;
- HT123 DA-TU: `5 - 4 1/4 = 3/4 = KI-RO`;
- HT88: six KI-RO personnel entries → `KU-RO 6`;
- HT94b: five → `KU-RO 5`;
- HT117 first list: ten → `KU-RO 10`.

Held-out semantic prediction:

- **HT15 HIT.** Prediction frozen before reading commentary: `KI-RO 400` should be a residual/unfulfilled amount rather than a total. Commentary independently calls it a deficit / 400 owed from an expected 1,254; visible 684 + 570 = 1,254.

Status-switch controls:

- DI-KI-SE: HT117 KI-RO context vs HT87 comparable QI-TU-NE / MA-KA-RI-TE context without KI-RO.
- KU-PA3-NU: KI-RO HT88/HT117 (also HT1), ordinary HT122.
- PA-TA-NE: KI-RO HT94b, ordinary HT122.
- PA-JA-RE: KI-RO HT88, ordinary HT8/HT29/ZA10 contexts.
- SA-RU: KI-RO HT94b, ordinary HT86/HT95 contexts.

These make a fixed personnel-class meaning for KI-RO unlikely. The same entities can occur with the negative status and without it.

### Reproducibility files

- `analysis/kiro_construction_grammar.csv`
- `analysis/kiro_construction_grammar.py`

Frozen executable assertions:

- construction grammar: **9/9**;
- arithmetic/cardinality controls: **6/6 pass**;
- recurring status-switch entities: **5**.

### Highest-value next experiments

1. **Full-corpus blind parser.** Use the Tsirkas `corpus_v1.json` (or reconstruct equivalent tokens from GORILA/SigLA). Before looking at outcomes, classify every exact KI-RO by next-token form: numeral vs divider vs damaged/other. Then score the frozen 9/9 construction rule on the remaining corpus. Do not tune after seeing failures.
2. **Matched-control test.** Measure how often comparable non-KI-RO signgroups followed by dividers begin coherent forward lists, and how often comparable signgroups followed by numerals behave as residuals. The current 9/9 rule is descriptive until it beats an appropriate baseline.
3. **Personnel-set test.** Build expected/present roster overlaps for HT87/HT117/HT122 and the other personnel 1-lists. Ask whether KI-RO lists preferentially select recurrent roster members whose status can change across tablets. This is the direct test of the set-difference model.
4. **KI-KI-RA-JA extension test.** HT85b structurally resembles a headed 1-list and has long been compared with KI-RO. Test it as an out-of-family candidate only after the KI-RO grammar is frozen. A match may expose morphology; a mismatch is equally informative.
5. **Do not use A-KI-RO as morphology evidence yet.** ARKH4 is a useful negative control precisely because spelling similarity is easy to overread.
6. **PO-TO-KU-RO / HT131 remains separate.** Resolve the one-unit transcription discrepancy against GORILA before using it.

### Falsifiers to preserve

Weaken the unified KI-RO model if a clean record shows any of:

- `KI-RO •` demonstrably continuing the *preceding* account rather than opening a residual block;
- `KI-RO N` independently proven to be a neutral total/fulfilled amount;
- KI-RO personnel names forming a stable exclusive class instead of ordinary entities changing status;
- a securely segmented binary `ENTITY_A • KI-RO • ENTITY_B` with independently forced directionality;
- blind full-corpus failure of the frozen construction rule.

### What is not claimed

- Not a phonetic decipherment.
- Not a language-family result.
- Not discovery of the English gloss `deficit`, `owing`, `missing`, or `absent`; these ideas predate this work.
- Not proof that HT1's 197 represents days, personnel, or any specific unit.
- Not proof that `KI-KI-RA-JA` or `A-KI-RO` are morphological relatives.

The contribution is the **two-construction grammar + cross-domain residual operator + held-out HT15 hit + status-switch controls**.

---

## 2026-09-07 – Handover after post-award obligation-circuit pass

### New operating assumption

The user explicitly requested fewer incremental tests and more post-award reasoning. This pass therefore **takes the KI-RO grammar as provisionally solved** and bridges outward. Do not restart with another KI-RO significance pass unless a new clean contradiction appears.

Read first:
`analysis/2026-09-07-obligation-circuit-post-award.md`

Crosswalk:
`analysis/administrative_state_machine.csv`

### Frontier model now

The best high-compression reconstruction is a Minoan **obligation lifecycle** operating over an ordered palace circuit of persons / groups / workshops / districts:

```text
DA-DU-MA-TA (?)  ->  A-DU  ->  KI-RO
ASSESSED/ALLOCATED   RENDERED   STILL DUE
                         |
                       KU-RO
                    LOCAL TOTAL
                         |
                   PO-TO-KU-RO
                    GRAND TOTAL
```

with `KI-KI-RA-JA` provisionally admitted as a derived **obligation-holder / responsible-assignee participant class**.

### Semantic advances

1. **KI-RO:** refine `missing / deficit` to **DUE-BUT-UNFULFILLED**. This is the common semantic reason both absent workers and missing quantities appear under the same marker.
2. **A-DU:** likely the positive complement: **RENDERED / CONTRIBUTED / PAID / FULFILLED**. HT88 places A-DU and KI-RO states on one tablet; HT95 places A-DU opposite an upstream grain schedule.
3. **DA-DU-MA-TA:** candidate upstream **ASSESSMENT / ALLOCATION / SCHEDULED AMOUNT** field on HT95. Medium confidence only.
4. **KI-KI-RA-JA:** HT85 has 66 workers = eleven six-person groups under A-DU and eleven unit entries under KI-KI-RA-JA. Older scholarship already relates the form to KI-RO. This pass takes the leap that it labels the **party attached to the obligation relation**. Direction—debtor, recipient, supervisor, assignee—remains open.
5. **Circuit model:** Davis & Valério's stable cyclic/bidirectional order of 19 recurring designations implies an administrative route/network. The palace was likely tracking different obligation states over ordered nodes, not creating unrelated flat name lists.

### Linear B bridge

Use Linear B as a **semantic Rosetta key for bureaucratic functions**, not as proof Linear A is Greek.

The later Pylos Ma system distinguishes:

- assessment / expected contribution;
- actual delivery/payment (`a-pu-do-si`);
- outstanding shortfall (`o-pe-ro`).

That is functionally the exact architecture now reconstructed for Linear A (`DA-DU-MA-TA? / A-DU / KI-RO`). Chiapello has proposed direct linguistic equations A-DU~a-pu-do-si and KI-RO~o-pe-ro, but this Hub pass explicitly does **not** adopt the Minoan-Greek conclusion. Functional continuity is enough to exploit.

### What to attack next

Do **not** spend the next session re-proving KU-RO or KI-RO.

Push one level further into the state machine. Highest-value targets:

1. Find the Linear A **exemption / non-liability** field by looking for blocks structurally parallel to Linear B `o-u-di-do-si`.
2. Find **prior-period carry / arrears** language: terms attached to KI-RO residuals that distinguish current from inherited debt.
3. Resolve `DA-DU-MA-TA` as assessment vs allocation vs distribution by following the repeated HT95 entities into other tablets.
4. Attack the `KI-RO -> KI-KI-RA-JA` morphological bridge. Treat a participant derivation as the default working hypothesis and ask what ending/reduplication pattern would produce it.
5. Use the fixed 19-node circuit as the scaffold: assign each repeated word a role/state across tablets, and read records as transitions in a database rather than isolated sentences.
6. Only after functional fields are recovered should phonetics/language affiliation be brought back in.

### What is still explicitly not claimed

- Not a full Linear A decipherment.
- Not proof Linear A is Greek.
- Not proof A-DU and Linear B a-pu-do-si are cognate.
- Not proof KI-RO and Linear B o-pe-ro are cognate.
- Not a literal translation of KI-KI-RA-JA; its participant role is a post-award working leap.

But the project now has something materially stronger than a one-word gloss: a **six-term partial semantic bookkeeping schema** and an explanatory model for how Haghia Triada's ordered administrative records were generated.