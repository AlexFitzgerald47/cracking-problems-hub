# The Blitz Ciphers have less bigram structure than any comparable block of genuine ciphertext — or one glyph in six is mistranscribed

**2026-09-27 · cracker session · first substantive Hub work on this problem**

Design frozen in `FREEZE.md` before any test was run; holdout prediction frozen separately in
`FREEZE_HOLDOUT.md` before the holdout was touched. Both freezes are in the git history ahead of
the results. Two of the four frozen predictions passed, one passed on the holdout and failed on
its point range, and **one was refuted outright with its direction backwards** — reported first.

---

## 0. What was refuted

I predicted (FREEZE, 3a) that the Borg cipher — monoalphabetic substitution of Latin — would show
an **excess** of adjacent identical symbols against a frequency-preserving shuffle, because Latin
has doubled letters and monoalphabetic substitution preserves them exactly.

**Wrong, and backwards.** Borg shows a strong *deficit*: z = **-47.3** over the whole 120,191-token
document, median **-3.21** per 470-token block. Copiale the same, z = **-33.0** overall. The reason
is elementary once seen: a within-line shuffle of a text's own symbols produces adjacent repeats at
rate Σpᵢ², about 4–7 % here, and **no natural language comes close to that** — English, German and
Latin all avoid adjacent identical letters far below their own letter frequencies would imply.

So a doublet **deficit is a natural-language signature**, not a fabrication signature, and
prediction 3b's logic was inverted. This matters beyond this problem: anyone reaching for
"hand-faked sequences avoid repeats" as a hoax detector on enciphered text will find genuine
ciphertext avoiding them harder.

---

## 1. Evidence and provenance

**Primary.** There is **exactly one transcription of Blitz pages 7 and 8 in existence**: Nick
Pelling's, published 2014-10-24 on Cipher Mysteries. The
`matthewdgreen/cipher_benchmark` copy that `HANDOVER.md` pointed this session at is
**byte-identical** to it (and its "canonical" and "diplomatic" files are byte-identical to each
other), so it is a mirror, not an independent reading. Every number below inherits Pelling's glyph
decisions. `data/p7.txt` (470 tokens, 53 types, 24 lines), `data/p8.txt` (159, 41, 11).

**Holdout.** Pelling's *original* 2011/2013 key transcription of other pages, from the permanent
page `ciphermysteries.com/other-ciphers/blitz-ciphers` (mirrored at `cipherfoundation.org`).
Different pages, different transcription key, three years earlier. 581 tokens in 11 paragraphs;
**paragraph 3 excluded before testing** because its glyph sequence runs `ABCDEFGHIJKL…` and
`PQR…STUVWXYZ` — it coincides with the order of Pelling's own key, so its "structure" is the key's
ordering. 468 tokens, 47 types remain. `data/holdout_2011key.txt`.

**Comparanda — audited, because the comparandum is the least-audited object in a session.**
Copiale (101 pp, 74,860 tokens, 136 symbols, homophonic + nomenclator, German) and Borg (397 pp,
120,191 tokens, 77 symbols, monoalphabetic, Latin), both solved and verified, canonical
transcriptions from `cipher_benchmark`. Audited: no empty pages; the symbol maps are genuinely
global (only page 1 of each document introduces S001..S008 in first-appearance order, as a global
map built from page 1 requires — a per-page map would have done it on all 498). Borg's `|` word
separator is stripped so its text has the same no-word-boundary shape as Blitz, which is the
conservative direction. `data/comparanda.sha256`; rebuild with `src/fetch_comparanda.sh`.

---

## 2. The null

Every test uses one null: **shuffle the tokens within each line**. It holds each line's symbol
multiset fixed — so the page's unigram distribution, its line lengths and its per-line composition
all survive exactly — and destroys only adjacency. It is the tightest null that still answers "is
there anything here beyond the symbol frequencies", and it is immune to the objection that the
Blitz frequency distribution is itself odd. 20,000 permutations for targets, 1,500–2,000 for
reference blocks. `src/fastnull.py`.

---

## 3. Pipeline validation and power (prediction 2a, 2b — both PASS)

| corpus | n | bigram-IC z | p |
|---|---:|---:|---:|
| Copiale p011 / p054 / p094 | 822 / 741 / 732 | +18.7 / +24.5 / +21.6 | 5e-5 |
| Borg 0022r / 0104r / 0184r | 329 / 354 / 251 | +11.5 / +12.3 / +5.5 | 5e-5 |
| Copiale, all 101 pages | 74,860 | +871 | 5e-4 |
| Borg, all 397 pages | 120,191 | +378 | 5e-4 |

Prediction 2a holds: substitution ciphertext of a natural language keeps its bigram repetition.

**Power (2b), the prediction that removes the excuse.** Cutting the genuine documents into
non-overlapping contiguous blocks of Blitz size and re-running the identical test:

| reference | blocks | z p05 | z median | z p95 | **power at p<0.05** |
|---|---:|---:|---:|---:|---:|
| copiale@159 | 416 | +1.23 | +4.36 | +8.52 | 0.885 |
| borg@159 | 718 | +2.34 | +4.97 | +8.77 | 0.982 |
| copiale@470 | 151 | +9.31 | +12.63 | +17.60 | **1.000** |
| borg@470 | 251 | +9.18 | +13.11 | +18.72 | **1.000** |
| copiale@629 | 114 | +12.63 | +16.59 | +23.31 | **1.000** |
| borg@629 | 188 | +12.41 | +16.65 | +23.26 | **1.000** |

At Blitz length the test is saturated. A Blitz result in the genuine range cannot be dismissed as
noise, and a Blitz result outside it cannot be dismissed as "too short to tell".

---

## 4. The result (prediction 2c)

| target | n | bigram-IC z | p | genuine blocks at or below it |
|---|---:|---:|---:|---|
| **Blitz p7** | 470 | **+5.84** | 5e-5 | **0 / 151** copiale@470 (min +6.42), **0 / 251** borg@470 (min +7.33) |
| **Blitz p7+p8** | 629 | **+6.81** | 5e-5 | **0 / 114** copiale@629 (min +10.73), **0 / 188** borg@629 (min +8.02) |
| **Holdout (2011 key)** | 468 | **+4.94** | 5e-5 | **0 / 151**, **0 / 251** |
| Blitz p8 | 159 | +2.42 | 0.020 | 70 / 416, 40 / 718 — unremarkable |

The Blitz pages **do** contain real structure beyond their symbol frequencies: every result above
is significant, some at the 20,000-permutation floor. They contain **much less of it than any
comparable block of genuine ciphertext**. At 470 tokens the *lowest* of 402 genuine blocks sits
above the *highest* Blitz value. Page 8 alone carries no information either way; 159 tokens is
where this test runs out.

**The holdout replicated it** (`FREEZE_HOLDOUT.md`): H1 pass (z>0, p<0.05), **H2 pass** (z below
the genuine 5th percentile and inside the frozen point range [+3, +9]) — on different pages, under
a different transcription key, made three years earlier, and against a known bias in the *opposite*
direction (the 2011 key merges at least two glyphs, per Tim T's correction of 5 Dec 2013, and
merging can only raise apparent repetition). **H3 failed**: the holdout's doublet z is -2.53, well
inside the genuine range (39/151 copiale@470 and 70/251 borg@470 blocks are at or above it), so the
doublet anomaly seen on pages 7–8 (p7 z = -0.42, 0/151 and 3/251) **does not generalise** and I do
not rely on it.

One result, replicated once, on one statistic. That is what this session establishes.

---

## 5. Test 1, exploratory: pages 7 and 8 do not share a symbol distribution

Labelled exploratory in `FREEZE.md` because I had already seen both unigram tables when I wrote it.
Two-sample chi-square homogeneity against a pooled-permutation null at the observed (470, 159):

- **Blitz p7 vs p8: chi² = 134.3 on 55 df, null mean 55.0 ± 9.6, z = +8.29, p ≤ 2.5e-4** (the
  permutation floor — all 4,000 resamples were lower).
- Copiale, consecutive-page pairs at the same sizes: 100 comparisons, median -0.77, max **+2.02**.
- Copiale, *within*-page splits (first 470 vs next 159 of the same page): 92 comparisons, max +1.84.
- Borg pages are ~300 tokens and cannot supply a 470-block, so at its own feasible (250, 159):
  348 comparisons, median +0.39, max **+7.65**.

**0 of 540 genuine comparisons reach +8.29** — but Borg's tail comes within 0.64 of it, so this is
a one-in-several-hundred observation, not an impossibility, and the length-matched reference
(Copiale) is the only one that is strictly comparable. The difference is broad, not one bad symbol:
the top 12 of 56 symbols supply 66 % of the chi². Largest movers are `Z` and `H` (each 2/470 on p7,
7/159 on p8) and `.` (26/470 on p7, 1/159 on p8). Fifteen codes occur only on p7, three only on p8.

Three confounds keep this from being decisive, and all three are real: Pelling records **at least
two hands** in the corpus ("a larger, bolder presentation hand and a small, finer annotation hand"),
so p7 and p8 may simply be different scribes; both pages were transcribed in one session with an
alphabet he was expanding as he went; and page 7 was read from an image rotated 180°.

---

## 6. What it would take to explain the result innocently

Noise degrades order and cannot create it, so the deficit is only evidence about the *document* if
transcription error cannot produce it. Two models, both run on the genuine corpora:

**(a) Random substitution** (`src/noise_model.py`): each token independently replaced, with
probability ε, by one drawn from the block's own unigram distribution. ε required to bring the
genuine median down to the Blitz value:

| | Blitz p7 (+5.84) | Blitz p7+p8 (+6.81) | holdout (+4.94) |
|---|---:|---:|---:|
| copiale | ε ≈ **0.143** | ε ≈ 0.180 | ε ≈ 0.179 |
| borg | ε ≈ **0.216** | ε ≈ 0.211 | ε ≈ 0.248 |

**About one glyph in five to one in seven would have to be outright wrong.**

**(b) Over-splitting** (`src/split_model.py`), which is the error Pelling says he deliberately
committed — *"I'd rather slightly expand the alphabet when transcribing than make a wrong
assumption that can't easily be undone"* — and therefore the one that matters. Symbols covering
fraction φ of tokens are each relabelled to one of two sub-codes at random:

| φ | 0.0 | 0.3 | 0.5 | 0.7 | 1.0 |
|---|---:|---:|---:|---:|---:|
| copiale@470 median z | +12.2 | +9.9 | +8.5 | +7.8 | **+6.7** |
| …types | 77 | 87 | 97 | 109 | **136** |
| borg@470 median z | +14.1 | +12.9 | +11.2 | +9.7 | **+7.2** |
| …types | 32 | 35 | 38 | 42 | **55** |

Over-splitting is far less damaging than random substitution, and **it cannot reach the Blitz value
at any partial rate**: only φ = 1.0, every glyph in the document split two ways, gets close — and
that doubles the alphabet. So the over-split explanation is not free, it carries a **falsifiable
consequence**: Blitz's 53 codes on page 7 would have to be a doubled rendering of a true alphabet
of roughly **26 glyphs**, and those 53 codes would then pair up into 26 contextually
indistinguishable pairs. That is a testable prediction and nobody has tested it (§8).

---

## 7. What this does and does not support

**Supported.** Blitz pages 7–8 and the 2011-key pages carry statistically unambiguous structure
beyond their symbol frequencies — they are not random glyph sequences, and Rich SantaColoma's
"outright fake" in the loosest sense (someone scribbling) is not what the text looks like. They
also carry **substantially less such structure than genuine substitution ciphertext of natural
language at the same length**, replicated on a holdout, with 0 of 402 length-matched genuine blocks
as low, at a length where the test has power 1.000.

**Not supported.** That the Blitz Ciphers are a hoax. A p-value against a shuffle null is
P(data | that shuffle), never P(data | hoax) or P(data | cipher). At least five live explanations
survive everything above, and this session cannot separate them:

1. a **mistranscription** at ~15–20 % per glyph, or a wholesale doubling of the alphabet (§6);
2. a cipher with **heavy nulls** — inserting meaningless glyphs is precisely a bigram-structure
   destroyer, and Pelling's own 2013 post is about null detection on this corpus;
3. a **polyalphabetic or cycling-homophone** scheme, which flattens bigram structure by design;
4. a plaintext that is **not running natural-language prose** — a list, a table of names, numbers,
   an index — for which the comparanda are simply the wrong benchmark;
5. a **fabrication**, which is also what "less structure than real ciphertext" looks like.

Pelling's 2014 verdict — *"a bit loose and patternless … the contact tables don't quite 'feel'
right"* — was correct, and this session's contribution is to replace "feel" with a number
(+5.84 against a genuine floor of +6.42, holdout +4.94) and with the exact price of the innocent
explanation (ε ≈ 0.14–0.25, or a doubled alphabet).

**Also not supported:** anything about the unreleased corpus. Eight images of a set believed to be
"significantly larger" are public; two of them have a transcription with the expanded key and some
part of the rest has one with the original key. Nothing here is a statement about the document.

---

## 8. Files

```
FREEZE.md              design, frozen before any test
FREEZE_HOLDOUT.md      holdout prediction, frozen before the holdout was touched
data/p7.txt p8.txt     Blitz pages 7-8 (Pelling 2014 expanded key)
data/holdout_2011key.txt   Pelling's original-key transcription, paragraph 3 marked excluded
data/comparanda.sha256 498 Copiale+Borg files, per-file and aggregate digests
src/fetch_comparanda.sh    rebuilds the comparanda from public sources
src/blitzlib.py            loaders and pure-python reference statistics
src/fastnull.py            vectorised within-line shuffle null (bigram IC, doublets)
src/test23_structure.py    Tests 2 and 3 on Blitz and on known-genuine pages
src/calibrate.py           length-matched reference distributions and the power curve
src/test_holdout.py        the frozen holdout test, with pass/fail printed against the freeze
src/test1_homogeneity.py   Test 1, page-distribution homogeneity
src/test1_extra.py         second genuine reference and per-symbol chi2 contributions
src/noise_model.py         random-substitution transcription noise
src/split_model.py         over-splitting transcription noise
out/*.json                 every number above
```

Reproduce: `src/fetch_comparanda.sh /tmp/comp`, then run each `src/test*.py` and
`src/*_model.py` with `/tmp/comp` as the argument. Pure Python plus numpy; the whole battery is
about 25 minutes on one core.
