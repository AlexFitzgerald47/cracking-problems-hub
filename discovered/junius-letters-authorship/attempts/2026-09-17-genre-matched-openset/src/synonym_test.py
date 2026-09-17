#!/usr/bin/env python3
"""Ellegard-style synonym-choice variables, with the competitor count that the
original argument omits.

WHAT IS AND IS NOT VERIFIED HERE. Alvar Ellegard, *A Statistical Method for
Determining Authorship: The Junius Letters 1769-1772* (1962), built his case on a
large set of lexical and synonym-choice variables. I have NOT read the 1962
monograph in this session and I do not assert which specific pairs he used or what
weights he assigned. What is tested below is the *method* -- binary synonym
preference as an authorship discriminator -- on the pairs that are standard in the
secondary literature and that the Hub's 2026-09-05 session inspected directly in the
primary texts (among/amongst, farther/further, till/until). The remaining pairs are
added by me as additional instances of the same variable type. Treat the pair list as
mine, not as a reconstruction of Ellegard's.

THE POINT OF THE EXERCISE. The received argument runs: Junius prefers X, Francis
prefers X, therefore Francis is Junius. That argument has no denominator. The
question that decides whether a shared preference is evidence is "how many other
writers of the period share it?" -- the board's standing rule to count the
competitors rather than score one. This script computes each author's preference on
each pair and then counts, for every pair, how many panel authors agree with Junius.
"""
import json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")

PAIRS = [
    ("among", "amongst"),
    ("farther", "further"),
    ("till", "until"),
    ("toward", "towards"),
    ("while", "whilst"),
    ("on", "upon"),
    ("among", "amidst"),
    ("betwixt", "between"),
    ("hath", "has"),
    ("doth", "does"),
]


def counts_for(texts):
    c = Counter()
    for t in texts:
        c.update(C.tokens(t))
    return c


def main():
    os.makedirs(RES, exist_ok=True)
    by_author = defaultdict(list)     # (author, genre) -> texts
    for d in C.load_jsonl("panel_chunks.jsonl"):
        by_author[(d["author"], d["genre"])].append(d["text"])
    for name in ("junius_1813_ocr.jsonl",):
        for d in C.load_jsonl(name):
            by_author[(d["author"], d["genre"])].append(d["text"])

    rows = []
    for (author, genre), texts in sorted(by_author.items()):
        c = counts_for(texts)
        total = sum(c.values())
        row = dict(author=author, genre=genre, n_docs=len(texts), n_tokens=total)
        for a, b in PAIRS:
            na, nb = c[a], c[b]
            key = f"{a}/{b}"
            row[key + "_n"] = f"{na}/{nb}"
            row[key] = (na / (na + nb)) if (na + nb) >= 10 else None
        rows.append(row)

    with open(os.path.join(RES, "synonym_preferences.json"), "w") as f:
        json.dump(rows, f, indent=1)

    # ---- report ----------------------------------------------------------
    hdr = f"{'author':22s} {'genre':16s} {'tokens':>8s} " + " ".join(f"{a[:6]}/{b[:6]:<7s}" for a, b in PAIRS[:5])
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        cells = []
        for a, b in PAIRS[:5]:
            v = r[f"{a}/{b}"]
            cells.append("   n/a    " if v is None else f"  {v:.2f}     ")
        print(f"{r['author']:22s} {r['genre']:16s} {r['n_tokens']:8d} " + "".join(cells))

    print("\nProportion is of the FIRST member of the pair. n/a = fewer than 10 joint")
    print("occurrences, i.e. the variable has no power on that author's sample.\n")

    # ---- competitor count ------------------------------------------------
    jun = next((r for r in rows if r["author"] == "Junius"), None)
    if jun is None:
        print("No Junius sample in panel yet; competitor count skipped.")
        return
    print("COMPETITOR COUNT -- how many panel authors share Junius's preference\n")
    print(f"{'variable':22s} {'Junius':>8s}  {'agree':>5s}/{'testable':>8s}   agreeing authors")
    others = [r for r in rows if r["author"] not in ("Junius", "Philo_Junius")]
    for a, b in PAIRS:
        key = f"{a}/{b}"
        jv = jun[key]
        if jv is None:
            print(f"{key:22s} {'n/a':>8s}   -- no power on the Junius sample")
            continue
        testable = [r for r in others if r[key] is not None]
        jside = jv > 0.5
        agree = [r for r in testable if (r[key] > 0.5) == jside]
        names = ", ".join(sorted({r['author'] for r in agree}))
        print(f"{key:22s} {jv:8.2f}  {len(agree):5d}/{len(testable):8d}   {names}")


if __name__ == "__main__":
    main()
