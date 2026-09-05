# Five-Lane Discovery — Lane E: Quantitative history & citation-chain audits

**Run date:** 2026-09-05 repository clock  
**Role:** Finder lane, coordinated by orchestrator  
**Brief:** `_templates/DISCOVERY_BRIEF.md`  

This lane screened **20 candidate problems**. Ten survived into the global top-50 target board; ten remain reserves. A SELECT here means “worth a full problem pack / cracker claim,” not “already solved” and not “all source debt is cleared.”

## Candidate screen

| ID | Candidate | Score /20 | Verdict | First falsifiable move |
|---|---|---:|---|---|
| E1 | Domesday population multiplier: recover uncertainty instead of one number | 18 | **SELECT** | Re-estimate population with explicit household-size, omission and urban assumptions; publish distributions rather than a point estimate. |
| E2 | McEvedy–Jones historical population ‘clone’ audit | 18 | **SELECT** | Trace modern datasets/results back to 1978 guesses and quantify how often cloned estimates masquerade as independent evidence. |
| E3 | SlaveVoyages missing-voyage estimator sensitivity | 17 | **SELECT** | Reproduce regional/time estimates under alternate missingness models; identify cells where published totals are prior-driven. |
| E4 | British slave-compensation wealth transmission via census/probate linkage | 17 | **SELECT** | Link LBS beneficiaries into later census/probate records and quantify uncertainty in intergenerational transmission claims. |
| E5 | Jamaica slave registers: longitudinal person linkage, 1817–1832 | 18 | **SELECT** | Use the Valuable Lives source series to link individuals across six censuses and measure births, deaths, transfers and family separation with match uncertainty. |
| E6 | Scottish witch-trial outcome missingness and prosecution network | 16 | **SELECT** | Use the open Survey database to separate accused/tried/executed and model regional investigator/judge networks plus missing outcomes. |
| E7 | Roman/Mediterranean shipwreck counts: correct discovery bias before economic inference | 17 | **SELECT** | Model depth, coast, survey technology and publication-era detection effects in the OxREP wreck series before reading counts as trade volume. |
| E8 | Ancient coin-hoard discovery bias in Nomisma-linked datasets | 16 | **SELECT** | Estimate geographic/period collection bias and uncertainty before using hoard counts to infer circulation or crisis. |
| E9 | Old Bailey long-run violence rates: denominator and repeat-person audit | 16 | **SELECT** | Entity-link defendants/victims and propagate population-estimate uncertainty into claimed homicide trends. |
| E10 | Cross-dataset slavery entity resolution | 17 | **SELECT** | Link people/estates/voyages across SlaveVoyages, LBS and other open linked datasets; quantify duplicates and false merges before aggregate inference. |
| E11 | Coin die-link mint-output estimator calibration | 13 | **RESERVE** | Strong method problem but needs a corpus with ground-truth production controls. |
| E12 | Roman price-series citation-chain audit | 12 | **RESERVE** | Promising but requires a tightly defined published series. |
| E13 | Medieval poll-tax population multiplier | 13 | **RESERVE** | Good companion to E1; lower incremental value. |
| E14 | Premodern homicide-rate denominator audit | 13 | **RESERVE** | High methodological value but overlaps E9. |
| E15 | Ancient shipwreck cargo-composition missingness | 12 | **RESERVE** | Useful second-stage question after discovery-bias correction. |
| E16 | European witch-trial accused→executed multiplier | 13 | **RESERVE** | Cross-country comparability is currently the main barrier. |
| E17 | Slave-register vital-rate reconstruction | 13 | **RESERVE** | Valuable but overlaps the richer person-linkage target E5. |
| E18 | Domesday unidentified-place geolocation | 12 | **RESERVE** | Hundreds remain uncertain, but impact is narrower than E1. |
| E19 | Coin-hoard closing-date uncertainty propagation | 12 | **RESERVE** | Good technical follow-up to E8. |
| E20 | Historical city-population estimate clone audit | 13 | **RESERVE** | Likely fertile but needs one canonical dataset/claim chain selected first. |

## Evidence anchors checked
- Timothy W. Guinnane, **We Do Not Know the Population of Every Country in the World for the Past Two Thousand Years**, *Journal of Economic History* (2023): https://www.cambridge.org/core/journals/journal-of-economic-history/article/we-do-not-know-the-population-of-every-country-in-the-world-for-the-past-two-thousand-years/D747DDC6E499C799B0471DBE33FEB0BB
- Domesday population literature and the Hull Domesday Project; modern work still stresses household multipliers, omissions and network mismeasurement.
- **SlaveVoyages** estimates/database, continuously revised: https://www.slavevoyages.org/
- UCL **Legacies of British Slavery** database: https://www.ucl.ac.uk/lbs/
- UCL **Valuable Lives** project, linking six Jamaica slave-register censuses (1817–1832): https://www.ucl.ac.uk/social-historical-sciences/history/research/research-projects-and-centres/centre-study-legacies-british-slavery-cslbs/cslbs-projects-and-partners/valuable-lives-black-unfreedom-and-collapse-slavery-jamaica
- University of Edinburgh, **Survey of Scottish Witchcraft 1563–1736**, downloadable database: https://doi.org/10.7488/ds/100
- Oxford Roman Economy Project, **Shipwrecks Database**: https://oxrep.web.ox.ac.uk/shipwrecks-database
- **Nomisma.org** open linked data, hoards, coins and SPARQL/API access: https://nomisma.org/
- **Old Bailey Online**, machine-readable proceedings corpus: https://www.oldbaileyonline.org/

Verification note: these targets are about correcting inference under missingness/linkage/measurement error, not merely making a new chart from an old database.

## Time-waster warnings
- Reproduce published totals before perturbing assumptions; otherwise a disagreement may just be an implementation bug.
- Treat duplicated/linked historical records as a latent-variable problem, not exact-string deduplication.
- Never interpret discovery counts as underlying event counts until detection probability is modelled.

## Domains not reached
- This lane was deliberately narrow. Adjacent ideas were left to the other four lanes to avoid collisions.
