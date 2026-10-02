# Provenance manifest — Linear A validation v2 (prior-art / independence lane), 2026-10-02

Everything below was retrieved during this session. Nothing in `../2026-09-25/` was
modified; its SigLA witness files were read in place.

## Primary corpus witness (vendored here, `data/`)

| file | source | fetched | sha256 |
|---|---|---|---|
| `data/LinearAInscriptions.js` | `https://raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js` | 2026-10-02 | `9a14cc300201ac8ed07563c09b92142ab59de91a74e646b2e743ca6aeb695f5e` |

Upstream is GORILA (Godart–Olivier) via George Douros's tabulation, with John Younger's
commentary carried in the `translatedWords` field. 1,721 records, 1,599 distinct
documents after merging faces, 435 tablet records, 205 HT tablet faces = 137 HT tablets.

### The edition is not stable, and the claim never pinned a version

The 2026-09-25 session vendored the same upstream file
(`4da8e1f9693d30880ee505e56541fc189add70605bad88436c44a8e11a57764c`). **Twelve records
changed in the seven days between the two fetches**, among them one of the claim's two
headline arithmetic anchors:

```
HT34  old:  ... 'SA+MU+KU','100', 'PA3','70', 'KI-RO','37',  ...
HT34  new:  ... 'SA+MU+KU','100', 'PA3','70', 'KI-RO','30','[[7]]', ...
```

Also changed: HT36 (`'64'` → `'[[20]]','44'`), HT46b (`'6'` → `'2','[[4]]'`),
HT127a/b, HTWa1020, HTWa1021bis, HTWc3016, HTWc3017, HTWeWc3020, KH8, PKZg22.

The claimant's `analysis/kiro_residual_checks.py` asserts `100 - 70 == 30` for HT34. On
the edition available when that check was written the tablet read `KI-RO 37`; the `30`
came from Younger's erasure reading in the commentary, not from the transcription. The
check now agrees with the edition, by the edition having moved. No claimant file records
a corpus version, a commit or a hash.

## Second witness

SigLA (Salgarella & Castellan), `https://sigla.phis.me/document/{doc}/index-word.html`,
word views for HT 85a/85b/87/88/94a/94b/117a/117b/119/122a/122b, as vendored by the
2026-09-25 session in `../2026-09-25/data/`. Read-only.

## External prior-art workspace (not vendored; CC-licensed third-party research)

`dbourdeau/cyphersolver`, branch `main`, `targets/lineara/`. Retrieved 2026-10-02 over
`raw.githubusercontent.com` (the GitHub API is not reachable for this repo from this
session; only raw file reads succeeded).

| file | sha256 at fetch |
|---|---|
| `targets/lineara/NOTES.md` (43.4 KB) | `794608384c9bc0dc2be159513d064be2057226bed07af0171aa39998b8673cfc` |
| `targets/lineara/RESEARCH_REPORT.md` (8.1 KB) | `66c1f18c4fa26603ffac49efb1ca2cff711c91959fb8bcbbac4b01000348373b` |
| `targets/lineara/LEADS_REPORT.md` (233 KB) | `4bfff7da283f93253a154c53b5352e68dc14543b4628ca9730f6e6566417f516` |

Its own stated sources: mwenge/lineara.xyz (same file as above), SigLA (same database),
Younger's commentaries, GORILA, Salgarella 2022/2025, Steele 2023, Corazza et al. 2021,
Davis 2014, and `ChristosTsirkas/corpus-validation-for-undeciphered-scripts-linear-a`.
**Every one of those is also a source of the Hub's claim.** The overlap map is in
`external_overlap_map.csv`.

Its figures: 1,722 records acquired / 1,721 names; SigLA decoded to 802 documents and
5,144 attestations; 436 records marked Tablet. These match this session's counts of the
same upstream files to within the one duplicate-name record it reports preserving.

## Scripts in this directory

- `independence_checks.py` — P1 coverage, P2 label permutation, P3 prior-art ablation,
  P4 information ceiling, P5 coverage on the most favourable denominator. Offline once
  `data/` is present. Seed 20261002.
- `out.txt` — its full output as run on 2026-10-02.
