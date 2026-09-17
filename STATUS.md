# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-17, cracker session (Shakespeare register self-match test run; negative result).

## Operating design — 2026-09-13

[Adaptive Research Practice](board/IMPROVEMENT.md) is installed by user direction:
bold leaps, decisive checks, compact handovers and proportionate validation.
ARP-001 is registered for explicit opt-in; no evaluated runs or performance gain yet.
This policy update does not change the research dispositions below or restart routines.

## Board state

**The delivery problem is now the board's biggest problem, and it is not a research problem.**
Between 2026-09-08 23:44 UTC and 2026-09-17 06:34 UTC — nine days, roughly 36 scheduled
cracker firings — the repository received **no research commits at all**. The only things
landed in that window were one orchestrator pass (09-11), one policy commit (09-12), and a
Debosnys claim on 09-14 that produced zero commits and then fenced the problem off for three
days. Every problem folder in `ciphers/`, `historical-texts/`, `ireland/` and
`historical-controversies/` was frozen at 2026-09-08 until this pass.

The lane that did nearly all the September 8 work — the externally-run GPT-5.6 Codex
sessions, which commit as `AlexFitzgerald47` — has delivered nothing since. The Claude
cracker lane delivered its first session on 2026-09-17 (Junius) and delivered it well.
This has now been observed by three consecutive orchestrator passes (09-12, 09-13, 09-17)
and **cannot be resolved from inside the repository**: the routine prompts and their
enabled/failed state live outside it. It is escalated to the human as a decision, not
recorded as deferred a fourth time. See `board/SCHEDULE.md`.

Two open pull requests were cleared this pass, both merged: #7 (three Irish-connected
cipher discovery packs, with the Maltravers target correctly self-closed as externally
solved) and #8 (`board/EXTERNAL_RESEARCH_INDEX.md`, an external-scoop watchlist).

One stale claim cleared: **Debosnys** — claimed 2026-09-14, folder last touched 2026-09-11,
no commits in the intervening three days. Crashed session; released.

Three worked problems promoted out of `discovered/`, which the repository's own convention
reserves for *unworked* finder proposals: **Junius** and **Mesha line 31** →
`historical-controversies/`, **Byblos** → `historical-texts/`. Each leaves a `MOVED.md` stub.

**No new solve is approved by this pass.** See `board/log/2026-09-17-orchestrator-pass.md`.

## Active Problems

### Ciphers
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| Debosnys Ciphers | `ciphers/debosnys-ciphers/` | Open — outward prediction, unconfirmed | Latest analysis predicts poem #4 L3/L4 terminal XP → /kos/ using the shared key, not Branch B alone. This is a conditional model application, not independently confirmed plaintext. Read `analysis/2026-09-08-xp-outward-crack.md` and the XP script; a new handover routing note points to both. **Claim released 2026-09-17** — the 2026-09-14 session left a claim and no commits. Unclaimed and available |
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
| Byblos syllabary | `historical-texts/byblos-syllabary/` | Open — conditional partial results, **unvalidated**; promoted out of `discovered/` 2026-09-17 | Partial-bigraph inventory split and ME anchor transfer, worked through 2026-09-08. `PARTIAL_BIGRAPH_KERNEL.md` and `ME_ANCHOR_TRANSFER.md` postdate the handover — read them first. Validate cylinder alignment and normalisation before extending conditional ME/T values. Panel pending |

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
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open — **register self-match test run and failed, 2026-09-17**; unclaimed | Two confounds now measured in this folder. Period carries ~half the authorial signal (0.824 → 0.475, 2026-09-05). **Register is larger than the signal**: same author across registers sits at Delta 470.5, different authors within one register at 447.9. Cross-register attribution collapses onto a sink — 59.4% of all non-dramatic chunks went to Lyly, 14 of 27 dramatists absorbed nothing, and on held-out civic pageants Middleton recovered 0 of his own 12, Heywood 0 of 8, Jonson 0 of 5. Both registers built from EEBO-TCP through one pipeline, so this is not an edition artefact; a same-play two-pipeline control sits at 5.3% of the between-author distance. **Do not run the Oxford/Bacon/Derby comparison** — it crosses exactly this gap. Next: regress period out and re-run, and subsample training sets to equal size before quoting the sink figures. See `attempts/2026-09-17-register-self-match/RESULTS.md` |
| Letters of Junius — authorship | `historical-controversies/junius-letters-authorship/` | Open — **evidence-blocked, and the block is measured**; promoted out of `discovered/` 2026-09-17 | Corpus built and reproducible (Junius from two independent digitisations, 173 acknowledged Francis letters, 14 rival period authors). Pipeline validated: Junius vs Draper 0.970, Philo Junius placed with Junius 34/34. **The register gap exceeds the author signal**: same-author cross-register Delta 0.588 vs different-author same-register 0.471; cross-register attribution 0.108 against chance 0.125, within-register 0.848. Francis ranks 8th of 15 and **that ranking is evidence neither way**. Reopens on ≥8,000 clean words of Junius's private letters to Woodfall, or ≥20,000 words of acknowledged Francis in the public polemical register 1769–1775 |
| Mesha Stele line 31 (BTDWD) | `historical-controversies/mesha-stele-line31/` | **HELD — awaiting human sign-off**; promoted out of `discovered/` 2026-09-17 | Three validator verdicts returned 2026-09-12, all PARTIAL. Balak rejected as an epigraphic reading. Not approved as a solve and not to be published as one. Decisive missing check: blind stroke comparison with genuine stone/squeeze independence |

## Next-session priorities

**Read this first if you are a cracker:** every problem below except Junius has been idle
since 2026-09-08. The board is not short of work, it is short of sessions that finish. A
session that ends without a commit has produced nothing, and a claim left behind fences a
problem off for days — that is exactly what happened to Debosnys between 09-14 and this pass.

1. **Shakespeare register self-match test — DONE 2026-09-17, and the answer is no.**
   The stylometric side of the Oxford/Bacon/Derby debate is **uninterpretable**, not
   merely weak: the register gap it must cross is wider than the author signal, and
   dramatists cannot recover their own out-of-register work. Two follow-ups are now the
   cheap high-value items, both with the code already written — (a) regress period out
   and re-run, which decides whether this folder's two measured confounds are one
   effect or two, and (b) subsample every author's plays to equal size, which decides
   how much of the sink is centroid noise. See that folder's `HANDOVER.md`.
2. **Validation before more solve language.** Ennis panel ran this pass (see the queue
   below). **VENONA is next and is not to be deferred again** — it has been queued since
   2026-09-06 with zero verdicts. Then the bounded Linear A and Byblos claims.
3. **Debosnys — unclaimed again.** Confirm XP glyph identity against the scan, freeze the
   key, test additional occurrences; seek independent plaintext confirmation. Use the
   handover routing note. Two consecutive sessions have now claimed this and produced
   nothing; if you claim it, commit something or release it.
4. **Linear A:** run the same-scribe cross-class self-match before the out-of-sample test,
   then the Scribe-9 grammar out of sample; resolve A-DU polarity and the HT85/HT122
   reconciliation. The cross-reference at the top of its `HANDOVER.md` says why the order
   matters.
5. **Voynich:** acquire exact ordered historical degree lists and the replication package;
   Taurus fit → Gemini/Cancer hold-out. Do not revive the withdrawn golden-cell argument.
6. **Ennis:** physical loop traversal from the captured 2023 photogrammetry/RTI. No more
   word search until that bottleneck changes — the validator panel says the same thing.
7. **Byblos:** read `PARTIAL_BIGRAPH_KERNEL.md` and `ME_ANCHOR_TRANSFER.md`, which postdate
   the handover. Validate cylinder alignment and normalisation before extending conditional
   ME/T values.
8. **Proto-Elamite** is unclaimed, idle since 2026-09-04, and one of the most tractable
   starts available: the exact-form M297 audit, reported alongside a cross-class
   self-distance.
9. **Fresh Irish cipher lane:** Crelly 1648–49 is the strongest of the three new discovery
   packs, but all three need a solution-status audit before a cracker session, not after.
   The Maltravers pack in the same batch was withdrawn because someone else had already
   solved it — check `board/EXTERNAL_RESEARCH_INDEX.md` before opening any cipher target.
10. **Balanced fresh work:** Caligula remains a bounded, untouched corpus question. Sidetic
    still has no landed problem pack.

**Categories going cold.** `ireland/` has had no session since 2026-09-08 and holds five
problems, three of them materially advanced and all five unclaimed — it is the coldest
category relative to its depth. `ciphers/` is cold for a different reason: Dorabella and
CD 286 are genuinely archive-blocked, so its idleness is partly real rather than neglect.
`historical-controversies/` just gained three folders and is the best-stocked lane for a
text-and-compute session with no archival dependency.

Archive-blocked lanes remain Dorabella and CD 286. Do not reuse Voynich's withdrawn
example as a validated control design.

## Validation queue

| Claim | Current disposition | Decisive missing check |
|---|---|---|
| Mesha BTDWD / House of David | 3 × PARTIAL — HELD, not validated as a full solve | Blind stroke comparison and genuine stone/squeeze independence |
| Ennis STINGING | Awaiting three-validator panel | Full physical traversal and complete search budget |
| VENONA Meredith / Vernon | Awaiting three-validator panel | Dated primary documentary links and competing candidates |
| Linear A labor-liability dossier | Bounded functional candidate; panel pending | Hold-out structure, semantic polarity, novelty versus prior scholarship |
| Byblos inventory split / anchor transfer | Bounded conditional candidate; panel pending | External name alignment, raw glyph identity and inventory sensitivity |

## Recently Proposed / In `/discovered/`

There are 22 problem packs under `discovered/` after this pass's three promotions and three additions, including the methodological asset and worked candidates. Physical location does not imply “unworked.” Full discovery provenance:
`discovered/_manifest/swarm-discovery-2026-09-04.md` and
`discovered/_manifest/discovery-2026-09-04-run2.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06); **Junius and Mesha line 31 →
`historical-controversies/`, Byblos → `historical-texts/` (2026-09-17)** — all three had
had full cracker sessions while sitting in a folder this repository defines as holding
*unworked* proposals, which misled every agent that read the dashboard. Each promoted folder leaves a one-line
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
| Dongba manuscripts | `discovered/dongba-manuscript-corpus/` | historical-texts | Good for corpus; structurally limited for meaning |
| Zapotec hieroglyphic writing | `discovered/zapotec-hieroglyphic-writing/` | historical-texts | Good for distributional analysis, poor for decipherment |
| Cypro-Minoan | `discovered/cypro-minoan/` | historical-texts | Blocked until corpus digitised |
| Blitz Ciphers | `discovered/blitz-ciphers/` | ciphers | Good for authenticity, poor for decryption |
| Crelly 1648–49 coded correspondence | `discovered/crelly-1648-coded-correspondence/` | ciphers | **New 2026-09-17.** Casway's 1978 edition describes an undeciphered passage; exact letter, shelfmark, ciphertext length and modern solution status all unverified. Strongest of the three: a same-date Antrim letter gives a parallel account |
| Ormond–Anglesey 1663–64 partial cipher | `discovered/ormond-anglesey-1663-cipher/` | ciphers | **New 2026-09-17.** Partial key known (E=13/14, THE=246). The volume-5 p.498 pointer is not yet proved to belong to this exchange — resolve that before any cracker session |
| Ormonde–Maltravers 1634–35 cipher | `discovered/ormonde-maltravers-1634-cipher/` | **CLOSED — solved externally** | Daniel Bourdeau published a reading of both letters, reported to Cryptiana 2026-09-16. The finder pass caught this itself and withdrew the candidate. Folder retained as the audit trail. Only residual: nomenclator values 185 and 149 in one clause. **Do not re-propose** |
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
