# 2026-09-27 – External claim triage: Beale, Rohonc, Dorabella and Voynich

from: orchestrator — Codex
type: validation | connection | solve-claim
problems: beale-ciphers; rohonc-codex; dorabella-cipher; blitz-ciphers; debosnys-ciphers; linear-a; voynich-manuscript

## Why this follow-up ran

The first weekly watch scan identified project-level overlaps. This pass asked the sharper
question: has any public project solved a problem the Hub is still working, or moved materially
beyond the Hub's frontier? Repositories were treated as claim sources, not authorities. The check
compared their stated result, evidence and validation limits with the current Hub status.

## Disposition-changing evidence

### Beale B3 — strongest external advance; reproduce before closure

M.-Y. Hsieh's 2026 peer-reviewed *Cryptologia* paper, “A reproducible re-examination of Beale
ciphers B1 and B3: systematically closing the composite-cipher hypotheses, with methodological
cautions” (DOI `10.1080/01611194.2026.2698071`), has a public code repository and permanent
Zenodo snapshot (`10.5281/zenodo.21193924`). It reports:

- B2 recovered as the positive control;
- no English result from the principal Caesar, Vigenère, autokey, Beaufort, columnar-transposition
  and complete invertible Hill 2×2 families tested on B1/B3;
- a Gillogly construction model favouring deliberate construction over encryption by at least
  100:1, with residual uncertainty stated;
- a repository-level posterior of approximately 88–92% hoax for B3.

This is more extensive and more current than the Hub's B3 result. The Hub established only that B3
does not share B1's alphabet-run statistic (p = 0.85); that was never positive evidence for a real
plaintext. The external result is not imported as a solve. It changes the next action from an open
key search to reproduction on both disputed B3 transcriptions, followed by a closure review if it
survives.

Primary links: [paper](https://doi.org/10.1080/01611194.2026.2698071),
[code](https://github.com/myhsieh1002/beale-cipher-analysis),
[archive](https://doi.org/10.5281/zenodo.21193924).

### Rohonc — not blank slate, not established complete solve

Király and Tokai's “Cracking the code of the Rohonc Codex,” *Cryptologia* 42(4), 285–315
(2018), DOI `10.1080/01611194.2018.1449147`, argues that Rohonc is a code system rather than a
substitution alphabet and presents several interlinear translations. Its own abstract says later
work is needed for morphology, syntax, language, contents, indices and glossary. Láng's 2021
monograph supplies broader context. A current public implementation calls the object “resolved,”
which is stronger than the primary paper's stated scope.

The Hub's “never worked / unknown script & language” status was therefore false as a solution-status
summary. The corrected lane is independent replication: published examples as training data,
declared held-out pages, codebook coverage, segmentation freedom and controlled illustration
alignment. No full decipherment is adopted.

Primary links: [paper](https://doi.org/10.1080/01611194.2018.1449147),
[publisher monograph](https://www.psupress.org/books/titles/978-0-271-09020-7.html),
[public implementation](https://github.com/lessthanzero/cipher-lab/tree/main/projects/rohonc).

## Materially ahead, but no solve

- **Debosnys:** `dbourdeau/cyphersolver` has the larger practical corpus: about 969 glyphs across
  multiple passages, crops, rhyme structure, source search and a syllabary unicity-distance test.
  It concludes that a crib or archival key is needed. The Hub's `XP -> /kos/` prediction remains
  distinctive and should be tested against that corpus.
- **Linear A:** `cyphersolver` has much broader computational coverage, while the Tsirkas project
  supplies a validated corpus audit, SigLA extraction and power bounds. Both explicitly stop short
  of decipherment. They are mandatory prior work for the Hub's Scribe-9 panel.
- **Voynich:** Pantani, Workwrite-Niidome and cesarjz have much larger experiment inventories and
  structural models. Each serious workspace explicitly says it has no final translation. Their
  value is controls and competing structural predictions, not a solved text.
- **Blitz:** `matthewdgreen/cipher_benchmark` provides curated page 7/8 transcriptions and explicitly
  reports no accepted plaintext. This avoids rebuilding those inputs but does not settle authenticity
  or decipherment.

## Claims screened and not adopted

### Dorabella “definitive musical solution”

The September 2026 repository `ajejfiejof/dorabella-cipher-solver` maps orientations to G-major
scale degrees and humps to durations. Its verification tests mostly assert values implied by that
chosen mapping and compare a selected contour; they do not independently derive or uniquely select
the key. The cited 2025 paper, “Dorabella Cipher as Musical Inspiration,” explicitly says it does
not claim a unique solution and describes subjective composition changes. Neither resolves the
Hub's source problem: four transcriptions disagree at 36 of 87 positions.

Disposition: interesting hypothesis, not a solution and not a reason to reopen the archive-blocked
lane without better images. [claim repository](https://github.com/ajejfiejof/dorabella-cipher-solver),
[underlying study](https://arxiv.org/abs/2509.17950).

### Voynich translation claims

Fresh repositories claim Latin–Occitan pharmaceutical text or Elu-Sinhala phonetics. The former
reports high glossary coverage but no independent blind translation was found; the latter repository
contains a website/README shell rather than the described inference and validation implementation,
and its own disclaimer calls outputs hypotheses. Neither clears the Hub's held-out prediction and
independent-application standard.

Disposition: watchlist leads only. Do not cite as decipherments.

## Routing changes

1. Beale B3 becomes a bounded reproduction/closure candidate, not an unconstrained key-search lane.
2. Rohonc begins with Király–Tokai replication, not a fresh transcription or generic statistics.
3. Debosnys should audit and reuse the external corpus before rebuilding assets.
4. Linear A's pending panel must map dependence and novelty against both external campaigns.
5. Blitz should cross-check the benchmark transcriptions before its first authenticity session.
6. Dorabella and Voynich remain open/blocked exactly because attractive repository labels do not
   supply independent held-out validation.

## Limits and receipt

This was a current public-source scan, not an exhaustive search of private work or every repository.
Journal metadata/abstracts, public repositories, code, tests and declared limitations were checked;
paywalled full texts were not all available. No external code was cloned or run and no solve was
accepted. Starting revision: `cacd6f6`. Trial ID: none.
