# Rime|onset factorization selects Branch B

**Session:** 2026-09-06, GPT-5.6 Sol  
**Status:** conditional breakthrough inside the HENECOS signature model; still awaiting an outward plaintext hit

## The leap after the leap

The shifted-signature work had reduced the atom map to two branches. I initially preferred Branch A by a crude frequency/parsimony prior. That was premature.

Once the cipher is treated as the mechanism Sektu actually proposed — **rime of the previous syllable + onset of the next syllable** — the three repeated `OS` transitions themselves supply a much stronger discriminator.

Candidate plaintext syllables:

`HE | NE | COS | DE | BOS | NOS | TYS`

Shifted phonetic units:

`H | EN | EC | OSD | EB | OSN | OST | YS`

The three complex `OS` transitions align to published subglyph pairs:

```
OS | D  <->  DOT | N
OS | N  <->    O | Z
OS | T  <->    O | O2RNO
```

Sektu had independently proposed that complex shifted groups could be split across two cipher symbols. If we take that literally — first subglyph = rime, second subglyph = following onset — the two branches are no longer equivalent.

## Branch A fails the natural factorization

Branch A was:

```
DOT = OS
N = D
O = O
Z = SN
O2RNO = ST
```

It spells the right flattened strings, but the rime boundary migrates inside the second atom for two transitions:

```
DOT | N      = OS | D    good
O   | Z      = O  | SN   boundary wrong
O   | O2RNO  = O  | ST   boundary wrong
```

That is an awkward way to implement a cipher whose independently proposed generating rule explicitly treats `OS` as the rime constituent.

## Branch B factorizes all three transitions exactly

Branch B is:

```
DOT = OS
N = D
O = OS
Z = N
O2RNO = T
```

Now all three complex shifted groups split at precisely the linguistic boundary:

```
DOT | N      = OS | D
O   | Z      = OS | N
O   | O2RNO  = OS | T
```

This is not a frequency preference. It is a **structural constraint imported from Sektu's pre-existing mechanism**.

Under the conditional assumptions that (a) the HENECOS signature crib is right and (b) two-symbol complex groups split as rime|onset, **Branch B is uniquely selected**.

Reproducer: `analysis/transition_factorization_test.py`.

## Revised provisional atom key

The useful conditional key is now:

| subglyph | provisional value/function |
|---|---|
| `C2` | initial onset `H` |
| `B2` | common transition `EN` |
| `X` | common transition `EC` |
| `DOT` | rime `OS` allograph |
| `N` | onset `D` |
| `U` | common transition `EB` |
| `O` | rime `OS` allograph |
| `Z` | onset `N` |
| `O2RNO` | onset `T` |
| `CROSSB` | terminal rime `YS/YA` |

The surprising duplicate `DOT = O = OS` is no longer gratuitous. It says the cipher has **rime allographs**, potentially selected by visual packing/position. A shorthand-like personal script with many allographs is consistent with the observed huge whole-glyph inventory and with Sektu's description of multiple graphical forms.

## Strongest new poem prediction: terminal XP -> final syllable COS

This factorization sharpens the earlier dotted-X prediction substantially.

The signature supplies:

- `X = EC` = previous rime `E` + onset `C`
- `DOT = OS` = rime of the syllable whose onset is that `C`

Therefore a line-final sequence `<X DOT>` decodes as transition stream:

`EC | OS`

The onset at the right edge of `EC` combines with the following final rime:

`C + OS = COS`.

So if the poem's lines 3 and 4 really end in the exact same `<X DOT>` form as the signature, the model predicts something much more specific than “an /os/ rhyme”:

> **both lines should end in a final syllable /kos/ (`COS` in the working orthography).**

That is an outward, falsifiable prediction derived without choosing a poem plaintext.

It also explains why the old naive whole-glyph guess `XP -> COS` looked uncannily natural: it was accidentally reading the correct reconstructed final syllable even though the true internal mechanism is transition-based.

## What the E-family tells us

The same signature has three single-subglyph common transitions sharing rime `E`:

```
B2 = EN
X  = EC
U  = EB
```

This suggests Debosnys may use dedicated shorthand signs for frequent rime+onset transitions, while less convenient groups such as `OSD/OSN/OST` are factorized as two signs (`OS` marker + onset sign).

That is a plausible compression rule:

- common transition -> dedicated one-sign codepoint;
- other transition -> rime sign + onset sign;
- final syllable -> terminal rime sign;
- graphical ligaturing packs these into larger whitespace glyphs.

If this is right, the cipher is not just a syllable-transition code; it is a **partially abbreviated syllable-transition shorthand**.

## Next decisive checks

1. Freeze visually whether poem line endings 3-4 are exactly `X+DOT`, not merely a dotted-X lookalike.
2. If exact, search source/language candidates under the hard prediction that those lines end in `/kos/`.
3. Find another ordinary `O+Z`, `O+O2RNO`, `DOT+N`, `B2`, `X`, or `U` occurrence. The model predicts `OSN`, `OST`, `OSD`, `EN`, `EC`, `EB` respectively in the same transition phase.
4. Keep `N.N` separate from `N`; terminal N.N must not be decoded as `D+D`.
5. Do not announce a full solve until at least one independent occurrence lands correctly.

## Bottom line

Skipping ahead paid off in one concrete way: the previously ambiguous two-branch signature map is no longer equally ambiguous once the **independently proposed rime|onset split** is enforced.

Conditional working key:

`DOT/O = OS-rime`, `N = D-onset`, `Z = N-onset`, `O2RNO = T-onset`, with `B2=EN`, `X=EC`, `U=EB` as dedicated transition signs.

And the cleanest held-out prediction is now:

**exact terminal `X+DOT` -> final syllable `COS` /kos/.**
