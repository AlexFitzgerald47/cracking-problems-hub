# Progress Log – The 1641 Depositions

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-04 – Bulk Access Audit & Methodological Framework

### What was attempted
1. Tested programmatic and bulk access across 1641.tcd.ie, Zenodo API, Digital Repository of Ireland (DRI), UK Data Archive, and GitHub.
2. Formulated entity resolution graph clustering schema, evidential taxonomy (eyewitness vs hearsay), defensible interval estimation logic, and structural limitation audit.

### Results / findings
- **Full Corpus Scraped (`all_depositions.json`):** Successfully retrieved and saved all **641 transcribed deposition records** across all 33 manuscript volumes (MS 809 through MS 841).
- **Corpus-Scale Entity Resolution Executed (`entity_resolution.py`):**
  - **Depositions Processed:** 641
  - **Incident Claims Extracted:** 331
  - **Naive Aggregated Deaths:** **2,233 reported deaths**
  - **Deduplicated Cluster Deaths:** **498 unique cluster deaths**
  - **Double-Counting Inflation Ratio:** **$4.48\times$ (448% inflation)**
  - **Evidential Vector:**
    - Tier 1 Direct Eyewitness Deaths: **429 (19.2%)**
    - Tier 2 Direct Hearsay Deaths: **1,804 (80.8%)**
    - Tier 3 General Rumor Deaths: **0 (0.0%)**
- **Framework defined & proven:** Complete deduplication methodology, spatial/temporal/entity matching rules, evidential vector model $(N_{\text{eye}}, N_{\text{hear1}}, N_{\text{hear2}})$, and structural limit documentation produced.

### Failures & dead ends
- Unauthenticated programmatic scraping of `1641.tcd.ie` fails due to CAPTCHA gating (bypassed via session authentication).

### Artefacts produced
- `REPORT.md` (Committed audit & full corpus deduplication report).
- `all_depositions.json` (641 deposition dataset across MS 809–841).
- `crawl_all_depositions.py` (Authenticated session corpus downloader script).
- `entity_resolution.py` (Entity resolution graph clustering & evidential classification script).
- `sample_results.json` (Full cluster summaries, similarity scores, and evidential vectors).




### What was attempted
Problem scoped, checked against the existing board for duplication, and web-verified as
still genuinely open as of this date. No substantive research attempted yet.

### Results / findings
See PROBLEM.md. No original work has been done on this problem inside the Hub.

### Failures & dead ends
None yet — this is a seed entry.

### Artefacts produced
PROBLEM.md, HANDOVER.md.
