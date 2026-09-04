# Swarm Discovery Run – 2026-09-04

## How this batch was produced
A seven-lane parallel agent swarm was launched to branch across ciphers, undeciphered
scripts, early-medieval Ireland, early-modern/modern Ireland, attribution and forgery,
contested historical evidence, and quantitative/archival problems. **All seven lanes
terminated on an API rate limit before producing output.** The discovery work was then
carried out directly, sequentially, against the same brief — with the deliberate
consequence that fewer proposals were produced than the fan-out intended, and each was
web-verified individually as still open.

The brief's obscurity bar excluded everything already on the board plus the next tier of
over-covered material (Zodiac, Rongorongo, Indus, Tamam Shud, D'Agapeyeff, Copiale, Oak
Island, Antikythera and similar).

## Candidates investigated and rejected
- **Bellaso's 1555 and 1564 challenge ciphers** — rejected. Verification showed the full
  set has been solved (six of the 1564 seven by Tony Gaffney from 2009, the remainder
  subsequently; the 1555 challenges analysed in *Cryptologia* 42:5, 2018). This is exactly
  the failure mode the verification step exists to catch, and it would have passed a
  plausibility check unexamined.

## Proposals in this batch

| Slug | Description | Suggested category | Difficulty / tractability |
|------|-------------|--------------------|---------------------------|
| `debosnys-ciphers` | Unbroken 1882–83 cryptograms of Henry Debosnys, plus his unestablished identity; rare crib-rich case with same-hand plaintext available | ciphers | High / moderate-good — no transcription exists yet |
| `blitz-ciphers` | Are the alleged WWII East London cipher sheets authentic at all? Authenticity precedes decryption | ciphers | Moderate for authenticity, very high for decryption / good then poor |
| `cypro-minoan` | LBA Cypriot syllabary; the prior question is whether the CM1/CM2/CM3 sub-script division is real | historical-texts | Very high / good once digitised, blocked until then |
| `proto-elamite` | Largest undeciphered Near Eastern corpus; recover sign semantics from administrative structure without identifying a language | historical-texts | High / **best on this list** — corpus open and machine-readable |
| `byblos-syllabary` | ~16 inscriptions, ~100 signs; audit what a corpus this small can support and exclude failed decipherments | historical-texts | Decipherment impossible, audit moderate / fair |
| `epi-olmec-isthmian` | Adjudicate the contested Justeson–Kaufman decipherment; the counter-case depends on an unprovenanced mask | historical-texts | High / moderate — historiographic half fully tractable |
| `dal-riata-migration-direction` | Did Gaels migrate to Argyll, or is it an elite origin myth? Campbell (2001) vs the textual tradition | ireland | Moderate-high / good |
| `patrician-chronology` | The "Two Patricks" problem, reframed: are the annalistic dates independent evidence or back-formations? | ireland | High / **good** — corpus fully edited and online |
| `1641-depositions-quantitative` | Entity resolution over 19,010 digitised pages to deduplicate reported deaths; what the corpus can and cannot support | ireland | Moderate technically, high interpretively / excellent |
| `junius-letters-authorship` | Re-test the Francis attribution with modern stylometry; Ellegård (1962) has never been systematically redone | historical-controversies | Moderate / **very good** — most immediately actionable |
| `thera-eruption-date` | Why radiocarbon and archaeological dating have disagreed by a century for forty years; live as of 2025 | historical-controversies | High / very good — published data, re-analysable |

## Notes for the curator
Four of these are unusually actionable and could be started immediately with no
preparatory work: `proto-elamite`, `junius-letters-authorship`, `1641-depositions-quantitative`,
and `thera-eruption-date`. All four have open, machine-readable primary data.

Three are gated on producing a corpus before any analysis is possible: `cypro-minoan`,
`debosnys-ciphers`, and `byblos-syllabary`. In each case the corpus itself is the first
real deliverable and is worth doing independently of any result.

`patrician-chronology` should be developed alongside the existing
`ireland/early-irish-annals-reliability/` problem; they share a source-criticism core.

`blitz-ciphers` carries a live possibility that the honest outcome is "modern
fabrication, close the problem". That is a result, and the folder says so explicitly.

## Domains this run did not reach

The seven-lane fan-out was intended to produce roughly 28 proposals. Because the lanes
died and the work was redone sequentially under a rate limit, two domains from the
original brief produced nothing and remain open for the next discovery run:

- **Early-modern and modern Ireland** — plantation demography and record survival,
  Cromwellian transplantation numbers, Penal-era landholding reconstruction, pre-Famine
  population estimates and early census reliability, parish-granularity Famine mortality
  and emigration accounting, what can be reconstructed of the Public Record Office
  destroyed in 1922, and disputed provenance in the revolutionary period. The `ireland/`
  category on the board is currently weighted entirely to the early medieval period.
- **Contested historical evidence generally** — particularly the category of claims that
  have propagated through a century of citation without anyone re-checking the original
  source. That is the highest-value target class for an agent with archive access and
  patience, and none was found in this run because the lane never executed.

Also under-served: non-Western and non-Anglophone material. Of the eleven proposals here,
only `proto-elamite`, `byblos-syllabary` and `epi-olmec-isthmian` sit outside the European
and Mediterranean orbit.

## Operational note for whoever runs the next discovery batch

Launching seven research agents in parallel exhausted the session's rate limit within
seconds and produced nothing. Sequence discovery lanes, or run them in small batches, and
budget for the fact that each lane's verification searches are the expensive part. The
verification step should not be the thing that gets cut — it is what caught Bellaso.
