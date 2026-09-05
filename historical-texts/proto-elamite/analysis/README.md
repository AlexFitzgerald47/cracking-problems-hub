# Proto-Elamite held-out structure analysis

This directory contains a reproducible first experiment against the SFU Natural
Language Lab's CDLI-derived Proto-Elamite ATF corpus. It tests positional and
numeral-sign associations without assigning lexical meanings.

## Corpus pin

- Repository: <https://github.com/sfu-natlang/pe-sign-value-data>
- Commit: `538949cca949a176400b144ef49c2036e9dc82a6`
- Expected files: 1,467 `corpus/*.values.atf`
- Corpus digest: recorded in `results/associations.json`; the digest covers each
  sorted filename and its bytes, separated by NUL bytes.

The corpus is not copied here. Clone the source at the pinned commit, then run:

```powershell
python structure_associations.py C:\path\to\pe-sign-value-data\corpus `
  --json results\associations.json `
  --csv results\associations.csv
python -m unittest -v test_structure_associations.py
```

## Design

- Lines containing `...` or a standalone `x` are excluded.
- Physical face is retained across `@column` and `@seal` subdivision tags; those
  tags do not start a new obverse/reverse sequence.
- M-signs are reduced to their three-digit family because variants are sparse. A
  family occurrence can therefore be a standalone sign or a component of a compound.
- N-sign zero-padding is normalized, but letter and orientation variants are retained.
- Only N-signs after the ATF entry-boundary comma (or on numeral-only lines) are
  treated as accounting numerals. This prevents an embedded numerical component of
  a compound M-sign from creating a tautological association.
- The split is deterministic at tablet level: SHA-256 of the P-number modulo five.
  Bucket zero (about 20%) is held out. No tablet contributes lines to both sets.
- Candidate selection uses only training data (Benjamini-Hochberg q <= 0.01 and
  Haldane-Anscombe-corrected odds ratio >= 3 or <= 1/3).
- Validation uses an exact randomization distribution that shuffles the target only
  among lines of the same tablet, so repeated lines are not treated as independent.
  A candidate is reported only when the held-out direction agrees, validation
  Benjamini-Hochberg q <= 0.05, and corrected odds ratio >= 1.5 or <= 2/3.

The output is evidence of structural association, not a decipherment. In particular,
an M-sign/numeral-sign pair does not by itself establish a commodity, unit, word, or
language reading.
