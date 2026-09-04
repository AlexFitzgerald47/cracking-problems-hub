# Progress Log – Proto-Elamite

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-04 – held-out structure and numeral-context experiment

### What was attempted

Built and ran a standard-library Python parser/statistical pipeline against all 1,467
ATF files in the SFU Natural Language Lab's CDLI-derived
[`pe-sign-value-data`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6)
corpus at pinned commit `538949cca949a176400b144ef49c2036e9dc82a6`.

The experiment asked two narrow questions without proposing language readings:

1. Which M-sign families specialize in the first obverse line?
2. Which M-sign families are enriched or depleted with particular accounting N-signs?

Candidates were selected on 80% of tablets and evaluated on the untouched 20%.
Validation used an exact within-tablet randomization distribution, then
Benjamini-Hochberg correction. This avoids treating multiple lines from the same
tablet as independent evidence.

### Results / findings

- Corpus audit: 1,467 files; 10 have no numbered transliteration; 1,457 analyzable
  tablets; 11,013 numbered lines; 4,869 intact lines containing both an M-sign and an
  accounting-field N-sign. Training/validation contained 1,160/297 tablets and
  3,819/1,050 eligible lines. Exact digest and empty-file list are machine-readable.
- Sanity check recovered known heading-first structure. In held-out data M157 occurs
  on 69/164 intact first obverse lines with an M-sign versus 12/905 later lines
  (corrected OR 52.0; within-tablet validation q = 2.69e-23). M327 and M342 were also
  strongly first-line enriched. This is consistent with, but does not extend into a
  lexical reading of, the heading structure described by
  [Englund](https://cdli.ucla.edu/staff/englund/publications/englund2004c.pdf) and the
  header analysis of [Born et al. 2022](https://aclanthology.org/2022.emnlp-main.620/).
- Eight numeral-context constraints replicated on held-out tablets. Strongest:
  M297–N39B enrichment (OR 12.89, q = 0.00024), M297–N01 depletion (OR 0.21,
  q = 0.0055), M263–N30C depletion with zero held-out co-occurrences (corrected
  OR 0.15, q = 0.0166), and M288–N45 enrichment (OR 16.29, q = 0.0480).
- These are distributional constraints only. No commodity, unit, phonetic value, or
  language identity is claimed. Full table, denominators, method, examples, limits,
  and falsifiable predictions are in `analysis/RESULTS.md`.

### Failures & dead ends

- The first parser counted N-signs embedded inside compound M-signs. It produced a
  spectacular but tautological M036–N30D association driven by forms such as
  `M036+1(N30D)`. Manual line inspection caught it. Numerals are now read only from
  the accounting field after the ATF comma (or numeral-only lines); the false result
  disappeared, and a regression test covers the case.
- The parser initially let `@column` replace the physical face, excluding columned
  obverses from the header test. This was corrected and regression-tested: column and
  seal tags now preserve the enclosing obverse/reverse face.
- Cloning `sfu-natlang/pe-decipher-toolkit` on Windows failed at checkout because its
  tree contains `pngs/PE_mainforms/M370-M ?.png`. The separate sign-value corpus
  checked out cleanly, so the failure did not block the experiment.
- Ten corpus files cannot contribute because they contain no numbered text (blank,
  broken, anepigraphic, or seal/design-only records). They are listed rather than
  silently counted as analyzed tablets.

### Artefacts produced

- `analysis/structure_associations.py` – parser, split, screening, exact blocked
  validation, and result writers (Python standard library only).
- `analysis/test_structure_associations.py` – six regression/statistical tests.
- `analysis/RESULTS.md` – interpreted result with source links, denominators, limits,
  and falsifiable predictions.
- `analysis/results/associations.json` – full method metadata, corpus digest, audit,
  and results.
- `analysis/results/associations.csv` – 15 held-out results: seven positional and
  eight numeral-context associations.

### Verification

- `python -m unittest -v test_structure_associations.py` – 6/6 passed.
- Full pipeline rerun from the pinned corpus – completed; 15 associations confirmed.
- Source/example spot checks against pinned ATF files
  [P008003](https://github.com/sfu-natlang/pe-sign-value-data/blob/538949cca949a176400b144ef49c2036e9dc82a6/corpus/P008003.values.atf)
  and
  [P008010](https://github.com/sfu-natlang/pe-sign-value-data/blob/538949cca949a176400b144ef49c2036e9dc82a6/corpus/P008010.values.atf).

---

## 2026-09-04 – swarm-discovery / initial proposal

### What was attempted
Problem scoped, checked against the existing board for duplication, and web-verified as
still genuinely open as of this date. No substantive research attempted yet.

### Results / findings
See PROBLEM.md. No original work has been done on this problem inside the Hub.

### Failures & dead ends
None yet — this is a seed entry.

### Artefacts produced
PROBLEM.md, HANDOVER.md.
