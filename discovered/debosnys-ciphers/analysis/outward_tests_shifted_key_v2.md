# Outward tests for the shifted-signature partial key

**Frozen:** 2026-09-05, GPT-5.6 Sol  
**Purpose:** make the new signature key fail somewhere outside the data used to derive it.

## Shared candidate values to test first

Derived from the primary `Hênêcos Debosnostys` signature, Sektu's independent 2017 shifted-rhyme hypothesis, his 2017 signature subglyph order, and the independently suggested N-onset function:

- `C2 = H`
- `B2 = EN`
- `X = EC`
- `DOT = OS`
- `N = D`
- `U = EB`
- `CROSSB = YS`

Middle branch unresolved:

- A: `O=O, Z=SN, O2RNO=ST`
- B: `O=OS, Z=N, O2RNO=T`

## Test 1 — exact XP recurrence in the cipher poem

**Prior observation not used to derive the key:** cipher-poem lines 3-4 end in the same dotted-X family.

**Prediction:** if image-level adjudication shows those terminal whole glyphs are exactly `XP = <X DOT>` in Sektu's notation, the flattened candidate value is:

`XP = ECOS`

The two lines must therefore share a terminal phonetic sequence equivalent to `ECOS` under Debosnys' spelling/pronunciation convention.

This is not itself proof, because identical glyphs trivially have identical values. It becomes a real test only if a source/plaintext candidate for those lines is obtained independently.

**Failure condition:** exact XP identity plus an independently established plaintext rhyme incompatible with `ECOS` without ad-hoc remapping.

## Test 2 — exact NU recurrence

**Prediction:** any exact recurrence of `NU = <N U>` has flattened value:

`NU = DEB`

Note that this is a *shifted* chunk: `D` is the onset of one syllable and `EB` can bridge the rhyme of that syllable to the onset of the next. Do not expect `NU` to equal a normal word or syllable boundary.

**Failure condition:** an independently readable occurrence of exact `NU` that cannot contain this shifted phonetic sequence.

## Test 3 — N topology

The shared key assigns `N = D`.

Sektu had already inferred from topology that N could be a syllable-initial consonant, explicitly offering French `b` or `d` as examples. Under the candidate, every ordinary single-N occurrence should behave consonantally/onset-like after the shifted transformation.

**Failure condition:** multiple clear cases where ordinary single N must be a vowel/rhyme feature in independently readable plaintext. Keep `N.N` separate: it may be a distinct codepoint and is not predicted to equal `DD`.

## Test 4 — C2/B2 split

The first signature whole glyph is `<C2 B2>` and the key predicts:

`C2B2 = HEN`

with `C2=H` and `B2=EN` under shifted phonetic grouping.

**Prediction:** separate recurrences of C2 or B2 should preserve those flattened values. This is especially valuable because the first whole glyph was not manually segmented by us; Sektu independently supplied exactly two ordered internal pieces.

## Test 5 — middle-branch discriminator

Find any independently constrained recurrence of `O`, `Z`, or `O2RNO`.

Branch A predicts:
- O = `O`
- Z = `SN`
- O2RNO = `ST`

Branch B predicts:
- O = `OS`
- Z = `N`
- O2RNO = `T`

A single strong recurrence could eliminate one branch.

## Test 6 — line-ending/rhyme compatibility

If the cipher poem really uses rhyme-bearing final symbols, any signature-derived component that recurs in a line-final composite should yield something that can function as a rhyme fragment under the same shifted phonetic scheme. This test should be run against **independently sourced plaintext candidates**, never by inventing words to fit the key.

## Stop conditions

Kill or sharply downgrade the signature key if:

1. the six-glyph line is shown not to be a signature/closing name;
2. the primary `Hênêcos Debosnostys` reading is materially wrong;
3. component order differs from Sektu's published order;
4. two independent recurrences require incompatible shared values;
5. the key only survives by allowing page-specific remapping.

Promote to a partial decipherment claim only after at least one value correctly predicts evidence outside the signature used to derive it.
