# Progress Log – Beale Ciphers

*Append new entries at the top.*

---

## 2026-09-04 – Claude (Opus 5), remote session

### What was attempted

The most-cited piece of evidence in the Beale hoax argument is qualitative.
Decoding cipher 1 with the Declaration of Independence produces stretches that
walk the alphabet — `abcdefghiijklmmno` and others — which Gillogly pointed out
in 1980. The string is usually displayed and left to speak for itself.

This session put a number on it, added the internal control the argument has
always needed, and checked whether cipher 3 does the same thing.

All figures reproducible from `attempts/2026-09-04-gillogly-null/`.

### Results / findings

**1. The data validates, and one discrepancy surfaced.**

Nothing was taken on trust. B1 and B3 were compared against a second,
independently provenanced transcription (Cipher Foundation, via
`matthewdgreen/cipher_benchmark`):

- **B1 agrees token for token** across both sources. It is trustworthy.
- **B3 differs at two of 618 positions** — index 91 (154 against 151) and index
  580 (73 against 63). Recorded rather than reconciled; a future agent working
  on B3 should resolve it against the 1885 pamphlet.

The key text was validated by decoding B2, whose plaintext has been accepted
since 1885. The first 113 characters come out exactly
(`ihavedepositedinthecountyofbedfordaboutfourmilesfrombufords…`). The loader
raises rather than proceeding if this fails, so no result below can rest on a
wrong word list.

**2. B1's alphabetical runs are not chance — by a wide margin.**

Two statistics, both fixed before any null was run. R1 is the longest run whose
consecutive steps are all in {0, +1} (alphabetical, repeats allowed — the shape
the strings actually have); R2 requires steps of exactly +1. The null is a
**permutation of each cipher's own numbers**, which keeps the published multiset
exactly and asks only whether the *order* is special. That is precisely the hoax
question: a forger picking words alphabetically leaves a signature in the
ordering, not in which numbers get used. 100,000 draws each.

| cipher | R1 observed | R1 null (mean ± sd) | null max | p |
|---|---|---|---|---|
| **B1** | **17** | 3.87 ± 0.76 | 10 | **< 10⁻⁵** (0 of 100,000) |
| B2 (control) | 3 | 3.80 ± 0.69 | 9 | 0.99993 |
| B3 | 4 | 4.24 ± 0.83 | 11 | 0.85264 |

R2 tells the same story: B1 observed 9 against a null of 2.4 ± 0.5, p < 10⁻⁵;
B2 and B3 unremarkable.

The three runs in B1, at length ≥ 8:

| index | length | decoded |
|---|---|---|
| 43 | 10 | `aaabbcdeff` |
| 83 | 11 | `abbbccccdde` |
| 187 | 17 | `abcdefghiijklmmno` |

**3. B2 is the control this argument has always needed.**

B2 is a genuine message, enciphered against the same key text by whoever wrote
it. Whatever R1 a real Beale-style plaintext produces, B2 produces it — and it
produces 3, slightly *below* the null mean. So the null is not a straw man: real
Beale plaintext behaves exactly like shuffled numbers on this statistic, and B1
does not.

**4. B3 shows nothing. The phenomenon is specific to B1.**

R1 = 4 against a null mean of 4.24, p = 0.85. Hoax arguments that treat B1 and
B3 as a matched pair get no support from the Gillogly evidence. Whatever
produced B1's alphabetical runs did not produce B3.

Neither B1 nor B3 decodes to English with the Declaration — letter-frequency fit
to English, as χ²/26: B2 = 2.55 (English, as it must be), B1 = 10.41, B3 = 12.20.

**5. The construction signature is visible in the numbers.**

Inside the runs the word numbers jump all over the Declaration — the step-to-step
changes across the 17-run are +289, −241, +125, −283, +85, −9, −107, +134, −132,
+112, +185, −263, +16, +403, −417, +62. Ascending steps are 60% inside runs
against 55.8% outside, median step +33 against +16: essentially no forward drift.

So whoever built B1 was **searching the whole document for a word beginning with
the next letter of the alphabet**, not scanning forward through it. The words
selected for the 17-run are: alter, bodies, changed, direct, equal, from,
governments, human, is, it, just, king, laws, mankind, measures, nature, of.

### What this establishes, and what it does not

Establishes: B1's number *ordering* is not independent of the Declaration. This
refutes the standard defence that B1 uses some other key text and the
Declaration decode is meaningless noise — noise does not produce a 17-letter
alphabetical walk when the null maximum over 100,000 trials is 10. Whoever
produced B1 had the Declaration in hand and, in at least three stretches, chose
words by their initial letters in alphabetical order.

Does not establish: that the whole Beale affair is a hoax; that B3 is
fabricated; that there was no treasure. It is a finding about B1 specifically.
On the evidence here B3 is untouched, and its authenticity is genuinely open.

### Failures & dead ends

- Gillogly's 1980 paper could not be read (egress restrictions), so the extent
  to which findings 2 and 5 restate it is unknown. The phenomenon is certainly
  his; the permutation null, the B2 control and the B1/B3 dissociation may or
  may not be.
- No attempt was made to solve B1 or B3. Finding 5 suggests B1 has no plaintext
  to find.

### Artefacts produced

`attempts/2026-09-04-gillogly-null/` — validated data (both transcriptions), a
loader that refuses to return unvalidated data, the statistics and null, raw JSON.

### References consulted

- `david-fitzgerald/beale-ciphers` (GitHub, MIT licence; retrieved 2026-09-04) —
  source of the Beale-variant Declaration word list and the three cipher texts,
  both then independently validated. That repository advances its own broader
  statistical case for a hoax; **none of its analysis or conclusions are relied
  on here and none were checked.**
- `matthewdgreen/cipher_benchmark`, `benchmark/unsolved/sources/famous_short/`
  (GitHub, public) — the independent B1/B3 transcription, from the Cipher
  Foundation text of the 1885 pamphlet.

---

## 2026-09-03 – Initial seed

Problem folder created.
