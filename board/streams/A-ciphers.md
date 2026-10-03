# Stream A — Ciphers

*Standing brief. Orchestrator-owned; opened 2026-09-27 from `STATUS.md` and `board/log/`.*

## Before anything
- **Run the solution-status audit first.** Search `board/EXTERNAL_RESEARCH_INDEX.md` and the
  live literature before opening any cipher. Ormonde–Maltravers was withdrawn because it had
  been solved elsewhere the day before; Beale B3's leading result is now an external 2026
  *Cryptologia* paper. Reproduce and adjudicate; do not rediscover.

## Methods that transfer
- **Chi-square tails are exact.** A too-flat or too-lumpy statistic against a uniform null is
  an integer event; enumerate it (`ciphers/chinese-gold-bar-cipher/attempts/2026-09-25-tail-images-mechanism/src/exact_tail.py`).
  A 20,000-draw Monte Carlo cannot resolve anything below 5e-5.
- **Both tails speak.** Ask whether a distribution is suspiciously *flat*, not only far from
  uniform. And a p-value against uniform is P(data | uniform), never P(data | cipher).
- **Separate inherited from independent structure.** Hold composition fixed and re-deal
  (`inherit.py`, same folder). On the gold bars, a face "balanced" at P = 7.4e-6 was 100 %
  inherited (p = 0.598).
- **Short texts carry little.** `discovered/short-cipher-validation-bound/` bounds what any
  crib or readability test can establish on a short ciphertext; cite it before claiming one.
- **Calibrate every shuffle null at your own token count** (2026-10-02). A z-score scales with
  √length, so cut each genuine comparandum into non-overlapping blocks of *exactly* your target's
  length and report a percentile. Blitz: "0 of 402 genuine blocks at 470 tokens fall this low."
  The same blocks give the power curve free. **And a doublet deficit is what genuine ciphertext
  looks like** — Borg z = -47.3 — not a hoax signature; the anomalous document sits *near* Σpᵢ².
- **A ready-made genuine-ciphertext comparandum corpus exists**: `matthewdgreen/cipher_benchmark`
  (101 verified Copiale pages, 397 verified Borg pages, 155 DECODE/Gallica, 180 synthetic), fetch
  script in `ciphers/blitz-ciphers/attempts/2026-09-27-authenticity-internal-nulls/src/`. Audit it.
- **Read `board/PRACTICES-CIPHERTEXT.md` before any null in this stream.** New 2026-10-02: the
  ciphertext-statistics family split out of `PRACTICES.md` into its own annexe. Five rules, and it
  is not optional for this stream.

- **Build the external overlap map before claiming any result as the Hub's.** New 2026-10-03, and it
  is the generalised form of the solution-status audit above: agreement with another project is
  evidence only if you could have disagreed. The Linear A panel found corpus overlap effectively
  total, source overlap near-total and **test dependence total** with a parallel public campaign on
  the same corpus, via one shared third-party script. One row per proposition you intend to claim →
  published elsewhere / Hub result / cannot assess, with a reason per row, plus the shared inputs
  named (corpus edition, commentary, third-party code, and the instruction that chose your
  experiment). Acute for the folders with large public communities — Voynich, Beale, Kryptos — and
  for the archival packs, where this board has already lost one problem to an external solve.
  `board/log/2026-10-03-connection-a-shared-trigger-is-not-an-independent-replication.md`.
- **Charge the transcription-variant budget before counting anchors.** From the Byblos refuter: where
  a witness has multiple published readings, "the two strings share a sign" is a statement about
  which reading you chose. Charge it against the argument, not the transcriber — a variant selection
  that is the editor's own published choice is attributable to them.
- **`board/PRACTICES-ARCHIVAL.md` is not optional for the archival packs in this stream** — Crelly
  1648, Ormond–Anglesey 1663, CD 286, VORFYDCGT. Role separation before identity constraint, the
  OBSERVED / INFERRED / MISSING ledger, and the second-scan replicate for any measurement over a
  scanned edition.

## Live threads
- The **IRA `VORFYDCGT`** and **CD 286** folders are one lane: same office, period, cipher
  family and archival bottleneck (Kennedy Group 2).
- **Debosnys** is parked on archive scans (Brewster Memorial Library); two archive-free
  tasks remain in its handover.
- **Dorabella** is blocked on source resolution, not cryptanalysis.
- **Crelly 1648 and Ormond–Anglesey 1663 are one lane** — the seventeenth-century counterpart of the
  VORFYDCGT/CD 286 arrangement above: same period, cipher class, archival route (HMC calendars,
  archive.org, Irish historical journals) and the same unverified-solution-status question. Whoever
  takes one should pull the other's shelfmark while in the same catalogue. Both are Irish in subject
  but ranked here, because their suggested category is `ciphers`. The solution-status ledger **is**
  the session, not preliminary work: Ormonde–Maltravers was lost to an external solve published days
  before it was proposed. The short-cipher bound may decide both before any key is attempted.
  `board/log/2026-10-02-connection-the-two-irish-archival-cipher-packs-are-one-lane.md`.
