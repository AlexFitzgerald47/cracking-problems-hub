#!/bin/sh
# 2026-10-02 VALIDATOR 1 independent reproduction, Linear A functional/historical claim.
# Offline: works against the vendored ./data.  To refresh witnesses:
#   curl -o data/LinearAInscriptions.js \
#     https://raw.githubusercontent.com/mwenge/lineara.xyz/master/LinearAInscriptions.js
#   curl -o data/GORILA-Vol1.pdf \
#     https://raw.githubusercontent.com/mwenge/lineara.xyz/master/papers/GORILA-Vol1.pdf
cd "$(dirname "$0")"
{ python3 census.py; echo; python3 arith2.py; echo; python3 tests.py; echo;
  python3 perm.py; echo; python3 lexemes.py; } 2>&1
