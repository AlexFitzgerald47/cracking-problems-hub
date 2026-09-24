# The Chinese gold bar cryptograms are not ciphertext

**Session 2026-09-24. Cracker, starting mode — the problem had never been worked.**

Reproduce with `python3 src/make_english_ref.py && python3 src/stats.py &&
python3 src/confirm.py && python3 src/adjudicate.py`. Predictions were
registered in `FREEZE.md`, committed (7539d24) before `confirm.py` ran.

---

## The result in one paragraph

Across the complete inventory of 16 distinct cryptograms (263 letters),
**21 of the 26 letters of the alphabet occur exactly ten times**; the other
five are E=11, I=13, O=9, S=11, T=9. The chi-square against a uniform
distribution is **1.251 on 25 degrees of freedom, where a genuinely random
process is expected to yield 25**. Analytically, P(chi2_25 <= 1.251) =
**9.3e-13**. The corpus is not merely "flat", as the cipher-community
literature has said since 2015 — it is *flatter than chance*, and that is a
different and much more informative fact. Every cipher samples letters, and
sampling produces multinomial noise. A one-time pad, the flattest possible
encryption, still gives chi2 ~= 25 +/- 7. **No encryption process of any kind
produces a letter distribution this even.** The strings were composed under a
letter-balance constraint, by someone counting letters as they wrote.

## What is excluded, and by what

| Cipher class | Excluded by | Statistic |
|---|---|---|
| Monoalphabetic substitution (any language) | index of coincidence, which is *invariant* under such substitution | obs 0.0397 vs 0.0606 English MASC (p = 0.0001), 0.0739 romanized-Chinese MASC (p = 0.0001); flat = 0.038 |
| Transposition (any language) | same — transposition preserves letter frequencies exactly | as above, plus zero repeated trigrams where English predicts ~29 (p = 0.0001) |
| Polyalphabetic / Vigenere family | the chi-square is *too low*, and no periodic structure at any period 2-8 | see power caveat below |
| One-time pad / any flat-output cipher | chi2 = 1.251 against an expectation of 25; P = 9.3e-13 | P-E: unreachable at any transcription-error rate |
| Physical tooling artefact (punch set, type case) | the balance holds on the **deduplicated inventory**, which is not a physical object | P-B |

The IC test is the load-bearing one for the first two rows because it does not
require guessing the plaintext language: monoalphabetic substitution and
transposition both leave IC unchanged, so an IC of 0.0397 rejects *any*
natural-language plaintext under them, Chinese romanization included.

## The five registered predictions

**P-A — FAILED.** I predicted the *instance* corpus (all 44 stamped lines
across the four documented bar faces, repeats counted, 771 letters) would be
significantly non-uniform, on the reasoning that a physical punch-set
explanation would constrain physical text rather than the inventory. It is
not: chi2 = 13.8, which is itself mildly flat. **The prediction was badly
designed and the fault is mine** — the instance corpus is a multiset drawn
from the inventory, so it inherits the inventory's balance and is not
independent evidence. It cannot discriminate and should not be quoted as if
it did. What survives is the *comparison*: near-exact balance at 263 letters
(chi2 1.251) against only mild flatness at 771 (chi2 13.8). The sharp
constraint lives at the inventory level.

**P-B — CONFIRMED, and it carries the argument P-A was meant to carry.**
The balance appears **only** when all 16 strings are taken together:

| subset | distinct strings | letters | chi2 | P(chi2_25 <= obs) |
|---|---|---|---|---|
| bar 10.2a | 8 | 103 | 20.94 | 0.304 |
| bar 10.2b | 5 | 110 | 20.00 | 0.253 |
| bar 9.1 | 9 | 152 | 10.16 | 0.0038 |
| bar 5.1 | 13 | 215 | 9.33 | 0.0019 |
| **whole inventory** | **16** | **263** | **1.25** | **9.3e-13** |

No bar is remotely as balanced as the complete set. This kills the tooling
hypothesis on a structural rather than statistical ground: **a deduplicated
inventory of 16 distinct strings is not a physical object.** No punch set, no
type case, no casting process operates on "the set of distinct strings, each
counted once". Only a person composing the text does. (Punches are in any case
reusable, so they were never consumable in the way the hypothesis needed.)

**P-C — CONFIRMED.** Against a null that deals the *exact* observed letter
multiset into the *exact* observed length structure, every order-sensitive
statistic is unremarkable (20,000 replicates):

| statistic | observed | null mean | p |
|---|---|---|---|
| max letter multiplicity in a string | 5 | 3.86 | 0.225 |
| adjacent doubles | 7 | 8.68 | 0.721 |
| max single-string IC | 0.0711 | 0.0679 | 0.703 |
| pooled IC | 0.0397 | 0.0350 | 0.238 |
| periodic IC, periods 2-8 | 0.035-0.059 | 0.035 | 0.132-1.000 |

The strings behave exactly like a random deal from a balanced pool. The
`FEWGDRHDDEEUMFFTEEMJXZR` line, which looks strikingly clumpy (E five times in
23 letters), is inside the null at p = 0.225.

**Power caveat, stated because it bounds the claim.** The periodic tests are
not strong. Pooled coset pairs give an IC standard error of 0.0083 at period 2,
rising to 0.0145 at period 5, so English-strength periodicity sits 3.4 s.e.
away at period 2 but only 1.9 s.e. at period 5. **A weak polyalphabetic
structure at period >= 4 would not be detected by this corpus**, and no
experiment on 263 letters can fix that. The polyalphabetic exclusion rests
primarily on the chi-square being too low, not on the periodic tests.

**P-D — CONFIRMED.** `YQHUDTABGALLOWLS` is the one string that looks like it
leaks plaintext. It does not: the substring is `GALLOWLS`, not GALLOWS, and
the corpus contains **zero** English words of length >= 6 anywhere. A random
deal from the balanced pool produces them at a rate of 0.0005 per corpus, so
zero is exactly what is expected either way. This is a null result on a
seductive pattern, not evidence of anything.

**P-E — CONFIRMED, and it is the decisive robustness check.** The IACR page
warns that "some of the letters are hard to read so there may be
inaccuracies". Simulating that directly:

- From an **exactly balanced** 263-letter original, corrupting ~6 letters
  reproduces the observed value precisely (median chi2 = 1.25 at k = 6).
  The five observed deviations are what a handful of misreadings looks like.
- From a **genuine flat-output cipher** (uniform random 263 letters),
  P(chi2 <= 1.251) = **0.0000** at k = 0, 10 and 30 misreadings alike.

Transcription noise degrades balance; it cannot manufacture it. So the true
inscription is *at least* as balanced as the transcription shows, and the
finding is robust in the only direction that matters.

## Robustness to the transcription dispute

Pelling / Cipher Foundation transcribe bar 5.1 differently from IACR on two
strings (`UGMNCBXCFLDBEY` vs `UGMNCBXCKDBEY`; `KOWVRSRKWTMLDH` vs
`KOWVRSRWTMLDH`). **The result does not depend on which is right**: IACR gives
chi2 = 1.251 (21/26 letters at exactly ten), Pelling gives chi2 = 1.490
(19/26), P = 9.3e-13 and 7.4e-12 respectively. The balance statistic *weakly*
prefers the IACR reading, which is a checkable prediction about two characters
on bar 5.1 — but the preference is modest and should not be oversold.

## What this means for the problem's success criteria

- **Criterion 2 (a rigorous negative) — MET, with margin.** The criterion
  asked for a demonstration that the strings are "statistically
  indistinguishable from a null model" under simple schemes. The evidence is
  stronger than that: they are *distinguishable from every cipher null*, in
  the direction that excludes encipherment rather than merely failing to
  establish it.
- **Criterion 1 (a checkable plaintext) — not met, and argued to be
  unreachable.** If the strings were not produced by encoding anything, there
  is no plaintext to recover. The named cribs (Wang Jialie, National City
  Bank, 1933) are not the obstacle; the absence of an encoding is.
- **Criterion 3 (authenticity) — materially advanced, not settled.** The
  authenticity case in the literature rests on iconography and dating
  (aircraft type, Wang Jialie's rank, simplified characters) argued by
  bloggers and commenters, with no forensic examination anywhere. This adds an
  **independent, quantitative, reproducible line** that needs none of that:
  whoever made these objects wrote balanced gibberish and presented it as
  enciphered financial text. That is an act of fabrication, and it is
  measurable from the transcription alone.

## The steelman I cannot exclude

A **deliberately flat homophonic cipher** — a system whose designer equalised
its 26 output letters on purpose — is not excluded by the balance statistic,
because equalisation is its design goal. I record it as live. But it requires
the encipherer to have balanced letter counts across exactly the *deduplicated
set of 16 strings*, which is a composition-level act indistinguishable from
the fabrication hypothesis, and it leaves no order structure to find (P-C). It
is unfalsifiable as stated rather than supported, and nothing in the evidence
recommends it over the simpler reading.

## The one public solution claim

Milton Kim (Cipher Mysteries, 26 Oct 2024, comment verified present) claims
`FEWGDRHDDEEUMFFTEEMJXZR` -> `OUSTGOVPBANKCTGOLEESVOG`, method unpublished.
The implied mapping is **not a function**: D -> {B,G,P}, E -> {A,E,L,N,U},
F -> {G,O,T}, M -> {C,E}, R -> {G,O} — at least 10 free choices beyond a
substitution alphabet, plus an ad-hoc "last 9 letters read backward" rule. An
unpublished position-dependent rule with that many degrees of freedom can
produce any 23-letter target, so the claim carries no evidential weight **as
stated**. This is not a refutation of his method, which nobody has seen. His
repository (`github.com/milton6310/cgbCiphers`) could not be fetched from this
session — the environment is scoped to this repository — so it remains
**unchecked, not absent**.

## Prior art, checked directly

Nick Pelling (Cipher Mysteries, 15 Mar 2015) observed that "the letter
instance statistics for the above are very flat" and published a frequency
table — **for one bar only**, and without a null model or a significance
test. That is the genuine prior art and it is correctly cited in `PROBLEM.md`
as the (previously unverified) "very flat" claim. It is now verified, and
extended: flatness is not the finding, *excess* flatness is.

I read the complete comment threads of both Cipher Mysteries posts (59 + 16 =
75 comments), Klaus Schmeh's Cipherbrain entry, and both Cipher Foundation
pages. No source states the exactly-ten-per-letter structure and none
quantifies the flatness. **A delegated researcher in this session reported a
"Bret Bowen, September 10, 2020" comment stating exactly that finding. No such
comment exists** — see `PROGRESS.md` and the board log entry.
