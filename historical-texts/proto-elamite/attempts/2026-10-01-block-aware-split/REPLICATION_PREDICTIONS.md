# Predictions frozen before the 130 new CDLI tablets were analysed

**Session:** 2026-10-01, Claude Opus 5 Breaker. Committed before
`results/cdli_replicate.json` exists.

This is the folder's recommended experiment 4 of 2026-09-17 — *"replication on a newer
CDLI export remains the strongest falsification test and is still unrun"* — and 2026-09-04's
recommended experiment 2. It is now runnable because a live bulk ATF route exists:

```
https://cdli.earth/search?period=Proto-Elamite&format=atf&aspect=inscriptions&limit=3000
```
fetched 2026-10-01T18:43:20Z, HTTP 200, `text/x-c-atf`, 508,015 bytes, 1,597 `&P` blocks.

**The new tablets are a strict superset of the pin.** All 1,467 pinned P-numbers are
present in the live export; **130 are new**. Nothing from the pin has been withdrawn.

**Parser compatibility is established, not assumed** (`cdli_compat.py`,
`results/cdli_compat.json`): on the 1,467 overlapping tablets the 2026-09-04 parser gives
4,869 eligible lines from the pinned SFU serialisation and 4,868 from the live CDLI one,
with only 11 tablets differing on eligible-line count and per-sign differences of ±1 or
±2. Those are CDLI's own curation edits since August 2022, not a serialisation
incompatibility. One systematic renaming exists — pinned `N08` is live `N08A` — which
touches no pair under test here.

At the time of writing I have read, from the 130 new tablets, only their P-numbers. No
line, sign, count or statistic from them has been computed.

## Predictions

**R1 — direction, the published falsification test.** On the 130 new tablets alone, the
three load-bearing pairs hold in the direction 2026-09-04 published: **M297–N39B
enriched, M263–N01 enriched, M263–N30C depleted** (corrected odds ratio on the right side
of 1). *This is the prediction the constraints were published under and the one that can
actually refute them.* **Confidence: moderate-high for M297–N39B and M263–N01, lower for
M263–N30C**, whose published form is an *absence* (0/46 in the 2026-09-04 holdout) and
which a single counter-example on a small sample pushes off zero.

**R2 — the new tablets are too few to confirm anything on their own.** For a majority of
the eight pairs the face-blocked p-value floor on the 130 new tablets exceeds 0.05: the
test cannot return a significant answer whatever the data say. I predict **at most two of
the eight** have power at 0.05 on the new tablets alone. This is the folder's own p-floor
discipline applied before looking, and it is why R1 is stated as a direction test rather
than a significance test.

**R3 — M288–N45 is untestable on the new tablets alone.** Its face-blocked p-floor on the
130 new tablets exceeds 0.05, and it contributes **at most 2** new informative
(tablet, face) blocks. *Rationale:* N45 occurs on 91 eligible lines across 1,457 tablets,
about one per sixteen tablets, and an informative block needs M288 and N45 on the same
face with slack. 130 tablets should yield almost none.

**R4 — the fair-coin faces hold up when the corpus grows.** On the pooled 1,597-tablet
corpus, the two-line fair-coin faces for M288–N45 (`total = 2, s = 1, t = 1`, of which the
pin has eight, all eight heads) still come up heads at a rate significant at 0.05 by
exact binomial. I predict **at most 3** new coin faces appear, and **at least 2 of 3** of
any that do are heads.

**R5 — no new load-bearing constraint appears.** Re-screening the pooled corpus and
re-validating does not add a ninth pair that clears the published confirmation rule under
face blocking with BH over the full re-screened candidate set. *Rationale:* this session
already found that under the published 54-candidate BH base, face blocking confirms only
two pairs on the pinned corpus; a 9% corpus increase should not change that.

## What would change the verdict

- **R1 failing for M297–N39B or M263–N01** → the folder's load-bearing constraints fail
  their own published falsification test on genuinely new tablets, and must be
  downgraded. This is the single most consequential outcome available this session.
- R1 failing for M263–N30C alone → weakens that pair specifically; an absence claim is
  the most fragile kind and a small sample is its worst test.
- R3 failing in the generous direction (the new tablets *do* carry informative blocks for
  M288–N45) → an unexpected bonus, and the pair's verdict should be recomputed pooled.

## Not claimed either way

Nothing here assigns a semantic, phonetic or metrological value to any sign. The 130 new
tablets' publication groups and proveniences have not been inspected and no claim about
where they come from is made.
