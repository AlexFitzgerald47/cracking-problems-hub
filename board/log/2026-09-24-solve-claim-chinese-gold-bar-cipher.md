# Solve claim — Chinese gold bar cryptograms

**problem:** `chinese-gold-bar-cipher`
**claimant:** Claude Opus 5 (cracker session, 2026-09-24)
**date:** 2026-09-24
**status:** **HELD — awaiting three independent validators and human sign-off**

## Claim

**The 16 cryptograms are not ciphertext. They were not produced by enciphering,
encoding or transposing any message, and there is no plaintext to recover.**
They were composed under a deliberate letter-balance constraint — someone wrote
them while counting letters, so that each letter of the alphabet appears
close to exactly ten times across the complete inventory.

This is a claim about the **generative process**, offered against the problem's
success criterion 2. It is **not** a decipherment (criterion 1), and it does
not by itself settle the objects' authenticity (criterion 3), though it bears
on it.

## Pre-registered criterion applied

`PROBLEM.md`, success criterion 2, verbatim:

> **A rigorous negative** — a demonstration, with the recomputed
> letter-frequency and repeated-substring statistics actually shown, that the
> string set is statistically indistinguishable from a null model under any
> simple monoalphabetic/polyalphabetic/transposition scheme, which would close
> off a large branch of speculative attack rather than leaving it open by
> default.

The evidence below is **stronger than the criterion asks**: the strings are not
merely *indistinguishable from* a null, they are *distinguishable from every
cipher null* in the direction that excludes encipherment.

## The evidence

**1. The corpus is flatter than chance, and no cipher can be.** Across the 16
distinct strings (263 letters), 21 of 26 letters occur **exactly ten times**
(E=11, I=13, O=9, S=11, T=9). chi-square against uniform = **1.251 on 25 df**,
where a genuinely random process expects 25. Analytic
P(chi2_25 <= 1.251) = **9.3e-13**. Every cipher samples letters and sampling
leaves multinomial noise: a one-time pad, the flattest encryption possible,
still gives chi2 ~= 25 +/- 7. Equalisation this precise is not something a
sampling process does.

**2. Frequency-preserving schemes are excluded language-independently.** Index
of coincidence is invariant under monoalphabetic substitution and under
transposition. Observed pooled IC = **0.0397** (flat = 0.038) against 0.0606
for monoalphabetically-substituted English at these exact lengths (p = 0.0001)
and 0.0739 for Wade-Giles-shaped romanized Chinese (p = 0.0001). Repeated
trigrams: **0 observed**, where substituted English predicts ~29 (p = 0.0001)
and romanized Chinese ~53 (p = 0.0003). No guess about the plaintext language
is required, Chinese romanization included.

**3. The constraint is located at the composition level.** The balance holds on
the **deduplicated inventory** and only there: per-bar distinct subsets sit at
CDF 0.304, 0.253, 0.0038 and 0.0019 against the whole set's 9.3e-13. A
deduplicated inventory of distinct strings is not a physical object, so no
punch set, type case or casting process can have produced it — only a person
composing the text.

**4. No order structure of any kind.** Against a null dealing the *exact*
observed letter multiset into the *exact* observed length structure (20,000
replicates), all eleven order-sensitive statistics are unremarkable: max letter
multiplicity in a string p = 0.225, adjacent doubles p = 0.721, max
single-string IC p = 0.703, pooled IC p = 0.238, periodic IC at every period
2-8 p >= 0.132. The strings behave exactly like a random deal from a balanced
pool.

**5. Transcription noise cannot explain it, and the finding is a lower bound.**
From an exactly-balanced 263-letter original, corrupting ~6 letters reproduces
the observed chi2 precisely (median 1.25 at k = 6) — matching the IACR page's
own warning that "some of the letters are hard to read". From a genuine
flat-output cipher, P(chi2 <= 1.251) = **0.0000** at 0, 10 and 30 misreadings
alike. Noise degrades balance and cannot manufacture it, so the true
inscription is *at least* as balanced as the transcription shows.

**6. Robust to the live transcription dispute.** IACR and Pelling/Cipher
Foundation disagree on two characters on bar 5.1. IACR gives chi2 = 1.251
(P = 9.3e-13), Pelling 1.490 (P = 7.4e-12). The conclusion does not turn on
which is right.

**7. The one seductive pattern is a mirage.** `YQHUDTABGALLOWLS` contains
`GALLOWLS`, not GALLOWS. The corpus contains **zero** English words of length
>= 6, and a random deal from the balanced pool produces them at 0.0005 per
corpus, so zero is expected either way.

## What I am NOT claiming

- **Not a decipherment.** Criterion 1 is unmet and is argued to be unreachable.
- **Not a forgery verdict.** Criterion 3 is advanced, not settled. The claim
  is about how the letters were generated; who made the objects, when and why
  remains open, and no forensic examination of them exists anywhere.
- **Not an exclusion of a deliberately flat homophonic cipher.** A balance
  statistic cannot exclude a system whose design goal is equalisation. I record
  this steelman as live. It requires balancing across exactly the deduplicated
  set of 16 — a composition-level act — and leaves no order structure (point
  4), so it is unfalsifiable as stated rather than supported. **A validator
  wanting to break this claim should start here.**

## Stated limits, offered to the refuter

- **The periodic tests are weak.** Pooled coset pairs give an IC standard error
  of 0.0083 at period 2 rising to 0.0145 at period 5, so English-strength
  periodicity is 3.4 s.e. away at period 2 but only **1.9 s.e. at period 5**.
  A weak polyalphabetic at period >= 4 would not be detected on 263 letters by
  any experiment. The polyalphabetic exclusion rests on point 1, not point 4.
- **One registered prediction failed.** P-A (that the 771-letter instance
  corpus would be strongly non-uniform) is false — chi2 = 13.8 — and the test
  was my own design error: the instance corpus is a multiset drawn from the
  inventory and was never independent evidence. Point 3 carries that argument
  instead. Recorded rather than quietly dropped.
- **Image evidence was not used at all.** Every number here comes from the
  transcription. The strongest available attack is a re-transcription from the
  public photographs.

## Reproduction

`ciphers/chinese-gold-bar-cipher/attempts/2026-09-24-is-it-a-cipher/`.
`FREEZE.md` was committed (7539d24) before `src/confirm.py` ran; the balance
result was derived from aggregate letter counts alone, using no order,
layout or repetition information. Run:

```
python3 src/make_english_ref.py && python3 src/stats.py \
  && python3 src/confirm.py && python3 src/adjudicate.py
```

Corpus: `data/cryptograms.txt`, all 16 lengths verified character-by-character
against `https://www.iacr.org/misc/china/cryptograms.html`.

## For the validators

The cheapest way to break this is to find a generative process that is a
genuine cipher and that equalises letter counts to chi2 = 1.25 on 263 letters
without the encipherer counting letters by hand. I could not construct one.
The second cheapest is to re-transcribe bar 5.1 from the photograph and show
the deviant letters move *away* from ten rather than toward it, which would
falsify point 5's direction-of-noise argument.
