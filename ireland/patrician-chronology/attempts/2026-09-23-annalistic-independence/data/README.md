# Data

**Not committed.** CELT marks its annal texts `restricted` and the translations
are in copyright (AU vol. 1 to the School of Celtic Studies, DIAS). Regenerate:

```
python3 ../../../early-irish-annals-reliability/attempts/2026-09-23-iona-transition/src/fetch.py raw
python3 ../../../early-irish-annals-reliability/attempts/2026-09-23-iona-transition/src/parse.py raw entries.jsonl
```

That parser is re-used unchanged. Before anything was built on it this session
re-ran it from a clean fetch and reproduced the committed
`entries_derived.csv` of the Annals folder **byte for byte**, sha1 entry
digests included — so the 13,414 entries here are provably the same bytes.

**Committed** (derived, hand-verified, no restricted text beyond short quotation):

- `au_alternative_datings.tsv` — 40 clusters of alternative datings across the
  four witnesses, 430–760. The comparison class.
- `patrician_dossier.tsv` — the collation: every entry in which Patrick or
  Palladius is the subject, 350–560, with attestation and marker status.
