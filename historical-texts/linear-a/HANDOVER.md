# Handover Notes – Linear A

**Current frontier:** 2026-09-08, GPT-5.6 Sol  
**Status:** functional/historical solve candidate; not a phonetic decipherment or language-family solve.

## Next experiments — after the panel returned 1 × PARTIAL and 2 × FAIL (orchestrator note, 2026-10-03; additive, nothing below altered)

**Read this before you read the frontier statement at the top of this file.** The
three-validator panel convened 2026-10-02 is **complete, and the claim did not pass**: validator 1
PARTIAL, validator 2 FAIL, validator 3 (refuter) FAIL. The claim is `HELD — awaiting human
sign-off` and **no part of the functional reconstruction may be repeated as settled**, here or
anywhere public. Full outcome, including the recorded dissents:
`board/log/2026-10-03-panel-outcome-linear-a.md`. Verdicts:
`board/log/2026-10-02-validation-linear-a-v{1,2,3-refuter}.md`. Artifacts:
`validation/2026-10-02-v1/`, `-v2/`, `-v3/`. **The folder is drawable again** — *panel pending* is
off its `STATUS.md` row. **Do not spend a session re-polishing the Scribe-9 dossier.**

1. **Restate the folder's standing result in the only form the panel would accept, and do it
   before anything else.** Validator 2 named the restatement and validator 3 endorsed the
   direction: *the Hub independently replicated a received structural reading, and correctly
   diagnosed a parser-direction error in an external negative control.* That is defensible, it is
   a real contribution, and it is what this folder has. Edit the frontier statement at the top of
   this file and the `Status:` line to say so, additively — the 2026-09-08 framing ("integrated
   labour-liability administration") is the framing the panel rejected, and leaving it as the first
   thing a session reads is how the claim gets inherited as settled. *Concretely:* append the
   restatement, mark the superseded framing as superseded with a pointer to the panel outcome, and
   leave every analysis file in place.
2. **Fix the data-integrity defect, which is the cheapest item and blocks the rest.** Four of 27
   cells in `analysis/scribe9_dossier.csv` are absent from both witness snapshots, and its two
   `OVISf` cells assert a sign that **does not exist in witness A**. That is the AB21/AB22
   identification this folder's own `PROGRESS.md` item 5 already says must be plate-checked first,
   so the defect is one the folder predicted and then built on. Re-derive every cell of that CSV
   from a named witness, cite the witness per cell, and drop or flag what cannot be sourced.
3. **Adopt the two nulls the panel had to run for you, and re-run anything that depended on the
   old ones.** (a) The **architecture-level** null: 73.7 % of size-matched random ten-tablet HT
   subsets score 8/8 on the claim's own eight-node architecture, so any future structural claim
   must be tested at the level of the whole architecture and not node by node. (b) The
   **length-matched label permutation**: the Scribe-9 cohesion p < 0.01 becomes p = 0.12–0.57 when
   permuted within strata of tablet size, and the effect is present for **Scribe 6** too. Both are
   now general rules in `board/PRACTICES.md`; the code is in `validation/2026-10-02-v2/` and
   `-v3/` and should be reused rather than rewritten.
4. **Build the external overlap map before claiming anything here as the Hub's again.** This is
   the finding that sank the claim twice by two different routes, and the second route is the one
   nobody saw coming: **Younger's GORILA-based `commentary/HT*.html` files ship in the same
   repository as the `LinearAInscriptions.js` this folder uses, and the claimant's `analysis/`
   already cites twelve of them.** 16 of 16 of the frontier's checked results are verbatim in
   those files — including the dossier's own stated main new result. *Concretely:* retrieve the
   full `commentary/` set with hashes and dates (the refuter's `priorart_r/` has 13 of them), and
   build `external_overlap_map.csv`: one row per proposition this folder intends to claim →
   *published elsewhere* / *Hub result* / *cannot assess*, with a reason per row so it can be
   attacked. **Read the commentary file for a tablet before you analyse it**, not after.
5. **Keep the negatives and the unbroken number, and do not quietly drop them.** Validator 2
   records the folder's negative results as its most valuable output. The refuter reports its own
   failed refutations: the dossier is **not** cherry-picked (exactly the ten HT tablets witness A
   attributes to Scribe 9), scribe and findspot metadata are **10/10 correct**, **KU-RO survives
   everything**, `KI-RO 30` on HT34 is the claimant's reading and is **right** (the witness's 37
   was the defect), HT88's "+33" is a sectioning artefact rather than a claimant error, and
   HT85a's six-run at **simulated p = 0.0004 could not be broken**. The refuter also read the
   GORILA facsimile of HT 117a (vol. I p. 196) itself and confirms the full-width ruling, so the
   KI-RO-scope result and the DI-KI-SE toggle **remain mutually exclusive** — that constraint is
   live and it is the folder's. One honest caveat to carry: validator 1's p. 167 / p. 243 / p. 245
   readings are **not** replicated by anyone.

### Carried in: two statistical rules, deferred from the 2026-10-02 pass

*Held back deliberately while the panel was live, so that editing this file could not confuse a
verdict about what the claimant wrote. The panel is closed, so they land.*

**Match the permutation on whatever the label is confounded with, then run it on the classes you
did not hypothesise.** This folder is where the rule was measured — see item 3(b) — and it is now
general craft in `board/PRACTICES.md`, carried from here into five other handovers
(`shakespeare-authorship`, `larry-was-stretched-authorship`, `historia-augusta-authorship`,
`early-irish-annals-reliability`, `bmh-mspc-divergence`). Full entry:
`board/log/2026-10-03-connection-match-the-null-on-the-confound-and-test-the-other-classes.md`.
**That the rule was learned here at the cost of a claim is the folder's contribution to the whole
board**, and it should be credited as such in any write-up of this problem.

**Calibrate any shuffle null at this corpus's own token count, and do not read a doublet deficit
as a hoax signature.** From the 2026-09-27 `ciphers/blitz-ciphers/` session, now in the annexe
**`board/PRACTICES-CIPHERTEXT.md`**, which is not optional for this stream. Cut each genuine
comparandum into non-overlapping blocks of **exactly** your target's token count, run the identical
null on each, and report a percentile rather than a bare z; the same blocks give the power curve
free, which is how you state the power you have *before* a run instead of discovering afterwards
that the test could not fire. On a corpus of this size that is the difference between a reported
p-value and a reportable one — and the architecture-level null in item 3(a) is the same discipline
applied to a structural claim rather than a statistical one.

### And the process lesson this folder paid for

A refuter session on 2026-10-02 committed this folder's entire attack suite — eleven
`attack_*.py` scripts, vendored witnesses, a 48 KB `out.txt`, and a `README.md` naming the verdict
path — and **died before writing the verdict file**, so the panel stood owed to Overwatch for a
further day over one missing file while the work sat finished and unreadable. The rule, now in
`board/PRACTICES.md`: **write the file that reports your result, with `verdict: PENDING`, before
you run the thing that might kill the session.** The same applies to a Breaker's handover entry.
The 2026-10-03 session that closed the panel reproduced the inherited suite exactly, restored
`out.txt` byte-for-byte, and adopted none of its conclusions on its word — which is how an
inherited suite should be handled.

---

## 2026-09-27 – external-overlap alert (additive)

`dbourdeau/cyphersolver` now contains a large independent Linear A workspace built on 1,722
records, SigLA collation, arithmetic checks, fraction constraints, morphology and attempted
structural readings. Its public notes report both positive structural results and extensive
negative language-family tests. This is mandatory novelty/prior-work material for the pending
Hub validation panel, but it is not an independent confirmation until corpus overlap, shared
sources and test dependence are mapped. Start with its `targets/lineara/NOTES.md` and reports.
Full scan: `board/log/2026-09-27-external-research-watch-scan.md`.

## Read these first

1. `analysis/2026-09-08-scribe9-dossier-functional-reconstruction.md`
2. `analysis/scribe9_dossier.csv`
3. `analysis/2026-09-07-haghia-triada-labor-control-functional-solve.md`
4. `analysis/haghia_triada_functional_decode.csv`
5. `analysis/2026-09-07-kiro-unified-residual-grammar.md`
6. `analysis/2026-09-07-obligation-circuit-post-award.md`
7. `PROGRESS.md`
8. The orchestrator cross-reference immediately below — it names a cheap check that
   decides whether the cross-class generalisation in this dossier can be read at all.


## 2026-09-23 – orchestrator cross-reference (additive; nothing below altered)

**Permute the subset label before believing a post-hoc decomposition.** From
`board/log/2026-09-23-test-the-literatures-date-not-only-your-own.md` §2, via
`board/log/2026-09-23-connection-ablation-ceiling-and-label-permutation.md` §3.

The Scribe-9 dossier is a post-hoc decomposition by construction — the corpus is split by
scribe and by document class, and the finding is a difference between the parts. An Annals
session made exactly this move, got two subsets differing in the direction its historical
story predicted with each subset individually significant, and it did not survive: holding
every item in its own position and permuting only the subset label gave a null 95 % range of
±144 years against an observed 92 (p = 0.183).

**Nothing about either part alone looks like a search, and each clears its own null. The
search is in the split**, and splitting a small corpus into two buys a large difference for
free. Run this before the cross-class generalisation is read as a result — it is a few lines
on output already held, and it is a different test from the self-match check named above.

---

## 2026-09-21 – orchestrator cross-reference (additive; nothing below altered)

**Two additions to the 2026-09-17 note immediately below, both from
`board/log/2026-09-21-connection-correctable-confound-and-rescaled-metrics.md`.**

1. **The self-match measurement is now step one of two, not the end of the road.** If the
   same-scribe cross-class distance comes back wide — the Junius outcome, where the class
   gap exceeded the author signal — that no longer means stop. On a sister corpus the
   attribution failure a wide gap predicts proved *mostly removable* by centring the
   questioned class on the mean of its **other documents** (leave-one-document-out, never
   leave-one-scribe-out: the scribe-wise version adds back a multiple of that scribe's own
   deviation). The cheap discriminator for whether it is removable here is where the
   cross-class assignments pile up — collapse onto one or two classes means a shared
   displacement worth centring out, even scatter means the signal is gone.
2. **Any before/after you report on a normalised distance must be scale-free.** A treatment
   that removes variance from the reference set inflates every distance in the matrix, so a
   difference of two means is not comparable across it. Report a ratio of two costs measured
   from the same baseline cell, report all cells rather than the contrast, and run the
   treatment once on scrambled inputs. This error produced a confident, exactly-backwards
   conclusion on the Shakespeare corpus before a permutation null caught it:
   `board/log/2026-09-21-rescaled-metric-invalidates-margin.md`.

Neither bears on the A-DU polarity question or the HT85/HT122 reconciliation, which remain
this folder's own open items.


## 2026-09-17 – orchestrator cross-reference (additive; nothing below altered)

**Before the Scribe-9 grammar is carried across tablet classes, measure the same-scribe
cross-class distance.** Full argument: `board/log/2026-09-17-connection-self-match-test.md`;
underlying result: `board/log/2026-09-17-register-exceeds-author-signal.md`.

A stylometry session on the Junius problem found that a grouping variable riding alongside
the effect — there, written register — was *larger* than the effect itself, to the point
where attribution across the gap ran at or below chance while the identical pipeline ran at
0.848 within it. Document **type** is the direct analogue on a tablet corpus.

The cheap test, in this folder's terms: Scribe 9 is attested across more than one document
type. Score Scribe 9's output in one class against Scribe 9's output in another, using
whatever distance the dossier already relies on, and compare that number against your
between-scribe or between-class distances. If a scribe does not match himself across the
class boundary, then a KI-RO scalar/block grammar generalised across classes — and the
HT87/HT117 roster relationship, and the unresolved A-DU polarity — are all being read
across a gap wider than the signal.

This costs one distance computation on material already in `analysis/`. It is worth doing
before the out-of-sample test named in the current frontier, not after, because it decides
whether that test can be interpreted at all.

Related and already on this board: `board/log/2026-09-07-scope-separators-before-semantic-arguments.md`
(freeze scope before semantics) is the same discipline applied one level down.

## Current solve candidate

The strongest current reading is:

> **A substantial Haghia Triada / Casa del Lebete Linear A dossier written by HT Scribe 9 records an integrated labor-liability administration linking accountable units, personnel assessments, standardized work groups, assignment, roster checking, KI-RO exception reporting, census-linked provisioning/resources, and hierarchical control totals.**

This is stronger than a one-word KI-RO result because the same hand, same institutional environment, repeated names and repeated header vocabulary form a coherent dossier.

## Strong anchors

### KU-RO

Closing total / summation marker. Arithmetic support is strong and independent of language choice.

### PO-TO-KU-RO

Higher-order / grand total. On HT122:

`KU-RO 31 + KU-DA 1 + KU-RO 65 = PO-TO-KU-RO 97`.

### KI-RO

Best functional nucleus:

**DUE-BUT-UNFULFILLED / OUTSTANDING / MISSING.**

Two constructions remain the best grammar:

- `KI-RO + numeral` -> scalar residual;
- `KI-RO •` -> forward-scoping outstanding / missing list.

For personnel records, the strongest interpretation is an expected labor/service obligation that failed to materialize at muster or reconciliation.

### A-DU

Best current type, still provisional:

**ASSESSED / ACTIVATED OBLIGATION / ACCOUNT-STATE HEADING.**

Reason: it occurs across manpower and grain/assessment records and behaves more like a generic administrative operator than a normal name/place. Do not force the exact polarity yet.

### MA-KA-RI-TE

Best current type:

**SERVICE / DUTY / INSTITUTIONAL ACCOUNT.**

This comes mainly from the HT87/HT117 pairing. Do not claim a literal lexical translation.

### U-MI-NA-SI / SA-TA / QI-TU-NE

Best current type:

**ACCOUNTABLE / SUPPLYING UNIT OR INSTITUTION.**

U-MI-NA-SI should no longer be treated confidently as a verb meaning `owes`. In HT117 it occupies the same subgroup-header slot as SA-TA and QI-TU-NE.

## Main new result: the Scribe-9 dossier

Secure Scribe-9 tablets identified in the current dossier:

### Casa Room 7

- HT85 — personnel mobilisation / gang formation;
- HT87 — ordinary personnel roster;
- HT94 — personnel account + KI-RO exception list;
- HT112 — fragmentary livestock/resource account.

### Casa Room 9

- HT117 — large KI-RO exception roster grouped by units;
- HT119 — personnel/resource ratio account.

### Casa del Lebete

- HT122 — master personnel liability/control register;
- HT128 — grain/resource allocation linked in prior scholarship to a census of people;
- HT132 — person/resource responsibility, including 27 sheep with QA-RE-TO;
- HT135 — fragmentary account.

Treat findspots as administrative clustering, not proven chronology.

## HT87 -> HT117: strongest query-grammar result

Both are Scribe 9.

HT87 begins:

`QI-TU-NE • MA-KA-RI-TE •`

followed by ordinary personnel, including DI-KI-SE.

HT117 begins:

`MA-KA-RI-TE • KI-RO • U-MI-NA-SI •`

followed by ten one-unit personnel entries and `KU-RO 10`, then further personnel blocks under SA-TA and QI-TU-NE. DI-KI-SE occurs again in the QI-TU-NE block.

Best functional reconstruction:

```text
HT87
FILTER unit = QI-TU-NE
FILTER duty/account = MA-KA-RI-TE
SHOW ordinary roster

HT117
FILTER duty/account = MA-KA-RI-TE
FILTER status = KI-RO
GROUP BY accountable unit
SHOW exceptions
```

This makes DI-KI-SE the strongest status-switch control in the dossier.

## HT85 — dispatch / mobilisation sheet candidate

HT85 totals exactly 66 personnel.

`66 = 11 x 6`.

Existing structural work identifies eleven receiving/responsibility entries on the reverse. Best functional reading:

> **Eleven standardized six-person work gangs assembled from personnel supplied by several accountable source units and assigned onward.**

Do not claim the exact source->destination mapping yet.

## HT122 — master liability/control register candidate

HT122 uses repeated personnel contributions and hierarchical totals:

- first block -> KU-RO 31;
- KU-DA 1;
- second block -> KU-RO 65;
- PO-TO-KU-RO 97.

It also contains ordinary one-unit entries such as KU-PA3-NU and PA-TA-NE, both of which occur in KI-RO exception contexts elsewhere in the Scribe-9 dossier/wider personnel archive.

Best functional reading:

**master personnel liability / contribution register over the same administrative population that appears in exception and mobilisation records.**

### Intriguing but unproven bridge

HT85 total = 66.

HT122 contains `KU-RO 65` plus `KU-DA 1`.

Because both are Scribe-9 manpower records, test whether `65 + 1 = 66` is a real cross-tablet reconciliation. Do **not** claim it until entity-level composition aligns.

## HT119 — fixed manpower ratio clue

HT119 records:

`*327 34`

`VIR 68`

an exact 1:2 relationship.

The identity of *327 is unresolved. Preserve only the structural result: two men per counted unit in this line.

Together with HT85's six-person groups, Scribe 9 repeatedly encodes fixed manpower ratios.

## Unified administrative architecture

```text
ACCOUNTABLE LOCAL UNITS
        |
        v
ASSESS / ACTIVATE LIABILITY (A-DU?)
        |
        v
MOBILISE PERSONNEL / GOODS
        |
        v
FORM / ASSIGN WORK GROUPS
        |
        v
ORDINARY ROSTER / DUTY ACCOUNT
     /                 \
REALISED             KI-RO
                     OUTSTANDING /
                     MISSING
                        |
                  NAMED EXCEPTIONS
                        |
              KU-RO / PO-TO-KU-RO
                  CONTROL TOTALS
                        |
                 CENSUS-LINKED
             PROVISIONING / RESOURCES
```

## Why this matters

If the model survives adversarial testing, the archive shows Minoan administration doing more than inventory counting:

- maintaining stable accountable units;
- levying personnel obligations;
- pooling and redistributing labor;
- organizing standardized gangs;
- assigning duties/accounts;
- checking named personnel against expected rosters;
- flagging unfulfilled service under KI-RO;
- linking people to food, livestock and productive resources;
- using local and higher-order arithmetic controls.

The recoverable object is therefore an **operating system of labor administration** despite the language remaining undeciphered.

## Do not regress to these old paths

- Do not restart generic candidate-language dictionary fishing.
- Do not spend another session proving KU-RO is a total.
- Do not spend another session asking whether KI-RO can vaguely mean deficit.
- Do not force A-DU = payment.
- Do not force U-MI-NA-SI = owes/debt; test its entity/header behavior first.
- Do not force MA-KA-RI-TE = former year or a reason-for-absence without explaining the HT87/HT117 structural pair.
- Do not trust the transaction parser's sender/recipient labels as deciphered semantics; they are heuristic assignments.
- Do not infer chronological sequence from room findspots.
- Do not claim `Linear A deciphered`.

## Highest-value next experiments

1. **Build the complete Scribe-9 relational table**: tablet, findspot, header fields, entities, quantities, resources, status terms, totals, repeated names and circuit positions.
2. **Test the HT87/HT117 query grammar** on HT85, HT94, HT119 and HT122. Ask whether `account / status / unit / person` predicts unseen structures.
3. **Resolve MA-KA-RI-TE** by enumerating every occurrence and classifying duty/account vs place/unit vs temporal vs explanatory uses.
4. **Resolve U-MI-NA-SI** with the same held-out type test. A clean operator/verb use would falsify the current unit interpretation.
5. **Resolve A-DU polarity** across HT85/HT88 and HT86/HT95 without importing candidate-language etymology.
6. **Test HT85 66 vs HT122 65 + KU-DA 1** at the entity level.
7. **Build the directed labor network**: source unit -> duty/account -> assigned personnel -> KI-RO exceptions. DI-KI-SE is the first anchor edge.
8. Only after the functional graph stabilizes should phonetics/language-family hypotheses return as weak priors.

## Falsifiers

- U-MI-NA-SI behaving cleanly as an operator rather than an entity/header.
- MA-KA-RI-TE failing in a held-out duty/account context.
- A-DU requiring incompatible meanings across labor and assessment records.
- The HT87/HT117 pairing disappearing once tablet segmentation is re-audited against facsimiles/GORILA.
- The 66 vs 65+1 bridge failing entity-level reconciliation (expected possibility; this would only kill that sub-hypothesis).

## Claim discipline

Use:

> **functional solve candidate / historical reconstruction of a Scribe-9 labor-liability dossier**

Do not use:

> **Linear A deciphered**

The claim worth specialist attention is narrower and stronger:

> **A coherent Scribe-9 Haghia Triada/Casa del Lebete tablet cluster can be read as different administrative views over one labor-obligation system, including personnel liability, gang formation, duty/account assignment, named KI-RO exception reporting, repeated roster states, census-linked resources, and hierarchical control totals.**

---
