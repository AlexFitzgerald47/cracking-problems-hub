# Frozen predictions — 2026-09-25 session

Written and committed **before** the corresponding tests were run. Everything
above the line was already settled by deterministic computation and is not a
prediction; everything below it is.

## Already settled before this file was written (not predictions)

- **Exact multinomial tail, IACR corpus.** `src/exact_tail.py` and the
  independent `src/exact_tail_dp_check.py` both return
  **P(chi2 <= 1.250951) = 1.7020973493e-12** for n = 263, k = 26, in exact
  integer arithmetic. Validators 1 and 2 are right; the claim's 9.3e-13 is
  1.83x optimistic and the refuter's 8.28e-13 is 2.06x optimistic. Panel repair
  item 1 is closed.
- **Re-transcription from the photographs** (panel repair item 2). Reported in
  `RESULTS.md` under "What the photographs say". Done by eye at up to 8x on the
  full-size IACR JPEGs before any statistic was recomputed on the result.

## Predictions frozen here, tests not yet run

**P1 — the balance survives the transcription correction.** The corrected
deduplicated inventory is 261 letters (two letters shorter than IACR's 263,
because both disputed strings are 13 glyphs and not 14). Its chi2 against
uniform is 1.4904 on 25 df. I predict the exact lower tail
P(chi2 <= 1.4904 | uniform multinomial, n = 261, k = 26) is **below 1e-10**,
i.e. the headline finding is robust to the correction and only its magnitude
moves.

**P2 — a bar face is not, in general, balanced.** Six photographed faces carry
Latin lines. Taking each face's complete physical text (every stamped line,
repeats included) I predict the per-face lower-tail P values are **not**
systematically small: median across the six faces **> 0.01**, and **at most one
of six below 1e-3**. This is a direct test of the refuter's finding that face
5.1's complete text is itself balanced at P = 4.0e-6; if faces are generally
balanced, the composition-level argument is in trouble and mine fails here.

**P3 — the depleting-supply alternative cannot fit, and the reason is I = 13.**
Validator 2's "compositor's case at ten sorts per letter, or a tile bag, drawn
once" is a *uniform urn drawn without replacement*. I predict that for every
uniform urn size c = 10..26 tiles per letter,
P(chi2 <= observed AND max letter count >= 13 | hypergeometric draw of n from
26c) is **below 0.01**, so the model is rejected across its whole parameter
range: a bag flat enough to give this chi2 is too small to contain 13 of any
letter, and a bag with 13 of a letter is too big to be this flat.

**P4 — the within-string reuse lead does not survive the correction.** The only
discriminating signal the panel found was validator 2's max-distinct-letters-
per-string, observed 15 against a deal null of 17.89, p = 0.010. I predict that
on the corrected corpus this test gives **p > 0.01** (it weakens), because one
of the two corrections removes a repeated letter from a string.

**P5 — the repertoire is closed.** No photographed face carries a Latin string
outside the 16. Stated as a prediction about the faces I had not yet examined
line by line when this was written; it is confirmed in RESULTS and is therefore
reported as weak evidence only.
