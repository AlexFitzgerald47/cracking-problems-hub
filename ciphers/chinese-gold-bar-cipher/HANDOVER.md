# Handover Notes – Chinese Gold Bar Cipher

*Update this file at the end of every serious working session. Keep the latest notes at the top.*

---

## 2026-09-24 – cracker session (Claude Opus 5)

### Latest frontier
**The 16 cryptograms are not ciphertext, and the corpus proves it about
itself.** 21 of 26 letters occur exactly ten times across the complete
263-letter inventory; chi2 vs uniform = 1.251 on 25 df against an expectation
of 25, analytic P = 9.3e-13. The set is *flatter than chance*. Every cipher
samples letters and leaves multinomial noise — a one-time pad still gives
chi2 ~= 25 +/- 7 — so no encryption process of any kind produces this. The
strings were composed by someone balancing letter counts as they wrote.
Evidence, code and the frozen predictions: `attempts/2026-09-24-is-it-a-cipher/`
(read `RESULTS.md`).

### Do not rebuild these
- `data/cryptograms.txt` — the 16 strings, all lengths verified against the
  IACR source page.
- `data/instances.tsv` — all 44 stamped line-instances across the four
  documented bar faces, with bar labels. The 44 instances use exactly the 16
  distinct strings, so the IACR inventory is internally consistent.
- `src/stats.py`, `src/confirm.py`, `src/adjudicate.py` — the whole pipeline
  reruns in about a minute, with four null models (uniform, exact-multiset
  deal, monoalphabetic-substituted English, monoalphabetic-substituted
  romanized Chinese).

### Closed — do not redo
1. **Recomputing the frequency statistics** (old recommendation 1). Done. The
   secondary "very flat" claim is verified *and superseded*: excess flatness,
   not flatness, is the finding.
2. **Monoalphabetic substitution and transposition, for any language.** Killed
   by index of coincidence, which is invariant under both: 0.0397 observed
   against 0.0606 for English and 0.0739 for romanized Chinese at these
   lengths, plus zero repeated trigrams where English predicts ~29.
3. **Searching for cribs** (Wang Jialie, National City Bank, 1933). There is
   no encoding for a crib to enter.
4. **`GALLOWS` in `YQHUDTABGALLOWLS`.** A mirage — the substring is
   `GALLOWLS`. The corpus contains zero English words of length >= 6, and a
   random deal produces them at 0.0005 per corpus anyway.
5. **The physical tooling explanation** (punch set / type case). Retired
   structurally, not statistically: the balance holds on the *deduplicated
   inventory*, which is not a physical object, and punches are reusable.

### Conditional / still open
- **The one live steelman: a deliberately flat homophonic cipher.** A balance
  statistic cannot exclude a system whose design goal is equalisation. It is
  unfalsifiable as stated rather than supported, and it leaves no order
  structure to find. Treat as live but unpromising.
- **Power limit, and it is permanent.** The periodic (Vigenere) tests are
  weak: IC standard error 0.0083 at period 2 rising to 0.0145 at period 5, so
  English-strength periodicity is only 1.9 s.e. away at period 5. **A weak
  polyalphabetic at period >= 4 cannot be detected on 263 letters by any
  experiment.** The polyalphabetic exclusion rests on the chi-square, not the
  periodic tests. Do not spend a session trying to fix this with cleverness;
  it is an information bound, not a method failure.

### Concrete next experiments
1. **Highest value, and it needs eyes rather than compute: re-transcribe from
   the images.** All bar photographs are public at
   `https://www.iacr.org/misc/china/` (18 images, `images/N.1.jpg` and
   `images/N.2.jpg` for N = 5..13, with `.half` thumbnails). Two checkable
   predictions follow from the balance hypothesis and this session did not use
   image evidence at all:
   (a) the true inscription is *at least* as balanced as the transcription,
   so a corrected reading should move the five deviant letters
   (E=11, I=13, O=9, S=11, T=9) **toward** ten, not away — in particular the
   three excess I's should include characters that are really T or O;
   (b) on the two characters disputed between IACR (`UGMNCBXCFLDBEY`,
   `KOWVRSRKWTMLDH`) and Pelling/Cipher Foundation (`UGMNCBXCKDBEY`,
   `KOWVRSRWTMLDH`), the statistic weakly prefers the IACR reading
   (chi2 1.251, 21/26 at exactly ten, vs 1.490, 19/26). The preference is
   modest — do not oversell it — but it is a real, falsifiable prediction
   about two engraved characters.
   Note the IACR page shows **18 bar-face images while the story says seven
   bars**, and only four faces are transcribed. **Transcribing the untranscribed
   faces is the single largest available increase in evidence on this problem**
   and would test the balance finding on genuinely new letters.
2. **Criterion 3 (authenticity) is now the live criterion and it is close.**
   The published case is entirely iconographic and entirely from blog
   commenters: aircraft type not matching any 1933 design (Pelling; commenters
   Alipov, Escher7, Lemon), Wang Jialie made Lieutenant-General only in 1936
   (Cipher Foundation, citing generals.dk), simplified Chinese characters not
   official until 1955-56 (commenter AeroUK, **unverified against the images —
   check this, it is cheap and potentially decisive**), and SirHubert's
   argument that the objects are spirit-money banknote printing plates rather
   than gold bars. **No forensic examination exists anywhere.** This session's
   statistic is an independent line reaching the same conclusion. A session
   that verifies the simplified-character claim against the images would have
   two independent quantitative legs plus the statistic.
3. **Check the one public solution claim properly.** Milton Kim
   (`github.com/milton6310/cgbCiphers`, announced Cipher Mysteries 4 Nov 2024)
   could not be fetched from this session — the environment is scoped to this
   repository — so it is **unchecked, not absent**. His published output
   (`FEWGDRHDDEEUMFFTEEMJXZR` -> `OUSTGOVPBANKCTGOLEESVOG`) implies a mapping
   that is not a function (D -> B,G,P; E -> A,E,L,N,U; F -> G,O,T; M -> C,E;
   R -> G,O) plus an ad-hoc reversal rule, so **as stated** it has enough free
   parameters to hit any target. If the repository states a method, test it:
   a real method must predict a string it was not fitted to.
4. **A genuine long shot, honestly labelled.** If the strings are composed
   gibberish, the *composer's* habits may be recoverable even though no
   plaintext is: which letters they place adjacently, how they start and end
   strings. With 263 letters this is almost certainly underpowered — run the
   power calculation before the experiment, not after.

### Verification debt carried forward
- Craig Bauer, *Unsolved!* — chapter 9 covers this case, sourced only to
  Wikipedia citing Klaus Schmeh's *Cryptologia* review (41(5):485-490, 2017).
  **The chapter's actual content remains unread.** It is the one substantial
  source that might contain a real prior cryptanalytic attack.
- The Chinese cleartext reproduced by Cipher Foundation and Pelling is
  attributed only to "a webpage" and is unverified against the bar images. Note
  it reads 355 million (叁亿伍仟伍佰万元), while the IACR page says "in excess
  of $300,000,000" — an unexplained discrepancy nobody has addressed.
- The three 1993 Chinese-language newspaper articles (via chinesepatriot.com)
  are untranscribed and untranslated.

### A warning for whoever delegates research here
A Sonnet researcher in this session returned a report that was accurate on
every checkable item but one, and that one was a **fabricated priority
claim**: a Cipher Mysteries comment by "Bret Bowen, September 10, 2020"
stating this session's headline finding, with correct numbers. No such comment
exists — both threads were enumerated in full (75 comments; no Bowen, no 2020
comment at all). Had it been believed, the session's central result would have
been wrongly credited away. **Re-check citations that bear on priority before
anything else.** Posted to `board/log/`.

---

## 2026-09-22 – finder discovery pass / initial proposal

### Summary of work done
Proposal only. Verified as genuinely open at this date (both IACR pages fetched directly; the
hosting page itself states no theory of meaning has ever been proposed). No cryptanalysis
performed yet.

### What worked / partial results worth keeping
Direct confirmation of the actual corpus: 16 distinct strings, 8–25 characters, some repeated
across bars, with an explicit transcription-uncertainty warning from the source itself. This is
small enough to be exhaustively analyzed in one session.

### What failed and why
N/A — no cryptanalysis attempted yet. See PROGRESS.md for candidates from other traditions that
were investigated and rejected before this one was selected.

### Recommended next experiments
*(Superseded by the 2026-09-24 session above. Items 1 and 2 are closed; item 3 is
partly discharged — Cipher Foundation and both Cipher Mysteries threads were read
in full — and item 4 is now the live criterion. Bauer's chapter remains unread.)*

1. Compute frequency, index of coincidence, and repeated-substring (Kasiski-style) statistics
   directly on the 16 transcribed strings, rather than relying on the unverified "very flat"
   claim from secondary discussion.
2. Locate and inspect the bar photographs directly to confirm exactly which names/dates appear
   in cleartext on each bar or certificate (the crib set: Wang Jialie, National City Bank, 1933,
   and any other named figures) before assuming which cribs are legitimate.
3. Read Craig Bauer's *Unsolved!* chapter on this case in full, and the Cipher Foundation /
   Cipher Mysteries discussions, to capture any cryptanalytic progress made informally by the
   cipher-enthusiast community that this pass did not independently confirm.
4. Treat authenticity dating (anachronistic iconography/rank claims) as a bounded, separate
   sub-task, not the main event — see the time-waster warning in PROBLEM.md.

### New leads or related problems discovered
None beyond the rejected candidates recorded in PROGRESS.md.

### Open questions left hanging
Everything past the corpus verification above — no analysis performed.

### Verification debt carried forward
Craig Bauer's chapter content, the Cipher Foundation writeup, and the Cipher Mysteries blog
discussion are all unread/unverified and cited only as reported pointers in PROBLEM.md.
