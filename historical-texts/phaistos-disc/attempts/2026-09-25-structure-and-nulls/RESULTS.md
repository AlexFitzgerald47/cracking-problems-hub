# Phaistos Disc — structure, nulls and a refuted prediction
### 2026-09-25, cracker session (Claude Opus 5). Starting mode: the folder was a seed.

Everything here is reproducible from `src/` against `data/`. Run order:
`build_corpus.py` → `reproduce.py` → `flatness.py` → `structure.py` → `repeats.py` →
`position.py` → `power.py` → `genre.py`. Predictions were frozen in `FREEZE.md`, committed
before any test ran and before any comparison corpus was on disk.

## Summary in one paragraph

The Disc is now workable: a three-way-verified transcription, a pipeline that reproduces the
published census blind, and eight tests with nulls. **One result appears to be new** — the 18
groups bearing the oblique stroke are formulaic as a class, repeating among themselves at
p = 4.5e-5 against a length-stratified label-permutation null, while the section-*initial*
slot shows nothing (p = 0.58). **Three results reproduce published work independently**,
including a five-week-old paper this session nearly claimed to have discovered. **One frozen
prediction was refuted**: the Disc's groups are *not* anomalously long once Linear B is the
comparison, and the "groups are too long to be words" argument should not be used again.

## 1. Corpus (`build_corpus.py`, `reproduce.py`)

Three *separately published* transcriptions were parsed and diffed: Achterberg et al. 2004
(Evans numbers), Everson & Jenkins 2006 (Unicode), Godart 1995 (pictorial, with explicit word
labels). **They agree exactly** — all 61 sign sequences and all 18 oblique strokes.

| | |
|---|---|
| groups | 61 (side A 31, side B 30) |
| sign slots | 242; legible tokens 241; one illegible sign in A8 |
| distinct signs | 45 (Evans 01–45, all attested) |
| oblique strokes | 18 |
| group lengths | 2:6, 3:16, 4:21, 5:13, 6:2, 7:3 — mean 3.967, **no 1-sign group** |

Blind reproduction of published descriptive claims: **14/15 pass**. The 15th is an error in
the source, not the pipeline — the hapax sign 43 is in group **B6**, not B4 as the Wikipedia
prose states; the labelled pictorial transcription and two independent passages in the same
article (the corrections list for B4, B10, B13) confirm B6.

## 2. F1 — the flatness test the handover asked for. Frozen prediction, confirmed.

The 2026-09-24 handover asked for the gold-bar "too flat" test with its p-floor computed
first. Frozen prediction: it would **not** transfer. It does not.

- expected count/cell 241/45 = 5.36, so the chi-square asymptotics are marginal → simulated
  null (B = 200,000, **p-floor 5.0e-6**), not the analytic tail.
- **chi2 vs uniform = 194.25** on 44 df, against a simulated null mean of 44.0 and a 95 %
  range of [27.7, 64.3]. P(chi2 ≥ observed | uniform) < 5e-6.
- **IC (normalised, uniform = 1.0) = 1.626**, null 95 % range [0.932, 1.084].

The Disc's sign counts are strongly **peaked**, not equalised. Sign 02 occurs 19 times
against a uniform expectation of 5.36. **Negative transfer, recorded as such**: the gold-bar
finding does not carry here. Per that entry's own same-day correction, this is
P(data | uniform) and not P(data | cipher); it identifies neither script nor language.

## 3. H1 — the section-final slot is formulaic. This is the new result.

The oblique stroke is standardly read as a section or "paragraph" terminator (Evans 1909;
Duhoux 1977b — see §6 on what I could and could not verify). Statistic:
`S = marked tokens − distinct marked types`. Null: permute **which groups carry the stroke**,
holding the group sequence and multiset fixed — one thing permuted.

| set | tokens | distinct | S | redundancy | mean length |
|---|---|---|---|---|---|
| stroke-marked | 18 | 13 | **5** | 27.8 % | 3.67 |
| unmarked | 43 | 40 | 3 | 7.0 % | 4.09 |

| null | S | null mean | p |
|---|---|---|---|
| N1 free label permutation | 5 | 0.728 | 5.5e-5 |
| **N2 length-stratified** | 5 | 0.650 | **4.5e-5** |
| N3 stratified, A24 crack dropped | 5 | 0.579 | 4.0e-5 |

- Pre-registered failure condition was p > 0.01 under N2. Pre-registered search budget was
  25 combinations, needing p < 4.0e-4. **N2 clears the budget-charged threshold by ~9×.**
- **0 of the 7 repeated group types straddle the marked/unmarked boundary.** Four are wholly
  marked (`02-12-31-26` ×3 at A16/A19/A22; `28-01` ×2; `29-45-07` ×2; `22-29-36-07-08` ×2),
  three wholly unmarked. No counterexample.
- **The control that matters:** the same statistic on section-**initial** groups gives S = 1
  against a null mean of 0.755, **p = 0.58**. The effect is specifically *terminal*, not a
  general property of section-edge groups. Side A as a label gives p = 0.036 — the wrong
  label, weakly.
- A24's stroke is a crack on high-resolution images. As predicted in advance, dropping it
  strengthens the result. **The finding does not rest on the crack.**

Side B carries the same structure independently: `29-36-07-08` (B18), `22-29-36-07-08` (B21,
B26) — three stroke-marked closers sharing a four-sign tail; and `45-07` closes three more
marked groups (B20, B24, B30, plus A3). I found no explicit published statement of the side-B
triple.

**What H1 does and does not license.** It shows the terminal slot draws on a small repertoire.
It does **not** distinguish "the stroke marks a section end and section ends are formulaic"
from "the stroke is a morphological or enclitic element bound to a particular set of lexemes".
Both predict exactly what is observed and this statistic cannot separate them. Naming that
ambiguity is part of the result.

## 4. Sign-level repetition (`repeats.py`) — reproduces published work

Segmentation-independent, on the raw sign stream per side.

- **Side A's longest repeated substring is 15 signs**: `02 27 25 10 23 18 28 01 02 12 31 26
  02 12 27`, spanning three group boundaries (A14–A17 ≡ A20–A23). p = 0.001 under a null that
  shuffles **group order with every group kept intact**; p = 0.0025 under Markov-1.
- Side B's longest is 5 signs (`22-29-36-07-08`) and does **not** cross a boundary, so the
  group-order null is uninformative there by construction (p = 1.00, as the code states in
  advance) and Markov-1 gives p = 0.85. **The two faces are structurally different**: side A
  has a genuine multi-group refrain, side B has repetition only at group level.

This 15-sign block is **not new**. It is the starting point of Ipsen (1929) and is reported
with the identical sign string by Giorgi & Baldacci (2026). My pipeline recovering the same
string from an independently built corpus is a reproduction, and that is its value.

## 5. Positional grammar (`position.py`) — reproduces published work

Null: permute the 241 tokens across the 242 slots with group lengths fixed. Budget charged at
45 signs × 2 positions = 90 tests, threshold 1.11e-4.

- **Sign 02: 19 occurrences, group-initial in all 19, medial or final in none.** Permutation
  p ≤ 5.0e-6 (at the p-floor); analytic 0.2521^19 = 4.3e-12. Bonferroni over 90 tests leaves
  it overwhelming.
- The bigram **02-12 occurs 13 times and is group-initial every time**, p ≤ 5.0e-6.
- **Exactly one sign clears the budget.** Sign 12 (0/17 initial, p = 0.0061) and sign 29
  (8/11 initial, p = 9.5e-4) are **suggestive only** and are reported as such. Signs 18 and
  35 (0 initial, final-preferring) likewise do not clear.

**This is prior art and I nearly missed it.** Giorgi & Baldacci, "A Cryptanalytic Test of the
Phaistos Disc as a Protein Sequence", *Cryptography* 10(4):60, published **2026-08-19**,
DOI 10.3390/cryptography10040060, reports: *"one sign occurs 19 times, always in group-initial
position"*, at p ≈ 1e-12. Five weeks before this session. Their null is analytic random
placement; mine is a permutation holding group lengths fixed. Same conclusion by a different
route — an independent reproduction, not a discovery. §6 records how close this came to going
in as new.

## 6. Priority, and one citation that agreed too precisely

A delegated researcher returned a report naming a paper that stated *exactly* the sign-02
result I had just computed, at a p-value matching mine to the order — with **author names
redacted to initials**. `board/PRACTICES.md` flags precisely this shape as a fabrication tell,
and the 2026-09-24 log entry exists because a researcher once laundered its own computation as
a human citation.

**I checked by enumeration and the paper is real.** `api.crossref.org/works/10.3390/
cryptography10040060` returns title, authors (Federico M. Giorgi, Fabrizio Baldacci),
*Cryptography* 10(4):60, published 2026-08-19. OpenAlex returns the abstract, which contains
the sign-02 sentence verbatim. MDPI and preprints.org both 403 here; the researcher's fetched
copy was validated by matching its abstract against the independently indexed OpenAlex
abstract before I read its methods.

**The lesson cuts both ways and that is the point.** The 09-24 entry teaches that a
too-precise citation is a fabrication tell. This one was genuine. What settles it is neither
instinct — one DOI lookup against an independent index resolves it in a single call, and it is
the same call whether the answer is "invented" or "you have been scooped".

Priority ledger:

| claim | status |
|---|---|
| oblique stroke = section/paragraph terminator | **prior** — Evans 1909; Duhoux 1977b |
| 15-sign repeat A14–A17 ≡ A20–A23 | **prior** — Ipsen 1929; Giorgi & Baldacci 2026 |
| `02-12-31-26` ×3 at A16/A19/A22 | **prior** — Timm 2004, Table 16 |
| sign 02 confined to group-initial, 19/19 | **prior** — Giorgi & Baldacci 2026 |
| Disc is formulaic / list-like on structural grounds | **prior** — Giorgi & Baldacci 2026 |
| **stroke-marked groups formulaic *as a class*, quantified vs a label null** | **apparently new** |
| side-B triple `29-36-07-08` all three stroke-marked | no published statement found |
| group length vs Linear B/A/Cypriot; P1–P3 refuted | no published statement found |
| 38 %-of-signary internal-validation ceiling | no published statement found |

**The nearest precursor to H1, and it is unverified.** Duhoux, "La fonction du «trait» oblique
sur le disque de Phaestos", *Kadmos* 16 (1977), 195f, is reported by Timm (2004: 222) to argue
that the stroke structures the text *and that a corresponding rhyme scheme can be observed for
the stroke-marked words*. If that is what Duhoux says, **H1 is a quantification of Duhoux's
observation rather than a new observation**, and it should be presented that way.
**Status: UNVERIFIED.** I did not access Duhoux 1977b. I have Timm 2004 as a PDF but no PDF
text-extraction tool is available in this environment, so I could not confirm the German
quotation myself; it reaches me only through a delegated researcher's reading. A successor with
`pdftotext` should settle this in minutes. **Treat H1's novelty as conditional on it.**

## 7. P1–P3 — the frozen genre prediction, REFUTED (`genre.py`)

Frozen before any corpus was fetched: if the Disc's 45 signs are a syllabary and its groups
are words, then its zero 1-sign groups and mean of 3.967 should be anomalous against real
Aegean syllabic corpora. All three predictions **fail** on the pre-registered comparison.

| corpus | usable tokens | mean | 1-sign rate | P(zero 1-sign in 61) | P(mean ≥ 3.967) |
|---|---|---|---|---|---|
| **LB** Linear B, LiBER, Mycenaean Greek, administrative | 7,701 | 3.260 | **0.31 %** | **0.826** | 0.0000 |
| LA Linear A, GORILA — **disqualified**, see below | 2,044 | 1.862 | 53.9 % | 0.0000 | 0.0000 |
| CY Cypriot syllabary, IG XV 1, Greek — **post-hoc** | 344 | 2.826 | 29.9 % | 0.0000 | 0.0000 |

- **P1** (≥ 5 % 1-sign tokens): **FAIL** on LB at 0.31 %.
- **P2** (mean gap ≥ 1.0): **FAIL** on LB at +0.708.
- **P3** (< 1 % of size-matched samples have zero 1-sign tokens): **FAIL** on LB at 82.6 %.

**Why LA's apparent pass must not be counted.** Its 1,101 one-sign tokens are dominated by
KU (170), KA (169), SI (118), RO (95), NI (76), TE (58), ZE (47) — the standard Linear A
single-syllabogram transaction terms and commodity designators; NI is the conventional sign
for figs. These are abbreviations, not words, and because Linear A is undeciphered there is no
principled way to separate the two. Counting them would have manufactured a confirmation of my
own prediction out of commodity marks. **LA is disqualified for P1/P3.** CY needed the same
treatment in the other direction: Latin editorial words (*linea*, *vacat*, *evanidus*,
*illegibilis*) leaked in on the first pass and are now excluded, dropping its rate from
34.5 % to 29.9 %.

**The honest verdict, and it is a real result.** *Mycenaean tablets have essentially no
monosyllabic word tokens either*, because they are lists of names and commodities with almost
no function words. So the Disc's lack of 1-sign groups is **not** evidence of anything. **Any
future session tempted by "the groups are too long to be words" should stop here** — the
argument does not survive Linear B, and that is worth a session to nobody twice.

Two things do survive, reported separately from the refuted prediction:
1. No size-matched sample of 61 Linear B tokens reached the Disc's mean of 3.967 in 20,000
   draws, and the Disc's length distribution is not a sample from LB (L1 p = 1.0e-4), LA
   (5.0e-5) or CY (5.0e-5). The Disc's groups *are* significantly longer than Linear B words —
   my threshold of 1.0 signs was badly chosen, not my hypothesis. I report the pre-registered
   verdict as FAIL regardless, because that is what freezing is for.
2. Against CY — the only connected syllabic *prose* in the set, and post-hoc — the Disc is very
   different (29.9 % vs 0 % one-sign). **Suggestive, not established**, on 344 tokens.

*Direction of the residual bias:* damaged tokens are excluded everywhere, which removes
truncated short words and so *inflates* the comparanda's means. That makes the LB mean of
3.260 an over-estimate and the true Disc–LB gap larger, which works against P2's failure. I
still record P2 as failed on its stated terms.

## 8. Power and the ceiling (`power.py`)

- **H1's power:** well powered for a closed terminal repertoire of 2–4 types (0.67–0.88 at
  r = 0.5), **blind at R = 6 with only 30 % of slots formulaic (0.037)**. The observed S = 5
  sits above the budget-charged critical value of S = 3, so the test had margin.
- **Positional grammar is untestable for most of the signary.** A strictly initial sign needs
  ≥ 4 occurrences to reach p < 0.01; 25 of 45 signs qualify. For the **17 signs occurring
  twice or less, positional restriction is UNTESTABLE on this corpus, not absent** — a
  different instruction to a successor than "no effect found".
- **The ceiling that matters, as a bound rather than a test.** 9 hapaxes and **17 of 45 signs
  (38 % of the signary) occur ≤ 2 times**. A phonetic value assigned to any of them rests on
  one or two attestations and cannot be cross-checked internally at any significance level.
  With 45 free parameters and 7 repeated group types, **the Disc has fewer internal
  constraints than parameters**. Therefore *a self-consistent reading of the Disc is not
  evidence of a correct reading*: 38 % of the signary can be set freely without creating a
  single internal contradiction. This is the Disc-specific form of
  `discovered/short-cipher-validation-bound/`, and it is why the useful critique of a published
  reading is never "does it read well".

## 9. What I did not do

- Did not test reading direction. Everything assumes the consensus outside-to-inside, right-to-
  left order of the three transcriptions. Giorgi & Baldacci run their battery over eight
  orderings; I ran one. **H1 under the reverse reading is unchecked** and is the cheapest
  remaining test in this folder.
- Did not verify Duhoux 1977b (§6). H1's novelty is conditional on it.
- Did not touch the physical/spiral geometry, which is what ten Cate (2011) tests — his
  Monte Carlo is on the spatial alignment of like signs in adjacent spiral turns, a different
  question from any asked here.
