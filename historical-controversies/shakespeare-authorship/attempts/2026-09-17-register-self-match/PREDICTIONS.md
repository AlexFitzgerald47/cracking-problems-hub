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
