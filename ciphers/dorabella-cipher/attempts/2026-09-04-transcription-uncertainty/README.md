# Attempt: what can actually be proved about the Dorabella cipher at 87 characters?

**Date:** 2026-09-04  ·  **Status:** complete, negative/limiting result  ·  **Reproducible:** yes

This attempt does not propose a decipherment. It measures the evidential ceiling
that any Dorabella decipherment of the monoalphabetic class has to clear, and
checks whether that ceiling is reachable at all at 87 characters.

Three questions:

1. **How stable is the ciphertext itself?** Every published attack picks one
   transcription and proceeds. How much do the transcriptions actually differ,
   measured in the only way that matters cryptanalytically?
2. **Do Dorabella's statistics distinguish it from English?** The literature
   repeats that they do. Tested against a proper null at n = 87.
3. **At 87 characters, does the highest-scoring key equal the correct key?**
   Measured directly on genuine English enciphered with a known key. This is the
   question that decides whether "my search found a readable high-scoring key"
   is evidence of anything.

## Headline

Dorabella fits English badly and beats the noise floor cleanly — but simulating
transcription error at the rate the published readings themselves exhibit puts
genuine English in exactly the same place 12–32% of the time. The monoalphabetic
question is therefore **blocked on the transcription, not on the cryptanalysis**.
Separately, 13 mutually unrelated messages score at or above the best published
monoalphabetic claim, so that claim's score gives it no special standing.

## Layout

```
data/transcriptions.json   seven readings, with provenance and caveats
src/lang.py                English reference model + its validation
src/dorabella.py           canonicalisation, relabelling-invariant comparison, stats
src/solver.py              quadgram hill climber
src/experiments.py         descriptive statistics + first (unmatched) solver pass
src/power.py               solver power / key-recovery measurement on known keys
src/matched.py             budget-matched comparison: cipher vs English vs noise
src/claimed.py             scores the best published claim; enumerates rival optima
src/families.py            clusters those optima into distinct messages
src/corrupt.py             does transcription error alone explain the gap?
src/extras.py              periodic IC; per-position transcription instability
src/report.py              renders results/summary_tables.md
results/                   raw JSON + rendered tables
```

## Reproduction

```
pip install numpy wordfreq
cd src
python experiments.py     # ~3 min
python power.py           # ~15 min
python extras.py          # ~2 min
python matched.py         # ~23 min
python claimed.py         # ~1 min
python families.py
python corrupt.py         # ~17 min
python report.py
```

Seeds are recorded in each result file. The English reference model is built on
first use and cached to `data/lang_cache.pkl` (not committed).

## Method note: comparing transcriptions

Under a monoalphabetic assumption the only cryptanalytically meaningful content
of a reading is its **partition** — which positions carry the same symbol. Two
readings that disagree only about what to *name* a symbol are the same reading.
So every comparison here is done on the equality relation `1[x_i == x_j]` over
all 3,741 position pairs, never on letter names. This also lets published
*decrypts* be compared against *transcriptions* on equal terms, since under a
monoalphabetic key a decrypt is just a relabelling of a transcription.
