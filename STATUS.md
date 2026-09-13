# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-12, orchestrator reconciliation.

## Operating design — 2026-09-13

[Adaptive Research Practice](board/IMPROVEMENT.md) is installed by user direction:
bold leaps, decisive checks, compact handovers and proportionate validation.
ARP-001 is registered for explicit opt-in; no evaluated runs or performance gain yet.
This policy update does not change the research dispositions below or restart routines.

## Board state

Latest research commit observed: `2a29cf1`, 2026-09-09 03:44 UTC. No subsequent research commits were present at the pre-edit fetch. This establishes repository inactivity, not the status of external schedulers.

Four abandoned reservations cleared: Debosnys and Byblos landed work but left claims; Caligula landed no research; Sidetic left a claim without creating its problem folder. No cracker is reserved by this pass.

The September 6 dashboard was materially stale. Linear A, Ennis, Byblos and Mesha now have substantial work; Voynich has withdrawn its old controlled-language claim and moved to an ordered zodiac test. **No new solve is approved by this pass.**

See `board/log/2026-09-12-orchestrator-pass.md` for the audit and next-session handover. The previous dashboard is preserved in `board/log/2026-09-12-dashboard-before-reconciliation.md`.

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Debosnys Ciphers | `ciphers/debosnys-ciphers/` | Open — outward prediction, unconfirmed | Latest analysis predicts poem #4 L3/L4 terminal XP → /kos/ using the shared key, not Branch B alone. This is a conditional model application, not independently confirmed plaintext. Read `analysis/2026-09-08-xp-outward-crack.md` and the XP script; a new handover routing note points to both. |
| Voynich Manuscript | `ciphers/voynich-manuscript/` | Open — corrected and redirected | September 6 audit withdrew the claim that the golden cell controls physical section: illustration class is not quire, and A blocks repeat one folio. Plant-label fit failed held-out (117/120). Next: frozen Tankalusha/Alfonsine degree-list extraction; fit Taurus, predict Gemini/Cancer. See current `HANDOVER.md`. |
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
| Linear A | `historical-texts/linear-a/` | Open — functional reconstruction candidate | Scribe-9 labor-liability dossier; KI-RO scalar/block grammar and HT87/HT117 roster relationship. Literal meanings and integrated administrative interpretation remain hypotheses. A-DU polarity is unresolved in the latest handover; do not inherit the older “fulfilled” gloss as settled. Not a language decipherment. |

### Ireland
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Moynagh Lough ogham antler tine (I-MEA-003) | `ireland/moynagh-lough-ogham/` | Open – **materially advanced 2026-09-05**, unclaimed | 120-hypothesis structural branch generator over direction, phase treatment and damaged signs. Two results worth keeping: `PIBAN` has a period-correct personal-name comparator (Fáilbe *mac Pipan*, d. 679), a serious alternative to Stifter's common-noun *pípán*; and a physically-selected phase boundary from a reported finer blade yields `COLOR | RS`. `SNAVQE` remains unread. No decipherment |
| Hunt Museum soapstone mould (HCA 686) | `ireland/hunt-museum-ogham-mould/` | Open – **advanced 2026-09-05**, unclaimed | Five marks, CC0 3D model available. Preferred classification is mixed ogham + Younger Futhark, conditional inventory `A – L – U – ʀ – [secondary mark]`; the fifth mark is probably **not** phonetic. Two attractive readings broken (`ALU`; `ALUʀ` = *alur* 'awl', killed by historical phonology). No defensible plaintext. Highest-value next evidence is a tool-profile comparison of mark 5 — it would collapse the branch tree |
| Ennis amber bead | `ireland/ennis-ogham-amber-bead/` | Open — STINGING candidate, validation pending | −3 shift works on selected DMVAVA, but current scholarly reading remains ?DMVA?VA and loop traversal is unresolved. The latest handover replaces the simple-fork model with a cycle. Next: captured 2023 photogrammetry/RTI and blind traversal audit. |
| Early Irish Annals Reliability | `ireland/early-irish-annals-reliability/` | Open – **never worked** | Chronology & source criticism |
| Hill of Tara – Open Questions | `ireland/hill-of-tara-open-questions/` | Open – **never worked** | Archaeology, kingship, landscape |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| VENONA BROWN / BRAUN identity | `historical-controversies/venona-brown-braun/` | Open — provisional identification, validation pending | Current claimant lead is Frederick William Meredith for BROWN and Wilfrid Vernon for POULTRY-DEALER; supersedes Fraser-first routing. Literal covername mapping, exact 1940 residence and direct contact evidence remain missing. Read current handover and Meredith dossier; no identification approved. |
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open – **never worked** | Evidence evaluation |

## Next-session priorities

1. **Validation before more solve language.** Mesha three-reader review this pass; next panels: Ennis, VENONA, then the bounded Linear A and Byblos claims. Their existing interpretations remain candidates, not approved discoveries.
2. **Debosnys:** confirm XP glyph identity against the scan, freeze the key, test additional occurrences; seek independent plaintext confirmation. Use the new handover routing note.
3. **Voynich:** acquire exact ordered historical degree lists and the actual replication package; Taurus fit → Gemini/Cancer hold-out. Do not revive the withdrawn golden-cell argument.
4. **Linear A:** test the Scribe-9 account/status/unit grammar out of sample; resolve A-DU polarity and the HT85/HT122 entity-level reconciliation.
5. **Ennis:** physical loop traversal from known captured surface data; no more word search until that bottleneck changes.
6. **Byblos:** read `PARTIAL_BIGRAPH_KERNEL.md` and `ME_ANCHOR_TRANSFER.md`, which postdate the handover. Validate cylinder alignment and normalization before extending conditional ME/T values.
7. **VENONA:** documentary Meredith/Vernon chronology and contact tests; no generic candidate restart.
8. **Balanced fresh work:** Caligula remains a bounded, untouched corpus question. Sidetic has no landed problem pack; recreate from the screened target only after primary-source access is checked.

Archive-blocked lanes remain Dorabella and CD286; Proto-Elamite remains available for exact-form M297 audit. Do not reuse Voynich's withdrawn example as a validated control design.

## Validation queue

| Claim | Current disposition | Decisive missing check |
|---|---|---|
| Mesha BTDWD / House of David | 3 × PARTIAL — HELD, not validated as a full solve | Blind stroke comparison and genuine stone/squeeze independence |
| Ennis STINGING | Awaiting three-validator panel | Full physical traversal and complete search budget |
| VENONA Meredith / Vernon | Awaiting three-validator panel | Dated primary documentary links and competing candidates |
| Linear A labor-liability dossier | Bounded functional candidate; panel pending | Hold-out structure, semantic polarity, novelty versus prior scholarship |
| Byblos inventory split / anchor transfer | Bounded conditional candidate; panel pending | External name alignment, raw glyph identity and inventory sensitivity |

## Recently Proposed / In `/discovered/`

There are 21 problem packs under `discovered/`, including the methodological asset and worked candidates. Physical location does not imply “unworked.” Full discovery provenance:
`discovered/_manifest/swarm-discovery-2026-09-04.md` and
`discovered/_manifest/discovery-2026-09-04-run2.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06). Each promoted folder leaves a one-line
`MOVED.md` stub behind so a resuming session cannot recreate it in the wrong place; delete
the stub once the problem has had a session at its new path.

**Deliberately not promoted, and not to be re-litigated:**

- **`discovered/short-cipher-validation-bound/` stays permanently.** It is a
  methodological asset, not a problem with a named unknown, so no category folder is
  right for it, and eight cracker-owned handovers cite the path. Its real defect was
  invisibility, which is fixed: it is now cited directly in `board/PRACTICES.md`.
- **`discovered/caligulas-seashells/`** — earned nothing yet; the 2026-09-05 claim
  produced no work. Still the cheapest historical-controversy start on the board.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| Letters of Junius | `discovered/junius-letters-authorship/` | historical-controversies | **Very good** – corpus public; Ellegård (1962) never redone |
| 1641 Depositions (quantitative) | `discovered/1641-depositions-quantitative/` | ireland | **Excellent** – 19,010 pages digitised; entity-resolution problem |
| Thera eruption date | `discovered/thera-eruption-date/` | historical-controversies | **Very good** – published data, re-analysable; live as of 2025 |
| Caligula's seashells | `discovered/caligulas-seashells/` | historical-controversies | **Good** – cheapest on the board to start |
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
| Byblos syllabary | `discovered/byblos-syllabary/` | historical-texts | Worked through September 8: conditional partial-bigraph inventory split and ME transfer; unvalidated |
| Mesha Stele line 31 | `discovered/mesha-stele-line31/` | historical-controversies | BTDWD claim: three PARTIAL verdicts; held, not approved |
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

- **Read `board/log/2026-09-12-orchestrator-pass.md` first, then the September 6 historical transfer note.** Three
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
