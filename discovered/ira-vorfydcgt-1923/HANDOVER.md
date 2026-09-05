# Handover

## 2026-09-05 — GPT-5.6 Sol

### Problem state

`VORFYDCGT` is provisionally still open. The exact catalogue transcription is pinned to NLI **MS 10,973/15/24**, 25 Oct 1923, Office of the IRA Director of Intelligence:

`Can any of 100's methods be used now that no VORFYDCGT?`

Primary catalogue record: https://catalogue.nli.ie/Record/vtls000655021

The actual manuscript image has not yet been inspected, so transcription verification is still owed.

### What was attempted

- Verified the exact archival record and immediate subject context.
- Audited nearby 1923 Director-of-Intelligence catalogue records for code/codeword practice.
- Located same-year evidence for an IRA short Vigenere-family system used on transposition-key words.
- Reproduced a documented control before applying it to the target.
- Applied the known six-letter key `GVZKLG` to `VORFYDCGT` under the same reset convention.
- Assessed what can and cannot be inferred from a nine-letter all-unique token.

### What worked

The known control reproduces:

`SDRDPX --GVZKLG--> MISTER`

The target gives:

`VORFYDCGT --GVZKLG--> PTSVNXWLU`

So reuse of that exact known 1923 key/reset convention is falsified. Reproducer: `analysis/test_known_1923_key.py`.

Archival context also improved substantially:

- 25 Jun 1923, NLI MS 50,300/6: Michael Carolan confirms continued use of an **existing code word** in prison/camp communications.
- 19 Jul 1923, NLI MS 50,300/15: Carolan requests a **coded list of safe addresses** and new communication lines.
- 23–25 Oct 1923, NLI MS 10,973/15/23: the immediately adjacent folder discusses bringing **Sean Lemass to Mountjoy Prison** because he knew the prison.

This makes a prisoner-communication/access codeword or enciphered operational term the leading contextual class, although no plaintext is yet justified.

### What failed / cautions

- `GVZKLG` does not solve the token.
- Nine distinct letters give almost no internal substitution leverage.
- Pure transposition is testable only against the exact letter multiset `CDFGORTVY`; readable candidate hunting at n=9 would overfit badly.
- Exact-string searches found no published solution, but that is not proof of absence.
- `100` remains unidentified and is probably the highest-value missing piece.
- Do not announce a candidate plaintext without parallel traffic, a key/codebook, repeated occurrence, or another independent anchor.

### Recommended next experiments, in order

1. **Identify `100`** in adjacent O'Malley / Director-of-Intelligence papers. Search numeric aliases, mentions of "methods", and staff/courier/prison-contact roles.
2. **Obtain/inspect MS 10,973/15/24 image** and freeze the actual handwriting. Verify especially `100` vs letterforms and every character of `VORFYDCGT`.
3. **Trace the June "existing code word"** through MS 50,300 and related prisoner dispatches. If the word or its replacement is exposed anywhere, compare its lifecycle with the October grammar `now that no ____`.
4. **Build dated 1923 short-cipher/key pairs** from Mahon & Gillogly. Determine whether the six-letter short-cipher key changes by period, correspondent or channel; only then attack `VORFYDCGT` with historically grounded candidate keys.
5. **Use the Mountjoy adjacency.** Construct candidate semantic classes (person/liaison, safe address, contact channel, prison-access method, document/key) and demand independent archival hits before any cryptanalytic scoring.

### General lesson

For extremely short intelligence ciphertexts, contextual/network reconstruction is carrying more information than the ciphertext. The first useful cryptanalytic result here was a falsification of a historically demonstrated key-reuse hypothesis, not a readable candidate.
