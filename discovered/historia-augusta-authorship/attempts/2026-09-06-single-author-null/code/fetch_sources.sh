#!/bin/sh
# Fetch the two text witnesses. Both are public mirrors on GitHub; direct
# access to Perseus, the Latin Library and archive.org was egress-blocked in
# the session that wrote this, and raw.githubusercontent was not.
#
# Usage: HA_SCRATCH=/some/dir sh fetch_sources.sh
set -e
: "${HA_SCRATCH:=./sources}"
mkdir -p "$HA_SCRATCH"
cd "$HA_SCRATCH"

# Primary witness: Perseus canonical-latinLit (Magie's Loeb text of the HA).
if [ ! -d plit ]; then
  git clone --filter=blob:none --sparse \
    https://github.com/PerseusDL/canonical-latinLit.git plit
  cd plit
  git sparse-checkout set \
    data/phi2331 data/phi1348 data/phi0588 data/stoa0023 data/stoa0162 \
    data/phi1351 data/phi0631 data/phi0448 data/phi1254 data/phi1318 \
    data/phi1242
  cd ..
fi

# Second witness: the Latin Library HA, via the CLTK mirror.
if [ ! -d ll ]; then
  git clone --depth 1 https://github.com/cltk/latin_text_latin_library.git ll
fi

echo "sources ready in $HA_SCRATCH"
