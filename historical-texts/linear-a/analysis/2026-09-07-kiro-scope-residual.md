# KI-RO: residual account marker with forward scope

**Session:** 2026-09-07, GPT-5.6 Sol  
**Status:** significant structural advance; not a language decipherment

## Question

Can the conventional KI-RO gloss be narrowed using internal administrative structure alone, without choosing a candidate language?

The previous Hub pass had repeated a recent computational result that KI-RO gives 0 exact matches under the same local-total test used for KU-RO. This session shows that this is the wrong orientation for testing KI-RO: several secure occurrences introduce what follows, whereas KU-RO closes what precedes it.

## Discovery set: KI-RO scopes forward

Two clean personnel tablets exposed the pattern.

### HT 88

The sequence is `KI-RO •` followed by six named entries, each `1`, and then `KU-RO 6`.

Source: https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT88.html

Thus KI-RO is not functioning as a closing total here. It opens a category/list; KU-RO closes that list arithmetically.

### HT 94b

Likewise `KI-RO •` is followed by five named entries, each `1`, and then `KU-RO 5`.

Source: https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT94.html

Again KI-RO opens the block and KU-RO totals it.

## Held-out prediction and result: HT 117

**Prediction, made before opening HT 117 in this pass:** if the HT88/HT94 pattern is real, the longer personnel record containing KI-RO should place KI-RO in a forward-scoping header and the subsequent unit entries should be closed by KU-RO.

**Result:** hit. HT117a begins with the three-word header

`MA-KA-RI-TE • KI-RO • U-MI-NA-SI •`

then has ten entries of `1`, followed by `KU-RO 10`.

Source: https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT117.html

A recent UCLA/Cotsen publication independently describes the physical layout of HT117 as three dot-separated words in the opening header, then ten one-unit entries, then the two-sign word for total plus 10. That confirms that the crucial segmentation is not an artefact of the transaction parser.

Source: https://escholarship.org/content/qt3t90s6zx/qt3t90s6zx.pdf (search-indexed discussion of Fig. 3.8, HT117)

This does **not** by itself prove how MA-KA-RI-TE and U-MI-NA-SI relate to KI-RO. The stronger claim that the header means something like `X owes/is due to Y` remains a hypothesis. Three-word headers can contain multiple entity terms (HT96a is a control), so middle position alone is not enough.

## Independent semantic discriminator: scalar residuals

Forward scope tells us KI-RO is a category/status marker. Two arithmetic contexts narrow what category.

### HT 34: exact subtraction residual

The record has an amount 100, an amount 70 that the commentary independently interprets as delivered/omitted, and `KI-RO 30`. The arithmetic is exact:

`100 - 70 = 30 = KI-RO`

Source: https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT34.html

This supports a residual/shortfall account, not a running-total function.

### HT 123+124a: make-up amount to a target ratio

For the DA-TU row, OLIV is 15. The *308 amount is `4 E` = 4 1/4. KI-RO is `J E` = 3/4. Together:

`4 1/4 + 3/4 = 5 = 15 / 3`

The same tablet explicitly totals OLIV with KU-RO, while KI-RO occupies its own balance field. The commentary uses this relation to discuss the 1:3 ratio.

Source: https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT123%2B124.html

Thus KI-RO is a positive *make-up/residual* amount needed to reach an account target.

## Additional corroboration

- **HT30:** KI-RO introduces a following commodity block. The source commentary describes the preceding entries as contributions/assessments and the KI-RO block as deficits. This is a forward-scoping use, not a closing total.  
  https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT30.html
- **HT37:** despite damage, `KI-RO` precedes a new sequence including KA-KI 11, A 15 and a final 17 entry. Again its visible position is block-initial.  
  https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT37.html
- **HT93b:** fragmentary `KI-RO[` occurs at the beginning of the largely blank/damaged reverse, compatible with forward scope but too damaged to count as a test.  
  https://github.com/mwenge/lineara.xyz/blob/master/commentary/HT93.html

## What this rules out / narrows

The internal evidence now distinguishes several glosses that are often treated as interchangeable.

1. **`KI-RO = subtraction operator` — poor model.** A mathematical operator should not repeatedly act as the heading of a list of people or commodities. HT88, HT94b, HT30 and HT37 show that KI-RO can scope over records rather than sit between operands.
2. **neutral `total/balance` — poor model.** KU-RO is the actual closing summation marker in the same tablets. HT34 and HT123 instead show KI-RO as the positive difference still needed to meet an amount/target.
3. **`KI-RO = outstanding balance / shortfall / amount due` — best current functional model.** It explains both syntactic modes: a scalar residual (`KI-RO 30`) and a heading for the detailed line-items making up that residual/status class (`KI-RO • NAME 1 ... KU-RO n`).

The **direction of obligation** is still unresolved: the corpus here does not yet distinguish cleanly between `owed by`, `owed to`, `missing from`, and a more generic `outstanding`. Do not turn the functional result into a phonetic/language-family claim.

## Correction to the 2026 computational control

`ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a/src/kuro_test.py` is well-oriented for KU-RO: `cases()` takes the numbers **before** a target sign-group and compares their sum to the number **after** it.

For KI-RO this is not a semantic test. The source code itself treats KI-RO as a member of `TOTALS`, finds a `section_start` before it, and calls the same `cases()` routine under the label `KI-RO (should NOT total)`.

Source: https://github.com/ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a/blob/main/src/kuro_test.py

But the primary structural evidence above shows that unquantified KI-RO frequently opens the following block. Therefore the reported `0 exact` KI-RO contrast is expected under a backwards-looking test and should **not** be cited as evidence against the conventional deficit/owed family of meanings. It does not weaken the KU-RO result; it only invalidates KI-RO as that test's negative control.

This corrects the Hub's 2026-09-06 entry, which repeated the 0/7 result as an evidential asymmetry.

## Reproducibility

- `analysis/kiro_scope_ledger.csv` freezes the checked tablet-role observations and sources.
- `analysis/kiro_residual_checks.py` reproduces the exact arithmetic relations and the three block-total checks.

The script is intentionally small: it does not pretend that a hand-checked seven-tablet ledger is a full corpus statistic.

## Next falsifier

On a genuinely unseen or newly published KI-RO occurrence:

- if KI-RO has no immediate scalar amount, predict that it will open a coherent block of line-items rather than close the preceding numeric list;
- if KU-RO closes that block before the next ruling/header, predict that KU-RO will total those forward-scoped entries;
- if KI-RO is quantified as a scalar in an account with an independently recoverable target and delivered amount, predict `target - delivered = KI-RO` (within documented damage/fraction uncertainty).

A clean counterexample to these predictions would force the unified `outstanding residual/status` model to be weakened.

## Novelty caution

The words `owed`, `deficit`, `balance`, `missing` and related interpretations have a long history in Linear A scholarship, so this is **not a claim to have coined the semantic family**. The advance made here is narrower and testable: (a) separating closing KU-RO from forward-scoping KI-RO, (b) obtaining a held-out hit on HT117 after forming the scope hypothesis on HT88/HT94, (c) unifying the scope pattern with exact residual arithmetic on HT34/HT123, and (d) identifying why the recent backwards-looking KI-RO computational control is mis-specified.

---

## Same-day erratum / supersession after wider contextual audit

The HT117 discussion above is **partly superseded** by the later analysis in `analysis/2026-09-07-kiro-unified-residual-grammar.md`.

Davis & Valério (2020) provide a stronger contextual segmentation than the binary-relational reading entertained above. Their analysis treats `MA-KA-RI-TE • KI-RO •` as the main heading over the personnel material, with following terms including `U-MI-NA-SI`, `SA-TA`, and `QI-TU-NE` functioning as subheadings for separate 1-lists. They also explicitly raise the possibility that KI-RO in these personnel records means something in the `missing / absent` family.

Therefore:

- retain the **held-out scope hit**: KI-RO is indeed in a heading whose effect extends forward over personnel entries, and KU-RO closes a unit list;
- **withdraw the suggestion that HT117 is evidence for a binary `X KI-RO Y` debtor/creditor relation**;
- supersede the next-step question `who owes whom?` with a stronger model test: whether KI-RO is a unary `UNFULFILLED / MISSING / OUTSTANDING` status that operates over both scalar quantities and sets of personnel.

The wider audit found a deterministic two-construction grammar in the current clean sample — `KI-RO + numeral` for scalar residuals and `KI-RO •` for forward residual blocks — plus status-switch controls in which the same named entities recur both with and without KI-RO. See the newer analysis and executable ledger for the frozen result.
