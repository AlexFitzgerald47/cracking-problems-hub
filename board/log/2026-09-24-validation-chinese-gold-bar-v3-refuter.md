# Validation — Chinese gold bar cryptograms (validator 3, refuter)

claim: The 16 cryptograms are not ciphertext at all — no plaintext exists —
because they were composed under a deliberate letter-balance constraint
(chi2 vs uniform = 1.251 on 25 df over 263 letters, analytic P = 9.3e-13).

problem: `chinese-gold-bar-cipher`

criteria applied: `PROBLEM.md`, success criterion 2, verbatim —

> **A rigorous negative** — a demonstration, with the recomputed
> letter-frequency and repeated-substring statistics actually shown, that the
> string set is statistically indistinguishable from a null model under any
> simple monoalphabetic/polyalphabetic/transposition scheme, which would close
> off a large branch of speculative attack rather than leaving it open by
> default.

validator role: 3 (refuter)

reproduced: **yes, exactly** — every number in the claim reproduces bit-for-bit,
plus independent re-derivation from the live primary source.

verdict: **PARTIAL**

---

## Summary

Criterion 2 is **met**, and I strengthened it: the claimant never ran the
polyalphabetic null the criterion names by name, and I ran it — a Vigenère of
any period 1–40 fails to reach the observed chi2 in 4,000 replicates per period
(minimum 6.19 at period 40, against an observed 1.251). Monoalphabetic,
transposition and polyalphabetic are all closed off.

The **board claim is broader than criterion 2** and at that wider scope it does
not hold at the stated strength. I broke three of its seven evidence points:

1. **Point 1's inference is false.** "Every cipher samples letters and sampling
   leaves multinomial noise" is not true of cycling homophones, a real
   historical technique that is deterministic rather than sampling. I built one.
   A fixed-table cycling homophone reaches chi2 <= 1.251 at rates between
   2.0e-6 and 1.9e-4 — up to **2.3 x 10^8 times more likely** than the 9.3e-13
   the claim quotes. The headline P-value is P(data | uniform multinomial),
   not P(data | cipher), and it is used as if it were the latter.
2. **Point 3's inference is false, and two of its four published numbers are
   wrong by 2–4 orders of magnitude.** "The balance holds on the deduplicated
   inventory and only there... not a physical object, so no punch set ... only a
   person composing the text." Bar face **5.1 is a physical object** and its
   complete stamped text (249 letters, 15 lines) has chi2 = 4.839,
   lower-tail P = **4.0e-6**. The claim's per-bar figures rest on an
   instance table built from an IACR arrangement diagram that **demonstrably
   omits lines**, which I verified both from the photograph and from the
   Cipher Foundation's independent transcription.
3. **Point 7's control is mis-specified.** `GALLOW` *is* an English word of
   length 6. The claimant's wordlist (4,303 words scraped from one 18th-century
   pamphlet) does not contain it. With a 344,415-word dictionary the corpus
   contains one length->=6 English word and the deal null produces one at
   p = **0.019**, not the "0.0005 per corpus, so zero is expected either way"
   the claim states.

What I **could not** break, having tried hard: the arithmetic, the exact null,
the transcription, the deduplication, and the direction-of-noise argument.
Details below, because a failed refutation is only worth recording if the
attempts are named.

---

## Reproduction

Copied the attempt to my scratch dir and ran it there. Nothing under
`ciphers/` was touched.

```
cp -r ciphers/chinese-gold-bar-cipher/attempts/2026-09-24-is-it-a-cipher $SCRATCH/attempt
python3 src/stats.py && python3 src/confirm.py && python3 src/adjudicate.py
```

All reproduce to the digit: chi2 = 1.2509505703422048, pooled IC = 0.0397,
rep3 = 0, rep4 = 0, doubles = 7; uniform null mean 24.89 sd 7.04; MASC-English
IC 0.0606 p = 1e-4; romanized-Chinese IC 0.0739 p = 1e-4; P-A chi2 13.822 on
771 letters (failed, as the claim states); P-B 0.3041 / 0.2532 / 0.0038 /
0.0019; all eleven P-C statistics inside the deal null; P-E as published.

Two reproduction frictions, both cosmetic: `src/make_english_ref.py` and the
P-D wordlist in `src/confirm.py` both read a file four directories up, inside a
*different* problem's attempt folder
(`historical-controversies/junius-letters-authorship/.../gutenberg_2173.txt`).
The pipeline will not run from a copy without that path being recreated. The
derived `data/english_reference.txt` is committed, so only `confirm.py` P-D is
actually blocked.

**Independent re-derivation from the raw source.** I fetched
`https://www.iacr.org/misc/china/cryptograms.html` (HTTP 200, 5,123 bytes) and
parsed the page's own "list of all of the known cryptograms" block. All 16
strings match `data/cryptograms.txt` character for character, all 16 of the
page's own stated lengths are correct, and the total is 263. The corpus is
clean.

---

## Attack 1 — CONSTRUCT THE COUNTEREXAMPLE (the claim's own nominated weak point)

`scratchpad/homophone_attack.py`, `homophone_attack2.py`, `homophone_tail.py`.

### 1a. The first attempt failed for an instructive reason

A homophonic cipher needs more ciphertext symbols than plaintext symbols. The
ciphertext alphabet here is exactly 26 Latin letters, so if the plaintext is
also a 26-letter alphabet there is **no room for homophones at all** and the
scheme degenerates to monoalphabetic (chi2 ~ 220). Cycling homophones are only
available if the plaintext alphabet is small — a digit code, a syllabary, a
code book. That is a real constraint the claim does not state but which works
*in its favour*, and I record it.

### 1b. With a reduced plaintext alphabet, cycling homophones do flatten — hard

Scheme: plaintext symbol *s* has *h_s* homophones, sum h_s = 26; the encipherer
takes the **next** homophone in a fixed rotation (deterministic, not sampling).
Each homophone of *s* then lands on floor(n_s/h_s) or ceil(n_s/h_s).

20,000 replicates each, target chi2 <= 1.2510:

| plaintext alphabet | table | min chi2 | median | P(chi2 <= 1.251) |
|---|---|---|---|---|
| m=10 digits, uniform | fixed in advance | 2.042 | 19.24 | 0 |
| m=10 digits, uniform | tuned to this message | 0.856 | 4.02 | **9.0e-4** |
| m=10 digits, uniform | tuned + message trimmed | 0.526 | 4.18 | **4.0e-3** |
| m=10 digits, amount-like skew | tuned + trimmed | 0.471 | 6.05 | 8.5e-4 |
| m=13 syllabary | fixed in advance | 1.251 | 11.73 | 0 |
| m=13 syllabary | tuned + trimmed | 0.750 | 7.04 | 1.0e-4 |
| m=16 syllabary | tuned | 2.240 | 10.94 | 0 |
| m=20 reduced English | tuned | 41.19 | 69.66 | 0 |

500,000 replicates for the **fixed-table** case — the historically realistic one,
where the encipherer counts *nothing* about this particular message:

| scheme | min chi2 | median | P(chi2 <= 1.251) |
|---|---|---|---|
| m=10 digits, h = 3,3,3,3,3,3,2,2,2,2 | 1.053 | 19.24 | 2.0e-6 |
| m=13 syllabary, h = 2 x 13 | 1.053 | 11.73 | 1.4e-5 |
| m=13 syllabary, mildly skewed | 1.251 | 15.88 | 2.0e-6 |
| **m=9 code, h = 3 x 8 + 2** | **0.460** | 11.73 | **1.9e-4** |
| m=16 syllabary, h = 2 x 10 + 1 x 6 | 5.996 | 46.53 | 0 |

**This is the break.** The claim's sentence — *"Every cipher samples letters and
sampling leaves multinomial noise ... Equalisation this precise is not something
a sampling process does"* — is exactly right about sampling and exactly wrong as
a statement about ciphers, because a cycling homophone does not sample. A
fixed-table cycling homophone over a nine-symbol code reaches the observed
flatness once in ~5,000, not once in ~10^12. The likelihood ratio between
"uniform-multinomial cipher output" and "fixed-table cycling homophone" at the
observed value is about **2.3 x 10^8**; with a table sized to the message
(counting the *plaintext*, which for a ten-symbol code book is a mundane
clerical act) it is about **4.8 x 10^9**.

The claim's 9.3e-13 is therefore not evidence against "a cipher". It is
evidence against "a cipher whose output is a uniform multinomial draw", which
is a much smaller class than the claim treats it as.

### 1c. Why this does *not* finish the claim off

Honesty requires the other half. The arithmetic of the scheme:

```
chi2  =  sum_s  h_s (n_s/h_s - 10.115)^2 / 10.115   +  rounding (<= m/4/10.115)
```

To get chi2 <= 1.25 the encipherer needs |n_s/h_s - 10.115| <~ 0.2 for nearly
every s — the *plaintext* symbol counts must sit within about 2% of a prescribed
target. A table fixed in advance cannot arrange that, because n_s fluctuates
multinomially with sd ~ 5 against a tolerance of ~0.5. So even the strongest
cipher counterexample I could build still needs someone counting symbols; the
counting has only moved one stage upstream, from ciphertext to plaintext.

And the scheme is narrow: it requires (a) homophony with a **cycling** rather
than a randomly-chosen homophone, (b) a plaintext alphabet of at most ~13
symbols, and (c) a table proportioned to the message. The prior on that specific
design for a 1930s Shanghai bank certificate is not high. So the claim's
*conclusion* — these are not the output of an ordinary cipher — survives. Its
*argument* and its *number* do not.

Other deterministic schemes I coded and that failed to reach the target
(3,000 replicates each unless noted):

- **Trithemius / progressive key** (walk the tableau in strict rotation, the
  literal form of "works through a tableau in rotation"): median 23.79,
  min 5.996 over 3,000 — no better than a one-time pad, because summing over
  all 26 shifts restores the full plaintext-frequency variance.
- Trithemius over repeated bank boilerplate: chi2 32.29.
- Fixed nomenclator, arbitrary codegroups over boilerplate: median 84.7,
  min 25.97.
- Cycling homophones over a highly repetitive plaintext: chi2 331.8 (repetition
  *hurts*, because it concentrates mass on few plaintext symbols).
- Keyed columnar transposition of a balanced text: preserves counts exactly, so
  it changes nothing — noted for completeness; it is not a counterexample,
  it is the claim's own point 2.
- Vigenère at every period 1–40: see Attack 5.

---

## Attack 2 — RE-TRANSCRIBE FROM THE PHOTOGRAPHS

Everything reachable. `https://www.iacr.org/misc/china/` and
`/cryptograms.html` both HTTP 200. I downloaded all fifteen bar photographs
(`images/5.1.jpg`, `9.1.jpg`, `10.2.jpg`, `6.2`, `7.1`, `7.2`, `8.2`, `9.2`,
`10.1`, `11.1`, `11.2`, `12.1`, `12.2`, `13.1`, `13.2`), max available
resolution 1152 px on the long edge. `http://cipherfoundation.org/modern-ciphers/chinese-gold-bar-ciphers/`
and its `chinese-gold-bar-transcription/` subpage: both HTTP 200 and read in
full. `ciphermysteries.com/the-chinese-gold-bar-ciphers` returns 404.

**Finding 2a — the disputed bar-5.1 characters.** The Cipher Foundation page
gives, verbatim, `UGMNCBXCKDBEY` and `KOWVRSRWTMLDH`. The claimant's
`adjudicate.py` encodes exactly these two variants, so point 6 is correctly
sourced; I confirm the provenance the claim asserts.

Photograph `12.1.jpg` turns out to be a **high-magnification detail of the same
bar face as 5.1**, and it shows the first disputed line far better than 5.1
itself does. My own reading of it is `UGMNCBXC F L D (?) E Y`: the head
`UGMNCB X C` is unambiguous, and after `C` I read `F`, `L`, `D`, `E`, `Y` with
no clear `B` between `D` and `E` — i.e. 13 glyphs where IACR lists 14. I can
neither confirm IACR's `B` nor Pelling's `K`-for-`FL`; the glyphs touch and
1152 px is marginal. On the second line `5.1.jpg` shows `K O W ? R S R W T M L
D H` — I see no `K` between `RSR` and `W`, which favours Pelling's 13-character
reading, again without certainty. **Limit: no higher-resolution image is
published, so neither disputed character can be settled from what is online.**

**Finding 2b — the alternative-transcription set, recomputed.** The claim's
point 5 says noise can only degrade balance. I tested every plausible variant I
could construct, including ones that *remove* letters (the direction most likely
to help a refuter):

| transcription | N | chi2 | P(chi2_25 <= obs) | letters off ten |
|---|---|---|---|---|
| IACR as published | 263 | 1.251 | 9.30e-13 | E11 I13 O9 S11 T9 |
| Pelling / Cipher Foundation | 261 | 1.490 | 7.44e-12 | E11 F9 I13 L9 O9 S11 T9 |
| my 12.1 reading (drop the B) | 262 | 1.374 | 2.84e-12 | B9 E11 I13 O9 S11 T9 |
| my 5.1 reading (drop the K) | 262 | 1.374 | 2.84e-12 | E11 I13 K9 O9 S11 T9 |
| both of my readings | 261 | 1.490 | 7.44e-12 | B9 E11 I13 K9 O9 S11 T9 |

Every one stays in the 1e-12 range. **No alternative transcription I can
construct moves the deviant letters away from ten enough to matter.** I also
enumerated all 6,575 single-character substitutions of the inventory: chi2 ranges
0.658 to 2.240, and only 5.6% of them *lower* chi2. Noise degrades balance 94%
of the time, so point 5's direction argument holds in expectation — though the
claim's implied strict monotonicity ("noise ... cannot manufacture it") is not
strictly true at the single-edit level. **Point 6 stands. Attack failed.**

**Finding 2c — the instance table is materially incomplete. This one lands.**
IACR's *arrangement diagrams* (as distinct from its canonical list) omit lines
that are visible in the photographs:

- Bar **5.1**: the bottom block is drawn with three lines; the photograph shows
  **four** — the fourth is `FEWGDRHDDEEUMFFTEEMJXZR`. The Cipher Foundation's
  independent transcription of the same bar lists it too. Two independent
  confirmations.
- Bar **9.1**: the photograph carries `HLMTAHGBGFNIV` at top right (clearly
  legible), and `JKGFIJPMCWSAEK` plus what reads as
  `SKCDKJCDJCYQSZKTZJPXPWIRN` faintly across the bottom landscape. None of the
  three appears in IACR's 9.1 arrangement or in `data/instances.tsv`.

`data/instances.tsv` inherits all of these omissions. It is the sole input to
P-A and P-B. Consequences in Attack 3.

**Finding 2d, incidental.** The Cipher Foundation page reproduces the Chinese
inscription, which does name 何应钦 / 朱培德 / 李福林 (He Yingqin, Zhu Peide,
Li Fulin) and gives the figure as 叁亿伍仟伍佰万 ($355m, not $300m) and the
weight as 1.8 kg. `PROBLEM.md` flags those three names as "unverified as
actually appearing on the artifacts"; they are now attested in a secondary
transcription, which matters for anyone working criterion 1 with cribs.

---

## Attack 3 — THE INFERENTIAL STRUCTURE

### 3a. Is the chi2 asymptotic valid at n=263, 26 cells, E=10.1? — attack failed

I computed the **exact** probability rather than trusting the chi2_25 CDF.
chi2 <= 1.2509505... is equivalent to sum(d_i - 0.1154)^2 <= 12.654 with
d_i = c_i - 10 and sum d_i = 3. Enumerating all deviation multisets that satisfy
it (22 patterns; the enumeration is provably complete, since the cheapest
deviation costs 0.7825 and the budget caps the number of nonzero cells at 11)
and summing the exact multinomial probabilities:

```
analytic P(chi2_25 <= 1.251)                    = 9.2979e-13   (what the claim reports)
EXACT   P(chi2   <= 1.251 | Multinomial(263,U))  = 8.2755e-13
ratio exact/analytic                             = 0.890
```

The asymptotic overstates the tail by 11%. **The headline number is sound to
within a factor of 1.1.** Simulation cross-check: 0 hits in 300,000 — consistent,
uninformative at this depth, as expected.

Note in passing that the observed deviation vector (I+3, E+1, S+1, O-1, T-1) has
sum of squares exactly 13, sitting precisely on the boundary of the acceptance
region. Nothing turns on it, but it means the reported value is the *largest*
chi2 in its equivalence class, not a cherry-picked interior point.

### 3b. Is the deduplication a post-hoc analytic choice? — attack failed

This was my best structural hope and it dies on the primary source. The IACR
page does not merely list the bars' arrangements; it prints, under the heading
**"Here is a list of all of the known cryptograms"**, exactly those 16 strings
with their lengths. The deduplicated inventory is **the source's own canonical
list**, not something the analyst constructed after seeing which aggregation
paid. `PROBLEM.md`, written before any analysis, already describes the page as
containing "16 distinct transcribed strings". `data/cryptograms.txt` was
committed at the freeze (7539d24); `data/instances.tsv` only at 832a4ef. The
ordering rules out fitting the aggregation to the answer.

I also checked whether two of the "16 distinct" strings might be one string read
twice, which would falsify the dedup. Minimum normalised Levenshtein distance
over all 120 pairs is **0.67** (`RHZVIYQIYSXVNQXQWIOVWPJO` / `HFXPCQYZVATXAWIZPVE`).
Nothing close. And leave-one-string-out never lifts the P-value above 9.4e-06;
no single string is carrying the effect.

Aggregation sensitivity, for the record:

| aggregation | N | chi2 | lower-tail P |
|---|---|---|---|
| inventory, 16 distinct | 263 | 1.251 | 9.30e-13 |
| all stamped instances (as claimed) | 771 | 13.822 | 0.035 |
| all stamped instances + my photo lines | 846 | 18.147 | 0.164 |

So the spectacular value does exist only under one aggregation — but that
aggregation is the source's own and was fixed before the analysis. **Attack
failed.**

### 3c. Point 3 — "only on the deduplicated inventory", "not a physical object"

**This is where the claim breaks.** With the omitted lines restored:

| bar face | IACR arrangement only | + lines from the photographs |
|---|---|---|
| 10.2a | 8 distinct, N=103, P = 3.04e-1 | unchanged |
| 10.2b | 5 distinct, N=110, P = 2.53e-1 | unchanged |
| 9.1 | 9 distinct, N=152, P = **3.79e-3** | 12 distinct, N=204, P = **9.52e-6** |
| 5.1 | 13 distinct, N=215, P = **1.89e-3** | 14 distinct, N=238, P = **1.99e-7** |

The board claim states these as "0.304, 0.253, 0.0038 and 0.0019". Two of the
four are wrong, by two and four orders of magnitude respectively, because the
instance table is built from arrangement diagrams that drop lines.

Worse for the argument: bar face **5.1 as a physical object** — all fifteen
stamped lines, repeats included, exactly what a punch set or a type case would
have had to produce — gives

```
N = 249,  chi2 = 4.839,  P(chi2_25 <= obs) = 3.96e-6
counts: A9 B8 C10 D10 E11 F10 G9 H8 I13 J11 K11 L8 M8 N9 O10 P10 Q8 R8 S11 T8 U10 V8 W10 X11 Y11 Z9
```

The claim's argument is: *"A deduplicated inventory of distinct strings is not a
physical object, so no punch set, type case or casting process can have produced
it — only a person composing the text."* There **is** a physical object here
whose letter counts are flat at 4.0e-6. The premise is false as stated, so the
inference fails. H3 is in fact still killed — bar 10.2b's physical counts run
J21, S18, C16, chi2 = 49.4, which no ten-per-letter punch set can yield — but it
is killed by 10.2b, not by the argument the claim gives.

And the deeper problem: the claim treats "the balance lives on the deduplicated
inventory" as evidence *for* composition and *against* encipherment. It is not.
Under the cipher hypothesis the deduplicated inventory is precisely *the
ciphertext, enciphered once, before the engraver stamped some groups more than
once*. Every cipher hypothesis makes the same prediction. **Point 3 does not
discriminate H1 from H2 at all.**

### 3d. "Not a simple cipher" -> "there is no plaintext to recover"

That leap is not supported, and the claim's own structure shows why. The
evidence licenses a negative about a class of generative processes. It cannot
license "no plaintext exists", because the balance statistic is silent about any
scheme whose *design goal* is equalisation — which the claim itself concedes
under "What I am NOT claiming" — and, per Attack 1, that concession is
quantitatively much larger than the claim lets on. The falsifiable content is
the narrow negative. The headline sentence is not falsifiable by the method that
produced it.

### 3e. FREEZE.md read adversarially

Checked against git. `7539d24` (freeze) contains `FREEZE.md`,
`data/cryptograms.txt`, `data/english_reference.txt`, `out/stats.json`,
`src/make_english_ref.py`, `src/stats.py`. `832a4ef` (confirm) adds
`instances.tsv`, `confirm.py`, `adjudicate.py`, `out/confirm.json`, `RESULTS.md`.
`out/stats.json` is **byte-identical** between the two commits — no silent rerun.
The sequencing is honest.

Two things are not:

1. FREEZE.md asserts *"Everything derived up to this point used only the
   aggregate letter counts of the 16 distinct strings — no use of string order,
   of the per-bar layout, or of the repetition structure."* The same document's
   derivation set reports "Zero repeated trigrams anywhere in the corpus", which
   **is** order information. The sentence is false about `stats.py`, though it is
   true about the balance result specifically, which is what actually matters.
2. `out/stats.json` at freeze time already contains the `corpus_shuffle` null
   with p-values for `ic` (0.2439), `doubles` (0.7309), `rep3` (0.6575) and
   `rep4` (1.0). `corpus_shuffle` is the same deal null that P-C "predicts"
   against, and four of the eleven statistics P-C registers were therefore
   already computed and already known to sit inside it. **P-C is partly a
   restatement of a known result, not a prediction.** The genuinely new parts
   are max letter multiplicity, max single-string IC, and periodic IC at
   periods 2–8 — which did pass.

The headline balance result was never presented as a prediction: FREEZE.md
correctly files it under "already established", and the claim says only that it
"was derived from aggregate letter counts alone". That is accurate. No
misrepresentation there.

---

## Attack 4 — the nulls the claimant did not run

**Polyalphabetic.** Criterion 2 names it explicitly, and `stats.py` has no
Vigenère null at all — only uniform, corpus-shuffle, MASC-English and
MASC-romanized-Chinese. I ran it: 4,000 replicates per period, English plaintext,
random key, the observed 16 length structure.

| period | mean chi2 | 5th pct | min | P(chi2<=1.251) | mean pooled IC |
|---|---|---|---|---|---|
| 1 | 222.2 | 183.6 | 147.0 | 0 | 0.0607 |
| 2 | 123.6 | 82.9 | 47.5 | 0 | 0.0500 |
| 4 | 74.4 | 44.6 | 19.6 | 0 | 0.0443 |
| 6 | 57.8 | 33.5 | 15.9 | 0 | 0.0420 |
| 10 | 44.5 | 26.2 | 11.1 | 0 | 0.0401 |
| 20 | 34.2 | 20.2 | 9.6 | 0 | 0.0385 |
| 40 | 29.3 | 16.9 | 6.2 | 0 | 0.0385 |

Observed: chi2 = 1.251, IC = 0.0397. **The polyalphabetic branch is closed by
the chi2 at every period, and by nothing else** — note that from period 12
upward the Vigenère IC (0.0385–0.0394) is indistinguishable from the observed
0.0397, exactly as the claim's own "stated limits" section concedes. This
confirms the claim on the point criterion 2 names, and it is the claimant's
omission that I am supplying.

**The GALLOW control, redone.** `confirm.py` builds its wordlist by regexing
length->=6 tokens out of one 18th-century political pamphlet — 4,303 distinct
words. `GALLOW` is a genuine, if archaic, English verb (King Lear III.ii) and it
is not in that pamphlet. With `words_alpha` (344,415 words of length >= 6):

```
observed English substrings of length >= 6 : ['GALLOW']
deal null (20,000 replicates)              : mean 0.0196 per corpus
P(>= 1 hit)                                 = 0.019
```

The claim states "The corpus contains **zero** English words of length >= 6, and a
random deal from the balanced pool produces them at 0.0005 per corpus, so zero
is expected either way." Both halves are wrong: there is one, and the null rate
is 39x higher than stated. P-D's "CONFIRMED" is an artefact of an undersized
wordlist. I would not read much into p = 0.019 on a single self-selected
feature — that is a textbook garden-of-forking-paths number, and `GALLOWLS` with
its intrusive L is still not `GALLOWS` — but the control as run does not
establish what the claim says it establishes.

---

## What I tried and could not break

Recorded specifically, per the role:

- The chi2 arithmetic: reproduces exactly, and is 11% conservative against the
  exact multinomial null (8.28e-13 vs 9.30e-13 analytic).
- The corpus: verified character-by-character against the live IACR page,
  including the page's own 16 stated lengths. No transcription error in
  `data/cryptograms.txt`.
- The deduplication: it is the source's own canonical list, registered in
  `PROBLEM.md` before analysis and committed at the freeze. Not post-hoc.
- Near-duplicate strings (two of the 16 being one string misread twice): minimum
  normalised edit distance 0.67 over all 120 pairs. Nothing.
- Leave-one-out: no single string carries the balance (worst case P = 9.4e-6).
- Alternative transcriptions: five variants including two of my own from the
  photographs. All stay at 1e-12 or below.
- Direction of noise: 94% of the 6,575 possible single substitutions raise chi2.
- Monoalphabetic and transposition: excluded by IC invariance, reproduced.
- Polyalphabetic: excluded at every period 1–40 by a null I ran myself.
- Trithemius, nomenclators, transposition-of-balanced-text, and repetitive
  plaintexts: none comes close.
- The freeze sequencing: `out/stats.json` byte-identical across the two commits.

---

## reasoning

On the **pre-registered criterion 2** the work delivers what was asked and more.
The letter-frequency statistics are shown; the repeated-substring statistics are
shown (rep3 = rep4 = 0 against 29 and 8 for substituted English, 53 and 14 for
romanized Chinese); monoalphabetic and transposition fall to the IC invariance
argument language-independently; and the polyalphabetic branch, which the
claimant left untested, falls too when I test it. Criterion 2: **met**.

The **board claim** is considerably stronger than criterion 2 and I do not think
it is carried. Its headline P-value is computed against a uniform-multinomial
null and then used to exclude "any cipher", and I have built the cipher that
exposes the gap: a fixed-table cycling homophone over a small plaintext alphabet
is deterministic, not sampling, and reaches the observed flatness up to 2.3e8
times more readily than the quoted figure implies. Its point 3 rests on a
premise I showed to be false with the primary photographs and a second
independent transcription, and on per-bar numbers that are wrong by up to four
orders of magnitude once the omitted lines are restored — and in any case point 3
does not discriminate the cipher hypothesis from the composition hypothesis,
because both predict that the balance lives on the deduplicated set. Its
point 7's control is mis-specified and its stated conclusion reverses under a
real dictionary.

None of that resurrects a decipherment. The cipher that survives my strongest
attack still needs someone counting symbols, only at the plaintext stage; the
corpus still has zero repeated trigrams, an IC at the flat floor, and no order
structure a random deal cannot produce. The direction of the claim is, in my
judgement, probably right. But "probably right" with a P-value inflated by eight
to nine orders of magnitude against the hypothesis it is aimed at, three broken
supporting points, and a conclusion ("there is no plaintext to recover") that
the method cannot falsify, is a PARTIAL and not a PASS.

**PARTIAL.** Criterion 2 met. The claim as posted overreaches and should be
restated as the narrow negative it can actually support: *the 16 strings are
excluded as the output of a monoalphabetic, polyalphabetic or transposition
cipher over any natural language, and are flatter than any sampling process
produces; a deterministic-equalisation scheme, homophonic or compositional,
remains — and the balance statistic cannot separate those two.*

## dissent

Recorded in advance of the other two verdicts, since I am writing without
sight of them.

1. If validators 1 or 2 pass the claim **as written** — "not ciphertext, no
   plaintext to recover" — I dissent. The fixed-table cycling-homophone
   simulation in Attack 1b is the specific reason, and it is reproducible:
   `homophone_tail.py`, 500,000 replicates, m=9, P(chi2 <= 1.251) = 1.94e-4.
   Any pass should be explicitly scoped to criterion 2 and should not carry
   the "no plaintext exists" sentence.
2. If either fails the claim outright, I dissent the other way. Criterion 2 is
   genuinely met and the polyalphabetic exclusion I added closes the last branch
   the criterion names. This is real progress on the board's stated question and
   should not be thrown away over the overreach in its framing.
3. Three specific corrections should be recorded against the attempt regardless
   of the panel's verdict, because they are matters of fact, not judgement:
   (a) `data/instances.tsv` omits at least four stamped lines that are visible
   in the IACR photographs, one of which the Cipher Foundation also transcribes;
   (b) the per-bar figures in the claim's point 3 become 9.5e-6 and 2.0e-7 once
   those lines are restored, and bar face 5.1's *physical* text is balanced at
   4.0e-6; (c) P-D's wordlist is too small to contain `GALLOW`, and the test
   inverts when a real dictionary is used.

Artefacts: `homophone_attack.py`, `homophone_attack2.py`, `homophone_tail.py`,
`refute.py` in my scratch dir, plus the fifteen downloaded bar photographs and
the two fetched Cipher Foundation pages. Nothing under `ciphers/` was modified.

**HELD — awaiting human sign-off.**
