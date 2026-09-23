# Reproducing this attempt

Python 3, no third-party packages. From this directory:

```bash
A=../../../early-irish-annals-reliability/attempts/2026-09-23-iona-transition

# 1. corpus (not committed: CELT `restricted`, translations in copyright)
mkdir -p data/raw
python3 $A/src/fetch.py       data/raw          # the four witnesses
python3 $A/src/parse.py       data/raw data/entries.jsonl
python3 src/fetch_afm.py      data/raw          # the holdout
python3 src/parse_afm.py      data/raw data/afm.jsonl

# 2. validate the pipeline against the Annals folder's committed corpus
python3 - <<'PY'
import subprocess, filecmp, os, shutil
os.makedirs("/tmp/chk/data", exist_ok=True)
shutil.copy("data/entries.jsonl", "/tmp/chk/data/entries.jsonl")
shutil.copytree("../../../early-irish-annals-reliability/attempts/"
                "2026-09-23-iona-transition/src", "/tmp/chk/src", dirs_exist_ok=True)
subprocess.run(["python3", "src/export_derived.py"], cwd="/tmp/chk", check=True)
assert filecmp.cmp("/tmp/chk/data/entries_derived.csv",
                   "../../../early-irish-annals-reliability/attempts/"
                   "2026-09-23-iona-transition/data/entries_derived.csv", shallow=False)
print("pipeline reproduces the committed corpus byte for byte")
PY

# 3. analyses  (export PYTHONPATH=src first)
export PYTHONPATH=src
python3 src/run_markers.py     data/entries.jsonl results/markers.json
python3 src/run_cp.py          data/entries.jsonl results/changepoint.json   # sec 1
python3 src/run_spreads.py     data/entries.jsonl results/spreads_raw.json \
                                                  results/spread_audit.txt
python3 src/run_gap.py         data/au_alternative_datings.tsv results/gap.json   # sec 3
python3 src/run_null.py        data/au_alternative_datings.tsv results/null.json
python3 src/run_afm.py         data/afm.jsonl results/afm_dupes.json \
                                              results/afm_dupe_audit.txt          # sec 4
python3 src/run_p2.py          data/afm_duplicate_datings.tsv results/afm_p2.json
```

`run_cp.py` and `run_null.py` take about ten seconds each (1000 permutations and
500 bootstraps); everything else is immediate.

**What is hand-work and cannot be re-derived by running the code**: the accept /
reject verdicts in `src/audit_verdicts.py`, the 40 clusters in
`data/au_alternative_datings.tsv` and the 9 in `data/afm_duplicate_datings.tsv`.
Those are judgements about whether two entries concern one person, and the
transcripts they were made from are in `results/spread_audit.txt`,
`results/afm_dupe_audit.txt`, `results/marker_audit.txt` and
`results/partner_searches.txt`. Attack them there.
