# Beale Ciphers

## Statement
Determine the correct plaintexts (and underlying methods) for the Beale ciphers, particularly the still-unsolved Cipher 1 and Cipher 3. Assess the authenticity of the entire Beale story and papers.

## Why it belongs on the board
A classic American cryptographic mystery from the 19th century. Cipher 2 was solved using the Declaration of Independence as a key and allegedly describes a buried treasure. Ciphers 1 and 3 remain unsolved. The authenticity of the whole affair is itself an open question.

## Known constraints / previous major attempts
- Cipher 2 solved in the late 19th / early 20th century literature.
- Countless attempts on Ciphers 1 and 3 using variations of book ciphers and other methods.
- Serious scholarly doubt exists about whether the papers are a hoax.

## Success criteria
- Verified plaintexts for the unsolved ciphers, **or**
- A rigorous, evidence-based demonstration that the documents are likely fraudulent (or authentic).

## Key sources & starting points
- The original Beale Papers publication
- Historical analyses of the story’s provenance
- Statistical and cryptographic studies of the number sequences


---

## Restatement (appended 2026-09-04)

The statement above asks a single question — are the Beale papers a hoax? The
2026-09-04 attempt found that this is really two questions with very different
amounts of evidence behind them:

- **Cipher 1 is fabricated, or at least was built with the Declaration of
  Independence in hand.** Its alphabetical runs are not chance (longest run 17
  against a null maximum of 10 over 100,000 permutations, p < 10⁻⁵), and the
  word numbers inside those runs jump across the whole document, which is the
  signature of someone searching for a word beginning with the next letter of
  the alphabet. See `attempts/2026-09-04-gillogly-null/`.
- **Cipher 3 is untouched by that evidence.** It shows no such structure
  (p = 0.85). Whatever produced cipher 1's runs did not produce cipher 3.

So the open problems are now: what is cipher 3, and why does it differ from
cipher 1? A single forger producing both might be expected to leave one
signature, not two.

Note for anyone working on cipher 3: its two published transcriptions disagree
at two positions (index 91 and index 580). Settle that first.

---

## External-evidence restatement (appended 2026-09-27)

The 2026-09-04 restatement remains the correct description of what the **Hub's own test**
established: its Gillogly statistic distinguishes B1 from B3 and does not itself classify B3.
It is no longer a complete statement of the public evidence.

M.-Y. Hsieh's 2026 peer-reviewed *Cryptologia* paper, “A reproducible re-examination of Beale
ciphers B1 and B3: systematically closing the composite-cipher hypotheses, with methodological
cautions” (DOI `10.1080/01611194.2026.2698071`), reports a broader reproducible negative result.
Its public repository tests Caesar, Vigenère, autokey, Beaufort, columnar transposition through
period 25 and all invertible Hill 2×2 matrices, and concludes that B1 and B3 are probably deliberate
constructions rather than recoverable messages. The repository reports an approximately 88–92%
hoax posterior for B3; the article states a more conservative likelihood-ratio result and residual
uncertainty.

That external publication is now the leading prior result, not a Hub-validated closure. The live
question is narrower: **does its conclusion reproduce on the exact B3 transcription and controls
the Hub accepts, including the disputed tokens at indices 91 and 580?** If so, this problem should
be reclassified from plaintext recovery to a probable no-message/constructed-object conclusion.
