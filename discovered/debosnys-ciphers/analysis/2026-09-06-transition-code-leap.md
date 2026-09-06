# Transition-code leap: stop asking what each atom 'letter' is

**Session:** 2026-09-06, GPT-5.6 Sol  
**Status:** strongest mechanism hypothesis after deliberately skipping ahead; conditional on the signature crib

## The key reframe

The previous pass still tried too hard to give every subglyph an independent plaintext string. That is probably one level too low.

Take the candidate plaintext signature:

`HE | NE | COS | DE | BOS | NOS | TYS`

and apply the phonetic transformation Brian/Sektu proposed independently in June 2017: retain the initial onset, then encode the **rime of one syllable plus the onset of the next**, finishing with the last rime.

This gives:

`H | EN | EC | OSD | EB | OSN | OST | YS`

Now compare Sektu's later, independently published component stream for the signature-like cipher line:

`C2 B2 X DOT N U O Z O O2RNO CROSSB`

There is a striking chunking which no longer requires choosing arbitrary atom values:

```
H    | EN   | EC | OSD       | EB | OSN   | OST          | YS
C2   | B2   | X  | DOT + N   | U  | O + Z | O + O2RNO   | CROSSB
```

This is a much cleaner object than either the naive whole-glyph map or the forced atom map.

## Why this matters

The three transitions with the very common rime `E` are:

- `E + N = EN` -> one component `B2`
- `E + C = EC` -> one component `X`
- `E + B = EB` -> one component `U`

The three transitions with the more complex rime `OS` are:

- `OS + D = OSD` -> two components `DOT N`
- `OS + N = OSN` -> two components `O Z`
- `OS + T = OST` -> two components `O O2RNO`

Sektu's 2017 hypothesis explicitly anticipated that common/simple phonetic groups might receive one symbol while complex or uncommon groups could be **split across two symbols**. The signature crib now appears to instantiate exactly that prediction.

This turns the Debosnys system from a mysterious 425-glyph alphabet into something much more specific:

> **a graphical code for transitions between adjacent syllables.**

The elementary code unit can therefore be a phonetic edge such as `EN`, `EC`, or `EB`, not necessarily a letter. Larger visual glyphs can pack multiple such edges or fragments; conversely, one edge can cross a whitespace-bounded visual glyph boundary.

## Finite-state interpretation

Represent a plaintext syllable as:

`S_i = onset_i + rime_i`.

Instead of encoding `S_i` directly, Debosnys may encode:

- initial boundary: `onset_0`
- internal transition `i`: `rime_(i-1) + onset_i`
- final boundary: `rime_n`

Decoding is therefore a finite-state transduction rather than substitution.

Given transition stream:

`H | EN | EC | OSD | EB | OSN | OST | YS`

recover:

- H + E -> HE
- N + E -> NE
- C + OS -> COS
- D + E -> DE
- B + OS -> BOS
- N + OS -> NOS
- T + YS -> TYS

The rime at the left side of one transition belongs to the previous syllable; the onset at the right belongs to the next syllable.

This explains why ordinary cryptanalysis has struggled: the code deliberately places pieces of adjacent plaintext syllables together and then uses a variable graphic packing layer on top.

## The whitespace problem stops being a problem

Sektu originally defined a glyph as a cluster bounded by white space. His signature decomposition is:

`<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`.

The transition chunking is instead:

`<C2> <B2> <X> <DOT N> <U> <O Z> <O O2RNO> <CROSSB>`.

So several true phonetic units **cross the visible whitespace boundary**:

- `DOT N = OSD` crosses `XP | NU`;
- `O O2RNO = OST` crosses `ZOO | OM2N`.

That looks bizarre under a substitution model. Under Debosnys' proposed broken-and-remerged phonetic mechanism it is exactly the sort of deliberate boundary displacement we should expect.

## A more robust provisional key

The strongest current readings are now transition chunks, not isolated atoms:

| cipher chunk | provisional phonetic unit |
|---|---|
| `C2` | `H` |
| `B2` | `EN` |
| `X` | `EC` |
| `DOT N` | `OSD` |
| `U` | `EB` |
| `O Z` | `OSN` |
| `O O2RNO` | `OST` |
| `CROSSB` | `YS` / `YA` |

This mapping is stored in `analysis/shifted_transition_key_v0.json`.

It is conditional on the signature crib, but it avoids the unnecessary `O=O` versus `O=OS` argument. Those atom-level splits can be learned later from repeated contexts.

## N=D becomes cleaner, not weaker

Sektu independently observed that N can occur only at the top of an N-glyph and explicitly offered a syllable-initial consonant such as `b` or `d` as one possible explanation.

In the transition chunk `DOT + N -> OSD`, the last sound is exactly the onset `D` of the next natural syllable `DE`.

Thus the simplest split is still:

`N -> D`

and therefore, inside this context:

`DOT -> OS`.

But the transition model is cautious about generalizing `DOT=OS` outside the `DOT N` environment until an outward occurrence proves it.

This distinction matters for the poem's dotted-X ending: the line-final form may be a terminal-rime code/allograph rather than the same internal transition decomposition.

## The N.N paradox is predicted

If ordinary `N` is an onset `D`, parsing the poem's repeated terminal `N.N` as `N+N` would create a nonsense `DD` rime.

Sektu independently noted that N cannot stand alone while N.N frequently can, and suggested N.N may be a separate codepoint.

The transition architecture explains why such terminal codepoints are needed:

- internal position requires `rime + next onset` transitions;
- final position has **no next onset**, so it requires a terminal-rime code.

Therefore `NN_PAIR` can naturally belong to a different terminal inventory while the ordinary single N remains an onset-bearing transition fragment.

That is a much stronger functional reason for pair-codepoints than merely saying they look ligatured.

## The large glyph inventory now makes sense

Sektu observed 1,188 whitespace glyph instances, 425 observed glyph types, and estimated from singleton behavior that the underlying whole-glyph inventory could be around 1,500.

A 1,500-symbol alphabet is absurdly large. A transition code is not.

If a language has dozens of common rimes and a few dozen possible syllable onsets, the cross-product `rime x next-onset`, plus line-boundary codes, split complex transitions, ligatures, allographs and pictorial/logographic exceptions, naturally produces hundreds to low thousands of possible visual clusters.

So the enormous type inventory ceases to be an anomaly and becomes a positive architectural prediction.

## What to attack now

The next solver should not be a substitution solver. It should be a **phonotactic finite-state decoder**.

For each candidate language/register:

1. generate likely syllabifications;
2. transform each candidate plaintext into `initial onset | rime+next onset | ... | final rime`;
3. allow frequent/simple transition groups to map to one subglyph and complex groups to split into two;
4. allow the graphical whitespace packing to be offset from transition boundaries;
5. seed the codebook with the eight signature transition chunks above;
6. score candidate paths jointly across all poem lines, forcing terminal rhyme equality within each couplet;
7. treat pictures and paired terminal signs as separate code families rather than forcing them into the ordinary transition alphabet.

This is a radically smaller and better structured search than assigning meanings independently to 425 glyphs.

## Most important falsification

The model now makes a very direct prediction:

> wherever `B2`, `X`, and `U` occur in the same transition phase, their decoded phonetics should behave like **E+N, E+C, E+B** respectively, not arbitrary unrelated chunks.

A second independent crib containing any two of those units can break or validate the model quickly.

Likewise, if ordinary `N` is really onset D, its placement should repeatedly line up with /d/-initial syllables after transition reconstruction.

## Bottom line

The leap is not 'we found more letter values'. It is more consequential:

**Debosnys may be encoding the edges between syllables rather than the syllables or letters themselves.**

The candidate signature gives the first eight transition-code entries:

`H, EN, EC, OSD, EB, OSN, OST, YS`.

That mechanism simultaneously explains the unnatural breaks, variable glyph complexity, rhyme-only line endings, N-topology, pair-codepoints, and the otherwise absurdly large glyph inventory.

This is the model to try to crack outward now.
