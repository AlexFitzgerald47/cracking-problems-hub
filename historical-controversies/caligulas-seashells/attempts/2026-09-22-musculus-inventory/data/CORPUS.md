# Corpus provenance

Two independent Latin corpora, cloned 2026-09-22. Neither is redistributed here (135 MB
and 220 MB); both are reproducible from the commands below.

| corpus | source | commit-pinned by | files | tokens |
|---|---|---|---|---|
| Latin Library | `https://github.com/cltk/lat_text_latin_library` | `git clone --depth 1` | 2,141 `.txt` | 13,353,918 |
| Perseus canonical-latinLit | `https://github.com/PerseusDL/canonical-latinLit` | `git clone --depth 1` | 364 Latin `.xml` | 7,926,686 |

Total searched: **21,280,604 word tokens.**

```
git clone --depth 1 https://github.com/cltk/lat_text_latin_library.git ll
git clone --depth 1 https://github.com/PerseusDL/canonical-latinLit.git perseus
python3 src/concordance.py --ll ll --perseus perseus \
  --forms "musculus,musculi,musculo,musculum,muscule,musculorum,musculis,musculos" \
  --out results/musculus_raw.json
python3 src/canonicalise.py results/musculus_raw.json results/musculus_canonical.json
python3 src/senses.py results/musculus_canonical.json \
  results/musculus_senses.tsv results/musculus_sense_summary.json
python3 src/collocations.py
python3 src/zoonym_null.py ll
```

## Known corpus limitations, recorded before any result depends on them

1. **The Latin Library's Pliny is incomplete** — books 1–5 of 37 only. Perseus carries the
   whole *Naturalis Historia*, which is why both corpora are needed. Any survey run on the
   Latin Library alone would have missed most of Pliny.
2. **Celsus is absent from the Latin Library entirely.** Perseus supplies it, and it alone
   contributes 24 of the 101 attestations.
3. **The Perseus Pliny text carries its critical apparatus inline.** Three "attestations"
   are apparatus repetitions or a rejected variant (`ramusculus`), not running text; they
   are classified `NOISE` and excluded from sense percentages where stated.
4. **Perseus ships multiple editions of the same work** (three of Celsus). `canonicalise.py`
   keeps one edition per work and then drops Perseus hits whose context already appears in
   a Latin Library hit. Three Caesar *Bellum Civile* duplicates survive this on orthographic
   variation and are noted in the analysis rather than silently counted.
5. **Neither corpus is the PHI/*Bibliotheca Teubneriana Latina* canon.** Coverage of
   fragmentary and technical authors is thinner than PHI5. The inventory below should be
   read as near-complete for the major authors, not as exhaustive for all Latin.
