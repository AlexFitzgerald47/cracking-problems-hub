#!/bin/sh
# Reproduce the 2026-09-25 session's refutation scripts, then this session's.
# Run from this directory.  The 2026-09-25 scripts are run in a copy so that
# nothing in another validator's directory is written to.
set -e
PRIOR=../2026-09-25
TMP=$(mktemp -d)
cp -a "$PRIOR"/. "$TMP"/
( cd "$TMP" && python3 parse_ocbi.py )
for f in refute refute2 refute3; do
  ( cd "$TMP" && python3 $f.py > ${f}_new.txt 2>&1 )
  if diff -q "$PRIOR/${f}_output.txt" "$TMP/${f}_new.txt" >/dev/null; then
    echo "$f: output IDENTICAL to the recorded 2026-09-25 output"
  else
    echo "$f: OUTPUT DIFFERS -- inspect $TMP/${f}_new.txt"
  fi
done
rm -rf "$TMP"
python3 lib_ocbi.py
for f in r4_power_null r5_merge_circularity r6_mirror_shape_test \
         r7_cylinder_standing r8_criterion4_pa r9_audit_and_chronology; do
  echo "== $f"; python3 $f.py > ${f}_output.txt 2>&1 && echo "   ok -> ${f}_output.txt"
done
