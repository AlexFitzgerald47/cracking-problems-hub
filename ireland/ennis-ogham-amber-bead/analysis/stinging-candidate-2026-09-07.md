# `STINGING` candidate — adversarial analysis

Session: 2026-09-07, GPT-5.6 Sol

## Claim under test

Take only the modern specialist's ordinary-sign right-hand path, `DMVAVA`, with epigraphic `V` occupying the ordinary ogham F/Fern position. Number the twenty ordinary ogham signs in canonical aicme order:

`B L F S N | H D T C Q | M G NG Z R | A O U E I`

Apply one global cyclic displacement of -3 positions to every sign:

| observed | D | M | V/F | A | V/F | A |
|---|---:|---:|---:|---:|---:|---:|
| index | 6 | 10 | 2 | 15 | 2 | 15 |
| index - 3 mod 20 | 3 | 7 | 19 | 12 | 19 | 12 |
| decoded token | S | T | I | NG | I | NG |

Thus `DMVAVA` -> `STINGING` (six ogham tokens, eight Latin letters because NG is one ogham sign).

This is a **solve candidate, not a solve claim**. The object-level success criteria in `PROBLEM.md` still require a physically justified path/direction and an explanation of the anomalous terminal structures/fork.

## Why the hit is worth testing

1. `V` -> the F/Fern position is standard epigraphic practice, not a special concession made for the candidate.
2. The transform was screened over the complete 20 cyclic offsets after fixing `DMVAVA`; `STINGING` was the only ordinary English hit in two independent lexicons.
3. The object was independently documented in 1856 as an inherited amulet used for sore eyes. `STINGING` is therefore semantically relevant to one recorded function of the object.
4. Irish manuscript culture genuinely combines ogham with simple alphabet-substitution ciphers, and an 1849-era manuscript written almost entirely in ogham contains healing charms including charms for weak eyesight / the evil eye. These facts support the *genre class* 'cryptic healing ogham', but do not establish this exact -3 transform.

## Primary Caesar-family null

Represent an English word as six ordinary-ogham tokens using the 20-sign alphabet above. Treat English V as the F/Fern sign and allow both NG-as-one-sign and N+G segmentations where applicable. For each lexicon, collapse six-token words into orbits under all 20 cyclic shifts.

- TextBlob spelling lexicon: 2,875 eligible six-token sequences; 2,874 distinct Caesar orbits. Probability that a uniformly random six-sign ogham sequence has **some** English word in its 20-shift orbit:

  `2,874 / 20^5 = 0.000898125` = **0.0898%**.

- CMUdict: 13,932 eligible six-token sequences; 13,893 distinct Caesar orbits:

  `13,893 / 20^5 = 0.0043415625` = **0.4342%**.

(The denominator is `20^6 / 20 = 20^5` possible cyclic orbits; repeated-period edge cases are automatically handled by canonical-orbit counting in the script.)

For `DMVAVA` itself, the 20 outputs contain exactly one word in each lexicon: `STINGING` at shift -3.

### Multiple structural branches

The first session established at least eight object-level structural cases before assigning values to anomalous marks. A narrower set of four fully specified ordinary-sign core/direction cases is:

- `DMVAVA`
- `DMLOVA`
- opposite-direction values of `DMVAVA` -> `ATATML`
- opposite-direction values of `DMLOVA` -> `ATODML`

Only `DMVAVA` yields an English hit under any cyclic offset.

A conservative union-bound adjustment gives:

| charged branches | TextBlob | CMUdict |
|---:|---:|---:|
| 1 frozen path | 0.0898% | 0.4342% |
| 4 fully specified paths | <=0.359% | <=1.737% |
| 8 lower-bound structural paths | <=0.719% | <=3.473% |

This is suggestive signal, not decisive proof.

## Wider garden-of-forks audit

To test whether `STINGING` is merely what appears when transform choice is broadened after seeing the data, enumerate all invertible affine maps on the twenty-position alphabet:

`y = a*x + b (mod 20)`, with `gcd(a,20)=1`.

There are 160 such maps. `STINGING` remains the **only** English hit for `DMVAVA` in both CMUdict and TextBlob.

However, the appropriate random-sequence false-positive rate rises because the search family is eight times larger:

- TextBlob affine-family reachability: approximately **0.703%**.
- CMUdict affine-family reachability: approximately **3.34%**.

A second robustness family treating ogham as a 4 x 5 aicme grid and allowing group/within-group cyclic shifts and reflections likewise yields only `STINGING` for `DMVAVA`, but its random reachability is ~0.355% (TextBlob) / ~1.68% (CMUdict).

Therefore the candidate is strongest only if the historically motivated search family was the simple cyclic displacement, not 'any convenient permutation'.

## Competitor outputs

For the frozen `DMVAVA` path, all 20 cyclic displacements are:

`dmfafa, tgsoso, cngnunu, qzhehe, mrdidi, gatbtb, ngoclcl, zuqfqf, remsms, aigngn, obnghngh, ulzdzd, efrtrt, isacac, bnoqoq, lhumum, fdegeg, stinging, ncbzbz, hqlrlr`

`STINGING` is the only English hit in either tested lexicon.

The alternative `DMLOVA`, and the physically recomputed opposite-direction paths `ATATML` and `ATODML`, yield no English hit under any of the 20 offsets.

## Evidence against premature acceptance

### 1. Exact key is not yet historically attested

Simple alphabetic +/-1 substitutions are attested in Irish manuscript cryptography, and learned ogham traditions manipulate the canonical 20-sign sequence in many ways. I have **not** yet located an attested source saying 'move every ogham sign three positions in the canonical twenty-letter order'. This is the largest historical weakness.

### 2. English before 1840 is possible but historically atypical

The bead's inscription was drawn by Windele in 1840, so `STINGING` would require an English-language ogham inscription no later than that date. Scholarship on post-medieval ogham distinguishes a mid-nineteenth-century antiquarian phase, typically Modern Irish, from a later revivalist phase where English becomes especially common. An English `STINGING` before 1840 would therefore be unusual, not impossible.

### 3. The physical path is not independently selected yet

The 1840 and 1856 drawings already show the anomalous extra geometry. They do **not** independently give a clean six-sign `DMVAVA`. The final `VA` path is selected from the right-hand branch in the 2023 direct examination. The candidate therefore does not yet have a held-out early-witness replication.

### 4. Semantics explain only one inherited use

`STINGING` fits the sore-eye use well, but the 1856 account also records protection in childbirth. A one-word symptom label does not explain that second use. Amulet functions can accrete over generations, but invoking that here would be an auxiliary assumption.

### 5. Charm comparators are usually fuller formulae

The nineteenth-century Minchin healing-charms manuscript establishes that ogham could encode eye-related healing charms, but its charms are generally prayers/invocations rather than bare symptom words. It supports genre plausibility, not the exact plaintext.

## Current verdict

**PARTIAL / high-value candidate. Do not post a solve claim yet.**

`DMVAVA -> STINGING` is statistically nontrivial under the frozen Caesar-family test and unusually well matched to one independently documented object function. But it currently fails the pre-registered physical criterion: the object evidence does not yet independently force the `DMVAVA` path, and the exact -3 ogham displacement remains unattested.

## Falsifiers / next tests fixed before further searching

The candidate should be killed or sharply downgraded if any of these occurs:

1. high-resolution surface evidence shows the right `VA` branch is secondary/non-inscriptional or not continuous with the main reading path;
2. a blind re-transcription of the 1840/1856 drawing cannot recover the modern sign counts required by `DMVAVA` even allowing drawing error;
3. an audit of learned/cryptic ogham traditions shows that a global +/-3 displacement is structurally alien while another attested map fits the physical signs better;
4. matched-budget nulls over a predeclared broader transform family produce many contextual English competitors;
5. provenance/dating evidence makes an English-language inscription before 1840 implausible beyond reasonable accommodation.

Conversely, the candidate becomes solve-claim worthy only if a physical witness independently selects `DMVAVA` and a historical mechanism independently licenses the transform (or a much stronger held-out prediction follows from it).
