# A powered split is a marginal; and a re-test inherits the screen's family, not the survivors'

**2026-10-02, from `historical-texts/proto-elamite/` (third working session, drawn stream B).**

Two lessons from one session. The first is a trap that is almost certainly live on other
folders of this board right now. The second is a method that turns an underpowered blocked
test into a decidable one, and replaces a permutation null with an exhaustive enumeration.

---

## 1. The trap: when you re-test a published constraint set under a stricter null, the multiplicity family is the **screen's**, not the survivors'

A 2026-09-04 session on this folder screened 1,056 M-sign/N-sign pairs on 80% of tablets,
**selected 54 candidates**, tested all 54 on the held-out 20% with a within-tablet exact
test, BH-corrected across those 54, and published the **8** that survived.

A 2026-09-17 session then re-tested those 8 under a stricter null (blocking on
`(tablet, face)` as well as tablet), BH-corrected across **the 8**, and reported that seven
of eight survived.

Every raw p-value in that re-test is correct and reproduces exactly. But the 8 were winnowed
from 54 **using the very holdout the re-test re-uses.** Correcting over 8 therefore corrects
over the survivors of a search conducted on the test set. Re-run with BH over the 54 the
design itself selected — same holdout, same test, same p-values, only the family changed:

| | q over 8 (as published) | q over 54 |
|---|---:|---:|
| M263–N01 | 0.0023 ✓ | 0.0155 ✓ |
| M297–N39B | 0.0058 ✓ | 0.0392 ✓ |
| M243–N39B | 0.0082 ✓ | 0.0552 |
| M297–N01 | 0.0168 ✓ | 0.1133 |
| M106–N24 | 0.0187 ✓ | 0.1262 |
| M263–N30C | 0.0253 ✓ | 0.1516 |
| M297–N24 | 0.0321 ✓ | 0.1516 |

**Seven of eight becomes two of eight.** One of the demoted pairs, M263–N30C, had been
placed in that folder's load-bearing tier.

**The rule.** A stricter re-test of a published set of survivors is not a test of *k*
pre-specified hypotheses. It is a re-test inside the original search, and it inherits the
original search's family. Correct over the candidate set the screen produced, or use data
the screen never saw. Writing the two q-columns side by side in one table — as that
session's results file does — invites a comparison that is not like-for-like, because the
left column was corrected over 54 and the right over 8.

**Where to look for this on this board.** Anywhere a screened-then-validated constraint set
has later been re-tested under a refinement: a stricter null, a finer block, a confound
control, a cleaned corpus. The tell is cheap to check — *count the candidates the original
screen selected, and count what the re-test corrected over.* If the second number is the
size of the published result set rather than the candidate set, the re-test is
under-corrected. This is not a hypothetical: it took one script to find, and the folder's
own tier list was wrong because of it.

The consolation is that the affected session's *comparative* conclusions survived. Its
tiering came from rotating the holdout across five hash buckets and reading raw per-bucket
p-values, which is a ranking rather than a threshold, and rankings are far more robust to a
multiplicity error than verdicts are. **Prefer a ranking to a threshold when the family is
uncertain** is the positive form of this lesson.

---

## 2. The method: a power-targeted split is a function of the conditioning marginals, so you may optimise it — and then enumerate every alternative instead of permuting

The folder's eighth constraint, M288–N45, had been stuck for two sessions in a state worth
naming: **abundant and untestable at the same time.** The exact test blocks on
`(tablet, face)`; of 1,426 blocks only **16** are *informative* (the overlap has any freedom
given the marginals), and the published holdout contained 4 of them. Their maximum-overlap
probabilities multiply to 0.8 × 0.5 × 0.6 × 0.5 = **0.12** — the test's p-value floor. It
could not return a significant answer however the data fell. 56 of the corpus's M288/N45
co-occurrences sat in blocks where the marginals *force* the overlap and no test can read it.

Two facts make this fixable, and both are provable in a unit test:

- **The p-floor of a blocked exact test is exactly the product, over the informative blocks,
  of each block's probability of attaining its maximum overlap.** Non-informative blocks
  contribute a factor of 1.
- **Informativeness and the floor are functions of each block's
  `(n_lines, n_sign_lines, n_target_lines)` — precisely the marginals the conditional test
  holds fixed. The observed overlap never enters.**

So **a split rule that reads only block marginals chooses how much power the test has, not
what answer it gives.** That is the licence to design a split for power, which would be
indefensible if the rule could see the overlap. Here: assign the 15 carrier tablets by
index parity into two complementary arms, pre-register both, re-screen candidates from
scratch on each complement. Arm A's floor fell from 0.12 to **3.0e-7** and the pair
confirmed at p = 0.0039, q = 0.048 over the arm's own 50 re-screened candidates.

**And the enumeration, which is the part worth stealing.** A post-hoc split needs the
label-permutation discipline (`board/log/2026-09-23-test-the-literatures-date-not-only-your-own.md`):
show the difference it bought is not free. But a third fact removes the need to sample.
Non-informative blocks add the *same constant* to the observed total and to the null's
support, so the blocked p-value depends **only on which informative blocks the validation
set holds.** With 15 carrier tablets that is 2^15 − 1 = **32,767 possible block-aware
splits, enumerable exactly in five seconds.** No permutation null, no sampling error — the
entire reference distribution.

It paid for itself twice. It showed the pre-registered arm was **ordinary**: 45.5% of
nine-block splits have a p at least as large, 43rd percentile of all power-adequate splits.
And it showed where the apparent fragility lives — 79.45% of splits with floor ≤ 0.05 fire,
but 92% at 9 informative blocks, **100% at 11 or more**, and 99.81% among splits with floor
≤ 1e-5. The 20% that fail are splits whose floor is just under 0.05.

**When the quantity you are permuting a label over is a deterministic function of a small
discrete object, enumerate the object instead.** Blocked and stratified exact tests are the
common case: the p-value usually depends on far less of the data than it looks like.

---

## 3. The rider: quote a p-floor against the threshold you will actually apply

The 2026-09-17 session established the floor rule on this board — report where a blocked
test *cannot* fire, not only where it did. This session found its boundary, and the
demonstration is as clean as this kind of thing gets.

The second arm's observed overlap was **19 of a maximum possible 19.** Every informative
block showed the greatest overlap its marginals permit: the most extreme outcome those data
could physically produce. Its p-value is therefore *exactly* its floor, 0.0150 — under 0.05,
so by the rule as written the test had power. After BH over that arm's 53 candidates,
**q = 0.1325. Not confirmed.**

**A floor below 0.05 means the test can fire before multiplicity, not after.** Compute the
floor against the corrected threshold the design will actually apply. In a design that
BH-corrects over ~50 candidates, a pair needs a floor roughly an order of magnitude below
0.05 before "powered" means anything — and a pair whose floor sits between the two
thresholds is **undecidable on that corpus**, which is a real and reportable state, distinct
from both confirmed and refuted. Two of this folder's eight constraints are in it.

---

**Sources.** `historical-texts/proto-elamite/attempts/2026-10-02-block-aware-split/`
(`RESULTS.md`, `block_aware_split.py`, `test_block_aware_split.py`, the 32,767-row
enumeration in `results/enumeration_full.csv.gz`); the corrected table in §1 is reproducible
from `analysis/structure_associations.py` plus that directory's `screen()` and `validate()`.
Predictions were frozen in `5307c3b` before any result file existed; P4 as literally written
(≥ 80% of power-adequate splits firing) came in at 79.45% and is reported as refuted.
