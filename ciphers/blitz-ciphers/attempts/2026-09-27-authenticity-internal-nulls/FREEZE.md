# FREEZE — Blitz Ciphers authenticity battery, 2026-09-27

Written **before** any of the three tests below was computed. What I had already seen when
writing this: (a) the two transcriptions as text, (b) the unigram frequency table of each page,
(c) page/token/type counts for the comparanda. Nothing else. Tests 1–3 below had not been run.

Because I had already seen the unigram tables, **Test 1 is exploratory-confirmatory, not
prospective**, and is labelled as such throughout. Test 2 and Test 3 are prospective in the sense
that no statistic bearing on them had been computed on any corpus when this was written; the
pipeline-validation predictions (2a, 3a) are the real prospective content, because they are
predictions about known-genuine corpora whose answers I do not know.

## Evidence

- **Primary.** Nick Pelling's transcriptions of Blitz Cipher pages 7 and 8,
  https://ciphermysteries.com/2014/10/24/blitz-cipher-partial-transcription (fetched 2026-09-27).
  p7 = 470 tokens / 53 types over 24 lines; p8 = 159 tokens / 41 types over 11 lines.
  One ASCII character per glyph. p7 is transcribed from the released image rotated 180°.
- **Provenance audit (done).** `matthewdgreen/cipher_benchmark`
  `benchmark/unsolved/sources/blitz/transcriptions/*` is **byte-identical** to the Cipher
  Mysteries text for both pages, and its canonical and diplomatic files are byte-identical to
  each other. The benchmark is a faithful copy, not an independent reading. There is therefore
  **exactly one transcription of these pages in existence**, and everything below inherits its
  glyph decisions.
- **Comparanda (genuine, solved, verified).** Copiale cipher, 101 pages, 74,860 tokens, 136
  symbols, homophonic substitution + nomenclator, German plaintext. Borg cipher, 397 pages,
  120,191 tokens, 77 symbols, monoalphabetic substitution, Latin plaintext. Both from
  `cipher_benchmark`, canonical (global symbol-map) transcriptions. Audited: no empty pages;
  global symbol maps confirmed (only page 1 of each document introduces S001..S008 in order).

## Test 1 — do pages 7 and 8 share a symbol distribution? (EXPLORATORY)

Statistic: two-sample chi-square homogeneity over the pooled symbol set, converted to a z-score
against a **pooled-permutation null** (pool the tokens, re-split at the observed sizes).
Length-matched reference distributions built from the comparanda at exactly (470, 159) tokens:

- **between-page**: 470 contiguous tokens from page *i*, 159 contiguous from page *i+1*;
- **within-page/locality**: 470 and 159 non-overlapping contiguous tokens from the same document
  stream within a 629-token window.

Reported as: where z_blitz falls in the genuine **between-page** z distribution.

## Test 2 — is there bigram structure under the unigram distribution? (PROSPECTIVE)

Statistic: bigram index of coincidence — the probability two randomly drawn adjacent-symbol pairs
from the text are identical — against a **within-line unigram shuffle** null (shuffle tokens
inside each line, preserving line lengths and the page's unigram distribution, destroying
adjacency). Report z and empirical p over 20,000 shuffles.

- **Prediction 2a (pipeline validation, prospective).** Copiale and Borg, at full page length,
  give z >> 0 — substitution ciphertext of a natural language retains bigram repetition. If this
  fails, the pipeline is broken and nothing else in this session may be believed.
- **Prediction 2b (power, prospective).** Subsampling Copiale and Borg to 470 tokens, I predict
  **more than half** of 470-token subsamples still reach p < 0.05. If fewer than half do, the
  test is underpowered at Blitz length and any Blitz null result is *untestable, not refuted* —
  and I will report it that way.
- **Prediction 2c (the actual question).** If the Blitz pages are enciphered natural language by
  any substitution-family method, Blitz z > 0 with p < 0.05 on the 629 pooled tokens. If Blitz
  lands at z ≈ 0 **and** 2b shows the test is powered, that is positive evidence against the
  pages being substitution ciphertext of a natural language.

## Test 3 — adjacent-repeat (doublet) rate (PROSPECTIVE)

Hand-fabricated "random-looking" sequences characteristically **under-produce immediate
repetitions**. Statistic: count of adjacent identical symbols within lines, against the same
within-line unigram shuffle null.

- **Prediction 3a (calibration, prospective).** Borg (monoalphabetic Latin) shows a doublet
  **excess** (z > 0), because Latin has doubled letters and monoalphabetic substitution preserves
  them exactly. Copiale (homophonic) shows a smaller excess or none, because homophones break
  doubles. This is a prediction about corpora whose answer I do not know and it tests whether the
  statistic measures what I claim.
- **Prediction 3b.** A hand-fabricated page shows a doublet **deficit**. If Blitz z is strongly
  negative, that is evidence for fabrication; if it sits at or above 0, this particular
  fabrication signature is absent.

## What none of this can establish

A p-value against a shuffle null is P(data | that null), never P(data | cipher) or
P(data | hoax). Test 2 failing does not prove fabrication: it excludes substitution-family
encipherment of a natural language *at the tested power*, and a nomenclator, a heavy-null
scheme, a polyalphabetic cipher or a non-natural-language plaintext could all survive it. Two
pages cannot establish anything about the unreleased corpus. Every glyph decision is Pelling's
and has never been independently replicated.

Starting revision: `accc499`. Role: cracker. Trial ID: none.
