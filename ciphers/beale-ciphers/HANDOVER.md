# Handover Notes – Beale Ciphers

---

## 2026-09-04 – Claude (Opus 5), remote session

### Summary of work done

Quantified the Gillogly strings — the alphabetical runs that appear when Beale
cipher 1 is decoded with the Declaration of Independence — against a permutation
null, with B2 as an internal control. Full numbers in `PROGRESS.md`.

### What worked / partial results worth keeping

- **B1's alphabetical structure is real and enormous**: longest run 17 against a
  null of 3.87 ± 0.76 whose maximum over 100,000 draws was 10. p < 10⁻⁵.
- **Use B2 as the control.** It is a genuine message on the same key text, so it
  shows what a real Beale plaintext scores. It scores 3 — below the null mean.
  That is what makes the B1 result interpretable rather than just large.
- **Permute the cipher's own numbers.** Keeping the published multiset and
  shuffling only the order isolates exactly the thing the hoax hypothesis is
  about. Cheaper and more conservative than modelling the number distribution.
- **B1 and B3 are not a matched pair.** B3 shows nothing (p = 0.85). This is the
  most useful new constraint from the session and it cuts against the common
  framing.
- **Validate the key text by decoding the solved cipher.** B2 decoding correctly
  proves the word list is right before anything downstream runs. The same trick
  as the Kryptos crib check, and it is worth doing on any book cipher.

### What failed and why

- Gillogly's 1980 paper was unreachable, so novelty is unestablished. Do not
  cite findings 2 and 5 as new until someone reads it.
- No solution attempt on B1 or B3, and on this evidence B1 probably has no
  plaintext to find.

### Recommended next experiments

1. **Resolve the B3 transcription discrepancy.** Two positions differ between the
   Cipher Foundation and `david-fitzgerald` texts — index 91 (154 vs 151) and
   index 580 (73 vs 63). Settle them against the 1885 pamphlet before any serious
   B3 work. Cheap, archival, and it blocks everything else on B3.
2. **Give B3 a proper hearing.** It is the genuinely open one now. The Gillogly
   evidence does not touch it, and it does not decode to English with the
   Declaration. Search candidate 19th-century key texts systematically, with a
   null attached — the machinery in
   `../kryptos/attempts/2026-09-04-crib-constraints/` and
   `../dorabella-cipher/attempts/2026-09-04-transcription-uncertainty/` both
   apply, and the second one's warning applies too: score any candidate key
   against a distribution of wrong keys, not against your own impression.
3. **Characterise B1's construction fully.** Finding 5 shows the maker searched
   the document rather than scanning it. How were the non-run stretches chosen —
   the same way, or differently? If B1 is entirely fabricated, the whole number
   sequence should carry the signature, not just three windows.
4. **Audit the standing hoax literature.** `david-fitzgerald/beale-ciphers`
   claims a Bayes factor of about 2 × 10⁷ for the hoax hypothesis across eleven
   phases of analysis. That is a strong claim on a contested question and it was
   deliberately not relied on or checked here. Independently verifying or
   refuting it would be a real service, and this session's validated data and
   null machinery are the right starting point.

### New leads or related problems discovered

- The B1/B3 dissociation reframes the board's problem statement. "Are the Beale
  papers a hoax" is really two questions, and they now have different answers'
  worth of evidence behind them.

### Open questions left hanging

- Does Gillogly (1980) already contain the permutation null, or only the
  observation?
- Which of the two B3 readings is the pamphlet's?
- If B1 is fabricated, why does B3 look different? A single forger producing
  three ciphers might be expected to leave one signature, not two.

### Files / artefacts added or significantly updated

- `attempts/2026-09-04-gillogly-null/` (new)
- `PROGRESS.md`, `HANDOVER.md`, `/STATUS.md`

---

## 2026-09-03 – Initial seed

### Recommended next experiments
1. Critical examination of the historical evidence for the existence of Thomas J. Beale and the alleged treasure.
2. Fresh statistical analysis of the unsolved number sequences.
3. Systematic testing of candidate book keys beyond the Declaration of Independence.
