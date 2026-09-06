# Progress Log

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-05 – GPT-5.6 Sol starting session

### What was attempted

Started from the three primary London GRU cables in which BROWN/BRAUN occurs and built a role-aware constraint set before searching names. The specific objective was to avoid the easy but unjustified inference that BROWN must personally have been a Henry Hughes employee.

Then searched the pre-1940 Henry Hughes technical record for people and apparatus that match the 4 September description, and checked current web-accessible historical/archival references for candidate links to Soviet espionage.

### Results / findings

#### 1. BROWN has exactly three useful primary-message appearances in the recovered London GRU corpus

- **No. 798, 22 Jul 1940:** BROWN is part of clandestine-radio logistics. A flat with a W/T set is to be found for him; STENLI receives Soviet material through him; he is to be linked with MINISTR/another Soviet contact.
- **No. 876, 13 Aug 1940:** an Area Secretary of the Communist Party knows of a W/T set from BROWN. POULTRY-DEALER describes BROWN as devoted to the Soviet cause but talkative. BROWN is told to move to his old flat during a security rearrangement.
- **No. 976, 4 Sep 1940:** a report signed BROWN conveys Henry Hughes information about a horizontal echo-sounder / underwater-reflection instrument. VENONA commentary explicitly leaves BROWN unidentified.

This establishes a **network/handler profile** independently of the Henry Hughes clue.

#### 2. The key role ambiguity is real

No. 976 says the *details* were received direct from the Henry Hughes production line. It does **not** state that BROWN worked there. I am carrying three competing models:

- **H1 insider:** BROWN personally works at Henry Hughes and supplies the material.
- **H2 handler:** BROWN receives a report/material directly from a Henry Hughes insider and forwards it.
- **H3 CPGB collector:** BROWN is a trusted Communist intermediary whose local network contains the Henry Hughes source.

Any candidate search that assumes H1 from the start is liable to miss the actual person.

#### 3. The Henry Hughes source pool can be narrowed to a small acoustic/echo-sounder circle

The patent record is unusually informative.

- **US2350080A**, priority 26 Nov 1937, names **Donald Orr Sproule** and Henry Hughes & Son; it is a compressional-wave indicator designed for shipboard/echo-sounding use.
- **GB591533A**, filed 22 Mar 1939, names **D. O. Sproule, A. J. Hughes and Henry Hughes & Son** and describes directional sound-wave apparatus using a transmitting/receiving element and rotatable reflector.
- **US2076330A**, priority 18 Mar 1931, names **Albert Beaumont Wood, Frederick Daniel Smith and James Andrew McGeachy**, assigned to Henry Hughes & Son, and explicitly concerns measurement of distance by echo reception with ultrasonic/magnetostrictive apparatus.
- A 1954/55 US court decision records that Henry Hughes licensed rights under US2076330A on **17 Apr 1940**, while retaining the receiving/transmitting oscillator component. This is close in time to the September 1940 cable and confirms the echo-sounder technology was commercially/technically active then.

The 4 September cable's wording therefore maps to a defined technology family, not generic wartime factory work.

#### 4. Donald Orr Sproule is the strongest source-level lead found in this pass

Reasons:

- direct Henry Hughes engineer/inventor;
- Ilford/London location in patents;
- pre-1940 work specifically on echo-sounding/directional/compressional-wave equipment;
- Canadian background, independently described in a 1998 technical history;
- that same 1998 article says he was later forced to resign from Kelvin Hughes because of an **alleged association with Russian spies**.

However, the espionage sentence in that article does not show an immediately visible citation. It is therefore a **lead requiring primary verification**, not a basis for accusing or identifying Sproule as BROWN.

Crucially, no public evidence was found in this pass connecting Sproule to the Communist Party, clandestine W/T logistics, BROWN's flat, POULTRY-DEALER, or the Soviet network. On present evidence he may be more plausible as the **technical source behind No. 976** than as BROWN himself.

#### 5. An archival route for Sproule exists

A secondary index to the UK National Archives SOE personnel-file series lists **Donald Orr Sproule, born 26 May 1903**, within **HS 9/1401**. Search results also show the same HS 9/1401 bundle contains several nearby surnames and a separately catalogued Patricia Ann Sproule file.

This corrects an early search-index misread that suggested HS 9/1428. The current lead is **HS 9/1401**, but the exact sub-file and contents must still be verified from the National Archives catalogue/file before treating the SOE association as established.

#### 6. “No. 256” is not a useful personal identifier

The immediately preceding London GRU message ends **“No. 255 BARCh”**, while the BROWN report ends **“No. 256 BROWN.”** This strongly indicates 255/256 are sequential local message numbers, not BROWN's agent number. Do not spend future effort trying to map “256” to a personnel identifier.

### Candidate matrix after first pass

| Candidate / class | Henry Hughes / echo access | CP/Soviet-network evidence found | W/T/logistics evidence found | Current interpretation |
|---|---:|---:|---:|---|
| **Donald Orr Sproule** | Very high | Weak indirect later allegation only | None | Strongest **technical-source** lead; unproven as BROWN |
| **Arthur Joseph Hughes** | Very high | None | None | Technical-access control candidate; poor network fit so far |
| **Philip Francis Everitt** | High company/instrument access | None | None | Company technical candidate, weaker echo-specific match |
| **A. B. Wood / F. D. Smith / J. A. McGeachy** | High historical echo-tech relevance | None | None | Earlier patent circle; 1940 employment/access needs checking |
| **Unknown CPGB-linked Henry Hughes worker/contact** | Unknown-to-high | Model predicts yes | Model predicts yes/intermediary | Main class to discover if H2/H3 is correct |

### Failures & dead ends

- A “Braun” appearing in Vassiliev-notebook search results was traced to a **US/NKGB** context, not London GRU. Discarded.
- Literal-name searches for a person surnamed Brown are not evidence. A post-war Kelvin Hughes engineer named Tom Brown replaced Sproule, but there is currently no reason to connect his surname to the covername.
- Generic searches for Communist associations of the known Henry Hughes inventors produced no reliable hits.
- The National Archives public search index did not expose a clean individual Donald Orr Sproule catalogue result; only secondary indexing currently gives HS 9/1401. This is an archival verification debt.

### Artefacts produced

- `PROBLEM.md` — formal problem pack and success criteria.
- `analysis/constraint-ledger.md` — cable constraints, hypotheses, candidate tests and next archival queries.
- `HANDOVER.md` — next experiments ranked by expected information gain.

### References consulted

Primary / near-primary:
- Wilson Center, *London GRU – Moscow Center Cables*: https://www.wilsoncenter.org/sites/default/files/media/documents/article/Venona-London-GRU.pdf
- NSA/DoD, London No. 976, 4 Sep 1940: https://media.defense.gov/2021/Jul/22/2002809208/-1/-1/0/4SEP_BROWNS_REPORT.PDF
- US2350080A: https://patents.google.com/patent/US2350080A/en
- GB591533A: https://patents.google.com/patent/GB591533A/en
- US2076330A: https://patents.google.com/patent/US2076330A/en
- *National-Simplex-Bludworth, Inc. v. Prothero*, 130 F. Supp. 146: https://www.casemine.com/judgement/us/5e80becb4653d029117461d1

Secondary lead sources:
- Newman & Rozycki, “The History of Ultrasound,” *Surgical Clinics of North America* 78(2), 1998, 179–195; searchable copy: https://www.scribd.com/document/655882787/Newman-1998
- Secondary SOE personnel index indicating Donald Orr Sproule in HS 9/1401: https://gatopardoblog.wordpress.com/2019/07/11/sg-sz-lista-secreta-de-los-agentes-del-special-operations-executive-soe/
