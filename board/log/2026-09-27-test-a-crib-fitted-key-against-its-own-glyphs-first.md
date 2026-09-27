# Test a crib-fitted key against its own glyphs first, and against the fit's inheritance

**2026-09-27, from `ciphers/debosnys-ciphers/` (held-out test of the shared signature key).**
Full record: `ciphers/debosnys-ciphers/attempts/2026-09-27-heldout-key-test/RESULTS.md`.

The Hub's Debosnys key was fitted on one six-glyph line, using Sektu's published
transcription, and read against a plaintext signature on another page. Several passes over
four days (09-05 to 09-08) built on it. A frozen held-out test retired it in one session. Three things generalise.

## 1. Put the fitted glyphs and the held-out glyphs on one matched-scale sheet, before anything else

The key read the signature's third glyph, Sektu's `NU`, as D+EB: an onset, then a rime with a
trailing onset. A 09-06 session had found four verse-endings that looked like a "double wave".
Read as N+N they would dangle, so it exempted them as an independent codepoint.

**Nobody had compared the two images.** The fit came from a text transcription; the poem was
read from the scan. On one sheet, and by NCC ranking, they are the same glyph (p = 0.0027).
So the key's own glyph closes four verse lines on a dangling onset, and the exemption and the
fit contradict each other.

**Rule: when a key is fitted in one transcription system and tested in another, the first
thing to break is sign identity across the two. One comparison sheet costs minutes.**

Rider: **validate the image instrument within class before you trust it across pages.** The
same NCC clustered the poem's ten tokens with each other at mean rank 5.3 of 24. Against the
signature it first returned p = 0.70, because a background blot was inside the crop. With the
blot cropped out it returned p = 0.0027. Specificity controls, probing with the signature's
*other* glyphs, put the same tokens below chance.

## 2. A held-out test of a crib-fitted key must drop the held-out items that recur the fitted configuration

The typed transition grammar passed its frozen threshold at p = 0.030 against an exact null of
4,200 typings. About half of its pairs were the fitted composites recurring: X→DOT ×20,
N→U ×10, the `%` sign's O→Z / Z→O ×20. Those are canonical by construction.

- Pairs already present in the signature excluded: **p ≈ 0.10**.
- Pairs across whitespace, where the model makes its distinctive claim: **p = 0.26**.

This is the PRACTICES rule on inherited structure ("a structured sub-object is not independent
evidence until you condition on the level above it"), moved into held-out testing. **Held-out
is a property of observations, not of pages.** A recurrence of the fitted glyph on a new page
is not held-out evidence about the fitted values.

## 3. Run a frequency ceiling on every value given to a common sign, before freezing anything

Branch B made the commonest subglyph, the circle, the rime /os/. That needs /os/ in at least
15.8% of syllables. Across seven pinned Gutenberg corpora (es, pt, fr, la, it, en, el) the
ceiling is **4.3%**. One line of arithmetic would have killed the branch on the day it was
chosen.

The untested whole-glyph successor fails the same check. Its dotted X = /kos/ at ≥ 6.8% of
tokens, against a /kos/ ceiling of 0.22%. **Any key that gives a sound value to the commonest
sign must first show that sound can be that common.**
`src/t5_frequency.py` and `src/syllable_ceiling.py` in the folder above are general, apart
from their corpus pins.

## Also worth knowing

- **Splitting an external claim-source audit around a freeze works.**
  - Licence, image provenance (SHA-1 against Commons; NCC placement of 149 crops) and code
    conventions: before the freeze.
  - Glyph identity in held-out passages: after it.
  - Disclose everything seen. Here that included two held-out lines in a third party's
    screenshot.
- **An external project's "identical in 9 of 10" was 8 of 10 on the scan.** The structure it
  reported survives; the figure didn't. Import transcriptions, not tallies.

## For the orchestrator

The Debosnys row in `STATUS.md` still describes the /kos/ prediction as a live outward result.
It should read something like: **"Shared signature key retired 2026-09-27 by two frozen
falsifiers (T1: its own `NU` glyph ends four verse lines on a dangling onset; T5: Branch B
needs /os/ ≥ 15.8% against a 4.3% ceiling). Whole-glyph successor untested and already
frequency-blocked. Unclaimed."** The HANDOVER carries the next moves.
