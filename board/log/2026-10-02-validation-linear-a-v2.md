# Validation — Linear A, validator 2 (prior-art and independence)

```
claim: A "functional/historical solve candidate; not a phonetic decipherment or
       language-family solve" — that a substantial Haghia Triada / Casa del Lebete
       Linear A dossier written by HT Scribe 9 records an integrated labour-liability
       administration linking accountable units, personnel assessments, standardized
       six-person work groups, assignment, roster checking, KI-RO exception reporting,
       census-linked provisioning and hierarchical control totals; together with the
       wider "Minoan obligation circuit" state machine
       (DA-DU-MA-TA -> A-DU -> KI-RO -> KU-RO -> PO-TO-KU-RO, with KI-KI-RA-JA as an
       obligation-holder participant class).
problem: linear-a
criteria applied: "A coherent linguistic decipherment that accounts for a substantial
       portion of the corpus and is consistent with the known archaeological and
       historical context."
validator role: 2 (prior-art and independence)

reproduced: partially — specifics below
verdict: FAIL
```

## What I did

I was the panel's prior-art and independence validator, so I did not re-run validator 1's
reproduction as my own result. I read and ran the in-progress `validation/2026-09-25/
refute_scribe9.py` (it works offline against its vendored data; its C6 label-permutation
and C1 arithmetic output informed my reading of the claim but none of its numbers are
reported here as mine), then built a separate set of checks in
`historical-texts/linear-a/validation/2026-10-02-v2/`:

- `independence_checks.py`, `out.txt` — coverage, label permutation, prior-art ablation,
  information ceiling, run against a corpus copy fetched fresh on 2026-10-02.
- `external_overlap_map.csv` — element-by-element mapping of the claim against
  `dbourdeau/cyphersolver` `targets/lineara/` and against the published literature.
- `SOURCES.md` — provenance, hashes, and the edition-instability finding.

## (a) External overlap: the mandatory mapping

`dbourdeau/cyphersolver` `targets/lineara/` (NOTES.md, RESEARCH_REPORT.md,
LEADS_REPORT.md, retrieved 2026-10-02; hashes in `SOURCES.md`) is a ~68-round parallel
campaign on 1,722 records. Its sources are mwenge/lineara.xyz (the *same file* the Hub
uses), SigLA (the same database), Younger's commentaries, GORILA, Davis 2014, Corazza et
al. 2021, Salgarella, Steele — and `ChristosTsirkas/corpus-validation-for-undeciphered-
scripts-linear-a`, which is also the Hub's 2026-09-06 entry point. Corpus overlap is
effectively total on the material at issue; source overlap is near-total; and on the
Hub's flagship result, **test dependence is total**: both projects were pushed to the
"KI-RO is a forward-scoping heading" reading by the *same* Tsirkas `kuro_test.py`
negative result on KI-RO. The external notes say so in terms.

Mapped against the mandate's three categories:

**(iii) Already published elsewhere, therefore not a Hub result.** KU-RO = total and
PO-TO-KU-RO = grand total (established; both projects concede it). KI-RO in the
deficit/owing/missing family (received; Davis & Valério 2020 already propose
"missing/absent" for the HT117 1-lists; and the mwenge edition's own `translatedWords`
field glosses KI-RO as `"owed"`, U-MI-NA-SI as `"owed"?`, A-DU as `"assessment"?`).
**KI-RO as a forward heading with HT88 = 6, HT94b = 5, HT117a = 10 closed by KU-RO** —
`RESEARCH_REPORT.md` has the identical three-row table and the identical conclusion,
dated 2026-09-23, with the sentence "John Younger's commentary already identifies these
lists. This is replication, not discovery." The 19-node cyclic circuit is Davis &
Valério 2020 entirely. HT85's 11 × 6 is Younger, with the circuit-sector reading Davis &
Valério. KI-KI-RA-JA ~ KI-RO reduplication is Schürr 1976. A-DU = assessment,
U-MI-NA-SI = debt, HT28 as a balance ledger are the existing synthesis the claimant
cites. A-DU ~ `a-pu-do-si` and KI-RO ~ `o-pe-ro` are Chiapello's equations.

**(ii) Merely shared-source agreement.** Everything the two projects agree on about
KI-RO/KU-RO runs through one digital edition that carries Younger's glosses as data
fields, one palaeographic database, one third-party statistics repo, and the same
secondary literature, in the same week, both AI-assisted. That is one source counted
twice, not a second witness.

**(i) Independently corroborated.** Almost nothing of the distinctive claim — and the
one item that *is* genuinely cross-confirmed runs against it. The external project
checked 35 KU-RO/PO-TO-KU-RO totals with exact fractions across five windows and found
**10 balance**, naming HT94a 1, HT119 1 and the HT122 grand total among the failures.
The Hub's own 2026-09-25 session and this one independently reproduce exactly that
pattern. The hierarchical control-total architecture the dossier draws for HT122 does
not close on HT122's own entries.

**Two Hub supporting results are contradicted by the external work.**

1. The "status-switch controls" (DI-KI-SE, KU-PA₃-NU, PA-TA-NE, PA-JA-RE, SA-RU recur
   both inside and outside KI-RO contexts, therefore KI-RO is a status not a class) is
   the Hub's argument that KI-RO applies to ordinary roster members, and DI-KI-SE is
   called "the strongest status-switch control in the dossier". The external project
   tested that proposition *with a null* — hypothesis E24, "KI-RO entry words recur on
   other tablets" — and got **p = 0.87, not supported**. The Hub's version is five
   hand-picked recurrences and no null. Cross-tablet recurrence of entry words has a
   base rate, and the Hub never measured it.
2. HT123+124a, which the Hub grades "high" and counts among its 6/6 arithmetic controls.
   The external algebra shows that if KI-RO is additive to \*308, one conversion ratio
   holds across the first two rows, and the repeated fraction sign has one value, then
   subtraction gives `J·r = J − 1`, so `r = −1`: **no positive ratio satisfies the
   bundle**, and no choice of fraction value repairs it. The Hub fits *one* row with a
   freely chosen 1/3 ratio. No Hub file addresses this.

**And the external project supplies a simpler explanation of the Hub's central new
result.** Its rounds 18–19 establish, with nulls and BH correction, that recurring entry
words stay with one scribe (D20, p = 0.002; HT only 22 % vs 9 %; sides merged 17.6 % vs
4.4 %), that same-scribe tablets share vocabulary (E2/E3, p = 0.004, surviving sides
merged and transaction terms removed), and that scribes specialise in commodities
(p = 0.001) and transaction terms (p = 0.009). Its conclusion: "The Haghia Triada archive
was divided by scribe and subject." It also identifies Scribe 9 as the scribe who wrote
the most lists (W9). So "the same hand, repeated names and repeated header vocabulary
form a coherent dossier" is **one instance of a corpus-general, independently
null-tested scribal-department effect published elsewhere** — and the obvious
explanation of the cohesion is scribal assignment, not an obligation circuit. The
claimant never compared Scribe 9 against any other scribe.

## (b) Post-hoc decomposition: the label permutation was never run here, and it fails

No claimant file in `historical-texts/linear-a/` contains a permutation, a shuffle or any
null model of its own. I ran the test the orchestrator cross-reference names, literally:
every record keeps its own content in its own position, only the label moves. Sides
merged per the external counting note.

**The cross-class generalisation — the thing the cross-reference said must pass before it
is read as a result — does not survive.** Permuting only the `exception` / `ordinary`
label among the Scribe-9 tablets (exception = HT117, HT94; ordinary = HT122, HT85, HT87):

| statistic | observed cross-class shared types | null mean | null 95 % | p |
|---|---|---|---|---|
| strict (multi-sign, admin operators dropped) | 4 | 4.78 | [1, 8] | **0.697** |
| loose (every sign-group, as the dossier counts) | 5 | 7.58 | [3, 11] | **0.796** |

The observed value sits *below* the null mean in both. This is the Annals outcome (null
±144 against an observed 92, p = 0.183) reproduced on this corpus, and it is worse: only
**10 distinct label assignments exist**, so no permutation test on this split can return
p < 0.1 whatever the data says. The HT87 → HT117 "query grammar", the DI-KI-SE
status-switch edge and the HT122 ↔ HT94/HT117 cross-links all live on that split.

**The dossier-level cohesion is confounded with tablet size.** Scribe 9 is 10 of 137 HT
tablets but 114 of 846 HT-tablet sign-group tokens.

| statistic | observed | label permuted over all 137 HT tablets | length-matched (±10 % of 114 tokens) |
|---|---|---|---|
| strict, shared-type count | 9 | p = 0.0004 | **p = 0.018** |
| strict, mean pairwise Jaccard | 0.0077 | p = 0.033 | **p = 0.142** |
| loose, shared-type count | 13 | p = 0.0038 | **p = 0.122** |
| loose, mean pairwise Jaccard | 0.0173 | p = 0.374 | **p = 0.574** |

On the loose statistic the dossier actually uses, and on any size-normalised statistic,
the Scribe-9 cohesion is not distinguishable from a length-matched relabelling.

**And Scribe 9 is not singled out.** Scoring every HT tablet scribe with ≥ 3 tablets:
12 scribes, of which 2 clear p < 0.05 on shared-type count (Scribe 9 at 0.0002, Scribe 6
at 0.0027) and 2 on Jaccard. A within-scribe vocabulary effect exists at HT — exactly as
the external project found corpus-wide — and Scribe 9 is its largest instance because it
is the largest hand. Nothing marks it as an administrative system.

## (c) The information ceiling

Three distinctions the reading depends on, measured before any interpretation:

1. **Entry vs abbreviation for single signs.** 265 of 846 HT-tablet sign-group tokens
   (31.3 %) are one syllabogram; the commonest is NI (41), the conventional sign for
   figs. The board's own 2026-09-25 rule, now in `PRACTICES.md`, is that in an
   administrative corpus the shortest units are mostly not words, that an undeciphered
   corpus offers no principled way to separate abbreviation from word, and that the right
   verdict is *disqualified*, not cleaned. **The headline "eleven standardized
   six-person work gangs" lives entirely inside that disqualified region.** HT85b has 12
   sign-groups of which PA, KA and DI are single signs; 12 − 1 heading = 11 entries and
   66/11 = 6. Drop the single signs and both witnesses agree on 8 entries
   (SigLA gives 9 sequences, 8 after the heading), and 66/8 = 8.25. The gang size is a
   by-product of one unresolvable segmentation decision. HT94a is worse: 4 of its 7
   sign-groups are single signs (TA, NI, NI, NI). The external project independently
   leaves this open — single signs are not shown to be abbreviations of KU-RO/KI-RO/
   KA-PA/A-DU (pooled p = 0.73), and tablet single signs track common word syllables.
2. **Sign-group segmentation.** Across the eleven dossier faces the two editions share 85
   of 106 / 106 normalised types, Jaccard **0.669**. A third of the sign-groups the
   reading must place are not agreed to exist by both editions (HT85b `pa`/`ka`/`di`
   only-A; HT119 `a306tu`, `a327ju` only-B; HT122a `parine`, `a324dira` only-B).
3. **The exception / ordinary class label.** 10 possible assignments, so a floor of
   p ≈ 0.1 on any permutation test. The question is unanswerable from this corpus at this
   size regardless of what the tablets say.

To this I add a shared-reference problem specific to this claim: **the two "held-out"
semantic hits were scored against a labelled edition.** `LinearAInscriptions.js`'s
`translatedWords` field already contains `"owed"` on HT15, HT34, HT88, HT94b and HT117a,
`"owed"?` for U-MI-NA-SI, and `"assessment"?` for A-DU. A prediction frozen and then
checked against Younger's commentary in the same file that supplies the transcription is
not a held-out test of the prediction.

## (d) Coverage, and the criterion

| denominator | touched |
|---|---|
| corpus records (faces/objects) | 1,721 |
| distinct documents after merging faces | 1,599 |
| documents named anywhere in `analysis/` | **30 = 1.88 %** |
| the Scribe-9 dossier proper | **10 = 0.63 %** |
| sign-group tokens given any function by the 7-term lexicon | 68 / 2,420 = **2.81 %** |
| + the 10 further type-assigned sign-groups | 107 / 2,420 = **4.42 %** |
| sign-group *types* given any function | 16 / 971 = **1.65 %** |
| records containing any lexicon term | 52 / 1,721 = **3.02 %** |

On the most favourable denominator available — HT tablets only, ignoring the rest of
Crete and all non-tablet supports — the claim names 26 of 137 HT tablets (19.0 %), the
dossier is 10 (7.3 %), and the dossier's tokens are 114 of 846 (13.5 %).

Against the pre-registered criterion:

- *"a coherent linguistic decipherment"* — **not met, and not attempted.** The claim's
  own status line says "not a phonetic decipherment or language-family solve"; its claim
  discipline forbids "Linear A deciphered". No phonetic value, morpheme, word class or
  language is assigned to any sign-group. `PROBLEM.md`'s statement asks to "Recover the
  underlying language and produce reliable readings of the corpus". Nothing here is a
  reading in that sense; the state machine assigns *database fields*, as the claimant
  says.
- *"accounts for a substantial portion of the corpus"* — **not met.** 1.88 % of
  documents, 4.42 % of sign-group tokens, 1.65 % of sign-group types.
- *"consistent with the known archaeological and historical context"* — **partially met
  and partially unresolved.** The findspot and scribe metadata are used correctly and the
  claim is properly cautious about chronology. But the reading's arithmetic backbone is
  largely inconsistent with the corpus. Re-deriving every control total on the dossier
  tablets myself under a sectioning rule fixed before looking at outcomes (a block is
  every integer since the previous total marker on that face), 3 of 9 blocks close:
  HT85a 66, HT94b 5, HT117a 10. HT88 (+33) is a sectioning artefact and should not be
  counted against the claim. The remaining five are not: **HT94a +1, HT119 −1,
  HT122a −9, HT122b −50, HT122b PO-TO-KU-RO −32.** HT122 is the "master personnel
  liability/control register" and the showpiece of the hierarchical-control architecture,
  and **none of its three stated totals is the sum of the entries it stands over** — the
  quoted `31 + KU-DA 1 + 65 = 97` is arithmetic over stated totals only. This agrees
  with the external project's independent count (10 of 35 balance, with HT94a, HT119 and
  the HT122 grand total named). Separately, A-DU occurs at Khania (×2) and Tylissos as
  well as at HT, so it is a pan-Cretan administrative term, not a state of a Haghia
  Triada labour system.

## What survives, and should stand as progress rather than a solve

- KI-RO's forward-scoping construction and the three exact cardinality closures
  (HT88 = 6, HT94b = 5, HT117a = 10) are real. They are also a replication of Younger and
  of an external project that says so itself, triggered by the same third-party negative
  result. The Hub's honest contribution here is the *correction* of the Tsirkas
  parser-direction mismatch, which is a genuine and useful methodological catch.
- A small Scribe-9 lexical residue survives the ablation that removes Davis & Valério's
  19 published designations: 5 of the 9 shared types are DV19 members (and 17 of 19 DV19
  members also occur outside Scribe 9), leaving DI-KI-SE, MA-KA-RI-TE, MI-TU, PA-TA-NE,
  which still beat a length-matched null at p = 0.039. That is a real, small, non-prior-art
  signal — and it is consistent with the externally published generic scribe effect, not
  with an obligation circuit. One of the four is a header term, not a person.
- The negative results are the most durable thing in the folder: corpus-only
  language-family inference is underpowered here, and most HT totals do not close.

## Two construction problems the panel should see

**The claim's two reproducibility artefacts read no data.**
`analysis/kiro_construction_grammar.py` hard-codes a table whose rows are
`(record, following_token, observed_construction)` and then checks that `divider →
forward` and `numeral → scalar`. Since the table was typed consistently, the "9/9 clean
cases, 0 contradictions" result cannot fail and tests nothing against the corpus.
`analysis/kiro_residual_checks.py` is the same shape: its "held-out HT117 check" is
`sum([1]*10) == 10`, and its HT123 check asserts `Fraction(15,3)` — the very ratio the
external algebra shows cannot hold across adjacent rows. Both scripts run and both print
PASS; neither is a reproduction.

**The evidential base is an unpinned moving edition.** Between the 2026-09-25 vendored
copy and my 2026-10-02 fetch, twelve records of `LinearAInscriptions.js` changed,
including HT34, where `KI-RO 37` became `KI-RO 30 [[7]]`. The Hub's frozen check
`100 − 70 = 30` was written against an edition that read 37; the 30 came from Younger's
erasure reading, not from the transcription. It is correct now because the edition moved,
not because the claim verified it. No claimant file records a corpus version or hash.
`PROGRESS.md` also has no entry for 2026-09-08, so the current frontier's main result is
not in the progress log at all.

## reasoning (summary)

The claim fails the pre-registered criterion on every clause: it is not a linguistic
decipherment and does not claim to be, and it touches 1.88 % of the corpus. Beyond that,
the specific new structural result — the Scribe-9 cross-class generalisation — fails the
label-permutation test the folder's own orchestrator cross-reference said must be run
before it is read as a result (p = 0.70 and 0.80, observed below the null mean, on a split
that cannot produce p < 0.1 at any effect size). Its dossier-level cohesion is confounded
with Scribe 9 being the archive's largest hand and disappears under a length-matched
relabelling on the statistic the dossier actually uses. Its most load-bearing single
number, the 11 × 6 gang structure, depends on a segmentation the board's own rule declares
unresolvable. Two of its supporting results are contradicted by externally null-tested
prior art, and its central framing — same hand, shared vocabulary, therefore one
administrative system — is a corpus-general scribal-department effect established
elsewhere with proper nulls, for which the Hub offers no comparison against other scribes.
Everything that holds is prior art, replication, or a negative.

## dissent

Recorded in advance of the other two verdicts, because I expect to be the most negative
member of this panel.

1. **If the majority records PARTIAL, I dissent from any PARTIAL that credits the KI-RO
   construction grammar or the Scribe-9 dossier as a *Hub result*.** The KI-RO forward-scope
   reading is published in `dbourdeau/cyphersolver` dated 2026-09-23, derived from the same
   edition, the same commentary and the same third-party trigger, and that project labels
   it "replication, not discovery". A PARTIAL that rests on it is crediting the Hub with
   someone else's result reached from a shared source. I would accept PARTIAL only if it
   is restated as: *the Hub independently replicated a received structural reading, and
   correctly diagnosed a parser-direction error in an external negative control.*
2. **If a co-validator reproduces the Scribe-9 cohesion and reads p < 0.01 as support, I
   dissent.** That p-value is an artefact of an unmatched null. The label permutation must
   be length-matched, because the scribe label is confounded with tablet size, and it must
   be compared against the other eleven HT scribes. Done that way the effect is p = 0.12
   to 0.57 on the dossier's own statistic, and it is present for Scribe 6 as well.
3. **I do not dissent from crediting the folder's negative results**, which are its most
   valuable output and are now cross-confirmed by an independent campaign.

Per the role: posting this verdict and leaving the claim **HELD — awaiting human
sign-off**. `STATUS.md`, `PRACTICES.md`, the claimant's files and `board/active/` were not
touched; no git command was run.

### Artefacts

`historical-texts/linear-a/validation/2026-10-02-v2/` — `independence_checks.py`,
`out.txt` (P1 coverage, P2 label permutation, P3 prior-art ablation, P4 information
ceiling, P5 favourable-denominator coverage, P6 totals re-derivation),
`external_overlap_map.csv`, `SOURCES.md`, `data/LinearAInscriptions.js`.
