#!/usr/bin/env python3
"""Build the English reference used by the MASC null.

Source: Project Gutenberg #2173 (Burke, public domain), already committed in
this repository under the Junius attempt. Reduced here to a letters-only
stream so the null draws windows from real English prose, not from a
frequency table.
"""
import os
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "..", "..", "..", "..",
                   "historical-controversies/junius-letters-authorship/attempts/"
                   "2026-09-17-genre-matched-openset/data/raw/gutenberg_2173.txt")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data",
                   "english_reference.txt")
t = open(SRC, encoding="utf-8", errors="ignore").read().upper()
t = "".join(ch for ch in t if "A" <= ch <= "Z")
t = t[20000:170000]          # skip front matter, keep 150k letters
open(OUT, "w").write(t)
print("english_reference.txt:", len(t), "letters")
