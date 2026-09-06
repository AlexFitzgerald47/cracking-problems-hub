# Hênêcos Debosnostys: a six-glyph signature crib hypothesis

**Session:** 2026-09-05, GPT-5.6 Sol  
**Status:** strongest concrete crib yet; not a validated decryption

## The leap

Sektu independently identified the short terminal sequence

`C2B2 XP NU ZOO OM2N SHI`

as a possible **signature line**, and decomposed it as

`<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`.

Source: https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html

A different primary page, cryptogram #4b, ends in a plainly written signature. The full-resolution Commons scan now resolves that signature much better than the old discussion crops:

**`. Hênêcos Debosnostys .`**

Primary scan: https://commons.wikimedia.org/wiki/File:Debosnys-Cryptogram-4b.png

This spelling matters. A 2015 Cipher Mysteries commenter independently noticed the extended surname and segmented it approximately `DE BOS NOS TYA`; the primary scan shows the final letter more convincingly as **S**, yielding `DE BOS NOS TYS`. That observation existed years before the present cipher alignment and therefore supplies useful independent structure rather than being invented to fit the six glyphs.

Source: https://ciphermysteries.com/2015/11/07/thoughts-on-the-debosnys-ciphers

The obvious high-risk alignment is therefore:

| Cipher whole glyph | Proposed plaintext chunk |
|---|---|
| `C2B2` | **HENE** |
| `XP` | **COS** |
| `NU` | **DE** |
| `ZOO` | **BOS** |
| `OM2N` | **NOS** |
| `SHI` | **TYS** |

or, concatenated:

`C2B2 XP NU ZOO OM2N SHI`  
`HENE COS DE BOS NOS TYS`

This is the first candidate in the Hub work that simultaneously explains (a) why the sequence is formatted like a signature, (b) why it has exactly six whitespace units, and (c) an independently visible Debosnys signature on another cryptogram page.

## Quantitative compatibility check

`analysis/signature_henecos_test.py` tests a deliberately stricter model than the hypothesis actually requires: every atomic subglyph must emit one fixed non-empty plaintext substring, repeated atoms must emit the same substring, and component order is plaintext order.

For normalized `HENECOSDEBOSNOSTYS`, the number of strict assignments is:

- max atom output 1 character: **0**
- max atom output 2 characters: **57**
- max atom output 3 characters: **702**
- max atom output 4 characters: **1,035**

For the conventional shorter `HENECOSDEBOSNYS`, there are **zero** assignments at maximum output lengths 1, 2, or 3, and only 2 when four-letter atom outputs are permitted.

A matched-budget permutation null shuffles the same letters of `HENECOSDEBOSNOSTYS` and runs the identical max-two-character search. With 10,000 deterministic trials (seed 20260905):

- observed compatible assignments: **57**
- null mean: **3.9152**
- null median: **0**
- null maximum: **84**
- empirical `p = 0.007599`

This is **not** a formal decryption significance level: the candidate was recognized post hoc and the atom model is only one possible grammar. It does establish that the unusual repeated-letter structure of the primary signature is materially more compatible with the published repeated-subglyph structure than a random rearrangement of the same letters usually is.

## More important than the p-value: the model changes

The natural whole-glyph mapping contains a crucial contradiction with naive atom concatenation:

`ZOO -> BOS`

Sektu decomposes this glyph as `<O Z O>`. If each O had one ordinary non-empty substring value and the glyph were formed by concatenating those values, the first and last plaintext pieces would have to be identical. They are not in `BOS`.

Therefore, **if this crib is correct, subglyphs cannot all be miniature plaintext strings**. At least some must instead be spatial features, modifiers, phonetic operators, or context-dependent pieces that jointly specify a larger sound/chunk.

This explains why the earlier atom-by-letter signature CSP failed while the compositional architecture remained compelling.

## First provisional values

The whole-glyph crib immediately supplies six provisional chunk values. Two are especially useful because their internal grammar is already independently constrained.

### `NU -> DE`

Sektu's N-glyph grammar explicitly allows `<N U>`, and he gave two structural possibilities for N: an initial consonant, or a suprasegmental vocalic feature. The new crib makes the **initial-consonant branch** much more attractive:

- provisional `N ≈ /d/` or D-like onset;
- provisional `U ≈ /e/` /ə/-like nucleus;
- hence `<N U> ≈ DE`.

This is not accepted as a key assignment yet. It has a sharp cross-page prediction: other N+vowel-like composites should pattern as **dV**, and exact `NU` recurrences should occur where `de` or /də/ is plausible.

`analysis/n_as_d_sanity.py` checks only the aggregate rate. Using the published 30 N-family occurrences across 20 poem lines and a French D frequency of 3.669%, `N≈D` implies an average plaintext line of **40.9 letters**. If four known N.N rhyme terminals are independent paired codepoints and are excluded from ordinary N, the implied line length is **35.4 letters**. Both are plausible poetic-line scales. Frequency alone cannot identify D—C/M/P also occupy plausible ranges—but D is uniquely nominated here by the independent `NU -> DE` crib plus Sektu's initial-consonant grammar.

French frequency source used for the sanity calculation: https://github.com/akleemans/letter-frequency/blob/master/letter_frequency.csv

### `XP -> COS`

Sektu decomposes `XP` as `<X DOT>`. On the primary cipher-poem scan #4a, poem lines 3 and 4 end in a visually matching **dotted-X** terminal family.

Primary scan: https://commons.wikimedia.org/wiki/File:Debosnys-Cryptogram-4a.png

That is exactly the kind of cross-page recurrence the crib must predict. Pending recovery of Sektu's raw line-by-line transcription, call this a **component-family hit**, not yet a proved exact whole-glyph identity.

If the identities are exact, the signature hypothesis predicts that rhyme class B in the cipher poem is **COS / /kos/**. That would be the first actual plaintext/sound chunk carried from an independently readable crib into the poem.

A literal `-cos` rhyme is common enough in Portuguese and Spanish word morphology to make those languages newly interesting for the cipher poem; it is less naturally French orthography. This is only a language-direction clue because the system may be phonetic and `/kos/` can be spelled many ways.

## Why this may reconcile earlier contradictions

The current best mechanism becomes:

**phonetic chunk / rhyme unit represented by a spatial composite of reusable features**

rather than either:

- `whole glyph = letter`, or
- `whole glyph = fixed French syllable with atom values concatenated inside it`.

That hybrid explains several otherwise awkward observations at once:

1. The poem can reuse exact whole glyphs as rhyme-bearing units.
2. Hundreds of apparent glyph types can be generated from a smaller component inventory.
3. Components such as N can have strict positional grammar without being standalone plaintext letters.
4. The six-glyph signature can encode six natural phonetic/orthographic chunks while its internal atoms remain non-concatenative.
5. Different languages could use the same feature inventory but produce very different whole-glyph frequencies, matching Sektu's observation about the cipher poem versus the four-line block above the French plaintext poem.

## Speculative side lead: the strange first name may itself be constructed

`Hênêcos` is not an ordinary version of Henry. It resembles both Greek `henikos` (ἑνικός, 'singular / relating to one') and the learned Greek numerical combining form `heneicos-` for 21. This is **not** evidence for either derivation, and the spelling is not exact. But Debosnys was demonstrably fond of classical-looking material, and the signature may be another invented persona rather than a birth name. Do not use this etymology in the cipher key unless independent 19th-century evidence connects his spelling to one of those forms.

## Falsifiers / next tests

This hypothesis is useful because it can now fail.

1. **Exact XP test.** Recover or reconstruct the raw Sektu transcription for cipher-poem lines 3-4. If their terminal whole glyph is not `XP`, the strongest proposed cross-page transfer fails.
2. **NU recurrence test.** Find every whole-glyph `NU` across the six pages. Under the crib, it should behave like `DE`/`də` much more often than chance; if its contexts make that impossible, reject `NU=DE` and probably the simple six-chunk alignment.
3. **ZOO / OM2N relationship.** `BOS` and `NOS` differ only in onset. If their graphical structures do not show an interpretable shared rhyme/coda feature under a better atomic decomposition, that weakens the crib.
4. **SHI test.** Search for `SHI` elsewhere. A TYS-like /tis/ or /tɪs/ value should have plausible phonotactic behavior, not arbitrary contexts.
5. **Language test from XP.** If `XP=COS` is confirmed at poem lines 3-4, rank French/Portuguese/Spanish/Latin/Greek corpora by the probability of a repeated line-final /kos/ rhyme and by the predicted occurrence of `DE`, rather than assuming French.
6. **Held-out page test.** Learn nothing else from the signature page before testing at least one predicted value on #1 or #3. A crib that cannot generalize is not a key.

## Bottom line

This does **not** justify announcing a solve. It does justify changing the attack order.

The six-glyph sequence should now be treated as a serious candidate encoding of **HÊNÊCOS DEBOSNOSTYS**, with provisional whole-glyph values `HENE | COS | DE | BOS | NOS | TYS`. The next goal is no longer to guess 30 atom values. It is to break this six-value hypothesis on held-out occurrences—or, if it survives, propagate `COS` and `DE` outward until a readable line emerges.
