# Frozen predictions

Written and committed **before** any distance or accuracy in this attempt was
computed. The corpus build (`src/build_corpus.py`) had been run and its
composition inspected; no Delta, no distance and no accuracy had been.

The reasoning behind these is the Junius result of 2026-09-17
(`board/log/2026-09-17-register-exceeds-author-signal.md`): on 18th-century
political letters versus private correspondence, the register gap was *larger*
than the author signal. This attempt asks whether early modern drama versus
non-dramatic prose and verse behaves the same way. If it does, the stylometric
arguments in the Shakespeare authorship debate - which almost all cross that gap -
are uninterpretable rather than merely weak.

Panel: 8 authors attested in both registers (Chapman, Dekker, Greene, Heywood,
Jonson, Lyly, Marston, Middleton). Chance attribution rate on this panel = 0.125.
All documents are 2,000-word chunks in both registers.

| # | Prediction | Fails if |
|---|---|---|
| **P1** | Mean same-author **cross-register** Delta will exceed mean different-author **same-register** (drama-drama) Delta. | Cross-register self-distance lands below the different-author same-register distance. |
| **P2** | Cross-register attribution (author centroids trained on play chunks, non-dramatic chunks attributed) will score **<= 0.25**, i.e. no better than twice chance. | Accuracy >= 0.30. |
| **P3** | Within-register attribution (play chunks attributed to play centroids, same 8-author panel, leave-one-work-out) will score **>= 0.70**. | Accuracy < 0.70. This is the positive control: if it fails, the pipeline is broken and P1/P2 mean nothing. |
| **P4** | For a **majority** of the 8 authors, the nearest play-centroid to that author's own non-dramatic chunks will **not** be himself. | 5 or more of 8 authors self-match. |
| **P5** | Pipeline control: the Delta distance between the **same play** extracted from engdracor and from its own TCP source will be **< 25%** of the mean different-author same-register distance. | >= 25%, in which case the two corpora are not interchangeable and the whole design is contaminated. |
| **P6** | Held-out arm. The register gap will be derived on the four authors with the most non-dramatic material (Greene, Heywood, Dekker, Lyly) and then used to predict cross-register accuracy on the four with the least (Chapman, Jonson, Marston, Middleton). Predicted held-out accuracy: **<= 0.25**. | Held-out accuracy > 0.25. |

## Not predicted, and to be reported whatever it says

- The permutation null for every distance statistic above.
- Where the test has **no power**: Jonson contributes only 8 non-dramatic chunks
  and Marston 11, and a per-author verdict on those is close to meaningless. Any
  per-author claim must carry its n.
- The TCP `<gap>` rate per author and register. TCP marks illegible passages with
  `<gap>`; if that rate differs systematically by register it is a transcription
  confound riding alongside the register effect, and it must be reported the way
  the Junius session reported long-s damage.

---

# Frozen predictions, round 2 — the attractor

Written after the 8-author panel was run and after `src/proseness.py` was run,
and **before** the 27-author panel was attempted. The 19 dramatists outside the
original panel have played no part in anything above.

The 8-author result showed that 59.4% of all non-dramatic chunks were attributed
to Lyly, against 7.0% of drama chunks, and that Lyly's apparently perfect
cross-register self-match (1.000) is an artefact of his being that sink. The
proposed mechanism is that Delta across the register gap is attributing by
**register**, not by author: every author's prose lands on whichever dramatist's
plays are physically most prose-like. Lyly's plays are mannered prose comedies
and he is the least verse-heavy dramatist in the corpus by a wide margin
(11.4 verse lines per 1,000 words; next is Shadwell at 17.8).

If that mechanism is right, it makes predictions about 19 authors never used to
derive it.

| # | Prediction | Fails if |
|---|---|---|
| **P7** | When the panel is widened from 8 to all 27 dramatists, the sink absorbing the largest share of the 943 non-dramatic chunks will be one of the three lowest-verse-density authors — **Lyly, Shadwell or D'Urfey**. | The top absorber is any of the other 24. |
| **P8** | Those three together will absorb a **majority (>50%)** of all 943 non-dramatic chunks, though 24 other dramatists are on offer. | They absorb 50% or less. |
| **P9** | Shadwell and D'Urfey, who wrote in the 1670s–1690s, will between them absorb **more than 10%** of the non-dramatic chunks — nearly all of which were written 1580–1640, before either man was born. Period cannot explain this; only register can. | They absorb 10% or less. |
| **P10** | Across all 27 dramatists, Spearman rank correlation between verse-line density and share of non-dramatic chunks absorbed will be **negative and below −0.45**. | Correlation is above −0.45. |
| **P11** | Cross-register macro accuracy on the 27-author panel will fall **below** the 0.337 measured on the 8-author panel, and below 0.20. | Macro accuracy >= 0.20. |

P9 is the decisive one. A dramatist who died in 1606 and a dramatist born in
1653 cannot both be stylistic neighbours of the same Elizabethan pamphlet for any
reason connected to authorship.

---

# Frozen predictions, round 3 — does the bias transfer?

Round 2 failed, and the failure is reported as a failure in `RESULTS.md`. Verse
density does not predict absorption at all (Spearman +0.039), and Shadwell and
D'Urfey — the two Restoration prose-comedy writers whose plays are physically the
least verse-like after Lyly's — absorbed **0.0%** of the non-dramatic chunks. The
prose-ness mechanism is dead.

What survives is the observation itself: on the 27-author panel, 41.0% of
non-dramatic chunks go to Lyly, 18.6% to Peele, 11.1% to Glapthorne and 11.0% to
Chapman, against a chance rate of 3.7%; fourteen of the twenty-seven dramatists
absorb nothing at all. Exploratory correlates of absorption are mean play year
(−0.530), number of training chunks (−0.438) and centroid L1 norm (+0.611). Those
three are entangled with one another and n = 27 authors cannot separate them, so
no mechanism is claimed here.

The round-3 prediction deliberately does **not** depend on which mechanism is
right. It asks only whether the bias is a property of the play centroids rather
than of the particular texts being attributed. If it is, then a completely
different body of out-of-register text should be captured by the same authors in
the same order.

The held-out body is the **19 civic pageants, royal entries and Lord Mayor's
Shows** excluded by `PAGEANTS` in `src/build_corpus.py`. They have been extracted,
classified and set aside, and no distance or attribution has ever been computed on
them.

| # | Prediction | Fails if |
|---|---|---|
| **P12** | Lyly will again be the single largest absorber of pageant chunks on the 27-author panel. | Anyone else is top. |
| **P13** | Spearman rank correlation between the per-author non-dramatic absorption profile and the per-author pageant absorption profile, across all 27 dramatists, will be **> +0.60**. | <= +0.60. |
| **P14** | A majority of the 27 dramatists will absorb **zero** pageant chunks, as 14 of 27 did for the non-dramatic chunks. | Fewer than 14 authors absorb zero. |
| **P15** | Middleton and Heywood — who between them wrote 12 of the 19 held-out pageants — will each be attributed **fewer than 25%** of their own pageant chunks. | Either is at or above 25%. |

P15 is the one that matters for the authorship debate. These are civic pageants of
known, undisputed authorship, by dramatists with 14 and 20 surviving plays
respectively in the training set. If the method cannot return their own pageants
to them, its verdict on a candidate with no surviving plays at all is not evidence.
