# Progress

## 2026-09-05 — GPT-5.6 Sol — starting session

### 1. Target sharpened from a generic archive mine to an explicit failed-decryption corpus

The strongest lead is the **Tadhg Kennedy Contemporary Documents collection, Group 2: “Cyphers and Codes — British (June 1920–September 1920)”**. The official BMH register says it contains RIC and military code/cypher telegrams and explicitly notes that attempts by the **Bureau of Military History and the National Library failed to decode the marked series**. Group 2 item 3 is particularly valuable because some messages have decoded versions, giving us calibration pairs.

This is much better than merely searching the Collins Papers for something mysterious: the archive itself records a historically unsuccessful cryptanalytic attempt.

### 2. Archive-reference discrepancy found

The current Military Archives appendix identifies the Tadhg Kennedy collection as **CD 286**. Kerry Library's 2020 source guide identifies apparently the same collection and matching Group 2 items as **CD 280**. Search/OCR derivatives can additionally misread the printed number. Until the archive clarifies the renumbering, retrieval requests should cite **Tadhg Kennedy, Group 2, “Cyphers and Codes — British”, and both CD 286/CD 280**.

### 3. Exact early RIC cipher reconstructed

Liam Archer, BMH WS 819, gives enough detail to implement the early RIC system exactly.

Procedure:

1. Deduplicate a keyword, normally 10–11 letters and no more than 13.
2. Write it as the start of a 13-character top row.
3. Append the earliest alphabet letters not already present until the row has 13 letters.
4. Put the remaining 13 alphabet letters below it.
5. Substitute each character with the character opposite it. The mapping is therefore self-inverse.

Archer's worked rows are resolved as:

```text
SWITZERLANDBC
FGHJKMOPQUVXY
```

(The PDF text extraction has one OCR variant `SWIIZER...`, but the stated no-repeat rule and alphabet partition resolve the intended row.)

`ric_cipher.py` implements this system. `test_ric_cipher.py` checks Archer's rows and the involution property.

Archer also records later evolution to:

- a two-key/double version of the paired-alphabet system; and
- a homophonic figure cipher using multiple two-digit values per letter (e.g. A with four alternatives, E with six, Z with two).

### 4. Cipher-family taxonomy: do not conflate “British code” into one system

Primary testimony now supports at least these distinct families:

| Traffic | System / evidence | Implication |
|---|---|---|
| RIC, early | Paired 13-letter keyword substitution (Archer WS 819) | Reconstructable now; suitable control system. |
| RIC, later | Two-key paired-alphabet system | Need worked examples / keys before implementation. |
| RIC / Auxiliary later traffic | Two-digit homophonic figure systems | Need full key tables or known pairs. |
| British military | **Playfair** explicitly identified by witnesses | Do not apply RIC keyword decoder to these messages. |
| Separate police/British system | “Two-word code”: daily word + weekly word + separate instructions (Eamon Broy) | Distinct mechanism; possession of code words alone was insufficient. |

James Hynes (WS 867) is especially useful: he says he could decode police cyphers but **never decoded military messages because he never got a key**; Harry Conroy intended to teach him the **Playfair system used by the military**, but they never reached that point. This makes surviving military Playfair traffic a particularly strong orphan-cipher seam.

### 5. Strong crib attack recovered for RIC traffic

BMH WS 1468 says RIC railway-warning messages were stereotyped. A common plaintext began:

`BY TRAIN TO YOU NOW ...`

The witness says the first three cipher characters were dead/nulls; aligning the next 15 characters to that phrase supplied enough substitution information to continue breaking the message. This gives us a historically attested crib attack to reproduce on suitable RIC traffic rather than relying on generic frequency analysis.

### 6. Real photographed Mullingar ciphertext located

A Westmeath Examiner article reproduces, courtesy of Military Archives, a damaged 1920 ciphertext sent to Collins by Mullingar Brigade acting commandant David Burke concerning RIC movements around Castlepollard/Granard. Collins-paper references are reported as `MA/CP/05/02/33-34` and `03/21`, with the main Mullingar correspondence also cited as `IE-MA-CP-05-02-33`.

The web reproduction is enough to establish that real raw ciphertext is digitally visible, but not enough to freeze every glyph safely: the paper is torn and several characters are ambiguous. I therefore **did not commit an OCR/transcription as ground truth**. Known-key trials on a rough visual transcription (`STAMBOUL`, `REPUBLIC`, `HONDURAS`, `PERSIAN GULF`, `CUMBERLAND`) did not yield obvious English, but this is not evidence against those keys because the transcription/date/system classification are not secure.

### 7. Parallel-traffic opportunity

Archer says that in November 1920 he removed copies of every police cipher message passing through the Central Telegraph Office for weeks, and that new monthly RIC keywords were sent in the old cipher. He also describes a February 1920 Inspector-General-to-Cork cipher message that he successfully deciphered. This suggests that large quantities of solved/solvable parallel RIC traffic once existed and may survive in Collins/BMH holdings.

Kerry testimony independently says Post Office workers intercepted Dublin Castle traffic and that Tadhg Kennedy supplied a key, confirming Kennedy was directly tied to the real codebreaking pipeline rather than merely collecting examples later.

### Current blocker

The decisive **Kennedy Group 2 message images themselves are not yet confirmed online**. Until those scans are obtained, the correct move is to reconstruct and validate the systems/cribs on known material, not pretend to solve unseen ciphertext.

### Next experiments

1. Obtain/freeze a high-quality transcription of a Collins RIC message with a known plaintext or key and validate `ric_cipher.py` end-to-end.
2. Locate the full figure-cipher table Archer says he possessed, or another surviving key sheet.
3. Obtain Kennedy Group 2 scans; cite donor + group title + both CD 286/CD 280 in the request/search.
4. Classify every Kennedy telegram by alphabetic/figure form, length and formatting before attempting decryption.
5. Use item 3 supplied decodes as blind controls, then attack only passages still lacking a supplied plaintext.
6. For military candidates, build a period-accurate Playfair attack using unit/date vocabulary and parallel traffic rather than RIC substitution assumptions.
