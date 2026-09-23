#!/bin/sh
# Rebuild the corpus this session used. Two INDEPENDENT OCR scans of the same four
# volumes are downloaded deliberately: they are used as replicates to show the
# result is not an OCR artefact.
#   *finn   = University of Ottawa scan
#   *finnu  = University of North Carolina scan
# Volumes 01,02 = A I, A II (text efter handskrifterne / diplomatic)
# Volumes 03,04 = B I, B II (rettet tekst / normalised, with Finnur's Danish prose translation)
mkdir -p corpus && cd corpus
for id in dennorskislandsk01finn dennorskislandsk02finn dennorskislandsk03finn dennorskislandsk04finn \
          dennorskislandsk01finnu dennorskislandsk02finnu dennorskislandsk03finnu dennorskislandsk04finnu; do
  curl -sSL "https://archive.org/download/$id/${id}_djvu.txt" -o "$id.txt"
done
