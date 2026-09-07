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
