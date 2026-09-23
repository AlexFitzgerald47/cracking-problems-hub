# Rerunning the 2026-09-23 blood-eagle analysis

    ./FETCH_CORPUS.sh            # ~11 MB, eight files, two independent scans
    export SKJ="$PWD/corpus"     # where the scripts look; defaults to /tmp/be/corpus
    python3 extract.py           # raw hits for skera / rista / bak / eagle  -> hits.json
    python3 inventory.py         # beast-of-battle verb-class inventory      -> beast_rows.json
    python3 construals.py        # base rates for the competing construals of `ara`
    python3 replicate.py         # SAME pipeline on the second OCR scan -- the replicate
    python3 final_numbers.py     # complete `bak` enumeration, both scans
    python3 formula.py           # the carrion formula ("under the eagle's talons")
    python3 emit_tables.py       # -> beast_blade_adjudication.tsv (blank verdict column)
    python3 adjudicate.py        # fills the verdict column from an explicit rule table

`foldlib.py` holds the OCR folding used by all of them.

Two things to know before trusting any number these print:

1. **The counts are candidate generators, not results.** `inventory.py` reports blade-verb
   co-occurrences within a character window; 18 of them in one scan, and all 18 are spurious.
   The verdicts in `adjudicate.py`'s rule table are the actual finding, and they are a human
   judgement about Old Norse syntax, not an output of the code. Audit them against Finnur's
   facing Danish translation, which sits in the same files.
2. **Every number is computed twice**, once per scan. If a change makes the two scans disagree
   on a *result* (rather than on a raw count, where ~7% drift is normal), something is wrong.
