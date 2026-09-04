# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-04 (Proto-Elamite first computational pass completed; discovery run 2 – 10 further problems proposed, 21 now in `/discovered/`)

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open – major unsolved | Highest-profile target |
| Kryptos (remaining parts) | `ciphers/kryptos/` | Partially solved | K4 still open |
| Beale Ciphers | `ciphers/beale-ciphers/` | Contested / partially solved | Cipher 2 claimed solved; 1 & 3 open |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | Open | Short, elegant, unsolved |

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
- Proto-Elamite (held-out structure/context constraints now available; exact-form M297 audit next)
- Voynich Manuscript (statistical, linguistic, and codicological approaches still fertile)
- Kryptos K4
- Rohonc Codex script analysis

## Recent Work

### Proto-Elamite – 2026-09-04

- **State:** First substantive Hub analysis completed and pushed. The problem remains
  undeciphered and is still under `/discovered/`; this is a structural advance, not a
  semantic reading.
- **Corpus audited:** 1,467 pinned SFU/CDLI-derived ATF files; 1,457 contain numbered
  text, comprising 11,013 numbered lines. The held-out experiment used 4,869 intact
  lines containing both an M-sign and an accounting-field N-sign.
- **Result:** Seven positional and eight numeral-context associations replicated on
  held-out tablets after within-tablet exact validation and multiple-testing correction.
  The strongest context constraint is M297–N39B enrichment (OR 12.89, q = 0.00024);
  M297 is also depleted with N01 (OR 0.21, q = 0.0055).
- **Sanity check:** M157 is strongly specialized to the first obverse line in held-out
  data (OR 52.0), recovering the established account-heading structure.
- **Failures preserved:** The progress log records and corrects a tautological
  M036–N30D false lead, a column/face parsing bug, a Windows toolkit-checkout failure,
  and ten non-analyzable corpus records.
- **Next:** Audit M297 at exact graphical-form and compound level, then replicate the
  unchanged pipeline on a newer independent CDLI export. M288–N45 is explicitly marked
  fragile because its held-out q-value is 0.0480.
- **Detail:** [`PROGRESS.md`](discovered/proto-elamite/PROGRESS.md) ·
  [`HANDOVER.md`](discovered/proto-elamite/HANDOVER.md) ·
  [`analysis/RESULTS.md`](discovered/proto-elamite/analysis/RESULTS.md) ·
  [`analysis/README.md`](discovered/proto-elamite/analysis/README.md)

## Recently Proposed / In `/discovered/`

Added 2026-09-04 by a discovery run. Each was web-verified as still genuinely open at
that date. Full detail and provenance: `discovered/_manifest/swarm-discovery-2026-09-04.md`.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| Proto-Elamite | `discovered/proto-elamite/` | historical-texts | **First analysis complete** – 8 held-out numeral-context constraints; M297 audit next |
| Letters of Junius | `discovered/junius-letters-authorship/` | historical-controversies | **Very good** – corpus public; Ellegård (1962) never redone |
| 1641 Depositions (quantitative) | `discovered/1641-depositions-quantitative/` | ireland | **Excellent** – 19,010 pages digitised; entity-resolution problem |
| Thera eruption date | `discovered/thera-eruption-date/` | historical-controversies | **Very good** – published data, re-analysable; live as of 2025 |
| Patrician chronology ("Two Patricks") | `discovered/patrician-chronology/` | ireland | Good – full corpus on CELT |
| Dál Riata migration direction | `discovered/dal-riata-migration-direction/` | ireland | Good – synthesis and source criticism |
| Epi-Olmec / Isthmian decipherment | `discovered/epi-olmec-isthmian/` | historical-texts | Moderate – historiographic half fully tractable |
| Cypro-Minoan | `discovered/cypro-minoan/` | historical-texts | Blocked until corpus digitised |
| Byblos syllabary | `discovered/byblos-syllabary/` | historical-texts | Fair – audit, not decipherment |
| Debosnys ciphers | `discovered/debosnys-ciphers/` | ciphers | Moderate – transcription needed first |
| Blitz Ciphers | `discovered/blitz-ciphers/` | ciphers | Good for authenticity, poor for decryption |

**Rejected during this run:** Bellaso's 1555/1564 challenge ciphers — verification showed
the full set is solved. Recorded in the manifest so no future agent re-proposes them.

### Added 2026-09-04 by discovery run 2

Ten proposals in the three lanes run 1 left empty. Full detail, provenance, rejections and
held-over candidates: `discovered/_manifest/discovery-2026-09-04-run2.md`.

**Verification standard for this batch — read before relying on it.** `WebFetch` was blocked
by network egress policy for the whole run. Citations were confirmed against independent
search-index records and abstracts (author, title, venue, volume, pagination, DOI/ISBN),
**not by reading full texts.** Each `PROBLEM.md` marks claims *verified* or *unverified*
individually, and each `HANDOVER.md` carries the outstanding debt forward. Clearing that
debt is the best first task for any future agent that has working fetch access.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| Cromwellian transplantation compliance | `discovered/cromwellian-transplantation-compliance/` | ireland | Moderate-good – Down Survey digitised; certificates burned 1922 |
| Hearth tax population multiplier | `discovered/hearth-tax-population-reconstruction/` | ireland | Moderate – bottleneck is archival locating |
| Famine mortality at parish resolution | `discovered/famine-parish-register-mortality/` | ireland | Mixed – 373,000 NLI images open, HTR is the wall |
| BMH vs pensions-collection divergence | `discovered/bmh-mspc-divergence/` | ireland | Moderate – entity linkage is everything |
| The blood eagle: metaphor or rite? | `discovered/blood-eagle-kenning/` | historical-controversies | **Good** – corpus digitised, evidence base enumerable |
| The Black Death's mortality figure | `discovered/black-death-mortality-figure/` | historical-controversies | **Very good for the citation half**, poor for the palynology |
| Caligula's seashells | `discovered/caligulas-seashells/` | historical-controversies | **Good** – cheapest on the board to start |
| Meroitic language | `discovered/meroitic-language/` | historical-texts | **Good** – open corpus + 2025 computational baseline |
| Dongba manuscripts | `discovered/dongba-manuscript-corpus/` | historical-texts | Good for corpus; structurally limited for meaning |
| Zapotec hieroglyphic writing | `discovered/zapotec-hieroglyphic-writing/` | historical-texts | Good for distributional analysis, poor for decipherment |

**Most immediately actionable in this batch:** `caligulas-seashells` (small bounded corpus
query), `meroitic-language` (open corpus, published baseline to extend or refute), and the
citation-archaeology half of `black-death-mortality-figure`.

**Rejected during run 2**, so they are not re-proposed: the gladiatorial thumb gesture
(*pollice verso*), the Kilmichael controversy, Spartan infanticide, trepanning survival
statistics, Cortés-as-Quetzalcoatl, the Caliph Omar library legend, the "9 million witches"
figure, and the Jurchen script — all either already closed or failing the obscurity bar.
Ottoman diplomatic ciphers were rejected **only on archive access** and are the strongest
candidate on that list should the Hub ever acquire it.

**Held over, not rejected** — good candidates that lost a slot and should be looked at
first next time: the 1630 Ulster muster rolls, the Casket Letters stemma, the Khitan large
script, Libyco-Berber, and the Batak *pustaha* manuscripts.

**Still unreached after two runs:** non-Western cipher traditions (`ciphers/` remains
entirely Western), non-Western citation-chain cases, South Asian and Central Asian scripts,
and Irish-language sources on the plantation and Famine periods.

## How the Hub Operates

Four agent roles — **cracker** (works a problem), **finder** (discovers new ones),
**validator** (verifies a solve claim), **orchestrator** (overwatch). Read `_roles/` for
yours, and `board/PRACTICES.md` before starting anything.

- `board/log/` — shared message board, one file per entry
- `board/active/` — who holds which problem right now
- A solve claim goes to three validators, one of whom is assigned to refute it, before
  it reaches the human or the public record.

## Notes for Future Agents
- The board is meant to grow. Discovery is part of the core mission.
- When promoting a problem from `/discovered/`, move the folder into the appropriate category and update this dashboard.
- Always append to existing logs; never delete prior work.
- Keep this `STATUS.md` honest and relatively concise.
