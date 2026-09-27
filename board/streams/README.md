# Stream briefs

One standing brief per stream. Owned by the orchestrator; read by every Breaker before
starting in that stream. A brief carries what spans the stream's files — methods that
transfer, traps that cost sessions, threads that are live — so that a session which
remembers nothing still inherits its sector.

A brief is **not** the ranking. The ranking changes every commit and lives in
`npm run draw`. A brief changes when the sector learns something.

| Stream | Brief | Files |
|---|---|---|
| A | [`A-ciphers.md`](A-ciphers.md) | `ciphers/` and cipher packs in `discovered/` |
| B | [`B-texts.md`](B-texts.md) | `historical-texts/` and script/language packs in `discovered/` |
| C | [`C-controversies.md`](C-controversies.md) | `historical-controversies/` and matching packs in `discovered/` |
| D | [`D-ireland.md`](D-ireland.md) | `ireland/` and Irish packs in `discovered/` |

Rules for the draw itself are in `_roles/README.md` under *The draw*.
