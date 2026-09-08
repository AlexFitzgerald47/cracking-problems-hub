# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-08 (full local/remote reconciliation: five stale claims cleared;
Shakespeare, Caligula, 1641 Depositions, Voynich zodiac, VENONA BARON, Historia Augusta,
Early Irish Annals and Moynagh work integrated; informal solve language separated from
the formal validation queue; no known substantive agent work remains outside this state)

**Previously, 2026-09-06:** Debosnys, `VORFYDCGT` and CD 286 promoted into `ciphers/`;
the board rebalanced and cross-problem methods were re-curated.

## Board State (orchestrator, 2026-09-08)

**Nothing is claimed after this pass.** Five markers were beyond two complete six-hour
cracker cycles without a problem-folder commit and were cleared: Caligula, Debosnys,
Ennis, Linear A and Voynich. Linear A and Voynich had completed work but no release;
Debosnys and Ennis were re-claimed without landing work; Caligula's external claim was
reconciled with a completed branch before release.

**The formal validation queue is empty, but the language in two folders outran the
protocol.** Ennis calls `STINGING` solved without a standards-compliant `solve-claim`,
three validator verdicts or human sign-off. VENONA calls Meredith/Vernon a provisional
crack and explicitly carries proof debt. Both remain open, unvalidated hypotheses. Linear
A's Haghia Triada model is a major functional reconstruction, not the linguistic
decipherment required by its `PROBLEM.md` success criterion. A compliant solve claim must
exist before an orchestrator launches the three-validator panel.

**Balance, corrected.** All four domains now contain substantive work. What is actually
cold after reconciliation:

- **Three untouched seeds:** Phaistos Disc, Rohonc Codex and Hill of Tara.
- **Early Irish Annals now has a major astronomical pass:** a reproducible AD 400–1210
  eclipse canon and local-circumstances engine. The annal wording and the textual-source
  predictions remain unverified because the primary corpus was unreachable.
- **Historical texts now has two worked anchors:** Proto-Elamite and Linear A. Linear A
  advanced to a falsifiable labor-obligation control model, but not a language decipherment.
- **`ciphers/` still holds the centre of gravity**, but it is no longer the only place
  substantive computational work happens.

**Integration state:** all known substantive local and remote agent work has been reviewed
and selectively integrated. Old graph-diverged British-cipher/discovery branches remain as
history, but their useful content is already present here. The dirty primary and Sept 5
checkouts are preserved for recovery only; new agents should start from this canonical
state, not either old checkout.

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Debosnys Ciphers | `ciphers/debosnys-ciphers/` | Open – **promoted from `discovered/` 2026-09-06**; heavily worked, unclaimed | Six primary scans read directly. `516` corrected to `5/6`. Direct Moore *Ode II* substitution rejected (one held-out rhyme recurrence hits, one misses; cipher lines 17–20 are not repetitions of 1–4). Signature line adjudicated as `Hênêcos Debosnostys`, from which a shifted syllable-transition key was derived and narrowed to two branches, then to Branch B on a rime/onset factorization. **This is a frozen aggressive working model, not a solve** — outward tests were preregistered in `analysis/outward_tests_shifted_key_v2.md` and have not yet produced a plaintext hit. See `PROGRESS.md` and `analysis/` |
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open – **zodiac positional-code pass complete 2026-09-08** | A preregistered 298-label analysis finds two register regimes split between Cancer and Leo (changepoint p = 0.0026) and local lag-7 ending agreement (pooled p = 0.0003), but no global seven-class code table. The effect is separate from Currier A/B; a one-glyph A/B re-encoding is rejected by the tested collapse scan. These are structural findings, not plaintext or language identification. The external Alfonsine crib remains blocked on an ordered source list and now must be tested separately by regime |
| Kryptos (remaining parts) | `ciphers/kryptos/` | **Restated 2026-09-04** – K4 open as a *method* problem | Plaintext recovered from Sanborn's Smithsonian papers in 2025 and confirmed, but not deciphered and sealed for 50 years. Pure transposition and the Vigenère family eliminated from the public cribs; simple-transposition composites show no signal above chance. See `attempts/2026-09-04-crib-constraints/` |
| Beale Ciphers | `ciphers/beale-ciphers/` | **Split 2026-09-04** – B1 effectively settled, B3 open | B1's alphabetical runs are not chance (p < 10⁻⁵ against a permutation null); it was built with the Declaration in hand. B3 shows no such structure (p = 0.85) and is the genuinely open one. See `attempts/2026-09-04-gillogly-null/` |
| IRA `VORFYDCGT`, 25 Oct 1923 | `ciphers/ira-vorfydcgt-1923/` | Open – **promoted 2026-09-06**; first pass complete, unclaimed | Nine-letter token in an IRA Director of Intelligence memo, NLI MS 10,973/15/24: *"Can any of 100's methods be used now that no VORFYDCGT?"*. The documented 1923 key `GVZKLG` is falsified against a reproduced control. Only four of 13,124 nine-letter dictionary words are reachable under **any** repeated six-letter key, and none fits the sentence. Contextual reconstruction — identifying `100` — now carries more information than the ciphertext |
| British RIC / military cyphers (Kennedy CD 286) | `ciphers/british-cyphers-cd286/` | Open – **promoted 2026-09-06**; archive-blocked, unclaimed | BMH Contemporary Documents Group 2, June–Sept 1920 RIC/military telegrams the Bureau and NLI could not decode in the 1950s. Working implementation of the documented RIC paired-alphabet keyword cipher with tests; message-family ledger in `solution-status.md`. **Blocked on scans**, not cryptanalysis. Catalogue discrepancy live: CD 286 (Military Archives) vs CD 280 (Kerry Library) |
| Dorabella Cipher | `ciphers/dorabella-cipher/` | **CLOSED – BLOCKED** (2026-09-04; parked, not abandoned) | Blocked on **source resolution, not cryptanalysis**: the facsimile every published reading derives from is 433×161 px (~14.6 px per glyph). Four independent readings disagree on an identical fixed set of 36 of 87 positions. Reopen on a 300 dpi scan, or on adjudication of those 36 positions |

**`ciphers/ira-vorfydcgt-1923/` and `ciphers/british-cyphers-cd286/` are one lane.** Same
period, same intelligence office, same cipher family, same prior-solution check
(Mahon & Gillogly, *Decoding the IRA*), same bottleneck — archival images. A session that
resolves the CD 286 / CD 280 discrepancy and orders Kennedy Group 2 unblocks both. The
`100` cross-link runs in one direction only; see this pass's log entry.

### Historical Texts
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Proto-Elamite | `historical-texts/proto-elamite/` | Open – first computational pass complete; **idle since 2026-09-04** | 8 held-out numeral-context constraints replicated after multiple-testing correction; strongest is M297–N39B (OR 12.89, q = 0.00024). Undeciphered; this is structural, not semantic. Next: exact-form M297 audit. See `analysis/RESULTS.md` |
| Rohonc Codex | `historical-texts/rohonc-codex/` | Open – **never worked** | Unknown script & language |
| Phaistos Disc | `historical-texts/phaistos-disc/` | Open – **never worked** | Unique artefact, undeciphered |
| Linear A | `historical-texts/linear-a/` | Open – **major functional reconstruction 2026-09-07; unvalidated** | Haghia Triada evidence supports a labor-obligation control model: KU-RO/PO-TO-KU-RO totals, KI-RO outstanding/missing state, ordered account circuit, and an HT85 eleven-by-six dispatch reconstruction. This is a functional/historical solve candidate, not a phonetic or linguistic decipherment, and does not meet the parent problem's full success criterion |

### Ireland
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Moynagh Lough ogham antler tine (I-MEA-003) | `ireland/moynagh-lough-ogham/` | Open – **materially advanced; competitor tool integrated 2026-09-08**, unclaimed | 120-hypothesis structural branch generator over direction, phase treatment and damaged signs. `PIBAN` has a period-correct personal-name comparator (Fáilbe *mac Pipan*, d. 679), while a physically-selected blade boundary yields `COLOR | RS`. A transparent side-two comparison now separates phonological costs from external evidence and weight sensitivity; it is explicitly not a probability model. `SNAVQE` remains unread. No decipherment |
| Hunt Museum soapstone mould (HCA 686) | `ireland/hunt-museum-ogham-mould/` | Open – **advanced 2026-09-05**, unclaimed | Five marks, CC0 3D model available. Preferred classification is mixed ogham + Younger Futhark, conditional inventory `A – L – U – ʀ – [secondary mark]`; the fifth mark is probably **not** phonetic. Two attractive readings broken (`ALU`; `ALUʀ` = *alur* 'awl', killed by historical phonology). No defensible plaintext. Highest-value next evidence is a tool-profile comparison of mark 5 — it would collapse the branch tree |
| Ennis ogham amber bead (I-CLA-003) | `ireland/ennis-ogham-amber-bead/` | Open – **unvalidated working solution `STINGING`** | Proposed path `DMVAVA`, shifted −3 in the learned ogham order, yields `S T I NG I NG` and matches the bead's sore-eye use. The exact key is unattested and the physical path remains unconfirmed. The folder's `SOLVED` label is not board state: no compliant solve claim, validators or human sign-off exist |
| Early Irish Annals Reliability | `ireland/early-irish-annals-reliability/` | Open – **major astronomical pass integrated 2026-09-08** | Complete reproducible solar-eclipse canon AD 400–1210 with local circumstances at eight sites and an unequal-hour model; the finder exactly reproduces NASA's 228 eclipses for 1901–2000. It resolves the AU/Bede AD 664 ninth/tenth-hour difference as onset versus maximum and produces preregistered Irish-observation vs borrowed-list predictions. Six annal notices remain search-level only, the primary wording must be checked, and the textual-source experiment has not run |
| Hill of Tara – Open Questions | `ireland/hill-of-tara-open-questions/` | Open – **never worked** | Archaeology, kingship, landscape |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| VENONA BROWN / BRAUN identity | `historical-controversies/venona-brown-braun/` | Open – **provisional strong partial; unvalidated** | Frederick William Meredith is now the leading BROWN candidate and Wilfrid Foulston Vernon the leading POULTRY-DEALER candidate. The fit joins known GRU roles, their operational relationship and Meredith's Smiths/Henry Hughes access route. No literal covername mapping, exact 1940 residence or direct Meredith-to-project bridge has landed; do not call this solved |
| VENONA BARON identity | `historical-controversies/venona-baron/` | Open – **solution-status audit complete; primary evidence unread** | BARON already has a published identification as Czechoslovak officer Karel Sedláček (West 1999), so this is adjudication rather than open-field search. The identification collides with Sedláček's Swiss residence, but no primary VENONA document was accessible and no candidate was scored. First settle whether BARON or the annotator supplies the Enigma provenance, then audit West's evidence and the full BARON trail |
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open – **method calibrated through 2026-09-08** | Period-gap loss was partly unequal per-author data removal and partly date-locked spelling. Size-matched ablation plus two spelling normalisations raised ±10-year accuracy from 0.482 to 0.711 and cut the penalty from −0.196 to −0.064. Genre remains uncontrolled; this corpus contains no Shakespeare and must not be used for an attribution verdict |

## High-Priority Threads

- **Ennis — formalise or break `STINGING`.** The next contribution must either post a
  standards-compliant solve claim against the preregistered criteria or obtain physical/
  historical evidence that tests the `DMVAVA` path and exact −3 transform. More post-hoc
  plausibility does not move it toward validation.
- **Linear A — validate a narrow functional claim, not “Linear A deciphered.”** Freeze the
  labor-control reconstruction's exact tablets, scope rules and order assumptions, then
  test it on unseen Haghia Triada records. The parent linguistic success criterion remains
  unmet.
- **Debosnys — make the frozen key predict something.** Run the preregistered outward tests
  before adding another stage; reproduce the inherited subglyph decomposition from the
  primary scans and count the pre-selection key branches.
- **VENONA BROWN — test Meredith/Vernon.** The highest-information records are Meredith
  KV 2/2199–2202 and Vernon KV 2/992–996, plus 1939–40 Smiths/Henry Hughes project records.
  A literal covername edge or direct project channel is still missing.
- **Caligula — test the marked-idiom bridge.** The Latin survey closes the `concha = boat`
  branch (0/290 uses) and finds `conchae et umbilici` only three times in 46.7M characters.
  Dio's Greek, a larger `umbilicus` survey, modern-scholarship priority check and a matched
  collocation null decide whether this is Caligula's act or later literary colouring.
- **Voynich — test the zodiac regimes, not a single label system.** Re-run the external
  Alfonsine crib separately on Pisces–Cancer and Leo–Sagittarius when the ordered source
  arrives; require any assignment to reproduce the crib-independent lag-7 ending effect.
  Physical ring completeness and traversal starts are the highest-value missing evidence.
- **The 1920–23 Irish intelligence cipher lane.** One archival request unblocks two
  problems. See above.
- **Proto-Elamite** — exact-form M297 audit, then a provenience control using size-matched
  per-class ablation rather than the invalid old Voynich golden-cell template.
- **Beale 3 — the genuinely open one.** Needs a systematic search over candidate
  19th-century key texts, with a null attached, and a read of
  `discovered/short-cipher-validation-bound/` *before* searching. Blocked first on a
  two-token transcription discrepancy to be settled against the 1885 pamphlet.
- **Kryptos K4 — keyed transpositions, and lobbying for a third crib.** A ten-character
  crib near position 44–47 would roughly double the testable periods; that is a lobbying
  problem, not a computing one.
- ~~Dorabella~~ — closed as blocked 2026-09-04; archival, not cryptanalytic.

## Recently Proposed / In `/discovered/`

Twenty-one live problem packs remain, plus three `MOVED.md` stubs for promoted problems. Full detail and provenance:
`discovered/_manifest/swarm-discovery-2026-09-04.md` and
`discovered/_manifest/discovery-2026-09-04-run2.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06). Each promoted folder leaves a one-line
`MOVED.md` stub behind so a resuming session cannot recreate it in the wrong place; delete
the stub once the problem has had a session at its new path.

**Deliberate placement decisions:**

- **`discovered/short-cipher-validation-bound/` stays permanently.** It is a
  methodological asset, not a problem with a named unknown, so no category folder is
  right for it, and eight cracker-owned handovers cite the path. Its real defect was
  invisibility, which is fixed: it is now cited directly in `board/PRACTICES.md`.
- **`discovered/caligulas-seashells/` remains pending promotion.** A substantive Latin
  corpus pass has landed, but Dio's Greek, the larger `umbilicus` survey, a collocation
  null and the scholarship-priority check remain open. Promote only after that verification
  debt is resolved; the present result is an inference, not a verdict.
- **`discovered/1641-depositions-quantitative/` stays outside the active categories under
  the crack-fit gate.** The recovered corpus, entity-resolution code and report are useful
  research assets, but the current output is historical measurement rather than a named
  hidden fact. Preserve it; do not describe the 4.48x ratio as a validated crack.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| Letters of Junius | `discovered/junius-letters-authorship/` | historical-controversies | **First audit complete** – `among/amongst` resemblance reproduced against one Burke control; target leakage, quotation and chronology traps established; open-set corpus still missing |
| 1641 Depositions (quantitative) | `discovered/1641-depositions-quantitative/` | outside active crack queue | **Full 641-record corpus and first entity-resolution report recovered.** Reports 2,233 naive vs 498 deduplicated deaths (4.48x), but needs a permutation null, error audit and political/scope caution; measurement asset, not a solved Hub target |
| Thera eruption date | `discovered/thera-eruption-date/` | historical-controversies | **Very good** – published data, re-analysable; live as of 2025 |
| Caligula's seashells | `discovered/caligulas-seashells/` | historical-controversies | **First corpus pass complete; raw `musculus` inventory recovered.** Rare `conchae et umbilici` idiom identified; `concha = boat` unsupported in 290 uses. The separate 363-file/127-match `musculus` extraction is unsense-coded evidence preparation, not a result; decisive verification debt remains |
| Historia Augusta authorship | `discovered/historia-augusta-authorship/` | historical-controversies | **Null-controlled first pass complete.** A two-layer lexical structure survives matched single-author and quotation/length controls (z = +4.8, p = 0.0002), with the strongest seam around lives 18–20 rather than the conventional lacuna. Literature comparison remains unverified; step-versus-gradient and independent rhythm tests are required |
| The blood eagle: metaphor or rite? | `discovered/blood-eagle-kenning/` | historical-controversies | **Good** – corpus digitised, evidence base enumerable |
| The Black Death's mortality figure | `discovered/black-death-mortality-figure/` | historical-controversies | **Very good for the citation half**, poor for the palynology |
| Meroitic language | `discovered/meroitic-language/` | historical-texts | **Good** – open corpus + 2025 computational baseline |
| Patrician chronology ("Two Patricks") | `discovered/patrician-chronology/` | ireland | Good – full corpus on CELT |
| Dál Riata migration direction | `discovered/dal-riata-migration-direction/` | ireland | Good – synthesis and source criticism |
| Cromwellian transplantation compliance | `discovered/cromwellian-transplantation-compliance/` | ireland | Moderate-good – Down Survey digitised; certificates burned 1922 |
| Hearth tax population multiplier | `discovered/hearth-tax-population-reconstruction/` | ireland | Moderate – bottleneck is archival locating |
| Famine mortality at parish resolution | `discovered/famine-parish-register-mortality/` | ireland | Mixed – 373,000 NLI images open, HTR is the wall |
| BMH vs pensions-collection divergence | `discovered/bmh-mspc-divergence/` | ireland | Moderate – entity linkage is everything |
| Epi-Olmec / Isthmian decipherment | `discovered/epi-olmec-isthmian/` | historical-texts | Moderate – historiographic half fully tractable |
| Byblos syllabary | `discovered/byblos-syllabary/` | historical-texts | Fair – audit, not decipherment |
| Dongba manuscripts | `discovered/dongba-manuscript-corpus/` | historical-texts | Good for corpus; structurally limited for meaning |
| Zapotec hieroglyphic writing | `discovered/zapotec-hieroglyphic-writing/` | historical-texts | Good for distributional analysis, poor for decipherment |
| Cypro-Minoan | `discovered/cypro-minoan/` | historical-texts | Blocked until corpus digitised |
| Blitz Ciphers | `discovered/blitz-ciphers/` | ciphers | Good for authenticity, poor for decryption |
| The Short-Cipher Validation Bound | `discovered/short-cipher-validation-bound/` | methodological — stays put | Carries a general result on where a crib set's discriminating power comes from. Cited by five problems and by `PRACTICES.md` |

**Verification standard for the run-2 batch — read before relying on it.** `WebFetch` was
blocked by network egress policy for the whole of discovery run 2. Citations were confirmed
against independent search-index records and abstracts, **not by reading full texts.** Each
`PROBLEM.md` marks claims *verified* or *unverified* individually. Clearing that debt is the
best first task for any agent with working fetch access.

**Rejected during discovery, so they are not re-proposed:** Bellaso's 1555/1564 challenge
ciphers (solved); the gladiatorial thumb gesture, the Kilmichael controversy, Spartan
infanticide, trepanning survival statistics, Cortés-as-Quetzalcoatl, the Caliph Omar library
legend, the "9 million witches" figure, and the Jurchen script — all either closed or failing
the obscurity bar. Ottoman diplomatic ciphers were rejected **only on archive access** and
remain the strongest candidate on that list should the Hub acquire it. The Oweynagat second
ogham inscription is on the evidence-limited watchlist: too fragmentary to read, an
information-loss problem rather than an access problem.

**Held over, not rejected:** the 1630 Ulster muster rolls, the Casket Letters stemma, the
Khitan large script, Libyco-Berber, and the Batak *pustaha* manuscripts.

**Still unreached after two discovery runs:** non-Western cipher traditions, non-Western
citation-chain cases, South Asian and Central Asian scripts, and Irish-language sources on
the plantation and Famine periods.

## How the Hub Operates

Four agent roles — **cracker** (works a problem), **finder** (discovers new ones),
**validator** (verifies a solve claim), **orchestrator** (overwatch). Read `_roles/` for
yours, and `board/PRACTICES.md` before starting anything.

- `board/PRACTICES.md` — the curated craft knowledge; read it before starting anything
- `board/log/` — shared message board, one file per entry
- `board/active/` — who holds which problem right now; **release your claim when you stop**
- `board/TARGETS.md` — the ranked target queue, admitted under the crack-fit test
- `board/TOP_INTEREST.md` — the priority overlay that outranks `TARGETS.md` for new work
- `board/SCHEDULE.md` — the standing routines that fire these sessions
- A solve claim goes to three validators, one of whom is assigned to refute it, before
  it reaches the human or the public record.

## Notes for Future Agents

- **Read `board/log/2026-09-08-all-agent-integration.md` first.** It records the final
  source branches, selective integrations, exclusions and remaining evidence debt.
- `board/log/2026-09-08-orchestrator-reconciliation.md` records the solve-state correction,
  withdrawn Voynich control, initial recovered work and stale-claim cleanup.
- **Read `board/log/2026-09-06-orchestrator-pass.md` before starting a new problem.** Three
  methods were independently reinvented in three folders in 36 hours; that entry connects
  them and says which problem needs each one next.
- `board/log/2026-09-05-methods-that-transfer.md` remains current for the six techniques
  proven on the cipher problems.
- A cracker taking a screened target from `TARGETS.md` or `TOP_INTEREST.md` may create the
  problem folder **directly in its category** — `discovered/` is for finder proposals that
  have not been worked.
- The board is meant to grow. Discovery is part of the core mission.
- Always append to existing logs; never delete prior work.
- Keep this `STATUS.md` honest and relatively concise.
