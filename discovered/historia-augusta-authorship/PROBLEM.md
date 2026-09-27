# The Historia Augusta: how many hands, and where do they change?

## Statement

The *Historia Augusta* is a collection of thirty Latin imperial biographies
covering Hadrian to Numerian (AD 117–284). It presents itself as the work of
six authors — Aelius Spartianus, Julius Capitolinus, Vulcacius Gallicanus,
Aelius Lampridius, Trebellius Pollio and Flavius Vopiscus — writing under
Diocletian and Constantine and dedicating their work to those emperors.

Hermann Dessau argued in 1889 that all six are a fiction: one author, writing
at the end of the fourth century, invented the sigla, the dedications and much
of the documentary evidence the lives quote. Dessau's core thesis is now
broadly accepted, but the specific unknowns are not settled. The revised
Oxford Classical Dictionary entry (Stover & Woudhuysen, 5 August 2026) still
describes the work's date, authorship and nature as uncertain.

The named unknowns this problem targets:

1. **How many authorial strata does the collection actually contain?** One,
   two, or six?
2. **If more than one, where is the boundary?** At which life does the text
   change hand or compositional mode?
3. **What else could produce the same signal?** The collection's later lives
   are far more heavily padded with quoted (and largely forged) documents than
   its earlier ones, and its "secondary" lives of caesars and usurpers are a
   different kind of composition from the lives of reigning emperors. Either
   could imitate a change of author.

## Why it belongs on the board

The *Historia Augusta* is the only extended narrative source for long stretches
of third-century Roman history. What is or is not trustworthy in it depends on
who wrote it, when, and out of what. It is also the text that first brought
computational stylometry into classical *Echtheitskritik* (Marriott 1979), so
it is a case where a methods-first attack has a real chance of moving a
substantive historical question rather than restating it.

It passes the crack test: the unknown is named, the evidence is a complete
machine-readable Latin corpus, competing answers make different predictions,
and a result would be recognisable as a discovery rather than a better
estimate.

## Known constraints / previous major attempts

- **Dessau (1889)** — single author, Theodosian date. The founding argument,
  made on prosopographic and linguistic grounds.
- **Marriott (1979)**, and 1990s follow-ups — early computational passes,
  generally read as supporting single authorship, but with methods that would
  not now be considered validated.
- **Stover & Kestemont, BICS 59.2 (2016)** — the strongest existing
  computational treatment. Uses the General Imposters authorship-verification
  framework and PCA. Reported here at second hand from published abstracts and
  summaries only: **the paper itself could not be fetched from this
  environment (egress-blocked), so its detailed claims are unverified in this
  repository.** The summarised conclusion is that GI verification does not
  support multiple authorship, but that two authorial layers appear,
  corresponding roughly to the *Hauptviten* and the later lives, with a
  discontinuity after the lacuna.
- **Ribary et al., *Applied Network Science* (2021)** — a complex-networks
  approach to the same question. Not examined here.

Hard constraints:

- **Short texts.** Sixteen of the thirty lives are under 3,000 tokens; the
  shortest is 1,018. Any method must state its power at those lengths.
- **Confounded partitions.** The six sigla, the position in the collection,
  the primary/secondary rubric and the quoted-document density all co-vary.
  A partition that separates cannot be named after one of them until the
  others are held constant.
- **No independent authorial sample.** Unlike a normal attribution problem,
  there is no securely attributed text by "Vopiscus" to compare against. Every
  test is necessarily internal.

## Success criteria

Real progress, in ascending order:

- A validated pipeline with a stated power curve on known Latin authors at
  Historia Augusta text lengths.
- A calibrated verdict on the six sigla, with the effect size expressed
  against a known two-author difference rather than against zero.
- A boundary located from the text with a stability estimate, rather than
  assumed from the manuscript lacuna.
- Elimination of the compositional-mode explanations (quotation density,
  Nebenvita rubric) as sufficient causes of any boundary found.
- A full solution would be a defensible account of how many hands wrote the
  collection, where they change, and when they wrote — the last of which is
  not attackable by internal stylometry alone.

## Key sources & starting points

- **Text (primary witness):** Perseus canonical-latinLit,
  `urn:cts:latinLit:phi2331`, perseus-lat2 (Magie's Loeb text, 1921–32),
  all thirty lives. Complete.
- **Text (second witness):** The Latin Library *Historia Augusta*, via the
  CLTK mirror. Independent digitisation, used for input validation.
  **Defect: its *Alexander Severus* is truncated at 3 of 68 chapters.**
- **Controls:** Suetonius' twelve Caesars and Nepos' *De viris illustribus* —
  single-author collections of lives in transmitted order, the matched nulls
  for any claim about structure inside an ordered collection of biographies.
- Stover & Woudhuysen, "Historia Augusta", *Oxford Classical Dictionary*,
  revised 5 Aug 2026, DOI 10.1093/acrefore/9780199381135.013.3132v1.
- Stover & Kestemont, "The Authorship of the Historia Augusta: Two New
  Computational Studies", *BICS* 59.2 (2016), 140–157.

## Notes

Proposed as Tom Holland target **T3** in
`discovered/_manifest/rest-is-history-host-targets-2026-09-05.md`, and ranked
**D4 / #25** in `board/TARGETS.md`.

Internal stylometry can count strata and locate seams. It cannot date the
work. The Theodosian-date question needs a different attack — prosopography,
source-dependence on datable texts, or lexical comparison against securely
dated fourth-century Latin — and should not be confused with the authorship
question when reporting results.
