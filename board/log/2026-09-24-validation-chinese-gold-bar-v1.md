# Validation — Chinese gold bar cryptograms (Validator 1)

**claim:** The 16 gold-bar cryptograms are not ciphertext at all. They were composed
under a deliberate letter-balance constraint (21 of 26 letters appear exactly ten
times across the 263-letter deduplicated inventory; chi-square vs uniform = 1.251 on
25 df; analytic P(chi2_25 <= 1.251) = 9.3e-13), which no sampling-based cipher can
produce. Offered against success criterion 2.

**problem:** `chinese-gold-bar-cipher`

**criteria applied:** `PROBLEM.md`, success criterion 2, verbatim:

> **A rigorous negative** — a demonstration, with the recomputed letter-frequency and
> repeated-substring statistics actually shown, that the string set is statistically
> indistinguishable from a null model under any simple monoalphabetic/polyalphabetic/
> transposition scheme, which would close off a large branch of speculative attack
> rather than leaving it open by default.

Criteria 1 and 3 are also quoted and addressed under *reasoning* below.

**validator role:** 1

---

## reproduced: yes — with one arithmetic correction of my own

I re-derived the corpus from the primary page and rebuilt every headline number with
my own code before running the claimant's. Then I ran the claimant's pipeline in a
scratch copy. Nothing under `ciphers/` was modified.

### 1. Corpus re-derived from the primary source — exact match

Fetched `https://www.iacr.org/misc/china/cryptograms.html` myself (HTTP 200, 5123
bytes). Parsed the canonical `<pre>` block (the one containing `length 25`) with my own
regex, independently of `data/cryptograms.txt`.

- 16 distinct strings recovered. Every string's actual length matches the length the
  page itself states (25, 24, 24, 23, 20, 19, 16, 14, 14, 14, 14, 13, 12, 12, 11, 8).
  **Zero stated-vs-actual mismatches.**
- **Diff against the claimant's `data/cryptograms.txt`: identical, character for
  character, in the same file order, on all 16 strings. No discrepancy of any kind.**
- Cross-check the claimant did not report: I also extracted every string from the three
  *arrangement* blocks higher up the page. The set of strings appearing there is exactly
  the canonical 16 — nothing in the arrangements is missing from the list, nothing in the
  list is absent from the arrangements.
- I independently rebuilt `data/instances.tsv` from the arrangement blocks: **44 stamped
  lines, 771 letters**, and the per-bar partition (10.2a=8, 10.2b=11, 9.1=11, 5.1=14) and
  the full (bar, string) multiset are **identical** to the claimant's file. Instance
  chi-square 13.822 — identical to theirs.

The page is reachable and the corpus is faithful. No limitation on this front.

### 2. My own statistics — all reproduce, and I found the exact tail

Total letters **N = 263**. My counts:

```
A10 B10 C10 D10 E11 F10 G10 H10 I13 J10 K10 L10 M10 N10
O9  P10 Q10 R10 S11 T9  U10 V10 W10 X10 Y10 Z10
```

- **21 of 26 letters at exactly ten** — confirmed (ABCDFGHJKLMNPQRUVWXYZ). Deviants
  E=11, I=13, O=9, S=11, T=9. No letter absent; all 26 used.
- chi-square vs uniform, as an exact fraction: **329/263 = 1.2509506**. Confirmed.
- **df = 25 is correct.** A multinomial goodness-of-fit over 26 categories with N fixed
  has 26 − 1 = 25 df. I checked the neighbouring errors: df=24 would give 4.21e-12 and
  df=26 would give 2.02e-13, neither of which is the stated figure, so the claimant used
  the right df and did not fudge it.
- I reimplemented the regularized lower incomplete gamma from scratch and get
  **P(chi2_25 <= 1.250951) = 9.2979e-13**, matching the claimed 9.3e-13. The claimant's
  `gammainc_lower_reg` in `src/confirm.py` is a correct series implementation.

**My correction.** The 9.3e-13 figure is the *asymptotic* chi-square CDF, but the null
here is multinomial and discrete, and this is an extreme lower tail where the asymptotic
approximation is not tight. Because N = 263 = 26·10 + 3, the statistic collapses to a
clean closed form: with d_i = c_i − 10 and Q = sum d_i², chi2 = (26Q − 9)/263. So
`{chi2 <= 1.251}` *is exactly* the event `{Q <= 13}`, and the exact multinomial
probability is computable. I computed it **two independent ways** — a DP over
(sum d, sum d²) and a combinatorial enumeration over deviation multisets — validating the
enumerator against brute force on N=8/K=4 (9 cutoffs, all exact) and against total mass
= 1 on N=30/K=6. Both agree:

| quantity | IACR reading (N=263) | Pelling reading (N=261) |
|---|---|---|
| chi2 (exact fraction) | 329/263 = 1.250951 | 389/261 = 1.490421 |
| asymptotic chi2_25 CDF | 9.2979e-13 | 7.4349e-12 |
| **exact multinomial tail** | **1.7021e-12** | **1.2231e-11** |

**The claim's headline probability is ~1.83x too small — i.e. it overstates the
extremeness, in the direction that favours the claim.** It should read 1.7e-12, not
9.3e-13. This is a real defect in the stated number and should be corrected in the
writeup, but it is immaterial to every conclusion: 1.7e-12 excludes a sampling cipher
exactly as decisively as 9.3e-13 does.

Two related exactness facts worth recording, neither of which the attempt states:
chi2 is *lattice-valued* here (only (26Q−9)/263 for integer Q is attainable), and the
minimum attainable value is 69/263 = 0.2624. The observed 1.2510 is the **sixth** most
balanced configuration reachable, not the floor — five strictly more balanced
arrangements exist. That is consistent with, and mildly supportive of, the attempt's
point 5 (a near-perfect original degraded by a few misreadings).

Other statistics I recomputed independently: pooled within-string IC = **0.039683**
(flat 1/26 = 0.038462); **zero** repeated trigrams across the 16 distinct strings.

### 3. The claimant's pipeline — runs clean and agrees

Copied the whole attempt directory to my scratch dir and ran it there. One wrinkle
worth flagging for reproducibility: both `make_english_ref.py` and the P-D test in
`confirm.py` reach four/five levels up out of the attempt directory into
`historical-controversies/junius-letters-authorship/.../gutenberg_2173.txt`. A naive
copy of the attempt folder alone **will not run**. I rebuilt a repo-depth mirror and
symlinked that tree. I also deleted the committed `out/*.json` and
`data/english_reference.txt` first so everything regenerated from scratch.

All four scripts ran. Every number I was asked to check reproduces:

- `stats.py`: observed chi2 = **1.25095**, IC = **0.03968**, rep3 = **0**, rep4 = **0**.
  Uniform-random null: chi2 mean **24.89**, sd **7.04** — this is the claim's
  "25 +/- 7" and it is right (Var(chi2_25) = 50, sd = 7.07). MASC English IC
  **0.0606** (p = 0.0001), MASC romanized-Chinese IC **0.0739** (p = 0.0001), rep3
  **28.77** and **53.38** respectively (p = 0.0001). All as claimed.
- `confirm.py`: P-B bar CDFs **0.3041, 0.2532, 0.0038, 0.0019** — matches the claim's
  "0.304, 0.253, 0.0038, 0.0019" exactly. P-C: all eleven order statistics inside the
  deal null — max multiplicity p = 0.2252, doubles p = 0.7212, max single-string IC
  p = 0.7034, pooled IC p = 0.2378, periodic IC periods 2–8 p >= 0.1322. P-D: zero
  English substrings of length >= 6, null mean 0.0005. P-E: from an exactly-balanced
  original, median chi2 = **1.25 at k = 6** misreadings; from a uniform-random cipher
  origin, P(chi2 <= 1.251) = **0.0000** at k = 0, 10 and 30.
- **The disclosed failure reproduces too:** P-A FAILED, instance chi2 = **13.822**
  (claim says 13.8). The claimant registered this prediction, it came out false, and
  they reported it as false rather than dropping it. I independently derived the same
  13.822 from the page. This is the single strongest indicator of good faith in the
  attempt.
- `adjudicate.py`: IACR chi2 = 1.251 (21/26 at ten); Pelling chi2 = 1.490, N = **261**,
  19/26 at ten.

### 4. The Pelling variant is real — independently confirmed

The claim's point 6 depends on a second transcription that the attempt hard-codes rather
than fetching. I checked it against the source. `ciphermysteries.com` yields
**`UGMNCBXCKDBEY`** and **`KOWVRSRWTMLDH`** — precisely the two variant readings coded in
`adjudicate.py`, against IACR's `UGMNCBXCFLDBEY` and `KOWVRSRKWTMLDH`. The remaining
strings match IACR. So point 6 is faithful to a real competing source, not invented.
Note the variant drops two characters, so N = 261, not 263 — this is why chi2 = 1.490 is
attainable (it corresponds to Q = 15; at N = 263 no integer Q yields 1.490). The
claimant's arithmetic is internally consistent. `cipherfoundation.org` returned HTTP 200
but no transcription content I could extract.

### 5. The pre-registration is real

```
7539d24  2026-09-24 00:40:55 +0000  gold bars: freeze predictions before confirming tests
832a4ef  2026-09-24 00:52:11 +0000  gold bars: the cryptograms are not ciphertext — solve-claim
```

- `7539d24` is a verified **ancestor** of `832a4ef` (`git merge-base --is-ancestor`).
- The freeze commit tree contains `FREEZE.md`, `data/cryptograms.txt`,
  `data/english_reference.txt`, `out/stats.json`, `src/make_english_ref.py`,
  `src/stats.py` — and **`src/confirm.py` is absent from it**
  (`git cat-file -e` fails: "exists on disk, but not in '7539d24'").
  `src/confirm.py`, `src/adjudicate.py`, `out/confirm.json`, `data/instances.tsv` and
  `RESULTS.md` all first appear in `832a4ef`, 11 minutes later.
- So P-A..P-E were committed before the code that tests them existed. **The
  pre-registration claim is structurally true.** Caveat for the record: both commits come
  from the same session, so the *ordering* is verifiable but the *honesty* of the freeze
  is not independently attested. The fact that P-A was registered and then failed, and
  the failure was published, is the best available evidence that the freeze was genuine.
  Note also that `stats.py`/`stats.json` were in the freeze commit, so the pre-freeze
  derivation included IC and trigram results, not only aggregate counts — consistent with
  what `FREEZE.md` itself states, and disclosed there.

---

## verdict: PARTIAL

Criterion 2 is substantially met. Criteria 1 and 3 are unmet. Criterion 2 alone is not a
solve of this problem.

---

## reasoning

### Does the claim satisfy criterion 2 as written?

The claim asserts it is "stronger than the criterion asks" — distinguishable rather than
indistinguishable. I do not accept that framing at face value, because criterion 2 names
a specific null ("a null model under any simple monoalphabetic/polyalphabetic/
transposition scheme") and states its purpose ("close off a large branch of speculative
attack"). Applying it as written rather than as the claim reframes it:

**What the criterion literally asks for, item by item:**

1. *"the recomputed letter-frequency ... statistics actually shown"* — **met.** Full
   per-letter counts, chi2, exact null distributions, shown and reproducible.
2. *"repeated-substring statistics actually shown"* — **met.** rep3 = 0, rep4 = 0,
   against four explicit nulls.
3. *"statistically indistinguishable from a null model"* — **met, on the reading the
   purpose clause forces.** The relevant null for closing the branch is a no-message
   null, and the corpus is indistinguishable from it on every structural statistic:
   IC p = 0.77, rep3 p = 0.46, rep4 p = 1.00 against uniform-random; and all eleven
   order-sensitive statistics p >= 0.13 against a null dealing the exact observed
   multiset into the exact observed length structure. The corpus departs from the
   uniform null in exactly *one* place — the letter-count balance — and in the
   direction of too-even, which argues against sampling rather than for a message.
   So "indistinguishable from a null" is in fact established; the extra balance finding
   sits on top of it.
4. *"under any simple monoalphabetic ... scheme"* — **met**, and correctly reasoned in
   `RESULTS.md`: IC is invariant under monoalphabetic substitution, observed 0.0397
   against 0.0606 for substituted English at these exact lengths (p = 0.0001) and
   0.0739 for Wade-Giles-shaped romanized Chinese (p = 0.0001), plus 0 repeated
   trigrams where English predicts ~29. Language-independent, Chinese romanization
   included. This is the strongest part of the work.
5. *"... transposition scheme"* — **met**, same argument, same invariance.
6. *"... polyalphabetic ..."* — **only partially met, and this is the real gap.** The
   claimant concedes it in their own stated limits: the periodic IC tests have almost no
   power, with English-strength periodicity only **1.9 s.e.** away at period 5 (694 coset
   pairs, s.e. 0.0145). I reproduced that power table. Their fallback is that
   polyalphabetic exclusion "rests on point 1, not point 4" — i.e. on the balance. That
   fallback is sound for this class: a Vigenère or a one-time pad flattens frequencies
   but still *samples*, so its chi2 is distributed about 25 with sd 7, and hitting
   <= 1.251 has exact probability 1.7e-12. So polyalphabetic *is* excluded — but by
   the balance argument, not by a direct test, and therefore only for schemes that
   sample. It is not excluded for a scheme designed to equalize output.

**A logical error in the writeup that the underlying work does not share.** The claim's
point 1 states: "Every cipher samples letters and sampling leaves multinomial noise."
That is false for two of the three schemes criterion 2 names. I verified computationally
that chi2-vs-uniform is a symmetric function of the count vector and is therefore
*exactly* invariant under monoalphabetic substitution (200 random substitutions: chi2 =
1.25095057 every time) and under transposition (200 random anagrams: identical). Both
are deterministic bijections on letters; neither samples. A *balanced plaintext* put
through either yields chi2 = 1.2510 with probability 1. So the balance statistic alone
cannot exclude mono-substitution or transposition — it only pushes the question back to
whether the plaintext was balanced.

To be fair to the claimant: `RESULTS.md` line 31 says explicitly "transposition
preserves letter frequencies exactly" and its exclusion table correctly assigns
mono/transposition to IC, not to chi2. So this is an **overstatement in the solve-claim
writeup, not an error in the analysis** — and it is exactly the kind of thing that only
shows up if you reproduce rather than read. The conclusion survives intact via IC.

**Decision on criterion 2: satisfied in substance, not "exceeded."** The claim does
close off the branch criterion 2 was written to close, and it shows the required
statistics. But the framing "stronger than the criterion asks" is not right: the balance
finding is a *different* result that happens to be striking, and it does less work
against mono/transposition than the claim implies, while the polyalphabetic closure
rests on an assumption (that the cipher samples) rather than on a powered test. It
neither cleanly exceeds nor cleanly sidesteps the criterion — it meets it by a different
route than the criterion anticipated, with one genuine residual gap.

### Criteria 1 and 3 are unmet — stated plainly

**Criterion 1** asks for "a checkable plaintext for one or more of the 16 cryptogram
strings," where checkable means "the recovered meaning predicts something independently
present elsewhere on the same bar or certificate in cleartext." **Unmet, and not
attempted.** The claim concedes this and argues it is unreachable. Correctly, it also
dismantles the one public decipherment claim (Milton Kim): I reproduced that the implied
mapping is not a function — D → {B,G,P}, E → {A,E,L,N,U}, F → {G,O,T}, M → {C,E},
R → {G,O}, at least 10 free choices beyond a substitution alphabet.

**Criterion 3** asks for "a sourced, dated authenticity argument (iconographic/rank/
insignia dating, or provenance-chain reconstruction)." **Unmet.** No iconography was
examined, no rank or insignia dated, no provenance chain reconstructed, and the attempt
states outright that image evidence was not used at all. `RESULTS.md` calls criterion 3
"materially advanced" on the grounds that balanced gibberish presented as enciphered
financial text is itself an act of fabrication. That inference is reasonable but it is
not what criterion 3 asks for: it is neither sourced nor dated, and it supplies no
terminus for when the objects were made. Criterion 3 should be recorded as untouched,
not as advanced.

### Is criterion 2 alone a solve?

No. `PROBLEM.md` sets out three criteria with no statement that any one suffices, and it
frames the named unknown as "what do the Latin-letter cryptograms actually encode?"
alongside a second, explicitly "separable but connected" authenticity question. The claim
answers the first as "nothing" — which is a legitimate answer to the named unknown, and a
genuinely valuable one, since it closes a branch that has absorbed a decade of attention.
But one of three criteria, met by a different route than intended and with a conceded
power gap, is a strong advance and not a solve. It should stand on the board as a
rigorous negative result on criterion 2, held for human sign-off, and the problem should
remain open on criteria 1 and 3.

---

## dissent

I have not seen the other two verdicts. Recording my position in advance so it is not
smoothed over if they land differently:

**If the other two validators return PASS, I dissent.** My objection is not the
arithmetic — which is sound, and which I reproduced to the last digit — but the
inferential step from "the letters were not generated by letter-level encipherment" to
"there is no plaintext to recover."

**My single strongest doubt: the claim does not exclude a balanced code-group table, and
its own point 3 argues *for* that reading as much as against it.** Suppose the 16 strings
are code groups from a nomenclator or codebook — each group standing for a name, a date,
an amount — and the table's designer distributed letters evenly across the table when
building it. Every one of the claim's seven findings follows:

- chi2 = 1.251 on the deduplicated inventory — yes, because the *table* is what was
  balanced.
- Balance appears only on the deduplicated set, not on the 44 stamped instances (P-A
  failed, P-B confirmed) — yes, because a codebook table is precisely a deduplicated
  inventory of distinct groups, stamped repeatedly on the objects.
- No order structure at all (P-C) — yes, because letters *within* a code group carry no
  message; the meaning is at the group level.
- IC at the flat value, zero repeated trigrams — yes, for the same reason.

Point 3 is the claim's argument that the constraint sits "at the composition level" and
that "a deduplicated inventory of distinct strings is not a physical object, so no punch
set, type case or casting process can have produced it — only a person composing the
text." I agree with the premise and it defeats H3. But it does not discriminate the
conclusion, because **a codebook is also not a physical object and is also composed by a
person.** The claim's registered steelman is a "deliberately flat homophonic cipher,"
which is a *letter-level* system; the codebook alternative is group-level and is
nowhere addressed in `FREEZE.md`, `RESULTS.md` or the solve claim. Homophonic
substitution with equalized homophone usage, and nomenclators with code-group tables,
are both historically attested rather than exotic.

What the evidence actually establishes, in my judgement, is the narrower proposition:
**the letters within these strings were not produced by enciphering a message letter by
letter, and the inventory was balanced by hand.** That is a real, well-supported, novel
finding and it is enough for criterion 2. The broader proposition in the claim's first
sentence — "there is no plaintext to recover" — is consistent with the evidence but not
established by it, and it should be softened.

Two lesser objections, recorded:

1. **The 9.3e-13 figure is wrong and should be restated as 1.7e-12** (exact multinomial,
   two independent derivations above). Direction of the error favours the claim. Nothing
   downstream changes.
2. **"Every cipher samples letters" (point 1) is false** for monoalphabetic substitution
   and transposition, both of which leave chi2 exactly invariant. The attempt's own
   `RESULTS.md` gets this right; the solve-claim writeup does not.

Against all of that I want to record what held up, because a refuter's checklist would
have caught it if it had not. The corpus is faithful to the primary source
character-for-character; the instance table is faithful; the pre-registration is real and
verifiable in the commit DAG; the competing Pelling transcription is real and checked;
a registered prediction failed and was published as failed; every null model is explicit
and actually run; and the power limitations are stated by the claimant before a validator
had to find them. This is careful work. My verdict is PARTIAL on the pre-registered
criteria, not a criticism of the research.
