# Data

**Not committed** (CELT marks these texts `restricted`, and the translations are in
copyright — AU vol. 1 to the School of Celtic Studies, DIAS):

- `raw/*.xml` — the four CELT TEI files. `python3 src/fetch.py data/raw` re-creates them.
- `entries.jsonl` — the parsed per-entry table *including entry text*.
  `python3 src/parse.py data/raw data/entries.jsonl` re-creates it.

**Committed** (derived, no text):

- `entries_derived.csv` — 13,414 rows, one per annalistic entry: witness, year, entry
  index, kalend flag, word count, the six tag flags, and a 12-hex sha1 prefix of the
  entry text so anyone can confirm they parsed the same bytes. Every number in
  `RESULTS.md` is computable from this file plus the year profile.
- `../results/audit_sample.json` — the 80 entries (40 tagged, 40 untagged) read by hand
  for the tagger audit, quoted at ≤300 characters each so the audit can be checked.
