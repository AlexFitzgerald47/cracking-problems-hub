#!/usr/bin/env python3
"""Blind reproduction of published descriptive facts about the Disc.

None of these facts was used to build data/phaistos_words.csv (that file comes
from diffing three transcriptions).  If the pipeline cannot recover them, it has
a bug, not a discovery.

Published claims tested (en.wikipedia.org "Phaistos Disc", citing Godart 1995):
  C1  241 sign tokens, 45 distinct signs
  C2  61 words: 31 on side A, 30 on side B; word lengths 2 to 7 signs
  C3  "The nine hapaxes are 04 (A5), 05 (B3), 11 (A13), 15 (B8), 17 (A24),
       30 (B27), 42 (B9), 43 (B4), 44 (A7)."
  C4  "Of the eight twice-occurring symbols, four (03, 21, 28, 41) occur on
       side A only, three (09, 16, 20) on side B only, and only one (14)
       occurs on both sides."
"""
import csv, os, json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(HERE, "data", "phaistos_words.csv"))))
for r in rows:
    r["signs"] = [int(x) for x in r["signs"].split("-")]
    r["n_signs"] = int(r["n_signs"]); r["oblique"] = int(r["oblique"])

LEG = [s for r in rows for s in r["signs"] if s != 0]
freq = Counter(LEG)
sides = defaultdict(set)
for r in rows:
    for s in r["signs"]:
        if s: sides[s].add(r["side"])

out, passed, failed = [], 0, 0
def check(name, got, want):
    global passed, failed
    ok = got == want
    passed += ok; failed += (not ok)
    out.append("%-5s %-48s got=%s%s" % ("PASS" if ok else "FAIL", name, got,
               "" if ok else "  want=%s" % (want,)))

check("C1 tokens (legible)", len(LEG), 241)
check("C1 distinct signs", len(freq), 45)
check("C2 words", len(rows), 61)
check("C2 side A words", sum(1 for r in rows if r["side"]=="A"), 31)
check("C2 side B words", sum(1 for r in rows if r["side"]=="B"), 30)
check("C2 min word length", min(r["n_signs"] for r in rows), 2)
check("C2 max word length", max(r["n_signs"] for r in rows), 7)

hapax = sorted(s for s,c in freq.items() if c == 1)
check("C3 hapax count", len(hapax), 9)
check("C3 hapax set", hapax, [4,5,11,15,17,30,42,43,44])
# which word each hapax sits in
hloc = {}
for r in rows:
    for s in r["signs"]:
        if s in hapax: hloc[s] = r["word_id"]
check("C3 hapax locations", [hloc[s] for s in hapax],
      ["A5","B3","A13","B8","A24","B27","B9","B4","A7"])

two = sorted(s for s,c in freq.items() if c == 2)
check("C4 doubleton count", len(two), 8)
check("C4 doubleton set", two, [3,9,14,16,20,21,28,41])
check("C4 side-A-only doubletons", sorted(s for s in two if sides[s]=={"A"}), [3,21,28,41])
check("C4 side-B-only doubletons", sorted(s for s in two if sides[s]=={"B"}), [9,16,20])
check("C4 both-sides doubletons", sorted(s for s in two if sides[s]=={"A","B"}), [14])

out.append("")
out.append("%d/%d published descriptive claims reproduced" % (passed, passed+failed))
out.append("")
out.append("word-length distribution (n signs -> count): %s" %
           dict(sorted(Counter(r["n_signs"] for r in rows).items())))
out.append("mean word length %.3f signs" % (sum(r["n_signs"] for r in rows)/len(rows)))
out.append("top sign frequencies: %s" % freq.most_common(12))
txt = "\n".join(out)
print(txt)
open(os.path.join(HERE,"results","reproduce.txt"),"w").write(txt+"\n")
