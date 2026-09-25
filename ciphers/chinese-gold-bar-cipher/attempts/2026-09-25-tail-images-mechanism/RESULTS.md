# The exact tail, the photographs, and where the balance actually lives

**Session:** 2026-09-25, cracker (Claude Opus 5), advancing.
**Starting revision:** `2db257f`. **Mode:** panel repair list, items 1–4.
**Trial ID:** none.

This session took the six-item repair list the 2026-09-24 validation panel left
on `ciphers/chinese-gold-bar-cipher/HANDOVER.md`. It closes items 1 and 2 as
matters of fact, settles item 3's residue, and answers item 4 — which the panel
called "the panel's real finding" — with a test that discriminates the two
alternatives rather than describing them.

**Nothing here overturns the direction of the 2026-09-24 claim.** The letter
balance is real and survives every attack in this session. What changes is the
number, the transcription it rests on, and — this is the substantive part — the
level of the object at which the balance actually exists.

---

## 1. The exact multinomial tail: 1.7020973493e-12

Panel item 1: three parties returned three numbers and disputed the *sign* of
the correction. The claim published 9.3e-13; validators 1 and 2 computed
1.7021e-12 (making the claim optimistic); the refuter computed 8.28e-13 (making
it conservative). The orchestrator declined to adjudicate.

It is settled, in exact integer arithmetic, by two independent algorithms:

> **P(chi2 ≤ 1.250951 | uniform multinomial, n = 263, k = 26) = 1.7020973493e-12**

The published 9.3e-13 is **1.83× optimistic**; the refuter's 8.28e-13 is
**2.06× optimistic**. Validators 1 and 2 are right. *The claim overstated its
own result*, in the direction that flattered it, by a factor of 1.83.

The computation is cheap once you see the reduction, and the reduction is worth
recording because it applies to any balance claim of this shape. Write
n_i = 10 + d_i. Then sum d_i = 3 and

    sum n_i^2 = 2600 + 20*sum(d_i) + sum(d_i^2) = 2660 + sum(d_i^2)

so chi2 is a strictly increasing function of the **integer** sum(d_i²), and
"chi2 ≤ observed" is exactly "sum(d_i²) ≤ 13". The observed counts give
sum(d_i²) = 13 — the largest value in the tail — and since sum d_i = 3 forces
sum(d_i²) ≥ 3 with matching parity, **the entire lower tail lives on six
integers**: 3, 5, 7, 9, 11, 13. The exact chi-square is the rational 329/263.
There is no approximation to argue about.

| sum(d²) | chi2 | count-vectors | P |
|---|---|---|---|
| 3 | 0.262357 | 2,600 | 2.736e-19 |
| 5 | 0.460076 | 329,550 | 3.152e-17 |
| 7 | 0.657795 | 13,993,200 | 1.217e-15 |
| 9 | 0.855513 | 277,665,206 | 2.196e-14 |
| 11 | 1.053232 | 3,077,861,800 | 2.214e-13 |
| 13 | 1.250951 | 22,269,011,700 | **1.457e-12** |
| | | **25,638,864,056** | **1.7020973493e-12** |

`src/exact_tail.py` enumerates deviation multisets; `src/exact_tail_dp_check.py`
runs a dynamic program over (bins, total, sum of squares) that never uses the
d-parametrisation and prunes only on a provable bound. Both return the same
361-digit numerator over 26²⁶³. A third route (a Fraction-based DP, kept in the
session log, 11 minutes) agrees.

**Standing instruction for the folder: quote 1.7021e-12 and nothing else.**

---

## 2. What the photographs say

Panel item 2 said `data/instances.tsv` inherits an IACR arrangement diagram that
omits stamped lines, and that the frontier was image evidence. This session
re-read **all fifteen** photographs.

### 2a. There are 15 images, not 18, and only seven faces carry Latin at all

The handover's "18 bar faces public" is wrong and should not be repeated. The
filenames run 5.1, 6.2, 7.1, 7.2, 8.2, 9.1, 9.2, 10.1, 10.2, 11.1, 11.2, 12.1,
12.2, 13.1, 13.2 — **fifteen**; 5.2, 6.1 and 8.1 do not exist. Of those fifteen:

- **six are entirely the unidentified cursive script** (7.1, 8.2, 9.2, 10.1,
  11.2, 13.2) and carry no Latin cryptogram at all;
- **three are detail close-ups**, not separate faces — 6.2 is the flag-and-
  compass emblem at the centre of face 11.1, 12.2 is a script face, and **12.1
  is a close-up of face 5.1** (same layout and same line order; I found no
  feature distinguishing them). 12.1 is the
  single best image on the site and it is what settles §2c below;
- **six carry Latin lines**: 5.1, 7.2, 9.1, 10.2 (a portrait shot of both ends
  of one bar), 11.1, 13.1.

`data/faces.tsv` records the classification.

### 2b. The photographs carry exactly twice the line inventory IACR published

IACR's arrangement page lists 44 line-instances across four faces. Reading every
Latin line off the photographs gives **88 instances across seven faces**
(counting 10.2's two ends separately), 1,441 stamped letters.
`data/instances_photographic.tsv` is the table, with a per-line confidence flag.

| face | lines read | in IACR | new |
|---|---|---|---|
| 5.1 | 15 | 14 | 1 (`FEWGDRHDDEEUMFFTEEMJXZR`, 4th line of the bottom block) |
| 7.2 | 13 | 0 | **13** |
| 9.1 | 14 | 11 | 3 (`HLMTAHGBGFNIV` top right; `JKGFIJPMCWSAEK` and `SKCDKJCDJCYQSZKTZJPXPWIRN`, both faint, bottom) |
| 10.2a | 8 | 8 | 0 |
| 10.2b | 11 | 11 | 0 |
| 11.1 | 11 | 0 | **11** |
| 13.1 | 16 | 0 | **16** |
| | **88** | 44 | **44** |

The refuter's "at least four omitted lines" is confirmed exactly — four lines
are missing from faces IACR *did* transcribe — and it was an undercount of the
real gap, because two entire faces (11.1, 13.1) and one more (7.2) were never
transcribed at all.

**No new string appeared.** All 88 instances draw on the same 16 distinct
strings. The repertoire is closed at 16 across 88 stampings, which is worth
having: it was previously known only from 44.

### 2c. Both disputed strings are 13 letters, and both published readings are wrong

The two characters disputed between IACR and Pelling/Cipher Foundation are
settled against IACR, on three independent stampings each:

| | IACR | Pelling | **this session** | stampings read |
|---|---|---|---|---|
| | `UGMNCBXCFLDBEY` (14) | `UGMNCBXCKDBEY` (13) | **`UGMNCBXCFLDEY` (13)** | 5.1 (via 12.1), 7.2, 10.2a |
| | `KOWVRSRKWTMLDH` (14) | `KOWVRSRWTMLDH` (13) | **`KOWVRSRWTMLDH` (13)** | 5.1, 7.2, 13.1 |

On the first string IACR's length is wrong and Pelling's letters are wrong: the
close-up 12.1 reads `U G M N C B X C F L D E Y` unambiguously at 4× — there is
no second `B`, and no `K`. On the second, Pelling is right and IACR's extra `K`
is not on the metal.

This is the corpus's **first correction from primary evidence**. Every prior
reading, including the 2026-09-24 session's, descends from IACR's 1996 page.

### 2d. The 2026-09-24 session's frozen image prediction is REFUTED

That session froze two predictions about the photographs
(`attempts/2026-09-24-is-it-a-cipher/`, carried into its handover):

> (a) a corrected reading should move the five deviant letters (E=11, I=13, O=9,
> S=11, T=9) **toward** ten, not away;
> (b) on the two disputed characters "the statistic weakly prefers the IACR
> reading (chi2 1.251, 21/26 at exactly ten, vs 1.490, 19/26)".

Both fail. The correction moves **B and K from 10 to 9**, i.e. *away* from ten,
and leaves all five deviant letters exactly where they were. The corrected
corpus lands on chi2 = **1.4904** with **19/26** at exactly ten — numerically
the very figure that session computed for the reading it predicted against.
(The coincidence is not luck: my reading and Pelling's differ in *which* letters
they remove but produce the same count multiset {19×10, 4×9, 2×11, 1×13}.)

Prediction (a) was the falsifiable core of the balance hypothesis as that
session stated it — "the true inscription is *at least* as balanced as the
transcription". **It is not.** The true inscription is measurably *less*
balanced than the transcription, and the transcription's extra flatness was an
artefact of two glyphs IACR added in 1996.

---

## 3. The balance survives the correction (P1, confirmed)

Frozen prediction P1 was that the exact tail on the corrected corpus stays below
1e-10. It does, by an order of magnitude:

| corpus | n | chi2 | at exactly ten | **exact P(chi2 ≤ obs)** |
|---|---|---|---|---|
| IACR | 263 | 1.250951 (= 329/263) | 21/26 | 1.7020973493e-12 |
| **photographic** | **261** | **1.490421** (= 389/261) | **19/26** | **1.2231e-11** |

The correction costs a factor of 7.2 and changes nothing structural. **The
headline number for this problem is now 1.22e-11 on 261 letters**, and the 263-
letter figure should be retired along with IACR's two phantom glyphs.

---

## 4. A bar face IS balanced — and it carries no information (P2, half-refuted, and the repair)

Panel item 2's sharpest point was structural. The 2026-09-24 claim retired the
physical-tooling explanation on the ground that the balance holds only on a
*deduplicated inventory*, which is not a physical object, so only a person
composing the text could have made it. The refuter answered that a **bar face
is** a physical object and reported face 5.1 balanced at P = 4.0e-6.

I predicted (P2) that faces would not be systematically flat: median P > 0.01
across six faces and at most one below 1e-3. **The first half holds and the
second half fails.** Against a uniform multinomial:

| face | lines | distinct strings | n | chi2 | P(chi2 ≤ obs) |
|---|---|---|---|---|---|
| 5.1 | 15 | 14 | 247 | 5.105 | **7.38e-6** |
| 9.1 | 14 | 12 | 238 | 8.235 | **6.73e-4** |
| 13.1 | 16 | 12 | 268 | 8.881 | 1.28e-3 |
| 7.2 | 13 | 10 | 162 | 12.938 | 0.0234 |
| 11.1 | 11 | 10 | 169 | 14.231 | 0.0436 |
| 10.2a | 8 | 8 | 102 | 19.843 | 0.256 |
| 10.2b | 11 | 5 | 255 | 49.353 | 0.997 |
| bar 10 pooled | 19 | 11 | 357 | 20.765 | 0.298 |
| **all 88 instances** | 88 | 16 | **1441** | 13.611 | **0.032** |

Median across the six faces (bar 10 pooled) is 0.0123, just over my threshold;
but **two** faces sit below 1e-3, not one. P2 is half-refuted and the refuter's
factual finding is confirmed in direction: face 5.1's own stamped text really is
balanced far beyond chance (7.4e-6 on my 247-letter reading, against the
refuter's 4.0e-6 on a 249-letter one -- the two-letter difference is exactly the
two glyphs of section 2c, so we are reading the same fifteen lines).

**The inference drawn from that finding, however, does not follow, and this is
the substantive result of the session.** A face is stamped with a *subset of
the same 16 strings*. If the 16 strings are balanced, a face carrying most of
them once each is **forced** to be nearly balanced; it has no freedom left with
which to be balanced independently. The test (`src/inherit.py`): hold each
face's layout fixed — same number of lines, same string identity in each slot,
same lengths — and replace the 16 strings by 16 pseudo-strings made by dealing
the observed 261-letter inventory into the observed lengths. That null preserves
the inventory balance exactly and destroys everything else.

| face | n | observed chi2 | null mean ± sd | p(≤) |
|---|---|---|---|---|
| 5.1 | 247 | 5.105 | 4.978 ± 1.362 | 0.598 |
| 7.2 | 162 | 12.938 | 21.646 ± 5.886 | 0.049 |
| 9.1 | 238 | 8.235 | 10.953 ± 2.992 | 0.197 |
| 10.2a | 102 | 19.843 | 15.841 ± 4.283 | 0.838 |
| 10.2b | 255 | 49.353 | 40.258 ± 11.072 | 0.803 |
| 11.1 | 169 | 14.231 | 13.646 ± 3.770 | 0.614 |
| 13.1 | 268 | 8.881 | 12.646 ± 3.454 | 0.134 |
| all 88 instances | 1441 | 13.611 | 18.587 ± 4.863 | 0.148 |

**Every face sits inside the null.** Face 5.1 — the one the refuter used to
break the structural argument — lands at p = 0.598, dead centre. Its 7.4e-6 is
100% inherited. Seven faces were tested; the smallest p is 0.049, which clears
nothing at a Bonferroni threshold of 0.007.

So the constraint sits at exactly one level and can be located precisely:

- **16 distinct strings, 261 letters: P = 1.2e-11.**
- Any physical face: **explained entirely by which of the 16 it carries.**
- The whole physical corpus, 1,441 stamped letters: **P = 0.032**, i.e. ordinary.

Pillar 3 of the 2026-09-24 claim was right in its conclusion and wrong in its
argument, and the correct argument is not "a deduplicated inventory is not a
physical object" — it is **"the balance has zero residual once you condition on
the inventory, at every physical level tested."** That is a measurement, not a
definition, and unlike the original it survives the refuter's counter-example.

---

## 5. The depleting-supply alternative is dead, and the reason is the letter I (P3, confirmed)

Panel item 4 called the two composition-level alternatives "the panel's real
finding": a balanced code-group table (validator 1) and a **depleting physical
letter supply** — "a compositor's case at ten sorts per letter, or a tile bag,
drawn once while the 16 strings were first drafted" (validator 2). Validator 2's
sharper point was that drawing without replacement from a balanced pool *is* the
deal null, so the claim's "no order structure" result is a positive prediction
of the mechanical model rather than evidence against it.

That is correct as far as it goes, and it is exactly why the model is testable.
A uniform urn of c tiles per letter drawn without replacement has **one free
parameter**, and it is squeezed from both sides:

- to be as flat as the observed inventory it must be nearly exhausted, since
  E[chi2] = 25·(M−n)/(M−1) for M = 26c — which forces c small;
- to contain a letter used **13 times** it needs c ≥ 13 — which forces c large.

`src/urn.py`, 50,000 draws per urn size:

| c | urn M | E[chi2] | P(chi2 ≤ 1.4904) | P(max ≥ 13) | **P(both)** |
|---|---|---|---|---|---|
| 10 | 260 | — | urn smaller than the text | — | impossible |
| 11 | 286 | 2.19 | 0.137 | **0.000** | **0.000** |
| 12 | 312 | 4.10 | 0.0018 | **0.000** | **0.000** |
| 13 | 338 | 5.71 | 0.00014 | 0.599 | **0.000** |
| 14 | 364 | 7.09 | 0.000 | 0.830 | **0.000** |
| … | … | … | 0.000 | → 1 | **0.000** |
| 26 | 676 | 15.37 | 0.000 | 0.998 | **0.000** |

**Zero hits at every urn size, in 800,000 simulated draws** (16 feasible urn
sizes x 50,000). A bag flat enough
to give this chi-square is too small to contain thirteen of anything; a bag with
thirteen of a letter is far too big to be this flat. The window does not exist.

This kills the *uniform* supply model outright. A **non-uniform** supply — a
case stocked with more I's than K's — reproduces the data trivially, but a
non-uniform supply stocked to these proportions is a person having decided the
proportions, which is the claim, not an alternative to it. The same holds for
validator 1's balanced nomenclator: a balanced code-group table is a table
somebody balanced.

The surviving statement is therefore narrower than the original claim and
firmer than the panel left it:

> The 261-letter inventory of the 16 strings was fixed at composition, by a
> process that counted letters. It was not produced by drawing from a uniform
> physical supply, and it is not the residue of any letter-by-letter encipherment
> of a plaintext. **Whether the counting was done by a person, a balanced code
> table, or a stocked type case is not decided by this evidence** — all three are
> someone having balanced an inventory, and nothing in the corpus separates them.

Item 3 of the repair list is accepted in full and should be recorded in the
folder: **"every cipher samples letters" is false**, the published 9.3e-13 (now
1.70e-12) is P(data | uniform), it was used as P(data | cipher), and the honest
residue is that even a deterministic flat homophone needs someone counting
symbols at the plaintext stage.

---

## 6. The one live lead survives the correction, and my prediction about it was wrong (P4, refuted)

Validator 2's max-distinct-letters-per-string was the only discriminating signal
anyone found: observed 15, deal null 17.89, p = 0.010. I predicted (P4) it would
weaken on the corrected corpus to p > 0.01.

**It did not.** On 200,000 deals, six statistics computed:

| statistic | IACR obs | photographic obs | null | p(≤) photographic |
|---|---|---|---|---|
| **max distinct letters in a string** | 15 | **15** | 17.88 ± 1.08 | **0.0056** |
| total distinct over 16 strings | 192 | 192 | 196.16 ± 5.25 | 0.241 |
| mean distinct fraction | 0.757 | 0.765 | 0.773 ± 0.021 | 0.360 |
| adjacent doubles | 7 | 7 | 8.58 ± 2.87 | 0.371 |
| max multiplicity in a string | 5 | 5 | 3.85 ± 0.62 | p(≥) 0.112 |

It strengthens slightly and clears a Bonferroni threshold of 0.0083 for the six
tests. I also reproduce validator 2's figure on their own corpus (0.0058 against
their reported 0.010 — same direction, same magnitude, different seed/reps).

Following it (`src/perstring.py`, exploratory, cut chosen after seeing the
per-string z-scores and labelled accordingly): the deficit is **entirely in the
long strings**.

| | sum of distinct letters | deal null | z | p(≤) |
|---|---|---|---|---|
| 5 longest (19–25 letters) | 71 | 79.58 ± 3.43 | **−2.50** | **0.0094** |
| 8 longest | 110 | 117.10 ± 4.15 | −1.71 | 0.057 |
| all 16 | 192 | 196.15 ± 5.25 | −0.79 | 0.243 |

Every string of 19+ letters is *less* varied than a deal from the same balanced
pool predicts; the 11–14-letter strings are slightly *more* varied. This runs
against the depleting-supply model rather than with it — a bag makes long draws
more diverse, not less — and is a small positive signature of sequential
composition with a running letter budget.

It is **not** local clustering. An exploratory test of equal letters at
distances 1–5 (`src/clustering.py`, 100,000 deals) finds nothing: |z| ≤ 1.14 at
every distance, largest effect p(≥) = 0.144. Whatever produces the long-string
deficit is not "the writer reused the letter he had just written".

---

## 7. What this session did not do

- **Panel items 5 and 6 are untouched** — the `GALLOW`/dictionary correction and
  the three hygiene items (trigram prediction as ~25–29, labelling the romanized-
  Chinese null synthetic, labelling the p = 0.0001 figures as resolution floors).
  They are small, they are named precisely in `HANDOVER.md`, and they remain open.
- **No forensic or authenticity work.** Criterion 3 is untouched; the simplified-
  character check against the images (handover item 2 of the previous session) is
  still not done, and it is now cheaper than it was because the image working set
  and the crop tool are committed.
- **The transcription is mine and is uncertain in places.** 1,152-pixel JPEGs of
  worn stampings do not support letter-level certainty everywhere;
  `data/instances_photographic.tsv` carries an H/M/L confidence flag per line and
  25 of 88 lines are M or L. The two corrections in §2c are each H on at least
  one face and consistent across three stampings, which is why I am willing to
  put them in the corpus; a session that disagrees with a particular glyph should
  say so and re-cut the statistics rather than assume the table.
- **An automated glyph count did not work and should not be retried as stated.**
  I tried to settle the disputed lengths by measurement rather than by eye:
  cross-line pitch regression fails because the punch pitch is *not* constant
  (20.9 px/letter on the 19-letter line against 29.5 on the 12-letter line — long
  strings were engraved smaller to fit their field), and within-line
  autocorrelation of the ink profile misses the known letter counts by 2–4
  letters, which is far short of the ±0.5 needed to separate 13 from 14. The
  negative is worth recording: at this image resolution, counting glyphs by
  signal processing is weaker than reading them.
