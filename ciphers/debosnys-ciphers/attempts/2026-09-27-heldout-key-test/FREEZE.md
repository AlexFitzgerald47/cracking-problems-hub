# FREEZE — held-out test of the Debosnys shared signature key

**Frozen:** 2026-09-27, Claude Code cloud session, in the commit that adds this file. Its git
timestamp is the freeze time. **Machine-readable half:** `src/freeze_rules.py`, committed
together with this file and not to be edited afterwards. Post-freeze code imports it.

**Nothing here was fitted to held-out data.** When this file was committed, none of the
held-out transcription lists (`VERSE`, `N9`, `N10` in `dbourdeau/cyphersolver`) and no
held-out region of any scan had been opened by this session, except as disclosed in §0.

---

## 0. Exposure disclosure — what had been seen when this was written

| seen | how | held-out? |
|---|---|---|
| Every file in this problem folder, including prior sessions' *descriptions* of poem line-endings: lines 1, 2, 17, 18 double-wave; 3, 4 dotted X; 13, 14 O-plus-cross; 19, 20 ornate | read as text | descriptions only; never viewed by this session |
| The signature-like line on `c2b.png` (x 602–777, y 623–667) at 4×, 6× and 12× | viewed | **no** — the key's fitting data |
| A 66 × 34 px window directly above that line's X (x 634–700, y 614–648) | viewed | touches the lowest ~10 px of N9 line 25 |
| Sektu's 2017-06-24 screenshot, which includes N9 lines 24–25 at ~0.76× | viewed once, not transcribed | **yes, disclosed** |
| cyphersolver: licence, `CLAUDE.md` head, file list and sizes, crop geometry (computed, not viewed), `NOTES.md` headings and first 12 lines, and the **docstrings** (code keys) of the three transcription files | read | code key only; no transcription tokens |
| Wikimedia Commons metadata for the six scans; Sektu's two 2017 posts as text | read | no |

**Not yet seen:** any poem line, any N9 or N10 line beyond the above, the `#1` lines, the
plaintext signature on #4b, cyphersolver's `NOTES.md` body, and every script output.

## 1. The object under test

This is Branch B, the only branch coherent with the transition model's own rime|onset rule.
Types: **O** = onset only, **RO** = rime + following onset, **R** = rime.

| sign | S1 (published `<X DOT>`) | S2 (dot above the X read first, `<DOT X>`) |
|---|---|---|
| `C2` (two c-hooks) | H · O | H · O |
| `B2` (two bars) | EN · RO | EN · RO |
| `X` | EC · RO | **OS · R** |
| `DOT` | OS · R | **EC · RO** |
| `N` (single tilde) | D · O | D · O |
| `U` (cup) | EB · RO | EB · RO |
| `O` (circle) | OS · R | OS · R |
| `Z` (slash of `%`) | N · O | N · O |
| `O2RNO` (horseshoe with rings) | T · O | T · O |
| `CROSSB` (±) | YS · R | YS · R |

Branch A (`O=O`, `Z=SN`, `O2RNO=ST`) enters only T5.

## 2. Derivation findings made before this freeze (from the fitting line, not held-out)

**D1. The load-bearing DOT is not visible.** At 4×, 6× and 12× on the only public image,
the signature's second glyph is a bare X. The only mark nearby is a compact blob 8–9 px
*above* the apex, at the lower edge of a ~35 px-wide dark blot. The blob is darker than the
X's own ink (min grey 2 against 44). It may be a pen dot inside the blot, or it may be only
the blot. Evidence: `evidence/sigline_c2b_6x.png`, `evidence/sig_above_X_12x_nearest.png`.
**Without the DOT the derivation has no solution.** At ≤2 characters per sign there are
**0** boundary-aligned maps, and at any chunk size up to 4 there are **0** with `N=D`
(`src/derivation_audit.py` records this run).

**D2. If the mark is a dot, it is above the X.** Sektu reads everything else in this line
top-first (`C2` over `B2`, `N` over `U`, `%` as upper-left `O`, `Z`, lower-right `O`). By
that rule `XP` is `<DOT X>`, which gives `DOT=EC`, `X=OS` (S2). The composite `ECOS`, and
therefore the /kos/ prediction for a glyph of the same shape, is identical under S1 and S2.
Every isolated X and every dot elsewhere flips value.

**D3.** `N=D` and the Branch-B choice are the same rime|onset rule applied twice (see the
PROGRESS entry of this date).

## 3. Branch count

- **Key-intrinsic, tested:** S1 / S2 = 2. A third state, S3 (no dot), leaves the key
  undefined and is not testable on held-out data. Branch A appears only in T5.
- **Analysis choices, fixed in advance (primary in bold):**
  - phonotactics: **Romance** / Greek-lenient (exempts κτ, κν, βδ)
  - punctuation: **transparent** / chain-break
  - backslash: **≠ Z** / ≡ Z
  - "ring": **≠ O** / ≡ O
  - `XD` counted as X + DOT **only where the scan shows a dot** / as coded
  - corpus: **the poem, scan-verified by this session** / N9 + N10 as coded by cyphersolver
- **Derivation forks already taken by earlier sessions (context, not re-tested):** ≥ 12
  cribs (ten in `signature_crib_csp.py`, plus TYS/TYA); ≥ 5 mechanisms (six whole-glyph
  chunks, seven-syllable hierarchy, strict atoms at 1–4 characters, shifted units,
  transition chunks); the `N` choice; the A/B choice. That is several hundred paths, of
  which the published key is one. Held-out testing is what prices that freedom.
- **Matched budget.** Any claim about "some branch" passing uses best-of-{S1, S2} against
  a null that takes the best of the same two operations (`swap_x_dot`) on each random
  typing. The primary test is single-shot: S1, Romance, transparent, poem.

## 4. Held-out set and audit protocol

**Held-out** means every cipher token except the signature-like line on #2b.

- **Primary corpus:** the 20-line poem (#4a lines 1–15, #4b lines 16–20). Every token is
  checked by this session against cyphersolver's 4× half-line crops of the Commons scans,
  whose provenance was verified by NCC ≥ 0.999. **Where scan and transcription disagree,
  the scan wins.** Every disagreement is recorded. Tokens that cannot be resolved are
  excluded and counted.
- **Secondary corpus:** N9 (25 lines, #2a + #2b) and N10 (the 4 lines on #3), as coded,
  with key-sign tokens spot-checked and an error rate reported.
- **Components:** each token is parsed with the frozen table in `src/freeze_rules.py`.
  Pairs touching a position-ambiguous component (`?…`) are excluded.
- **Adjacent pairs:** within a glyph, consecutive components; across glyphs, the last
  component of one glyph and the first of the next glyph in the same line. Only pairs where
  both components are key signs are tested. `NN` (double tilde) is non-key; any use of it
  is reported.

## 5. Frozen predictions and what falsifies each

**T1 — every verse line closes on a rime (rhyme positions).** For each poem line, the last
component of the last non-punctuation glyph must be R-type if it is a key sign.
*Falsified (per convention)* if any scan-verified couplet ends in an O- or RO-type key sign.
Couplet mates are counted once. A double-tilde terminal needs the 09-06 "NN is a separate
codepoint" exemption; each use is counted as a spent free parameter, not a pass.

**T2 — the /kos/ glyph is the signature's glyph.** Poem lines 3 and 4 must end in an X with
a single dot centred above the apex, the geometry of the mark above the signature X. The
dot must not be a tick or stroke, and the base must be the same X (not `CX`, `BX` or `HX`).
*Falsified* if either terminal's mark is a tick or stroke, is not above, or sits on a
different base. *If it passes:* evidence level is **visual identity**, still conditional
on D1.

**T3 — the tilde is an onset (cleanest subset of T4).** For every glyph beginning with a
single tilde `N`, the preceding component in the line must be R-type, non-key, or the
line start. *Violation:* an O- or RO-type predecessor, which gives an onset cluster HD,
DD, ND, TD, CD or BD.

**T4 — typed transition grammar, all pairs (PRIMARY).**
- Statistic: `V` = the number of violation pairs, where `(O|RO) → O` is a violation.
  Hiatus pairs `R → R` and `R → RO` are reported separately.
- Null: **exact**, over all **4,200** typings that assign the key's type multiset
  {O×4, RO×3, R×3} to the ten signs. `p = P(V_random ≤ V_key)`, ties counted against the key.
- *Survives* if p ≤ 0.05. *Fails* if `V_key` is at or above the null median. In between is
  inconclusive.
- *Underpowered, not refuted* if fewer than 20 testable pairs exist, or if the null's 5th
  percentile equals its median.

**T5 — Branch B's circle cannot be a rime of every syllable class.** Under B every circle is
the rime /os/. Each syllable has exactly one rime-bearing unit, and a unit spans at least one
component; a pictogram may carry up to 3 syllables. So the implied share of syllables rhyming
in /os/ is at least:

    L = #O / (#non-pictogram components + 3 · #pictograms)

The ceiling `f_os` is the largest orthographic share of syllables whose rime is o + s-coda,
taken over the seven pinned corpora (`CORPORA` in `src/freeze_rules.py`). Orthographic
counting overstates French /os/, which biases the test in favour of the key.
*Branch B falsified* if `L > max f_os`. Rescuing it by splitting "the `%` circle" from
"other circles" is a new free parameter, reported as such, and does not count as survival.
Branch A's circle is scored against the /o/-nucleus share for information only.

**T6 — rhyme predictions for the verse lines.**

| couplet (lines) | prior Hub description | key's frozen prediction |
|---|---|---|
| 1 (1–2) and 9 (17–18) | double wave | a bare double tilde is `NN`. Read as N+N it gives D D, a dangling onset, i.e. a T1 violation. The key survives only by the NN exemption, which is logged as a free parameter. If another key sign ends the glyph, that sign's rule applies. |
| 2 (3–4) | dotted X | **/kos/** under S1 and S2, conditional on T2 |
| 7 (13–14) | O plus cross | if the last component is the circle, **/os/** under B; the key then predicts couplets 2 and 7 share the -os family. If the last component is a non-key cross, no prediction. |
| others | not described | decode the terminal by the frozen table; predict the rime if the last component is a key sign |

*Falsified* if the two lines of one couplet end in different scan-verified glyphs that both
decode to different final rimes. Identical glyphs agreeing is **not** evidence and will not
be reported as a hit.

**T7 — language condition.** Where an identification of the poem's language exists that
does not come from the key, check it against the /kos/ couplet. English and French have no
ordinary rhyme family on /kos/. An independently supported English or French poem therefore
falsifies the key, conditional on that identification. Each language claim found
(cyphersolver's included) is graded by its evidence level before use.

**T8 — extension toward plaintext (run only if T4 survives).** Decode every run of ≥ 3
consecutive key-sign components within a line. Count the substrings of length ≥ 4 that
occur as word types (count ≥ 3) in the pinned corpora. Compare against 10,000 random value
permutations over the same runs, at the same best-of-2 budget. A readable decoded string is
a **solve-claim for the validator panel, not a result**, and will not be announced.

## 6. Verdict rules, fixed now

- **Retire the key** if any of these holds:
  1. T1 is falsified under both S1 and S2.
  2. T4 fails under both S1 and S2 at matched budget.
  3. T5 falsifies Branch B, the model-coherent branch; Branch A is already excluded by the
     rime|onset rule that selected B.
- **Survives at structural-recurrence level only** if T1 holds, T4 survives at the matched
  budget, and T5 does not falsify B. Values used by passing tests are labelled *structural
  recurrence*. Nothing is labelled *independent phonetic truth* without T7 or T8
  confirmation from outside the key.
- Everything else is **inconclusive**, stated as such with the power numbers.
- Whichever way it goes, the write-up leads with every frozen prediction that failed.
