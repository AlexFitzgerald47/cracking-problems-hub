# Primary-scan test of the Moore Ode II candidate — 2026-09-05

## Status

**Not a solve.** The previously blocked held-out test is now executable from full-resolution Commons scans supplied during the session.

Primary images checked:

- `Debosnys-Cryptogram-4a.png` — 1107 × 1493 px
  - https://upload.wikimedia.org/wikipedia/commons/f/fd/Debosnys-Cryptogram-4a.png
- `Debosnys-Cryptogram-4b.png` — 1105 × 563 px
  - https://upload.wikimedia.org/wikipedia/commons/4/4f/Debosnys-Cryptogram-4b.png

The poem has 20 lines: 15 on 4a and the final 5 on 4b.

## Test that was specified before seeing 4b

The preceding source-sieve selected Thomas Moore's *Odes of Anacreon*, Ode II because it is exactly 20 lines in ten rhyming couplets and because Moore is independently implicated by the Greek text on the reverse and by Debosnys' plagiarism habits.

Crucially, Ode II repeats its opening four lines at the end:

- lines 1–2: `song / along`
- lines 3–4: `string / sing`
- lines 17–18: `song / along`
- lines 19–20: `string / sing`

Before the lower scan was available, the session recorded the following held-out prediction: if the terminal cipher glyphs encode rhyme material, the terminal class at cipher lines 1–2 should recur at 17–18, and the class at 3–4 should recur at 19–20.

## Primary-image result

The images make the comparison unambiguous at the whole-glyph level.

### Prediction 1 — HIT

- cipher lines 1–2 end in the same distinctive horizontal double-wave / curled glyph;
- cipher lines 17–18 end in that same distinctive glyph.

Therefore the non-adjacent recurrence demanded by Ode II's `song / along` couplet is present.

This recurrence was not used to select Ode II; it is genuinely held-out evidence.

### Prediction 2 — MISS

- cipher lines 3–4 end in a simple dotted-X glyph;
- cipher lines 19–20 end in a different ornate curled/looped glyph.

Therefore the second recurrence demanded by Ode II's `string / sing` couplet is absent at the whole-glyph level.

## Stronger exact-stanza check

Moore's lines 17–20 are not merely similar to lines 1–4; they repeat them exactly:

`Give me the harp of epic song / Which Homer's finger thrilled along / But tear away the sanguine string / For war is not the theme I sing.`

The cipher lines 17–20 are visibly not whole-glyph repetitions of cipher lines 1–4. Thus a deterministic one-symbol/one-group substitution of Ode II is ruled out.

That does **not** strictly rule out a homophonic or compositional encoding, because the same plaintext material could in principle be written with different glyph variants. But the asymmetry matters: the first repeated rhyme class reuses exactly the same terminal glyph while the second repeated rhyme class does not. A direct line-preserving Ode-II plaintext is therefore **weakened, not confirmed**.

## Interpretation

The result is more interesting than either a clean hit or a clean miss:

1. The first held-out recurrence succeeds exactly where Ode II predicts it.
2. The second held-out recurrence fails.
3. The full repeated stanza does not reproduce glyph-for-glyph.

The safest current reading is:

- **Exact deterministic Ode II plaintext:** rejected.
- **Homophonic/compositional direct Ode II plaintext:** still possible but now requires a mechanism that explains why one repeated rhyme class is stable and the other is not.
- **Adapted / partially copied Moore Ode II:** remains plausible and is arguably more consistent with Debosnys' known habit of modifying copied material.
- **Chance structural resemblance:** still live; the first recurrence is a real positive but cannot carry the claim alone.

## Next decisive experiments

1. Freeze a two-level transcription of only eight lines first: 1–4 and 17–20.
   - whitespace-bounded glyph IDs;
   - ordered subglyph decomposition.
2. Compare the four exact Moore line-pairs `1↔17`, `2↔18`, `3↔19`, `4↔20` for repeated subglyph n-grams, positional correspondences and length ratios.
3. Calibrate those similarities against unrelated line pairs from the same cipher poem. If the repeated-Moore pairs do not exceed the internal null, reject direct Ode II even under a compositional/homophonic model.
4. Independently sieve Moore/Anacreon source poems for the observed stronger rhyme pattern: a 20-line couplet poem in which the ninth couplet repeats the first rhyme class but the tenth does **not** repeat the second. This may identify a better source than Ode II.
5. Do not force a decryption from the single successful rhyme recurrence. The candidate has earned further testing, not a solve claim.

## External anchors

- Thomas Moore, Ode II text: https://www.gutenberg.org/cache/epub/8187/pg8187-images.html
- Sektu, first phonetic/rhyme hypothesis: https://sektu.blogspot.com/2017/06/first-hypothesis-for-debosnys-cipher.html
- Sektu, transcription revision / compositional glyph model: https://sektu.blogspot.com/2017/08/debosnys-cipher-transcription-revision.html
- Cipher Mysteries 2021 summary of Moore connection: https://ciphermysteries.com/2021/04/30/sektu-and-henry-debosnys
