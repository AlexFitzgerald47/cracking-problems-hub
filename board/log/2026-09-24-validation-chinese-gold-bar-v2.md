# Validation — Chinese gold bar cryptograms (VALIDATOR 2)

**claim:** The 16 IACR gold-bar cryptograms are not ciphertext. They were not produced
by enciphering, encoding or transposing any message; they were composed under a
deliberate letter-balance constraint (~10 occurrences per letter across the
deduplicated 263-letter inventory), by someone counting letters as they wrote.

**problem:** `chinese-gold-bar-cipher`

**criteria applied:** `PROBLEM.md`, success criterion 2, verbatim —

> **A rigorous negative** — a demonstration, with the recomputed letter-frequency and
> repeated-substring statistics actually shown, that the string set is statistically
> indistinguishable from a null model under any simple monoalphabetic/polyalphabetic/
> transposition scheme, which would close off a large branch of speculative attack
> rather than leaving it open by default.

Criteria 1 (a checkable plaintext) and 3 (a sourced, dated authenticity argument) are
quoted in full in `PROBLEM.md` and are not claimed by the claimant.

**validator role:** 2 — assigned the **null models and the reference corpora**

---

**reproduced: yes — bit-identical.**

I copied the attempt to my own scratch directory (mirroring the repo depth so the
relative source paths resolve) and ran, unmodified:

```
python3 src/make_english_ref.py && python3 src/stats.py && python3 src/confirm.py && python3 src/adjudicate.py
```

Every headline number reproduced. `out/stats.json`, `out/confirm.json` and
`data/english_reference.txt` are **byte-identical** (`diff`/`cmp` clean) to the
committed artifacts — the scripts are fully seeded (`random.seed(20260924)`), so
reproduction is deterministic rather than merely statistical. Runtime 1m28s.

Reproduced headline values: 263 letters over 16 strings, lengths
`[25,24,24,23,20,19,16,14,14,14,14,13,12,12,11,8]`; 21/26 letters at exactly 10
(E=11, I=13, O=9, S=11, T=9); chi2 vs uniform = **1.25095** on 25 df; pooled
within-string IC = **0.03968**; repeated trigrams = **0**; repeated 4-grams = **0**;
MASC-English null IC 0.0606 / rep3 28.77 / chi2 219.2; MASC-romanized-Chinese null
IC 0.0739 / rep3 53.38; P-A **FAILED** as disclosed (instance chi2 = 13.822);
P-B/P-C/P-D/P-E confirmed as reported; IACR chi2 1.251 vs Pelling 1.490.

**verdict: PARTIAL**

Criterion 2 is **met, and exceeded** as written. The claim's further inferential step —
*who or what* imposed the balance — is **not established** at the strength stated, and
two headline numbers need correcting. Criteria 1 and 3 are unmet (acknowledged by the
claimant). This is a real and unusually well-executed negative result, not a solve of
the problem's named unknown.

---

## reasoning

### 1. Independent re-derivation from the primary source (not the claimant's files)

I fetched `https://www.iacr.org/misc/china/cryptograms.html` directly (HTTP 200, 5123
bytes) and parsed all five `<pre>` blocks with my own regex, then computed every
statistic with my own script, importing nothing from `src/`.

- The final `<pre>` block is the page's authoritative "list of all of the known
  cryptograms": 16 strings. `data/cryptograms.txt` is **identical to it, string for
  string and in the same order**. Every string's actual length equals the length the
  page itself states beside it (25, 24, 24, 23, 20, 19, 16, 14×4, 13, 12, 12, 11, 8).
  Total 263 letters. The 8-char `ZUQUPNZN` and 25-char `SKCDKJCDJCYQSZKTZJPXPWIRN`
  named in `PROBLEM.md` are both present.
- `data/instances.tsv` (44 stamped lines over bars 10.2a, 10.2b, 9.1, 5.1) matches my
  parse of the four per-bar blocks **exactly as a multiset, and per bar**. The only
  difference is the order of two adjacent lines on bar 5.1 (`GKJFHYXODIE` /
  `SKCDKJCDJCYQSZKTZJPXPWIRN`), which the page lays out in two visual columns. No
  statistic anywhere uses instance line order, so this is immaterial.
- My own counts: A10 B10 C10 D10 **E11** F10 G10 H10 **I13** J10 K10 L10 M10 N10 **O9**
  P10 Q10 R10 **S11** **T9** U10 V10 W10 X10 Y10 Z10. chi2 = **1.25095**.
- My own pooled IC = **0.03968** (178 coincidences / 4486 within-string pairs;
  flat = 0.03846).
- My own n-gram counts over the 16 distinct strings: **231 trigrams, 0 repeated;
  215 4-grams, 0 repeated**; bigrams 247 total, 30 distinct repeated, excess 35
  (most repeated: YQ, WI, UP, IY, AB at 3 each). The zero-repeated-trigram claim is
  correct and I confirm it by hand.

**The corpus, the lengths and all four observed statistics are independently
confirmed.** Nothing here rests on the claimant's transcription or code.

### 2. Is the English reference corpus legitimate, or does it bake in the answer?

**It is legitimate, and I verified its provenance.** `src/make_english_ref.py` reads
`historical-controversies/junius-letters-authorship/attempts/2026-09-17-genre-matched-openset/data/raw/gutenberg_2173.txt`
— Project Gutenberg #2173, Edmund Burke, *Thoughts on the Present Discontents, and
Speeches*, already in the repository from an unrelated earlier attempt. I read the file:
it is genuine 18th-century English prose, 297 KB. The script upper-cases it, strips
everything outside A–Z, and slices letters 20000–170000 (150,000 letters) to skip front
matter. It is **not** a frequency table, not synthesised, and not derived in any way from
the gold-bar corpus. There is no path by which it can bake in the answer.

The real weakness is different and smaller: **it is one 18th-century political tract,
and it happens to be the most favourable of the three English corpora I tested.** I
re-ran the identical MASC null (same lengths, same estimator, my own code) against two
corpora the claimant never touched, which I fetched myself:

| English source | null IC (mean, 95%) | null rep3 (mean, 95%) | null chi2 | reps with rep3 = 0 | reps with IC <= 0.0397 |
|---|---|---|---|---|---|
| Burke pg2173 (claimant's) | 0.0606 [0.0504, 0.0722] | 28.66 [17, 42] | 219.2 | 0 / 8000 | 0 / 8000 |
| Austen pg1342 (mine) | 0.0581 [0.0481, 0.0691] | 25.25 [15, 38] | 202.2 | 0 / 8000 | 0 / 8000 |
| Doyle pg1661 (mine) | 0.0592 [0.0490, 0.0704] | 25.75 [15, 38] | 205.1 | 0 / 8000 | 0 / 8000 |

So the quoted "0.0606" and "~29" are both the **high end** of the plausible range:
independent English gives IC ≈ 0.058–0.059 and rep3 ≈ 25–26. The headline trigram
expectation is inflated by roughly 12% by the choice of Burke. **This does not touch the
conclusion** — 0 of 24,000 replicates across three corpora ever produced zero repeated
trigrams, and the 2.5th percentile of rep3 is 15 under the *least* repetitive corpus.
But "~29" should be quoted as "~25–29 depending on the English source", and the
claim should not lean on a single 1770 tract.

### 3. Is the substituted-English null matched to the observed length structure?

**Yes, exactly, and I verified it in code.** `null_masc()` (stats.py:86-99) iterates
`for L in LENGTHS`, draws an independent contiguous window of exactly that length from
the 150k-letter source, and applies one random letter permutation per replicate. `LENGTHS`
is derived from the observed corpus at stats.py:25. So the null is 16 strings at
8/11/12/12/13/14/14/14/14/16/19/20/23/24/24/25 = 263 letters, identical to the
observation, and `ngram_repeats` is evaluated over the same 231 trigram positions as the
observation. The trigram-repeat expectation is **not** inflated by a length mismatch.

Two design details I checked and endorse: the permutation is irrelevant to IC and to
n-gram *repeat counts* (both are invariant under relabelling), so the MASC step is
cosmetic — correctly so, since the point is that IC is invariant under monoalphabetic
substitution. And `ngram_repeats` is deliberately computed over the **deduplicated** 16
strings, so the whole-string repetition on the bars cannot manufacture repeats. Had it
been run over the 44 stamped instances, the trigram excess would be **452** (I computed
this) — an artefact of stamping, and the claimant was right to exclude it.

### 4. Is the Wade-Giles / romanized-Chinese reference a real corpus?

**No. It is a synthetic generator, and `src/stats.py` says so explicitly** in the
docstring of `synth_romanized_chinese` (lines 107-118): *"NOT a real corpus -- a
generative stand-in"*. It concatenates a uniformly-random draw from a hand-written list
of 28 Wade-Giles initials and 36 finals. There is no Chinese text anywhere in this
attempt. The reported **0.0739** and **~53** are therefore properties of a model the
claimant wrote, not measurements of romanized Chinese, and `RESULTS.md`'s comparison
table labels the row "romanized-Chinese MASC" without carrying that caveat across from
the code — a reader of the writeup alone would take 0.0739 for a measurement. That
should be fixed in the writeup.

Two mitigations, both of which I tested rather than assumed:

- **The approximation errs in the claim's favour.** Real syllable use is highly uneven;
  the generator samples syllables uniformly, which flattens it. Re-running the same
  generator with Zipf-weighted syllables gives **IC 0.1084** and **rep3 61.2**, versus
  0.0739 and 53.6 uniform. A more realistic romanized-Chinese model sits *further* from
  the observation, not nearer. The synthetic null is conservative.
- **The language-independence claim does not need it.** IC is invariant under
  monoalphabetic substitution and transposition, so the right question is: *how flat
  would a plaintext language have to be for the observed IC to be unremarkable?* I
  measured that directly, simulating at the observed length structure from letter
  distributions interpolated between English and uniform:

| language monogram IC | null pooled IC (mean) | 2.5th pctl | P(null IC <= 0.0397) |
|---|---|---|---|
| 0.0650 (English) | 0.0649 | 0.0531 | 0.0000 |
| 0.0554 | 0.0553 | 0.0450 | 0.0013 |
| 0.0515 | 0.0514 | 0.0415 | 0.0132 |
| 0.0480 | 0.0481 | 0.0388 | 0.0457 |
| 0.0451 | 0.0452 | 0.0366 | 0.1308 |

So the IC test excludes, at p < 0.05, **any plaintext language whose monogram IC
exceeds about 0.048** — which is every natural language and every romanization of one
(the flattest commonly cited, transliterated Russian, is ≈0.053; Chinese romanizations
are far higher because of the small syllable inventory). That is the number the
language-independence claim should rest on, and it is corpus-free. Stated honestly, the
bound is not infinite: a hypothetical plaintext with IC ≈ 0.045 would *not* be excluded
by IC alone. That is the correct scope of "no guess about the plaintext language is
required".

### 5. Are the reported p-values 0.0001 and 0.0003 resolution floors?

**Yes — 0.0001 is a floor. I confirmed this arithmetically and by recount.**
`pval_two_sided` (stats.py:136-139) returns `2*min((ge+1)/(n+1), (le+1)/(n+1))` with
`REPS = 20000`, so the smallest attainable value is `2/20001 = 9.9995e-05`, printed as
`0.0001`. Recovering the replicate counts from `out/stats.json`:

| null | statistic | reported p | replicates at or beyond the observation |
|---|---|---|---|
| uniform_random | chi2 | 0.0001 | **0** of 20000 |
| masc_english | IC | 0.0001 | **0** of 20000 |
| masc_english | rep3 | 0.0001 | **0** of 20000 |
| masc_english | chi2 | 0.0001 | **0** of 20000 |
| masc_english | rep4 | 0.0113 | 112 of 20000 |
| masc_romanized_zh | IC | 0.0001 | **0** of 20000 |
| masc_romanized_zh | rep3 | 0.0001 | **0** of 20000 |
| masc_romanized_zh | rep4 | 0.0003 | **2** of 20000 |
| masc_romanized_zh | chi2 | 0.0001 | **0** of 20000 |

Every "p = 0.0001" in the claim means *zero of 20,000 replicates were as extreme* —
a resolution limit, correctly read as **p < 1e-4**, not as a measured 1-in-10,000.
The single "0.0003" is a genuine measured value (exactly 2 replicates), also
resolution-limited. **The claim and `RESULTS.md` should write these as `p < 1e-4
(0/20000)`.**

A related mislabel: the claim states "romanized Chinese ~53 (p = 0.0003)" for repeated
*trigrams*. The run shows the romanized-Chinese **trigram** p is 0.0001 (0/20000); the
0.0003 belongs to the **4-gram** statistic. Harmless, but wrong as printed.

One degenerate p-value worth noting: `corpus_shuffle` reports chi2 p = 1.0000 because
shuffling preserves the letter multiset, so chi2 is constant across replicates. That is
correct behaviour, not a bug, but it is a p-value with no content.

### 6. The exact probability is 1.83× larger than the headline 9.3e-13

This is the one substantive numerical correction. `P(chi2_25 <= 1.251) = 9.3e-13` is the
**asymptotic** chi-square CDF, and the asymptotic approximation is known to be poor in
the extreme lower tail with expected cell counts of only 263/26 = 10.1. Here the exact
multinomial probability is computable in closed form. Writing `c_i = 10 + d_i`:

`sum c_i^2 = 2660 + sum d_i^2`, and `chi2 = (sum c_i^2 - N^2/26)/e`, so with the observed
`sum c_i^2 = 2673` the event `{chi2 <= 1.25095}` is exactly `{sum d_i = 3, sum d_i^2 <= 13}`.
I enumerated that event exactly (dynamic program over the 26 cells, `Fraction`
arithmetic, multiplied by `263!/26^263`):

- **Exact P(chi2 <= 1.25095 | uniform random 263 letters) = 1.7021e-12**
- Asymptotic chi2_25 CDF at 1.25095 = 9.2979e-13 (I reimplemented the incomplete gamma
  independently and reproduce the claimant's 9.3e-13 exactly)
- **exact / asymptotic = 1.831**

The cumulative breakdown: `sum d^2 <= 3` → 2.7e-19, `<= 7` → 1.2e-15, `<= 11` → 2.4e-13,
`<= 13` → 1.70e-12. The observed corpus sits at exactly the boundary, `sum d^2 = 13`.
Also confirmed: the **minimum attainable** chi2 at N = 263 is 0.2624 (23 letters at 10,
3 at 11), matching `confirm.py`'s k = 0 row — the observation is remarkably close to the
floor.

**Direction of the error: the claim is 1.8× too strong.** `9.3e-13` should be `1.7e-12`
in `RESULTS.md`, `FREEZE.md`, the claim, and `adjudicate.py`'s output. This changes
nothing qualitatively — 1.7e-12 is still overwhelming, and the same correction applies
to the Pelling variant — but a headline probability quoted to two significant figures
should be the exact one when the exact one is this easy to get.

### 7. Order-structure statistics the claimant did not report

Against the same exact-multiset deal null (10,000 replicates, my own implementation):

| statistic | observed | null mean | 95% | p (two-sided) |
|---|---|---|---|---|
| bigram excess | 35 | 34.27 | [25, 44] | 0.9445 |
| distinct bigrams repeated | 30 | 31.53 | [23, 40] | 0.8151 |
| trigram excess | 0 | 1.13 | [0, 4] | 0.6677 |
| reversed-bigram matches | 79 | 83.92 | [65, 103] | 0.6519 |
| **max distinct letters in a string** | **15** | **17.89** | **[16, 20]** | **0.0100** |

Four of five confirm pillar 4. The fifth does not: the most letter-diverse string
(`SKCDKJCDJCYQSZKTZJPXPWIRN`, 15 distinct letters in 25) is **less** diverse than a
random deal predicts, at p = 0.010. Two of the claimant's own statistics lean the same
way — max letter multiplicity in a string (obs 5 vs null 3.86, p = 0.225) and pooled IC
(obs 0.0397 vs null 0.0350, p = 0.238). Three statistics agreeing in one direction is
worth recording: **letters repeat within strings slightly more than a pure random deal
from the balanced pool allows.** With ~16 order statistics now tested, one at p = 0.01
is about what chance gives (Bonferroni ≈ 0.16), so this is a hint, not a finding — but
"the strings behave exactly like a random deal" and "no order structure of any kind"
overstate it. "No order structure that survives correction for multiplicity" is right.

### 8. P-B: the per-bar CDFs are the wrong comparison, but the conclusion survives

Pillar 3 rests on the per-bar distinct-subset CDFs (0.304, 0.253, 0.0038, 0.0019 against
the whole set's 9.3e-13). Those are computed against a **uniform** null, which is not the
right question: any large subset of a balanced whole is *automatically* flat-ish, so bar
5.1 (13 of the 16 strings, 215 of the 263 letters — 82% of the inventory) would look flat
whatever produced the balance. This looked to me like the claim's weakest link, so I built
the conditional null the argument actually needs: **random k-of-16 subsets of the same
inventory**, 20,000 draws each.

| bar | distinct strings | letters | chi2 | uniform-null CDF (claimant) | random k-of-16 subsets: mean chi2 | P(subset chi2 <= obs) |
|---|---|---|---|---|---|---|
| 10.2a | 8 | 103 | 20.94 | 0.3041 | 14.31 | 0.9410 |
| 10.2b | 5 | 110 | 20.00 | 0.2532 | 19.10 | 0.5868 |
| 9.1 | 9 | 152 | 10.16 | 0.0038 | 12.65 | 0.2610 |
| **5.1** | **13** | **215** | **9.33** | **0.0019** | **6.17** | **0.9267** |

The result is the opposite of a problem: **no bar is flatter than a random subset of the
same size, and the two largest bars are markedly less flat** (5.1 at P = 0.93, 10.2a at
P = 0.94). Bar 5.1's apparent flatness is entirely explained by its being 82% of a
balanced inventory. Under the correct comparison, the localisation argument is
**stronger** than the claim states: the balance is a property of the complete 16-string
set and of nothing smaller. `RESULTS.md` should replace the uniform-null CDFs with this
conditional test, which is the one that actually discriminates.

### 9. The steelman is NOT unfalsifiable as stated

The claimant flags a deliberately flat **homophonic** cipher as live and unfalsifiable,
and invites the refuter to start there. It has a testable consequence they missed: a
**capacity bound**.

A homophonic substitution must assign each plaintext letter *i* a set `S_i` of ciphertext
letters, and the sets must be **disjoint** or the message is not uniquely decipherable.
If plaintext letter *i* occurs `n_i` times and no output letter may exceed `m`
occurrences, then `|S_i| >= ceil(n_i/m)`, so the scheme exists only if
`sum_i ceil(n_i/m) <= 26`. I evaluated this over 3,000 random 263-letter windows of real
English:

| max output count m | distinct output letters required (mean, range) | feasible in 26 letters? |
|---|---|---|
| 10 | 37.8 [33, 43] | **no** |
| 11 | 35.8 [31, 41] | **no** |
| **13 (the observed maximum, I = 13)** | **32.8 [28, 38]** | **no** |
| 15 | 30.9 [26, 35] | marginal |
| 20 | 26.7 [22, 31] | yes |

**A homophonic letter-for-letter cipher over a 26-letter output alphabet cannot equalise
a 263-letter natural-language plaintext to a maximum of 13 per output letter. It needs
about 33 disjoint output symbols and only 26 exist.** The steelman therefore survives
only by abandoning one of its own premises: either the mapping is non-injective (not
decipherable — not a cipher), or the plaintext is much shorter than the ciphertext
(expansion, i.e. a codebook or polygraphic system whose *designer* still hand-balanced the
output — which is the claimant's own conclusion under another name), or the "plaintext" is
itself already flat (not a natural language). This is a genuine falsification of the
letter-level version of the steelman, and the claimant should take the win: their
"unfalsifiable as stated" is too pessimistic, and the claim is stronger than they argued.

### 10. Judgment against criterion 2, and whether criterion 2 alone is a solve

Criterion 2 asks for four things. On my own reproduction and re-derivation:

1. *Recomputed letter-frequency statistics, actually shown* — **yes**, and I confirm
   them from the primary page: 21/26 at exactly 10, chi2 = 1.25095.
2. *Recomputed repeated-substring statistics, actually shown* — **yes**: 0 repeated
   trigrams, 0 repeated 4-grams, 35 bigram excess, all independently confirmed.
3. *A demonstration against an explicit null model* — **yes**, four nulls, correctly
   matched to the observed length structure, plus the exact analytic calculation.
4. *Closing off monoalphabetic / polyalphabetic / transposition* — **substantially yes.**
   Monoalphabetic and transposition are closed language-independently via IC invariance
   for any plaintext language with monogram IC above ≈0.048 (my measured bound), which
   covers every natural language and romanization. Polyalphabetic is closed by chi2 being
   *too low* rather than by the periodic tests, which the claimant correctly concedes lack
   power at period >= 4 (1.9 s.e. at period 5). I regard the chi2 route as sound: any
   Vigenère-family cipher is still a sampling process and leaves chi2 ≈ 25 ± 7.

The criterion's literal wording — "statistically indistinguishable from a null model" —
is in fact *weaker* than what the attempt delivers, which is distinguishability from
every cipher null in the direction that excludes encipherment. **Criterion 2 is met, and
exceeded.**

Does criterion 2 alone constitute a solve of this problem? **In my judgment, no — it
constitutes full satisfaction of one of three independently-stated deliverables.**
`PROBLEM.md` lists the three as separate numbered items, and criterion 3 opens with
"Separately," so they read as disjunctive contributions rather than a conjunction. But
the problem's **Statement** names the unknown as "what do the Latin-letter cryptograms
actually encode?", and criterion 2 is described in its own text as something that "would
close off a large branch of speculative attack rather than leaving it open by default" —
the language of narrowing the field, not of answering the named unknown. The claim does
answer that question negatively, which is a real and substantive result, and it is the
first quantified null model ever applied to this corpus (Pelling's 2015 "very flat" is
one bar, no null, no test — I confirm that `PROBLEM.md`'s characterisation of the prior
art was accurate and that the flatness claim is now verified and materially extended).
That is worth publishing as a rigorous negative under criterion 2. It is not a
decipherment, the claimant does not pretend it is, and with criteria 1 and 3 unmet the
problem should not be marked solved.

Hence **PARTIAL**, and the claim stands **HELD — awaiting human sign-off**.

### Required corrections before this goes anywhere public

1. `P(chi2_25 <= 1.251) = 9.3e-13` → **exact value 1.7e-12** (asymptotic approximation
   is 1.83× optimistic at these cell counts). Applies in `RESULTS.md`, `FREEZE.md`, the
   claim, and `adjudicate.py`. The Pelling variant's 7.4e-12 needs the same treatment.
2. `p = 0.0001` → **`p < 1e-4 (0 of 20,000 replicates)`** everywhere. It is a resolution
   floor (`2/(REPS+1)`), not a measured value.
3. "romanized Chinese ~53 (p = 0.0003)" → the trigram p is 0.0001; 0.0003 is the 4-gram
   p-value.
4. `RESULTS.md`'s comparison table must carry the caveat that `src/stats.py` already
   states in its docstring: the romanized-Chinese null is a **synthetic generative
   stand-in, not a corpus**. Replace the language-independence argument's reliance on it
   with the measured critical-IC bound (any language with monogram IC > ≈0.048 is
   excluded at p < 0.05).
5. "English MASC predicts ~29 repeated trigrams" → **~25–29 depending on the English
   source** (Burke 28.7, Austen 25.3, Doyle 25.8). The conclusion is unaffected
   (0 of 24,000 replicates across three corpora reached zero).
6. Replace P-B's uniform-null per-bar CDFs with the conditional random-k-of-16-subset
   test (§8), which is the comparison the argument needs and which supports it better.
7. Soften "no order structure of any kind" / "exactly like a random deal" to account for
   §7: max-distinct-letters-per-string sits at p = 0.010, and two further statistics lean
   the same way.

## dissent

I formed and wrote this verdict without reading validator 1's, to avoid anchoring. Having
then checked it: validator 1 also returns **PARTIAL** (criterion 2 substantially met,
criteria 1 and 3 unmet, criterion 2 alone not a solve), so **there is no disagreement on
the verdict**, and validator 1 independently identifies the polyalphabetic power gap as
the residual weakness in criterion 2, which I concur with. Validator 3's verdict I have
not seen. What follows is therefore additive — reservations that must travel with a PASS
on any component of this claim, not a dispute with a colleague. **If any validator
upgrades this to a solve, or passes pillar 3 as stated, I dissent on two points.**

**First, and this is my strongest doubt: pillar 3 does not license "someone counting
letters."** The statistics establish, very robustly, that the 263-letter inventory was
*not produced by any process that samples letters*. They do not establish that a *person
was counting*. A **depleting physical letter supply** — a compositor's case holding ten
sorts per letter, a set of engraver's letter tiles, a bag drawn without replacement —
used once while the 16 distinct strings were first drafted, would produce exactly the
observed signature: near-exact balance on the deduplicated inventory only (because the
supply was depleted once, during composition), no balance on the 44 stamped instances
(because the draft was then copied repeatedly), and — critically — **no order structure
whatever, because drawing without replacement from a balanced pool IS the deal null that
P-C confirms**. P-C is therefore not evidence for "a person counting"; it is a *positive
prediction of the mechanical alternative*. The claimant dismisses the tooling hypothesis
on the ground that punches are reusable and a deduplicated inventory is not a physical
object — both true, and both aimed at the wrong version of the hypothesis: the constraint
need only have acted once, at drafting, not at stamping. The honest formulation is
"generated under a letter-supply-or-balance constraint at the moment the 16 distinct
strings were first written", with *deliberate counting* and *depleting supply* both live
and, on present evidence, the mechanical one requiring fewer assumptions. This matters
because the claim's contribution to criterion 3 — "whoever made these objects wrote
balanced gibberish and presented it as enciphered financial text… that is an act of
fabrication" — reads intent off a statistic that does not distinguish intent from tooling.
The mild excess within-string letter repetition I found (§7) is the only evidence that
anyone was choosing rather than drawing, and it is a p = 0.01 hint across ~16 tests.

**Second, the language-independence claim as published overstates its footing**, because
its Chinese leg is a synthetic generator the claimant wrote (§4) and its English leg is a
single 1770 tract that returns the most favourable numbers of the three corpora I tried
(§2). Both weaknesses are conservative in direction and I verified that, and the
measured critical-IC bound of ≈0.048 (§4) repairs the argument completely — but the
repair is mine, not the attempt's, and the writeup should carry it before anyone quotes
"no guess about the plaintext language is required, Chinese romanization included." I note
specifically that validator 1 calls the IC leg "the strongest part of the work" while
quoting "0.0739 for Wade-Giles-shaped romanized Chinese (p = 0.0001)" at face value. It is
the strongest part, and I agree — but that particular number is generated by
`synth_romanized_chinese()`, a 28×36 hand-written syllable table sampled uniformly, and
that p is `2/(REPS+1)`. Both validators should be quoting the critical-IC bound instead.

Neither reservation resurrects the cipher hypothesis. I record no doubt at all about the
central negative: I re-derived chi2 = 1.25095 and IC = 0.03968 from the live IACR page
with my own code, computed the exact rather than asymptotic tail probability, and the
strings are not the output of any letter-sampling process. That part I would defend.

---

*Validator 2, 2026-09-24. Reproduction and independent re-derivation performed in a
scratch directory; nothing under `ciphers/` was modified. Scripts and logs for §2–§9 are
not committed to the repository.*
