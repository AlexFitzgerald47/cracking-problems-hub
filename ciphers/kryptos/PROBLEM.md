# Kryptos (Remaining Parts)

## Statement
Decrypt the remaining unsolved portion(s) of the Kryptos sculpture (particularly K4) created by Jim Sanborn and installed at CIA headquarters. Recover the plaintext and, if possible, the full cryptographic method used.

## Why it belongs on the board
One of the most famous modern unsolved cryptographic challenges. Three of the four passages have been solved; K4 (and possibly related elements) remain open despite decades of effort by skilled cryptanalysts.

## Known constraints / previous major attempts
- K1, K2, K3 solved (Vigenère variants and transposition).
- K4 is 97 characters and has resisted all public attempts.
- Sanborn has released limited clues over the years.
- The physical sculpture and its orientation contain additional information.

## Success criteria
A verified plaintext for K4 that is accepted by the cryptologic community and, ideally, confirmed by Sanborn or consistent with known clues.

## Key sources & starting points
- Photographs and transcriptions of the sculpture
- Published solutions for K1–K3
- Jim Sanborn’s public statements and released clues
- Cryptologia and other technical analyses


---

## Correction and restatement (appended 2026-09-04)

**The problem stated above is out of date, and in an important way.** It asks for
K4's plaintext. The plaintext has been recovered.

In September 2025 the journalists Jarett Kobek and Richard Byrne found K4's
plaintext in Jim Sanborn's papers at the Smithsonian — Sanborn had accidentally
included scraps of it while compiling documents years earlier. Sanborn confirmed
the material was authentic. The discoverers were explicit that they did not
solve the cipher: they recovered the plaintext from archival material and
obtained neither the key nor the method. They chose not to publish it, and at
Sanborn's request the Smithsonian sealed the files for fifty years.

So the open problem is now narrower and harder:

> **Recover the encryption method and key that map the 97-character K4
> ciphertext onto its plaintext** — and do it cryptanalytically, from public
> information.

Consequences for anyone working on this:

- **Success can no longer be self-certified by a plausible-looking plaintext.**
  An authenticated plaintext exists and is sealed. A claimed solution now stands
  or falls on whether it exhibits a method that is reproducible and independently
  checkable, not on how good its output reads.
- **Claimed public reconstructions of the plaintext are circulating.** Do not
  import any of them as ground truth. Nothing in this repository treats a claimed
  reconstruction as known plaintext; the 2026-09-04 attempt uses only the two
  cribs Sanborn released publicly.
- **The two public cribs remain the only confirmed plaintext available**:
  `EASTNORTHEAST` at positions 22–34 and `BERLINCLOCK` at 64–74 (1-based).

### Verified 2026-09-04 (post-dating this agent's training data, so checked by search)
- Scientific American, "A Solution to the CIA's Kryptos Code Is Found after 35 Years"
- RR Auction, "Kryptos K4: Discovered, Not Solved — Here's What Actually Happened"
- New York Times reporting of 16 October (via secondary summary) — the discoverers
  do not intend to release the plaintext
- Reported sale of Kryptos-related material at auction for $962,500

These were read as search-result summaries only; the full articles were not
reachable from this session. A future agent should verify the details against
the primary reporting before relying on them.
