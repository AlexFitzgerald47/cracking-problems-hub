# Progress Log – Kryptos

*Append new entries at the top. Never delete previous entries.*

---

## 2026-09-04 – Claude (Opus 5), remote session

### What was attempted

Two things: correcting the problem statement, which had been overtaken by
events, and then spending the two public cribs on the widest cipher hypotheses
they will reach.

K4 gives 24 characters of confirmed plaintext at known positions in a
97-character ciphertext. The question asked here was not "what is the message"
but "what do those 24 characters actually eliminate, and how much is each
elimination worth".

All figures reproducible from `attempts/2026-09-04-crib-constraints/`.

### Results / findings

**0. The problem has changed shape.** K4's plaintext was recovered from Sanborn's
Smithsonian papers in September 2025 and confirmed by him, but not deciphered and
not released; the files are sealed for fifty years. The open problem is now the
*method and key*, not the plaintext. `PROBLEM.md` has been corrected accordingly.
This matters practically: a claimed solution can no longer be certified by how
well its output reads, because an authenticated plaintext exists that the claimant
cannot check against.

**1. The ciphertext checks itself.** The cribs fix what K4 must read at those
positions, so `src/k4.py` verifies the transcription at load time: positions
64–74 must be `NYPVTTMZFPK` and 22–34 must be `FLRVQQPRNGKSS`. Both hold. Unlike
the Dorabella work earlier today, the source text here is not in doubt.

**2. Pure transposition is eliminated — no search required.** Under a pure
transposition the plaintext is an anagram of the ciphertext, so every plaintext
letter must be available in the ciphertext multiset. The cribs contain **three**
E's (`EASTNORTHEAST` has two, `BERLINCLOCK` one). The K4 ciphertext contains
**two**. K4 is therefore not a pure transposition of its plaintext. This is
believed in the literature; here it is a two-line proof from public data.

**3. The Vigenère family is eliminated at every period the cribs can see.**
Vigenère and variant Vigenère require the shift `C − P` to be constant within a
residue class; Beaufort requires the same of `C + P`. Tested for every period
1–97 against a null of random ciphertext letters at the crib positions
(K4's own letter distribution, 20,000 draws):

| family | periods where the test has power | K4 survives at | expected under null |
|---|---|---|---|
| Vigenère / variant | 49 | **none** | 0.12 |
| Beaufort | 49 | **none** | 0.12 |

The periods that do "survive" are 27–29 and 53–97, and they survive only because
at those periods almost no two crib characters share a residue class. For a
97-character message a key period of 53 or more is not a periodic cipher in any
useful sense.

**4. The cribs barely touch the general polyalphabetic family — worth knowing
before spending a month on it.** The general test (within a residue class the
plaintext→ciphertext map must be a partial bijection) covers Vigenère, Beaufort,
all four Quagmires and any keyed-alphabet scheme at once. It eliminates only
**19 of 97 periods**. Observed survivors 78, expected under the null 72.6. The
cribs carry almost no information about this family: the test has power at only
13 of the 97 periods.

**5. One lead, and it is not significant.** Period 19 — and its multiple 38 —
is the only period that survives a powered test. It rests on the nine crib
position pairs separated by 38, of which one is a genuine agreement: plaintext
**R** maps to ciphertext **P** at both position 27 and position 65, and the other
eight pairs produce no contradiction. The null survival rate at period 19 is
2.9%. But 13 powered periods were tested, giving 0.20 expected chance survivors
and P(at least one) ≈ 0.18. **That is not evidence.** It is recorded because it
is the single most specific target the public cribs offer, and because it would
become checkable the moment a third crib is released.

### Failures & dead ends

- The general polyalphabetic test is too weak at 24 crib characters to be worth
  much. This was the intended centrepiece; it produced a mostly negative result
  about its own usefulness. Recorded so nobody repeats it expecting more.
- Composite schemes — transposition followed by substitution, or Sanborn's
  hinted "masking" — are not testable by this method and remain wide open. The
  transposition elimination in finding 2 applies only to a *pure* transposition.
- Full articles on the 2025 recovery were not reachable (egress restrictions);
  the status correction rests on search-result summaries and should be verified
  against primary reporting.

### Artefacts produced

`attempts/2026-09-04-crib-constraints/` — data with a self-verifying loader,
four scripts, raw JSON results, and a README stating the method.

### References consulted

- `matthewdgreen/cipher_benchmark`, `benchmark/unsolved/sources/kryptos/`
  (GitHub, public; retrieved 2026-09-04) — ciphertext, cross-checked against the
  AZdecrypt and Zenith unsolved sets, and crib positions.
- Search-result summaries on the 2025 plaintext recovery: Scientific American;
  RR Auction; NYT reporting via secondary summary. **Full texts not read.**

---

## 2026-09-03 – Initial seed

Problem folder created. Awaiting first serious agent work on K4 and related elements.
