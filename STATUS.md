# Cracking Problems Hub – Status Dashboard

**Last updated:** 2026-09-24, orchestrator pass (two rows on this page said "never worked" about problems worked the day before, and are corrected; the gold-bar solve-claim went to a three-validator panel; the two proposals the last pass committed to are promoted; three results carried into twelve handovers; `PRACTICES.md` recurated).

## Operating design — 2026-09-13

[Adaptive Research Practice](board/IMPROVEMENT.md) is installed by user direction:
bold leaps, decisive checks, compact handovers and proportionate validation.
ARP-001 is registered for explicit opt-in; no evaluated runs or performance gain yet.
This policy update does not change the research dispositions below or restart routines.

## Board state

**The board is working again, and the delivery problem has changed shape.** Four consecutive
passes recorded the same thing: scheduled sessions firing and landing nothing. That is no
longer what the log shows. Since the 2026-09-21 pass the repository has received **six
distinct research sessions in 48 hours** — Junius (09-21 evening), Thera (09-22), Caligula
(09-22), a finder gap-fill run (09-22), Early Irish Annals (09-23) and Shakespeare (09-23) —
each with committed code, data, a `FREEZE.md` where predictions were frozen, and a handover.
Three of them produced results general enough to change how other folders work. **The
delivery gap is not re-litigated this pass because it did not recur.** What it leaves behind
is a different problem: six sessions of method in two days, most of it stranded in the folder
that produced it. That is the work this pass did.

**The externally-run Codex lane has still landed no research commit since 2026-09-08** —
fifteen days — and the PR queue is empty again this pass, so it is not contributing by that
route either. This is now the only unexplained silence on the board and it is a standing
item for the human, escalated on 2026-09-17 and unchanged since.

**PR queue: empty.** Nothing to review, nothing merged, nothing rejected. Third consecutive
pass.

**Claim hygiene: good, and leave it alone.** `board/active/` is empty and correct. Every
claim opened since 09-17 was released by its own session in the commit that landed the work,
including the three opened since the last pass. No stale claim needed clearing and none was
cleared. The folder rule (`git log -1 -- <problem folder>`, not the claim file's date) did
not need to fire this pass.

**The dashboard was wrong about the board's stated top priority, and that is the most
important correction on this page.** The 2026-09-21 pass named Junius "the cheapest
high-value item on the board" and recommended a compute route past its archival block. The
Junius session ran that route to completion **the same evening** and closed it, with committed
evidence (`attempts/2026-09-21-shift-or-loss/`). The recommendation then sat at the top of
this file for two days. Any cracker who read the dashboard and not the handover would have
spent a full session re-running a closed experiment. **Where this file and a folder's
`HANDOVER.md` disagree, the folder wins** — now written into `PRACTICES.md` as a standing
rule.

**One live consequence of that, and it is an argument rather than a ruling.** The Shakespeare
ablation of 09-23 shows that *centring alone* is worse than doing nothing on both arms it has
been tested on, including the arm where the full two-step correction reaches 0.365. Junius
could not run the detrend half at all (its panel carries `period` as a volume-level range
string), so it ran the half that scores below nothing even where the treatment works. Its
readings 1–3 — the sink null, the bootstrap instability, the 0.214 leave-one-author-out shared
fraction — are untouched and the compute route stays closed. **Reading 4 should be withdrawn
as evidence.** One cheap untried form of the route survives: the same run showed the detrend
needs the questioned corpus's *period*, not per-document dates, so a volume-level range string
may be enough after all. Posted as an argument to the log, per `_roles/ORCHESTRATOR.md`; the
cracker who next holds Junius decides. See
`board/log/2026-09-23-connection-ablation-ceiling-and-label-permutation.md`.

**Two solve-claim panels were incomplete, and this file said one of them was finished.** The
09-21 pass recorded "the Ennis panel is now complete". It had two verdicts, not three. VENONA
had one. Both were completed this pass under `_roles/VALIDATOR.md` with the refuter assigned
explicitly, and **every verdict on this board is PARTIAL — there is no PASS anywhere.** The
Ennis panel is 3 × PARTIAL reached *independently*: its refuter read the other two only after
running the code and forming its own attack, and the three arrived by different roads — the
criteria, the evidence chain, and an attempt to kill it. That is worth more than the
agreement itself, and it is the answer to the correlated-error problem `_roles/VALIDATOR.md`
exists to address. VENONA returned 3 × PARTIAL: the panel's finding is not that Meredith is
contradicted but that he is **unevidenced and was never ranked against a field**, the field
having been closed by written instruction rather than exhausted, and the refuter built a
rival who beats him on the two clues the claim admits it cannot match. **No solve is approved
by this pass, nothing is published as solved, and all three held claims stop where they are
until the human signs them off.**

**Four proposals promoted out of `discovered/`,** each leaving a `MOVED.md` stub:
**patrician-chronology** and **dal-riata-migration-direction → `ireland/`**,
**blood-eagle-kenning → `historical-controversies/`**, **chinese-gold-bar-cipher →
`ciphers/`**. The two Ireland promotions are made on a specific ground rather than on their
tractability rating: the 09-23 Annals session committed a **13,414-row, four-witness CELT
entry table** with a validated parse-and-changepoint pipeline, and that artefact is the
*stated core deliverable* of patrician-chronology and directly bears on dal-riata. Both now
carry the pointer, and the Annals folder is told two problems depend on it.
`chinese-gold-bar-cipher` is promoted because `ciphers/` has had no unblocked new work in two
weeks and this is the only cipher on the board with a public, machine-readable corpus and no
archival dependency. `blood-eagle-kenning` is promoted because it has been rated "Good" and
passed over for five consecutive passes, which is the failure mode `_roles/ORCHESTRATOR.md`
names by name.


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
| Chinese gold bar cryptograms (1933) | `ciphers/chinese-gold-bar-cipher/` | **Worked 2026-09-24 — solve-claim posted, HELD pending three validators**; unclaimed | **Criterion 2 is met with margin and the claim is that there is no plaintext.** Across the complete 263-letter inventory **21 of 26 letters occur exactly ten times** (E=11, I=13, O=9, S=11, T=9); chi2 vs uniform = **1.251 on 25 df** against an expectation of 25, analytic P = **9.3e-13**. The set is not merely flat — the literature's unverified "very flat" claim, now confirmed as Pelling's and *superseded* — but **flatter than chance**, which no cipher can be: every cipher samples letters and even a one-time pad leaves chi2 ~= 25 +/- 7. Monoalphabetic substitution and transposition are excluded language-independently by IC (0.0397 vs 0.0606 English, 0.0739 romanized Chinese, both p = 0.0001; zero repeated trigrams where English predicts ~29). The balance holds **only on the deduplicated inventory** (per-bar subsets at CDF 0.30/0.25/0.0038/0.0019), which is not a physical object — so tooling explanations die structurally and the constraint sits at composition. Order structure is indistinguishable from a random deal of that pool on all eleven statistics. **Two stated limits:** the periodic tests are weak (period 5 separation only 1.9 s.e., a permanent bound at 263 letters), and one registered prediction (P-A) **failed** on the claimant's own design error. A deliberately flat homophonic cipher is recorded as the live steelman. Criterion 1 unmet and argued unreachable; criterion 3 materially advanced by an independent quantitative line. Next move is **image evidence, which this session did not touch at all**: 18 bar faces are public and only four are transcribed. See `attempts/2026-09-24-is-it-a-cipher/RESULTS.md` |
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
| Ennis amber bead | `ireland/ennis-ogham-amber-bead/` | **HELD — awaiting human sign-off**; 3 × PARTIAL, panel completed 2026-09-23 | Not a solve and not to be published as one. The −3 shift on the *selected* `DMVAVA` is arithmetically exact and **survived the refuter's attack**: expanded twelvefold to 480 cycle-model combinations across three lexicons it still yields exactly one English word and zero Irish words. What fails is everything around it. The scholarly reading is `?DMVA?VA`; the payload is that string with signs deleted, and no assignment of the deleted signs yields a word. Direction, start point and closure geometry are undetermined by the physical evidence; the −3 key is an acknowledged nonce; the post-medieval date is derived *from* the reading. **Three corrections the folder must carry.** (1) **The headline null figure is wrong and must stop being quoted.** "0.406 %, about 1 in 246" is the most favourable of *four* values now in the repo and does not reproduce; it is frozen-path, English-only and conditional on the deletion. The defensible figure, by exact enumeration over all 64,000,000 six-sign sequences under the 12-reading cycle budget with an English ∪ Irish lexicon, is **7.2 %, about 1 in 14** — and 31.5 % if charged for the affine family. (2) **The `VAVA repeated` falsifier is discharged, in the claim's favour** — the live OG(H)AM EpiDoc decomposes to exactly one FEARN+AILM pair, so the phrase means "VA, repeated from DMVA", not `VAVA` on the branch. Stop carrying it as the open kill test. (3) **New evidence against the historical bridge, from the claim's own cited source:** all 45 pages of Hayden & Stifter 2025 were read, and the attested nineteenth-century ogham ciphers contain **no positional rotation**, the Minchin charms carry no superimposed cipher, and the eye-charms are Irish prayers under `ar x` headings — a comparator predicting specifically *against* a bare English participle. "Cryptic healing ogham" is the dossier's construction, not an attested genre; `SOLUTION.md` §5's "operation class attested" should be downgraded. Next evidence is physical, not lexical: the captured 2023 photogrammetry/RTI and a blind traversal audit with the budget declared in advance. **No more word search** |
| Early Irish Annals Reliability | `ireland/early-irish-annals-reliability/` | **Worked 2026-09-23** — corpus and pipeline committed, one question answered negatively; unclaimed | `attempts/2026-09-23-iona-transition/data/entries_derived.csv` holds **13,414 entries across four witnesses** (Ulster, Tigernach, Inisfallen, Chronicon Scotorum) in one schema; `src/parse.py` and `src/changepoint.py` are reusable and the pipeline validates blind, recovering AU's +1 AD offset and three manuscript lacunae unprompted. **The raw CELT text is deliberately not committed** (marked `restricted`, translations in copyright) — derive, do not redistribute. Result: Scottish content in AU falls 6.51 % → 1.85 %, real (p = 0.0002), a step not a trend (p = 0.017), reproduced in Chronicon Scotorum (p = 0.0004). **The date is not resolved and should not be quoted:** the full tag puts the break at 808 and rejects 740 (p = 0.0097); excluding Iona by name puts it at 738 and rejects 808 (p = 0.012); the two are not distinguishable (label permutation p = 0.183). The gazetteer decides, not the annals. **Added 2026-09-24 by cross-reference:** the Patrician session extended your corpus (a Four Masters parser, 9,503 entries, reproducing your table byte for byte) and produced two things directly executable here — a **marker instrument** (87 hand-read alternative-source markers, precision 1.00, rate collapsing at a fitted changepoint of 663, LR 205.4 against max null 18.1, present in all four witnesses) which is a *second, independent* signal on your unresolved 738-vs-808 break; and a measured warning that **within-witness duplicate detection runs at ~1/15 precision on this corpus** while cross-witness matching audits 20/20 — do not write the former. See that folder and this folder's `HANDOVER.md` |
| Patrician chronology ("Two Patricks") | `ireland/patrician-chronology/` | **Worked 2026-09-23 — criterion 1 delivered; the sharp test was refuted by its own holdout**; unclaimed | **Do not rebuild the corpus or the collation; both exist.** `attempts/2026-09-23-annalistic-independence/` holds the criterion-1 collation (`data/patrician_dossier.tsv`), a parser for the Four Masters (9,503 entries, AD 1–1372) that reproduces the Annals folder's corpus byte for byte, and `RUN.md` reproduces everything in about a minute. **One solid result to build on:** the annals' alternative-source markers ("as some books state", "Or here", "I have found this in the Book of Cuanu") are 87 entries, all hand-read, precision 1.00, and their rate collapses at a fitted changepoint of **663** — LR **205.4** against a max null LR of 18.1 over 1000 label permutations, bootstrap CI 596–666, independently present in all four witnesses. That is a new, cheap instrument for dating the chronicle's transition to contemporary record, orthogonal to the scribal arguments normally used. **One result measured but not to be over-read:** Patrick's AU obit years 457/461/492/493 have gaps 4, **31**, 1 against 40 hand-verified alternative-dating clusters (median gap 4, max 25) — the measurement is right, the inference is not. **The headline claim was refuted by its own holdout and should not be revived without new evidence:** the Four Masters carries a *silent* 35-year duplication (Ceallach son of Raghallach, King of Connaught, at 703 and again at 738, where AU/AT/CS all give 705, with no marker), so gap magnitude alone does not discriminate a merged tradition from an unnoticed duplication. Two exposures stated in the handover: everything rests on CELT translations with no Latin/Irish original consulted, and the marker instrument is **translator-dependent** (57 markers in Mac Airt's Ulster against 8 in Stokes's Tigernach) — the four-witness *direction* survives, the cross-witness *magnitudes* should not be quoted. Next: freeze and test the one surviving asymmetry, and settle the Passion-era lead (AI 496.1's "432nd year from the Passion" + a Passion of AD 29 = 461, exactly AU's alternative), which if it checks out dissolves the annalistic bimodality entirely. Original promotion ground, still true: its success criterion 1, which its own `PROBLEM.md` calls "the core deliverable", is a full collation of fifth-century Patrician entries across the annalistic witnesses with stemmatic analysis of which are independent — and four of those witnesses are **already parsed and committed** by the Annals session above. Start from `entries_derived.csv`, not from CELT; the Four Masters is the one named witness still to add, which is a fetch and a parser. Inherit that corpus's stated tag assumptions, and expect the circularity to be the finding. Criterion 4 licenses "the evidence cannot discriminate" as a real result |
| Dál Riata migration direction | `ireland/dal-riata-migration-direction/` | Open — **never worked**; promoted out of `discovered/` 2026-09-23 | The Annals result above *is* on this axis and its code re-cuts by tag. The more valuable inheritance is the warning: that session's break date moved 70 years and flipped which published date the evidence rejects on **one defensible gazetteer decision**, with the two tag sets statistically indistinguishable. This folder's whole debate turns on which evidence counts as Irish and which as Scottish — same decision, same load-bearing position. Declare the attribution rule before measuring and report under at least two defensible tag sets; if they disagree, that is the finding |
| "The Night Before Larry Was Stretched" — authorship | `ireland/larry-was-stretched-authorship/` | Open — **never worked**; promoted out of `discovered/` 2026-09-24 | Promoted on the commitment the 2026-09-23 pass recorded, not on a fresh judgement: proposed 09-22, well-formed, still unworked, and that pass wrote "promote next pass if still unworked — that is a date, not a shrug". Who wrote the 1789 Dublin Newgate-cant execution ballad; unresolved since Farmer (1896) rejected the traditional attribution and named no author. **The order of work is not the obvious one and the handover says so: run the information-ceiling calculation *before* any stylometry.** A single short ballad against period candidates is exactly the short-text regime `discovered/short-cipher-validation-bound/` covers, and criterion 2 already licenses "structurally untestable by authorship methods" as the right answer. Then the confound: the candidates span a shoemaker-poet, a cathedral dean's formal prose and a barrister's oratory, against a questioned text in cant and ballad metre — **the widest register gap any folder on this board has faced**, wider than Junius, where the gap already exceeded the author signal. Score a candidate attested in both registers against himself before ranking anyone; if none is, that is the result |
| Hill of Tara – Open Questions | `ireland/hill-of-tara-open-questions/` | Open – **never worked** | Archaeology, kingship, landscape |
| 1641 Depositions (quantitative) | `ireland/1641-depositions-quantitative/` | Open — **corpus access blocked, measured 2026-09-23**; never worked | The tractability rating was wrong. Every path on `1641.tcd.ie` returns a reCAPTCHA page; **6,011 of 6,037 archived `deposition.php` captures are access-denied redirects**, dating back to the 2010 crawls, so Wayback reconstruction is measured and does not work; the IMC printed edition on the Internet Archive is lending-restricted. Two routes return bytes and neither carries testimony (archived `searchResults.php` metadata; Hickson 1884 extracts). The dispute is still open and the problem still belongs on the board, but the bottleneck is **an archive request to TCD, for a human to send**, not computation. See that folder's `HANDOVER.md` |

### Historical Controversies
| Problem | Folder | Status | Notes |
|---------|--------|--------|-------|
| VENONA BROWN / BRAUN identity | `historical-controversies/venona-brown-braun/` | **HELD — awaiting human sign-off**; three-validator panel completed 2026-09-23 | Meredith for BROWN and Vernon for POULTRY-DEALER. **No identification is approved** and none should be repeated as settled. The panel's load-bearing finding is that the candidate field was closed by written instruction rather than exhausted: `fraser-residence-kill-test.md` ends "BLOCKED / UNRESOLVED — not passed" yet Fraser was demoted the next day with no new evidence, the Barnard file's own prescribed program was dropped, and constraint-ledger Q2/Q3 — the two *small, enumerable* populations the cables actually name — were never run. The Smiths → Henry Hughes bridge establishes only employment somewhere in the S. Smith & Sons group, which every Hainault shop-floor employee satisfies better, and No. 976 points at the production line. Two textual corrections are settled and belong in `PROBLEM.md` and `constraint-ledger.md`: **"illicit *link*"**, not "ink", and the leak-reading of "a MUSIC from BROWN" — both *raise* the W/T bar. The refuter demonstrated the ranking failure rather than merely asserting it: **Oliver Green** (CPGB 1935, International Brigade, recruited by Soviet intelligence in Spain, London address 1939, ran unnamed factory sub-agents, caught 1942 with films of classified material) ties or beats Meredith on every dimension the claim evidences, and beats him decisively on the two clues the claim admits it cannot match. It also logged a **new primary constraint nobody had recorded**: London No. 798 §4 has STANLEY "looking for work on an agricultural farm near the MUSIC", so BROWN's July 1940 radio flat sat within working distance of farmland — which points back at the Essex end (Hainault in 1940 was farmland with the Hughes works in it) that the Meredith detour abandoned. Cheapest untried tests: ledger Q3 (name the Ilford/Hainault CPGB Area Secretary — one person) and Q2 (1939 Register roster for the Hughes works). The Vernon leg is weaker than validator 1 graded it and its central person-to-person bridge rests on a single source logged UNVERIFIED |
| Shakespeare Authorship | `historical-controversies/shakespeare-authorship/` | Open — **the cross-register correction is validated out of sample, 2026-09-23**; unclaimed | The 2026-09-21 correction generalises: on 496 non-dramatic chunks by **eleven dramatists who contributed none of the developed arm**, detrend + author-blind centring reaches micro **0.365** (p = 0.001, chance 0.037) against 0.358 on the arm it was developed on. Uncorrected 0.133; sink 33.1% → 17.5%. The folder's reopening condition is met. Three changes to the recipe, both arms: (1) the two steps are **inseparable** — each alone is worse than nothing (0.117 / 0.109 vs 0.133; 0.161 / **0.067** vs 0.141); (2) leave-one-work-out centring is unnecessary, the questioned arm's global mean matches it; (3) the detrend needs the questioned corpus's **period**, not per-document dates — dating every chunk at the arm mean costs 0.010, wrong per-document dates cost 0.041. Handover item 2 is **closed**: nothing predicts which authors recover, and once authors with too little text are dropped the test has no power (n = 10 needs |ρ| ≥ 0.636). Next: genre inside the register — the two failures are one prose romance and one hack's polemic. Still **do not run Oxford/Bacon/Derby**. See `attempts/2026-09-23-third-register-holdout/RESULTS.md` |
| Letters of Junius — authorship | `historical-controversies/junius-letters-authorship/` | Open — **evidence-blocked, and the block is measured**; promoted out of `discovered/` 2026-09-17 | Corpus built and reproducible (Junius from two independent digitisations, 173 acknowledged Francis letters, 14 rival period authors). Pipeline validated: Junius vs Draper 0.970, Philo Junius placed with Junius 34/34. **The register gap exceeds the author signal**: same-author cross-register Delta 0.588 vs different-author same-register 0.471; cross-register attribution 0.108 against chance 0.125, within-register 0.848. Francis ranks 8th of 15 and **that ranking is evidence neither way**. Reopens on ≥8,000 clean words of Junius's private letters to Woodfall, or ≥20,000 words of acknowledged Francis in the public polemical register 1769–1775. **The compute route recommended here on 2026-09-21 was run that evening and is CLOSED** — see `attempts/2026-09-21-shift-or-loss/` (`FREEZE.md` committed before any test ran; 30 s on the committed corpus). The gap on this corpus is a **loss**, not a shared displacement: the prediction sink does not collapse (observed concentration 0.341 sits *below* its own permutation null's 0.399 ± 0.098), the sink's identity is unstable across bootstraps, and **79 % of each author's register displacement is author-specific** (leave-one-author-out shared fraction 0.214; in-sample the same corpus reads 0.505 and would have said "go"). Do not re-run any centring variant without new evidence. **One reading is withdrawn and one cheap route survives, added 2026-09-23:** the Shakespeare ablation shows centring *alone* scores below doing nothing even where the full treatment works, so "both centrings failed" is not a fourth independent reading; and the detrend — untried here because the panel carries `period` as a volume-level range string — needs only the questioned corpus's *period*, not per-document dates (dating every chunk at the corpus mean costs 0.010). That is the only untried form of the route. Second item: derive the reopening word count from an information-ceiling calculation rather than asserting 8,000. See `board/log/2026-09-23-connection-ablation-ceiling-and-label-permutation.md` |
| The blood eagle: metaphor or rite? | `historical-controversies/blood-eagle-kenning/` | **Worked 2026-09-23 — the premise is measured and the verdict is *undecidable for a measurable reason***; unclaimed | **The problem is workable at hour one, not hour six:** the complete skaldic corpus is one shell script away (`analysis/code/FETCH_CORPUS.sh`), the pipeline runs in seconds, and the prose dossier is coded in `analysis/data/prose_feature_matrix.tsv`. **Central result: Knútsdrápa st. 1 is a hapax on every axis.** 0 of 772 beast-of-battle occurrences has the beast as agent of a blade verb; 1 of 21 `bak` occurrences involves a beast or a blade, and it is this one; and the corpus's actual carrion formula (`falla und ara greipar`, ≥4 poets) is not what Sigvatr wrote. **Frank's premise that the stanza is "a conventional utterance" fails at corpus level; her conclusion — no viking-age support outside the stanza — is right and now has a denominator.** Because a hapax cannot adjudicate itself the honest verdict is **undecidable, for a measurable reason: n = 1**. Priority for the underlying idea belongs to **Bjarni Einarsson (1986)**, not to this session. Two things to attack first, both flagged by the session itself: the **35-row blade co-occurrence adjudication is load-bearing and is one agent's judgement** (`analysis/data/beast_blade_adjudication.tsv`, a reason per row — if one row is really a beast governing a blade verb the headline moves from 0 to 1), and **finding (i) depends on the *Orkneyinga saga* passage being c. 1200–30 rather than a Flateyjarbók-stage interpolation**, the single most dangerous assumption in the files. Frank 1984 (EHR) remains unread; the argument is reconstructed from her 1988/1990 restatements. A three-hour result is available: *Speculum* 97:1 reports she supports the dative-of-agent reading with three prepositionless instrumental datives elsewhere in *Knútsdrápa* — one was checked and **its datives are instruments, not agents**; if all three are, her own syntactic support argues against her construal. The OCR question here is closed: two independent scans, every number computed twice, same answer. Original promotion ground, still true: "Good — corpus digitised, evidence base enumerable" and passed over for five consecutive passes, which is the failure mode `_roles/ORCHESTRATOR.md` names by name. The deliverable is two inventories — every occurrence of the eagle-tears-the-back image in skaldic verse with manuscript attestation, and every prose blood-eagle narrative with an argued judgement on whether it is independently attested or textually dependent — then a transmission map. Criterion 4 makes "the surviving text cannot decide this" a legitimate and likely outcome. The citation-chain method here is the same one `templo-mayor-1487-sacrifice-count` needs |
| Templo Mayor 1487 dedication sacrifice count | `historical-controversies/templo-mayor-1487-sacrifice-count/` | Open — **never worked**; promoted out of `discovered/` 2026-09-24 | Promoted on the commitment the 2026-09-23 pass recorded (proposed 09-22, well-formed, still unworked). Is the widely repeated 80,400 figure a transmitted count or a citation artefact — and are Ixtlilxóchitl and Mendieta independent witnesses or copying Durán? The second is a standard textual-filiation problem and is the actual target. **Two things on this board make it materially cheaper than when it was proposed**, which is why it goes now: `blood-eagle-kenning` worked this exact shape of problem on 09-23 and its audited-citation-chain method transfers directly, and the same session established that **archive.org usually holds two independent library scans of a public-domain edition** — close to load-bearing here, because a filiation argument built on one OCR pass of each chronicler is partly an argument about the scanner, and the object of study is a *numeral*. A third hypothesis the proposal does not list, added in the handover: 80,400 may be a **notation** artefact rather than an embellishment (structured Nahuatl reckoning), testable against how the same chroniclers render other large numbers |
| Mesha Stele line 31 (BTDWD) | `historical-controversies/mesha-stele-line31/` | **HELD — awaiting human sign-off**; promoted out of `discovered/` 2026-09-17 | Three validator verdicts returned 2026-09-12, all PARTIAL. Balak rejected as an epigraphic reading. Not approved as a solve and not to be published as one. Decisive missing check: blind stroke comparison with genuine stone/squeeze independence |
| Thera eruption date | `historical-controversies/thera-eruption-date/` | **Worked 2026-09-22** — the success criterion is answered and the answer is a bound; reasoning-ready, unclaimed | Calibration engine, OxCal-equivalent phase model and a validated pipeline are committed and rerun in minutes — **do not rebuild them**. The prior-sensitivity criterion is met and it is large: changing only the within-phase prior on Manning's 31 Akrotiri determinations moves the posterior median **1561 → 1618 BCE**. The deeper result is an information bound — IntCal20 is flat across **1610–1540 BCE** and the asymptotic d′ for 1610 vs 1560 is **0.19**, so no sample size resolves the plateau interior; the endpoints do separate (1620 vs 1530, ceiling 4.89). Bias-corrected by simulation, the evidence gives a 95.4 % support set of **1610–1560 BCE peaking near 1600**, reproducing Manning's published 95.4 % range by another route while his published 68.3 % range is ~3× too narrow. Reopening condition is specific: an annual-resolution curve whose 1610–1540 amplitude exceeds ~40 ¹⁴C yr. Ice cores and tephra geochemistry untouched |
| Caligula's seashells | `historical-controversies/caligulas-seashells/` | **Worked 2026-09-22** – corpus built, inventory complete, verdict delivered; open on the *reading* side | 120-token sense inventory of `muscul*` across ~19.3M words now in `data/`, rebuildable from `code/`. Verdict: the Latin does **not** support emending *conchae* — `conchas legere` is Cicero's own idiom (*De Or.* 2.22) and Tacitus uses it of gathering Ocean pearls in Britain (*Agr.* 12). **`PROBLEM.md` misattributed Woods's thesis** (huts = Balsdon 1934; Woods argues *boats*) — correction appended there. Woods's boat sense of *musculus* is unattested until c. AD 400. What remains is library access: Malloch *CQ* 2001 and the body of Woods 2000 are unread, so success criterion 3 is still open |

## Next-session priorities

**Read this first if you are a cracker.** The board is no longer short of sessions that land
— six landed in the last 48 hours. What it is short of is sessions that pick up what those
six left. Four problems now hold **committed, validated, reusable pipelines** that a
successor is told not to rebuild: Thera (calibration engine and phase model), the Annals
(four-witness entry table and changepoint machinery), Shakespeare (corpus builder and the
two-step correction), Junius (corpus and Delta pipeline). Reading the relevant `HANDOVER.md`
first is worth more here than it has ever been, and **where this page and a handover
disagree, the handover wins** — that rule exists because this page got its own top priority
wrong for two days.

1. **Templo Mayor and "Larry Was Stretched" — the two cheapest unworked starts, both promoted
   this pass, and each has the method it needs already built by another folder.** Templo Mayor
   inherits the audited-citation-chain method from `blood-eagle-kenning`, which ran that exact
   shape of problem on 09-23; both it and Larry inherit the second-scan replicate rule from the
   same session, and on Templo Mayor that is close to load-bearing because the object of study
   is a numeral read off OCR. Neither has an archival dependency and both have criteria that
   make a negative a passing result. **On Larry, run the information-ceiling calculation before
   any stylometry** — its handover explains why, and its criterion 2 already allows "structurally
   untestable" as the answer.

2. **Blood eagle — one three-hour result and one load-bearing thing to attack, and both are
   named.** This is now a *worked* folder, not a start, and its next session is cheap because
   the corpus and pipeline are committed. The three-hour result: Frank supports her
   dative-of-agent reading with three prepositionless instrumental datives elsewhere in
   *Knútsdrápa*; one has been checked and **its datives are instruments, not agents**, so if all
   three are, her own syntactic support argues against her construal. The thing to attack: the
   **35-row blade co-occurrence adjudication is one agent's judgement and the headline zero rests
   on it** — take the Old Norse, check each verdict against Finnur's facing Danish, and say
   plainly if any row is wrong. Second priority in that folder is dating the *Orkneyinga saga*
   passage, its most dangerous assumption.

3. **Patrician chronology — worked, and the next step is a freeze, not a rebuild.** Criterion 1
   is delivered and the corpus and collation exist; the marker changepoint at 663 (LR 205.4
   against max null 18.1, all four witnesses) is solid and is the folder's real asset. The
   headline gap argument was **refuted by its own holdout** — the Four Masters carries a silent
   35-year duplication — so do not revive it without new evidence. Two live routes, in order:
   freeze and test the one surviving asymmetry (a gap > 15 combined with an explicit
   alternative-date marker, Patrick excepted) across all clusters plus any new witnesses, since
   at n = 49 it has almost no power; and settle the **Passion-era lead**, where AI 496.1's "432nd
   year from the Passion" plus a Passion of AD 29 gives exactly AU's alternative 461 — if that
   checks out against early Irish computistical texts, the annalistic bimodality dissolves and
   there is no second Patrick in the annals at all. That is the highest-upside cheap check on
   the Irish lane.

4. **Thera — answered on its stated criterion; the next move is narrow and it is the only one
   that matters.** Do not re-run the prior sensitivity, it is done. The single live question is
   whether an annually-resolved calibration curve has real structure in 1610–1540 BCE that
   IntCal20's smoothing averages out. If it does, the information bound lifts and the eruption
   year becomes recoverable; if not, the bound is permanent and the dispute stops being a
   radiocarbon question. Reopening condition is quantified: amplitude above ~40 ¹⁴C yr.

5. **Shakespeare — genre inside the register, and nothing else.** The cross-register
   correction is now validated out of sample (0.365 on 496 chunks by eleven dramatists who
   contributed none of the developed arm, against 0.358 on the developed arm), and the
   ablation closed the outstanding recipe questions. The two remaining failures are one prose
   romance and one hack's polemic, which points at genre within register. Handover item 2 is
   **closed** — nothing predicts which authors recover, and once authors with too little text
   are dropped the test has no power (n = 10 needs |ρ| ≥ 0.636). Still **do not run
   Oxford/Bacon/Derby**.

6. **Junius — one cheap experiment, not a session's worth of work, and read the handover
   before you touch it.** The compute route is closed on three independent readings. The only
   untried form: the detrend needs the corpus's *period*, not per-document dates, so the
   volume-level range string the panel already carries may be sufficient. Pair it with an
   information-ceiling calculation to replace the asserted 8,000-word reopening threshold with
   a derived one. If the ceiling says the panel cannot separate Francis from fourteen rivals
   across the register gap at any word count, that is a publishable negative and it retires
   the problem honestly.

7. **Debosnys — unclaimed, untouched since 09-11, and the board's standing embarrassment.**
   Confirm XP glyph identity against the scan, freeze the key, test additional occurrences.
   Two consecutive sessions claimed this and produced nothing. If you claim it, commit
   something or release it.

8. **Linear A and Byblos — the two remaining unpanelled bounded claims**, in that order. Both
   carry new cross-references this pass: Linear A gets the label-permutation null for its
   post-hoc scribe/class decomposition, Byblos gets the information-ceiling calculation to run
   *before* extending any conditional ME/T value.

9. **Proto-Elamite — the block-aware split that would settle M288–N45.** Two of its five
   standing recommended experiments are closed; the handover says which. New this pass: carry
   the label permutation before interpreting any post-hoc face or block split, paired with the
   p-floor rule this folder itself established.

10. **Voynich:** acquire exact ordered historical degree lists; Taurus fit → Gemini/Cancer
   holdout. Tabulate which source entries the labels land on, not just the alignment score. Do
   not revive the withdrawn golden-cell argument.

11. **Ennis — physical, not lexical, and three documentary corrections come first.** All
    three validators agree the bottleneck is the captured 2023 photogrammetry/RTI and a blind
    traversal audit with the string budget declared in advance. **The "VA repeated" falsifier
    is now discharged** — it resolved in the claim's favour and is no longer the cheap kill
    test; do not re-run it. Before anything else, the folder needs its headline null figure
    replaced (0.406 % does not reproduce and is one of four values; the defensible figure is
    **7.2 %**, or 31.5 % charged for the affine family), and `SOLUTION.md` §5 downgraded in
    light of Hayden & Stifter 2025, which the refuter read in full and which argues against
    the historical bridge. Those are edits to a cracker-owned folder, so they need a cracker
    session, not an orchestrator.

12. **VENONA — two small enumerable populations, never run.** Constraint-ledger Q3 (the
    Ilford/Hainault CPGB Area Secretary — one person) and Q2 (the 1939 Register roster for the
    Hughes works). The panel's finding is that the candidate field was closed by instruction
    rather than exhausted; these are how it gets reopened. Carry the two settled textual
    corrections into `PROBLEM.md` and `constraint-ledger.md` first.

13. **1641 Depositions — do not take this as a compute session.** Measured 2026-09-23: 6,011
    of 6,037 archived `deposition.php` captures are access-denied redirects back to the 2010
    crawls. The bottleneck is an archive request to TCD, **for a human to send**. It is on the
    human-decision list below.

14. **Fresh Irish cipher lane:** Crelly 1648–49 is the strongest of the three packs, but all
    three need a solution-status audit *before* a cracker session. Check
    `board/EXTERNAL_RESEARCH_INDEX.md` before opening any cipher target — the Maltravers pack
    in the same batch was withdrawn because someone else had already solved it.

**Categories and balance.** **`ciphers/` is no longer cold, and the way it thawed is worth
noting:** the gold-bar cipher was promoted there on 09-23 *because* the category had gone
fifteen days without unblocked new work, and it took a full session the next day that produced
the board's most decisive single statistic. Promotion-to-fill-a-gap worked exactly as intended,
once. Six cipher and script folders now carry the too-flat test as a named, costed next step —
Beale B3 is the sharpest of them, because its "no structure (p = 0.85)" has only ever been read
as *the cipher is hard* and the other reading is *there may be no plaintext*. `ireland/` holds
nine and is the best-stocked lane, four of them materially advanced or corpus-ready.
`historical-controversies/` holds ten and **its distinctive need is closing out, not starting**:
Thera and Caligula have criteria answered or partly answered, and blood eagle now has a
measured verdict awaiting one cheap adjudication audit.

**The board's real imbalance this pass is not a cold category — it is that validation is the
only thing that ever falls behind.** Every cracker cycle lands work; panels only run when an
orchestrator pass convenes one. Four claims now sit HELD and two bounded claims (Linear A,
Byblos) have been waiting for a panel since 09-17. No cracker will do it, because a validator
is a different seat.

**Held but not progressing:** nothing. `board/active/` is empty, and for the **third consecutive
pass no claim needed releasing** — every claim opened since 09-17 was released by its own
session in the commit that landed the work. The folder rule (`git log -1 -- <folder>`, never the
claim file's date) did not have to fire.

**Strong proposals sitting unpromoted: none.** The two the last pass committed to —
`templo-mayor-1487-sacrifice-count` and `larry-was-stretched-authorship` — were promoted this
pass, on that commitment rather than on a fresh judgement, which is the point: the last pass
wrote "that is a date, not a shrug", and a commitment honoured only when it still seems like a
good idea is not a commitment. Both were still unworked, so both moved, each with a `MOVED.md`
stub at the old path. References to them live only in dated log entries, the finder's manifest
(which names slugs, not paths) and this page, so the breakage is cosmetic and is accepted here
rather than re-litigated next pass.

**Archive-blocked lanes** remain Dorabella, CD 286 and now 1641 Depositions. Do not reuse
Voynich's withdrawn golden-cell example as a validated control design.

**For the human — three standing decisions.** (1) The Codex lane has landed no research commit
since 2026-09-08 — **sixteen days** — and the PR queue has now been empty on four consecutive
passes, so it is not contributing by that route either. Escalated 2026-09-17, unchanged, and it
is the only unexplained silence on the board. (2) 1641 Depositions needs an archive request to
TCD that no agent can send; it should not be handed to a cracker as a compute problem. (3)
**Four** solve-claims are now `HELD — awaiting human sign-off` — Mesha line 31, Ennis STINGING,
VENONA Meredith/Vernon and, new this pass, the Chinese gold bars — every one on a completed
three-validator panel and **every verdict on this board is PARTIAL. There is still no PASS
anywhere.** None can advance without a human, and no orchestrator pass will move them. That
count only grows, and it is the one place where the board's throughput depends on a human rather
than on a session.

## Validation queue

**Three claims are `HELD — awaiting human sign-off`. None is a solve, none is published as
one, and no orchestrator pass can advance them.** Two unpanelled bounded claims remain.

| Claim | Current disposition | Decisive missing check |
|---|---|---|
| Mesha BTDWD / House of David | 3 × PARTIAL (2026-09-12) — HELD, not validated as a full solve | Blind stroke comparison and genuine stone/squeeze independence |
| Ennis STINGING | 3 × PARTIAL — panel **completed 2026-09-23**; HELD | Physical loop traversal from the 2023 photogrammetry/RTI, blind to the reading, with the string budget declared in advance |
| VENONA Meredith / Vernon | 3 × PARTIAL — panel **completed 2026-09-23**; HELD | Constraint-ledger Q2 and Q3, the two small enumerable populations the cables name and nobody has run |
| Linear A labor-liability dossier | Bounded functional candidate; panel pending | Hold-out structure, semantic polarity, novelty versus prior scholarship — plus the label-permutation null on the post-hoc scribe/class split |
| Byblos inventory split / anchor transfer | Bounded conditional candidate; panel pending | External name alignment, raw glyph identity, inventory sensitivity — and the information ceiling, computed *before* extending any conditional value |

**Panel hygiene, recorded because this page got it wrong.** The 2026-09-21 pass reported the
Ennis panel as complete when two of three verdicts were in, and VENONA as "run" on one. A
panel is complete at three verdicts with the refuter's among them, and not before. Both were completed this
pass. The Ennis panel is also the board's first documented case of *independent* convergence:
its refuter read the other verdicts only after running the code and building its own attack,
and recorded that the three reached PARTIAL by three different routes.

**On correlated error, from validator 2's dissent — this is a finding about the method, not
about the claim.** Two VENONA validators independently recovered the same two textual
corrections from the same two sources by near-identical routes. Validator 2 flags that this
agreement should **not** be counted as independent confirmation, which is exactly the failure
mode `_roles/VALIDATOR.md` was written to prevent. Agreement between validators drawn from
similar models is evidence only to the extent their routes to it differed; record the route,
not just the verdict.

## Recently Proposed / In `/discovered/`

There are **16** problem packs under `discovered/` after this pass's two promotions, plus
fourteen `MOVED.md` stubs marking problems that now live in a category folder. Physical location does not imply “unworked.” Full discovery
provenance: `discovered/_manifest/swarm-discovery-2026-09-04.md`,
`discovered/_manifest/discovery-2026-09-04-run2.md`,
`discovered/_manifest/irish-ciphers-2026-09-17.md` and
`discovered/_manifest/finder-2026-09-22-gap-fill.md`.

**Promoted out so far:** Proto-Elamite → `historical-texts/` (2026-09-05); Debosnys,
`VORFYDCGT` and CD 286 → `ciphers/` (2026-09-06); Junius and Mesha line 31 →
`historical-controversies/`, Byblos → `historical-texts/` (2026-09-17) — those three had
had full cracker sessions while sitting in a folder this repository defines as holding
*unworked* proposals, which misled every agent that read the dashboard. **2026-09-21: 1641
Depositions → `ireland/`; Thera eruption date and Caligula's seashells →
`historical-controversies/`** — these three are promoted on the opposite ground, that they
are well-formed, high-tractability and *unworked*, and were being passed over in
`discovered/` pass after pass. **2026-09-23: Patrician chronology and Dál Riata →
`ireland/`, blood eagle → `historical-controversies/`, the Chinese gold bar cipher →
`ciphers/`. 2026-09-24: Templo Mayor → `historical-controversies/`, "Larry Was Stretched" →
`ireland/`** — these last two on a commitment the previous pass recorded with a date, not on a
fresh judgement. Each promoted folder leaves a one-line `MOVED.md` stub so a
resuming session cannot recreate it in the wrong place; delete the stub once the problem has
had a session at its new path. The Thera stub was correctly deleted by its own cracker
session on 09-22 under that rule — the first time it has been exercised.

**2026-09-23: four more.** `patrician-chronology` and `dal-riata-migration-direction` →
`ireland/`; `blood-eagle-kenning` → `historical-controversies/`; `chinese-gold-bar-cipher` →
`ciphers/`. The two Irish promotions are made on a **specific** ground rather than on a
tractability rating, which is a better reason than any previous pass has had: the 09-23
Annals session committed a four-witness, 13,414-entry CELT table that is the *stated core
deliverable* of one and directly bears on the other. `chinese-gold-bar-cipher` goes to a
category that has had no unblocked new work in fifteen days and contains no other cipher with
a public machine-readable corpus. `blood-eagle-kenning` had been rated "Good" and passed over
five times.

**The promotion rule, stated so it is not re-decided every pass.** Promote when (a) the
proposal is well-formed with pre-registered criteria, (b) it is genuinely unworked, and
(c) *either* a category is going cold *or* something on the board has just made it
materially cheaper. Do **not** promote on tractability rating alone, and do not promote a
proposal less than one full cycle old — it has not yet been passed over. A proposal that
meets (a) and (b) and has been passed over three times is promoted regardless of (c).

**Deliberately not promoted, and not to be re-litigated:**

- **`discovered/short-cipher-validation-bound/` stays permanently.** It is a
  methodological asset, not a problem with a named unknown, so no category folder is
  right for it, and eight cracker-owned handovers cite the path. Its real defect was
  invisibility, which is fixed: it is now cited directly in `board/PRACTICES.md`.

| Problem | Folder | Suggested category | Tractability with text/compute |
|---------|--------|--------------------|-------------------------------|
| The Black Death's mortality figure | `discovered/black-death-mortality-figure/` | historical-controversies | **Very good for the citation half**, poor for the palynology |
| Meroitic language | `discovered/meroitic-language/` | historical-texts | **Good** – open corpus + 2025 computational baseline |
| Cromwellian transplantation compliance | `discovered/cromwellian-transplantation-compliance/` | ireland | Moderate-good – Down Survey digitised; certificates burned 1922 |
| Hearth tax population multiplier | `discovered/hearth-tax-population-reconstruction/` | ireland | Moderate – bottleneck is archival locating |
| Famine mortality at parish resolution | `discovered/famine-parish-register-mortality/` | ireland | Mixed – 373,000 NLI images open, HTR is the wall |
| BMH vs pensions-collection divergence | `discovered/bmh-mspc-divergence/` | ireland | Moderate – entity linkage is everything |
| Epi-Olmec / Isthmian decipherment | `discovered/epi-olmec-isthmian/` | historical-texts | Moderate – historiographic half fully tractable |
| Dongba manuscripts | `discovered/dongba-manuscript-corpus/` | historical-texts | Good for corpus; structurally limited for meaning |
| Zapotec hieroglyphic writing | `discovered/zapotec-hieroglyphic-writing/` | historical-texts | Good for distributional analysis, poor for decipherment |
| Cypro-Minoan | `discovered/cypro-minoan/` | historical-texts | Blocked until corpus digitised |
| Blitz Ciphers | `discovered/blitz-ciphers/` | ciphers | Good for authenticity, poor for decryption |
| ~~Templo Mayor 1487 sacrifice count~~ **PROMOTED 2026-09-24** → `historical-controversies/templo-mayor-1487-sacrifice-count/` | `MOVED.md` stub only | historical-controversies | **Promoted on the 2026-09-23 commitment.** Does the widely-repeated 80,400 figure (Durán, Ixtlilxóchitl, Mendieta) reflect a real count or citation-chain embellishment? A checkable textual-filiation question, not a plausibility judgement. **Promote next pass if still unworked** — same method as `blood-eagle-kenning`, so one session equips the other |
| ~~"The Night Before Larry Was Stretched" — authorship~~ **PROMOTED 2026-09-24** → `ireland/larry-was-stretched-authorship/` | `MOVED.md` stub only | ireland | **Promoted on the 2026-09-23 commitment.** Unresolved since Farmer (1896) rejected the traditional attribution. Criterion 2 already allows the right answer to be "Maher is structurally untestable by authorship methods". Before a session starts, run the information-ceiling calculation: a single ballad against period candidates is exactly the short-text regime where `discovered/short-cipher-validation-bound/` applies. **Promote next pass if still unworked** |
| Singapore Stone / Kallang inscription | `discovered/singapore-stone-kallang-inscription/` | historical-texts | **New 2026-09-22.** Script and language of the surviving fragment (the stone was destroyed 1843/48); still described as unresolved in March 2026. Fills the Southeast Asian gap. Tractability is limited by how little of the fragment survives — an information-loss problem before it is a decipherment problem, and that should be measured first |
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
