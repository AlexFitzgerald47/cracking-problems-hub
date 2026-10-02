#!/usr/bin/env python3
"""
REFUTER ATTACK 4 -- THE CYLINDER'S OWN STANDING.

PROBLEM.md concedes "the seal's provenance/script classification is not
equivalent to a stratified Dunand find, so every use of it must state that
dependency", and PARTIAL_BIGRAPH_KERNEL.md repeats that restraint.  Neither
asks the obvious quantitative question: DOES THE SEAL USE THE BYBLOS SIGNARY?

If a putative witness of a script shares few or no sign forms with the rest of
the corpus, its classification as that script is carried entirely by the shapes
of signs attested nowhere else -- and an alignment built on those signs cannot
be checked against anything.

Test: for every witness, what fraction of its distinct sign forms also occur on
some OTHER witness?  Small witnesses will score low by sampling alone, so the
seal is compared against a size-matched null built from the other witnesses.
"""
import collections, random, statistics
import lib_ocbi as L

random.seed(20261002)
src = L.load_src()
frags = L.parse_fragments(src)
GN = L.glyphnames()


def nm(c):
    return GN.get(c, {}).get("name", "?")


# physical witness = fragment id with the variant/face suffix stripped,
# except that the seal's four columns ra-rd are ONE object.
def witness(fid):
    base = fid.split(" (")[0].strip()
    if base in ("ra", "rb", "rc", "rd"):
        return "r (the Garbini cylinder seal)"
    return base


w_signs = collections.defaultdict(collections.Counter)
for f in frags:
    for ln in f["lines"]:
        for t in ln:
            if t["kind"] == "sign":
                w_signs[witness(f["id"])][t["cp"]] += 1

allw = sorted(w_signs)
print("=" * 78)
print("Q1.  HOW MUCH OF EACH WITNESS'S SIGN SET IS ATTESTED ELSEWHERE?")
print("=" * 78)
rows = []
for w in allw:
    mine = set(w_signs[w])
    others = set()
    for w2 in allw:
        if w2 != w:
            others |= set(w_signs[w2])
    shared = mine & others
    rows.append((len(shared) / len(mine), len(mine), len(shared),
                 sum(w_signs[w].values()), w))
rows.sort()
print("  share  |types|shared|tokens| witness")
for fr, nt, ns, tok, w in rows:
    print("  %.3f  | %3d | %3d  | %4d | %s" % (fr, nt, ns, tok, w))

seal = "r (the Garbini cylinder seal)"
sealset = set(w_signs[seal])
others = set()
for w2 in allw:
    if w2 != seal:
        others |= set(w_signs[w2])
seal_shared = sealset & others
print()
print("  THE SEAL: %d distinct forms, %d of them attested on any other witness"
      % (len(sealset), len(seal_shared)))
print("  forms UNIQUE to the seal in the whole OCBI corpus:")
for c in sorted(sealset - others):
    print("     %-6s %s" % (c, nm(c)))
print("  forms shared with the rest of the corpus:")
for c in sorted(seal_shared):
    tot = sum(w_signs[w][c] for w in allw if w != seal)
    print("     %-6s n=%-3d elsewhere  %s" % (c, tot, nm(c)))

print()
print("=" * 78)
print("Q2.  SIZE-MATCHED NULL: is the seal unusual, or just small?")
print("=" * 78)
pool = []
for w in allw:
    if w == seal:
        continue
    for c, n in w_signs[w].items():
        pool += [(w, c)] * n
ntok = sum(w_signs[seal].values())
print("  Draw %d sign tokens at random from the non-seal corpus (preserving its" % ntok)
print("  token frequencies) and ask what fraction of the DISTINCT forms drawn")
print("  are attested outside the drawing.  Since every drawn form is by")
print("  construction attested elsewhere this would be 1.0, so instead the null")
print("  is built per-witness: for each real non-seal witness, compute its own")
print("  share and compare like-for-like on size.")
xs = [(nt, fr) for fr, nt, ns, tok, w in rows if w != seal]
print("  non-seal witnesses, share of own sign types attested elsewhere:")
print("    n_types  share")
for nt, fr in sorted(xs):
    print("    %4d     %.3f" % (nt, fr))
small = [fr for nt, fr in xs if nt <= 25]
print()
print("  witnesses with <=25 distinct forms (seal has %d): n=%d, median share %.3f,"
      % (len(sealset), len(small), statistics.median(small)))
print("  min %.3f, max %.3f" % (min(small), max(small)))
sealfr = len(seal_shared) / len(sealset)
print("  SEAL share = %.3f -> %d of %d size-matched witnesses score lower."
      % (sealfr, sum(1 for f in small if f < sealfr), len(small)))

print()
print("=" * 78)
print("Q3.  WHICH SIGNS CARRY THE ALIGNMENT?")
print("=" * 78)
anchors = {"E49A": "ME (rb)", "E4B0": "ME' (rc)", "E44D": "PA (ra)",
           "E4AF": "ATON terminal", "E42A": "AMUN 1st", "E483": "AMUN 2nd",
           "E416": "the split's other member", "E491": "the 'T-bearing' sign"}
for c, lab in anchors.items():
    out = sum(w_signs[w][c] for w in allw if w != seal)
    onw = sorted(w for w in allw if w != seal and w_signs[w][c])
    print("  %-6s %-24s off-seal tokens=%-3d on witnesses %s"
          % (c, lab, out, ", ".join(onw) if onw else "-- NONE --"))
print()
print("  Of the eight forms that the whole partial bigraph is built on, the")
print("  following are attested ONLY on the seal: %s"
      % ", ".join(c for c in anchors if not any(w != seal and w_signs[w][c] for w in allw)))

print()
print("=" * 78)
print("Q4.  EXTERNAL RECORD ON THE OBJECT (for the verdict file)")
print("=" * 78)
for line in [
    "Garbini, G.; Luiselli, M.M. & Devoto, G. (2004), 'Sigillo di eta amarniana",
    "  da Biblo con iscrizione', Rendiconti dell'Accademia Nazionale dei Lincei",
    "  9/15, 377-390 -- the seal's only primary publication.  Neither",
    "  PARTIAL_BIGRAPH_KERNEL.md nor PROBLEM.md cites it; both cite only",
    "  Maeder and Schmutz & Maeder, who cite Garbini et al. 2004 for the object.",
    "Colless (2019, cryptcracker.blogspot.com, 'WEST SEMITIC CYLINDER STAMPS')",
    "  records the provenance as 'apparently emanating from somewhere in",
    "  Phoenicia, possibly Byblos (Gubla)' -- i.e. no excavation context at all,",
    "  and the attribution to Byblos is itself an inference.",
    "GEAS's own 2021 anchor page calls it 'the historisizing Garbini (2004)",
    "  seal'.  Neither the word 'historicizing' nor Garbini's publication",
    "  appears in the Hub files.",
    "Colless (2019) disputes, from the image, exactly the two observations the",
    "  kernel's constraint (3) rests on: \"I would have to say that these '2'",
    "  letters are not the same\" and \"the signs at the bottom of the cartouches",
    "  are similar but not the same\".  OCBI itself encodes that disagreement as",
    "  its rc Var. 2, whose terminal is E4FD and not E4AF.",
]:
    print("  " + line)
