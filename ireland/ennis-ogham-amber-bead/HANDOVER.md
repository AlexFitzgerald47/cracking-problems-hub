# Handover — Ennis ogham amber bead

Last session: 2026-09-08, GPT-5.6 Sol

## 2026-09-23 — orchestrator cross-reference: the validation panel is complete (additive; nothing below altered)

**Three verdicts, all PARTIAL. `HELD — awaiting human sign-off`. Not a solve, and not to be
written up as one anywhere.** Verdicts:
`board/log/2026-09-17-validation-ennis-stinging-v1.md`, `…-v2.md`, and
`board/log/2026-09-23-validation-ennis-stinging-v3-refuter.md`.

**What survived the refuter — say this first, because it is real.** Expanded twelvefold to
480 cycle-model combinations across three lexicons, the decipherment still yields **exactly
one English word and zero Irish words**. The refuter could not break the cryptographic core
and says so explicitly. This claim's problem has never been its arithmetic.

**Four things the next cracker session on this folder must do, none of which need new
evidence:**

1. **Replace the headline null figure.** "0.406 %, about 1 in 246" is the most favourable of
   **four** values now committed across `PROGRESS.md`, `analysis/stinging-candidate-2026-09-07.md`
   and `SOLUTION.md`, and it **does not reproduce** — the committed script returns a different
   figure on a current `cmudict` (drift, not arithmetic error). It is also frozen-path,
   English-only and conditional on the deletion. The defensible figure, by exact enumeration
   over all 64,000,000 six-sign sequences under the 12-reading cycle budget with an English ∪
   Irish lexicon, is **7.2 %, about one in fourteen** — and **31.5 %** charged for the affine
   family. Pin the lexicon version when you re-derive, or quote the TextBlob figure, which
   reproduces exactly.
2. **Stop carrying the "VA repeated" falsifier as the open kill test — it is discharged, and
   it resolved in the claim's favour.** The live OG(H)AM EpiDoc record decomposes to exactly
   one FEARN+AILM pair after the second `?`, so the apparatus phrase means "VA, repeated from
   DMVA", not `VAVA` on the branch. (`DMVAVAVA` yields nothing in any case.) One caveat: the
   GitHub API was gated for that session, so only the *current* edition was confirmed.
3. **Downgrade `SOLUTION.md` §5's "operation class attested / nonce key inferred" split.** The
   refuter read all 45 pages of Hayden & Stifter 2025 — the dossier's own cited source, which
   neither co-validator had read past the abstract. The attested nineteenth-century ogham
   ciphers (*ogam craobh*, *ogam coll*, *ogam consaine*) contain **no positional rotation**;
   the Minchin charms are plain ogham with no superimposed cipher; and the eye-charms are
   Irish *drochshúil* prayers to St Brigid under `ar x` headings — a comparator predicting
   specifically *against* a bare English participle. "Cryptic healing ogham" is this dossier's
   construction, not an attested genre.
4. **Record the error tolerance, which is zero.** None of the 12 sign-confusions the editors
   record *on this object* leave the reading standing, and 1 of 114 single-sign neighbours
   survives (`DNVAVA` → `SLINGING`).

**One methodological finding that belongs to the folder.** The zero-hit results at length 7
and 8 that two validators reported are the *expected* outcome under the null — eight-sign
English words are ~478× rarer in sign space than six-sign — so they are nearly uninformative.
The real finding is the reverse: **deleting two signs relocated the search to the length of
maximal false-positive density**, and no committed figure charges for that.

**The bottleneck is unchanged and it is physical.** All three validators say the same thing:
the captured 2023 photogrammetry/RTI, and a blind traversal audit that fixes the traversal
*before* any lexical search with the string budget declared in advance. Two sources remain
UNVERIFIED because `ogham.glasgow.ac.uk` is behind a site-wide captcha: both cited OG(H)AM
posts, and Macalister CIIC 53 at document level.

---

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
