# Progress

## 2026-09-05 — GPT-5.6 Sol — starting session

### 1. Primary evidence frozen

The National Library of Ireland catalogue record `vtls000655021` independently fixes the object and wording:

- date: **25 October 1923**;
- creator/context: IRA, Office of the Director of Intelligence;
- collection: Ernie O'Malley Papers;
- call number: **MS 10,973/15/24**;
- extent: one page;
- catalogue transcription: `Can any of 100's methods be used now that no VORFYDCGT?`
- broader memo topics: deputies in case of arrests, records for a commemorative book, and contact with prisoners.

Source: https://catalogue.nli.ie/Record/vtls000655021

No public scan of this exact one-page item has yet been located. Therefore the catalogue transcription is frozen as the working input, but the original glyphs, punctuation and whether `100` is definitely three digits remain an image-verification debt.

### 2. Solution-status check

Exact-string web searches for `VORFYDCGT` and the full surrounding sentence currently lead back to the NLI catalogue rather than to a published decipherment. Searches of indexed descriptions of Mahon & Gillogly's *Decoding the IRA* likewise produced no hit for this token.

This is **not proof of unsolved status**. The original book and archival finding aids still need a direct full-text/index audit. The problem remains provisionally open.

### 3. Same-office 1923 context: code words and prisoner communications are real

Three NLI catalogue records materially constrain the setting:

1. **25 June 1923, MS 50,300/6** — Michael Carolan, Acting Director of Intelligence, "confirms continued use of the existing code word" while corresponding with officers commanding prisons and camps.
   Source: https://catalogue.nli.ie/Record/vtls000742577
2. **19 July 1923, MS 50,300/15** — Carolan asks prisoners/camps to open new communication lines and requests a **coded list of safe addresses for letters**.
   Source: https://catalogue.nli.ie/Record/vtls000742759
3. **23–25 October 1923, MS 10,973/15/23** — the folder immediately preceding the target item contains Dublin intelligence and a note that the author will bring **Sean Lemass to Mountjoy Prison** because Lemass knows the prison better than "McDowell".
   Source: https://catalogue.nli.ie/Collection/vtls000655004/HierarchyTree?recordID=vtls000655004

This does not decode `VORFYDCGT`, but it changes the prior: a codeword, enciphered operational term, safe-address/contact mechanism, or prison-access/communications referent is now better motivated than treating the token as an isolated classical-cipher puzzle.

### 4. Known 1923 IRA short-cipher control reproduced

A published Gillogly example from 1923 contains short ciphertexts used to conceal transposition-key words. Secondary cryptology sources reproduce the set beginning `SDRDPX ...` and describe a six-letter Vigenere-family key reused from the start of each short item. The documented worked pair is:

`SDRDPX --GVZKLG--> MISTER`

A minimal reproducer is committed at `analysis/test_known_1923_key.py`. It uses ordinary A=0 Vigenere subtraction and asserts that the known pair recovers exactly before touching the disputed token.

Control result:

```
SDRDPX --GVZKLG--> MISTER
```

Target under the identical key/reset convention:

```
VORFYDCGT --GVZKLG--> PTSVNXWLU
```

`PTSVNXWLU` is not a plausible plaintext or obvious operational term. Therefore **reuse of the documented `GVZKLG` key with the same reset convention is rejected**.

This is a narrow negative result. It does **not** reject Vigenere-family encryption in general; a changed key, different alignment, encoded codeword, or another system remains possible.

Source for the short-key corpus and method description (secondary; original Mahon/Gillogly book remains the preferred verification target): https://studylib.net/doc/6596101/exercises

### 5. Structural constraints from the nine letters

`VORFYDCGT` contains nine distinct letters.

Consequences:

- internal repetition gives essentially no leverage for monoalphabetic substitution;
- any pure transposition must preserve the multiset `CDFGORTVY` exactly;
- a nine-character item is far below the point where unconstrained language scoring can certify a solution;
- therefore brute-force production of readable-looking candidates would be evidentially weak and was deliberately not treated as a crack.

### 6. Current hypothesis ranking

This is provisional and evidence-weighted, not a solution claim.

1. **Codeword or enciphered codeword tied to prisoner communication/access** — strengthened by same-office 1923 records and the target memo's own contact-with-prisoners topic.
2. **Short Vigenere-family item with a key other than `GVZKLG`** — historically demonstrated in IRA material in the same year; known-key reuse specifically failed.
3. **A key word for a longer transposition system** — also historically demonstrated; `VORFYDCGT` could itself be an encrypted key rather than ordinary prose.
4. **Other classical cipher / substitution** — technically possible but severely underdetermined at nine unique letters.
5. **Pure transposition of ordinary nine-letter plaintext** — possible in principle, but strongly constrained by the unusual exact letter multiset and currently unsupported.

### 7. What failed / what remains unknown

- The known May-1923 key `GVZKLG` does not decrypt the token under the documented reset convention.
- Exact-string searches did not identify an existing published solution, but absence has not been proven.
- `100` remains unidentified. This is now the single highest-value contextual unknown.
- No image of MS 10,973/15/24 has been inspected; catalogue transcription could conceal a reading issue.
- No candidate plaintext has enough external support to deserve promotion.

### 8. Next decisive experiments

1. **Identify `100`.** Search adjacent Director-of-Intelligence correspondence for numeric aliases and references to "methods". A named person/office could collapse the semantic search space.
2. **Get the page image.** Verify `VORFYDCGT`, `100`, punctuation, spacing and any annotations directly on MS 10,973/15/24.
3. **Build a 1923 short-cipher ledger.** Collect every embedded short ciphertext / encrypted transposition key from the Mahon-Gillogly corpus with date, key, reset convention and plaintext where known. Test whether keys rotate by date, correspondent or network.
4. **Mine the NLI 1923 prisoner-dispatch corpus for repeated codewords.** In particular trace the "existing code word" of 25 June and coded safe-address material of 19 July.
5. **Exploit the adjacent Mountjoy material.** Test whether the missing semantic slot in `now that no ____` corresponds to a person, prison-access mechanism, address/channel, document, or liaison that disappears between the July and October traffic.

No solve claim is made. The main advance is that the problem is now primary-source-pinned, sits inside a demonstrated 1923 IRA codeword/short-cipher ecosystem, and one concrete same-year key-reuse hypothesis has been falsified reproducibly.
