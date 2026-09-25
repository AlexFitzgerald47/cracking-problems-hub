# Comparanda

Derived comparison corpora. Sources and licences:

- `liber_transliterations.tsv` — Linear B, 5,084 tablet transliterations extracted from
  LiBER (https://liber.cnr.it), CC BY-SA 4.0. Fetched 2026-09-25 from the per-tablet
  pages' `<meta name="description">` field. This is the derived transliteration table,
  not the 178 MB of source HTML.
- `lineara_inscriptions.json`, `lineara_signs.json` — Linear A, GORILA corpus,
  1,721 inscriptions, via `ryanpavlicek/pyaegean` on raw.githubusercontent.com.
- `cypriot_ig_inscriptions.json` — Cypriot syllabary, *Inscriptiones Graecae* XV 1
  (Berlin-Brandenburg Academy / TELOTA digital edition, CC BY 4.0), 178 inscriptions,
  via the same repository.

**Caveat that cost this session a prediction.** A first pass at the Linear B distribution
(supplied by a delegated researcher) reported lengths starting at 2 syllabograms with no
one-sign tokens at all. That was an artifact of a regex requiring a hyphen, which excludes
every one-sign token by construction. Believed, it would have confirmed prediction P1 on a
bug. `src/genre.py` re-extracts everything from the raw files. Any successor should do the
same rather than trust these counts.
