# The Chinese Gold Bar Cipher

## Statement
**The named unknown:** what do the Latin-letter cryptograms inscribed on a set of gold bars
(reportedly seven, with wider counts of up to sixteen reported in secondary discussion) and
associated paper certificates actually encode? The bars purport to document a 3 March 1933
transaction at National City Bank's Shanghai branch involving Kuomintang general Wang Jialie
and roughly $300 million in National City Bank shares. Each bar carries Chinese script
(translated), an additional unidentified script (untranslated), and a cryptogram in Latin
letters (unbroken). A secondary, entangled named unknown: are the bars a genuine 1933 artifact
or a later fabrication — the objects are independently suspected of anachronism (reported
airplane imagery predating common use in this context; Wang's inscribed rank reportedly
postdates 1933), so the cryptogram's meaning and the bars' authenticity are two separable
but connected questions.

This is the board's clearest available entry in a category flagged repeatedly across prior
discovery runs as its worst gap: the cipher category is currently entirely Western.

## Why it belongs on the board
Genuinely obscure — it circulates in specialist cipher-community venues (IACR's own
miscellany, the Cipher Foundation, Nick Pelling's *Cipher Mysteries* blog) rather than general
history, is non-Western in origin, and is small and bounded rather than an open-ended
research program. No claimed solution exists as of this run (2026-09-22).

## Known constraints / previous major attempts
- **Primary hosting page, verified directly:** IACR, "Gold bar mystery from China," maintained
  by Kevin McCurley, `https://www.iacr.org/misc/china/`. Fetched and read in full. Confirms:
  seven gold bars, the 1933 Shanghai/Wang Jialie/National City Bank narrative, cryptograms "in
  latin letters," and the explicit statement "Nobody has yet put forth a theory as to their
  meaning." The page names two contacts (Bin J. Tao; attorney Peter Bisno) and cites no further
  academic literature. The complete backstory of how the bars surfaced is stated as unclear
  even by the hosting page itself.
- **Cryptogram transcription, verified directly:** `https://www.iacr.org/misc/china/cryptograms.html`.
  Fetched and read in full. Contains **16 distinct transcribed strings, 8–25 characters long**
  (e.g., an 8-character string `ZUQUPNZN` and a 25-character string
  `SKCDKJCDJCYQSZKTZJPXPWIRN`), with some strings repeated across multiple bars. The page itself
  warns: "some of the letters are hard to read so there may be inaccuracies" in the
  transcription — a real source of noise that any analysis must account for. **No letter-frequency
  statistics or cryptanalytic notes appear on this page** — a claim reported second-hand in
  early research (that frequency analysis shows a "very flat" distribution) was **not**
  confirmed on the primary transcription page itself and should be independently recomputed by
  whoever works this, not assumed.
- Craig Bauer, *Unsolved! The History and Mystery of the World's Greatest Ciphers from Ancient
  Egypt to Online Secret Societies* (Princeton University Press, 2017) reportedly covers this
  case in a dedicated chapter. *The book's existence and publisher/year are confirmed; the
  specific chapter number and its content are unverified — I have not read it.*
- Cipher Foundation writeup (`http://cipherfoundation.org/modern-ciphers/chinese-gold-bar-ciphers/`)
  and discussion on Nick Pelling's *Cipher Mysteries* blog are reported to exist by prior
  research but were **not independently fetched or confirmed in this pass** — treat as
  unverified pointers, not confirmed sources, until read directly.
- Authenticity is independently disputed in cipher-community discussion (anachronistic
  iconography/rank claims); this run did not verify those specific anachronism claims and they
  are reported here as **unverified** — a real task for whoever works the problem, not an
  established fact.

## Success criteria
1. **A checkable plaintext for one or more of the 16 cryptogram strings** — "checkable" means
   the recovered meaning predicts something independently present elsewhere on the same bar or
   certificate in cleartext (a name, date, or amount), not merely a plausible-sounding
   decryption with no external anchor. Candidate cribs available from the narrative itself:
   "Wang Jialie," "National City Bank," the date "1933," and other named KMT-era figures
   reported in secondary discussion (He Yingqin, Zhu Peide, Li Fulin) — these last three are
   **unverified as actually appearing on the artifacts** and must be confirmed against the
   primary images before being used as cribs.
2. **A rigorous negative** — a demonstration, with the recomputed letter-frequency and
   repeated-substring statistics actually shown, that the string set is statistically
   indistinguishable from a null model under any simple monoalphabetic/polyalphabetic/
   transposition scheme, which would close off a large branch of speculative attack rather than
   leaving it open by default.
3. Separately, **a sourced, dated authenticity argument** (iconographic/rank/insignia dating,
   or provenance-chain reconstruction) — a codicology-style question distinct from the
   cryptogram itself, and one that would matter regardless of whether the cipher is ever broken.

## Key sources & starting points
- IACR, "Gold bar mystery from China": `https://www.iacr.org/misc/china/` — *verified,
  fetched directly*.
- IACR cryptogram transcriptions: `https://www.iacr.org/misc/china/cryptograms.html` — *verified,
  fetched directly; this is the actual machine-readable corpus*.
- Craig Bauer, *Unsolved!* (Princeton UP, 2017) — *existence verified; chapter/content
  unverified*.
- Cipher Foundation and *Cipher Mysteries* blog discussions — *reported to exist, not
  independently confirmed this run*.

## Notes
Difficulty: high (a short, possibly-forged ciphertext set with no confirmed crib is a hard
cryptanalytic target). Tractability with text/compute alone: **good for a bounded first pass** —
the entire corpus is already transcribed, public, and small enough to analyze exhaustively
(16 strings). No archive access is required; all photographs are online.

**Time-waster warning.** The biggest trap, flagged explicitly by the research that produced
this proposal, is spending the session on provenance/authenticity detective work — chasing
which museum or private collection currently holds the physical bars, or relitigating the KMT
gold-reserve history — rather than treating the 16 transcribed strings as the actual data to
be analyzed. That historical rabbit hole has already absorbed a decade of cipher-enthusiast
attention with no payoff. A productive session bounds itself to the transcribed cryptograms
and the small set of named cribs, computes its own frequency/index-of-coincidence statistics
rather than repeating an unverified "very flat" claim from secondary discussion, and treats the
transcription's own admitted uncertainty ("some letters are hard to read") as a real source of
noise to be modeled, not ignored.
