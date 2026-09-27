#!/bin/sh
# Rebuild the comparandum corpora used by this attempt.  They are not committed
# here: Copiale and Borg transcriptions belong to the cipher_benchmark project
# and the Borg images are Vatican Library "linked_only".  Everything is public.
#
#   ./fetch_comparanda.sh /some/dir
# then pass /some/dir as <comparanda_dir> to the analysis scripts.
#
# Note: github.com HTML and the GitHub API are blocked from this environment;
# raw.githubusercontent.com is not.  Hence the manifest-then-raw route.
set -e
OUT="${1:?usage: fetch_comparanda.sh <outdir>}"
B=https://raw.githubusercontent.com/matthewdgreen/cipher_benchmark/main/benchmark
mkdir -p "$OUT"
curl -sS -o "$OUT/records.jsonl" "$B/manifest/records.jsonl"
curl -sS -o "$OUT/unsolved_records.jsonl" "$B/unsolved/manifest/records.jsonl"
python3 - "$OUT" <<'PY' > "$OUT/ids.txt"
import json, sys
for l in open(sys.argv[1] + "/records.jsonl"):
    r = json.loads(l)
    f = r.get("transcription_canonical_file")
    if f and r["source"] in ("copiale", "borg"):
        print(r["source"], r["id"], f)
PY
while read -r src id f; do
  mkdir -p "$OUT/$src"
  [ -s "$OUT/$src/$id.txt" ] || curl -sS -o "$OUT/$src/$id.txt" "$B/$f"
done < "$OUT/ids.txt"
# Blitz pages 7 and 8, straight from the source of record (identical to the
# cipher_benchmark copy, which is a mirror, not an independent reading).
curl -sS -o "$OUT/ciphermysteries_p7p8.html" \
  https://ciphermysteries.com/2014/10/24/blitz-cipher-partial-transcription
curl -sS -o "$OUT/ciphermysteries_permanent.html" \
  https://ciphermysteries.com/other-ciphers/blitz-ciphers
echo "done: $(ls "$OUT/copiale" | wc -l) copiale, $(ls "$OUT/borg" | wc -l) borg"
