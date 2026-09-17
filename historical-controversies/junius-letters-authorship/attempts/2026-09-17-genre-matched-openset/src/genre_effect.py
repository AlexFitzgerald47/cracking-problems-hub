#!/usr/bin/env python3
"""How much does GENRE move a synonym-choice variable, compared with how much AUTHOR
moves it?

This is the control the Junius/Francis argument has never had. Junius is polemical
newspaper prose; Philip Francis's best-attested acknowledged writing is private family
correspondence. If a variable shifts as much between two registers of ONE author as it
does between two authors, then a Junius/Francis difference on that variable is not
evidence about authorship, and neither is a Junius/Francis agreement.

Three authors in the panel have both private letters and published formal prose:
Burke, Johnson and Hume. For each variable we report the within-author between-genre
shift for each of them, alongside the between-author spread within the private-letter
genre. Any variable whose genre shift is comparable to its author spread is unusable
for this problem and is reported as such.
"""
import json, os, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import corpus as C
from synonym_test import PAIRS

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")

MIN_JOINT = 25


def prop(counter, a, b):
    n = counter[a] + counter[b]
    return (counter[a] / n, n) if n >= MIN_JOINT else (None, n)


def main():
    cells = defaultdict(Counter)          # (author, genre) -> token counts
    for d in C.load_jsonl("panel_chunks.jsonl"):
        cells[(d["author"], d["genre"])].update(C.tokens(d["text"]))
    for d in C.load_jsonl("junius_1813_ocr.jsonl"):
        cells[(d["author"], d["genre"])].update(C.tokens(d["text"]))

    both = [a for a in {k[0] for k in cells}
            if (a, "private_letter") in cells and (a, "published_prose") in cells]
    both.sort()

    out = {}
    print(f"WITHIN-AUTHOR GENRE SHIFT  (private letters -> published prose)\n")
    print(f"{'variable':20s} " + " ".join(f"{a.split('_')[-1][:9]:>18s}" for a in both))
    print("-" * (20 + 19 * len(both)))
    genre_shifts = defaultdict(list)
    for a, b in PAIRS:
        key = f"{a}/{b}"
        cellstr = []
        for au in both:
            p1, n1 = prop(cells[(au, "private_letter")], a, b)
            p2, n2 = prop(cells[(au, "published_prose")], a, b)
            if p1 is None or p2 is None:
                cellstr.append(f"{'--':>18s}")
            else:
                genre_shifts[key].append(abs(p2 - p1))
                cellstr.append(f"{p1:.2f} -> {p2:.2f} ({p2-p1:+.2f})".rjust(18))
        print(f"{key:20s} " + " ".join(cellstr))

    # between-author spread inside the private-letter genre
    print(f"\n\nBETWEEN-AUTHOR SPREAD inside the private-letter genre, versus the")
    print(f"largest within-author genre shift observed above.\n")
    print(f"{'variable':20s} {'authors':>7s} {'min':>6s} {'max':>6s} {'spread':>7s}"
          f" {'max genre shift':>16s}   verdict")
    print("-" * 92)
    for a, b in PAIRS:
        key = f"{a}/{b}"
        vals = []
        for (au, g), c in cells.items():
            if g != "private_letter":
                continue
            p, n = prop(c, a, b)
            if p is not None:
                vals.append(p)
        gs = max(genre_shifts[key]) if genre_shifts[key] else None
        if len(vals) < 3 or gs is None:
            print(f"{key:20s} {len(vals):7d}      -      -       -"
                  f" {'--':>16s}   untestable")
            out[key] = dict(spread=None, max_genre_shift=gs, verdict="untestable")
            continue
        spread = max(vals) - min(vals)
        verdict = "UNUSABLE - genre shift >= author spread" if gs >= spread * 0.6 \
            else "usable"
        print(f"{key:20s} {len(vals):7d} {min(vals):6.2f} {max(vals):6.2f} {spread:7.2f}"
              f" {gs:16.2f}   {verdict}")
        out[key] = dict(spread=round(spread, 3), max_genre_shift=round(gs, 3),
                        verdict=verdict)

    os.makedirs(RES, exist_ok=True)
    with open(os.path.join(RES, "genre_effect.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
