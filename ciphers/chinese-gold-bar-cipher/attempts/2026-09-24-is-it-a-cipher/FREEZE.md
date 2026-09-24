# FREEZE — predictions registered before the confirming tests were run

Session 2026-09-24. Written and committed **before** any of the tests in
`src/confirm.py` were executed. Everything derived up to this point used only
the *aggregate letter counts* of the 16 distinct strings — no use of string
order, of the per-bar layout, or of the repetition structure.

## What is already established (derivation set)

Over the 16 distinct cryptograms (263 letters) from
`https://www.iacr.org/misc/china/cryptograms.html`:

- 21 of 26 letters occur **exactly 10 times**. The others: O=9, T=9, E=11,
  S=11, I=13.
- chi-square against uniform = **1.251** on 25 df, where the *expected* value
  under a genuinely uniform random process is 25.
  Analytic P(chi2_25 <= 1.251) = **9.3e-13**.
- Pooled within-string IC = 0.0397, versus 0.0606 for a monoalphabetic
  substitution of English at these lengths (p = 0.0001) and 0.0739 for
  Wade-Giles-shaped romanized Chinese (p = 0.0001).
- Zero repeated trigrams anywhere in the corpus; English MASC predicts ~29.

The letters are therefore not merely "flat" (the unverified secondary claim)
but **flatter than chance** — too even to be the output of any process that
samples letters, including a one-time pad.

## Competing hypotheses

- **H1 "real cipher"** — some substitution / polyalphabetic / transposition /
  code system applied to a real message.
- **H2 "designed balanced inventory"** — the 16 strings were constructed by
  dealing from a pool holding ~10 copies of each letter, i.e. manufactured
  to look like ciphertext.
- **H3 "punch-set exhaustion"** — a physical explanation: the engraver's
  letter-punch set held ~10 of each letter and the balance is an artifact of
  the tooling, not of the content.
- **H1b "flat-by-design cipher"** — the steelman for H1: a homophonic system
  deliberately equalising its 26 output letters. This one is NOT excluded by
  the balance statistic and must be attacked on order structure instead.

## Frozen predictions

**P-A (discriminates H3).** The balance is a property of the *deduplicated
inventory* of 16 strings. Physically, the bars carry far more text than that,
because whole strings are stamped repeatedly. If H3 were true the balance
should appear in the **instance** corpus (every stamped line across the three
bars shown on the page, repeats counted), since that is what a punch set
constrains. Prediction: the instance corpus will be **significantly
non-uniform, chi2 well above 25**, and H3 dies.

**P-B (discriminates H2 from coincidence).** The balance is a whole-inventory
property, not a local one. No per-bar distinct subset of the strings will be
as balanced as the full 16.

**P-C (attacks H1b).** If the strings are a random deal from the balanced
pool, then every *order-sensitive* statistic should be unremarkable against a
null that shuffles the exact observed letter multiset across the exact
observed length structure. Specifically: maximum per-letter multiplicity
inside a string, per-string IC, adjacent doubles, and periodic (Vigenere-style)
IC at every period 2..8 will all sit inside the central 95% of that null.
A failure here — some string clumpier or more periodic than the deal allows —
would be the first positive evidence of encipherment and would reopen H1.

**P-D (the seduction control).** `YQHUDTABGALLOWLS` contains the string
GALLOW. Prediction: a random deal from the balanced pool produces English
substrings of length >= 6 at a rate that makes this unremarkable, so it is
not evidence of plaintext leakage.

**P-E (transcription robustness).** If the true inscription is exactly
balanced and the deviations (I+3, O-1, T-1, E+1, S+1) are the transcription
errors the source page itself warns about, then corrupting an exactly-balanced
corpus at a plausible error rate should reproduce a chi2 near the observed
1.251; whereas no achievable rate of transcription error can drive a genuine
cipher's chi2 (~25 or far higher) down to 1.251. Prediction: the observed
value is reachable from a balanced original and unreachable from a cipher one.
