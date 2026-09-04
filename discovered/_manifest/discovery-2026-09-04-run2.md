# Discovery Run 2 – 2026-09-04

Ten proposals, in the three lanes the previous run's manifest named as its own gaps.

## How this batch was produced

Three researcher subagents, one lane each, run in **two small batches** (lanes 1 and 2
together, then lane 3) rather than as a single fan-out. This was deliberate: the previous
run launched seven lanes simultaneously and all seven died on a rate limit within seconds,
producing nothing. Batching worked — all three lanes returned full reports.

Researchers drafted candidates and reported sources. **No candidate was accepted on a
researcher's word.** The coordinator independently re-checked every load-bearing citation
before anything was written to disk, and the proposals record what survived that check and
what did not.

## Verification standard actually achieved — read this before trusting anything here

**`WebFetch` was blocked by network egress policy for the entire run**, for the coordinator
as well as all three researchers. Every attempted fetch returned `EGRESS_BLOCKED`, across
academic publishers, university sites, national archives and general reference sites alike.

`WebSearch` did work, and returns substantive extracted content — abstracts, author lists,
volume and issue numbers, pagination, DOIs. Verification was therefore carried out against
**independent search-index bibliographic records and abstracts, not by reading full texts.**

This is a weaker standard than `_templates/DISCOVERY_BRIEF.md` assumes, and it is stated
plainly here and in every folder rather than smoothed over. What it can establish: that a
paper exists, by whom, where, when, and roughly what it argues. What it cannot: whether the
argument is correctly characterised. Every `PROBLEM.md` marks claims *verified* or
*unverified* individually, and each `HANDOVER.md` carries the outstanding verification debt
forward.

The brief's rule was still enforced in the form that matters: **citations that could not be
independently confirmed were flagged in place or dropped, and candidates were tested for
whether the problem is genuinely still open.**

### Corrections the verification pass caught

- **Blum (2026)** was proposed as single-authored evidence that parish-level Famine
  mortality is open. It is **Blum, Colvin and McLaughlin**, *Economic History Review* 79:1
  (2026), 189–220 — and it is an anthropometric study of scarring and selection. It shows
  Famine demography is actively worked; it is **not** evidence about parish-level mortality
  and the folder says so.
- **R. J. Hunter** confirmed as author of *Men and Arms: The Ulster Settlers, c. 1630*,
  which the researcher had left unverified.
- **Urcid (2001)** confirmed at **338 figures and 54 tables**, not the ~1,200 line drawings
  reported. The discrepancy is recorded in the folder rather than resolved by guessing.
- **MSPC size** is reported inconsistently across sources (~285,000 files vs "up to
  350,000", released in phased tranches). No single figure was adopted; the disagreement is
  recorded as a scoping hazard.
- **Jedwab / Johnson / Koyama** — the 38.75% mean is confirmed, but these authors have
  several overlapping Black Death papers and *which one carries the figure was not
  established*. Recorded as an open citation question, which is a small live instance of
  the exact failure mode that problem studies.

## Proposals in this batch

### Lane 1 — Early modern and modern Ireland
The previous run produced nothing here and the `ireland/` category was weighted entirely to
the early medieval period. Four proposals, spanning plantation to revolution.

| Slug | Description | Category | Difficulty / tractability |
|------|-------------|----------|---------------------------|
| `cromwellian-transplantation-compliance` | How many adjudged transplantable actually went to Connacht? The certificates that would settle it burned in 1922 | ireland | High / moderate-good — adjacent corpus digitised, certificate evidence must be reconstructed |
| `hearth-tax-population-reconstruction` | The multiplier under every pre-census Irish population figure; Dickson–Ó Gráda–Daultrey (1982) never systematically redone | ireland | High / moderate — bottleneck is archival locating, not compute |
| `famine-parish-register-mortality` | Parish-resolution Famine mortality from the NLI's 373,000 untranscribed register images | ireland | High / mixed — corpus open, HTR is the real wall |
| `bmh-mspc-divergence` | Two self-report archives of the same revolution, differently incentivised; measure the divergence | ireland | High / moderate — entity linkage is everything |

### Lane 2 — Contested historical evidence
Weighted to the brief's highest-value class: claims propagated through a century of
citation without anyone re-checking the source.

| Slug | Description | Category | Difficulty / tractability |
|------|-------------|----------|---------------------------|
| `blood-eagle-kenning` | Did a skaldic metaphor become a ritual through retelling? Frank (1984) vs. the 2022 *Speculum* anatomy | historical-controversies | High / **good** — corpus fully digitised, evidence base enumerable (four individuals) |
| `black-death-mortality-figure` | Where the "one third of Europe" number actually comes from, and whether an aggregate figure means anything | historical-controversies | High on substance, moderate on citation history / **very good for the citation half** |
| `caligulas-seashells` | *Conchae* or *musculi* — a military term misread into a madness anecdote | historical-controversies | Moderate / **good** — cheapest problem here to start |

### Lane 3 — Non-Western scripts, ciphers and archives
The board's worst-represented area: of eleven previous proposals only three sat outside the
European and Mediterranean orbit. These three are Sudan, Yunnan and Oaxaca.

| Slug | Description | Category | Difficulty / tractability |
|------|-------------|----------|---------------------------|
| `meroitic-language` | Script deciphered since 1911, language still unread; ~100 secure glosses. First machine-readable corpus published 2025 | historical-texts | Very high / **good** — open corpus plus a current computational baseline |
| `dongba-manuscript-corpus` | The last living pictographic script; bind glyphs to priests' oral readings before the readers are gone | historical-texts | Moderate-high / good for corpus, structurally limited for meaning |
| `zapotec-hieroglyphic-writing` | Mesoamerica's other script, genuinely undeciphered; Urcid's corpus is free and unexploited as data | historical-texts | High / good for distributional analysis, poor for decipherment |

## Candidates investigated and rejected

Recorded so the next run does not re-propose them.

- **`pollice-verso` (the gladiatorial thumb gesture)** — rejected. The researcher proposing
  it flagged it as its own weakest candidate and was right. The interesting half ("the
  modern convention comes from Gérôme's 1872 painting") is already thoroughly covered by
  general-audience myth-busting outlets including a site dedicated to closing exactly this
  class of question. The residual open question — whether Corbeill's reversed reading is
  consensus — could not be shown to be unclaimed, and the candidate rests on proving a
  negative that was never established.
- **Kilmichael ambush / the Hart–Ryan controversy** — rejected on the obscurity bar. Real
  and contested, but it has an entire scholarly cottage industry attached. `bmh-mspc-divergence`
  deliberately approaches the same archive family at corpus level instead.
- **"Dead of the Irish Revolution" (O'Halpin and Ó Corráin, 2020) completeness** — rejected.
  A mature reference work; no specific evidenced gap was found, and "is this database
  complete?" without a documented deficiency is speculation, not a problem.
- **Convert Rolls (Penal-era conversions)** — rejected for this run. Real record class,
  already digitised and searchable, but no specific unresolved historiographical dispute
  attached to it could be found. A database is not by itself an open problem.
- **Virtual Record Treasury "what is still missing" as a standalone problem** — rejected as
  too diffuse. No record class could be pinned to a pre-1922 total, a reconstructed
  fraction, and a defined remaining gap — the three numbers a falsifiable criterion needs.
  `cromwellian-transplantation-compliance` is the one place in this territory where a
  specific record class has a named scholarly literature about its post-1922 reconstruction.
- **Spartan infanticide / the Kaiadas pit** — rejected as already closed. Excavation of the
  cave found bones exclusively of males aged 18–35 and no infants; the debunking is
  published and popularised.
- **Trepanning survival-rate statistics** — rejected as already closed. Exactly the target
  pattern in shape, but the re-examination has happened (Kushner, Owens and Verano, 2018,
  ~800 trepanned Peruvian crania) and was widely covered.
- **Cortés mistaken for Quetzalcoatl** — rejected. Townsend's "Burying the White Gods"
  (*American Historical Review*, 2003) already did the definitive tracing. Popular
  persistence of a myth is not the same as a live scholarly dispute.
- **Library of Alexandria burned by Caliph Omar** — rejected. Strong citation-chain shape,
  but the primary-source debunking is already published and citable, and the topic sits
  close to household-name territory.
- **"9 million witches burned"** — rejected as closed; traced by Ronald Hutton to Gottfried
  Christian Voigt's 1783 estimate.
- **Pytheas of Massalia and the location of Thule** — deprioritised. A lost-source problem
  offering little a text-and-compute agent could newly contribute, and already given a full
  modern treatment by Cunliffe (2001).
- **Jurchen script** — rejected. Generally considered deciphered as a writing system; a
  surviving glossary and the *Nüzhen zishu* primer give it grounding that Khitan lacks. What
  is unread is unread through physical damage, not linguistic mystery.
- **Bamum, Vai and Bassa Vah scripts** — rejected. Modern invented scripts with documented
  creators and known histories; neither undeciphered nor orphaned. *Rejected on background
  knowledge without a verification pass — flagged so a future run can check rather than
  inherit the judgement.*
- **Ottoman diplomatic ciphers (Ibrahim Afif Effendi's undecrypted correspondence)** —
  **genuinely open and genuinely interesting**, and rejected only on access. Sedat Bingöl,
  "Methods for encryption in early 19th-century Ottoman diplomatic correspondence,"
  *Cryptologia* 46:6 (2022), 498–524, confirms the cipher key could not be located in the
  Ottoman State Archives, leaving the correspondence unreadable. But the BOA digitises only
  a subset remotely, full images need an e-Devlet account or a reading-room visit, and
  cipher documents were not confirmed to be in the open subset. This fails the brief's rule
  against object-access-gated problems. **Revisit if the Hub ever acquires archive access —
  this is the best candidate on the reject list.**

## Held over — good candidates, not proposed this run

Distinct from rejections. These survived scrutiny but lost their slot; a future run should
look at them first.

- **`ulster-plantation-muster-roll-demography`** — the 1630 muster roll (British Library,
  283 folio sheets, 13,147 named males across the nine counties of Ulster; R. J. Hunter,
  *Men and Arms: The Ulster Settlers, c. 1630*). Verification confirmed a real methodological
  problem: the rolls "seriously underestimate" the population, figures are missing for
  Kilmacrenan barony and the Salter's Company lands, and the household multiplier sits
  somewhere between 2.0 and 2.5. **Held over** because its core question — converting a
  fiscal-military listing into population via a contested multiplier — substantially
  duplicates `hearth-tax-population-reconstruction`, which is better anchored in
  peer-reviewed work, and because this candidate's sourcing is largely genealogy-sector
  rather than scholarly. Note it also leaves the plantation period itself thinner than
  ideal in the Ireland lane. Excellent corpus readiness; revive it with a peer-reviewed
  dispute to anchor against.
- **`casket-letters-authenticity`** — the Casket Letters of Mary, Queen of Scots. The
  originals were destroyed in 1584; everything descends from copies, translations and
  transcriptions, several removes from any original, and authenticity remains disputed
  among named modern historians. A near-perfect fit for the citation-chain lane, and the
  proposed deliverable — a stemma of every surviving copy showing which modern "standard
  text" descends from which — would be genuinely new. **Held over because corpus status
  could not be resolved.** Cecil's annotated transcripts survive and Henderson's 1889
  edition is on the Internet Archive, but where the manuscript copies are held and whether
  they are digitised was not established. Settle that first and this becomes proposable.
- **`khitan-large-script`** — over half the characters have no accepted reading, no
  dictionary survives, and a 2025 survey describes the field as at a "methodological
  impasse". Held over because the researcher's own honest read is that fresh decipherment is
  not tractable for a remote agent, and the defensible contribution — assembling the ~17
  large-script monuments into one encoded corpus — is worth doing but is a narrower problem
  than the framing promises. A pending Unicode proposal may change this materially.
- **`libyco-berber-numidian-language`** — script largely deciphered, language barely.
  Held over because the LBI database covers only the Canary Islands and Morocco, not the
  larger Numidian corpus, and because the framing rests on tertiary sourcing.
- **Batak *pustaha* manuscripts (Sumatra)** — a strong runner-up. The script is deciphered
  but the esoteric *poda* divinatory register of the content is obscure; Leiden holds ~340
  catalogued manuscripts, and the Library of Congress was digitising as of 2026. An archive
  problem rather than a decipherment one, which fits the brief well.
- **Nsibidi (Cross River, Nigeria)** — not rejected on evidence, dropped for time. Corpus
  reportedly fragmentary and dispersed across colonial-era ethnographic collections; needs a
  dedicated pass to assess honestly.

## Domains this run did not reach

- **South Asian scripts** beyond the excluded Indus — nothing investigated. A real gap.
- **Central Asian material** — Old Turkic, Yenisei and Talas inscriptions with contested
  readings; Tangut-adjacent minor corpora. Untouched.
- **Non-Western cipher traditions** — Persian, Safavid, Mughal, Chinese, Japanese, Korean and
  Ethiopian. Only the Ottoman case was examined, and it was rejected on access grounds. This
  remains the single most conspicuous hole on the board: `ciphers/` is entirely Western.
- **Non-Western citation-chain cases** — claims that entered Western scholarship through
  nineteenth-century orientalist translation and were never re-checked against the originals.
  Lane 2 stayed in the classical and early-modern European orbit because that is where
  checkable citations were quickest to find. This is probably the highest-value unworked
  territory identified by this run.
- **Munster Plantation demography**, the Composition of Connacht (1585), Griffith's Valuation
  and the tithe applotment books, and the 1926 Free State census — all unreached in lane 1.
- **Irish-language sources** on plantation and Famine, as against English-language
  administrative records. Both previous manifests flag non-Anglophone material as
  under-represented and this run did not fix it.

## Operational note for the next run

Batching worked. Two lanes, then one, all three returned. Do not go back to a single
seven-way fan-out.

The binding constraint this time was not rate limits but **egress**: `WebFetch` was blocked
throughout, so no full text was read by anyone, coordinator included. If a future run has
working fetch access, the highest-value first task is not new discovery — it is clearing the
verification debt flagged in these ten folders and in the eleven from the previous run.
