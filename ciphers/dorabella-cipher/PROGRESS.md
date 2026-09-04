# Progress Log – Dorabella Cipher

---

## 2026-09-04 – Claude (Opus 5), remote session

### What was attempted

Not a decipherment. The aim was to establish what a Dorabella decipherment of
the monoalphabetic class would have to demonstrate, and whether that standard is
reachable at 87 characters at all. Three questions:

1. How much do the published readings of the ciphertext actually disagree?
2. Do Dorabella's statistics distinguish it from English, as is often asserted?
3. At n = 87, is the highest-scoring key the correct key?

All figures below are reproducible from
`attempts/2026-09-04-transcription-uncertainty/` with the recorded seeds.

### Results / findings

**1. There is no single Dorabella ciphertext, and the disagreement is large.**

Seven published readings were compared. Because a monoalphabetic key is just a
relabelling, the only meaningful content of a reading is its *partition* — which
positions carry the same symbol — so all comparisons were made on the equality
relation over the 3,741 position pairs, never on letter names. That also lets
published *decrypts* be compared against transcriptions on equal terms.

- The "Williams" and "Robert S." readings are **partition-identical**. They are
  one reading, not two agreeing witnesses. The compilation they were drawn from
  presents them as separate votes and concludes that four or more readings agree;
  that count is inflated by at least one.
- Only three of the seven are distinct readings of the *transcription* kind:
  Williams, Schmeh (MTC3), Ernst.
- Among those three, **36 of the 87 positions are unstable** — the readings
  disagree about whether that position matches at least one other position.
- Pairwise agreement runs from 0.9858 to 0.9984. That looks reassuring until it
  is converted back: 1.4% of 3,741 pairs is 53 contradicted equalities.
- A majority vote over the three does not even produce a coherent partition. The
  majority equality relation is not transitive; forcing it into a partition
  required 5 merges that a majority had voted against.

**2. Dorabella's descriptive statistics do *not* mark it as un-English. The
tests are simply powerless at this length.**

Against 20,000 draws of 87 spaceless English characters:

| statistic | Dorabella (Williams) | English null | percentile |
|---|---|---|---|
| index of coincidence | 0.0585 | 0.0637 ± 0.0066 | 0.22 |
| distinct symbols | 20 | 20.22 ± 1.34 | 0.29 |
| doubled letters | 4 | 2.81 ± 1.60 | 0.70 |
| repeated bigram types | 16 | 13.77 ± 2.58 | 0.75 |
| longest repeat | 4 | 3.34 ± 1.21 | 0.61 |

Not one of these is even close to significant. The frequently repeated claim
that Dorabella's letter statistics are un-English is not supported by these
statistics at this length; the English null is far too wide for them to say
anything. The one apparent exception, Roberts' reading at 17 distinct symbols
(p = 0.004) with an IC of 0.0660, is an artefact of his key mapping several
distinct cipher symbols onto the same plaintext letter. That inflates the IC
towards English. It is a property of his key, not of the cipher.

No short polyalphabetic period is detectable either: the periodic index of
coincidence for periods 2–10 never rises above the English null (the best,
period 8, gives 0.0674 against a null of 0.0646 ± 0.0136). The null's spread
grows with period, so this test is close to powerless for periods above about 4
— this is weak absence of evidence, not evidence of absence.

**3. Under a budget-matched search, Dorabella fits English badly.**

*(Numbers pending: the budget-matched run `src/matched.py` was still executing
when this entry was first committed. It gives every text — Dorabella, 100
genuine English controls and 100 shuffles of Dorabella — an identical budget of
500 restarts, which is the only way these scores can legitimately be compared.
This section is updated in a follow-up commit; see `results/matched_results.json`.)*

**4. At 87 characters, the top-scoring key is frequently not the correct key.**

150 genuine English texts of 87 characters were enciphered with a *known* random
key and attacked with 200 restarts each — the question nobody asks of a claimed
Dorabella solution, because for Dorabella the answer is unknowable:

| quantity | value |
|---|---|
| exact key recovered | 36.7% |
| median character accuracy of recovered plaintext | 98.9% |
| runs recovering >90% of characters | 88.0% |
| runs where a **wrong** key outscored the true key | **46.7%** |

The method is not useless — on genuine English it usually lands within a few
characters of the truth. But the exact top-scoring key is close to a coin flip.
Any Dorabella argument of the form "this key scores highest, therefore it is the
message" is resting on that coin flip.

**5. The best published monoalphabetic claim is neither the best-scoring key nor
a lonely one.**

The claimed key from `ShadowWolf387/DorabellaCipher` (`PSTYEHKWBARIGMXJFVOLDUNCZQ`,
verified here to reproduce that repository's published plaintext exactly from the
Williams reading) scores −4.7426 per quadgram — around the 10th percentile of
genuine English, which is a poor but not impossible fit. A 4,000-restart search
on the same reading explored 3,906 distinct local optima and found:

- **23 distinct keys scoring at or above the claim**, forming **13 mutually
  different messages** (median pairwise Hamming distance 62 of 87 characters);
- a top optimum at −4.6891 that beats the claim, and which is a near-variant of
  it, differing only in the assignment of rare symbols. The claimed key is not
  even optimal within its own family.

That repository's stated evidence — that 1.5 million trials found nothing better
— does not survive. This is not a refutation of the *reading* (the case for it
rests on Elgar's idiosyncratic spelling, which is outside statistics), but it
removes the statistical support offered for it. Thirteen unrelated messages clear
the same bar, and each is exactly as "readable" once the same interpretive licence
is applied.

### Failures & dead ends

- **No primary-source transcription was obtained.** This session's network egress
  reached only GitHub and PyPI; Wikipedia, ciphermysteries.com, dcode, arXiv,
  the HistoCrypt proceedings and CELT were all blocked. The seven readings come
  from a secondary compilation assembled by a partisan of one claimed solution,
  and their fidelity to the original publications is *not* independently verified.
  Every number above inherits that weakness.
- **The HistoCrypt 2021 paper *Experimental Analysis of the Dorabella Cipher with
  Statistical Language Models* could not be read.** Findings 2 and 3 plausibly
  overlap it. Nothing here should be claimed as novel until someone checks.
- **The arc-count / orientation coding of each symbol could not be obtained**, so
  the most interesting structural hypothesis — that the 3 arc counts and the 8
  orientations are two separate channels (e.g. one carrying vowels) — is untested.
- The English reference model had to be *generated* from a frequency-weighted
  lexicon rather than drawn from a corpus. It validates well (IC 0.0646 against
  the textbook 0.0667; RMS letter-frequency error 0.32 percentage points) but
  under-represents H (5.03% against 6.09%), a web-versus-literary register effect.
  Conclusions that turn on H should be treated with suspicion.
- **A methodological error worth recording:** the first solver run used 40
  restarts and reported Dorabella at −4.7970, apparently the best available. The
  published claimed key scores −4.7426, and a 4,000-restart run reached −4.6891.
  Search budget dominates these scores, and comparisons across different budgets
  are meaningless. Finding 3 was re-run with every text on an identical budget
  after this was noticed; the earlier unmatched numbers are retained in
  `results/raw_results.json` for the record.

### Artefacts produced

`attempts/2026-09-04-transcription-uncertainty/` —

- `data/transcriptions.json` — seven readings with provenance and caveats
- `src/lang.py` — English reference model and its validation
- `src/dorabella.py` — canonicalisation, relabelling-invariant comparison, statistics
- `src/solver.py` — quadgram hill climber
- `src/experiments.py`, `src/power.py`, `src/matched.py`, `src/claimed.py`,
  `src/families.py`, `src/extras.py` — the experiments
- `src/report.py` → `results/summary_tables.md` — every table in one place
- `results/*.json` — raw output with seeds

### References consulted

- `ShadowWolf387/DorabellaCipher` (GitHub, public; retrieved 2026-09-04) —
  `Transcripts.pdf`, `Dorabella-SolutionPt2.pdf`, `Texts/`. Source of the seven
  readings and of the claimed key tested in finding 5.
- Search-result summaries only (full text unreachable): HistoCrypt 2021,
  *Experimental Analysis of the Dorabella Cipher with Statistical Language
  Models*; ACL SMP 2021 / arXiv:2509.17950, *Dorabella Cipher as Musical
  Inspiration*; Sams (1970), reported as the foundational frequency and contact
  analysis. **None of these were read.**

---

## 2026-09-03 – Initial seed

Problem folder created.
