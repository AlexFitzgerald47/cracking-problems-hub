# Attempt: how improbable are the Gillogly strings?

**Date:** 2026-09-04 · **Status:** complete; one strong positive result and one dissociation · **Reproducible:** yes

Decoding Beale cipher 1 with the Declaration of Independence produces stretches
that walk the alphabet — most famously `abcdefghiijklmmno`. Gillogly noticed
this in 1980, and it is the single most-cited piece of evidence that the Beale
papers are a hoax. It is also almost always presented qualitatively: the string
is displayed, and the reader is invited to find it striking.

This attempt puts a number on it, and checks whether the same thing is true of
Beale 3.

## Headline

- **B1's alphabetical runs are not chance.** Longest alphabetical run 17, against
  a null of 3.87 ± 0.76 whose maximum over 100,000 draws was 10. p < 10⁻⁵.
- **B2, a genuine message on the same key, behaves exactly like the null** (run
  of 3, p = 0.99993). The perfect internal control: whatever a real Beale-style
  plaintext looks like, B2 is it.
- **B3 shows nothing** (run of 4, p = 0.85). The Gillogly phenomenon is specific
  to B1. Hoax arguments that lump B1 and B3 together are not supported by it.
- **The construction signature is visible.** Inside the runs the Declaration
  word numbers jump all over the document (+289, −241, +125, −283 …). Whoever
  made B1 was *searching* the whole text for a word beginning with the next
  letter of the alphabet, not scanning forward through it.

## Method

The statistics were fixed before any null was run:

- **R1** — longest run whose consecutive steps are all in {0, +1} (alphabetical,
  repeats allowed; this is the shape the strings actually have)
- **R2** — longest run whose consecutive steps are all exactly +1

The null is a **permutation of each cipher's own numbers**. It keeps the
published multiset exactly and asks only whether the *order* is special — which
is precisely the hoax question, since a forger picking words alphabetically
leaves a signature in the ordering, not in which numbers get used. 100,000 draws
per cipher per statistic.

## Data validation

Nothing was taken on trust. Two checks run at load time in `src/beale_data.py`:

1. B1 and B3 are compared against a second, independently provenanced
   transcription (Cipher Foundation, via `matthewdgreen/cipher_benchmark`).
   **B1 agrees token for token.** B3 differs at two of 618 positions (index 91:
   154 vs 151; index 580: 73 vs 63) — recorded, not silently reconciled.
2. The key text is validated by decoding B2, whose plaintext has been accepted
   since 1885. The first 113 characters come out exactly
   (`ihavedepositedinthecountyofbedford…`). If the word list were wrong, B2
   would not decode, and `load()` raises rather than proceeding.

```
data/                  B1/B2/B3, the Beale-variant Declaration word list, both transcriptions
src/beale_data.py      loader; refuses to return unvalidated data
src/gillogly.py        the two statistics, the permutation null, the runs
results/               raw JSON
```

## Reproduction

```
pip install numpy
cd src
python gillogly.py     # ~4 min
```

## Provenance and credit

The Beale-variant Declaration word list (1,311 words, with the pamphlet's
documented departures from the standard text) and the three cipher texts were
taken from `david-fitzgerald/beale-ciphers` (MIT licence), then validated
independently as above. That repository advances its own, broader statistical
case for a hoax; **none of its analysis or conclusions are relied on here**, and
its claims have not been checked by this attempt. The analysis in this folder
was written from scratch.
