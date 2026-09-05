# Held-out structure and numeral-sign associations

**Run date:** 2026-09-04
**Corpus:** SFU `pe-sign-value-data` at commit
[`538949cca949a176400b144ef49c2036e9dc82a6`](https://github.com/sfu-natlang/pe-sign-value-data/commit/538949cca949a176400b144ef49c2036e9dc82a6)

## Result in one sentence

A deterministic tablet-level holdout recovered the expected first-line structure and
confirmed eight M-sign/numeral-sign associations after a within-tablet exact
randomization test; these narrow context for the sign families but do not establish
word meanings.

## Corpus audit

The pinned source has 1,467 ATF files. Ten contain no numbered transliteration line
(they are blank, broken, anepigraphic, or have only seal/design metadata), leaving
1,457 tablets with 11,013 numbered lines. After excluding damaged lines and requiring
both an M-sign and an accounting N-sign, 4,869 lines remained: 3,819 from 1,160
training tablets and 1,050 from 297 tablets reserved for validation. The exact empty
file list and corpus digest are in `results/associations.json`.

The split is by P-number hash, so a tablet cannot leak across training and validation.
Validation p-values come from an exact null distribution that preserves each tablet's
line count and the within-tablet marginal frequencies of the M-sign and target. The
reported validation q-values apply Benjamini-Hochberg correction across the screened
candidates.

## Sanity check: first-line structure

The strongest result is M157. In validation it occurs on 69 of 164 intact first
obverse lines with an M-sign (42.1%), but only 12 of 905 later such lines (1.3%):
corrected odds ratio 52.0, within-tablet validation q = 2.69e-23. M327 and M342 are
also enriched on the first obverse line (validation odds ratios 12.5 and 12.2).

This is a pipeline sanity check, not a new decipherment claim. Englund describes the
known heading-first structure of Proto-Elamite accounts, and Born et al. later tested
header identification computationally. The present result independently recovers that
structure with a simple held-out statistic:

- [Englund, “The State of Decipherment of Proto-Elamite”](https://cdli.ucla.edu/staff/englund/publications/englund2004c.pdf)
- [Born et al. 2022, “Sequence Models for Document Structure Identification in an Undeciphered Script”](https://aclanthology.org/2022.emnlp-main.620/)
- Example held-out tablet: [P008003](https://github.com/sfu-natlang/pe-sign-value-data/blob/538949cca949a176400b144ef49c2036e9dc82a6/corpus/P008003.values.atf), whose first obverse line is `M157 ,`

## Confirmed numeral-sign context constraints

Eight training-screened associations replicated in the held-out tablets. The strongest
and most interpretable constraints are:

| M-sign family | Accounting N-sign | Validation context rates | Corrected OR | Validation q | Constraint |
|---|---:|---:|---:|---:|---|
| M297 | N39B | 32/55 vs 96/995 | 12.89 | 0.00024 | Strong enrichment |
| M297 | N24 | 13/55 vs 51/995 | 5.83 | 0.0055 | Enrichment |
| M297 | N01 | 20/55 vs 731/995 | 0.21 | 0.0055 | Strong depletion |
| M263 | N30C | 0/46 vs 68/1004 | 0.15 | 0.0166 | Replicated absence/depletion |
| M263 | N01 | 38/46 vs 713/1004 | 1.85 | 0.0189 | Modest enrichment |
| M243 | N39B | 8/15 vs 120/1035 | 8.61 | 0.0222 | Strong enrichment, low support |
| M106 | N24 | 3/18 vs 61/1032 | 3.57 | 0.0390 | Enrichment, low support |
| M288 | N45 | 15/118 vs 8/932 | 16.29 | 0.0480 | Strong enrichment, boundary q |

“Context rates” means target-N-sign lines among lines with that M-sign, versus target
N-sign lines among other eligible validation lines. The odds ratio uses a 0.5 cell
correction; the q-value comes from the blocked exact test, not an independence
assumption over lines.

Examples can be inspected directly in the pinned corpus:

- [P008003 obverse 3](https://github.com/sfu-natlang/pe-sign-value-data/blob/538949cca949a176400b144ef49c2036e9dc82a6/corpus/P008003.values.atf) contains M297 with `2(N39B)`.
- [P008010 reverse 2](https://github.com/sfu-natlang/pe-sign-value-data/blob/538949cca949a176400b144ef49c2036e9dc82a6/corpus/P008010.values.atf) contains M288 with `1(N45) 3(N14)`.

Contextual coupling between numerical systems and quantified objects is an established
route to semantic analysis, explicitly discussed by Englund. This experiment supplies
held-out candidate constraints for that route; it does **not** map N39B, N24, N01,
N30C, or N45 to a semantic domain, and it does not assign a lexical value to any M-sign.

## Failure caught during the run

The first parser version counted every parenthesized N-sign on a line. That produced a
very strong M036–N30D association, but inspection showed that many occurrences were
the compound `M036+1(N30D)` before the ATF comma. The result was tautological. The
parser now accepts only N-signs in the accounting field after the comma (or on
numeral-only lines), and the false association disappears. A regression test fixes
this behavior.

The SFU `pe-decipher-toolkit` repository also failed to check out on Windows because
its tree includes `pngs/PE_mainforms/M370-M ?.png`. This did not block the experiment:
the separate `pe-sign-value-data` repository checked out cleanly and is the pinned
input used here.

## Limits and falsifiable predictions

- M-sign variants are merged to the three-digit family and explicit compounds are
  split into family components. The associations therefore apply to family presence,
  not necessarily to every graphical variant or compound independently.
- This is one historical corpus snapshot. The strongest falsification test is to run
  the unchanged script on later or newly published ATF tablets.
- Predictions: M297 should remain enriched with N39B and depleted with N01; M263 should
  remain absent or rare with N30C; M288 should remain enriched with N45. Failure of the
  direction on genuinely new tablets would weaken the corresponding constraint.
- The M288–N45 result is least secure statistically because its validation q-value is
  near 0.05. It should be treated as a priority replication target, not as settled.
- Novelty relative to every specialist publication has not been established. The
  contribution here is the reproducible held-out test and its constraints, not a
  claim that these pairings have never been noticed.

## Reproducibility and related work

- Code and exact commands: `analysis/README.md`
- Machine-readable output: `results/associations.json` and
  `results/associations.csv`
- Unit tests: `test_structure_associations.py`
- Earlier computational analysis of sign context: [Born et al. 2019, “Sign Clustering and Topic Extraction in Proto-Elamite”](https://aclanthology.org/W19-2516/)
