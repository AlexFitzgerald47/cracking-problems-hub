# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-04 (Proto-Elamite first computational pass completed; discovery run 2 – 10 further problems proposed, 21 now in `/discovered/`; four cipher problems worked — Dorabella closed as blocked, Kryptos K4 restated, Beale split, Voynich A/B confound resolved)

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open – **first attempt logged 2026-09-04** | Currier A/B shown not to be a scribal artefact: it survives holding scribe and section constant (p < 0.0002). Section effects are as large as language effects, which argues against reading "language" literally. See `attempts/2026-09-04-hand-language-confound/` |
| Kryptos (remaining parts) | `ciphers/kryptos/` | **Restated 2026-09-04** – K4 open, but as a *method* problem | Plaintext recovered from Sanborn's Smithsonian papers in 2025 and confirmed, but not deciphered and sealed for 50 years. Pure transposition and the Vigenère family (incl. Beaufort) now eliminated from the public cribs; simple-transposition composites show no signal above chance. See `attempts/2026-09-04-crib-constraints/` |
| Beale Ciphers | `ciphers/beale-ciphers/` | **Split 2026-09-04** – B1 effectively settled, B3 open | B1's alphabetical runs are not chance (p < 10⁻⁵ against a permutation null); it was built with the Declaration in hand. B3 shows no such structure (p = 0.85) and is the genuinely open one. See `attempts/2026-09-04-gillogly-null/` |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | **CLOSED – BLOCKED** (2026-09-04; parked, not abandoned) | Blocked on **source resolution, not cryptanalysis**: the facsimile every published reading derives from is 433×161 px (~14.6 px per glyph). Four independent readings disagree on an identical fixed set of 36 of 87 positions. Reopen on a 300 dpi scan, or on adjudication of those 36 positions. See `attempts/2026-09-04-transcription-uncertainty/` |

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
- **Voynich — are the A→B and Herbal→Biological axes parallel?** Section effects match
  language effects in size. If the two directions are close to parallel, the "two languages"
  framing is probably wrong and both are topic or register effects. A few lines on top of the
  existing decomposition.
- **Beale 3 — the genuinely open one.** The hoax evidence that settles B1 does not touch B3,
  and B3 does not decode to English with the Declaration. Needs a systematic search over
  candidate 19th-century key texts, with a null attached. Blocked first on a two-token
  transcription discrepancy to be settled against the 1885 pamphlet.
- **Kryptos K4 — keyed transpositions, and lobbying for a third crib.** Single-stage families
  and simple-transposition composites are both exhausted from the public cribs (no signal
  above chance across 12,901 hypotheses). A ten-character third crib near position 44–47 would
  roughly double the number of testable periods; that is a lobbying problem, not a computing one.
- Rohonc Codex script analysis
- ~~Dorabella~~ — closed as blocked 2026-09-04; archival, not cryptanalytic. Reopens on a
  300 dpi scan or adjudication of 36 named positions.

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

### Four cipher problems – 2026-09-04

Worked in one session; every result carries a Monte Carlo null and reproducible code.
Attempt folders sit under each problem's `attempts/`.

- **Dorabella — closed as blocked.** Not a cryptanalysis problem. The facsimile every
  published reading derives from is 433×161 px (~14.6 px per glyph) and cannot be read;
  four independent readings disagree on an identical fixed set of 36 of 87 positions, of
  which eight do most of the damage. Also established that at n=87 a wrong key outscores
  the true key 46.7% of the time on known-key English, and that 13 mutually unrelated
  messages beat the best published claim — so no monoalphabetic solution can be certified
  by fit alone at this length.
- **Kryptos K4 — restated and narrowed.** The board asked for the plaintext; it was
  recovered from Sanborn's Smithsonian papers in 2025, confirmed, and sealed. The open
  problem is the method. Pure transposition eliminated by a letter count; the Vigenère
  family eliminated at every period the cribs can see; 12,901 transposition-composite
  hypotheses show no signal above chance. Produced the crib-power rule now promoted to
  `discovered/short-cipher-validation-bound/`.
- **Beale — the problem splits.** B1's alphabetical runs are not chance (longest run 17
  against a null of 3.87 ± 0.76, null max 10, p < 10⁻⁵); inside the runs the word numbers
  jump across the whole Declaration, the signature of a searcher rather than a scanner.
  B2, a genuine message on the same key, scores 3 — the control the argument always needed.
  B3 shows nothing (p = 0.85) and is now the live thread.
- **Voynich — Currier A/B is not a scribal artefact.** Hand 1 wrote 112 of the 114
  Language A pages, so A/B is confounded with both scribe and section. Hand 3's Stars
  pages break both confounds and the difference survives: 12.76 against a null of 5.53,
  p < 0.0002. But section effects match language effects in size, which is the loose thread.
- **Failures preserved:** the Dorabella log records a budget-matching error that made an
  early comparison meaningless; the Kryptos log records a period-19 "lead" withdrawn once
  133 transpositions were tested; the Voynich log keeps an uncontrolled first pass that
  reached the opposite conclusion.

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
| The Short-Cipher Validation Bound | `discovered/short-cipher-validation-bound/` | methodological | **Not empty** — carries its first general result: where a crib set's discriminating power comes from, and how to design crib placement. Below what length does a readable high-scoring decryption stop being evidence? Dorabella, Kryptos K4 and the Phaistos Disc all turn on it |

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
