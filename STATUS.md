# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-04

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open – major unsolved | Highest-profile target |
| Kryptos (remaining parts) | `ciphers/kryptos/` | Partially solved | K4 still open |
| Beale Ciphers | `ciphers/beale-ciphers/` | Contested / partially solved | Cipher 2 claimed solved; 1 & 3 open |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | Open – **first serious attempt logged 2026-09-04** | 87 chars. Monoalphabetic-English hypothesis now quantitatively disfavoured; no published claimed solution survives a budget-matched search. See `attempts/2026-09-04-transcription-uncertainty/` |

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
- Kryptos K4
- Rohonc Codex script analysis
- **Dorabella: obtain a primary-source transcription.** The 2026-09-04 attempt showed
  that published readings disagree at ~40% of positions, and that everything downstream
  inherits that uncertainty. This is the binding constraint on the problem, and it is
  an archival task rather than a cryptanalytic one.

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
