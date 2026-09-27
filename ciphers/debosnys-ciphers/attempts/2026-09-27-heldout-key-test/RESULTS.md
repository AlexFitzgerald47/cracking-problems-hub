# RESULTS — held-out test of the Debosnys shared signature key

**2026-09-27, Claude Code cloud session.** Frozen in `FREEZE.md` at commit `fa52442`
(17:51:45 UTC). Every held-out transcription list and held-out scan region was opened
after that commit. The run is reproducible from `src/` (commands at the end).

## Verdict: the key is retired

Two frozen falsifiers fired, and either alone retires the key under the verdict rules
fixed in FREEZE §6. **T1:** the key's own third glyph closes four verse lines on a dangling
onset, under both conventions. **T5:** Branch B, the only branch coherent with the model's
own rule, needs /os/ in at least 15.8% of syllables. The most /os/-rich comparison corpus has
4.3%.

The one test that passed at its frozen threshold, T4, passes **only** on glyph-internal pairs
that repeat the fitted composites. On the part of the grammar that expresses the model's
distinctive claim, it is at chance.

No value reaches *independent phonetic truth*. No plaintext was produced. Nothing here is a
solve-claim.

---

## Frozen predictions that failed

### 1. T1 — every verse line must close on a rime: **FAILED under S1 and S2**

The signature's third glyph, Sektu's `NU`, is read by the key as `<N U>` = **D + EB**:
N is an onset, and U is rime E plus an onset B. In the poem, cyphersolver's `TCURL` is **the
same glyph**. The evidence:

- **Matched-scale comparison:** `evidence/signature_NU_vs_poem_TCURL.png`. Both have two
  stacked wavy strokes, each ending in a hook or blob on the right.
- **Validated instrument:** max-NCC over ±15% scale. It clusters the poem's ten `TCURL`s with
  each other at mean rank 5.3 of 24 (chance 11.5, best possible 4.0).
- **Blot-free signature crop** (y 630–656): the two closest glyphs in the poem are both
  `TCURL`s, and all ten rank in the top 14 of 25. Mean rank is 7.1 (chance 12.0); exact
  rank-sum **p = 0.0027**.
- **Blot-contaminated crop** (the first run, reported here): p = 0.49–0.70, depending on the
  ink threshold. The dark blot above the glyph entered that crop.
- **Specificity:** probing with the signature's *other* glyphs (`O2RNO`, `CROSSB`, `C2B2`)
  ranks `TCURL`s at 16.8–17.2, below chance.

`TCURL` ends **lines 1, 2, 17 and 18** (couplets 1 and 9). Under the key these lines end
`…D|EB`. The final unit carries an onset B with no rime after it, which violates the
line-closure rule that produced the /kos/ prediction. Read as a rhyme instead, all four lines
end in *-deb*. No candidate language supplies that.

The 09-06 note exempted exactly these line-endings as "N.N, an independent terminal codepoint,
never N+N". It did so without comparing them with the signature glyph the key decodes as N+U.
**One glyph type cannot be both.** The exemption does not rescue the key either
(`src/derivation_audit.py`). If the glyph is one indivisible sign, then:

- the signature's third glyph is one component, and at ≤ 2 characters per sign there are
  **0** aligned maps;
- at ≤ 3 the only fits are `DOT = OSD`, `NU = EB`;
- lines 3–4 then end "…cos**d**", so /kos/ is gone and T1 fails at three couplets instead of
  two;
- `N = D`, the "strongest independent hook", disappears with it.

The frozen table had left `TCURL` opaque. FREEZE §4 assigns identity to the scan ("the scan
wins"), and the T6 row for couplets 1 and 9 anticipated this case: "if another key sign ends
the glyph, that sign's rule applies." With `TCURL` left opaque, T1 would pass vacuously.
Both readings are reported in `evidence/heldout_test_output.txt`.

### 2. T5 — Branch B's circle: **FAILED (Branch B falsified)**

Under B every circle is the rime /os/. The scan-verified poem has 80 circles among 507
component-equivalents (pictograms counted as 3). That gives a lower bound of
**L = 0.158** on the share of syllables rhyming in /os/, or 0.237 if S1's dots count as well.

The ceiling over the seven pinned corpora is orthographic, which overstates French and
English, in the key's favour:

| corpus | /os/ share |
|---|---|
| Camões, pt | **0.0428** |
| Cervantes, es | 0.0310 |
| Iliad, el | 0.0297 |
| Virgil, la | 0.0154 |
| Dante, it | 0.0097 |
| Baudelaire, fr | 0.0035 |
| Moore's *Odes of Anacreon*, en | 0.0009 |

L exceeds the ceiling **3.7-fold**. The only rescue is to call the circle inside `%` a different
sign from the circle in Sektu's own N-glyph grammar, which contradicts the transcription the
key was fitted to:

- circles in `%` glyphs only: 21/507 = 0.041, at the ceiling;
- circles in `%` glyphs plus tilde-glyphs: 0.071, still falsified.

Branch A's circle, read as the /o/ nucleus (0.158 against 0.09–0.25 in the corpora), is
ordinary. But A is the branch the rime|onset rule rejected, and T1 kills A and B alike
(`U = EB` is shared).

### 3. A frozen premise of my own was wrong (T7)

FREEZE claimed that English and French have no ordinary rhyme family on /kos/. **French
does:** *cosse*, *Écosse* /e.kɔs/, *précoce* /pʁe.kɔs/. *Écosse/précoce* even reproduces the
key's full `EC|OS` tail. The error biased against the key. With it corrected, T7 can fire only
on an English identification. None exists that is independent of the key: cyphersolver's
"French syllabary" rests on glyphs per line and the rhyme-identity rate. **T7 did not fire.**

---

## Frozen predictions that passed, and what they are worth

**T2 — the /kos/ glyph is the signature's glyph: passed.** Lines 3 and 4 end in an X with a
single round dot centred ~9–12 px above the apex (`evidence/composite_identity_sheet.png`).
This is the position of the blob above the signature's X. Evidence level: **visual identity**.
It says nothing about the value.

**T4 — typed transition grammar: passed at its frozen threshold, but the pass is
inherited.**

- **Primary** (S1, by-eye dot/tick calls, `TCURL`=`<N U>`, Romance, punctuation transparent):
  154 pairs = 118 canonical + 29 hiatus + 7 violations. Null median 41, 5th percentile 12.
  **p = 0.030.**
- **All 48 declared variants:** p = 0.018–0.050.
- **Best-of-{S1,S2} at matched budget:** p = 0.029–0.045.

*Exploratory decomposition, not frozen:*

| pairs | n | violations | null median | p |
|---|---|---|---|---|
| within a glyph | 107 | 1 | 28 | 0.014 |
| across whitespace, S1 | 47 | 6 | 12 | **0.26** |
| across whitespace, S2 | 45 | 4 | 11 | **0.16** |
| pairs absent from the signature | 89–95 | 7 | 24–26 | **0.098–0.109** |

About half the within-glyph pairs are the fitted composites recurring: X→DOT ×20 (`XP`),
N→U ×10 (`NU`), O→Z / Z→O ×20 (`%`). Those are canonical by construction. The last row drops
every ordered pair already present in the signature.

The key's typing matches *glyph-internal vertical order*: tops (tilde, bars, cc) as onsets,
bottoms (circle, dot) as rimes. That is Sektu's 2017 syllable-structure observation, not
support for H, EN, EC, OS or D. **Across whitespace**, where the model places its signature
case `DOT|N` = OS|D, the key does no better than chance. Its commonest violation there is X→N
= EC|D, an onset cluster /kd/, five times under S1. The PRACTICES rule applies: a structured
sub-object is not evidence until you condition on the level above it.

**T3 — the tilde as onset: reported, not a separate verdict.** 31 glyph-initial tildes; 5 of
18 key-sign predecessors are violations under S1 (4 of 19 under S2).

**T6 — rhyme predictions for the verse (scan-verified terminals):**

| couplet | lines | terminal | key's final syllable (S1 = S2) | status |
|---|---|---|---|---|
| 1 | 1–2 | `TCURL` = signature `NU` | …D·**EB**, dangling | **violation** |
| 2 | 3–4 | `XD`, round dot | EC·OS → **/kos/** | rime; model output, never tested against a plaintext |
| 3 | 5–6 | `SL(y,o)` | N·OS → **/nos/** | rime |
| 4 | 7–8 | `EQ3_O` | ?·OS → **/os/** | rime |
| 5 | 9 / 10 | ♀ / ♀ with a dot inside | non-key | no prediction; **mates differ** (see audit) |
| 6 | 11–12 | Δ | non-key | no prediction |
| 7 | 13 / 14 | `OX` / `OPLUS` (differ) | ?·OS / ?·OS | consistent (/os/ both) |
| 8 | 15–16 | `MARS_II` | ends in a non-key tick pair | no prediction |
| 9 | 17–18 | `TCURL` | …D·**EB**, dangling | **violation** |
| 10 | 19–20 | `BX` | non-key | no prediction |

The T6 falsifier (different glyphs in one couplet decoding to different rimes) did not fire.
But four of the six decodable couplets rhyme on *-os* and the other two violate. A poem that
saturated with *-os* is the T5 problem showing through the rhymes.

**T8 — extension toward plaintext: no signal.** The decoded runs are dominated by repeats:
`OSNOS` ×7, `ECOSECOS`, `DOSOS`, `OSNOSDOSOSECOSECOS`. They yield 11 distinct lexicon hits
(*ecos*, *seco*, *enos*, *debe*…). Permuted values do as well: null median 6, 95th
percentile 13, **p = 0.15**. No readable text.

**Secondary corpus (N9 and N10 as coded; not scan-verified beyond a spot check):**

| corpus | all pairs, S1 | all pairs, S2 | across whitespace |
|---|---|---|---|
| N9 | 0.059 | 0.025 | 0.089–0.13 |
| N10 | 0.061 | 0.022 | 0.081–0.20 |

Same pattern: the within-glyph order carries the effect, across-boundary pairs don't reach
significance. N9 contains no `NU`/`TCURL` glyph; its look-alike `N_Z` ranks 21 of 26
against the signature `NU`.

---

## Derivation audit (made before the freeze, from the fitting line only)

- **D1.** The DOT in `XP` is not separately visible on the only public scan. The mark above
  the X lies inside a dark blot. **Without the DOT the fit has no solution:** 0 aligned maps
  at ≤ 2 characters, and 0 with `N=D` at any chunk size up to 4.
  - *Post-freeze update, in the key's favour:* the blob sits exactly where the dot of every
    poem `XD` sits (`evidence/composite_identity_sheet.png`), and `XD` is the commonest glyph
    in the corpus. The mark is probably a dot.
- **D2.** A dot *above* the X, read top-first as Sektu reads every other composite, gives
  `<DOT X>`: **DOT = EC, X = OS**. The published order `<X DOT>` is a diacritic-last
  convention. The composite still reads ECOS, so /kos/ is unaffected. Both conventions were
  carried through every test.
- **D3.** The published "57 → 4 → 2 → Branch B" is two binary choices made by one rime|onset
  rule, applied at `DOT|N` and at `O|Z`, `O|O2RNO`. `N=D` and "Branch B" are not two
  confirmations.

## Audit of `dbourdeau/cyphersolver` `targets/debosnys/` @ `648309e` (claim source)

**Licence and provenance.**

- Notes are CC BY 4.0; code is MIT.
- All six page images are **byte-identical (SHA-1) to the Wikimedia Commons files**, which
  Commons marks Public Domain (Debosnys, c. 1883; uploaded 2015-11-10, credited to K. Schmeh).
  The repository's licence paragraph names other institutions and not this route. That is a
  gap in its credit line, not a restriction.
- All 149 crops were located in the Commons pages:
  - 146 at NCC ≥ 0.999, scale 3× or 4×;
  - `N10_L1c`–`L3c` overrun the page edge by 8 px (black fill), NCC 0.98–0.99;
  - `c3_block` is an exact crop.
- `cf.htm` is a failed download (a Mod_Security "Not Acceptable" page), not source material.
- The Debosnys signature line (the Hub key's fitting data) lies in the "portrait area" that N9
  excludes. cyphersolver never transcribed it.

**Glyph identities, poem (all 20 lines checked against the 4× crops).** Glyph-level agreement
on every legible token; cyphersolver's own `?` marks sit on genuinely stained tokens. The
disagreements, all resolved by the scan in `src/poem_scan_verified.py`:

1. **`XD` merges dots and ticks.** 25 tokens: 18–19 round dots and 3 clear ticks (L6 t7,
   L7 t6, L17 t6), plus borderline cases (L7 t7, L11 t11, L14 t12, L16 t3). Measured in
   `evidence/glyph_identity_output.txt` and `xd_marks_sheet.png`. All tests were run under
   three declared variants; none changes a verdict.
2. **Line 10's final ♀ has a dot inside its circle; line 9's is open.** Couplet terminals are
   therefore identical in **8 of 10**, not 9 of 10 as cyphersolver's NOTES claim. Couplet 7
   also differs (`OX`/`OPLUS`). The AABB structure stands; cyphersolver's chance figures need
   recomputing for 8 identical couplets plus two near-matches.
3. **Line 17, `N_OX`:** the x stands *left* of the o, so the order is `[N, X, O]`.
4. **Uncoded marks:** a dot at the upper left of L18 `N_OX`; a bar under L18 `N_COLON`; dots
   inside L20 `GATE`; a dot in the ring of L15 `DELTA_RING`.
5. **Possible order and identity slips:**
   - L2 `BARS_II` may be ticks over bars;
   - L2 t11 `N_O?`: the top stroke reads as well as a cup as a tilde;
   - L18 `SL(t,d)`: the lower mark may be a tick.
6. **Internal inconsistencies:**
   - NOTES says "Y with ring" for lines 5–6; the code is `SL(y,o)`.
   - NOTES says "two dots below" for lines 15–16; the code key says `MARS_II` has "two ticks
     below".
   - `DELTA_BAR` is defined as "Δ underlined" in the verse key and "Δ with bar above" in N10.
   - `II_EQ` and `SL2_BAR_O` are used in the verse but defined in no code key.
   - In N9, **180 of 268 distinct codes (254 of 637 tokens) are defined in neither code key**.
7. **Spot check, N9 line 2:** 23 of 24 tokens right; the comma after `516` is omitted.
8. **`516` versus the Hub's `5/6`:** neither reading is unambiguous
   (`evidence/num516_10x.png`). The middle mark is a straight stroke of digit height, leaning
   about 8° forward, on the digits' baseline. The Hub's 09-05 "unambiguously 5/6" overstated
   the scan.
9. **Identity finding that neither project made:** cyphersolver's `TCURL`, which is the Hub's
   "double wave / N.N" line-ending class, is Sektu's signature glyph `NU`. So are cyphersolver's
   `CC_EQ` = `C2B2`, `PM` = `CROSSB` and `SL(o,o)` = `ZOO`
   (`evidence/composite_identity_sheet.png`). Sektu's `O2RNO` has no recurrence in the poem;
   `HEART` is a different glyph (pedestal, inward horns).

**Imported, with attribution:** the poem transcription (MIT), with this session's
scan-verified overrides listed row by row. **Not imported:** N9 and N10. They were read from
the external repository at the pinned commit for the secondary analysis only, because they
were not scan-verified here. cyphersolver's "French syllabary" conclusion and its
unicity-distance argument are recorded as claims (statistical level), not adopted.

## The retired key, value by value, by evidence level

| sign | value (S1 / S2) | visual identity: held-out recurrence | structural recurrence | independent phonetic truth |
|---|---|---|---|---|
| `C2` | H | yes: `CC_EQ` ×2, `CC_EQ_OO`, `CC_BAR_O` | inherited only | none |
| `B2` | EN | yes: `EQ_*` family | inherited only | none |
| `X` | EC / OS | yes: 49 X components (19 round-dotted `XD`, 3 bare `X`) | across whitespace: X→N violations (/kd/) | none |
| `DOT` | OS / EC | probable in the signature; yes in `XD` | inherited only | none |
| `N` | D | yes: 31 glyph-initial tildes | within-glyph order consistent; across: 5 of 18 violations | none |
| `U` | EB | yes: lower stroke of 10 `TCURL`s, plus 3 cups | **contradicted**: four line-ends dangle | **contradicted** (*-deb* rhyme) |
| `O` | OS (B) / O (A) | yes: 80 circles | **B contradicted** by T5 | none |
| `Z` | N (B) | yes: slash of `%`-glyphs | inherited only | none |
| `O2RNO` | T (B) | **no held-out recurrence found** | — | none |
| `CROSSB` | YS | yes: `PM` ×2 (L3, L9) | no testable pairs | none |

"Model output" is every value above; that is how they were obtained. The /kos/ reading of
lines 3–4 never rose above model output.

## What would reopen it

- **A better image of #2b's signature line** from the originals (Essex County Historical
  Society or the Adirondack History Museum). If the third glyph proved to differ from the
  poem's `TCURL` at higher resolution, T1's failure would lift. T5 would still stand against
  Branch B.
- **A new atom-level derivation.** It would have to fit the signature *and* close every verse
  line on a rime. It would also have to keep every common sign under the frequency ceiling
  of the value it is given. That is a new hypothesis needing its own FREEZE, not a repair of
  this one.

## Reproduce

```
cd ciphers/debosnys-ciphers/attempts/2026-09-27-heldout-key-test/src
python3 freeze_rules.py            # frozen rules self-check (4,200 typings)
python3 derivation_audit.py        # D1/D2 and the NN-codepoint escape
python3 heldout_test.py            # T1, T3, T4 (+ all variants, best-of-2 null)
python3 diagnostics.py             # exploratory: within/across split, violations, positions
python3 t5_frequency.py <corpora>  # T5; corpora = Gutenberg 2000 3333 6099 227 1000 38230 36248 saved as <lang>.txt
python3 t8_lexical.py <corpora>    # T8
python3 secondary_n9_n10.py <cyphersolver>/targets/debosnys
python3 glyph_identity.py <cyphersolver>/targets/debosnys ../evidence
```

Requires Python 3.11, numpy, opencv-python-headless and pillow; `<cyphersolver>` is a checkout
of `dbourdeau/cyphersolver` at `648309e`.
