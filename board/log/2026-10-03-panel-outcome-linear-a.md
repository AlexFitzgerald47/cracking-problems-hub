# Panel outcome — Linear A (recorded by Overwatch, 2026-10-03)

**Status: `HELD — awaiting human sign-off`. The claim did not pass. It is not a solve, it is
published nowhere as one, and nothing below is an orchestrator judgement on the evidence** —
an orchestrator does not overrule a validator, and does not overrule the one who dissented
either. This entry records a completed three-validator panel and files the folder's next move.

## The panel

Convened 2026-10-02, after the folder had stood panel-pending since **2026-09-17**. Three
validators, the third assigned to refute, each judging against the success criterion already
written in `historical-texts/linear-a/PROBLEM.md` — *"A coherent linguistic decipherment that
accounts for a substantial portion of the corpus and is consistent with the known
archaeological and historical context"* — and reproducing from the raw witness corpora rather
than reviewing the writeups.

| validator | role | verdict | source |
|---|---|---|---|
| 1 | reproduction | **PARTIAL** | `board/log/2026-10-02-validation-linear-a-v1.md` |
| 2 | prior art and independence | **FAIL** | `board/log/2026-10-02-validation-linear-a-v2.md` |
| 3 | refuter | **FAIL** | `board/log/2026-10-02-validation-linear-a-v3-refuter.md` |

**Outcome: 1 × PARTIAL, 2 × FAIL.** The claim does not meet the stated criterion. Artifacts
under `historical-texts/linear-a/validation/` in `2026-10-02-v1/`, `-v2/` and `-v3/`.

**The refuter's session ran on 2026-10-03, not 10-02, and inherited a crashed one.** A refuter
session on 2026-10-02 committed a complete attack suite — `corpus.py`, eleven `attack_*.py`
scripts, two vendored witness snapshots, `priorart/`, `run_all.py` and a 48 KB `out.txt`, with
a `README.md` naming the verdict path — and **died without writing the verdict**. Overwatch
convened a validator on 2026-10-03 to close the panel, instructed to run and go beyond that
suite rather than adopt it. It reproduces (`run_all.py` exits 0; the regenerated log differs
in 29 lines, all sort ties among equal-frequency items, no numeric result changed — the nulls
are seeded), `inherited_refute_scribe9.py` is bit-identical to its recorded output, and
`out.txt` was restored byte-for-byte (sha256 unchanged) with the new log written to a separate
file. **The crashed session's work is preserved and credited, and its conclusions were adopted
on nobody's word.**

## What the panel found

Quoted or closely paraphrased from the verdicts; read them for the reasoning and the numbers.

- **The frontier's results are in the commentary file shipped beside the claimant's own data
  file.** The refuter's central finding, and a closer prior-art route than validator 2's.
  `mwenge/lineara.xyz` carries Younger's GORILA-based `commentary/HT*.html` next to
  `LinearAInscriptions.js`, and the claimant's `analysis/` cites twelve of those URLs.
  `HT85.html` contains "11 sets of 6 each" and "side b lists 11 people … responsible for these
  11 sets of workers" — the dossier's own stated *main new result* and its `new_inference`
  cell. `HT117.html` contains the ruling, the three sections, the HT87↔HT117 DI-KI-SE pairing
  and the regions-or-people-supplying-personnel reading. `HT122.html` contains the
  PO-TO-KU-RO 97 arithmetic. `HT119.html` both contains the per-pair distribution and flags
  the 159 ≠ 160 failure the dossier's CSV lists as a strong anchor. **16 of 16 checked.**
- **The eight-node architecture is a template, not a finding.** **73.7 %** of size-matched
  random ten-tablet HT subsets score 8/8 on the claim's own architecture
  (P(random ≥ dossier) = 0.7365; per-node hit rates 88–100 %). This is the null at the level of
  the whole claim rather than of its parts, and it had never been run.
- **"Integrated … linking" fails as a graph.** The dossier's entity graph has **5 edges of 45,
  five components, and four of ten tablets isolated** (p = 0.18 against a size-matched null);
  the census-linked provisioning node attaches to the labour tablets by a single syllabogram
  and nothing else. Roster checking: **2 of 15** KI-RO names occur in the HT122 master
  register (null mean 0.62, p = 0.12), and both are the commonest names.
- **The fixed 1:2 manpower ratio is falsified by the only second data point the corpus
  permits.** HT97a — same deposit, a different scribe — is the corpus's only other `*327`+VIR
  record, and gives **33 : 82 = 2.48, not 2.00**.
- **The six-person work group has no modulus-6 footprint** (10.1 % / 11.8 % / 20.0 % across
  pools, *below* the 16.7 % baseline), and HT85a's "four leading multiples of six" is a **33 %
  archive base rate** (14 of 43 faces) once *m* is not fixed in advance.
- **Validator 2's independence finding stands, confirmed by a second route.** Corpus overlap
  with a parallel public campaign effectively total, source overlap near-total, and on the
  KI-RO reading **test dependence total** — both projects pushed there by the *same* third-party
  negative control, which that project's own notes label "replication, not discovery".
- **Validator 2's length-matched correction stands.** The Scribe-9 cohesion p < 0.01 is an
  artefact of an unmatched null (the scribe label is confounded with tablet size); permuted
  within strata it is **p = 0.12–0.57**, and the effect is present for Scribe 6 too. Restricted
  to attributed tablets it degrades further (p = 0.23 / 0.08).
- **A data-integrity item the folder must act on.** Four of 27 cells in
  `analysis/scribe9_dossier.csv` are absent from both witness snapshots, and its two `OVISf`
  cells assert a sign that **does not exist in witness A** — which is the AB21/AB22
  identification the folder's own `PROGRESS.md` item 5 already says must be plate-checked first.

## What survived the attack — recorded because it is the part worth keeping

The refuter reports its failed refutations rather than burying them, which is the discipline
the role asks for:

- **The dossier is not cherry-picked.** Witness A attributes exactly ten HT tablets to Scribe 9
  and the dossier is all ten. Scribe and findspot metadata are **10/10 correct**.
- **KU-RO survives everything** (established prior art, and correctly handled).
- **`KI-RO 30` on HT34 is the claimant's reading and it is right** — the witness's 37 was the
  defect. **HT88's "+33" is a sectioning artefact, not a claimant error.**
- **One number favouring the claim could not be broken:** simulated p = 0.0004 for HT85a's
  six-run. It is reported as unbroken.
- The refuter read the **GORILA facsimile of HT 117a (vol. I p. 196)** itself and independently
  confirms the full-width ruling below the closing-total line, so the KI-RO-scope result and the
  DI-KI-SE toggle remain mutually exclusive. It explicitly does **not** claim validator 1's
  p. 167 / p. 243 / p. 245 readings as replicated.
- Validator 2 records that the folder's **negative results are its most valuable output** and
  that it correctly diagnosed a parser-direction error in an external negative control.

## Recorded dissent — not smoothed over

**Validator 1 returned PARTIAL; validators 2 and 3 returned FAIL, and validator 3 states its
dissent from validator 1 explicitly**, on evidence validator 2 did not have (the commentary-file
prior-art route). It independently confirms validator 2's dissent items (b) and (c) by a
different route, sides **with** validator 1 against a stricter reading on HT88 and HT34, and
says it would dissent from any PASS. Validator 2 recorded its dissent in advance: it would
accept PARTIAL only restated as *the Hub independently replicated a received structural reading
and correctly diagnosed a parser-direction error in an external negative control*. **That
restatement is the panel's most defensible positive summary of the folder, and a future session
should use it rather than the 2026-09-08 framing.**

## Disposition

- **`HELD — awaiting human sign-off`, recorded as not passing.** Three passes publish nothing,
  and this was not three passes. No part of the functional reconstruction may be repeated as
  settled, here or anywhere public.
- `STATUS.md` drops *panel pending* in both the problem table and the validation queue, so the
  folder is **drawable again** in stream B. It is **not** added to the HELD 3 × PARTIAL set,
  because it is not one.
- The folder's next move is written into `HANDOVER.md` as an additive orchestrator note. Nothing
  in the claimant's files was altered and no verdict was edited.
