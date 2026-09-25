# Reproducing this attempt

Pure Python 3, no third-party packages except `pillow` (only for the image
crops; every statistic runs without it). Total runtime about 25 minutes, almost
all of it in `reuse.py` and `urn.py`.

```
python3 src/exact_tail.py           # panel item 1: the exact tail, 263 letters      (~20 s)
python3 src/exact_tail_dp_check.py  # same number by a different algorithm            (~5 s)
python3 src/corrected_tail.py       # P1: exact tail before and after the correction (~30 s)
python3 src/face_balance.py         # P2: is a physical bar face balanced?           (~4 min)
python3 src/inherit.py              # the decisive test: is face balance inherited?  (~2 min)
python3 src/urn.py                  # P3: the depleting-supply model, all urn sizes  (~8 min)
python3 src/reuse.py                # P4: within-string reuse, both corpora          (~8 min)
python3 src/perstring.py            # where the reuse deficit lives                  (~3 min)
python3 src/clustering.py           # exploratory: local clustering (negative)       (~4 min)

sh src/FETCH_IMAGES.sh /tmp/goldbars          # the 15 photographs (not committed)
python3 src/crop.py /tmp/goldbars/12.1.jpg /tmp/ugm.png 350,125,875,185 4
```

`data/instances_photographic.tsv` is the session's own reading of the 15
photographs and is the main new artefact. `data/cryptograms_corrected.txt` is
the deduplicated 16-string inventory implied by it (261 letters, not 263).
