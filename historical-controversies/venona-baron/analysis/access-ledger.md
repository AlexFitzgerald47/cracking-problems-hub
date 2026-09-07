# Access ledger — what could and could not be read, 2026-09-07

**Verification regime for this whole folder.** The opening session had **no working
`WebFetch` and no general outbound HTTP**. `WebFetch` returned `EGRESS_BLOCKED` for every
domain attempted (`wilsoncenter.org`, `nsa.gov`, `en.wikipedia.org`, `coldspur.com`,
`sunnycv.com`, `winstonchurchill.org`). Direct `curl` reached only GitHub hosts; it returned
`000`/403 for `media.defense.gov`, `archive.org`, `web.archive.org`, `cia.gov`,
`digitalarchive.wilsoncenter.org`, `en.wikipedia.org`. GitHub code search was available but
is out of scope for this session's repository permissions.

`WebSearch` worked. So every factual claim in this folder is at best **search-grade**:
established by a search engine's synthesis of indexed sources, not by reading a source.
This is the same regime discovery run 2 operated under, and `board/PRACTICES.md` is explicit
about what it is worth: *"Search depth is not reading depth, and the difference is invisible
in the output."*

Labels used throughout this folder:

| Label | Meaning |
|---|---|
| `[PRIMARY]` | Read in the primary document. **Nothing in this folder carries this label yet.** |
| `[SEARCH]` | Established via WebSearch synthesis of indexed sources; source named; not read |
| `[HUB]` | Inherited from an earlier Hub file, itself unverified here |
| `[INFERRED]` | This session's reasoning from the above |
| `[MISSING]` | Named, load-bearing, and not established |

## What the next session should fetch, in order of expected branch elimination

| # | Item | URL / reference | What it settles | Branches killed |
|---:|---|---|---|---|
| 1 | *Report from BARON*, 29 Jul 1941, 2 pp. | `nsa.gov/.../venona/dated/1941/29jul_baron_report.pdf`; mirror `archive.org/details/1941_29jul_baron_report` | Whether BARON reports **product** or **provenance**; subject matter; what the translator footnote says about identification | Decides H1 vs H3 outright; two pages |
| 2 | London No. 649, 3 Apr 1941 | Wilson Center aggregate PDF | Whether the ENIGMA reference is BARON's own words or an annotator's gloss; the "Military Intelligence" note; whether the content matches the Churchill/Cripps warning of the same date | Decides H1/H2/H3 and tests `analysis/churchill-date-collision.md` |
| 3 | Every other BARON occurrence in the London GRU corpus | Wilson Center aggregate PDF; NSA dated releases | The true size of the BARON trail. Two documents is a very thin base; the corpus may hold more | Sets the real evidence budget |
| 4 | West, *VENONA* (1999), pp. 67–69 | Book | **What West's identification actually rests on.** Traffic-internal evidence, or inference from Sedláček's known multi-service dealings? | Decides whether the standing hypothesis is evidence or attribution |
| 5 | TNA KV 2 file, Sedláček / Selzinger | Piece number `[MISSING]` | Sedláček's movements, British handling, and whether any Soviet contact is recorded for 1941 | Directly tests West |
| 6 | Hinsley vol. 1, Apr–Jun 1941 warnings | Book | The London provenance-knowledge circle in April 1941 — who could have known | Sizes the H1 candidate set |

## Note for whoever has fetch access

Items 1 and 2 are **two pages and one page** of released document. They are the entire
difference between this folder and a real attack on the problem. Do not start anywhere else.
