# Progress Log – Kryptos

*Append new entries at the top. Never delete previous entries.*

---

## 2026-09-04 (continued) – composites, and what a third crib is worth

### What was attempted

The two items this session's own handover put first: test composite
transposition-plus-polyalphabetic schemes, and quantify what an additional crib
would buy.

### Results / findings

**6. Composite transposition + periodic polyalphabetic: no signal above chance.**

The polyalphabetic stage preserves position, so for `ct = T(m)` with
`m = periodic_poly(pt)`, undoing a candidate T gives an intermediate text that
aligns positionally with the plaintext — and the same crib tests apply at the
same positions. Two useful consequences: the search is one permutation per
candidate, and the null rates are unchanged (T is a permutation, so it preserves
the letter multiset), so no new Monte Carlo is needed.

133 transpositions (identity; columnar widths 2–48; rail fence 2–20 rails; each
in both directions) × 97 periods = **12,901 hypotheses**:

| family | tests with power | survived | expected by chance |
|---|---|---|---|
| general polyalphabetic | 1,729 | 35 | 26.9 |
| Vigenère / variant | 6,517 | 13 | 15.8 |
| Beaufort | 6,517 | 13 | 15.8 |

Vigenère and Beaufort come in **at or below chance**. The general family shows a
mild excess (35 against 26.9, z ≈ 1.6, p ≈ 0.06) that does not survive scrutiny.

**This also demotes finding 5.** The period-19 lead was the only powered survivor
when only the identity transposition was considered. Against 133 transpositions
it is one of 35 survivors where 27 were expected. It is not a lead any more.

**7. Where the cribs' power actually comes from — an exact rule.**

The Monte Carlo power measurements turn out to have a clean structural
explanation. A period *p* is testable **if and only if two crib positions
differing by a multiple of *p* carry the same plaintext letter.** Verified
across periods 1–26 with no overlap whatever:

| | same-plaintext pairs in a class | measured null survival |
|---|---|---|
| periods 1, 2, 3, 4, 5, 9, 15, 17, 19 | ≥ 1 | 0.000 – 0.035 |
| every other period | 0 | 0.167 – 0.956 |

The reason is simple once seen: a violation needs either a collision (one
plaintext letter going to two ciphertext letters — near-certain under the null
wherever a same-letter pair exists) or a merge (two plaintext letters landing on
one ciphertext letter — only about 1 in 26). So same-letter pairs supply
essentially all the power, and everything else is noise.

This replaces a simulation with a combinatorial count, which is what makes the
next finding possible.

**8. What a third crib would buy — and where to ask for it.**

Current cribs give 13 powered periods, only 9 of them at or below 30. A
hypothetical additional crib, letters drawn i.i.d. from English frequencies
(mildly conservative — real English repeats letters slightly more at short range),
averaged over placements:

| extra crib length | powered periods | of which ≤ 30 |
|---|---|---|
| — (current) | 13 | 9 |
| 5 | 22.6 | 16.1 |
| 10 | 28.1 | 19.8 |
| 15 | 32.2 | 22.3 |
| 20 | 35.3 | 24.1 |
| 30 | 40.0 | 26.8 |

**A ten-character third crib would roughly double the number of testable
periods.** Placement matters and is not intuitive — for a 12-character crib,
mean powered periods ≤ 30:

| placement (1-based start) | value |
|---|---|
| **47** (the untouched gap between the two cribs) | 24.5 |
| **1–2** (the opening) | 24.4 |
| **86** (the tail) | 24.3 |
| 21–24 (abutting `EASTNORTHEAST`) | 13.8–14.4 |

A crib adjacent to an existing one is worth barely more than nothing, because it
creates few new position *differences*. If anyone is in a position to ask
Sanborn's estate for one more crib, **ask for the middle** — around position 44–47.

### Failures & dead ends

- The composite search covers only simple, unkeyed transpositions. Keyed columnar
  transpositions (which is what K3 actually used) have a factorial column-order
  space and were not searched. That is the obvious gap.
- The mild excess in the general family (35 vs 26.9) is not significant and
  should not be chased without more crib data.

### Artefacts produced

- `src/composite.py`, `src/crib_value.py`
- `results/composite_results.json`, `results/crib_value.json`

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
