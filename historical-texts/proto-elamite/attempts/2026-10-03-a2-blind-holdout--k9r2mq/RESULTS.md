# Tier A2 and the blind-holdout warrant — 2026-10-03 (Breaker, stream B draw)

**Drawn pick:** `historical-texts/proto-elamite`, stream B, coverage debt 12.6.
**Drawn next move (item 1 of the 10-03 reconciliation handover):** give four of the
six tier-A2 pairs the blind-holdout warrant they lack.
**Corpus:** SFU `pe-sign-value-data` @ `538949cc` (two commits total; remote HEAD
re-verified this session). LF digest `8849716c6afbf963…`, matching the handover's
note that the digest in `associations.json` is a CRLF/Windows artefact.
**Plus:** live CDLI export, fetched 2026-10-03T18:45Z, 508,015 bytes / 1,597
inscriptions, sha256 `2521a4ff45db98be6ef9c6845dcb8069ebf539a82375f39cb3817445394a94fe`.
**Model/platform:** Anthropic Claude Opus 5, Claude Code cloud session. **Trial ID: none.**
**Starting revision:** `31d0584`.

---

## Headline

1. **The drawn item's premise is wrong, and the correction is the session's first
   result.** Tier A2 pairs do not "lack a blind screen". Four of the six are inside
   the pre-specified family of 54 and **already failed the pre-specified blind test**
   — BH q over base 54 of **0.095 (M288–N39B), 0.202 (M288–N24), 1.0 (M376–N08A),
   1.0 (M370–N39B)**. The other two, **M288–N14 (train OR 2.27, below the OR ≥ 3
   gate) and M362–N14 (train q = 0.0226, above the q ≤ 0.01 gate), are screened
   OUT by the unchanged 2026-09-04 rule** and cannot be promoted under it at all.
   The handover listed four pairs as "promotable"; two of those four are not even
   candidates. Its power table is correct — it measures marginals — but power to
   test is not a licence to test, and the test it licensed had already been run.
2. **A pre-registered 5-fold cross-fit does supply the missing warrant, to three
   pairs.** Running the published rule five times over the hash buckets already in
   the design — screen on four, test on the fifth — reproduces the published eight
   exactly on fold 1 (the gate) and, on folds 2–5 which **no session in this folder
   has ever computed**, warrants **M288–N24 (3 of 4 folds), M288–N39B (2 of 4) and
   M376–N08A (2 of 4)**. All three survive the composition control run *inside the
   blind buckets*. This is the folder's first new held-out constraint since 2026-09-04.
3. **A pair can cross-validate perfectly and still be a pure composition artefact.**
   **M263–N01 confirms in 4 of 4 blind folds** — more than any other pair in the
   table — and is **refused by the composition control with power** (Mantel–Haenszel
   OR **1.39** against a crude OR of **6.70**; p = 0.34, floor 3e-06). Cross-fitting
   buys power, not confound control. The tier-C demotions stand.
4. **The novelty gap closes, negatively, for the two signs that carry the folder's
   headline.** **Born, Monroe, Kelley & Sarkar, "Disambiguating Numeral Sequences to
   Decipher Ancient Accounting Corpora", CAWL 2023, pp. 71–81, §5** — open access
   since 2023, never cited here — already report:

   > "Entries ending in M288 have the largest capacity magnitudes on average,
   > while those ending in M263 are among the smallest."

   Reproduced independently this session with a raw-multiplier proxy: of 110 M
   families clearing the 20-line bar, **M288 ranks 5th (96th percentile)** and
   **M263 ranks 98th (11th percentile)**. The folder's M288 enrichment family and
   its M263–N01 result are the sign-level shadow of a published magnitude fact.
   **They are not reducible to it** — every M288 pair survives magnitude
   stratification — but the relation is prior art and must be cited.
5. **The 2026-09-04 design is far more conservative than its nominal level**, which
   is the measured mechanism behind "the published eight is a power-limited sample".
   Across 500 replicates of a null that holds the real screen fixed and permutes the
   test arm, the whole 4-fold pipeline produced a mean of **0.03** confirmed pairs
   and **not one replicate in 500 put any pair in ≥ 2 of 4 folds**.

---

## Gates — five, all exact, before anything downstream was believed

| Gate | Result |
|---|---|
| Corpus audit vs 2026-09-04 | 1,467 files / 10 empty / 1,457 tablets / 11,013 numbered lines / 4,869 eligible / 1,050 holdout — **exact** |
| The published 15 associations | reproduced **field-for-field, 0 mismatches** over every float at 1e-12 |
| 2026-09-17 face-blocked table | all **80** values (8 pairs × 2 schemes × 5 quantities) to 1e-12 |
| Screen enumeration | **1,056 tested / 54 selected** — third independent confirmation, set-identical |
| Published validation arm on the 54 | returns **exactly the published eight** |
| numpy fast path vs audited path | identical confirmed sets on **all 5 folds** |

The screen's correction base is **54**, not 8 and not 16. `src/screen.py` recovers
it by enumeration from the audited parser rather than trusting any handover figure.

---

## Part 1 — the drawn test, run as specified, declared exploratory

Bucket 0 already carried the published validation arm, so a different statistic on
it is a **statistic swap on seen data**, not a warrant. Recorded as such in advance.
All three frozen predictions held.

| pair | train OR | tablet p / q | face p / q | co-numeral p / q |
|---|---:|---|---|---|
| M288–N39B | 3.91 | 0.01591 / 0.0954 | 0.02796 / 0.1516 | **1.34e-05 / 0.00036** |
| M288–N24 | 4.81 | 0.03742 / 0.2021 | 0.02691 / 0.1516 | 0.2162 / 0.8148 |
| M376–N08A | 146.27 | 1 / 1 | 1 / 1 | 1 / 1 |
| M370–N39B | 0.21 | 0.7051 / 1 | 0.8182 / 1 | 0.736 / 1 |

*(q is BH over the real base of 54.)*

**The unplanned finding here is about the criterion, not the pairs.** Applying the
handover's own proposed bar — face **and** co-numeral at q ≤ 0.05 over base 54 on
bucket 0 — to the **published eight** retains **only M297–N39B**. M288–N45, the
flagship, has **no face power at all** on bucket 0 (floor = 1.0). A promotion
criterion that demotes seven of the eight constraints it was meant to extend is
mis-specified for 1,050 lines. That is why Part 2 exists.

## Part 2 — pre-registered 5-fold cross-fit (the warrant)

Unchanged rule, unchanged bars, unchanged test; only the held-out bucket rotates,
and BH is taken within each fold over that fold's own selected set.

| fold | test bucket | train / test lines | tested | selected | confirmed |
|---|---|---|---|---|---|
| 1 *(gate)* | 0 | 3819 / 1050 | 1056 | 54 | **8 = the published eight** |
| 2 | 1 | 3954 / 915 | 1080 | 47 | 9 |
| 3 | 2 | 3662 / 1207 | 1080 | 41 | 6 |
| 4 | 3 | 4043 / 826 | 1222 | 53 | 8 |
| 5 | 4 | 3998 / 871 | 968 | 51 | 3 |

**16 distinct pairs confirmed in ≥ 1 of folds 2–5**; 6 reach ≥ 2 folds:

| pair | blind folds | status |
|---|---|---|
| M263–N01 | **4 of 4** | published; **refused by the composition control** (see Part 6) |
| M288–N24 | 3 of 4 | **A2 → blind-warranted** |
| M297–N39B | 3 of 4 | published, tier A1 |
| M263–N30C | 2 of 4 | published |
| M288–N39B | 2 of 4 | **A2 → blind-warranted** (but see Part 5) |
| M376–N08A | 2 of 4 | **A2 → blind-warranted** (2 strata only — fragile) |
| *10 further pairs* | 1 of 4 each | reported as a **count**, not as findings |

**M106–N24, which the tier table places in A1, confirms in 0 of 4 blind folds.**
**M288–N45, the flagship, confirms in 1 of 4.** Neither is refuted by that — the
folds are small — but A1 is not a uniformly robust tier.

Frozen predictions: P2.1 (gate) **held**; P2.2, P2.3, P2.4, P2.5 **held**;
**P2.6 refuted** — M297–N24 confirmed in 1 of 4 blind folds, not the ≥ 2 I
predicted. I expected a composition artefact to replicate reliably under a design
that does not control composition. It did not, so fold-replication count is a
weaker proxy for "artefact" than I assumed, and Part 6 had to do that work directly.

## Part 3 / Part 4 — two nulls

**Null A** (whole-corpus within-tablet permutation of numeral sets, full pipeline
re-run, 500 replicates): union mean **0.01**, median 0, p99 **1**, max **1**, against
**16** observed; exact p = **0.002** (floor-limited by 500 replicates). All three
predictions held. Weak, though: under it the *screen itself* finds nothing.

**Null B** (real screen held fixed in every fold, test bucket permuted, 500
replicates) — gated against `crossfit.json` on all 5 folds first:

| quantity | null mean | null p95 | null max | observed |
|---|---:|---:|---:|---:|
| pairs in ≥1 of 4 blind folds | 0.03 | 0 | 3 | **16** |
| pairs in ≥2 of 4 blind folds | 0.000 | 0 | **0** | **6** |
| singletons | 0.03 | — | — | 10 |

P(any pair reaching ≥2 of 4 blind folds under the null) = **0.0000** over 500
replicates. Exact p for the ≥2 count = **0.002**.

**P4.1 and P4.5 both failed, and they failed informatively.** I predicted BH at
q ≤ 0.05 over ~48 candidates in each of 4 folds would produce 1–12 false
confirmations and ≥ 1 false singleton. It produces **0.03**. My error was
conflating a per-test α with FDR control: under the global null BH bounds
P(any rejection) near 0.05 per fold (~0.2 expected over four), and the realised
rate is another ~7× below even that, because the confirmation criteria are
conjunctive (BH **and** |OR| ≥ 1.5 **and** ≥ 5 validation sign-lines **and**
direction agreement) and the exact test is discrete, so many candidates have no
power at all. **Consequence: the 10 singletons are not noise either** — but with
the per-fold false rate this low, a singleton's weakness is a power statement, not
a contamination statement, and I still decline to name them per the frozen rule.

## Part 5 — the independent CDLI corpus (handover item 2, discharged)

CDLI is **back up**: homepage HTTP 200; the export route returned 508,015 bytes /
1,597 inscriptions — byte-count-identical to `u82zig`'s 2026-10-01 fetch.
`cdli_compat.py` reproduces that session's report exactly (11 tablets differing on
eligible-line count; M288 557→558, M263 191→190, N39B 621→620, N01 3585→3587; the
N08→N08A rename). **130 new tablets, 576 lines, 109 eligible** — `u82zig`'s figures
confirmed. N08 merged into N08A, policy stated.

| pair | a | b | c | d | corrected OR | direction | face floor |
|---|---:|---:|---:|---:|---:|---|---|
| M288–N24 | 0 | 9 | 3 | 97 | 1.47 | agrees | 0.67 |
| **M288–N39B** | **0** | 9 | 19 | 81 | **0.22** | **OPPOSITE** | 0.33 |
| M376–N08A | 0 | 2 | 0 | 107 | 43.00 | agrees | 1.0 |
| M288–N45 | 1 | 8 | 1 | 99 | 11.71 | agrees | 0.33 |
| M297–N39B | 2 | 2 | 17 | 88 | 5.06 | agrees | 1.0 |
| M106–N24 | 0 | 1 | 3 | 105 | 10.05 | agrees | 1.0 |
| M263–N01 | 3 | 2 | 50 | 54 | 1.51 | agrees | 0.17 |

**P5.2 held: 0 of 7 pairs have face-blocked power at 0.05** — predicted in advance
so that a null result could not be re-described afterwards as a refutation.
**P5.1 failed: M288–N39B points opposite** (zero co-occurrences on 9 M288-bearing
lines where ~1.6 were expected). By the rule frozen before the fetch was parsed, a
direction opposing **without power does not fire the reopening condition** — but it
is the one discordant signal against the session's strongest new pair and it is
recorded as such, not smoothed over. P5.3 was ill-formed: M288–N24 and M288–N39B
share M288 and therefore tie at 9 M-bearing lines, so "the most" was not a
well-defined prediction. My error in framing.

## Part 6 — the composition control inside the blind buckets

`c7h0lh` ran this control on the **full** eligible corpus, which contains the
training data that selected these pairs. Here it runs on blind buckets 1–4 only.

| pair | blind folds | crude OR | MH OR | p | floor | strata | verdict |
|---|---|---:|---:|---|---|---:|---|
| M288–N24 | 3/4 | 4.81 | 3.61 | 1.2e-08 | 1.5e-80 | 20 | **SURVIVES** |
| M288–N39B | 2/4 | 3.91 | 3.62 | 1.4e-14 | 5.2e-157 | 21 | **SURVIVES** |
| M376–N08A | 2/4 | 146.27 | 104.92 | 2.2e-19 | 1.9e-31 | **2** | SURVIVES (fragile) |
| **M263–N01** | **4/4** | **6.70** | **1.39** | **0.343** | 3e-06 | 4 | **REFUSED, with power** |
| M297–N39B | 3/4 | 9.07 | 3.36 | 4.9e-10 | 1.9e-150 | 21 | SURVIVES |
| M288–N45 | 1/4 | 12.70 | 5.83 | 6.2e-09 | 2.5e-36 | 12 | SURVIVES |

P6.1, P6.3, P6.4 held. **P6.2 failed**: I predicted M376–N08A would get no usable
pooled verdict; its floor is 1.9e-31 on only 2 informative strata, because those
two strata are large. The verdict is usable and the pair survives — but a survival
resting on 2 strata is the most fragile entry in the table and `ux87d8`'s warning
about this pair stands.

**P6.4 is the session's most transferable result.** M263–N01 is the single
best-replicating pair in the whole cross-fit and the composition control refuses it
with power. Blind replication and confound control are orthogonal; neither
substitutes for the other.

## Part 7 — the rival explanation from the literature

**Step 1, reproduction of Born et al. §5** (raw-multiplier proxy; *not* their
system-disambiguated capacity measure, so agreement is corroboration and
disagreement would be weak evidence of my error, stated before running):
110 M families clear the 20-line bar. **M288 rank 5/110, mean 4.20** (top of the
list: M348 5.75, M056 5.47, M362 4.87, M327 4.23, M288 4.20). **M263 rank 98/110,
mean 1.97.** **P7.1 held** — their finding reproduces.

**Step 2, magnitude-stratified exact test, blind buckets 1–4**, bins fixed on
magnitude alone before looking at any association:

| pair | crude OR | MH OR | p | strata | verdict |
|---|---:|---:|---|---:|---|
| M288–N39B | 3.91 | 3.20 | 1.1e-19 | 7 | SURVIVES |
| M288–N24 | 4.81 | 3.79 | 8.9e-15 | 7 | SURVIVES |
| M288–N14 | 2.27 | 1.77 | 2.1e-06 | 7 | SURVIVES |
| M288–N45 | 12.70 | 10.38 | 1.3e-17 | 7 | SURVIVES |
| **M263–N01** | 6.70 | **8.90** | 1.6e-14 | 5 | **SURVIVES** |
| M376–N08A | 146.27 | 140.23 | 2.1e-48 | 6 | SURVIVES |
| M297–N39B | 9.07 | 9.92 | 6.5e-43 | 7 | SURVIVES |

**P7.2 held, P7.3 failed — and the failure is the informative part.** M263–N01
survives *magnitude* stratification (MH OR 8.90) while being refused by the
*co-numeral* control (MH OR 1.39). The two controls disagree, and that localises
the confound precisely: M263–N01 is not explained by M263 lines being small, it is
explained by **which other numeral signs are present** — M263 lines carry N01 and
little else. "Numeral-poor" was the right diagnosis; "small-magnitude" is not.

*Numerical note:* several floors here are at or below double-precision underflow
(M288–N39B shows 0, M288–N14 shows 1.4e-321, subnormal). The reported p-values
(1e-19, 2e-06) are nowhere near underflow and the verdicts do not depend on the
floors; the floors are reported as computed.

---

## Priority / novelty — handover item 3, partially discharged

All DOIs and author lists re-verified against Crossref and the ACL Anthology
`.bib` files by me, not accepted from a researcher.

- **Born, Logan; Monroe, M. Willis; Kelley, Kathryn; Sarkar, Anoop**,
  "Disambiguating Numeral Sequences to Decipher Ancient Accounting Corpora",
  **CAWL 2023, pp. 71–81**, `https://aclanthology.org/2023.cawl-1.9.pdf` (HTTP 200,
  open access). **§5 contains the M288 / M263 magnitude finding quoted above.**
  Also an arXiv version, `arXiv:2502.00090`. **This is the prior art that matters
  and no session here had cited it.**
- **Born, Kelley, Monroe, Sarkar**, "Compositionality of Complex Graphemes in the
  Undeciphered Proto-Elamite Script…", Findings of ACL-IJCNLP 2021, pp. 4136–4146,
  `https://aclanthology.org/2021.findings-acl.362.pdf`. Mentions M288 13×; inferential
  vocabulary: none beyond one use of "enrich".
- **Born, Monroe, Kelley, Sarkar**, "Sequence Models for Document Structure
  Identification in an Undeciphered Script", **EMNLP 2022** (not 2023), pp. 9111–9121,
  `https://aclanthology.org/2022.emnlp-main.620.pdf`.
- **Born, Monroe, Kelley, Sarkar**, "Learning the Character Inventories of
  Undeciphered Scripts Using Unsupervised Deep Clustering", CAWL 2023, pp. 92–104,
  `https://aclanthology.org/2023.cawl-1.11.pdf`. Names none of the signs at issue.
- **Born, Kelley, Kambhatla, Chen, Sarkar**, "Sign Clustering and Topic Extraction
  in Proto-Elamite", SIGHUM 2019, pp. 122–132, `https://aclanthology.org/W19-2516.pdf`.
  **Settled by enumeration, not keyword search:** all 16 numeral-sign mentions in the
  paper fall inside a single illustrative transliteration figure spanning characters
  7126–7333. The paper contains **zero** occurrences of Fisher, significance,
  p-value, held-out, validation, Benjamini, permutation or null hypothesis. It claims
  no M-family × numeral association. *(Its sample figure does happen to contain
  `M056~f M288 , 1(N45) 1(N14)` — the flagship pair inside a worked example. That is
  an illustrative transliteration, not a claim, and is noted here so nobody later
  finds it and reads it as prior art.)*
- **NEW to this folder: Kelley, Born, Monroe, Sarkar**, "On Newly Proposed
  Proto-Elamite Sign Values", *Iranica Antiqua* **LVII (2022)**, `10.2143/IA.57.0.3291506`,
  open-access PDF at `https://anoopsarkar.github.io/papers/pdf/IA57001.pdf` (HTTP 200).
  **It names M288 91 times and M263 64 times** and applies Desset et al.'s Linear
  Elamite values to the PE corpus. **Not read this session. It is the largest
  remaining novelty exposure and it is now the folder's next move.**
- **Monroe, Kelley, Born, Sarkar**, "Recent Progress in Deciphering Proto-Elamite",
  *Near Eastern Archaeology* **88(4):314–323**, 2025-12-01, `10.1086/738240`.
  Crossref re-verified (four authors, University of Chicago Press). **Confirmed
  closed** by two independent services: OpenAlex (`is_oa=false`, `oa_status=closed`,
  no repository full text) and Unpaywall (`is_oa=false`, `oa_locations=[]`).
  Publisher landing page and PDF both HTTP 403. **Still unread.**
- **Kelley, Kathryn**, *Proto-Elamite: Writing and Society in Early Iran*, Cambridge
  Elements, 2026-07-18, `10.1017/9781009614559`. Crossref re-verified (monograph,
  CUP). Only the summary and reference list are reachable; **still unread**.

## Frozen-prediction record

**27 predictions frozen across five commits before the code that tested them
existed: 20 held, 6 failed, 1 ill-formed.** The failures — P2.6, P4.1, P4.5, P5.1,
P6.2, P7.3 — are each discussed where they fall. Freeze commits: `dc1802b`
(Parts 1–3), `5afe79f` (Part 4), `055bd8d` (Part 5), `28fff42` (Part 6),
`9d2dba1` (Part 7).

## Reproduction

```bash
git clone https://github.com/sfu-natlang/pe-sign-value-data   # @ 538949cc
cd historical-texts/proto-elamite/attempts/2026-10-03-a2-blind-holdout--k9r2mq
C=/abs/path/to/pe-sign-value-data/corpus
python3 src/screen.py $C            # 1056 tested / 54 selected
python3 src/published_arm.py $C     # the published eight
python3 src/part1_bucket0.py $C     # Part 1, BH over 54
python3 src/crossfit.py $C          # Part 2, gate + folds 2-5     (~41 s)
python3 src/verify_fast.py $C       # fast path == audited path
python3 src/null_model.py $C 500    # Null A                        (~7 min)
python3 src/null_b.py $C 500        # Null B                        (~6 min)
python3 src/part6_composition.py $C # Part 6
python3 src/part7_magnitude.py $C   # Part 7
# Part 5 needs the live export:
curl -sS 'https://cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions&limit=3000' -o pe_all.atf
python3 ../2026-10-01-block-aware-split--u82zig/cdli_fetch.py pe_all.atf /abs/cdli-corpus
python3 src/cdli_new.py $C /abs/cdli-corpus
```

Both nulls are seeded (`20261003`). The live CDLI export is not committed — it is
CDLI's data; the route, the timestamp, the byte count and the sha256 above are
what make the run repeatable.

## What a validator should attack first

1. **The cross-fit's fold dependence.** The five training sets overlap by ~75%, so
   the folds are not independent and "confirmed in k of 4" is not a binomial count.
   Null B prices this correctly *by construction* (it re-runs the same dependent
   design) but a validator should check that claim rather than take it.
2. **M376–N08A's two strata.** The pair survives every control, with 2 informative
   co-numeral strata and 0 informative face blocks on bucket 0. If any single entry
   in this session's table is an artefact, it is this one.
3. **M288–N39B's CDLI direction reversal.** Underpowered, but it is the one
   independent corpus and it points the wrong way.
4. **My magnitude proxy is not Born et al.'s measure.** I sum raw ATF multipliers
   across number systems; they disambiguate systems first. The rank agreement
   (M288 5/110, M263 98/110) is corroboration, not reproduction.
