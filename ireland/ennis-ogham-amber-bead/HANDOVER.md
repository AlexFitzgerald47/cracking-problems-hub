# Handover — Ennis ogham amber bead

Last session: 2026-09-06, GPT-5.6 Sol

## State in one paragraph

The bead is **not deciphered**, but the problem is now materially narrower. Do not start from `ATUCMLU` as if it were observed text. The best remote object evidence is the OG(H)AM team's December-2023 direct examination: detached/non-ogham `<`-like mark, core `DMVA` or `DMLO`, then a stemline fork around the perforation with a right branch apparently `VA` and an anomalous left branch. This creates at least eight structural cases before anomalous signs receive phonetic values. Macalister's `ATUCMLU` depends on two explicitly weak U-forfid identifications. The older `MTBCML` → reverse `LMCBTM` comparison with Glenfahan `LMCBDV` also fails to reproduce against the modern reading. Westropp's account appears to swap the Ennis/Glenfahan assignments and should not be counted as independent evidence.

## What was attempted

1. Froze the modern specialist observations before lexical interpretation.
2. Audited the main historical readings (`MTBCML`, `ATUCMLU`) against the direct modern examination.
3. Reconstructed the origin of the Glenfahan parallel and Marstrander's *rúnogam* proposal.
4. Cross-checked the object assignments against the machine-readable OG(H)AM data corpus.
5. Counted the minimum structural branch budget and committed a small reproducible enumerator.

## What worked

- The modern report is specific enough to show that a one-dimensional text model is premature.
- The historical literature provides a falsifiable genealogy of the “magical formula” idea: its strongest cross-object support arose from an older Ennis transcription that is no longer reproduced.
- Cross-source checking caught a probable Westropp attribution/transmission swap before it could become a false independent witness.

## What failed / was killed

- **`ATUCMLU` as ground truth:** killed. It remains a historical hypothesis only.
- **Glenfahan resemblance as independent confirmation of the Ennis reading:** killed in its strong form. The resemblance is transcription-dependent.
- **Immediate dictionary / name search:** not justified while the input graph remains unresolved.
- **Simple reverse-string treatment:** invalid for the opposite ogham reading direction; values must be recomputed from stroke geometry.

## Highest-value next experiment

Obtain or generate high-resolution 3D / RTI / photogrammetric surface evidence for British Museum 1888,0719.119, especially the fork and both anomalous marks.

Blind to language, answer these in order:

1. Does the left-hand apparent branch actually intersect the main stemline, or merely approach/cross it in projection?
2. Which strokes terminate at the stem, cross it, or continue through it?
3. Is there a detectable cutting-order/tool-profile difference between the two fork branches?
4. Is the detached `<` genuinely two intentional strokes, and is either stroke continuous with the stem under surface relief?
5. Does either fork branch have a natural start/end geometry that selects the reading path?

One good surface model could collapse most of the branch tree. That is more valuable than another hundred lexical searches.

## Secondary next experiment

Adjudicate Westropp 1911 against the original printed plate and footnote [107], then trace the pre-1945 `MTBCML` reading to its earliest drawing/transcription. Goal: determine whether `MTBCML` was ever an independent observation of the bead or was already a transformation of the Glenfahan comparison.

## Only after the geometry is frozen

- Recompute both reading directions from actual stroke side/count, not string reversal.
- Enumerate all surviving character-value branches in a machine-readable table.
- Compare ordinary ogham formulae, personal names, learned/cryptic ogham systems, magical notation and non-phonetic marking at the **same branch budget**.
- Use Glenfahan only as a held-out comparator after the Ennis transcription is fixed; do not use it to choose Ennis signs and then claim the resemblance as validation.

## Files

- `PROBLEM.md` — target and inherited readings
- `SOURCES.md` — source ledger and cautions
- `PROGRESS.md` — full first-session findings
- `analysis/evidence-ledger.md` — OBSERVED / INFERRED / MISSING ledger and hypothesis audit
- `code/branch_model.py` — conservative branch enumerator
