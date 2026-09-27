# 2026-09-27 – Reconciliation of unmerged local and remote research

## Baseline and decision

The integration baseline is `origin/main` at `0396dbf05a6e51e9c7239a63d2afb31221619f09`
(2026-09-25). It had no open pull requests and no active board claim at audit time. This
pass recovers missing, self-contained research artifacts without merging any stale branch
dashboard, status page, or historical checkout wholesale.

## Recovered into the canonical tree

| Source | Recovered scope | Classification |
|---|---|---|
| `origin/claude/busy-galileo-9cj9he` | Caligula 2026-09-22 *musculus* inventory | unique research record |
| `origin/claude/busy-galileo-aafjll` | Junius 2026-09-21 register correction | unique research record |
| `origin/claude/busy-galileo-wxsv88` | Dál Riata 2026-09-24 onomastic founder test | unique negative result |
| `origin/claude/frontier-problem-solving-2vji0y` | Voynich 2026-09-08 zodiac ordinal crib | unique research record |
| `origin/claude/frontier-problem-solving-b1gbnm` | Shakespeare 2026-09-08 period invariance | unique precursor record |
| `origin/claude/irish-problems-progress-o6q34y` | Annals offline eclipse engine, bootstrap and sources | reproducibility package |
| `origin/claude/new-dominic-problem-tvznaf` | VENONA BARON audit | unique problem package |
| `origin/claude/tom-holland-problem-1222zs` | Historia Augusta authorship package | unique problem package |
| `origin/cracker/moynagh-lough-ogham-2` | Moynagh readings comparison script | unique utility |

## Deliberate exclusions

- The older local primary and 2026-09-05 worktrees remain recovery sources only. Their 1641
  pipeline/output was not imported: current main records an access limitation, and the old
  history contains an embedded browser credential. No credential value is carried here.
- The 2026-09-08 orchestrator branch was not merged as a whole: its dated content is
  recovered from the individual source branches above, while its dashboard is stale.
- Older Caligula local raw files are superseded by the recovered full 2026-09-22 inventory.
- `origin/deal-room-prototype` is unrelated to this research hub. Landscape/discovery branches
  whose paths already match main are already-present work, not imports.

## Operating consequence

Use a fresh checkout of updated `main` for new work. Keep the three older checkouts untouched
until the owner decides on archival treatment; do not use them as integration bases.
