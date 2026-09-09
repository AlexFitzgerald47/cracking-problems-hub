# Evidence ledger — Ennis amber bead

Last updated: 2026-09-08, GPT-5.6 Sol

## Witnesses kept separate

| Witness | Object access | Reported reading / observation | Evidential role |
|---|---|---|---|
| 1856 *Proceedings and Papers* | contemporary woodcut derived from a lithograph | no interpretation attempted | earliest published object witness located; provenance and amulet tradition |
| Westropp 1911 | secondary antiquarian account | Ennis `LMCBDV`; Fahan `LMCBTM` | **conflicted assignment**; likely swaps the two comparanda |
| Arntz, *Das Ogom* | secondary epigraphic discussion | Ennis `MTBCML`; Glenfahan `LMCBDV` | preserves pre-1945 reading and Marstrander cryptic-ogham hypothesis |
| Macalister 1945 CIIC 53 | corpus description | `ATUCMLU` in opposite direction; stemline described as encircling/running around bead | inherited reading weak at anomalous signs; useful independent witness that geometry is circular |
| OG(H)AM Dec 2023 examination / Jan 2024 report | direct modern inspection and photographs | `?DMVA?VA`; core `DMVA` or `DMLO`; initial `<` not known ogham; ambiguous closure/split region | highest-weight published remote examination |
| OG(H)AM live EpiDoc I-CLA-003 | current project source record | conservative `?DMVA?VA`; records 2023 photogrammetry + RTI capture | highest-weight current digital source-control witness |

## OBSERVED / INFERRED / MISSING

### OBSERVED from the modern specialist record

- Perforated amber object, about 2.1 cm diameter.
- A cut stemline runs around the object and is best modelled geometrically as a **loop/cycle** rather than assumed to be a straight line.
- A detached `<`-like shape does not meet the stemline and does not match a known ogham character.
- A relatively clear run can be read `DMVA`, with `DMLO` retained as an alternative.
- Near the perforation / closure region the stem geometry becomes ambiguous.
- One arc appears to carry ordinary `VA`; the final A is short and X-like.
- Another nearby arc/structure ends with an anomalous oblique stroke.
- OG(H)AM captured **photogrammetry on 2023-12-05 using Agisoft Metashape**.
- OG(H)AM captured **RTI on 2023-12-05 using Relight**.
- The live OG(H)AM source record remains conservatively transcribed as `?DMVA?VA`.

### INFERRED, but not secure

- The ambiguous region may reflect avoidance of the perforation.
- The two apparent arcs may represent a disturbed or overlapping **loop closure**, not a true fork.
- The ordinary-looking `VA` may be the intended continuation after `DMVA`, but that traversal has not been established from surface data.
- The anomalous arc may be structural, corrective, delimiter-like, aborted, or phonetic.
- The detached `<` may be non-phonetic.
- The amuletic use recorded in the nineteenth century may preserve an older function of the object, but it does not date the inscription.

### MISSING

- Public access to the raw photogrammetry / RTI / 3D surface products known to have been captured.
- Tool-profile and intersection evidence showing cutting order at the ambiguous closure.
- A physically justified start point and traversal direction for the loop.
- Secure sign identities for the two anomalous structures.
- A secure date for bead manufacture or inscription.
- An independently attested historical alphabet table matching the proposed −3 rotation.

## Corrected structural model

The first session treated the geometry as a branch budget. That was useful defensively, but the stronger current abstraction is a **cycle graph**.

Minimal graph components:

1. loop/circular stemline around bead;
2. detached anomalous `<` mark;
3. ordinary-sign run `DMVA` or weaker `DMLO`;
4. ambiguous closure/perforation region;
5. ordinary-looking `VA` on one arc;
6. anomalous oblique structure on another arc.

The key question is no longer simply “which fork branch do we choose?” It is:

> **What is the natural ordered traversal of the circular inscription, and does surface evidence show that the `VA` arc is continuous with `DMVA` in that traversal?**

Do not reverse a serialized string mechanically. Direction must be recomputed from the actual side/count geometry of strokes around the loop.

## Historical hypothesis audit

### H1 — Macalister's `ATUCMLU`

Fails as a frozen transcription. Two load-bearing `U` identifications are precisely the anomalous marks for which Macalister admitted little justification. The 2023 inspection instead describes one as detached/non-ogham and the other as part of an ambiguous terminal/closure structure. `ATUCMLU` remains a historical decoding branch, not observed ground truth.

### H2 — Ennis and Glenfahan carry the same cryptic/magical consonant skeleton

Historically testable form: older Ennis `MTBCML`, reversed to `LMCBTM`, resembles Glenfahan `LMCBDV`; Marstrander therefore proposed the same *rúnogam* and vowel insertion.

Result: **not reproduced against the best modern Ennis transcription**. The modern examination yields a materially different sign sequence/topology. The resemblance was contingent on an older reading; it is not an independent semantic fact about the bead.

### H3 — Westropp provides independent support for Ennis=`LMCBDV`

Rejected as currently stated. Westropp's account conflicts with Arntz, Macalister's corpus tradition and the machine-readable modern assignment of Glenfahan `LMCBDV`. Treat as a probable attribution/transmission swap until the original publication is adjudicated.

### H4 — `DMVAVA` → `STINGING` by uniform −3 rotation

**Status: strongest working solution, not physically closed.**

Support:

- six ordinary signs `D M V A V A` produce `S T I NG I NG` under one global −3 shift in the learned 20-letter ogham order;
- repeated `VA VA` maps exactly to repeated `I-NG I-NG`;
- `STINGING` was the unique English lexical hit among the 20 cyclic shifts tested;
- the bead's sore-eye use is independently documented;
- learned ogham alphabet transposition and healing-charms-in-ogham are historically attested in nineteenth-century Ireland.

Residual problems:

- live OG(H)AM transcription remains `?DMVA?VA`, not `DMVAVA`;
- no source has yet supplied the exact −3 key as an attested named alphabet;
- the loop traversal connecting `DMVA` to the ordinary `VA` arc is not yet proven from the captured surface data.

## Corpus sanity check

The OG(H)AM data-v1 readings file contains inherited Ennis `ATUCMLU` and Glenfahan `LMCBDV` (plus variant `LBMCBDV`). This validates that the famous inherited strings belong to different corpus objects. It is not linguistic evidence against the modern reading because data-v1 predates the December-2023 re-examination.

## Current frontier finding

The most important new fact is operational: **the decisive physical evidence is known to exist**. OG(H)AM's source history records both photogrammetry and RTI capture of I-CLA-003 on 5 December 2023.

The next serious agent should spend effort obtaining or locating those surface products, not performing more dictionary search. The intended test is to resolve:

- whether the apparent two-arc region is a loop closure, correction, overlap or true fork;
- which strokes physically intersect / terminate;
- cutting order;
- whether `DMVA` and the ordinary `VA` arc form one continuous directed path;
- whether the detached `<` and anomalous oblique structure belong to the same carving episode.

If that evidence validates `DMVA → VA`, the physical half of `STINGING` becomes substantially stronger. If it does not, reopen the decipherment.
