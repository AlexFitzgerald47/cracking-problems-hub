# Handover Notes – Kryptos

*Latest notes at the top.*

---

## 2026-09-04 – Claude (Opus 5), remote session

### Summary of work done

Corrected the problem statement (K4's plaintext was recovered from archives in
2025 and confirmed by Sanborn; the open problem is now the method and key), then
used the two public cribs to eliminate whole cipher families rather than to test
candidate keys. Full numbers in `PROGRESS.md`.

### What worked / partial results worth keeping

- **Spend cribs on families, not on candidates.** The partial-bijection test
  kills a period for every periodic polyalphabetic cipher at once, without
  knowing the alphabet or key. Much better value per crib character than testing
  keys one at a time.
- **Pure transposition dies on a letter count.** The cribs need three E's; the
  ciphertext has two. Worth doing this multiset check first on any cipher with
  cribs — it is free.
- **The Vigenère family (Vigenère, variant, Beaufort) is gone** at every period
  where the cribs have power. Reproducible, with the null attached.
- **Pair every elimination with a null.** Most of K4's "surviving" periods
  survive because the test has no power there, not because the hypothesis fits.
  Without the null this attempt would have produced a list of 78 "possible
  periods" that means nothing.

### What failed and why

- The general polyalphabetic test has power at only 13 of 97 periods. 24 crib
  characters is simply not much leverage against that family. This was the
  intended main result and it mostly measured its own weakness.
- Composite schemes (transposition then substitution, Sanborn's hinted masking)
  are untouched — the method here cannot reach them.
- Could not read the primary reporting on the 2025 recovery; egress restrictions.

### Recommended next experiments

*(Items 1 and 2 below were completed later the same day — see findings 6–8 in
`PROGRESS.md`. Simple transposition composites show no signal above chance, and
the crib-value question is answered: ask for a ten-character crib near position
44–47. What remains is item 1', below.)*

1'. **Keyed columnar transposition.** The composite search covered only simple
   unkeyed transpositions. K3 used a keyed one. The column-order space is
   factorial, so this needs a smarter search than enumeration — but the crib
   test is cheap per candidate and the null rates are already computed and
   reusable, so a randomised or beam search over column orders is affordable.

1. **Test composite hypotheses.** The obvious one, given Sanborn's hints and the
   K1–K3 lineage: a transposition applied before or after a Quagmire. The
   partial-bijection test can be run *after* applying a candidate transposition,
   so a search over plausible route/columnar transpositions with the cribs
   carried along is tractable and would eliminate a lot at once.
2. **Quantify what a third crib would buy.** Simulate: given a hypothetical extra
   crib of length L at position x, how many periods would become eliminable? That
   tells the community exactly what to ask Sanborn's estate for, and is cheap.
   It is the same "what is the evidence worth" question as
   `discovered/short-cipher-validation-bound/`.
3. ~~**Chase or kill period 19.**~~ **Killed the same day.** It was the only
   powered survivor against the identity transposition, but against 133
   transpositions it is one of 35 survivors where 27 were expected by chance.
   Do not spend time on it.
4. **Do not import claimed plaintext reconstructions.** Several are circulating
   post-2025. Treating one as ground truth would silently invalidate everything
   downstream. The two public cribs are the only confirmed plaintext.

### New leads or related problems discovered

- The 2025 recovery makes K4 an unusually clean instance of a general question:
  what counts as solving a cipher whose plaintext is known but sealed? That bears
  directly on `discovered/short-cipher-validation-bound/`.

### Open questions left hanging

- ~~Is the period-19 survival known in the literature, or new?~~ Moot — it is
  chance (finding 6).
- Does the exact power rule in finding 7 generalise? It says a crib set's
  discriminating power against periodic ciphers is carried entirely by pairs of
  positions sharing a plaintext letter. That looks like a general fact about
  crib-based cryptanalysis, not a K4 fact, and if so it belongs in
  `discovered/short-cipher-validation-bound/`.
- Does any claimed public reconstruction actually satisfy the two public cribs?
  That is a cheap filter this session did not run, because it declined to handle
  reconstructions at all. A future agent could test crib-consistency without
  treating any reconstruction as true.

### Files / artefacts added or significantly updated

- `attempts/2026-09-04-crib-constraints/` (new)
- `PROBLEM.md`: appended a correction and restatement of the open problem
- `PROGRESS.md`, `HANDOVER.md`, `/STATUS.md`

---

## 2026-09-03 – Initial seed

### Recommended next experiments
1. Systematic re-evaluation of all publicly released Sanborn clues against the known ciphertext.
2. Test modern computational approaches (including AI-assisted search) on the remaining ciphertext while respecting known constraints from K1–K3.
3. Examine the physical and orientational aspects of the sculpture for additional cryptographic information.
