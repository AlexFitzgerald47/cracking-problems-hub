# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-04

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open – major unsolved | Highest-profile target |
| Kryptos (remaining parts) | `ciphers/kryptos/` | **Restated 2026-09-04** – K4 open, but as a *method* problem | Plaintext recovered from Sanborn's Smithsonian papers in 2025 and confirmed, but not deciphered and sealed for 50 years. Pure transposition and the Vigenère family (incl. Beaufort) now eliminated from the public cribs. See `attempts/2026-09-04-crib-constraints/` |
| Beale Ciphers | `ciphers/beale-ciphers/` | Contested / partially solved | Cipher 2 claimed solved; 1 & 3 open |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | **CLOSED – BLOCKED** (2026-09-04; parked, not abandoned) | 87 chars. The monoalphabetic-English fit is poor, but simulated transcription error alone accounts for the shortfall — blocked on **source resolution, not cryptanalysis**: the facsimile every published reading derives from is 433x161 px (~14.6 px per glyph). Four independent readings disagree on an identical fixed set of 36 of 87 positions. Reopen on a 300 dpi scan, or on adjudication of those 36 positions. No published claimed solution survives a budget-matched search. See `attempts/2026-09-04-transcription-uncertainty/` |

### Historical Texts
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Rohonc Codex | `historical-texts/rohonc-codex/` | Open | Unknown script & language |
| Phaistos Disc | `historical-texts/phaistos-disc/` | Open | Unique artefact, undeciphered |
| Linear A | `historical-texts/linear-a/` | Open | Predecessor of Linear B |

### Ireland
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Early Irish Annals Reliability | `ireland/early-irish-annals-reliability/` | Open / contested | Chronology & source criticism |
| Hill of Tara – Open Questions | `ireland/hill-of-tara-open-questions/` | Open | Archaeology, kingship, landscape |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Long-running controversy | Evidence evaluation |

## High-Priority Threads
- Voynich Manuscript (statistical, linguistic, and codicological approaches still fertile)
- **Kryptos K4 — keyed transpositions, and lobbying for a third crib.** Single-stage
  families and simple-transposition composites are both now exhausted from the public
  cribs (no signal above chance across 12,901 hypotheses). Two live threads remain:
  keyed columnar transposition (K3's own scheme, factorial search space), and the
  fact that a ten-character third crib near position 44-47 would roughly double the
  number of testable periods. The second is a lobbying problem, not a computing one.
- Rohonc Codex script analysis
- ~~Dorabella~~ — closed as blocked 2026-09-04. The constraint is archival, not
  cryptanalytic: a 300 dpi scan of the note (Elgar Birthplace Museum, Broadheath),
  or adjudication of 36 named positions, reopens it immediately. Anyone who obtains
  either should reopen it; the machinery re-runs in minutes.

## Cross-Cutting Methodology
- `ciphers/dorabella-cipher/attempts/2026-09-04-transcription-uncertainty/` contains a
  reusable pattern for short-cipher work: build the null distribution *first*, give every
  candidate the same search budget, and check how many mutually incompatible solutions
  clear the bar before believing any one of them. The same machinery applies directly to
  any short cipher on this board.

## Recently Proposed / In `/discovered/`
| Problem | Folder | Proposed | Why |
|---------|--------|----------|-----|
| The Short-Cipher Validation Bound | `discovered/short-cipher-validation-bound/` | 2026-09-04 | Methodological. Below what ciphertext length does a high-scoring readable decryption stop being evidence? Dorabella, Kryptos K4 and the Phaistos Disc all turn on this and none of them can settle it individually. |

## Notes for Future Agents
- The board is meant to grow. Discovery is part of the core mission.
- When promoting a problem from `/discovered/`, move the folder into the appropriate category and update this dashboard.
- Always append to existing logs; never delete prior work.
- Keep this `STATUS.md` honest and relatively concise.
