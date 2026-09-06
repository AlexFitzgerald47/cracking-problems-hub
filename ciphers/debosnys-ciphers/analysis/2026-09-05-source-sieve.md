# 2026-09-05 source sieve — cryptogram #4

## Status

Not a solve. This session materially narrows the attack and produces one new high-value plaintext candidate plus one correction to a published statistical argument.

## Primary evidence recovered

A complete public scan set exists on Wikimedia Commons (ultimately sourced from the Brewster Memorial Library / Essex County material):

- Debosnys-Cryptogram-1.png
- Debosnys-Cryptogram-2a.png
- Debosnys-Cryptogram-2b.png
- Debosnys-Cryptogram-3.png
- Debosnys-Cryptogram-4a.png
- Debosnys-Cryptogram-4b.png

Cryptogram 4a is available at 1107×1493 px and 4b at 1105×563 px.  The scan itself labels #4 as `monographie, verse.` (handwriting uncertain in exact punctuation/spelling).

Commons category:
https://commons.wikimedia.org/wiki/Category:Henry_Debosnys

## What is already established externally

1. Cryptogram #4 has 20 lines and a couplet-like terminal pattern: adjacent lines repeat their final glyph/symbol class.  This has been noted independently by Cipher Mysteries / Cipherbrain and by Sektu.
2. The text on the reverse, presented by Debosnys as a Greek "translation", is meaningful Greek.
3. Olivia von Westernhagen identified that Greek text in 2016 as Thomas Moore's **"An Ode by the Translator"**, from Moore's *Odes of Anacreon*. Therefore the Greek is not Debosnys translating his cipher plaintext into Greek; Moore wrote it decades earlier.
4. Later work reported by Klaus Schmeh / Cipherbrain found that a large fraction of Debosnys' apparently original unencrypted writing and art was copied or assembled from earlier sources.  In particular, "The City of the Death" was pieced together from Thomas Moore poems.
5. Sektu's transcription work treats a whitespace-bounded cluster as one glyph and reports 1188 instances of 425 glyph types across the material, then decomposes those glyphs into a smaller ordered subglyph inventory.  This makes a simple one-glyph-per-letter MASC an unattractive default model.

Sources:
- https://ciphermysteries.com/2015/11/07/thoughts-on-the-debosnys-ciphers
- https://scienceblogs.de/klausis-krypto-kolumne/2015/12/03/fall-debosnys-liefert-ein-gedicht-den-entscheidenden-hinweis/
- https://scienceblogs.de/klausis-krypto-kolumne/henry-debosnys-was-a-copyist/
- https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html
- https://sektu.blogspot.com/2017/06/first-hypothesis-for-debosnys-cipher.html

## New candidate: Thomas Moore, *Odes of Anacreon*, Ode II

A targeted source sieve of Moore's *Odes of Anacreon* produced an unusually strong structural candidate that I have not found named in indexed prior Debosnys discussion:

**Ode II** is exactly **20 verse lines**, and all 20 are organized as rhyming couplets.

Project Gutenberg text:
https://www.gutenberg.org/cache/epub/8187/pg8187-images.html

The structural coincidence matters because:

- cipher #4 = 20 lines;
- cipher #4 = adjacent-line terminal repetition consistent with AABBCC... couplets;
- Moore Ode II = 20 lines;
- Moore Ode II = ten rhyming couplets;
- the reverse of this same cipher sheet is already sourced to Moore's *Odes of Anacreon*;
- Debosnys is independently documented as repeatedly copying Moore.

This raises Ode II far above an arbitrary poem match. It is still only a candidate until it survives glyph-level tests.

### Strong held-out prediction

Ode II has a particularly useful feature: its opening four lines are repeated, with slight framing, at the end.

Rhyme classes:

- lines 1–2: `song / along`
- lines 3–4: `string / sing`
- lines 17–18: `song / along`
- lines 19–20: `string / sing`

If the repeated terminal cipher glyphs encode a rhyme (as Sektu argues), then under the Ode-II plaintext hypothesis:

1. the terminal class of cipher lines 1–2 should recur at lines 17–18;
2. the terminal class of cipher lines 3–4 should recur at lines 19–20.

This is a much sharper test than simply asking whether each adjacent pair rhymes. A failure of both recurrence predictions is strong evidence against Ode II as the direct line-preserving plaintext.

### Secondary predictions

If #4 is a line-preserving phonetic/polygraphic encoding of Ode II, then:

- line-level glyph counts should correlate positively with a reasonable phonetic-unit count of the corresponding Ode-II lines;
- repeated plaintext fragments in lines 1–4 versus 17–20 should generate detectable repeated subglyph n-grams even if complete whitespace-bounded glyphs are homophonically varied;
- likely rhyme nuclei `/ong/` and `/ing/` should yield repeated terminal substructure across those non-adjacent pairs.

These tests require a frozen machine-readable transcription of all 20 lines. Published discussion says Sektu made one, but no downloadable transcription was located in this session.

## New audit result: Sektu N-glyph histogram contains a one-line inconsistency

Sektu's 2017 test of the hypothesis `N subglyph ≈ French vowel nasalization` states:

- cipher poem: 20 lines;
- total N-glyphs: 30;
- histogram: 0 N = 2 lines; 1 N = 6; 2 N = 9; 3 N = 2.

But 2+6+9+2 = **19**, not 20. The listed 19 lines already account for all 30 N-glyphs. Therefore, if the stated 20-line and 30-N totals are correct, the omitted twentieth line must have **zero** N-glyphs. The internally consistent histogram is thus:

- 0 N = **3** lines;
- 1 N = 6;
- 2 N = 9;
- 3 N = 2.

Reproducible audit: `analysis/n_glyph_recheck.py`.

Using Sektu's own Baudelaire comparison corpus (3182 Alexandrines, 6536 nasalized vowels), the exact results are:

- cipher mean = 1.5 N-glyphs/line;
- Baudelaire mean = 2.054 nasalized vowels/line;
- exact probability, under the empirical Baudelaire per-line distribution, that 20 lines contain <=30 nasalized vowels: **0.034436**;
- a collapsed 0/1/2/3/4+ multinomial shape test gives Pearson = **6.265476**, exact tail p = **0.172057**.

Interpretation: the coarse histogram shape is not strongly incompatible with Baudelaire, but the low total count is mildly surprising under the stated null. That makes `N = all French nasalization marks` weaker than the original "promising match" wording suggests. It does **not** rule out French, and it does not rule out N marking only a subset of nasal phenomena.

Source:
https://sektu.blogspot.com/2017/08/another-note-on-n-glyphs.html

## Current ranking of hypotheses

1. **Copied/source text encoded with a compositional/polygraphic script** — strengthened substantially by the Moore/copyist evidence.
2. **Direct English or French translation/paraphrase of Moore's Greek "An Ode by the Translator"** — still live and historically suggested; needs line-by-line source alignment.
3. **Moore Ode II as direct plaintext** — new high-value candidate because of exact 20-line/couplet structure and same-volume provenance; has immediate falsification tests above.
4. **Original French poem with N = universal nasalization mark** — weakened by the corrected N statistics, though still possible.
5. **Simple monoalphabetic substitution** — disfavored by the 425 whitespace-glyph inventory and visible compositional structure.

## Highest-value next action

Freeze a 20-line transcription of #4a/#4b at two levels:

1. whitespace-bounded glyph IDs;
2. decomposed subglyph sequence.

Before doing any broad search, test Ode II's held-out recurrence prediction on line endings 1–2 vs 17–18 and 3–4 vs 19–20. If it survives, run full line-length and n-gram alignment. If it fails, reject Ode II cleanly and move to the known English translations / likely French translation of Moore's Greek ode.
