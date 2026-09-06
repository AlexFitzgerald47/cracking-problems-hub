# Progress Log

*Append new entries at the top (most recent first). Never delete previous entries.*

---

## 2026-09-06 – Claude Code (Opus 5), cracker, starting

### What was attempted

First working session on this problem. Goals in order: make it workable (get a
machine-readable corpus and validate it), calibrate the instrument on known
authors, then test the collection's own authorship claim and the strongest
existing computational claim about it — that there are two authorial layers
with a break at the manuscript lacuna.

Nine experiments, all in
`attempts/2026-09-06-single-author-null/`, outputs in `results/`.

### Results / findings

**The corpus is sound.** Perseus/Loeb (`phi2331`, perseus-lat2) carries all
thirty lives complete. Cross-checked against an independent digitisation from
the Latin Library: the same vita in the two witnesses is 13.2× closer in
200-MFW space than two different vitae in one witness, with zero overlap. The
features are properties of the text.

**The instrument has power at these lengths.** Work-held-out nearest-neighbour
Delta identifies known Latin prose authors at 0.96 accuracy on 1,000-token
samples and 1.00 at 1,500+. Sixteen of the thirty lives are under 3,000 tokens,
so this number is what makes any null result interpretable.

**The six sigla do not mark six hands.** Separation p = 0.065 and only 19% of
the magnitude of a real two-author difference in the same genre (Suetonius vs
Nepos). No individual siglum separates. Same-siglum lives are also adjacent
lives, and the weak effect tracks position as much as siglum.

**There is a real two-layer structure, and single authors do not produce it.**
On 1,000-token blocks with a text-level permutation null, the pre/post-lacuna
split gives z = +4.8, p = 0.0002, stable from 50 to 400 features. Run
identically on Suetonius' twelve Caesars split at his own sharpest source break,
and on Nepos, the statistic goes *negative*: a single hand's ordered collection
of lives is more internally alike than a random regrouping of it. This is the
control the two-layer claim needed and it holds.

**The break is not the forged documents.** The later lives are 24.0% quoted
material against 10.5% earlier — the single most plausible alternative
explanation. Deleting every `<q>` from the text and re-running: p = 0.0006.
Restricting to lives whose quote density falls in the range shared by both
sides: p = 0.0012. The break is in the narrative.

**The seam is earlier than the lacuna.** Scanning every cut point instead of
testing the assumed one puts the maximum after vita #18, *Alexander Severus* —
where the Marius Maximus source material ends — not after #21 where the
manuscripts break. Leave-one-vita-out moves the peak between #18 and #20 but
never past the lacuna: 30/30 all-text runs, 28/30 narrative-only. The scan was
positive-controlled first on a synthetic collection (Suetonius then Nepos) and
recovered the planted seam exactly.

**No evidence for more than two layers.** Pollio vs Vopiscus inside the later
block: p = 0.53–0.84. The four sigla inside the earlier block: p = 0.24–0.42.

**One further partition, weaker.** Hauptvitae vs Nebenvitae *within the earlier
block only*: p = 0.006–0.023, surviving quote removal. Not significant across
all thirty. Thin (8–11 blocks on the small side) and reported as suggestive.

### Failures & dead ends

- **First power curve was leaky and wrong.** Reported 97.5% at 1,000 tokens
  because a chunk's nearest neighbour was usually another chunk of the same
  work. Rebuilt with the whole work held out. Recorded in RESULTS.md because
  the trap is general.
- **The whole-vita split design contradicted itself** — p = 0.50 at full length,
  p = 0.012 at equalised length. Vita length was carrying it. Abandoned in
  favour of the block design, which removes length from the question. E4's
  output is kept as the reason to distrust whole-vita designs here.
- **Stover & Kestemont 2016 could not be read.** Egress policy blocks
  ora.ox.ac.uk, academic.oup.com, archive.org and every other host tried;
  only `raw.githubusercontent.com` and search-result snippets were reachable.
  Their claims are used here only as second-hand characterisation and are
  flagged unverified everywhere they appear.
- **The Latin Library's *Alexander Severus* is truncated** at 3 of 68 chapters.
  Caught by the token-count check, not by anything downstream. Its *Tacitus*
  also looks short (13 chapters against an expected 17) and was not run down.

### Artefacts produced

- `PROBLEM.md`, `HANDOVER.md`
- `attempts/2026-09-06-single-author-null/RESULTS.md` — the write-up
- `attempts/2026-09-06-single-author-null/PROVENANCE.md` — sources, defects,
  normalisation, the input-validation result
- `code/` — `fetch_sources.sh`, `build_corpus.py`, `stylo.py`, and `e1`–`e9`
- `data/manifest.csv` — 67 lives with siglum, rubric, order, length, quote share
- `results/e1..e9_*.txt` — full output of every experiment

`data/segments.json` (14 MB of token streams) is deliberately not committed;
`fetch_sources.sh` plus `build_corpus.py` regenerate it exactly.

### References consulted

- Perseus `canonical-latinLit`, `urn:cts:latinLit:phi2331` (Magie, Loeb
  1921–32) — **used directly**
- `cltk/latin_text_latin_library`, Historia Augusta — **used directly**
- Stover & Woudhuysen, "Historia Augusta", *Oxford Classical Dictionary*, rev.
  5 Aug 2026 — **cited from the Hub's own manifest, not re-verified this
  session**
- Stover & Kestemont, *BICS* 59.2 (2016), 140–157 — **abstract and secondary
  summaries only; full text unreachable, claims unverified**
- Ribary et al., *Applied Network Science* (2021), complex-networks approach to
  the same question — **noted from a search result, not examined**
