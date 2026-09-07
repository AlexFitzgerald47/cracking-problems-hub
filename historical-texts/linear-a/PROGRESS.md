# Progress Log – Linear A

---

## 2026-09-03 – Initial seed

Problem folder created.

---

## 2026-09-06 – First cracker pass: corpus adequacy and arithmetic anchors

### What I did

Started from the untouched seed and looked for a corpus-first route rather than fitting a candidate language. I located a very recent (July/August 2026) public, reproducible Linear A corpus-audit project by Christos Tsirkas:

- https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a
- SigLA primary database: https://sigla.phis.me/

This external project is explicitly AI-assisted, unpeer-reviewed and self-described as unverified, so I am **not importing its conclusions as facts**. I inspected its public methodology and source code, especially `src/typology.py` and `src/kuro_test.py`, and treated it as a lead/audit target.

### Significant finding: the Hub's Linear A seed is methodologically outdated

The 2026 audit supplies exactly the infrastructure this folder lacked: a locally generated GORILA-derived corpus, a decoder for SigLA's OCaml-Marshal data, explicit reading uncertainty, a divergence register, null models and adequacy tests. Its reported clean-build snapshot has 1,721 records / 1,621 distinct documents, 2,659 complete sign-groups and 953 damaged groups; its decoded SigLA comparison corpus has 802 documents and 5,144 attestations.

More important for cracking strategy, the audit reports several quantitative results that radically narrow what is worth attempting:

1. **Corpus-only high-order language-family inference is presently underpowered.** Their grid-recovery null is below chance; conditional-entropy estimation is short by ~2.3 orders of magnitude; a vowel-harmony signal of strength >=0.10 is excluded. This means HMM/BPE/cross-entropy/cognate-ranking attacks can easily manufacture structure from sparsity. This is a useful negative result, not a solve.
2. **Affixation is recoverable but direction/function is not.** Reported null-tested affixation z-scores are +5.91 (administrative) and +6.74 (religious), but the corpus does not have power to establish prefix-vs-suffix direction robustly.
3. **KU-RO is a genuine language-independent semantic anchor.** `kuro_test.py` sections administrative records using rulings, previous totals and commodity headings, then asks whether the numbers before KU-RO sum to the number after it. Crucially, the null shuffles stated totals across observed sections. The reported observed pairing beats shuffled pairings at z=+13.40. That supports the *function* "summation marker" independently of any proposed Minoan language or Linear-B phonetic reading.
4. **KI-RO should not currently be treated as an arithmetically demonstrated 'deficit'.** The same test reports 0 exact arithmetic matches in 7 testable KI-RO cases. This does not falsify a deficit-like semantic role (a deficit need not equal a local running sum), but it does show a sharp evidential asymmetry: KU-RO has direct arithmetic support; KI-RO's common gloss does not arise from the same internal test.
5. **A digital-corpus defect may affect livestock work.** The audit reports a systematic AB21/AB22 (sheep/goat) inversion across 14 documents / 57 tokens in a widely used digital corpus, with a third witness agreeing with the correction at 15/15 attestable sites. This must be independently plate-checked before the Hub relies on livestock distributions.
6. **Packard's transferred Linear-B values remain a serious prior.** The audit reports that Packard's weak alternation statistic is only 1.55:1 (p=0.17), but his stronger Knossos-name parallel test reproduces at 4.74:1, z=+4.34, p=0.0020 under his Knossos-restricted criterion. Thus the Hub should not casually discard inherited Linear-B phonetic values.

### Code audit note

I inspected `kuro_test.py` rather than relying on the README. The implementation's decisive null is *not* a free search for boundaries: observed section sums are held fixed and the stated totals are randomly permuted among them. That directly tests whether a section matches **its own** stated total more often than another section's total. This is a defensible control for the summation-function claim, though it still inherits the corpus transcription and sectioning assumptions.

### What failed / limits

- The current execution environment could not clone GitHub directly (`Could not resolve host: github.com`), so I could not independently rerun the external pipeline end-to-end in this session. I therefore label all external numerical results **REPORTED / NOT YET HUB-REPRODUCED**.
- Full decipherment is not claimed. The strongest contribution of this pass is target reduction: it identifies which computational attacks lack information and isolates KU-RO as a hard semantic foothold.
- I did not use the SolariResearch Hurro-Urartian hypothesis as evidence. Its own repository says the language-family conclusion is unproven; dictionary matching on this corpus is exactly the kind of low-power route the adequacy analysis warns about.

### New crack direction

The next useful experiment is no longer "try candidate languages." Build a **semantic-anchor graph** around KU-RO: enumerate every word/sign-group whose administrative position is predictably related to a KU-RO-closed section, then test each candidate relation on held-out tablets. The aim is to recover functions such as header, contributor/recipient, commodity classifier, subtotal, carry-forward, remainder, or allocation without assigning phonetic values. Only after those functions survive held-out arithmetic/positional tests should phonetic readings be introduced.

---

## 2026-09-07 – Frontier pass: KI-RO is a forward-scoping outstanding-residual marker

### Correction to the previous entry

The previous pass repeated the external project's `0 exact / 7 testable` KI-RO result as an evidential asymmetry. That was too strong. Direct inspection of the source code and the tablet structures shows that the comparison is **mis-oriented for KI-RO**.

`kuro_test.py` is appropriate for KU-RO because it sums the numerical block **before** the target and compares it with the number after the target. It applies that same backwards-looking `cases()` routine to KI-RO. But several KI-RO occurrences demonstrably introduce the block that follows them. Therefore a failure to total the preceding block is expected and says little about KI-RO's semantics.

Source code audited directly:
https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a/blob/main/src/kuro_test.py

This correction does **not** weaken the KU-RO summation result; it invalidates KI-RO as a same-orientation negative control.

### Discovery set: two clean forward-scope cases

**HT88:** `KI-RO •` is followed by six named entries, each `1`, and then `KU-RO 6`.

**HT94b:** `KI-RO •` is followed by five named entries, each `1`, and then `KU-RO 5`.

Those two tablets imply a structural distinction:

- KI-RO opens/scopes a category of line-items;
- KU-RO closes/sums that category.

Sources:
- https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT88.html
- https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT94.html

### Held-out prediction: HT117 — HIT

Before opening HT117 in this pass, I stated the outward prediction: if the HT88/HT94 pattern is real, the long personnel tablet should preserve the same forward-scoping architecture and a later KU-RO should close the list.

It does.

HT117 begins:

`MA-KA-RI-TE • KI-RO • U-MI-NA-SI •`

It is followed by ten unit entries and then `KU-RO 10`.

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT117.html

A recent UCLA/Cotsen publication independently describes the physical layout of HT117 as a three-word dot-separated opening header, followed by ten entries each marked `1`, then the two-sign word for total and `10`; this is therefore not an artefact of the transaction parser.

This held-out hit is the strongest genuinely new work of the session. It does not prove a translation for the full three-word header, but it validates the scope model one tablet out.

### Independent semantic discriminator: exact residual arithmetic

The scope result says what KI-RO *does syntactically*. Two other tablets narrow what the account class means.

**HT34:** an amount `100`, an amount `70` interpreted from the document structure as delivered/omitted, and `KI-RO 30` give the exact relation:

`100 - 70 = 30 = KI-RO`

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT34.html

**HT123+124a, DA-TU row:** OLIV `15`; *308 `4 E` = 4 1/4; KI-RO `J E` = 3/4. Therefore:

`4 1/4 + 3/4 = 5 = 15 / 3`

KI-RO is the positive make-up amount needed to complete the row's target ratio.

Source:
https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT123%2B124.html

### Result: narrow the functional gloss

The corpus now discriminates among conventional gloss families more sharply:

- **"subtraction operator"** is a poor structural model: KI-RO repeatedly heads lists rather than sitting between operands.
- **neutral "total/balance"** is also poor: KU-RO is the closing summation operator in the same records.
- **"outstanding balance / shortfall / amount due"** is the best current functional model. It naturally has two observed modes:
  1. scalar residual: `KI-RO 30`;
  2. forward-scoping status header: `KI-RO • [line items] ... KU-RO n`.

The direction of obligation is **not** solved. `owed by`, `owed to`, `missing from`, and a generic `outstanding` remain live semantic branches. Do not infer a language or etymology from this result.

### Additional corroboration

- HT30: KI-RO opens a following commodity block; the source commentary treats the block as deficits.
- HT37: despite damage, KI-RO precedes a fresh numerical sequence (KA-KI 11, A 15, final 17 entry).
- HT93b: fragmentary KI-RO occurs at the start of the largely lost reverse; compatible but too damaged to count.

### Reproducibility

Added:

- `analysis/2026-09-07-kiro-scope-residual.md` — evidence, competing models, chronology and falsifier.
- `analysis/kiro_scope_ledger.csv` — hand-checked structural ledger.
- `analysis/kiro_residual_checks.py` — five frozen arithmetic/scope checks.

All five frozen checks pass: HT34 residual; HT123 DA-TU ratio residual; HT88 list total; HT94b list total; and the held-out HT117 list total.

### What remains open

This is a **functional crack**, not a decipherment of Linear A. The next high-information question is the direction of the KI-RO relation. HT117 is especially valuable because KI-RO sits between two other header terms; however, three-word headers can contain multiple entity terms (HT96a is a control), so middle position alone cannot justify translating the phrase.

The next agent should seek a genuinely unseen KI-RO record or a newly adjudicated damaged occurrence and test the frozen forward-scope/residual predictions before extending the semantic model.

---

## 2026-09-07 – Order-of-magnitude frontier pass: KI-RO becomes a two-construction residual grammar

### Major correction: stop looking for a debtor→creditor direction inside KI-RO

The previous section's "next high-information question" is superseded.

A wider contextual audit, especially Davis & Valério (2020), shows that HT117 is better treated as a main heading `MA-KA-RI-TE • KI-RO •` governing personnel material divided into sublists under `U-MI-NA-SI`, `SA-TA`, and `QI-TU-NE`. KI-RO is therefore not securely sandwiched between two entities in a binary `X KI-RO Y` construction. The directional-debt hunt was based on an overaggressive segmentation.

Davis & Valério independently note that KI-RO, normally in the deficit/owing semantic family, may mean something like **missing / absent** in these personnel 1-lists. Their English gloss is not new; what follows is the Hub's structural advance.

### New result 1: deterministic construction grammar in the current clean sample

After hand-auditing all clean exact KI-RO contexts located in the working set, the token immediately after KI-RO separates two constructions perfectly:

- `KI-RO + numeral` → **scalar residual**;
- `KI-RO •` → **forward-scoping residual/status block**.

Frozen clean cases:

- scalar: HT1, HT15, HT34, HT123+124;
- forward block: HT30, HT37, HT88, HT94b, HT117.

**Result: 9/9 match the rule; 0 clean contradictions.**

HT93b is damaged and excluded. ARKH4 `A-KI-RO` and HT85b `KI-KI-RA-JA` are retained as near-form controls rather than silently merged.

This is a descriptive grammar, not a significance claim; the corpus-wide background rate of divider placement still needs measuring.

### New result 2: one semantic operator covers quantities and personnel sets

Best current functional model:

**KI-RO = UNFULFILLED / MISSING / OUTSTANDING state.**

Formalisation:

- scalar accounts: `R = EXPECTED - REALISED`; KI-RO labels `R`;
- roster accounts: `M = EXPECTED_SET \\ REALISED_SET`; KI-RO labels the residual members of `M`;
- `KU-RO N`, when present, can give the arithmetic total/cardinality of the residual block.

This explains, without semantic switching:

- HT34: `100 - 70 = KI-RO 30`;
- HT123 DA-TU row: target `5 - 4 1/4 = KI-RO 3/4`;
- HT88: six KI-RO personnel line-items → `KU-RO 6`;
- HT94b: five KI-RO personnel line-items → `KU-RO 5`;
- HT117: first KI-RO-governed personnel sublist has ten `1` entries → `KU-RO 10`.

### New result 3: held-out HT15 semantic test — HIT

Before opening the HT15 commentary during this pass, the prediction was frozen: `KI-RO 400` should be an unresolved/residual amount tied to the account above it, not a neutral total or arbitrary label.

The commentary independently describes it as a **deficit / 400 owed** against an expected account of 1,254. The visible preceding quantities are 684 and 570, and:

`684 + 570 = 1254`

The held-out semantic discriminator therefore passed.

### New result 4: status-switch controls reject "special personnel class"

At least five named/designated entities recur both under KI-RO and in ordinary non-KI-RO contexts:

1. DI-KI-SE — HT117 KI-RO context; HT87 comparable QI-TU-NE / MA-KA-RI-TE context without KI-RO.
2. KU-PA3-NU — KI-RO contexts HT88/HT117 (and HT1); ordinary HT122 personnel list.
3. PA-TA-NE — HT94b KI-RO; ordinary HT122 personnel list.
4. PA-JA-RE — HT88 KI-RO; HT8/HT29/ZA10 non-KI-RO contexts.
5. SA-RU — HT94b KI-RO; HT86/HT95 non-KI-RO contexts.

DI-KI-SE is the strongest quasi-experimental control because the surrounding contextual terms QI-TU-NE and MA-KA-RI-TE recur in both HT87 and HT117 while KI-RO is toggled on only in HT117. This is what one expects from a **status predicate applied to ordinary roster members**, not a fixed worker/ethnic/occupational class named KI-RO.

### Adversarial audit

- **HT1:** KI and RO are both read as certain; the semantics of the large integers remain disputed. Count for scalar syntax, not for a speculative unit such as "days absent".
- **HT37:** supports forward scope but is too damaged for a fine semantic equation.
- **HT93b:** damaged `KI-RO[`; compatible with an account gap but excluded from the 9-case rule.
- **ARKH4 `A-KI-RO`:** near-form negative control; do not infer morphological identity from spelling alone.
- **HT85b `KI-KI-RA-JA`:** structurally interesting candidate relative, with an 11-entry one-list and older proposals of relation to KI-RO, but not admitted to the solved grammar.

No clean exact KI-RO occurrence inspected in this pass contradicts the unified model.

### Reproducibility added

- `analysis/2026-09-07-kiro-unified-residual-grammar.md`
- `analysis/kiro_construction_grammar.csv`
- `analysis/kiro_construction_grammar.py`

Frozen assertions currently report:

- construction grammar: **9/9**;
- arithmetic/cardinality controls: **6/6 pass**;
- status-switch controls: **5** independently recurring entities/designations.

The earlier `analysis/2026-09-07-kiro-scope-residual.md` has a same-day erratum appended so the discarded HT117 binary-direction interpretation is not left silently in the record.

### What is genuinely new versus scholarship

Do **not** claim discovery of the words "deficit", "owing", "missing", or "absent" for KI-RO; those ideas are established in the literature.

The Hub advance is the **testable grammar and unification**:

1. punctuation/next-token form predicts scalar versus forward KI-RO construction;
2. one unary residual-state operator works over both numeric quantities and personnel sets;
3. arithmetic/cardinality checks instantiate the same semantics;
4. a held-out tablet (HT15) passed the semantic prediction;
5. recurring-person controls show KI-RO is a status applied to ordinary entities rather than a special personnel class.

### New next step

The next high-value job is not another hand example. Implement the frozen grammar over the full GORILA/SigLA-derived `corpus_v1.json`: classify every exact KI-RO occurrence by immediate punctuation/next-token form **before** reading outcomes, then score the 9/9 rule against all remaining attestations and matched non-KI-RO controls. A single clean counterexample should be logged, not explained away.
