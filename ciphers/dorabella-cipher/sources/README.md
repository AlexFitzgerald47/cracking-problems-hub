# Primary sources – Dorabella Cipher

This folder is for primary material: facsimiles of the original note, scans of
the published transcriptions, and anything else an agent should be able to read
for itself rather than take on trust from a secondary compilation.

It is currently **empty, and that is the problem**. The 2026-09-04 attempt
established that the whole Dorabella question is blocked on transcription
uncertainty rather than on cryptanalysis: the three genuinely distinct published
readings disagree at 36 of 87 positions, and simulated misreading at that rate
is by itself enough to account for the cipher's poor fit to English. See
`../attempts/2026-09-04-transcription-uncertainty/`.

## Wanted, in priority order

1. **A facsimile image of the original note.** The highest-value single artefact
   on this problem. It lets an agent produce a reading with known provenance,
   made blind to the existing claimed solutions.
   Canonical copy: `Dorabella-cipher-image.png` on Wikimedia Commons
   (`upload.wikimedia.org/wikipedia/commons/7/73/`). Public domain — Elgar died
   in 1934 and the note dates from 1897.
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
