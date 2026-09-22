# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-21, orchestrator pass (VENONA panel run after 15 days queued; three proposals promoted; the Shakespeare correction carried into four handovers; delivery gap re-measured).

## Operating design — 2026-09-13

[Adaptive Research Practice](board/IMPROVEMENT.md) is installed by user direction:
bold leaps, decisive checks, compact handovers and proportionate validation.
ARP-001 is registered for explicit opt-in; no evaluated runs or performance gain yet.
This policy update does not change the research dispositions below or restart routines.

## Board state

**The delivery problem is still the board's biggest problem, it is not a research problem,
and this pass has new data on it: the gap is no longer confined to the Codex lane.**

Since the last pass (2026-09-17 10:14 UTC) the repository received research commits in
exactly two windows — the Proto-Elamite face-confound audit on 09-17 evening and the
Shakespeare period-detrend session on 09-21 morning. Both were excellent. Between them,
**twelve scheduled cracker firings at the documented six-hour cadence landed nothing**
(09-18 06:32 through 09-21 00:32), the daily orchestrator routine landed nothing on 09-18,
09-19 or 09-20, and the Friday 09-18 finder landed nothing. One cracker firing on 09-18
00:33 wrote a claim file and no folder commit at all; the 09-21 session correctly detected
it by the folder rule and retook the claim. That detection is the claim protocol working
as designed and is the one piece of good news in this paragraph.

The externally-run GPT-5.6 Codex lane (committing as `AlexFitzgerald47`) has landed **no
research commit since 2026-09-08** — thirteen days. Its last activity of any kind was
merging two finder PRs on 09-17, and the PR queue is empty this pass, so it is not
contributing by that route either.

This is the **fourth** consecutive pass to record the same thing, and it was escalated to
the human as a decision on 2026-09-17. It is not re-litigated here; what is added is that
the silence now covers all three routines rather than one lane, which points at the
scheduler or the environment rather than at any single prompt. See `board/SCHEDULE.md`.

**Claim hygiene is now good and should be left alone.** Every claim opened since 09-17 was
released by its own session in the same commit that landed the work. `board/active/` is
empty and correct at the time of this pass. No stale claim needed clearing — the first pass
since 09-05 that can say so.

**PR queue: empty.** Nothing to review, nothing merged, nothing rejected.

**Three proposals promoted out of `discovered/`** into the folders crackers actually read,
each leaving a `MOVED.md` stub: **1641 Depositions → `ireland/`** (rated Excellent, and
`ireland/` is the coldest category on the board), **Thera eruption date** and **Caligula's
seashells → `historical-controversies/`**. All three are well-formed with pre-registered
success criteria. Caligula in particular has been recorded as "cheapest start on the board,
still untouched" by three consecutive passes; promoting it is that decision being made
rather than noted a fourth time.

**One connection carried, and it changes a folder's stated position.** The 2026-09-21
Shakespeare session showed that a measured confound gap can be *corrected*, not just
measured — and that the detrending which corrects it rescales the metric badly enough to
invert a headline margin. It wrote both results to `board/log/` and updated `STATUS.md`,
but the four other folders the results bear on had nothing in their `HANDOVER.md` files.
Those cross-references are now written into Junius, Linear A, Voynich and Proto-Elamite.
The Junius consequence is the large one: that folder declares itself evidence-blocked
pending archival text, and the cheaper route is a compute session on the corpus it has
already built and committed. See
`board/log/2026-09-21-connection-correctable-confound-and-rescaled-metrics.md`.

**No new solve is approved by this pass.** See `board/log/2026-09-21-orchestrator-pass.md`.

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
| Proto-Elamite | `historical-texts/proto-elamite/` | Open — **constraint set re-tiered and audited 2026-09-17**; unclaimed | The 2026-09-04 pipeline reproduces exactly. Seven of the eight numeral constraints survive a null blocking on `(tablet, face)`, not just tablet. Three are load-bearing (M297–N39B, M263–N01, M263–N30C: pass in every powered holdout bucket); the rest are power-limited leads. **M288–N45 is untestable, not refuted** — its face-blocked test has a p-value floor of 0.12 and cannot fire. The M297 family merge was audited and upheld (M297 vs M297~B homogeneous, p = 0.0757/0.6941/0.1377). Face gap is 0.41× the sign signal corpus-wide, but M297 is the most face-skewed sign in the corpus. Recommended experiments 1 and 4 are now closed out — read `HANDOVER.md` before redoing either. See `attempts/2026-09-17-exact-form-and-face/RESULTS.md` |
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
| 1641 Depositions (quantitative) | `ireland/1641-depositions-quantitative/` | Open – **never worked**; promoted out of `discovered/` 2026-09-21 | The board's highest-tractability untouched problem: 19,010 pages transcribed and openly accessible from TCD, and the dispute genuinely unresolved. The difficulty is **double-counting and hearsay propagation**, not arithmetic — an entity-resolution problem with a pre-registered success criterion that explicitly permits "no estimate is supportable" as an answer. No archival dependency, no fetch dependency beyond the corpus |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| VENONA BROWN / BRAUN identity | `historical-controversies/venona-brown-braun/` | Open — provisional identification, validation pending | Current claimant lead is Frederick William Meredith for BROWN and Wilfrid Vernon for POULTRY-DEALER; supersedes Fraser-first routing. Literal covername mapping, exact 1940 residence and direct contact evidence remain missing. Read current handover and Meredith dossier; no identification approved. |
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open — **register gap confirmed independent of period, and substantially corrected, 2026-09-21**; unclaimed | The 2026-09-17 register result reproduces byte-identically and its distance cells stand. Three things changed this pass. (1) **Period and register are two confounds, not one**: detrending raises the author cost 32.11 -> 49.50 Delta while the register cost *rises* 54.71 -> 57.64, and a year-permutation null shows the gain is real chronology (null author cost 31.63). (2) **The Lyly sink is not a training-size artefact** — 41 chunks per author for all 27 over 50 subsamples leaves it at 41.5% +- 3.0%; prose-ness and training size are both now refuted causes. (3) **The cross-register failure is largely correctable**: detrending plus author-blind register centring takes 27-candidate attribution from micro 0.141 to **0.358** (null p95 0.227, p = 0.000) and 8-candidate from 0.216 to 0.498, against a within-register reference of 0.740. "Uninterpretable" is right about the arguments as made, too strong about the method. **Unconfirmed on the only held-out register** (35 pageant chunks, p = 0.220) and fails for Greene and Middleton. Next: a 300+ chunk third-register holdout — that single item decides whether this is a general result. Still **do not run Oxford/Bacon/Derby**. See `attempts/2026-09-21-period-detrend-and-equal-n/RESULTS.md` |
| Letters of Junius — authorship | `historical-controversies/junius-letters-authorship/` | Open — **evidence-blocked, and the block is measured**; promoted out of `discovered/` 2026-09-17 | Corpus built and reproducible (Junius from two independent digitisations, 173 acknowledged Francis letters, 14 rival period authors). Pipeline validated: Junius vs Draper 0.970, Philo Junius placed with Junius 34/34. **The register gap exceeds the author signal**: same-author cross-register Delta 0.588 vs different-author same-register 0.471; cross-register attribution 0.108 against chance 0.125, within-register 0.848. Francis ranks 8th of 15 and **that ranking is evidence neither way**. Reopens on ≥8,000 clean words of Junius's private letters to Woodfall, or ≥20,000 words of acknowledged Francis in the public polemical register 1769–1775. **New, cheaper reopening route added 2026-09-21:** the Shakespeare folder has now *corrected* a register confound of the same shape rather than only measuring it — detrend against date and centre on the questioned register (author-blind), which took 27-candidate cross-register attribution from 0.141 to 0.358, p = 0.000. Junius's cross-register 0.108 against chance 0.125 is exactly the pattern that motivated it, the corpus is already built and committed, and the code transfers. Try this before waiting further on archival text. See `board/log/2026-09-21-confound-gaps-are-correctable.md` |
| Mesha Stele line 31 (BTDWD) | `historical-controversies/mesha-stele-line31/` | **HELD — awaiting human sign-off**; promoted out of `discovered/` 2026-09-17 | Three validator verdicts returned 2026-09-12, all PARTIAL. Balak rejected as an epigraphic reading. Not approved as a solve and not to be published as one. Decisive missing check: blind stroke comparison with genuine stone/squeeze independence |
| Thera eruption date | `historical-controversies/thera-eruption-date/` | Open – **never worked**; promoted out of `discovered/` 2026-09-21 | Published radiocarbon determinations, re-analysable under current calibration; the dispute was still live as of 2025. The success criterion targets **prior sensitivity in the Bayesian model**, which is where much of the disagreement hides and is frequently under-reported. Second item: whether the 2025 Ahmose dates resolve the discrepancy or transfer it into Egyptian chronology |
| Caligula's seashells | `historical-controversies/caligulas-seashells/` | Open – **worked 2026-09-22; verdict reached against Woods (2000)**, unclaimed | Full-corpus *musculus* inventory built over 21.3M tokens (Latin Library + Perseus): 101 hand-classified attestations. The *musculi* misreading is philologically **weaker** than the literal reading — shellfish sense is 5.9%, the military sense never leaves technical literature and never takes a gathering verb, `conchas legere` is an attested idiom a century earlier (Cicero, Val. Max.), and Dio's independent Greek is κογχύλια not the ambiguous μῦς. Better mechanism: assimilation to the Scipio/Laelius shore-gathering topos. Corrections: Vitruvius does **not** use *musculus* (PROBLEM.md wrong); Aurelius Victor is not an independent witness. Next: read Woods's own text (does it defuse the *galeas/sinus replere* objection?) and Malloch CQ 2001. See `attempts/2026-09-22-musculus-inventory/RESULTS.md` |

## Next-session priorities

**Read this first if you are a cracker:** `ciphers/` and `ireland/` have not had a session
since 2026-09-08 — thirteen days — and every problem in them is unclaimed. The two folders
that *have* moved (Shakespeare, Proto-Elamite) are both well past the cheap wins. The board
is not short of work; it is short of sessions that land. A session that ends without a
commit has produced nothing.

1. **Junius — the cheapest high-value item on the board, and it is a compute session, not
   an archival wait.** This folder declares itself evidence-blocked pending ≥8,000 words of
   Junius's private correspondence. On 2026-09-21 the Shakespeare folder *corrected* a
   register confound of the same shape rather than only measuring it — detrend against date,
   then centre author-blind on the questioned register — taking 27-candidate cross-register
   attribution from micro 0.141 to 0.358 (p = 0.000). Junius sits at 0.108 against chance
   0.125, which is exactly the pattern that motivated the correction, and its corpus is
   already built and committed. **Step one is nearly free:** tabulate where the existing
   cross-register attributions pile up. Collapse onto one or two of the fifteen candidates
   means a removable shared displacement; even scatter means the signal really is gone and
   the archival condition is the only route. The handover now carries the full recipe and
   its three pitfalls.

2. **Shakespeare — a 300+ chunk third-register holdout, and nothing else.** Items (a) and
   (b) were done on 2026-09-21 and (b) changed the answer: period and register are
   **independent** confounds, the Lyly sink is **not** a training-size artefact, and the
   cross-register failure is **largely correctable**. The result is established on the arm
   it was developed on and unvalidated elsewhere — the pageant holdout is 35 chunks with no
   power (p = 0.220). Widening `build_corpus.py`'s author list to the 19 dramatists
   currently contributing no non-dramatic text is a one-line change plus a re-fetch, and
   that single experiment decides whether this folder has a positive methodological result
   or a corpus-specific one. Still **do not run Oxford/Bacon/Derby**.

3. **1641 Depositions — newly promoted, never worked, and the best-tractability problem on
   the board.** 19,010 transcribed pages, openly accessible, no archival or fetch
   bottleneck. The problem is entity resolution over hearsay propagation, and its success
   criterion explicitly allows "no estimate is supportable" as a passing answer, so a
   careful negative result is a win here rather than a disappointment. It also puts a
   session into `ireland/`, the coldest category on the board.

4. **Caligula's seashells — newly promoted, and the cheapest start anywhere.** A bounded
   Latin-corpus inventory of *musculus*/*musculi* in the military-technical sense, then a
   philological judgement on the Suetonius passage against it. One session, no dependencies.

5. **Validation — the queue, not more solve language.** VENONA's panel ran this pass after
   fifteen days queued, and the Ennis panel is now complete. The remaining unpanelled
   bounded claims are Linear A and Byblos; take them in that order.

6. **Debosnys — unclaimed, and untouched since 09-11.** Confirm XP glyph identity against
   the scan, freeze the key, test additional occurrences; seek independent plaintext
   confirmation. Use the handover routing note. Two consecutive sessions claimed this and
   produced nothing; if you claim it, commit something or release it.

7. **Linear A:** run the same-scribe cross-class self-match before the out-of-sample test,
   then the Scribe-9 grammar out of sample; resolve A-DU polarity and the HT85/HT122
   reconciliation. The 2026-09-21 cross-reference adds the step *after* that measurement —
   a wide gap is no longer a reason to stop — and the scale-free reporting rule.

8. **Voynich:** acquire exact ordered historical degree lists and the replication package;
   Taurus fit → Gemini/Cancer hold-out. Tabulate which source entries the labels land on,
   not just the alignment score — the sink check is now in the handover. Do not revive the
   withdrawn golden-cell argument.

9. **Ennis:** physical loop traversal from the captured 2023 photogrammetry/RTI. No more
   word search until that bottleneck changes — all three validators say the same thing.

10. **Byblos:** read `PARTIAL_BIGRAPH_KERNEL.md` and `ME_ANCHOR_TRANSFER.md`, which postdate
    the handover. Validate cylinder alignment and normalisation before extending conditional
    ME/T values.

11. **Proto-Elamite — worked 2026-09-17.** The constraint set is tiered by robustness and
    the folder's cheapest decisive item is a *block-aware split* that would settle M288–N45
    one way or the other. Two of its five standing recommended experiments are closed and
    should not be repeated — the handover says which and why.

12. **Fresh Irish cipher lane:** Crelly 1648–49 is the strongest of the three discovery
    packs, but all three need a solution-status audit before a cracker session, not after.
    The Maltravers pack in the same batch was withdrawn because someone else had already
    solved it — check `board/EXTERNAL_RESEARCH_INDEX.md` before opening any cipher target.

13. **Thera eruption date — newly promoted.** Prior sensitivity in the Bayesian
    radiocarbon model is the target, not another recital of the high/low chronology debate.

**Categories going cold.** `ireland/` has had no session since 2026-09-08 and now holds six
problems, three materially advanced, one newly promoted and excellent, all unclaimed — the
coldest category relative to its depth, and it has been the coldest for three passes.
`ciphers/` is cold for a different reason: Dorabella and CD 286 are genuinely
archive-blocked, so part of its idleness is real rather than neglect — but Debosnys,
Kryptos, Beale B3, `VORFYDCGT` and Voynich are not blocked and have not moved in thirteen
days. `historical-controversies/` is the best-stocked lane for a text-and-compute session
with no archival dependency, and now holds the two cheapest unworked problems on the board.

**Held but not progressing:** nothing, this pass — `board/active/` is empty and every
recent claim was released by its own session. The problem is not held-and-idle, it is
unheld-and-idle.

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

There are **18** problem packs under `discovered/` after this pass's three promotions, plus nine `MOVED.md` stubs marking problems that now live in a category folder. Physical location does not imply “unworked.” Full discovery provenance:
`discovered/_manifest/swarm-discovery-2026-09-04.md` and
`discovered/_manifest/discovery-2026-09-04-run2.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06); Junius and Mesha line 31 →
`historical-controversies/`, Byblos → `historical-texts/` (2026-09-17) — those three had
had full cracker sessions while sitting in a folder this repository defines as holding
*unworked* proposals, which misled every agent that read the dashboard. **2026-09-21: 1641
Depositions → `ireland/`; Thera eruption date and Caligula's seashells →
`historical-controversies/`** — these three are promoted on the opposite ground, that they
are well-formed, high-tractability and *unworked*, and were being passed over in
`discovered/` pass after pass. Each promoted folder leaves a one-line `MOVED.md` stub so a
resuming session cannot recreate it in the wrong place; delete the stub once the problem has
had a session at its new path.

**Deliberately not promoted, and not to be re-litigated:**

- **`discovered/short-cipher-validation-bound/` stays permanently.** It is a
  methodological asset, not a problem with a named unknown, so no category folder is
  right for it, and eight cracker-owned handovers cite the path. Its real defect was
  invisibility, which is fixed: it is now cited directly in `board/PRACTICES.md`.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
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
