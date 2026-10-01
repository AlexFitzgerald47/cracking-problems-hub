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

## Live threads
- The **IRA `VORFYDCGT`** and **CD 286** folders are one lane: same office, period, cipher
  family and archival bottleneck (Kennedy Group 2).
- **Debosnys** is parked on archive scans (Brewster Memorial Library); two archive-free
  tasks remain in its handover.
- **Dorabella** is blocked on source resolution, not cryptanalysis.
