#!/usr/bin/env python3
"""Build a canonical Phaistos Disc word corpus by diffing three PUBLISHED transcriptions.

Sources (all quoted on the en.wikipedia.org "Phaistos Disc" article, but each
originating in a different publication, which is what makes the diff meaningful):

  E = Evans-number transcription, after Achterberg, Best, Enzler, Rietveld &
      Woudhuizen, *The Phaistos Disc: a Luwian Letter to Nestor* (2004).
  U = Unicode transcription, after Everson & Jenkins, "Proposal for encoding the
      Phaistos Disc characters in the SMP of the UCS", ISO/IEC JTC1/SC2/WG2 N3066R
      (L2/06-095R, 2006).  Sign N == U+101D0 + (N-1); U+101FD == combining oblique stroke.
  P = Pictorial transcription, after Godart, *The Phaistos Disc: the enigma of an
      Aegean script* (1995); recovered from the glyph-image filenames.

Emits data/phaistos_words.csv and prints a full three-way diff.
Two conventions inherited from the sources and recorded, not silently applied:
  - word A8 ends in an illegible sign, written here as 00 (an unknown, NOT sign 49);
  - the sources print an oblique stroke on A24 which high-resolution images show
    to be a crack.  Kept for comparability with the literature; flagged below and
    ablated in the analysis.
"""
import csv, os, re, sys, json

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, "data", "raw")

OBLIQUE = "\U000101fd"
ILLEGIBLE = 0            # our code for the unreadable sign in A8


def u_to_sign(ch):
    cp = ord(ch)
    if cp == 0x2370:      # boxed question mark used for the illegible sign
        return ILLEGIBLE
    if 0x101D0 <= cp <= 0x101FC:
        return cp - 0x101D0 + 1
    raise ValueError("not a Phaistos codepoint: %r U+%04X" % (ch, cp))


def strip_markup(line):
    line = re.sub(r"<[^>]*>", " ", line)
    line = line.replace("'''", " ")
    line = re.sub(r"^\s*:", " ", line)
    return line


def parse_evans(path):
    """-> list of (side, [ (signs, oblique_flag) ... ]) in reading order."""
    sides = {}
    side = None
    for line in open(path, encoding="utf-8"):
        s = strip_markup(line)
        if "Side A" in s:
            side = "A"; sides[side] = []; continue
        if "Side B" in s:
            side = "B"; sides[side] = []; continue
        if side is None:
            continue
        s = s.replace("¦", "|").replace("^", " ")
        if "|" not in s:
            continue
        for chunk in s.split("|"):
            chunk = chunk.strip()
            if not chunk:
                continue
            obl = chunk.endswith("/")
            chunk = chunk.rstrip("/").strip()
            signs = []
            for tok in chunk.split():
                if tok == "??":
                    signs.append(ILLEGIBLE)
                elif re.fullmatch(r"\d{1,2}", tok):
                    signs.append(int(tok))
                else:
                    raise ValueError("bad token %r in %r" % (tok, chunk))
            if signs:
                sides[side].append((signs, obl))
    return sides


def parse_unicode(path):
    sides = {}
    side = None
    for line in open(path, encoding="utf-8"):
        s = strip_markup(line)
        if "Side A" in s:
            side = "A"; sides[side] = []; continue
        if "Side B" in s:
            side = "B"; sides[side] = []; continue
        if side is None:
            continue
        s = s.replace("¦", "|")
        if "|" not in s:
            continue
        for chunk in s.split("|"):
            chunk = chunk.strip()
            if not chunk:
                continue
            obl = OBLIQUE in chunk
            signs = [u_to_sign(c) for c in chunk if c != OBLIQUE and not c.isspace()]
            if signs:
                sides[side].append((signs, obl))
    return sides


def parse_pictorial(path):
    """The pictorial block encodes each sign as [[File:Phaistos glyph NN*.svg...]].
    Sign 47 is the word-separating radial stroke, 48 the start-of-text stroke,
    49 the illegible sign, 46 the oblique stroke.  Word labels appear as <sup>A1</sup>."""
    sides = {}
    side = None
    for line in open(path, encoding="utf-8"):
        if "Side A" in line:
            side = "A"; sides[side] = []; continue
        if "Side B" in line:
            side = "B"; sides[side] = []; continue
        if side is None:
            continue
        toks = re.findall(r"\[\[File:Phaistos glyph (\d+)[^\]]*\]\]|<sup>([AB]\d+)</sup>", line)
        cur = None
        for g, lab in toks:
            if lab:
                if cur is not None:
                    sides[side].append(cur)
                cur = ([], False, lab)
                continue
            if cur is None:
                continue          # leading separator before first label
            n = int(g)
            signs, obl, lab0 = cur
            if n in (47, 48):     # radial strokes: word boundary, handled by labels
                continue
            elif n == 46:         # oblique stroke
                cur = (signs, True, lab0)
            elif n == 49:
                cur = (signs + [ILLEGIBLE], obl, lab0)
            else:
                cur = (signs + [n], obl, lab0)
        if cur is not None:
            sides[side].append(cur)
    return {k: [(s, o) for s, o, _ in v] for k, v in sides.items()}, \
           {k: [lab for _, _, lab in v] for k, v in sides.items()}


def main():
    E = parse_evans(os.path.join(RAW, "wp_evans.txt"))
    U = parse_unicode(os.path.join(RAW, "wp_unicode.txt"))
    P, labels = parse_pictorial(os.path.join(RAW, "wp_pictorial.txt"))

    report = []
    ok = True
    for side in ("A", "B"):
        n = {"E": len(E[side]), "U": len(U[side]), "P": len(P[side])}
        report.append("side %s word counts: %s" % (side, n))
        if len(set(n.values())) != 1:
            ok = False
            report.append("  !! word-count disagreement on side %s" % side)
            continue
        for i in range(n["E"]):
            e, u, p = E[side][i], U[side][i], P[side][i]
            lab = labels[side][i] if i < len(labels[side]) else "%s%d" % (side, i + 1)
            if not (e[0] == u[0] == p[0]):
                ok = False
                report.append("  DIFF %s signs: E=%s U=%s P=%s" % (lab, e[0], u[0], p[0]))
            if not (e[1] == u[1] == p[1]):
                report.append("  diff %s oblique: E=%s U=%s P=%s" % (lab, e[1], u[1], p[1]))

    rows = []
    for side in ("A", "B"):
        for i, (signs, obl) in enumerate(E[side]):
            lab = labels[side][i] if i < len(labels[side]) else "%s%d" % (side, i + 1)
            rows.append({
                "word_id": lab,
                "side": side,
                "seq": i + 1,
                "n_signs": len(signs),
                "signs": "-".join("%02d" % s for s in signs),
                "oblique": int(obl),
                "has_illegible": int(ILLEGIBLE in signs),
            })

    out = os.path.join(HERE, "data", "phaistos_words.csv")
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    tok = sum(r["n_signs"] for r in rows)
    types = sorted({int(x) for r in rows for x in r["signs"].split("-")} - {ILLEGIBLE})
    report.append("")
    report.append("words: %d (A=%d, B=%d)" % (len(rows),
                  sum(1 for r in rows if r["side"] == "A"),
                  sum(1 for r in rows if r["side"] == "B")))
    report.append("sign tokens incl. illegible: %d" % tok)
    report.append("sign tokens legible: %d" % (tok - sum(r["has_illegible"] for r in rows)))
    report.append("distinct legible signs: %d  -> %s" % (len(types), types))
    report.append("oblique-marked words: %d  -> %s" % (
        sum(r["oblique"] for r in rows), [r["word_id"] for r in rows if r["oblique"]]))
    report.append("three-way agreement on sign sequences: %s" % ("YES" if ok else "NO"))
    txt = "\n".join(report)
    print(txt)
    open(os.path.join(HERE, "results", "corpus_build.txt"), "w").write(txt + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
