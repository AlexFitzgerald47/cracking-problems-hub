# 2026-09-27 – External research watch scan

## Why this scan ran

The 2026-09-17 public landscape index was recovered from the earlier ChatGPT research thread
and confirmed merged through PR #8. This is the first recorded weekly follow-up under that
index's own cadence. It is a prior-work and overlap check, not validation of external claims.

## High-signal changes

### `dbourdeau/cyphersolver`

- Repository `main` was active through 2026-09-26 (`648309e85b8a`). Its latest structural
  commit moved **315 top-level target directories** under `targets/` (the commit message says
  314; the current tree enumerates 315).
- Five targets directly overlap current Hub campaigns: `beale`, `debosnys`, `goldbar`,
  `lineara`, and `voynich`. `ormonde` also overlaps the Hub's externally closed discovery pack.
- Its Debosnys directory includes images/crops and a long syllabary investigation; this may be
  useful source/transcription infrastructure and deserves an audit before the Hub spends another
  session rebuilding those assets.
- Its Linear A directory is a large parallel campaign using 1,722 records plus SigLA material.
  The pending Hub panel must treat it as prior work and map corpus/test dependence before making a
  novelty or independent-replication claim.
- Its gold-bar note is **stale relative to the Hub's 2026-09-25 photographic audit**: it still
  uses 263 letters and the earlier tail figure, whereas the Hub now has 261 letters and exact
  P = 1.2231e-11. Its categorical “not encryption” framing is stronger than the Hub's evidence,
  which establishes deliberate inventory balancing but does not separate every mechanism or
  settle authenticity.
- Its Beale B1 conclusion points in the same direction as the Hub's construction finding but
  comes from a different and partly incomplete scan. Agreement is a comparison target, not a
  second validator verdict.
- Its Voynich work is explicitly not a decipherment and is most valuable as a suite of competing
  structural controls.

Primary links: [repository](https://github.com/dbourdeau/cyphersolver),
[public case site](https://dbourdeau.github.io/cyphersolver/).

### `aaymeloglu/unsolved-ciphers`

- Active through 2026-09-23 (`2495c45e8b94`). Since the index snapshot it added or expanded
  Ferdinand 1634/1635–40, Moray 1568, Starhemberg 1758 and Vande Perre 1653 case files, plus
  shared transcription, alignment, segmentation, corpus and permutation-control tooling.
- No direct collision with a live Hub target was identified in this scan. The main value is its
  evidence-grading conventions and reproducible image/transcription pipeline.
- Treat its project-reported readings as leads until the cited manuscript image, key and control
  reproduce independently.

Primary link: [repository](https://github.com/aaymeloglu/unsolved-ciphers).

### Other weekly entries

- `matthewdgreen/decipher`: latest visible commit 2026-09-08; no newer target collision found.
- `matthewdgreen/cipher_benchmark`: latest visible commit 2026-07-20; no new change.
- `solveathome/platform`: active on 2026-09-27, but current changes concern collaboration UI,
  not a Hub target.
- `kevjenz/prize-problem-lab`: latest visible commit 2026-09-04.
- DECRYPT, Tomokiyo's unsolved list, Cipher Mysteries and solveathome.org all returned HTTP 200
  during the reachability check. Reachability does not prove their case lists are unchanged;
  Tomokiyo supplied a `Last-Modified` header dated 2026-09-27 and merits a case-level diff on the
  next cipher discovery pass.

## Routing consequence

1. Make the external index a mandatory first check for every cipher/script session.
2. Audit the external Debosnys assets before rebuilding a transcription.
3. Add the external Linear A campaign to the pending panel's novelty/dependence checklist.
4. Preserve the Hub's corrected gold-bar corpus as authoritative locally; do not import the
   external stale figures.
5. Keep external agreement separate from independent validation—shared public sources and similar
   agent methods can produce correlated conclusions.

No external solve or target disposition was adopted by this scan.
