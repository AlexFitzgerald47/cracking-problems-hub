# Handover Notes – Dorabella Cipher

*Latest notes at the top.*

---

## 2026-09-04 – Claude (Opus 5), remote session

### Summary of work done

Measured what a monoalphabetic Dorabella solution would have to prove, rather
than attempting one. Built a reproducible toolkit
(`attempts/2026-09-04-transcription-uncertainty/`), collected seven published
readings, and ran the null-model, power and uniqueness experiments that the
existing literature on this cipher mostly omits. Full numbers in `PROGRESS.md`
and `attempts/.../results/summary_tables.md`.

### What worked / partial results worth keeping

- **Compare readings by partition, not by letter names.** Under a monoalphabetic
  key the letter names are arbitrary, so the equality relation over position
  pairs is the right object. This immediately showed that two of the seven
  readings are the same reading, and that only three are genuinely distinct.
  Reusable for any symbol-substitution cipher on the board.
- **The transcription is the binding constraint**, not the cryptanalysis.
  36 of 87 positions are unstable across the three distinct readings. Everything
  downstream inherits that. This is the single most useful thing established here.
- **Build the null before believing the fit.** At n = 87 the English null for IC,
  distinct-symbol count, doubles and repeats is so wide that none of them
  discriminates. Several confident claims in the popular literature about
  Dorabella's "un-English" statistics do not survive contact with a null.
- **Match the search budget.** Hill-climb scores rise with restarts; comparisons
  across different budgets are worthless. This caught an error in this session's
  own first run — see `PROGRESS.md`.
- **Count the competitors.** Thirteen mutually unrelated messages score at or
  above the best published monoalphabetic claim. Counting competing optima is a
  far better test of a claimed solution than looking at its score.

### What failed and why

- No primary-source transcription could be obtained. Egress in this session
  reached GitHub and PyPI only. The readings used come from a secondary,
  partisan compilation whose fidelity to the original publications is unverified.
- The relevant academic literature (HistoCrypt 2021; ACL SMP 2021; Sams 1970)
  could not be read for the same reason. Findings 2 and 3 may duplicate published
  work. **Do not cite them as novel until this is checked.**
- The arc-count / orientation coding per symbol was not obtainable, so the
  structural hypothesis went untested.
- No decipherment. None was attempted, and on this evidence none of the
  monoalphabetic class can be validated from 87 characters by fit alone.

### Recommended next experiments

1. **Get a primary transcription.** Obtain the standard consensus transcription
   in orientation-letter + arc-count form (A–H, 1–3) from the HistoCrypt paper or
   from a facsimile of the original note, and commit it to `data/`. Re-run every
   script against it. This is an archival task, and it dominates everything else
   in value. If a facsimile image is reachable, transcribe it independently and
   add that as an eighth reading.
2. **Test the two-channel hypothesis.** With the arc/orientation coding in hand,
   test whether arc count and orientation are statistically independent
   (χ² on the 8 × 3 table), and whether either channel alone carries
   English-like structure. If Elgar used one channel for something systematic —
   vowels, or a musical mapping — this is where it shows.
3. **Widen the language model.** Everything here assumed English. Elgar wrote in
   a private idiom, and the claimed solutions lean on that. Repeat the
   budget-matched comparison with (a) an Elgar-letters-derived model if a corpus
   of his correspondence can be reached, (b) Latin, (c) an abbreviated /
   vowel-dropped English. Do it as a like-for-like comparison of nulls, not by
   eyeballing outputs.
4. **Extend the class beyond monoalphabetic.** The entire analysis here bears
   only on simple substitution. Homophonic (some symbols sharing a plaintext
   letter) is the obvious next class and would explain the mildly depressed IC.
   Note that adding homophones raises the key entropy, which pushes the
   validation bound further out of reach — quantify that before searching.
5. **Solve the calibration problem properly.** See
   `discovered/short-cipher-validation-bound/`. `src/power.py` measures the key
   quantity at one point; sweeping n and k would give the whole board a shared
   standard of proof.

### New leads or related problems discovered

- `discovered/short-cipher-validation-bound/` — proposed this session. Below what
  ciphertext length does a readable high-scoring decryption stop being evidence?
  Dorabella (87), Kryptos K4 (97) and the Phaistos Disc all depend on the answer.
- The machinery in `attempts/2026-09-04-transcription-uncertainty/src/` is
  cipher-agnostic and should be lifted to a shared location when a second problem
  needs it.

### Open questions left hanging

- Are the seven readings faithful to their attributed sources? Unverified.
- Does the HistoCrypt 2021 paper already establish findings 2 and 3?
- Is the mildly depressed IC (0.0585 against 0.0637) real signal for homophony,
  or the noise it looks like at this sample size? Only a longer text or a second
  ciphertext in the same system could settle it — and no second Elgar ciphertext
  in this alphabet is known to this agent. Whether one exists is worth checking.

### Files / artefacts added or significantly updated

- `attempts/2026-09-04-transcription-uncertainty/` (new): data, seven scripts, results
- `PROGRESS.md`: full session entry
- `PROBLEM.md`: appended structural notes, the transcription warning, and sources
- `/STATUS.md`: Dorabella row updated; new proposal listed
- `/discovered/short-cipher-validation-bound/` (new)

---

## 2026-09-03 – Initial seed

### Recommended next experiments
1. Exhaustive analysis of the symbol set and possible monoalphabetic or simple polyalphabetic mappings.
2. Incorporation of known Elgar linguistic habits and the personal correspondence context.
3. Critical review of all major published proposed solutions for internal consistency.
