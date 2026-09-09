# First outward application of the shifted signature key: poem XP -> final /kos/

**Session:** 2026-09-08, GPT-5.6 Sol  
**Status:** first non-crib phonetic recovery under the frozen shared key; not a full plaintext solve

## Executive result

The strongest inherited partial key can finally be pushed onto a cipher occurrence that was not used to fit the signature.

The second composite of Sektu's signature transcription is:

`XP = <X DOT>`

The cross-page signature fit gives, in **both surviving branches**:

- `X = EC`
- `DOT = OS`

Primary scan inspection of cryptogram #4 shows that poem lines 3 and 4 terminate in the same distinctive dotted-X construction. This is the same visual family as signature `XP`; the working adjudication is therefore that both line terminals are `<X DOT>`.

Under the already-frozen shifted rime|onset model, terminal `<X DOT>` reconstructs a final syllable:

`X | DOT = EC | OS -> C + OS = COS`

So the first outward phonetic prediction is:

> **cryptogram #4 lines 3 and 4 end in the syllable /kos/ (orthographic working form COS).**

No value was retuned to obtain this. `X=EC` and `DOT=OS` were fixed by the independent cross-page signature crib before this poem occurrence was used.

This is a stronger claim than the earlier loose `DOT -> /os/ rhyme` prediction. If `XP` is correctly identified, the onset is also recoverable: **/k/ + /os/**, not merely `/os/`.

## Important correction to the branch story

This outward result tests the **seven-value shared core**, not Branch B specifically. Both surviving signature branches already had `X=EC` and `DOT=OS`.

Branch B remains the preferred full branch because the later structural factorization uniquely gives clean rime|onset splits:

- `DOT | N = OS | D`
- `O | Z = OS | N`
- `O | O2RNO = OS | T`

But poem `XP -> COS` survives even if that Branch-B preference is later reversed. It therefore sits one level deeper in the evidence hierarchy.

## Evidence chain

### Observation 1 — signature transcription

Sektu's published 2017 revision gives the signature-like six-glyph line as:

`C2B2 XP NU ZOO OM2N SHI`

and decomposes it as:

`<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`

Source: https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html

### Observation 2 — poem terminal recurrence

On the primary cryptogram #4a scan, lines 3 and 4 end with the same simple dotted-X construction. This whole-glyph recurrence was already frozen in the Hub during the Moore Ode-II test, but had not yet been tied strongly enough to the signature `XP` to count as an outward key application.

Primary scan:
https://upload.wikimedia.org/wikipedia/commons/f/fd/Debosnys-Cryptogram-4a.png

The image-level identity should remain versioned as **high-confidence manual adjudication**, not a machine-pixel identity: the full public Sektu transcription has not been recovered.

### Observation 3 — shared atom values were fitted elsewhere

The signature crib `Hênêcos Debosnostys` / normalized `HENECOSDEBOSNOSTYS` produced the shifted sequence:

`H | EN | EC | OSD | EB | OSN | OST | YS`

and both surviving maps assign:

`X=EC`, `DOT=OS`.

That was derived from the separate signature-like cipher line, not from poem lines 3-4.

### Inference — terminal reconstruction

The shifted mechanism carries a syllable's rime into the following onset, except at line/text termination where the terminal rime has no next onset to borrow.

For signature syllable `COS`, the transition stream around it is:

- `X = EC`: previous rime `E` + onset `C`
- `DOT = OS`: terminal/next transition contributes rime `OS`

At a line ending, `EC | OS` therefore reconstructs the final syllable `C + OS = COS`.

The claim is phonetic first. Exact orthography could be `cos`, `kos`, Greek `κος`, Spanish `cos`, or a Debosnys phonetic/pseudo-language equivalent.

## Immediate source falsification: Moore's uncopied Greek remainder is rejected

Sektu proposed in June 2017 that cryptogram #4 might encode the 20-21 lines of Thomas Moore's Greek *An Ode by the Translator* that Debosnys did not copy onto the reverse. This is now directly testable.

Moore's original ode contains 41 Greek lines. Sektu's count places the cutoff with either 20 or 21 lines remaining, so there are two direct line-preserving alignments:

- remainder starts at Moore line 21; cipher lines 3-4 would align to Moore lines 23-24, ending `Κυπριδος / Λιναον`;
- remainder starts at Moore line 22; cipher lines 3-4 would align to Moore lines 24-25, ending `Λιναον / αινων`.

Neither alignment has a repeated `/kos/` ending at lines 3-4. Therefore:

> **The cipher poem is not a direct line-preserving encoding of Moore's uncopied Greek remainder, if the shared XP key and visual identity are correct.**

This is a useful negative crack: a historically privileged plaintext candidate is now falsified by the partial key rather than by vague structural mismatch.

Moore source scan/OCR:
https://upload.wikimedia.org/wikipedia/commons/0/09/The_poetical_works_of_Thomas_Moore_%28IA_poeticalworkstmo00moor%29.pdf

Sektu source hypothesis:
https://sektu.blogspot.com/2017/06/

### Anti-cherry-pick check: `γυναικος`

The same Moore remainder does contain a later line ending `γυναικος` (`gynaikos`, final syllable `/kos/`), in `Μετα του καλου γυναικος`.

That is acoustically interesting because `/kos/` exists in the independently privileged Greek source family. But it occurs around Moore line 34, which would map to cipher line 13 or 14 under the two possible remainder starts — **not** cipher line 3 or 4. It therefore does not rescue the direct-remainder hypothesis and must not be promoted as a plaintext hit.

## Language update

A repeated line-final `/kos/` pair is substantially more natural as a target in:

- Greek / Greek-influenced material (`-κος` is productive);
- Spanish or pseudo-Romance material (`-cos` endings are ordinary);

than as a native English or ordinary French rhyme.

That does **not** identify the language. It does change search priority, especially because:

1. the reverse side already contains Greek;
2. the plaintext name form `Hênêcos Debosnostys` is conspicuously Hellenizing/pseudo-classical in appearance;
3. Debosnys also left pseudo-Portuguese/pseudo-Romance-looking material whose orthography is highly nonstandard.

For the poem, Greek / Greek-influenced / pseudo-Romance now deserves priority over a default ordinary-French model.

## Independent structural convergence on N=D remains live

Sektu's pre-crib topology analysis found that single `N` never stands alone and can occur only at the top of a glyph (or under another N); he explicitly listed a syllable-initial consonant such as `b` or `d` as one possible explanation before later favoring nasalization.

The shared signature key independently gives `N=D` exactly in the shifted `OS|D` transition. This does not add a new atom in this session, but the outward `XP` result makes the overall onset/rime interpretation less isolated: one shared component pair now produces a poem-final syllable while `N` independently has the topology expected of an onset-like consonant.

`N.N` remains deliberately unresolved as a potentially separate codepoint.

## Failure conditions

The `/kos/` prediction should be killed if any of these occur:

1. higher-quality/transcription evidence shows poem L3/L4 terminal is not the same `XP=<X DOT>` construction;
2. an independently readable plaintext for L3/L4 has a final rhyme incompatible with `/kos/`;
3. a larger cross-page transcription shows `X` or `DOT` behaving incompatibly with the fixed shared values often enough that the signature crib is better treated as accidental;
4. the internal order of `<X DOT>` proves non-phonological in a way that invalidates transition reconstruction.

## Reproducibility

See `analysis/xp_outward_test.py` for the frozen derivation and the two Moore-remainder alignment checks. The script does not search or tune values; it simply applies the already-fixed shared key and asserts the resulting source falsification.

## Bottom line

This is the first outward phonetic read from the cross-page signature key:

**poem #4, lines 3-4: terminal `XP` -> final syllable `COS` /kos/.**

It is not a full decryption. But the partial key is no longer confined to the crib that generated it, and it has already done useful work by killing the strongest direct Greek-remainder candidate without retuning.
