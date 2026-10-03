# Block-aware split for the face-blocked null (2026-10-02)

Discharges HANDOVER item 1: settle M288–N45, which the 2026-09-17 session left
*untestable rather than refuted* (p-floor 0.12 on the bucket-0 holdout).

**Read [`RESULTS.md`](RESULTS.md).** Predictions were frozen in
[`PREDICTIONS.md`](PREDICTIONS.md), commit `31a1004`, before any file in `results/` existed.

## Corpus

Not copied here. Clone the pin and point the scripts at it:

```sh
git clone https://github.com/sfu-natlang/pe-sign-value-data
cd pe-sign-value-data && git checkout 538949cca949a176400b144ef49c2036e9dc82a6
```

Expected: 1,467 `corpus/*.values.atf`; LF digest
`8849716c6afbf963e5ee02535da013c87c931c61e88e2c05ced9cd58bf2b2dcf`. The CRLF hash
`ee4fa7ba…c083d6a` recorded in `analysis/results/associations.json` is the same corpus checked out
on Windows — **not drift, do not re-pin.**

Every script takes the corpus directory as its last argument, or reads it from a local
`corpus_path.txt` (git-ignored) in this directory.

## Run

```sh
python3 -m unittest -v test_block_aware_split.py        # 10 tests, ~3 s
python3 block_aware_split.py  /path/to/corpus           # the eight pairs, ~7 s
python3 null_calibration.py   20000 /path/to/corpus     # procedure size, ~2 min
python3 competitor_null.py    200   /path/to/corpus     # the sweep + its null, ~4 min
python3 competitors.py        /path/to/corpus           # permissive variant, see caveat
```

Pure Python standard library — no third-party dependency, matching the `analysis/` pipeline.

## Files

| file | what it does |
|---|---|
| `common.py` | loads the corpus through the audited 2026-09-04 parser; per-block marginals |
| `block_aware_split.py` | the split rule, the re-screen, the exact face-blocked test, the p-floor |
| `null_calibration.py` | **the decisive check** — procedure size under two permutation nulls |
| `competitor_null.py` | all 390 testable pairs through the gate, against the gate's own null |
| `competitors.py` | same sweep with direction taken from validation — **inflated, see below** |
| `test_block_aware_split.py` | 10 tests; the load-bearing one reproduces 2026-09-17 at 1e-12 |

## Two things not to misread

1. **Six of the eight pairs fail the re-screen and that is not a refutation.** All eight clear the
   face-blocked validation test; the split rule moves 34–100 % of a pair's co-occurrence evidence
   into validation, gutting the screen for pairs whose evidence lives in informative blocks.
   M106–N24 loses all 14 of its co-occurrence lines and its training odds ratio inverts to 0.44.
2. **Cite 72, not 121.** `competitors.py` reads each pair's direction off its validation odds
   ratio (deliberate double-dipping, to give competitors their best shot) and reports 121 passing
   / rank 27. `competitor_null.py` reads direction from the training complement and is the clean
   procedure: **72 passing of 390 tested, rank 14, null expectation 9.4.**
