# Folger exact-key test and revised Debosnys mechanism

**Session:** 2026-09-05, GPT-5.6 Sol  
**Status:** material narrowing; no reproducible decryption yet

## Question attacked

The previous session promoted the 1827 Robert Folger Masonic cipher from generic iconographic resemblance to a concrete comparison class. This pass asked the sharper question: **does Debosnys plausibly use the Folger key itself, or only a related compositional idea?**

## Folger mechanism recovered from the NSA solution

The declassified NSA paper *An Unsolved Puzzle Solved* gives enough of the recovered Folger system to remove guesswork:

- Folger has roughly an alphabet's worth of **elemental signs** representing plaintext letters, plus a handful of signs for frequent whole words.
- Those elemental signs are **combined/nested into larger clusters**; a cluster generally corresponds to a plaintext word.
- Reading within a cluster is governed mainly by top-to-bottom / left-to-right placement, while many size and artistic differences are decorative rather than semantic.
- The recovered key is dominated by simple geometric strokes, corners, boxes, arcs and related forms. Vowels include extremely simple marks. U/V/W share a sign; there are a few contextual/special variants and common-word signs.

Primary source: NSA, *An Unsolved Puzzle Solved* (declassified Cryptologic Spectrum article), public PDF via NSA archive.

## Result: exact Folger key is a poor fit

Direct visual/key comparison does **not** support the proposition that Debosnys copied Folger's recovered alphabet unchanged.

Why:

1. Debosnys' recurring atomic-looking components include many curves, waves, circles, astronomical/zodiac-like forms, crosses, dots and percent/slash-like forms that do not map naturally onto the recovered Folger inventory without arbitrary reassignment.
2. A high-value six-unit line at the bottom of cryptogram #2b — the line Sektu identified as signature-like and transcribed as `C2B2 XP NU ZOO OM2N SHI` — does not yield a credible name or phrase under a straightforward Folger-key reading.
3. Debosnys' pictorial tokens (sun, animals, buildings, anchor, etc.) are inserted directly in running cipher text. Folger's system certainly permits decorative camouflage and composite forms, but the Debosnys pages appear to use a richer pictorial vocabulary than the recovered Folger alphabet itself.

**Conclusion:** retire `Debosnys = Folger key` as the working hypothesis unless a future crib produces a non-arbitrary exact match.

## Result: Folger remains a strong mechanism analogue

The more general architecture remains strikingly relevant:

- Folger: small reusable signs -> ordered/nested composite cipher-words.
- Debosnys: Sektu found 1,188 whitespace-bounded glyph instances, 425 whole-glyph types, and demonstrated that those whole glyphs can be decomposed into a much smaller ordered subglyph inventory.

So the useful inference is not "use Folger's alphabet". It is: **model Debosnys as a compositional script whose apparent hundreds of symbols are generated from a smaller atomic inventory.** The atoms may encode letters, phonemes, syllabic features, or semantic operators.

## Important unit-of-encoding constraint from cryptogram #4

A pure Folger-like `one composite cluster = one plaintext word` interpretation has a problem in cryptogram #4. Adjacent verse lines repeatedly end in the same whitespace-bounded terminal glyph, producing the poem's couplet structure. If each such glyph represented a whole plaintext word, many couplets would have to end in the same exact word twice. That is possible but stylistically unusual.

This pushes the Debosnys whitespace units toward **phonetic/rhyme-bearing chunks, syllables, or mixed units**, even if the *method of composing atoms into larger forms* is Folger-like.

The known repeated terminal class at couplets 1 and 9 is especially useful because it gives an internal constraint independent of any proposed plaintext.

## Six-unit signature-like line isolated

The bottom-right line of cryptogram #2b has now been isolated from the primary scan. Sektu's published transcription is:

`C2B2  XP  NU  ZOO  OM2N  SHI`

with a subglyph decomposition given as approximately:

`<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`

This is a high-value future crib because it is positioned and formatted like a signature/closing expression. An Internet claim that the six units read `ULTIME` is not accepted: no reproducible key or derivation was supplied, and forcing one whitespace unit to one letter conflicts with the broader compositional evidence.

## `H.D.D.L.M.F.` remains the strongest literal crib

The omission-count construction remains hard data:

- `H[4]` = **Henry**
- `D[8]` = **Deletnack**
- `D[7]` = **Debosnys**
- `L[6]` = unknown seven-letter L-word
- `M[6]` = unknown seven-letter M-word
- `F[5]` = unknown six-letter F-word

This gives a fixed 7/7/6 search problem for `L.M.F.`. Masonic-context completions are attractive but remain unproved.

## Revised model ranking

1. **Compositional subglyph system** — strongest.
2. **Phonetic/syllabic or rhyme-bearing composite units** — strengthened by poem endings.
3. **Mixed phonetic + semantic/logographic system** — live because large pictorial tokens sit within running text.
4. **Personal system influenced by Masonic/fraternal cryptography** — plausible, with independent Masonic context.
5. **Exact Folger key** — downgraded / effectively rejected absent a future exact crib hit.
6. **Simple monoalphabetic substitution / ordinary pigpen** — poor fit.

## Highest-value next attack

The remaining bottleneck is no longer choosing a historical cipher family. It is producing a **machine-readable atomic transcription** of the complete six-scan corpus and then solving at the subglyph level.

Priority order:

1. Freeze a compact atomic inventory from repeated unmistakable components across all pages.
2. Encode the six-unit signature-like line and the 20 poem line-endings with those atoms first.
3. Use the exact repetition constraints in the poem as internal supervision: same rhyme-class endings should share atomic structure more strongly than random endings if the system is phonetic/compositional.
4. Jointly test French phoneme/grapheme models and known Debosnys/Moore source text, but require mappings to generalize across pages.
5. Attack `L.M.F.` independently as a 7/7/6 historical phrase and use any externally supported expansion as a crib rather than fitting it after the fact.

## Bottom line

No plaintext has been responsibly recovered yet. The useful advance is that a tempting historical-key hypothesis has now been **split and tested**: Folger's exact alphabet is a poor match, while Folger's compositional architecture remains highly relevant. The target is therefore a smaller, learnable Debosnys atomic grammar rather than 425 independent symbols or a stock Masonic substitution alphabet.
