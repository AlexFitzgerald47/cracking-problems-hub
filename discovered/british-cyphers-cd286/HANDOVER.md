# Handover

**Updated:** 2026-09-05  
**State:** first cryptanalytic groundwork complete.

## What changed this session

The generic “mine Collins Papers for orphan ciphertexts” idea has been replaced by a much sharper target: **Tadhg Kennedy's BMH Contemporary Documents Group 2**, where the archive itself records failed BMH/NLI decryption attempts on British RIC/military telegrams.

A working implementation of the documented early RIC paired-alphabet keyword cipher is now in `ric_cipher.py`, with tests in `test_ric_cipher.py`. The message-family ledger is in `solution-status.md`.

## Highest-value next move

**Get the Kennedy Group 2 scans.** Search/order under all of:

- Tadhg Kennedy
- Group 2 — “Cyphers and Codes — British”
- CD 286 (current Military Archives appendix)
- CD 280 (Kerry Library / older reference)

Specifically request all of Group 2 items 1–3, including explanatory donor letters, the purported 31 May 1921 RIC key, and every supplied decoded version. Do not ask only for “the unsolved telegrams”; the solved/control material is essential.

## Once images arrive

1. Freeze exact ciphertext/transcriptions independently from any supplied plaintext.
2. Classify each message: early RIC alphabetic, later paired/double RIC, figure code, military Playfair, two-word system, or unknown.
3. Hold out the supplied decodes in Group 2 item 3.
4. Recover those plaintexts blindly from their ciphertexts/keys. Do not touch the historically failed series until this control passes.
5. Then attack the undecoded messages and record every assumption.

## Other immediate useful work without CD scans

- Acquire the highest-quality Collins scan of the Mullingar 1920 ciphertext and its surrounding pages; the newspaper reproduction is too damaged for a frozen transcription.
- Search Collins/BMH holdings for full figure-cipher tables. Archer explicitly says he possessed one supplied by Collins.
- Search for worked British military Playfair examples from Ireland in the same date range and identify likely key-distribution practices.
- Follow the cross-link from Collins agent `100` to the later IRA `VORFYDCGT` memo; do not assume identity, but the wording “100's methods” makes it worth auditing.

## Do not repeat

Do not run known keywords against a hand-guessed transcription of the damaged Mullingar newspaper image and interpret failure as evidence. That experiment was tried only as a sanity probe and is underdetermined because the source transcription and cipher family are not fixed.
