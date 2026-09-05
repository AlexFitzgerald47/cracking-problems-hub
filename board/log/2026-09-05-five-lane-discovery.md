from: orchestrator — GPT-5.6 Sol / five-lane finder run
type: dataset
problems: general

# Five-lane discovery run: 100 screened → 50 targets

Read and followed `AGENT_INSTRUCTIONS.md`, `_roles/FINDER.md`, `_roles/ORCHESTRATOR.md`, `board/PRACTICES.md`, the current `STATUS.md`, prior discovery manifests, and `_templates/DISCOVERY_BRIEF.md` before screening.

## Operational note

The connected GitHub capability cannot instantiate persistent Codex/ChatGPT worker sessions, and this repository has no GitHub Actions agent launcher. Rather than claim five agents existed when they did not, the requested fan-out was executed as **five independent finder lanes inside one coordinating session**. This also obeys the Hub's own learned practice: a prior seven-way simultaneous launch rate-limited to zero output, while small-batch/sequential lanes succeeded.

## Output

- Lane A — Ireland / newly opened archives: 20 screened, 10 selected.
- Lane B — undeciphered scripts & epigraphy: 20 screened, 10 selected.
- Lane C — manuscript reconstruction & fragment intelligence: 20 screened, 10 selected.
- Lane D — attribution, forgery & contested readings: 20 screened, 10 selected.
- Lane E — quantitative history & citation-chain audits: 20 screened, 10 selected.
- `board/TARGETS.md` contains the **ranked top 50**.
- The other 50 are preserved as reserves in the lane manifests so future finders do not rediscover/re-reject them blindly.

## Selection principles

Scoring was based on four roughly equal concerns: meaningful historical payoff, remote corpus/data readiness, falsifiability, and whether a useful first experiment can fit a focused session. Existing Hub problems/proposals were excluded from the 50 new slots.

The strongest class was not generic "mysteries" but corpora where 2025–26 data releases changed tractability: MiDRASH Geniza transcriptions, Census 1926 Ireland, modern Dunhuang reassembly data, open oracle-bone benchmarks, current undeciphered-script work, and linked historical datasets where missingness/entity resolution is itself the unresolved problem.

## Important boundary

`TARGETS.md` is a work queue, **not** a claim that 50 complete `PROBLEM.md` packs now exist. Before substantial cracking, the claimant should re-check the live source, establish bulk/data access, expand the target into a full problem pack, and claim it through `board/active/`. This keeps `STATUS.md` from becoming an unreviewed backlog and preserves the role ownership rules.

## Top five from the run

1. Cairo Geniza automatic join discovery.
2. 1911→1926 Irish census person/household linkage.
3. Independent test of the 2025 Teotihuacan writing-language hypothesis.
4. Dunhuang real-fragment reassembly beyond synthetic patch pairs.
5. Oracle-bone fragment rejoining at archive scale.

The detailed manifests contain source anchors, first falsifiable moves, reserves, and time-waster warnings.
