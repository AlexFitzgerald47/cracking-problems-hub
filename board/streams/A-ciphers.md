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
