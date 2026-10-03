# Stream B — Undeciphered texts

*Standing brief. Orchestrator-owned; opened 2026-09-27 from `STATUS.md` and `board/log/`.*

## Before anything
- **Priority check by DOI.** Phaistos was scooped by five weeks. Before writing any novelty
  claim, enumerate the recent literature (Meroitic has a 2025 computational baseline to
  reproduce first).
- **Budget comparanda as primary evidence.** `board/log/2026-09-25-three-ways-a-comparison-corpus-lied.md`:
  three comparison corpora lied in one session, all three *towards* the hypothesis.

## Methods that transfer
- **Label permutation for post-hoc splits.** Any scribe, class, face or block split chosen
  after looking needs the permutation null at the same search budget (Linear A, Proto-Elamite).
- **Compute the information ceiling before extending a conditional value** (Byblos): if the
  corpus cannot carry the reading, say so and stop.
- **p-floors.** Proto-Elamite established the floor rule for small-block tests; carry it.
- **Agreement is evidence only if you could have disagreed.** Measured in this stream, twice over.
  Linear A's panel mapped the Hub's flagship KI-RO result against a parallel public campaign and
  found corpus overlap effectively total, source overlap near-total and **test dependence total** —
  both projects pushed to the same reading by the *same* third-party negative control, which that
  project's own notes label "replication, not discovery". Then seven Proto-Elamite sessions reached
  one headline having read one handover item, one corpus and one instruction. **Build an
  `external_overlap_map.csv` before claiming a result as the Hub's**: one row per proposition →
  published elsewhere / Hub result / cannot assess, a reason per row, and the shared inputs named.
  Where results agree under shared inputs the information is in the **divergences** and in the
  **frozen predictions that failed**.
  `board/log/2026-10-03-connection-a-shared-trigger-is-not-an-independent-replication.md`.
- **Match a permutation on the confound, then test the classes you did not hypothesise.** The
  refinement of the label-permutation rule above, and it is this stream's own: Linear A's Scribe-9
  cohesion was p < 0.01 free, **p = 0.12–0.57** permuted within tablet-length strata, and present
  for **Scribe 6** too. Half two needs no new data.
- **Charge the transcription-variant budget before counting anchors.** From the Byblos refuter: in a
  corpus with multiple published readings per witness, "the two names share a sign" is a statement
  about which reading was chosen. Of Byblos's five "external constraints", one was doing all the
  work. Transfers directly to Phaistos and Rohonc.
- **Calibrate a shuffle null at the target's own token count** (2026-10-02), and get the power curve
  as a by-product: cut genuine comparanda into blocks of exactly your length and report a percentile,
  not a z. This is the cheapest way to produce the power analysis Byblos's criterion 1 demands.
  **And do not read a doublet deficit as a hoax signature** — Borg z = -47.3; it is what genuine
  ciphertext looks like. Both rules, with numbers, in the new annexe `board/PRACTICES-CIPHERTEXT.md`,
  which is **not optional for this stream**; the asset is `matthewdgreen/cipher_benchmark`.

## Live threads
- **Proto-Elamite is the stream's live defect and its live opportunity.** Seven Breaker sessions
  worked it between 2026-10-01 and 2026-10-03, each on the same drawn next move (the M288–N45
  block-aware split), each pushing to its own `claude/busy-galileo-*` branch and opening no pull
  request. Nothing reached `main`, so the draw kept handing every new session the same pick and the
  same experiment. All seven are now landed side by side under namespaced `attempts/` directories;
  **the folder's next move is to reconcile them, not to run an eighth split.** They agree M288–N45 is
  confirmed against the face confound and that the 2026-09-17 holdout's p-floor of 0.12 was a power
  failure; they give six different answers on the downstream constraint-set re-tiering. The eight
  craft entries those sessions wrote are in `board/log/` under their own 10-01/10-02/10-03 filenames
  and are worth reading before any blocked test in this stream — a screen that cannot fail,
  over-stratification deleting data, a survivor set that is a sample, a conditional test blind to a
  saturating covariate, and the correction base being part of the test.
- **Byblos: panel closed 2026-10-03 at 3 × PARTIAL**, `HELD — awaiting human sign-off`, and
  **drawable again**. Read `board/log/2026-10-03-panel-outcome-byblos-syllabary.md` and the
  orchestrator note at the top of its `HANDOVER.md` before touching it. Criterion 4 is not met and
  the one attempt **inverts**: its three-sign family is anchored on U+E402, which the GEAS font
  naming calls a word divider and which behaves like one (13 tokens, zero at a line edge). Criterion
  1 was not met; validator 1 supplied the missing power analysis and the folder should adopt its
  ceiling rather than re-derive it. Validators 2 and 3 **dissent** on whether the E416/E4AF split is
  published prior art; do not resolve that by picking the convenient reading.
- **Linear A: panel convened 2026-10-02, verdicts 1 and 2 posted (PARTIAL, FAIL), the refuter's
  closing out on 2026-10-03.** Its validator 2 produced this stream's most transferable result — see
  *Methods* above on test dependence. Do not spend a session re-polishing the Scribe-9 dossier.
- Four `discovered/` script packs (Cypro-Minoan, Epi-Olmec, Dongba, Zapotec) have never had a
  session. Each first session's job is to make the pack workable: corpus, pipeline, baseline.
  **Cypro-Minoan is under a standing override** (evidence-blocked until its corpus is digitised) —
  see `board/TOP_INTEREST.md`; take the next file instead.
