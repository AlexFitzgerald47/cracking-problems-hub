#!/usr/bin/env python3
"""
Independent re-parse of the OCBI Byblos corpus from the primary machine-readable
source, for the 2026-09-25 refuter validation session.

Source (fetched 2026-09-25):
  https://raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm
  https://raw.githubusercontent.com/elamicon/elamicon/master/src/Specialchars.elm

Marker semantics taken from Specialchars.elm, not from the Hub write-ups:
  's' -> guessMarkerL  (zero-width, OVERLAPS THE PREVIOUS CHARACTER => the
                        preceding glyph is a guess)
  'a' -> fractureMarker (line assumed incomplete at this point)
  'x' -> wildcardChar   (unreadable sign)

Nothing in historical-texts/byblos-syllabary/ is modified by this script.
"""
import re, sys, json, os

HERE = os.path.dirname(os.path.abspath(__file__))

def load(path):
    return open(path, encoding="utf-8").read()

def cp(ch):
    return "%04X" % ord(ch)

FRAG_RE = re.compile(
    r'\{\s*id\s*=\s*"(?P<id>[^"]*)"\s*,\s*source\s*=\s*"(?P<source>[^"]*)"\s*,'
    r'\s*group\s*=\s*"(?P<group>[^"]*)"\s*,\s*dir\s*=\s*(?P<dir>\w+)\s*,'
    r'.*?text\s*=\s*\n?\s*"""(?P<text>.*?)"""', re.S)

def parse_fragments(src):
    frags = []
    for m in FRAG_RE.finditer(src):
        lines = []
        for raw in m.group("text").strip().split("\n"):
            toks = []            # list of dicts
            for ch in raw.strip():
                if ch == "s":
                    if toks:
                        toks[-1]["guess"] = True
                elif ch == "a":
                    toks.append({"cp": "FRACTURE", "guess": False, "kind": "fracture"})
                elif ch == "x":
                    toks.append({"cp": "WILDCARD", "guess": False, "kind": "wildcard"})
                elif ch == " ":
                    continue
                elif 0xE000 <= ord(ch) <= 0xF8FF:
                    toks.append({"cp": cp(ch), "guess": False, "kind": "sign"})
                else:
                    raise ValueError("unexpected char %r in %s" % (ch, m.group("id")))
            lines.append(toks)
        frags.append(dict(id=m.group("id"), source=m.group("source"),
                          group=m.group("group"), dir=m.group("dir"), lines=lines))
    return frags

SYL_RE = re.compile(r'\{ id = "(?P<id>[^"]+)"\s*,\s*name = "(?P<name>[^"]+)"\s*,'
                    r'\s*syllabary = String\.trim\s*"""(?P<body>.*?)"""', re.S)

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

def main():
    src = load(os.path.join(HERE, "Byblos.elm"))
    frags = parse_fragments(src)
    syls = parse_syllabaries(src)
    json.dump(dict(fragments=frags, syllabaries=syls),
              open(os.path.join(HERE, "ocbi_parsed.json"), "w"), indent=1)
    nsign = sum(1 for f in frags for l in f["lines"] for t in l if t["kind"] == "sign")
    print("fragments: %d   sign tokens: %d   syllabaries: %d"
          % (len(frags), nsign, len(syls)))
    print("fragment ids:", ", ".join(f["id"] for f in frags))

if __name__ == "__main__":
    main()
