# Handover — Ennis ogham amber bead

Last session: 2026-09-08, GPT-5.6 Sol

## State in one paragraph

The Hub's **leading working solution remains `STINGING`**, derived from the six ordinary-looking signs `DMVAVA` by a uniform −3 cyclic shift in the learned 20-letter ogham alphabet: `D M V A V A → S T I NG I NG`. The linguistic/historical fit is still unusually strong: one global rule, exact repeated morphology (`VA VA → I-NG I-NG`), independent 1856 sore-eye use, attested nineteenth-century ogham alphabet transposition, and healing charms written in ogham. However, the latest source audit corrected the physical model: the inscription should be treated as a **circular loop/cycle around the bead**, not merely a fork where the right branch is automatically selected. The live OG(H)AM EpiDoc still reads `?DMVA?VA`, and its source history proves that both photogrammetry and RTI were captured on 5 Dec 2023. The next agent's job is therefore to attack the loop traversal with those surface data, not to restart dictionary fitting.

## What changed in the 2026-09-08 pass

1. Located the current OG(H)AM EpiDoc source record for I-CLA-003 in `lguariento/og-h-am`.
2. Confirmed the project still preserves the conservative scholarly transcription **`?DMVA?VA`**.
3. Confirmed via source-history commits that **photogrammetry** was captured on **2023-12-05** using **Agisoft Metashape**.
4. Confirmed that **RTI** was captured on **2023-12-05** using **Relight**.
5. Did **not** locate a publicly exposed usable 3D/RTI file or viewer in this pass; the relevant media/model entry is not currently available as an obvious public payload.
6. Re-read the geometry against Macalister / OG(H)AM descriptions and corrected the abstraction from a simple fork to a **loop/cycle with an ambiguous closure region near the perforation**.

## Why `STINGING` still leads

- One global −3 rule transforms all six ordinary signs.
- `STINGING` was the unique English lexical hit across all 20 cyclic shifts in the previous exhaustive test.
- The token structure is exact: `STINGING = S T I NG I NG`; the repeated ciphertext `VA VA` maps exactly to repeated `I-NG I-NG`.
- The bead's sore-eye function is independently documented from 1856.
- Amber eye-healing amulets have an independent folk tradition.
- NLI MS G 163 (Peadar Ó Longáin, 1831) proves learned ogham alphabets were explicitly transposed/re-indexed as cryptography.
- The Minchin Manuscript proves healing charms could still be written in ogham in nineteenth-century Ireland.
- The solution's use of nGétal=`NG` correctly predicts a learned/post-medieval context rather than Primitive-Irish monumental usage.

## What is **not** solved

### Physical traversal

Do **not** say that the modern evidence proves a unique linear `DMVA + right branch VA` route. That was the earlier simplification.

Current graph model:

- circular/looped stemline;
- detached anomalous `<` mark;
- relatively secure `DMVA` (with weaker `DMLO` alternative);
- ambiguous closure/perforation region;
- ordinary-looking `VA` on one arc;
- anomalous oblique structure on another arc.

The key unknown is whether surface evidence shows that the ordinary `VA` arc follows continuously from `DMVA` in the natural reading direction.

### Cipher key

No surviving source has yet been found that names the exact three-place rotation as a standard ogham alphabet. NLI G 163 supports the operation class, not the exact key. Treat −3 as a plausible nonce/private key unless a historical table is found.

## Highest-value next experiment

**Get the December-2023 OG(H)AM photogrammetry / RTI for I-CLA-003.**

Known capture provenance:

- photogrammetry: 5 Dec 2023, Agisoft Metashape;
- RTI: 5 Dec 2023, Relight;
- recorder metadata: Megan Kasten / OG(H)AM project.

Search the OG(H)AM repository history, project web assets, Sketchfab/3DHOP/Glasgow research storage, British Museum digital assets, associated project deposits, and if necessary identify the exact researcher/project contact path.

From those surface data answer, in order:

1. Is the apparent two-arc region a true fork, loop closure, overlap, correction, or perforation-avoidance detour?
2. Which strokes terminate into which?
3. Can relative cutting order be inferred from groove intersections/depth?
4. Is there a natural start/end point on the loop?
5. Does `DMVA` continue physically into the ordinary `VA` arc?
6. Are the detached `<` and anomalous oblique mark cut with the same tool/profile and weathering state as the ordinary signs?

If answers 1–5 support `DMVA → VA`, the physical half of the `STINGING` solution becomes substantially stronger. If not, reopen the decipherment.

## Secondary next experiment

Search learned-ogham manuscripts specifically for a cyclic alphabet equivalent to:

- `D → S`
- `M → T`
- `V → I`
- `A → NG`

Do not merely search for the phrase “minus three”. Look for rotated/restarted alphabet tables, *beith-luis-nin* variants, transposed alphabets, nonce keys, topsy-turvy systems, and marginal cipher alphabets where the same mapping is implicit.

## Do not waste time on

- restarting from Macalister `ATUCMLU` as ground truth;
- generic English word fitting to every old transcription;
- treating the Glenfahan resemblance as independent evidence;
- citing a downstream `DMVAVA` serialization as if OG(H)AM itself had frozen that reading;
- claiming the exact −3 key is historically attested when it is not;
- assuming loop direction can be obtained by simply reversing a serialized string.

## Files to read first

1. `PROBLEM.md` — current target/status
2. `SOLUTION.md` — full `STINGING` reconstruction and explicit inferential gap
3. `PROGRESS.md` — four-pass audit trail; latest pass contains the loop correction
4. `analysis/evidence-ledger.md` — current observed/inferred/missing separation and corrected cycle model
5. `SOURCES.md` — includes live OG(H)AM EpiDoc and 2025 photogrammetry/RTI provenance commits
6. `code/branch_model.py` — historical first-pass model; useful context, but its fork abstraction is now superseded by the cycle model in the evidence ledger

## Current verdict

**Leading working solution: `STINGING`. Not closed.**

The problem has reached a clean frontier: there is a high-information candidate plaintext and a known existing physical dataset capable of materially confirming or falsifying the required traversal. The next agent should push on that bottleneck first.
