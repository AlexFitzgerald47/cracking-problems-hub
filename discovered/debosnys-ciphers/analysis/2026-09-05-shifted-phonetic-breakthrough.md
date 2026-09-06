# Shifted-phonetic breakthrough: the old Sektu hypothesis locks onto the new cross-page crib

**Session:** 2026-09-05, GPT-5.6 Sol  
**Status:** strongest partial-decipherment hypothesis in the Hub; not yet a validated solve

## Executive result

A leap that initially looked like loose pattern-fitting becomes much stronger when combined with an **independent mechanism hypothesis published by Sektu in June 2017**.

Three ingredients were developed independently:

1. A 2015 observer read the plaintext stylized name on Debosnys' material as approximately **`Hênecos DE BOS NOS TYA`**.
2. Sektu later transcribed the cipher's separate signature-like line as six whitespace glyphs and eleven ordered subcomponents:

   `C2B2 XP NU ZOO OM2N SHI`

   `<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`

3. Before publishing that subglyph transcription, Sektu had proposed a specific phonetic mechanism for Debosnys: write speech phonetically, then **break/remerge it so a unit can contain the rhyme of one syllable plus the onset of the next**. He illustrated the operation on Debosnys' French verse and explicitly allowed complex groups to be split across multiple symbols.

Applying that already-published mechanism to the independently observed name produces a highly structured fit to the cipher component stream.

## Apply Sektu's transformation to the known name

Take the conservative 2015 spelling, accent-stripped:

`HENECOS DEBOSNOSTYA`

The obvious syllabic parse is:

`HE | NE | COS | DE | BOS | NOS | TYA`

Split each syllable into onset + rhyme:

| syllable | onset | rhyme |
|---|---|---|
| HE | H | E |
| NE | N | E |
| COS | C | OS |
| DE | D | E |
| BOS | B | OS |
| NOS | N | OS |
| TYA | T | YA |

Now apply Sektu's 2017 resegmentation: initial onset, then `rhyme_i + onset_(i+1)`, then the final rhyme.

This gives:

`H | EN | EC | OSD | EB | OSN | OST | YA`

Flattened:

**`HENECOSDEBOSNOSTYA`**

The transformation therefore reconstructs the observed name exactly while predicting where the phonetic boundaries *ought* to lie.

## Fit those boundaries to Sektu's eleven cipher components

The eleven ordered cipher components are:

`C2 | B2 | X | DOT | N | U | O | Z | O | O2RNO | CROSSB`

A context-free component -> one-or-two-character search has 57 mappings that can spell the 18-character target. That by itself is not impressive enough.

But require **every boundary of Sektu's independently specified shifted-phonetic units** to coincide with a cipher-component boundary. The 57 possibilities collapse to **four**.

Then add a second independent observation from Sektu's August 2017 N-glyph study: because `N` only occurs at the top of a glyph and cannot stand alone, he specifically proposed that it could be a **syllable-initial consonant such as French b or d**. In the cross-page name the relevant onset is exactly **D**.

Require `N = D`. The four mappings collapse to **two**.

`analysis/signature_shifted_phonetic_model.py` reproduces the count.

## Shared partial key — the important part

Both surviving mappings agree on seven assignments:

| Debosnys component | candidate phonetic text |
|---|---|
| `C2` | **H** |
| `B2` | **EN** |
| `X` | **EC** |
| `DOT` | **OS** |
| `N` | **D** |
| `U` | **EB** |
| `CROSSB` | **YA** (or `YS` if the final letters are read from the primary scan that way) |

Only the middle `O / Z / O2RNO` allocation remains ambiguous:

### Branch A

- `O = O`
- `Z = SN`
- `O2RNO = ST`

Full atom stream:

`H | EN | EC | OS | D | EB | O | SN | O | ST | YA`

### Branch B

- `O = OS`
- `Z = N`
- `O2RNO = T`

Full atom stream:

`H | EN | EC | OS | D | EB | OS | N | OS | T | YA`

Both flatten exactly to:

`HENECOSDEBOSNOSTYA`

and both preserve every shifted-phonetic boundary.

The primary-image reading `...TYS` changes only the final value `CROSSB = YS`; all other assignments survive unchanged.

## Why this is substantially stronger than the earlier whole-glyph guess

The previous cross-page pass noticed the tempting six-part visual split `HENE | COS | DE | BOS | NOS | TYA`. That was useful but still somewhat arbitrary.

The shifted model explains **why whitespace-glyph boundaries look wrong**.

Under Branch B, for example, the six visible cipher glyphs output:

- `C2B2` -> `HEN`
- `XP` -> `ECOS`
- `NU` -> `DEB`
- `ZOO` -> `OSNOS`
- `OM2N` -> `T`
- `SHI` -> `YA`

Those are linguistically ugly in isolation — exactly what Sektu's 2017 mechanism predicts after material has been broken and remerged at unnatural phonetic positions. Concatenate them and the normal name reappears.

This also resolves the earlier apparent paradox of `<O Z O>` containing the same `O` twice while a forced whole-glyph `BOS` reading would begin and end differently. We should not assign plaintext at whitespace-glyph boundaries in the first place.

## The N=D convergence is the strongest independent hook

The most striking single agreement is `N -> D`.

Sektu inferred from **glyph topology alone** that N might be a syllable-initial consonant, explicitly giving `b` or `d` as examples. That was published before this cross-page crib was constructed.

The shifted-signature model independently places the single `N` component at precisely the `D` onset in:

`... COS | DE ...`

The candidate therefore does not merely make the name fit; it lands on one of the concrete functional values Sektu had already said the N topology could support.

His later preference for nasalization was based on a frequency comparison that the Hub has already weakened statistically, and that comparison is further complicated by `N.N` possibly being a separate codepoint.

## What this says about the writing system

The best current model is no longer simply "syllabic".

It looks closer to:

1. phonetic plaintext;
2. syllabify it;
3. shift boundaries so rhyme material is carried toward the following onset;
4. allow complex shifted groups to split into smaller reusable components;
5. combine those components spatially into whitespace-bounded glyph clusters.

That is remarkably close to the direction Sektu reached qualitatively but could not exploit because he lacked a usable crib.

The new cross-page name supplies that crib.

## A sharper held-out prediction

The signature gives the composite `XP = <X DOT>` the candidate flattened value:

`X + DOT = EC + OS = ECOS`

The Hub had already frozen the poem's lines 3-4 as ending in a **dotted-X component family**, independently of this name attack.

If image adjudication shows that those poem terminals are the exact same `XP` whole form/allograph, the shifted-key model predicts those lines end in a phonetic chunk equivalent to **`ECOS`** (or a systematic language-specific pronunciation thereof).

That would strongly favor a Greek / pseudo-Greek / other language with such a rhyme over the already-rejected direct Moore `string/sing` reading. Conversely, an exact XP identity combined with a plainly incompatible independently recoverable rhyme would damage the signature model.

The identity still needs to be frozen against the scans; "same dotted-X family" is not yet enough.

## Current epistemic status

This is **not a complete solve claim**. It is, however, materially stronger than every previous Debosnys plaintext proposal in the Hub because it combines:

- plaintext evidence from a different page;
- an independently observed 2015 segmentation of that plaintext;
- Sektu's independently published 2017 phonetic resegmentation mechanism;
- Sektu's independently published ordered subglyph stream;
- and his independently derived N-onset constraint.

The raw strict search gives 57 ways to fit the name. The old mechanism shrinks that to four; the old N-topology hypothesis shrinks it to **two**, sharing seven component values.

That is now the primary cracking lane.

## Next work

1. Adjudicate whether poem line-end dotted-X is exactly `XP`; if yes, test the `ECOS` prediction.
2. Search visually for exact `NU`, `C2`, `B2`, `XP`, and `ZOO` recurrences across the six scans.
3. Build a parser implementing shifted-rhyme boundaries rather than whitespace boundaries.
4. Use the shared candidate values `C2=H`, `B2=EN`, `X=EC`, `DOT=OS`, `N=D`, `U=EB` first; postpone the A/B middle branch until another occurrence separates it.
5. Treat any outward contradiction as a falsifier. One genuine independent hit would justify calling this a partial decipherment and preparing a validator package.
