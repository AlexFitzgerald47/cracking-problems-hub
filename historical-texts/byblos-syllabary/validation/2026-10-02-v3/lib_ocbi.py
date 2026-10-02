#!/usr/bin/env python3
"""
Independent re-parse of the OCBI Byblos corpus for the 2026-10-02 REFUTER
(validator 3) session.  Written from the primary source, not from the
2026-09-25 session's ocbi_parsed.json.

Primary sources, re-fetched 2026-10-02 and verified byte-identical (md5) to the
copies held in validation/2026-09-25/:
  https://raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm
      md5 bbfb29fd2605d33999d9a7dc43c55797
  https://raw.githubusercontent.com/elamicon/elamicon/master/src/Specialchars.elm
      md5 da866ec156a6ccf134f05d6e0d8de563

Marker semantics are taken from the Byblos.elm source comment itself:
    -- In the source material "s" is a guessmark and "a" marks a fracture
    -- whereas x is a placeholder for unreadable glyphs.
  replaceGuessmark = Token.replace 's' guessMarkerL      (E7E1)
  replaceFracture  = Token.replace 'a' fractureMarker    (E7E0)
  replaceWildcard  = Token.replace 'x' wildcardChar      (E7E3)
and from Specialchars.elm: guessmarkers are ZERO WIDTH and OVERLAP THE PREVIOUS
character, i.e. 's' marks the glyph that PRECEDES it as hard to read.

Difference from the 2026-09-25 parser (deliberate, documented):
  * a run of spaces inside a line is preserved as a SEGMENT BREAK token, so
    that adjacency is never asserted across a visible gap in the transcription
    (Byblos.elm fragment "c" last line contains "xa   a<E453>...").
  * witness-variant handling is explicit: see CANON below.

Nothing under historical-texts/byblos-syllabary/ outside this directory is
modified by this file.
"""
import re, os, json

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Byblos.elm.fetched20261002")
GLYPHNAMES = os.path.join(HERE, "..", "2026-09-25", "glyphnames.json")

CYLINDER = {"ra", "rb (Var. 1)", "rb (Var. 2)", "rb (Var. 3)",
            "rc (Var. 1)", "rc (Var. 2) ", "rc (Var. 3)", "rd"}

# One reading per physical witness.  For the seal we keep the Hub's own
# preferred readings (rb/rc Var. 3) so that we never weaken its case by
# picking a different variant; for o/a' we keep Var. 1.
CANON_DROP = {"o (verso) Var. 2", "a' (Var. 2)",
              "rb (Var. 1)", "rb (Var. 2)", "rc (Var. 1)", "rc (Var. 2) "}

FRAG_RE = re.compile(
    r'\{\s*id\s*=\s*"(?P<id>[^"]*)"\s*,\s*source\s*=\s*"(?P<source>[^"]*)"\s*,'
    r'\s*group\s*=\s*"(?P<group>[^"]*)"\s*,\s*dir\s*=\s*(?P<dir>\w+)\s*,'
    r'.*?text\s*=\s*\n?\s*"""(?P<text>.*?)"""', re.S)

SYL_RE = re.compile(r'\{ id = "(?P<id>[^"]+)"\s*,\s*name = "(?P<name>[^"]+)"\s*,'
                    r'\s*syllabary = String\.trim\s*"""(?P<body>.*?)"""', re.S)


def cp(ch):
    return "%04X" % ord(ch)


def load_src():
    return open(SRC, encoding="utf-8").read()


def parse_fragments(src):
    frags = []
    for m in FRAG_RE.finditer(src):
        lines = []
        for raw in m.group("text").strip("\n").split("\n"):
            toks, pending_space = [], False
            for ch in raw.strip():
                if ch == " ":
                    pending_space = True
                    continue
                if pending_space and toks:
                    toks.append({"cp": "GAP", "kind": "gap", "guess": False})
                pending_space = False
                if ch == "s":
                    if toks and toks[-1]["kind"] in ("sign", "wildcard"):
                        toks[-1]["guess"] = True
                elif ch == "a":
                    toks.append({"cp": "FRACTURE", "kind": "fracture", "guess": False})
                elif ch == "x":
                    toks.append({"cp": "WILDCARD", "kind": "wildcard", "guess": False})
                elif 0xE000 <= ord(ch) <= 0xF8FF:
                    toks.append({"cp": cp(ch), "kind": "sign", "guess": False})
                else:
                    raise ValueError("unexpected char %r in %s" % (ch, m.group("id")))
            lines.append(toks)
        frags.append(dict(id=m.group("id"), source=m.group("source"),
                          group=m.group("group"), dir=m.group("dir"), lines=lines))
    return frags


def parse_syllabaries(src):
    out = []
    for m in SYL_RE.finditer(src):
        groups = []
        for line in m.group("body").strip().split("\n"):
            g = [cp(c) for c in line.strip() if 0xE000 <= ord(c) <= 0xF8FF]
            if g:
                groups.append(g)
        out.append(dict(id=m.group("id"), name=m.group("name"), groups=groups))
    return out


def parse_syllable_map(src):
    m = re.search(r'syllableMap = String\.trim\s*"""(.*?)"""', src, re.S)
    out = []
    for line in m.group(1).strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        label = parts[0]
        signs = [cp(c) for c in parts[1] if 0xE000 <= ord(c) <= 0xF8FF] if len(parts) > 1 else []
        out.append((label, signs))
    return out


def classmap(syl):
    """codepoint -> grapheme class id, for one syllabary definition."""
    d = {}
    for i, g in enumerate(syl["groups"]):
        for c in g:
            d.setdefault(c, i)
    return d


def glyphnames():
    try:
        return json.load(open(os.path.join(HERE, "..", "2026-09-25", "glyphnames.json")))
    except Exception:
        return {}


def corpus(canon=True, off_cylinder=True, clear_only=False):
    """Return list of (fragid, lineno, [tokens]) after filtering."""
    frags = parse_fragments(load_src())
    out = []
    for f in frags:
        if canon and f["id"] in CANON_DROP:
            continue
        if off_cylinder and f["id"] in CYLINDER:
            continue
        for ln, toks in enumerate(f["lines"], 1):
            if clear_only:
                toks = [t for t in toks if not (t["kind"] == "sign" and t["guess"])] \
                    if False else toks
            out.append((f["id"], ln, toks))
    return out


def runs(lines, allow_guess=True):
    """Maximal runs of consecutive SIGN tokens, broken by wildcard / fracture /
    gap / line end.  These are the only places where adjacency is asserted by
    the transcription."""
    out = []
    for fid, ln, toks in lines:
        cur = []
        for t in toks:
            if t["kind"] == "sign" and (allow_guess or not t["guess"]):
                cur.append(t)
            else:
                if cur:
                    out.append((fid, ln, cur))
                cur = []
        if cur:
            out.append((fid, ln, cur))
    return out


if __name__ == "__main__":
    src = load_src()
    frags = parse_fragments(src)
    syls = parse_syllabaries(src)
    n = sum(1 for f in frags for l in f["lines"] for t in l if t["kind"] == "sign")
    print("fragment entries: %d   sign tokens (all variants): %d   syllabaries: %d"
          % (len(frags), n, len(syls)))
    can = corpus(canon=True, off_cylinder=True)
    nt = sum(1 for _, _, toks in can for t in toks if t["kind"] == "sign")
    print("canonical off-cylinder: %d lines, %d sign tokens" % (len(can), nt))
    print("syllableMap:", parse_syllable_map(src))
