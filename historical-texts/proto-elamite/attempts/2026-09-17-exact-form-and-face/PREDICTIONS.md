# Frozen predictions — 2026-09-17 session

Written **before** running any of the three tests below, and committed before the
result files. Everything here is a prediction about evidence not used to derive it.
The 2026-09-04 result table was used to choose *which* eight pairs to test; the
predictions are about what happens to those pairs under new conditions.

## Test A — face-blocked null

The 2026-09-04 validation permutes the target within *tablet*. Any confound constant
within a tablet (provenience, scribe, period, publication, tablet type) is therefore
already controlled. What is **not** controlled is position within the tablet: a
Proto-Elamite obverse carries itemised entries and the reverse carries totals, and the
two faces use numerals differently. I re-run the identical exact test with blocks
keyed on `(tablet, face)` instead of `tablet`.

- **A1.** M297–N39B survives at validation q ≤ 0.05 under the face-blocked null.
- **A2.** M288–N45 does **not** survive. M288 is strongly depleted on the first obverse
  line (validation OR 0.19), i.e. it is face-skewed, and its held-out q was already
  0.0480. I expect the face block to remove it.
- **A3.** Of the eight confirmed numeral associations, at least six survive. If fewer
  than four survive, the 2026-09-04 constraint set is substantially a face artefact and
  must be restated.

## Test B — exact-form audit of M297

M297 occurs in the corpus under exactly these surface forms (whole-corpus counts):
plain `M297` 265, `M297~B` 80, `M297~D` 12, `M297~C` 4, `M297~A` 1, `M297@b` 1, plus
the compounds `M297+X` (2), `M297+M296` (2), `M297~BC` (2), `M297~B+M388` (1).
Only plain M297 and M297~B have enough support to test separately.

The 2026-09-04 design merges all of these into the family `M297`. That merge is an
assumption, and Proto-Elamite scholarship does not agree that graphic variants are
allographs.

- **B1.** The merge is sound: plain M297 and M297~B have statistically homogeneous
  N39B rates (Fisher two-sided p > 0.05 on the 2×2 of form × N39B-presence), and the
  same for N01 depletion.
- **B2.** Both forms individually show N39B enrichment in the same direction relative
  to the corpus base rate.

If B1 fails, the family merge is hiding two functionally different signs and the
published constraint is about one of them, not about "M297".

## Test C — cross-class self-match (the 2026-09-17 handover instruction)

The board's instruction: take a class attested in two conditions, score it against
itself across the boundary, and report that number beside the association statistics.
Here the class boundary is **face** (obverse = entries, reverse = totals), and the
"score" is the distance between numeral-context profiles.

Profile of a sign on a face = the vector of P(N-sign present | line has that sign) over
the common N-signs, estimated on that face only. Distance = total variation distance.

- **C1.** The self-distance — the same M-sign compared with itself across the
  obverse/reverse boundary — is **large**, comparable to or greater than the distance
  between different M-signs on the same face. This is the Junius/register analogue and
  I expect it to reproduce here, because totals and entries are genuinely different
  numeral contexts.
- **C2.** If C1 holds, then any pooled obverse+reverse odds ratio is partly a face
  statistic, and the correct reporting unit is within-face. This is a prediction about
  how the folder's result table should be restated, and Test A is its direct check.

## Null model

Every test above is reported alongside a null in which the tested quantity is
recomputed on M-signs matched for line count but with no selected association, and —
for Test C — on a permutation that reassigns the face label within tablet, preserving
line counts. A distance that looks large must be shown to be larger than the null's.
