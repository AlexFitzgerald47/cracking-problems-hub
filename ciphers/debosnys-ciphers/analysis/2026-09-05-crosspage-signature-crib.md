# Cross-page signature crib: the first serious reading candidate

**Session:** 2026-09-05, GPT-5.6 Sol  
**Status:** major crib advance; **candidate reading, not yet a validated decryption**

## The jump

Previous work treated the six-glyph line that Sektu called a **signature line** as a place where Debosnys' *unknown real name* might be hidden. That led naturally to speculative cribs such as Jacob Pomries, Henry Debosnys, Rampon, Laugran, etc.

There is a much cheaper crib sitting elsewhere in the same public corpus.

Cryptogram **#4b ends with an unencrypted stylized signature** visibly reading approximately:

`Hênecos Debosnostys`

(stripping accents for computation: `HENECOSDEBOSNOSTYS`). A Cipher Mysteries commenter independently noticed the same unusual form in 2015 and parsed the surname as `DE BOS NOS TYA`; the final few manuscript letters are palaeographically less secure than the rest, so `...TYS` and `...TYA` are both retained as variants.

Sektu's independently published transcription of the cipher signature-like line is exactly six whitespace glyphs:

`C2B2  XP  NU  ZOO  OM2N  SHI`

with internal decomposition:

`<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`

The obvious leap is therefore: **test the known stylized signature from #4b as the plaintext of the six-glyph cipher signature on #2b.** This uses evidence on a different page and was not fitted from the cipher line itself.

Primary/public anchors:
- Wikimedia Commons `Debosnys-Cryptogram-4b.png` (original 1105x563): the plaintext signature is visible at bottom.
- Sektu, *Debosnys Cipher Transcription Revision* (2017-08-04): exact six-glyph and subglyph transcriptions.
- Sektu, *Debosnys' Real Name* (2017-06-28): the line was independently identified as signature-like before this crib was proposed.
- Cipher Mysteries comments, 2015-12-03: independent reading `Henecos` and `DE BOS NOS TYA`.

## Test 1 — strict atomic concatenation, used only as a discriminator

The existing `signature_crib_csp.py` asks whether every distinct atom can emit a fixed 1-2-character plaintext chunk, in published component order, with repeated `O` required to emit the same chunk both times.

That model had **zero** <=2-character solutions for the previously tested shorter form `HENECOSDEBOSNYS`.

For the cross-page form:

`HENECOSDEBOSNOSTYS`

there are **57** strict zero-null solutions with every atom emitting at most two characters. Of those, **32** put the known first-name/surname boundary after the first two whole cipher glyphs.

The `...TYA` variant has the same counts.

This is not unique enough to declare a key, but it is qualitatively different from the old shorter-name cribs.

## Null calibration

`analysis/signature_crosspage_crib.py` freezes the above test and runs two 50,000-trial nulls with the identical search budget.

For `HENECOSDEBOSNOSTYS`, the observed thresholds are 57 total strict mappings and 32 mappings whose first two whole glyphs end exactly at the 7-letter `HENECOS` word boundary.

Approximate Monte Carlo tails (fixed seed, 50,000 trials):

| Null | total-fit tail | word-boundary tail |
|---|---:|---:|
| iid random A-Z strings, length 18 | 0.00154 | 0.00150 |
| random permutations of the target letters | 0.00664 | 0.00626 |

The letter-permutation null is the more conservative of the two because it preserves the target's repeated-letter composition. These p-values are **descriptive, not a solve probability**: the model family was chosen during an exploratory session. Their value is to show that the cross-page signature compatibility is not the default behavior of arbitrary 18-character strings.

## Test 2 — the much cleaner whole-glyph segmentation

The more important observation does not require atom-by-letter concatenation at all.

The visible signature has an almost embarrassingly natural six-part split:

`HENE | COS | DE | BOS | NOS | TYS`

(or final `TYA` under the 2015 reading).

That gives a direct six-glyph crib:

| cipher whole glyph | candidate plaintext chunk |
|---|---|
| `C2B2` | `HENE` |
| `XP` | `COS` |
| `NU` | `DE` |
| `ZOO` | `BOS` |
| `OM2N` | `NOS` |
| `SHI` | `TYS` / `TYA` |

Combined: **`HENE|COS DE|BOS|NOS|TYS`**.

This segmentation is especially notable because the 2015 observer independently spaced the surname `DE BOS NOS TYA`, without reference to Sektu's later 2017 six-glyph transcription. Add the obvious `HENE COS` split of the first name and the independently observed plaintext gives exactly six chunks for exactly six cipher glyphs.

That is the strongest crib now on the board.

## Mechanism consequence: atoms are probably not literal concatenated letters

The proposed whole-glyph reading produces an immediate structural result.

Sektu decomposes `ZOO` as:

`<O Z O>`

The candidate plaintext chunk is:

`BOS`

If each `O` atom emitted the same non-empty literal letter/string in a left-to-right concatenative system, the plaintext for `<O Z O>` would have to begin and end with the same emitted string. `BOS` does not.

So **the strongest signature crib is incompatible with a naive atom = fixed plaintext substring model**, even though the full name happens to admit 57 accidental strict segmentations when word boundaries are allowed to drift.

This is useful, not a failure. It points directly at what Sektu suspected: the internal pieces are more likely **positional phonological features / onset-rime elements / operators inside a syllabic or shorthand-like composite**, rather than little plaintext strings concatenated in order.

## A very suggestive local fit: `NU -> DE`

One candidate whole glyph is particularly informative:

`<N U> -> DE`

Sektu's independent topology says `N` can only occur at the top of a glyph (or under another N), cannot normally stand alone, and he explicitly listed as one possibility that `N` is a **syllable-initial consonant**.

Under the new crib, the simplest phonographic interpretation is therefore:

- `N` contributes an onset near **/d/** (or an onset class containing /d/);
- `U` contributes the nucleus/rime near **/e/**.

This is not yet promoted to a fixed atom key, because a composite code could be non-separable. But it is the first externally anchored sign-value hypothesis that also agrees with a pre-existing structural prediction about where the atom can occur.

It also further weakens `N = universal French nasalization`: `NU -> DE` is a much more direct crib-based explanation for at least this N-glyph.

## Another outward prediction: `XP -> COS`

The candidate assigns the whole glyph `XP` / `<X DOT>` to `COS`.

The same dotted-X component family occurs as the repeated terminal rhyme glyph on cipher-poem lines 3-4. If the cross-page signature crib is correct *and* the same whole form is indeed being used there, the poem's second rhyme class should carry a sound near **/kos/** (or whatever pronunciation Debosnys intended for `cos`).

This is a high-value held-out prediction because the poem occurrence was not used to obtain the signature reading. It now needs image-level identity adjudication and then a source/rhyme search. A failure would sharply downgrade the crib.

## Revised working model

The ranking after this pass is:

1. **Six-glyph cipher signature = stylized plaintext `Hênecos Debosnostys` family** — strongest new crib hypothesis.
2. **Whole glyphs encode syllables/rimes/phonetic chunks; internal marks are positional features/operators** — substantially strengthened.
3. **N is an onset-like element; `NU` may encode `DE`** — first sign-value hypothesis worth attacking across the corpus.
4. **Mixed phonetic + semantic/pictorial layer** — still live.
5. Flat atom-letter concatenation — now a useful null/baseline, but probably the wrong mechanism.
6. Exact Folger key / ordinary pigpen — remain rejected/downgraded.

## Next falsification experiments

1. **Adjudicate `XP` identity** between the signature line and poem lines 3-4. If exact, freeze `XP = COS` as a held-out prediction and search for plausible `/kos/` rhyme behavior/source text.
2. Search every available N-glyph occurrence for `NU`. If the same whole glyph recurs, inspect its local contexts for a plausible `de` / /də/ function. This is the shortest route to turning the crib into a reusable decryption key.
3. Treat `<O Z O> -> BOS` as a feature-grammar clue. Build candidate positional models where identical geometric atoms can have different contributions by slot (onset/nucleus/coda), instead of requiring literal concatenation.
4. Repeat the cross-page test on any other repeated whole glyph shared between #2b and #4. One additional correct prediction would move this from an attractive crib to a serious partial decipherment.
5. Do **not** announce a solve yet. The current claim is a high-value crib and mechanism breakthrough, not a complete plaintext.
