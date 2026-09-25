#!/bin/sh
# Fetch the IACR gold-bar photographs. They are Copyright 1996 IACR and are NOT
# committed to this repository; this script reproduces the working set used by
# the 2026-09-25 session. ~3 MB total.
#
#   sh src/FETCH_IMAGES.sh /tmp/goldbars
#
# The 15 images are the complete set linked from https://www.iacr.org/misc/china/ .
# Note 5.2, 6.1 and 8.1 do not exist; there are 15 images, not 18.
OUT="${1:-./images}"
mkdir -p "$OUT"
for f in 5.1 6.2 7.1 7.2 8.2 9.1 9.2 10.1 10.2 11.1 11.2 12.1 12.2 13.1 13.2; do
  curl -sS -o "$OUT/$f.jpg" "https://www.iacr.org/misc/china/images/$f.jpg" || echo "failed: $f"
done
curl -sS -o "$OUT/cryptograms.html" "https://www.iacr.org/misc/china/cryptograms.html"
ls -l "$OUT"
