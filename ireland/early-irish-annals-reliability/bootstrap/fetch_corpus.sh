#!/usr/bin/env bash
# Try to fetch the Annals of Ulster into sources/. Run it once at the start of a
# session; it is a no-op if the hosts are blocked or the files already exist.
#
# Honest about what it does not know: the CELT URL patterns below are candidates,
# not verified paths -- the session that wrote this script could not reach CELT
# to check them. The script tries each, reports which worked, and never pretends
# a failure was a success. Fix the list when you have a session that can see the
# site, and commit the correction.

set -u
DEST="$(cd "$(dirname "$0")/.." && pwd)/sources"
mkdir -p "$DEST"

get() { # get <url> <outfile> <description>
  local url="$1" out="$2" desc="$3"
  [ -s "$DEST/$out" ] && { echo "  have    $out"; return 0; }
  if curl -fsSL --max-time 120 "$url" -o "$DEST/$out" 2>/dev/null && [ -s "$DEST/$out" ]; then
    echo "  GOT     $out  ($(wc -c < "$DEST/$out") bytes)  <- $desc"
    return 0
  fi
  rm -f "$DEST/$out"
  echo "  missed  $out  <- $url"
  return 1
}

echo "== archive.org: Hennessy, Annala Uladh (1887), public domain =="
# vol 1 = AD 431-1056; later volumes carry 1057-1541. Identifiers follow the
# archive.org pattern annalauladhannal0Nroyauoft.
for n in 01 02 03 04; do
  get "https://archive.org/download/annalauladhannal${n}royauoft/annalauladhannal${n}royauoft_djvu.txt" \
      "AU-hennessy-vol${n}-1887.txt" "Annals of Ulster vol ${n}"
done

echo "== CELT: Mac Airt & Mac Niocaill text and translation (URLs UNVERIFIED) =="
for id in T100001A T100001B T100001C G100001A G100001B G100001C; do
  get "https://celt.ucc.ie/${id}.html" "celt-${id}.html" "CELT ${id}" \
    || get "https://celt.ucc.ie/published/${id}/index.html" "celt-${id}.html" "CELT ${id} (alt path)"
done

echo
echo "in $DEST:"
ls -la "$DEST" 2>/dev/null | tail -n +2
echo
echo "NOTE: archive.org text is raw OCR of 1887 print in Latin and Irish. Verify"
echo "every quoted phrase character by character before relying on it, and mark"
echo "OCR-suspect readings as such. It is Hennessy, not Mac Airt & Mac Niocaill"
echo "(1983) -- adequate for the astronomical notices, not for arguing about"
echo "which annal-year an entry sits at."
