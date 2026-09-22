# Code — how to rebuild the corpus and the inventory

All scripts assume a working directory `$SP` holding the corpus; they were run with
`$SP` = the session scratchpad. Set `SP` at the top of each script (it is a single
module-level constant) to wherever you want the ~280MB corpus to live, then:

```bash
# 1. corpus
git clone --depth 1 https://github.com/PerseusDL/canonical-latinLit.git $SP/corpus/perseus
python3 crawl_ll.py $SP/ll_raw          # first pass over thelatinlibrary.com
python3 complete_ll2.py                 # second pass: follows EXTENSIONLESS directory
                                        # links (/caesar, /cicero) the first pass drops.
                                        # Without this you silently lose Cicero, Caesar
                                        # and Ammianus — see HANDOVER.md.
# 2. extract
python3 perseus_meta.py                 # author/work names from the CTS metadata
python3 build_corpus.py                 # Latin Library HTML -> jsonl
python3 build_perseus2.py               # Perseus XML -> jsonl, keeping div markers

# 3. search and classify
python3 concord.py '\bmuscul[a-z]*' 200 out.json      # concordance with citations
OUT_CSV=../data/musculus_inventory.csv python3 finalize.py
```

`concord.py` is the reusable piece: `search(regex, context_chars)` returns every hit with
corpus, author, work, a reconstructed citation where the Perseus markup allows it, and the
matched form. The next experiments in `HANDOVER.md` (`umbilicus`, `spolia`) need nothing
more than a different regex.

`finalize.py` carries the hand-audited sense overrides. Each entry is a decision made by
reading the passage, with its reason; the reason is written into the CSV's `note` column.
Disagree with them in writing — do not silently recount.

**Corpus caveats**, repeated here because they bite: PHI Latin (`latin.packhum.org`) is
Cloudflare-403 and is *not* in this corpus. The Latin Library's own index pages carry stale
links (`gallic/gall1.shtml` is now `caesar/gall1.shtml`), so 259 paths 404 legitimately.
Perseus ships several editions of the same work — `finalize.py` keeps one per work, and
skipping that step inflates Celsus threefold.
