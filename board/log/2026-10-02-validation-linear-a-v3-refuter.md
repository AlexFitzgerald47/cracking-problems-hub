# Validation — Linear A, validator 3 (refuter)

Panel convening date 2026-10-02; this session ran 2026-10-03 and inherits the
attack suite a 2026-10-02 refuter session committed and never reported on.

```
claim: The Linear A folder's frontier as stated in HANDOVER.md (2026-09-08) — a
       "functional/historical solve candidate; not a phonetic decipherment or
       language-family solve": that a substantial Haghia Triada / Casa del Lebete
       tablet dossier written by HT Scribe 9 records an integrated labour-liability
       administration linking accountable units, personnel assessments, standardized
       six-person work groups, assignment, roster checking, KI-RO exception
       reporting, census-linked provisioning and hierarchical KU-RO / PO-TO-KU-RO
       control totals. Supporting artefacts:
       analysis/2026-09-08-scribe9-dossier-functional-reconstruction.md,
       analysis/2026-09-07-haghia-triada-labor-control-functional-solve.md,
       analysis/2026-09-07-kiro-unified-residual-grammar.md,
       analysis/2026-09-07-obligation-circuit-post-award.md,
       and the CSV decode tables in analysis/.

problem: linear-a

criteria applied: "A coherent linguistic decipherment that accounts for a
       substantial portion of the corpus and is consistent with the known
       archaeological and historical context."

validator role: 3 (refuter)

reproduced: partially — the prior refuter suite reproduces exactly; the claim's
       own results largely do not survive the new attacks. Specifics below.

verdict: FAIL
```

---

## 0. What I inherited, and whether it still runs

A 2026-10-02 refuter session committed `validation/2026-10-02-v3/` — `corpus.py`,
eleven `attack_*.py`, two vendored witness-A snapshots, `priorart/`, `run_all.py`
and a 48 KB `out.txt` — and died without posting. I ran it before doing anything
else.

- `python3 run_all.py` — **exit 0, reproduces.** The regenerated log differs from
  the committed `out.txt` in **29 lines, all of them sort ties among
  equal-frequency items** (`DA-RE`/`DA-RI-DA` at rank 25/26; `MA-KA-RI-TE`,
  `MI-TU`, `DI-KI-SE` all at 2 tablets). **No numeric result changed.** The
  permutation nulls are seeded (`random.Random(SEED)`), so the p-values are
  deterministic. I restored the committed `out.txt` byte-for-byte afterwards
  (sha256 `1b464095…f50e33` before and after) and wrote my own log to a separate
  file.
- `python3 inherited_refute_scribe9.py` — **bit-identical** to `inherited_out.txt`,
  as that session claimed.

I adopt none of its conclusions on its word. Where I confirmed something myself I
say so below; where I did not, I say that too.

My own work is `validation/2026-10-02-v3/r_common.py`, `attack_r1_integration.py`,
`attack_r2_template.py`, `attack_r3_six.py`, `attack_r4_cells.py`,
`attack_r5_priorart.py`, `run_refuter3b.py`, `out_refuter3b.txt`, `priorart_r/`,
`README_refuter3b.md`. Everything else in that directory is untouched.

---

## 1. The five new attacks

### R1 — "integrated … linking" fails as a graph

The claim is not that ten tablets share a hand. It is that they are an
**integrated** administration **linking** eight named functions. That is a graph
assertion and nothing in the inherited suite, or in v1 or v2, tests it as one. I
built the dossier's own entity graph from the raw witness: an edge is a shared
multi-sign designation.

| | |
|---|---|
| edges among the 10 dossier tablets | **5 of 45 possible** |
| connected components | **5** |
| tablets with no link to any other dossier tablet | **4** — HT112, HT119, HT128, HT132 |
| largest connected component | **6 of 10** |
| size-matched null (±10 % of 109 type-slots, n = 20 000) | null mean 2.84, 95 % [0, 7], **p = 0.18** |

The dossier is not more internally linked than a size-matched random draw of ten
HT tablets. And the specific links the architecture needs are the ones that are
missing:

- **"census-linked provisioning"** is HT128. Its sign-groups are `*326, PA-RA,
  TU-RU-NU-SE-ME, WA-TU-MA-RE, MI-TA, DI, MA-RI, RU`. Exactly **one** of them
  occurs on any of the six labour tablets: **`DI`, a single syllabogram** — which
  the board's own 2026-09-25 rule (now in `PRACTICES.md`) says cannot be separated
  from an abbreviation in an administrative corpus. Multi-sign overlap: **zero**.
  The provisioning node of the "operating system" is attached to the labour nodes
  by nothing that survives the board's own disqualification rule.
- **HT112 and HT132 share no sign-group at all** with the labour tablets.

**Roster checking, at entity level.** The architecture says KI-RO flags named
people missing against an accountable population, and HT122 is the master register
over that population. Taking the two KI-RO blocks the claim names:

- HT94b: `TU-MA, PA-TA-NE, DE-DI, KE-KI-RU, SA-RU`
- HT117a: `U-SU, MI-TU, KU-RA-MU, MA-RU, KU-PA₃-NU, TU-JU-MA, U-DI-MI,
  MI-RU-TA-RA-RE, TE-JA-RE, NA-DA-RE`

HT122's fifteen designations contain **2 of those 15** — `KU-PA₃-NU` and
`PA-TA-NE`. Null (15 names drawn at random from the 365 HT multi-sign
designations): mean 0.62, **p = 0.12**. And the two hits are the two commonest
names in the set (`KU-PA₃-NU` is on 6 of 133 HT tablets). **Thirteen of fifteen
"exceptions" never appear in the register they are exceptions against, and
thirteen of fifteen register entries never appear in an exception list.** The
only entity-level instantiation of "roster checking" the corpus offers is at
chance.

### R2 — the eight-node architecture is a template, not a discovery

This is the attack I most wanted to make and the one neither prior verdict
makes: a null **at the level of the whole claim** rather than its parts. I turned
each of the claim's eight architectural nodes into a detector, written to be as
generous as the claimant's own usage and frozen before any set was scored
(accountable-unit header slot; personnel assessment; standardized group ratio;
assignment; roster checking; KI-RO exception; census-linked staple; KU-RO control
total — definitions in `attack_r2_template.py`), then scored the dossier, every
HT scribe, and random 10-tablet subsets.

| set | score |
|---|---|
| the Scribe-9 dossier | **8/8** |
| HT Scribe 6 (n = 3) | 7/8 |
| HT Scribe 5 (n = 5) | 7/8 |
| HT Scribe 2 (n = 8), HT Scribe 7 (n = 3) | 6/8 |

| null | result |
|---|---|
| **size-matched random 10-tablet HT subsets** (n = 2000) | **73.7 % score 8/8; 97.1 % score ≥ 7/8** |
| P(a size-matched random subset scores ≥ the dossier's 8/8) | **0.7365** |
| unmatched random 10-tablet subsets | 14.2 % score 8/8; P(≥ dossier) = 0.1415 |

Per-node hit rates in size-matched random subsets: accountable-unit header 100 %,
personnel assessment 100 %, assignment 100 %, census-linked staple 100 %, KU-RO
total 99.8 %, roster checking 92.8 %, KI-RO exception 89.7 %, standardized group
ratio 88.0 %.

**Three quarters of comparable ten-tablet slices of the Haghia Triada archive
instantiate the claim's entire architecture.** The "integrated labour-liability
administration" is not a reading of Scribe 9's output; it is a description of what
Haghia Triada tablets look like, applied to one slice. This is the whole-claim
version of the post-hoc-decomposition warning the folder's own `HANDOVER.md`
carries from `board/log/2026-09-23-…`, and it had not been run.

### R3 — the "fixed manpower ratios" are falsified by their own second data points

`HANDOVER.md`: *"Together with HT85's six-person groups, Scribe 9 repeatedly
encodes fixed manpower ratios."* A fixed administrative ratio is a prediction
about the rest of the archive. Both predictions fail.

**(a) `*327 : VIR = 1 : 2` is contradicted by its only other attestation.** The
corpus contains exactly **two** records carrying both a `*327` sign and a VIR/MUL
ideogram:

| | scribe | findspot | `*327` | VIR | ratio |
|---|---|---|---|---|---|
| HT119 | HT Scribe 9 | Casa Room 9 | 34 | 68 | **2.0000** |
| HT97a | HT Scribe 7 | **Casa Room 7** | 33 | 82 | **2.4848** |

Under a fixed 1:2 manpower ratio HT97a should read 33 : 66. It reads 33 : 82.
Younger's commentary further notes that `*327` is standardly conjectured to be
**AES — bronze** (B *140; Palaima 1988: 326), not a counted personnel unit, and
cross-references HT119 ↔ HT97a himself. **Neither prior validator, nor the
inherited suite, found HT97a.** The inherited suite's `attack_nulls.py` 2a showed
the observation was cheap; R3 shows it is not merely cheap but *wrong* on the one
test the corpus permits. HT119 is one coincidence, not a standard.

**(b) No six-footprint exists anywhere in the archive.** Divisibility by 6:

| pool | % divisible by 6 |
|---|---|
| all HT entry amounts (n = 552) | 10.1 % |
| amounts on VIR/MUL-bearing faces (n = 119) | 11.8 % |
| stated totals (n = 35) | 20.0 % |

All below the 16.7 % uniform baseline, and below the rates for 4 and 5 in every
pool. If the administration ran on standardized six-person groups, nothing in the
archive's numbers knows it.

**(c) HT85a's "first four entries are multiples of six" is a 33 % base rate once
the modulus is not fixed in advance.** Simulated, `P(4 leading multiples of 6 in 7
corpus-like amounts > 1) = 0.0004` — which looks strong, and I report it because
it is the single best number the claimant has. But *m* = 6 is not given in
advance: it is chosen because 66/6 = 11 matches face b's entry count. The honest
statistic is a leading run of ≥ 4 sharing **some** modulus in 2–12, measured
directly on the archive rather than simulated: **14 of 43** comparable HT faces
(**33 %**) open with one — HT10a, HT11b, HT122b, HT146, HT28b, HT29, HT39, HT47a,
HT6b, HT85a, HT86a, HT9a, HT95a, HT95b. And the smallest modulus witnessing
HT85a's run (12, 12, 6, 24) is **2, not 6**.

**(d) The header formula is the archive's, not the dossier's.** HT85a's
`A-DU · *307+*387 · VIR ·` — read as Scribe 9's assessment signature — is the
form of HT27a (Scribe 11), HT32 and HT5 (Scribe 1), HT89 (Scribe 2) and
**HT97a (Scribe 7, found in Casa Room 7, the same deposit)**, which is the same
formula under `KA-RU` instead of `A-DU`.

### R4 — the dossier table's own cells, and the cohesion null on the right pool

**(a)** Mechanical audit of all 27 factual anchor cells in
`analysis/scribe9_dossier.csv` against **both** vendored witness-A snapshots,
with ideogram citations treated generously (`VIR 68` matches `VIR+[?] 68`;
"GRA variants" matches `GRA+KU`):

- **21 ok, 2 ok as ideogram variants, 4 absent from both snapshots (15 %).**
- The four are `QI-TU-NE` (HT87, HT117) and `OVISf` (HT112, HT132).
- **There is no `OVIS` sign anywhere in witness A.** The ovicaprid-family signs
  attested are `*21F` (4), `*21F-*118` (3), `*21F-JA-DU`, `*21F-RI-TU-QA`,
  `*21F-TU`, `*21F-TU-NE` (3), `*21M` (8), `*22F` (14), `*22M` (3). HT112 reads
  `*21F TU-PA ⟦lac⟧ | CYP 6`; HT132 reads `*22F 27`. Both cells assert the
  sheep/goat identification of the undeciphered `*21F`/`*22F` series — **which is
  exactly the identification this folder's own `PROGRESS.md` item 5 flags as
  subject to a systematic AB21/AB22 inversion across 14 documents in a widely used
  digital corpus, "to be independently plate-checked before the Hub relies on
  livestock distributions."** The dossier relies on it twice without the check.
  (This confirms validator 1's two hand-found errors and supplies the reason they
  matter.)
- `QI-TU-NE`, the dossier's "accountable unit", is Younger's `QIᶠ-TU-NE` with the
  `ᶠ` dropped — a phonetic value for `*21F`, the same disputed series.
- **The metadata cells are perfect: scribe and findspot reproduce 10/10.** The
  dossier's frame is sound; its content cells are where the failures are.

**(b)** Every earlier null — 2026-09-25, v1, v2, and the inherited `attack_split`
— draws the comparison set from all 133 HT tablets, **58 of which carry no
scribal attribution at all**. For a claim about a hand that is the wrong pool: a
random draw can mix tablets that are in fact one hand. Restricting the null to the
75 attributed tablets:

| statistic | observed | pool = all 133 | **pool = attributed only** |
|---|---|---|---|
| all sign-group types | 13 | p = 0.191 | **p = 0.226** |
| strict (multi-sign, operators dropped) | 8 | p = 0.055 | **p = 0.084** |

Restricting to the pool the claim is actually about moves the p-value **in the
unfavourable direction**. I confirm validator 2's finding that the cohesion does
not survive a matched null, by a route neither v2 nor the inherited suite used.

### R5 — 16 of 16 frontier results are in the commentary file next to the claimant's own data file

Validator 2 established prior art through an external AI workspace
(`dbourdeau/cyphersolver`) and the secondary literature. That route invites the
reply "shared sources, parallel discovery". R5 closes it. `mwenge/lineara.xyz`
carries, **beside** `LinearAInscriptions.js`, a `commentary/HT*.html` per tablet
reproducing John Younger's GORILA-based commentary. The claimant cites twelve of
these files **by URL** in `analysis/`. I fetched the dossier's thirteen, hashed
them, and searched each of the frontier's named results as a literal string.

**16/16 found verbatim.** The decisive ones:

- `commentary/HT85.html`: *"side a lists regions contributing personnel totalling
  66 workers in **11 sets of 6 each**; and that side b lists **11 people and/or
  their functionaries responsible for these 11 sets of workers**"* — the dossier's
  "Main new result" and `scribe9_dossier.csv`'s `new_inference` cell, verbatim,
  credited there to Brent Davis. Also *"**These groups of 6 personnel are
  obviously conventional**"*, *"the names on HT 85a are **toponymns**"*, *"places,
  from which personnel are **assessed (A-DU)** in sets of 6 workers"*, and the
  `PA`/`KA`/`DI` absorption the dossier's rendering table performs.
- `commentary/HT117.html`: *"**the rule there apparently introduces a second
  section** on side a, headed by SA-TA … Side b therefore presents a **third
  section** headed by QIᶠ-TU-NE"*; *"in both HT 87 & HT 117, QIᶠ-TU-NE … and
  DI-KI-SE … appear in the same paragraph"*; *"**SA-TA, QIᶠ-TU-NE, and MA-KA-RI-TE
  may be regions or people supplying personnel**"* — the HT87→HT117 "strongest
  query-grammar result" and the U-MI-NA-SI/SA-TA/QI-TU-NE "accountable unit"
  result, both already published.
- `commentary/HT122.html`: *"**PO-TO-KU-RO 97 = KU-RO b.5 65 + a.8 31 + 1**"* and
  *"the document probably lists places by name and **their contributions of groups
  of personnel**"* — the hierarchical control-total flagship and the
  master-register reading.
- `commentary/HT119.html`: *"**each unit of *327 could be distributed per pair
  VIR**"* — the 1:2 manpower ratio; and *"the numbers total **159, not KU-RO's
  160**"* — the failure `scribe9_dossier.csv` lists as a strong anchor without
  noting that it fails, flagged by the source the claimant reads.

The Hub's own `analysis/2026-09-07-ht85-order-preserving-dispatch-reconstruction.md`
says so for HT85 (*"Younger had already seen eleven six-person groups and multiple
groups assigned to QE-KA / TE-TU"*), to the folder's credit. **`HANDOVER.md`'s
frontier statement and `scribe9_dossier.csv`'s `new_inference` column do not carry
that attribution forward, and the frontier is what is under validation.**

---

## 2. What I checked against the primary edition

I read the GORILA facsimile of HT 117a myself — vol. I **p. 196** (the image
validator 1 vendored as `2026-10-02-v1/data/gorila_p232_HT117a.png`; the file name
is the PDF page, the printed page is 196). **A full-width horizontal ruling runs
across the tablet immediately below the short line that carries the closing total,
with three further lines below it.** Both the photograph and the facsimile show
it. This independently confirms validator 1's decisive internal objection and the
inherited `attack_structure.py` §5a, and Younger's apparatus states it in words.

So the claim's two strongest advertised results remain mutually exclusive, and I
reached that conclusion from the plate rather than from either of their reports:
either `KU-RO 10` closes the KI-RO block — in which case HT117 is not "a large
KI-RO exception roster grouped by units", `SA-TA` and `*21F-TU-NE` are not
parallel subheadings inside one KI-RO block, and **DI-KI-SE (on face b, below the
ruling, on the far side of the tablet) is not marked KI-RO at all**, so nothing
switches — or the KI-RO heading governs all three sections, in which case the
HT88 = 6 / HT94b = 5 / HT117a = 10 cardinality result loses the scope rule that
makes it work.

**What I did not check.** I did not download GORILA vol. I myself; I read only the
three page images validator 1 vendored, and only the HT117a one bears on any
finding of mine. I therefore cannot independently confirm v1's reading of the
p. 167 apparatus on HT85's 66 (*"marque d'ongle accidentelle"*) or the p. 243/245
value columns for HT122. I take those as v1's, unreplicated by me.

---

## 3. Refutation attempts that FAILED — these stand

Per the role file, a refutation that fails is worth more than an agreement. Four
did:

1. **The dossier is not cherry-picked at tablet level.** I expected the ten
   tablets to be a favourable selection from Scribe 9's output. They are not:
   witness A attributes **exactly ten** HT tablets to Scribe 9 and the dossier is
   all ten. No exclusion.
2. **The scribe and findspot metadata are exactly right**, 10/10, including the
   three-deposit distribution. The archaeological frame reproduces cleanly, as
   validator 1 said.
3. **KU-RO as a summation marker survives everything.** I tried to break it and
   could not; the inherited audit's 8 exact integer-only balancing blocks hold,
   and the mismatches track lacuna counts (mean 1.50 on balancing faces vs 3.20 on
   failing ones). This is prior scholarship, but it is not in doubt.
4. **HT34's `KI-RO 30` is the claimant's, and it is right.** Witness A's `37` was
   a tabulation defect that the edition has since corrected to `30 [[7]]`;
   Younger's table reads `30 [[7]]`. The claimant was right and the witness was
   wrong. Equally, **HT88's "+33 mismatch" is a sectioning artefact and must not
   be counted against the claimant** — I confirm validator 1 on both, from the raw
   face and the commentary.

---

## 4. Against the pre-registered criterion

> *"A coherent linguistic decipherment that accounts for a substantial portion of
> the corpus and is consistent with the known archaeological and historical
> context."*

- **"a coherent linguistic decipherment"** — not met, and expressly not attempted.
  Zero phonetic values, zero morpheme boundaries, no language or family, no
  reading of running text in any language. The claim's own status line and claim
  discipline say so.
- **"accounts for a substantial portion of the corpus"** — not met by two orders
  of magnitude. Reproducing the counts from the raw witness: 1 721 records,
  1 024 sign-group types, 2 520 tokens; the dossier is 10 tablets / 17 faces =
  **0.6 % of documents, 115 tokens = 4.6 %**; the whole programme assigns a
  function to **14 types = 1.37 %**, covering **104 tokens = 4.13 %**.
- **"consistent with the known archaeological and historical context"** — the only
  clause partly met. The hand, the three deposits and the LM IB horizon are used
  correctly and nothing contradicts the record. But the architecture is
  *transferred* from the Mycenaean Pylos Ma series, not recovered, and R2 shows
  that the transferred template fits 74 % of comparable archive slices.

---

## reasoning

The frontier claim fails the pre-registered criterion on every clause, which the
claimant concedes for the first. That alone settles the verdict against a PASS and
is not where the interesting disagreement is.

I record **FAIL rather than PARTIAL** because, having attacked it, I cannot find a
component of the *frontier claim itself* that is both Hub-originated and survives
a null:

- the eleven six-person gangs, the HT85b responsibility slots, the toponym/source-
  unit reading, A-DU as assessment, the HT87↔HT117 pairing, the supplying-unit
  reading of SA-TA/QIᶠ-TU-NE/MA-KA-RI-TE, the `97 = 65 + 31 + 1` identity and the
  1:2 manpower ratio are **sentences in the commentary file that ships beside the
  data file the Hub parsed** (R5, 16/16);
- the one genuinely synthetic contribution — assembling those into an eight-node
  architecture — is a **template that 74 % of size-matched random ten-tablet HT
  subsets instantiate in full** (R2);
- **"integrated … linking"**, the word the claim turns on, fails as a graph:
  5 edges of 45, four isolated tablets, p = 0.18, and the provisioning node hangs
  on a single syllabogram (R1);
- **roster checking** has 2/15 entity-level instantiation at p = 0.12 (R1b);
- one of the two "repeatedly encoded fixed manpower ratios" is **contradicted by
  its only other attestation in the corpus** (R3c), and the other leaves no trace
  anywhere in the archive's numbers (R3a–b);
- the cohesion that motivates treating the ten as a dossier **weakens further**
  when the null is drawn from the pool the claim is about (R4b);
- 15 % of the dossier table's factual cells are absent from the witness, and the
  two substantive ones assert the very sign identification the folder's own
  `PROGRESS.md` says must be plate-checked first (R4a).

What remains is real but is not the claim: a correctly attributed ten-tablet
Scribe-9 roster, a clean reproduction of KU-RO, the parser-direction correction to
an external negative control, and a now-substantial set of closed branches with
numbers attached. Those should be banked. They are not an integrated labour-
liability administration recovered from Linear A.

**Status: HELD — awaiting human sign-off.** Nothing here is recorded as solved.
`STATUS.md`, `board/PRACTICES.md`, `board/active/`, the claimant's `analysis/`,
`HANDOVER.md`, `PROGRESS.md` and the other validators' verdicts were not touched;
no git command was run.

---

## dissent

I read both prior verdicts before writing this, after my own runs were complete.

**1. I dissent from validator 1's PARTIAL, and side with validator 2's FAIL — but
on evidence v2 did not have.** V1 and I agree on every fact and differ only on
what PARTIAL is for. V1 kept PARTIAL for two Hub-side items: the parser-direction
correction to the external `kuro_test.py` negative, and the set of closed
branches. I accept that both are real. I still say FAIL, because **R5 removes the
rest of the ground PARTIAL would stand on**: not "published somewhere by someone",
but *written in `commentary/HT85.html`, `HT117.html`, `HT119.html` and
`HT122.html` in the same GitHub repository as the `LinearAInscriptions.js` the
Hub parses, by an author the Hub cites by URL twelve times in the same `analysis/`
directory*. A frontier that presents those as its main new result is not a partial
solve of Linear A; it is a restatement of its own data source's apparatus, with an
architecture laid over it that R2 shows fits three quarters of the archive.
A methodological correction and a list of closed branches are worth banking —
they are not a fraction of the claim under validation.

**2. I confirm validator 2's dissent item (b) by an independent route, and
strengthen it.** V2 predicted in advance that any co-validator reading the
Scribe-9 cohesion p < 0.01 as support would be reading an artefact of an unmatched
null. I reproduce that: size-matched p = 0.18 (all types) and 0.06 (strict), and
when the pool is correctly restricted to *attributed* tablets — a correction
neither v2 nor the inherited suite made — it degrades further to 0.23 and 0.08.
I also confirm Scribe 6 and Scribe 2 are comparably "cohesive".

**3. I confirm validator 2's dissent item (c) without reservation.** The folder's
negative results are its most valuable output, and this session adds to them:
HT97a as the falsifier of the 1:2 ratio, the 33 % base rate for modular prefixes,
the absence of any six-footprint, the 74 % template base rate, the dossier's
disconnected graph, and the 2/15 roster-check overlap. Each has a number attached
in `validation/2026-10-02-v3/out_refuter3b.txt` and should not be re-derived.

**4. Where I side with validator 1 against a stricter reading.** Two apparent
"claimant errors" are not: **HT88's +33** is a sectioning artefact of summing
across a forward-scoping heading, and **HT34's `KI-RO 30`** was right while the
digital witness was wrong. Neither should be counted as carelessness, and I would
dissent from any verdict that did. I also endorse v1's framing that the decisive
objection is internal rather than statistical — the ruling on HT117a makes the
KI-RO-scope result and the DI-KI-SE toggle mutually exclusive — and I verified
that ruling on the GORILA facsimile myself rather than taking it from v1.

**5. One place where I am the most generous member of the panel.** I report, and
do not bury, the one number that favours the claimant and that I could not break:
HT85a's leading run of four multiples of six has a simulated probability of
0.0004 under a corpus-like amount pool. I believe the 33 % archive-wide base rate
for *some* modular prefix is the honest comparator and that it dissolves the
result, but a reader who thinks *m* = 6 was fixed before HT85 was selected should
weigh it, and should know that no other validator reported it.

**6. I would dissent from any PASS, and from any verdict recording any part of
this as a decipherment.** On the criterion itself the panel is unanimous.
