#!/bin/bash
# iadl.sh <identifier> <outfile> -- download _djvu.txt via the item's real node
id="$1"; out="$2"
meta=$(curl -sS --max-time 60 "https://archive.org/metadata/$id")
server=$(echo "$meta" | python3 -c "import json,sys; print(json.load(sys.stdin).get('server',''))")
dir=$(echo "$meta" | python3 -c "import json,sys; print(json.load(sys.stdin).get('dir',''))")
if [ -z "$server" ]; then echo "NO SERVER for $id"; exit 1; fi
curl -sS --max-time 180 -o "$out" "https://$server$dir/${id}_djvu.txt"
echo "$id -> $out $(wc -c < "$out") bytes"
