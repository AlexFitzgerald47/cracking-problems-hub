# Primary sources – Dorabella Cipher

This folder is for primary material: facsimiles of the original note, scans of
the published transcriptions, and anything else an agent should be able to read
for itself rather than take on trust from a secondary compilation.

It currently holds the commonly circulated facsimile — **which has been measured
and found too coarse to read** (433 × 161 px, ~14.6 px per glyph; see
`../attempts/2026-09-04-transcription-uncertainty/results/facsimile_results.json`).
That is the problem. The 2026-09-04 attempt
established that the whole Dorabella question is blocked on transcription
uncertainty rather than on cryptanalysis: the three genuinely distinct published
readings disagree at 36 of 87 positions, and simulated misreading at that rate
is by itself enough to account for the cipher's poor fit to English. See
`../attempts/2026-09-04-transcription-uncertainty/`.

## Wanted, in priority order

1. **A high-resolution scan of the original note** — 300 dpi or better. The
   highest-value single artefact on this problem, and the one thing that would
   unblock it. The physical note is held by the Elgar Birthplace Museum,
   Broadheath. A plate from a published facsimile edition of the Elgar–Penny
   correspondence would also serve.

   *Already here and NOT sufficient:* `dorabella-facsimile.png`, the Wikimedia
   Commons copy (`commons/7/73/Dorabella-cipher-image.png`, public domain —
   the note is from 1897, Elgar died 1934). At 433 × 161 px it resolves the three
   cipher lines and the dated signature cleanly, but not glyph boundaries: ink
   runs correspond to arcs rather than symbols, and the eight orientations are
   45° apart across about fourteen pixels. Every published reading appears to
   derive from this image, which is the likeliest explanation for why they
   disagree at 36 of 87 positions. Do not attempt a reading from it.
2. **The consensus transcription in orientation + arc-count form** (orientation
   A–H, arcs 1–3), as used in the HistoCrypt 2021 paper. This is what makes the
   two-channel structural hypothesis testable at all; the letter-label readings
   in `../attempts/.../data/transcriptions.json` have thrown that information away.
3. **Scans or PDFs of the original publications** behind each reading in that
   file — Sams (1970), Roberts, Gaffney, Schmeh/MTC3, Ernst — so the attributions
   can be verified rather than inherited from a partisan compilation.

## How to add material

Commit the file here and note it in `../PROGRESS.md`. Agents can read images and
PDFs directly from the repository, so a committed facsimile is immediately
usable and, unlike a link, survives egress restrictions and link rot.

Record provenance and licence for anything added. Do not commit material whose
copyright status is unclear.
