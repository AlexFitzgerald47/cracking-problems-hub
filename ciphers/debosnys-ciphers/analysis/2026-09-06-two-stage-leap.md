# Two-stage leap: freeze the shifted model, choose a branch, and read through the visual boundaries

**Session:** 2026-09-06, GPT-5.6 Sol  
**Status:** deliberately aggressive working model; not yet a public solve claim

## What was skipped

Instead of waiting for (1) a full six-page atom transcription and then (2) a statistically clean independent crib, this pass temporarily treats the strongest existing convergence as true and asks what the cipher *must* look like two stages later.

The working assumptions are:

1. the six-glyph signature-like cipher line encodes the stylized plaintext name family `HENECOS DEBOSNOSTYS/A`;
2. Sektu's independently published 2017 phonetic transformation is basically right: syllables are broken/remerged so the rhyme of one syllable can be carried with the onset of the next;
3. Sektu's ordered subglyph decomposition is meaningful;
4. ordinary `N` is an onset-like atom and the signature convergence `N=D` is real;
5. paired forms such as `N.N` are first-class codepoints unless forced otherwise.

These are not promoted to facts. They are frozen as a high-risk attack key so they can make predictions.

## Stage skipped #1: collapse the two surviving signature branches

The previous shifted-phonetic search reduced the raw signature fit to two maps.

Shared:

- `C2 = H`
- `B2 = EN`
- `X = EC`
- `DOT = OS`
- `N = D`
- `U = EB`
- `CROSSB = YS` or `YA`

Branch A:

- `O = O`
- `Z = SN`
- `O2RNO = ST`

Branch B:

- `O = OS`
- `Z = N`
- `O2RNO = T`

For cracking purposes, **select Branch A**.

The reason is independent of the name spelling. Sektu reports `O` as the most frequent Debosnys subglyph. Branch B makes this globally dominant primitive emit the two-character sequence `OS`, while Branch A makes it emit a single vowel-like `O`. In a large Portuguese reference corpus, `O` is about 10.78% of letters while `OS` is about 1.97% of bigrams. A modern Spanish corpus likewise has `o` among the most frequent letters while `os` is only the 23rd-ranked bigram. The exact Debosnys language is unknown, so this is not a likelihood ratio, but it is a strong minimum-complexity prior.

Branch A also avoids introducing a gratuitous homophone: Branch B would make both `DOT` and `O` emit `OS`.

Therefore the aggressive v0 key is:

```
C2      H
B2      EN
X       EC
DOT     OS
N       D
U       EB
O       O
Z       SN
O2RNO   ST
CROSSB  YS / YA
```

Machine-readable version: `analysis/shifted_key_v0.json`.

## Stage skipped #2: stop reading at whitespace glyph boundaries

This is the more important leap.

Under Branch A, the signature components read:

`H | EN | EC | OS | D | EB | O | SN | O | ST | YS`

but the *phonological* shifted units are:

`H | EN | EC | OSD | EB | OSN | OST | YS`

The striking part is where the units cross visual boundaries:

- `DOT + N = OS + D = OSD`
- `O + Z = O + SN = OSN`
- `O + O2RNO = O + ST = OST`

Those are exactly what Sektu's transformation predicts from the natural syllables:

`HE | NE | COS | DE | BOS | NOS | TYS`

because:

- rhyme of `COS` (`OS`) + onset of `DE` (`D`) -> `OSD`;
- rhyme of `BOS` (`OS`) + onset of `NOS` (`N`) -> `OSN`;
- rhyme of `NOS` (`OS`) + onset of `TYS` (`T`) -> `OST`.

So the ugly-looking component assignments are not a defect. **They reconstruct the exact boundary-shifting rule that Sektu proposed independently years before this crib.**

This suggests a concrete architecture:

`ordinary speech -> syllables -> onset/rhyme split -> shift rhyme_i onto onset_(i+1) -> optionally split complex shifted units -> spatially ligature adjacent pieces into visual glyphs`

Whitespace is therefore a calligraphic packing boundary, not a linguistic boundary.

## New outward prediction: DOT is probably a terminal /OS/ rhyme atom

This is the highest-value consequence of skipping ahead.

Inside the signature, `DOT=OS` is followed immediately across the whitespace boundary by `N=D`, producing the shifted unit `OSD`: the rhyme of `COS` plus the onset of `DE`.

But at the **end of a verse line**, there is no following syllable onset to borrow. Sektu's original mechanism says the last encoded unit should therefore collapse to the rhyme itself.

Hence:

> **At a real line boundary, a terminal `DOT` should be able to mean final rhyme `/OS/` without a following onset.**

The poem's lines 3-4 independently end in the dotted-X family already frozen by the Hub as rhyme class B. If image/transcription adjudication confirms that this is exactly `<X DOT>`, then the important prediction is not naively `XP = the word ECOS`. It is subtler:

- `X = EC` can belong to the preceding shifted material;
- the **final component `DOT = OS` is the rhyme-bearing coda**;
- therefore poem lines 3 and 4 should rhyme in `/os/` (or a very close phonetic equivalent).

That is a much cleaner fit to Sektu's line-final-rhyme observation than the earlier whole-glyph `XP=COS/ECOS` reading.

This is now the first thing to try to break.

## Why the recurrent N.N poem ending no longer hurts N=D

The poem's strongest repeated terminal class (lines 1,2,17,18) looks like the paired double-wave `N.N` family.

If we mechanically read that as `N + N` under `N=D`, it would yield something like `DD`, an implausible rhyme ending. That would kill the model.

But Sektu explicitly observed *before this key existed* that `N` cannot stand alone while `N.N` frequently can, and suggested paired `N.N`, `I.I`, `O.O` may be different codepoints from their single forms.

The leap is therefore to **freeze `NN_PAIR` as independent**, not recursively decode it as `D+D`.

This makes a further prediction: single `N` should behave onset-like; `NN_PAIR` should have its own rhyme value and distribution. If future transcription shows ordinary single-N behavior bleeding into N.N contexts, this separation should be reconsidered.

## Language leap: rank Romance/pseudo-Romance above French for the poem, but do not freeze a language

A final controlled leap follows from `/os/`.

- Spanish uses final `-os` extremely productively.
- Portuguese also has very common `os` sequences; a Portuguese reference corpus puts `OS` among its top bigrams.
- Debosnys demonstrably wrote Spanish and claimed Portuguese, although his surviving so-called Portuguese is highly nonstandard and may be phonetic, argot-like, or invented.
- Sektu independently believed the cipher poem and another cipher block were written in different languages and had already found that a straightforward French-syllable model did not fit well.

So for the next source-text/rhyme search, **Spanish + Debosnys' pseudo-Portuguese/pseudo-Romance register move ahead of ordinary French**. Greek/Latin remains live because of the Anacreontic context, but one `/os/` rhyme is not enough to choose among them.

A particularly important possibility is that Debosnys did not encode standard orthography at all. His bizarre pseudo-Portuguese may be direct evidence of the sort of private phonetic respelling/resegmentation habit that the cipher mechanism now appears to require.

## Working key v0

| component | v0 reading | status |
|---|---|---|
| `C2` | `H` | shared by both surviving signature branches |
| `B2` | `EN` | shared |
| `X` | `EC` | shared |
| `DOT` | `OS` | shared; highest-value outward rhyme anchor |
| `N` | `D` | shared after independent onset constraint |
| `U` | `EB` | shared; likely boundary-shifted chunk, not normal phoneme |
| `O` | `O` | Branch A selected by frequency/parsimony prior |
| `Z` | `SN` | Branch A |
| `O2RNO` | `ST` | Branch A |
| `CROSSB` | `YS/YA` | final palaeographic ambiguity |
| `NN_PAIR` | unknown independent rhyme codepoint | deliberately *not* `D+D` |

## What would count as a real breakthrough from here

The next result should not be another internally fitted name.

A real outward hit would be one of:

1. exact `<X DOT>` at poem lines 3-4 plus independent recovery of an `/os/` rhyme there;
2. another exact `DOT` at a verse boundary behaving as `/os/`;
3. exact `N` recurrences whose shifted contexts repeatedly require /d/ onsets;
4. exact `O` recurrences behaving like a high-frequency vowel-like /o/ contribution and disfavoring Branch B;
5. another independently readable plaintext/cipher adjacency reproduced by this same shifted parser.

One such hit should trigger a validator package. Two independent hits would justify describing the work as a serious partial decipherment rather than merely a strong crib hypothesis.

## Bottom line

The leap of faith is now explicit and falsifiable:

**Assume the HENECOS signature crib is right; assume Sektu's boundary shift is right; choose Branch A; parse N.N as an independent codepoint; and read across visual glyph boundaries.**

That produces a coherent provisional key and, crucially, a new poem prediction:

**terminal `DOT` -> rhyme `/OS/`.**

That is where the attack should now be driven outward.
