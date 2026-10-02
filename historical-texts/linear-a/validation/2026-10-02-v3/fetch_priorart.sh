#!/bin/sh
# Prior-art and adjudication documents used by ATTACK 8 and the novelty check.
set -e
mkdir -p priorart
B=https://raw.githubusercontent.com/dbourdeau/cyphersolver/main/targets/lineara
curl -sS "$B/NOTES.md"           -o priorart/cyphersolver_NOTES.md
curl -sS "$B/RESEARCH_REPORT.md" -o priorart/cyphersolver_RESEARCH_REPORT.md
curl -sS https://raw.githubusercontent.com/mwenge/lineara.xyz/master/commentary/HT34.html \
     -o priorart/younger_HT34_commentary.html
