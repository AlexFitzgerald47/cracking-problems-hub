# BARON constraint ledger

*Opened 2026-09-07. Labels defined in `access-ledger.md`. **Nothing here is `[PRIMARY]`** —
the two released BARON documents were egress-blocked during this session, so every
"cable" row below is somebody else's reading of a document this folder has not seen.*

The model for this file is
`historical-controversies/venona-brown-braun/analysis/network-intersection-1940.md`, which
`PRACTICES.md` names as the board's best defence against candidate enthusiasm: one table,
explicit labels, and the load-bearing edge you have *not* found listed as MISSING beside
the attractive ones.

## The document set

| # | Document | Date | Status |
|---:|---|---|---|
| 1 | London GRU No. 649 | 3 Apr 1941 | `[HUB]`/`[SEARCH]` — exists; content not read |
| 2 | NSA release "Report from BARON" (2 pp., Release 5) | 29 Jul 1941 | `[SEARCH]` — exists; content not read |
| ? | Any further BARON occurrences | — | `[MISSING]` — the corpus has not been enumerated |

**Two documents is a very thin base.** Before anyone scores a candidate, the BARON trail has
to be enumerated across the whole published London GRU corpus, exactly as the BROWN sessions
eventually did. Note the corpus is itself partial: NSA held ~65 GRU London↔Moscow
translations for 1940–41 while GCHQ is described as having sent ~159 on that lane and those
years `[SEARCH]` — so roughly 60% of the known lane traffic is not in the public set, and
absence of a BARON message is weak evidence of anything.

## Constraints on BARON

| # | Constraint | Status | Note |
|---:|---|---|---|
| B1 | Reporting connected with **British decryption of German Enigma traffic** | `[HUB]`/`[SEARCH]` | The whole value of the target rests on this line. **Verify it in the cable first.** |
| B2 | Cable 649 states the information came **solely from BARON** | `[HUB]` | From the Hub's own frontier manifest, itself citing Wilson Center. Not independently confirmed |
| B3 | Annotator notes a **possible connection with Military Intelligence** | `[HUB]` | Ambiguous by design: British MI (MI14 etc.), or Czechoslovak military intelligence, both fit the words |
| B4 | Active in **April and July 1941** | `[SEARCH]` | Two dated documents, four months apart |
| B5 | Runs to the **GRU**, not the NKVD residency | `[INFERRED]` | It is London GRU traffic. This is the constraint that excludes the Blunt/Cairncross-shaped candidates by default |
| B6 | Filed by Haynes under the **U.K. line** | `[SEARCH]` | Attribution is West's; see `solution-status-ledger.md` |
| B7 | Whether the ENIGMA reference is **BARON's own claim** or the annotator's gloss | `[MISSING]` | **The single highest-information unknown in this folder.** It decides H1 vs H3 |
| B8 | Whether BARON is a **person, an organisation, or a relay** | `[MISSING]` | GRU covernames cover all three |

## Context that does not depend on the cables

| # | Fact | Status | Source |
|---:|---|---|---|
| C1 | The London GRU resident in this period was probably **Simon Kremer**, private secretary to the military attaché | `[SEARCH]` | NSA VENONA discussion |
| C2 | In 1940–41 the London GRU used a so-called **Emergency System**, a variant of the basic VENONA cryptosystems | `[SEARCH]` | NSA VENONA discussion |
| C3 | A London GRU message of **10 Aug 1941** covers re-establishing contact with **Klaus Fuchs** | `[SEARCH]` | NSA VENONA discussion. Same residency, three weeks after document 2 — relevant to how ambitious this residency's scientific/technical reporting was |
| C4 | On **3 April 1941** Churchill sent Stalin, via Cripps, a warning derived from Enigma about three of five panzer divisions moving from Romania to southern Poland — deliberately attributed to "a trusted agent" to conceal the SIGINT source | `[SEARCH]` | Churchill's message text is widely quoted; see `churchill-date-collision.md` |
| C5 | Churchill subsequently had Eden pass further Enigma-derived warnings to Ambassador **Maisky in London**; the most detailed went from Maisky to Moscow on **10 June 1941** | `[SEARCH]` | Same |
| C6 | Beneš ordered Moravec to prepare **cooperation with Soviet intelligence**, on terms under which material received from the Soviets would be passed to the British; a meeting took place "in late December" | `[SEARCH]` | Year of the meeting **not established** — this matters and is listed below as MISSING |
| C7 | Moravec's Czechoslovak military-intelligence HQ was at **Porchester Gate, London** | `[SEARCH]` | — |
| C8 | Moravec met British officials in October 1941 and disclosed to the Soviet contact **Chichaev** what Britain knew of German plans against the USSR | `[SEARCH]` | Chichaev was the **NKVD** liaison, not GRU — this is a different channel from B5 and must not be conflated with it |

## MISSING — the load-bearing gaps

| # | Gap | Why it is load-bearing |
|---:|---|---|
| M1 | The **text of both BARON documents** | Everything above marked `[HUB]`/`[SEARCH]` collapses or hardens on two pages plus one cable |
| M2 | **What West's identification rests on** (pp. 67–69) | Decides whether this is an adjudication or an open search |
| M3 | The **year** of the Beneš/Moravec Soviet-cooperation meeting (C6) | If late 1940, a Czech→Soviet channel predates document 1 and H2 strengthens sharply. If late 1941, H2 weakens for April 1941 |
| M4 | Whether the Czech–Soviet channel ran to the **GRU** or only to the NKVD (Chichaev) | C8 documents an NKVD route. H2 needs a GRU route. **This is the bridge that carries H2, and it has not been found** |
| M5 | The **TNA KV 2 piece number** for Sedláček/Selzinger | Directly tests West |
| M6 | The **complete BARON trail** in the published corpus | Sets the real evidence budget; two documents may not be all there is |

## The trap to avoid

The BROWN sessions over-constrained their candidate set for two full sessions by assuming a
property (radio operation) belonged to BROWN when the surrounding traffic assigned it to
STANLEY. `PRACTICES.md` records that as **separate the roles before you constrain the
identity.** The same error is available here in an even more expensive form: assuming that
BARON *knew* the Enigma provenance, when it may have been Moscow or the VENONA annotator who
supplied that framing. Constraint B7 is that error waiting to happen, and it is why B7 must
be settled from the document before any candidate is scored.
