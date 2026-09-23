# Reproduction of the 2026-09-17 and 2026-09-21 attempts

**Run:** 2026-09-23, fresh container, nothing cached. `data/chunks.json` is
gitignored, so both prior attempts were rebuilt from source before anything new
was run. This is the check the board's practices require before trusting a
pipeline on a new arm.

## Re-run, unchanged

```
curl .../textcreationpartnership/Texts/master/TCP.csv       # 29,286,409 bytes
git clone --depth 1 dracor-org/engdracor
python fetch_tcp.py          # 774 TCP texts: 774 ok, 0 failed
python build_corpus.py
python expG_authorblind.py
```

`numpy` 2.4.6, as on 2026-09-21.

## Result: identical

**Corpus.** `data/manifest.json` rebuilt **byte-identically** to the committed
copy (md5 `7abdc15ea5b866aa07480c746f2b41df`): 74 kept non-dramatic texts, 42
drops with the same reasons (14 markup, 6 too short, 19 pageant, 3 manual), 943
non-dramatic chunks, 3,062 drama chunks, 27 authors.

**Experiment G.** `results/expG_authorblind.json` rebuilt **byte-identically**
(md5 `d9cd6237a628bff1099cb412467748ad`). The headline cells reproduce exactly:
27-author non-dramatic uncorrected micro 0.141 / max share 41.0%, author-blind
0.358 / 17.9% with null p = 0.000, leave-one-author-out 0.399; 8-author panel
0.216 → 0.498, p = 0.005; pageant arm 0.114 → 0.286, p = 0.220. Per-author
figures including Greene 0.033 and Middleton 0.038 are unchanged.

Both prior sessions are reproducible from committed code and manifests alone.
The 2026-09-21 attempt's own reproduction of 2026-09-17 therefore now stands at
two independent rebuilds on two containers.

## One thing this session changed about reproducibility

`expH_holdout.py` seeds each permutation null separately rather than drawing from
one session-long stream, because adding a treatment to the script shifted every
subsequent null's p-value in the earlier drafts of this session's own run (the
uncorrected arm's p moved 0.041 → 0.128 → 0.117 across edits, on unchanged data).
Two consecutive runs of the committed script now produce byte-identical output.
The prior attempts' scripts share the single-stream design; their published
p-values are correct for their own run order, but an edit that inserts a draw
will move them.
