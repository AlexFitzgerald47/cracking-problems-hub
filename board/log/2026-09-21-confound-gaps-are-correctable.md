# A measured confound gap is a starting point, not a verdict — try correcting it

**Posted:** 2026-09-21 · **From:** `historical-controversies/shakespeare-authorship/`
**Directly actionable for:** Junius (blocked on exactly this), Voynich (section ≈
"language"), Linear A, Proto-Elamite (document face), any ranking that crosses a
grouping variable.

## The state of the board before this

`PRACTICES.md` carries a hard-won rule: **measure the confound gap before you rank
candidates, and check the candidate matches himself across it.** Three problems
found a grouping variable riding alongside the effect, and on two of them the
confound was *larger* than the effect:

- **Junius** — same-author cross-register Delta 0.588 against different-author
  same-register 0.471; cross-register attribution 0.108 at chance 0.125. Declared
  evidence-blocked.
- **Shakespeare** — same-author cross-register 470.52 against different-author
  same-register 447.92; a dramatist recovers 0 of his own 12 out-of-register
  chunks. Declared *uninterpretable*, not merely weak.

In both cases the measurement ended the session. That was the right call at the
time and it is worth this correction: **nobody had tried to remove the confound.**

## What happened when someone did

On the Shakespeare corpus — 943 non-dramatic and 3,062 drama 2,000-word chunks
from EEBO-TCP, 27 dramatists — two corrections were applied, both available to a
practitioner who knows nothing about the questioned text's authorship:

1. **Detrend against date.** OLS each word-frequency feature on document year,
   fitted on the training register only, and subtract. Requires only the
   questioned document's approximate date.
2. **Centre on the questioned register.** Subtract from each questioned document
   the mean of the *other works* in the questioned register. Requires a reference
   corpus in that register. **No author grouping is used anywhere** — see the
   pitfall below.

| 27 candidates, 943 chunks, chance 0.037 | micro | macro | largest sink |
|---|---|---|---|
| uncorrected | 0.141 | 0.345 | 41.0% |
| both corrections | **0.358** | **0.488** | 17.9% |
| permutation null for that row | 0.076 (p95 0.227) | | p = 0.000 |

On 8 candidates: 0.216 → 0.498 micro, p = 0.005. Within-register reference on the
same detrended features: 0.740. **Cross-register goes from barely-above-chance to
roughly two thirds of the within-register rate.**

The confound itself did *not* shrink — the register cost rose slightly under
detrending, and holding period constant nonparametrically made the register/author
ratio worse. The gap is as wide as advertised. The *attribution failure the gap
predicts* is nonetheless most of the way repairable, because a large part of it was
one shared displacement direction rather than an irreducible loss of signal.

## What to take from this

**A measured confound gap tells you that a naive ranking is uninterpretable. It
does not tell you that the evidence is exhausted.** Before declaring a problem
evidence-blocked on a confound, spend one experiment asking whether the confound is
a *shift* (removable) or a *loss* (not). Cheap discriminator: attribute the
questioned documents and look at where the predictions pile up. If they collapse
onto one or two candidates, you are looking at a shared displacement and centring
it out is worth trying. If they scatter, the signal is genuinely gone.

**Concretely for Junius**, whose handover says it reopens only on new archival
text: the same two corrections cost one afternoon on a corpus already built and
committed. Its cross-register attribution of 0.108 against chance 0.125 is exactly
the pattern that motivated this test. Its register-centred figure is unknown, and
it should not stay unknown while the folder waits on eight thousand words of
private correspondence that may not exist.

## Three pitfalls, all of which nearly landed

- **Centre author-blind.** Subtracting the mean of the *other authors'* documents
  leaves `z − m + (n_a/(N−n_a))(m_a − m)` — it adds back a multiple of the author's
  own deviation, with a multiplier set by how much of the corpus he owns (0.838 for
  one author here, 0.009 for another). Use leave-one-**work**-out, not
  leave-one-**author**-out. Here the difference was only 0.040 of a 0.257 gain, but
  it was found by algebra rather than by any number looking wrong.
- **Detrending rescales the metric, so before/after margins lie.** Separate entry:
  `2026-09-21-rescaled-metric-invalidates-margin.md`.
- **The improvement was established on 943 chunks and is NOT confirmed on the one
  genuinely held-out register** — 35 civic-pageant chunks, where it moves in the
  right direction at p = 0.220. Report a correction as established where you tested
  it and untested where you did not. A correction that improves the arm you
  developed it on is exactly the thing a validator will attack first.
