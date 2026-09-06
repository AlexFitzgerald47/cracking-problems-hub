# Cryptogram #1 completes the public scan corpus

**Session:** 2026-09-05, GPT-5.6 Sol
**Status:** primary-evidence advance; not a decryption

## New evidence
The user supplied the missing high-resolution self-portrait page. It matches Wikimedia Commons `Debosnys-Cryptogram-1.png` (original 1111×481), dated circa 1883 and attributed to Henry Debosnys. This means the working session has now directly inspected the complete six-scan public cryptogram set (#1, #2a, #2b, #3, #4a, #4b).

Primary source: https://commons.wikimedia.org/wiki/File:Debosnys-Cryptogram-1.png

## What #1 establishes
- Six cipher lines followed by an unencrypted signature `. H.D. Debosnys .`.
- The cipher is visually the same compositional family seen on the other pages: recurring base strokes (X, wave/tilde, circles, bars, curls) acquire dots, superscript/underscript marks and neighboring components rather than behaving like a small flat alphabet.
- Pictorial inserts occur inside the running text: horse/donkey-like animal in line 1, sun in line 2, bird-like figure in line 3, tree/plant in line 4. This strengthens the need to distinguish (a) true semantic logograms/determinatives from (b) decorative or homophonic cipher glyphs. The images are not merely page-margin decoration: they occupy positions in the cipher stream.
- The clear signature is important as a negative control: unlike the `H.D.D.L.M.F.` construction on #2a, there are no omission-count marks under the signature here. Therefore the under-marks in `H.D.D.L.M.F.` are unlikely to be a generic signature flourish; their interpretation as explicit length/omission metadata remains plausible.

## Transcription context recovered from prior work
A 2015 Cipherbrain commenter produced an early flat transcription of cryptogram #1, but explicitly needed a very large symbol alphabet. This independently foreshadowed Sektu's later result: across the Debosnys material a whole-glyph transcription gives 1,188 instances of 425 glyph types, whereas decomposing glyphs exposes recurring ordered subglyph structure. Sektu gives the signature-line example as six glyphs `C2B2 XP NU ZOO OM2N SHI`, decomposed as `<C2 B2> <X DOT> <N U> <O Z O> <O2RNO> <CROSSB>`.

Sources:
- https://scienceblogs.de/klausis-krypto-kolumne/2015/02/23/die-ungeloesten-codes-des-mutmasslichen-frauenmoerders-henry-debosnys-teil-1/
- https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html

## Consequences for current model ranking
1. **Ordered compositional/subglyph writing system** remains the best-supported mechanism class. #1 visibly reinforces it.
2. **Phonetic/syllabic system** remains live. Sektu independently proposed this from subglyph grammar and rhyme behavior.
3. **Masonic/fraternal influence** remains historically plausible but #1 does not by itself add a decisive Masonic key. Do not force ordinary pigpen values onto these symbols.
4. **Pictorial semantic layer** becomes more important to test because images occur inline across multiple pages. A mixed system (phonetic composites + logograms/determinatives) should be tested explicitly.
5. **Flat monoalphabetic substitution** is further disfavored by the enormous whole-glyph inventory and systematic internal modifiers.

## Important corpus-level observation
The public set now shows that inline pictures are recurrent and structurally placed, not isolated curiosities. Examples include sun/animal/bird/tree on #1; cube/pitcher/glass, sun, buildings, anchor and other pictures on #2; and other pictorial forms elsewhere. The next transcription should therefore encode every picture as a positional token rather than omit it as artwork. If pictures recur in similar local subglyph contexts, they may be readable semantic anchors.

## Highest-value next experiment
Build a complete **positional token map** for the six scans at two levels:
1. whitespace-bounded glyph/picture token;
2. ordered subglyph decomposition.

Then measure local contexts around recurring pictorial tokens (especially SUN, TREE/PLANT, ANCHOR, HOUSE/BUILDING, BIRD) and repeated abstract subglyphs. The strongest path to a crib is now likely a recurring picture whose surrounding compositional material behaves consistently across pages. Use the explicit plaintext metadata (`H.D. Debosnys`, `H.D.D.L.M.F.`, French poem) as controls, not assumed line-for-line plaintext.

## Current bottom line
The full public image corpus is now available. No honest decryption can yet be claimed, but the evidence increasingly points away from a conventional cipher alphabet and toward a mixed, ordered compositional notation in which subglyphs carry reusable information and some inline pictures may function as semantic units. The Masonic/Folger analogue remains a useful mechanism comparison, not an established key.
