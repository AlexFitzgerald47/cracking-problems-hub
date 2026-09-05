# Five-Lane Discovery — Lane C: Manuscript reconstruction & fragment intelligence

**Run date:** 2026-09-05 repository clock  
**Role:** Finder lane, coordinated by orchestrator  
**Brief:** `_templates/DISCOVERY_BRIEF.md`  

This lane screened **20 candidate problems**. Ten survived into the global top-50 target board; ten remain reserves. A SELECT here means “worth a full problem pack / cracker claim,” not “already solved” and not “all source debt is cleared.”

## Candidate screen

| ID | Candidate | Score /20 | Verdict | First falsifiable move |
|---|---|---:|---|---|
| C1 | Cairo Geniza automatic join discovery | 20 | **SELECT** | Use 2025 MiDRASH automatic transcriptions plus image metadata to rank previously unknown joins; validate on known joins and expert-check top predictions. |
| C2 | Dunhuang real-fragment reassembly beyond synthetic patch pairs | 19 | **SELECT** | Take the 2025 handwriting matcher from benchmark-style pairs to cross-collection retrieval of actual unmatched fragments. |
| C3 | Oracle-bone fragment rejoining at archive scale | 19 | **SELECT** | Benchmark modern rejoin models on known joins, then search unmatched fragments with provenance and break-edge controls. |
| C4 | Oracle-bone undeciphered character candidate readings | 18 | **SELECT** | Use open deciphered/undeciphered glyph datasets and evolutionary graphs to produce ranked readings with held-out historical-form tests. |
| C5 | Dead Sea Scrolls scribal-hand network | 18 | **SELECT** | Extend writer identification from demonstration scrolls to a corpus-wide graph; validate clusters against known multi-scribe manuscripts and 14C. |
| C6 | Dead Sea Scrolls fragment rejoining with script + material constraints | 17 | **SELECT** | Combine handwriting, text continuation and physical edge evidence; require recovery of known joins before proposing new ones. |
| C7 | Khipu non-numeric structural code | 18 | **SELECT** | Use the Open Khipu Repository to test whether knot/color/cord structures carry recurring non-accounting categories beyond quantity. |
| C8 | Gāndhārī manuscript fragment/provenance joins | 16 | **SELECT** | Use the digital corpus, orthography and scribal features to rank fragments likely from the same original manuscript or scribe. |
| C9 | P.Oxy. 90: writing exercise or cryptogram? | 17 | **SELECT** | Formalise the British Library catalogue’s two live possibilities and compare symbol/sequence structure against writing-exercise and cipher null corpora. |
| C10 | Silk Road Sanskrit manuscript fragment reassembly | 15 | **SELECT** | Use digitised fragment imagery/transcriptions to cluster scribes/text continuations across dispersed collections. |
| C11 | Batak pustaha formula/source alignment | 13 | **RESERVE** | Strong archive target, but corpus normalisation is still a first-stage task. |
| C12 | Nsibidi corpus construction and sign concordance | 12 | **RESERVE** | High value, but dispersed colonial-era sources make corpus readiness uncertain. |
| C13 | Oxyrhynchus cross-collection fragment joins | 13 | **RESERVE** | Promising, but a reliable bulk image/transcription route should be established first. |
| C14 | Cairo Geniza scribal-hand clustering | 13 | **RESERVE** | Useful but secondary to the higher-value join task. |
| C15 | Dunhuang cross-language scribe identification | 12 | **RESERVE** | Potentially useful after cross-script handwriting comparability is demonstrated. |
| C16 | Dead Sea palaeographic dating vs radiocarbon | 13 | **RESERVE** | Good calibration task, but overlaps active specialist projects. |
| C17 | Oracle-bone periodisation from glyph evolution | 13 | **RESERVE** | Open data exists; novelty versus 2025–26 work must be checked carefully. |
| C18 | Khipu provenance/account cluster recovery | 13 | **RESERVE** | Good structural task but overlaps C7. |
| C19 | Papyri.info duplicate/parallel-text reconciliation | 12 | **RESERVE** | Data-cleaning value is clear; a sharper historical payoff is needed. |
| C20 | Palimpsest undertext OCR benchmark | 11 | **RESERVE** | Methodologically useful but not yet tied to one specific unresolved corpus. |

## Evidence anchors checked
- Cambridge Genizah Research Unit (July 2026), demonstrating a new join found through the 2025 **MiDRASH automatic transcriptions**: https://www.lib.cam.ac.uk/collections/departments/taylor-schechter-genizah-research-unit/fragment-month/fotm-2026/fragment-6
- Zheng et al., **Dunhuang manuscript fragment reassembly based on patch-level handwriting style recognition**, *npj Heritage Science* 13 (2025), 507: https://www.nature.com/articles/s40494-025-02078-y
- **Open-Oracle** (maintained July 2026), datasets/benchmarks for oracle-bone recognition, rejoining and decipherment: https://github.com/Yuliang-Liu/Open-Oracle
- EU CORDIS, **Hands that Wrote the Bible**, writer identification and digital palaeography for Dead Sea Scrolls: https://cordis.europa.eu/project/id/640497/reporting
- **Open Khipu Repository**, current open dataset (v2.1.0 in 2026; Zenodo/GitHub).
- Gāndhārī.org digital corpus of published Gāndhārī texts/manuscripts.
- British Library catalogue, Papyrus 761 / **P.Oxy. 90**, explicitly describing the last two lines as a “writing exercise or cryptogram”.
- International Dunhuang Programme / partner collections for dispersed Silk Road manuscripts.

Verification note: synthetic benchmark success is not counted as a historical discovery. Selected reassembly targets require recovery of known joins first and then real unmatched-fragment retrieval.

## Time-waster warnings
- Do not confuse an online search interface with bulk/programmatic access; establish export/API terms first.
- Do not infer openness from age. Re-check whether a newer paper has already done the proposed test.
- Do not promote a high-scoring fit without a null/control that matches corpus size, transcription noise and search budget.

## Domains not reached
- This lane was deliberately narrow. Adjacent ideas were left to the other four lanes to avoid collisions.
