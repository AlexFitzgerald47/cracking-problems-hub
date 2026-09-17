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
