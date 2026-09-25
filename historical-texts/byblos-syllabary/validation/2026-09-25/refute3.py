#!/usr/bin/env python3
"""
Part 3 of the 2026-09-25 refuter checks.

The decisive question this part answers: WHAT IS E402?

ME_ANCHOR_TRANSFER.md treats E402 as an ordinary sign and builds a three-sign
lexical unit  E49A-E402-{E48F,E412}  on it. The OCBI font's own glyph name for
E402 is "b I 7  kurzer Worttrenner oben" -- short word divider, upper. This part
tests the divider hypothesis distributionally, without relying on that name,
and then re-reads the three held-out loci under it.
"""
import json, os, random, math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "ocbi_parsed.json")))
T = json.load(open(os.path.join(HERE, "glyphnames.json")))
FR = D["fragments"]
CYL = {"ra", "rb (Var. 1)", "rb (Var. 2)", "rb (Var. 3)",
       "rc (Var. 1)", "rc (Var. 2) ", "rc (Var. 3)", "rd"}
core = [f for f in FR if f["id"] not in CYL]
sign = lambda t: t["kind"] == "sign"
DIV = {"E402", "E404"}          # the two "kurzer Worttrenner" glyphs

print("=" * 78)
print("F. IS E402 A SIGN OR A WORD DIVIDER?  (distributional test, name-free)")
print("=" * 78)
# base rate of edge positions among all off-cylinder sign tokens
tot = ini = fin = 0
for f in core:
    for l in f["lines"]:
        idx = [i for i, t in enumerate(l) if sign(t)]
        for j, i in enumerate(idx):
            tot += 1
            if j == 0: ini += 1
            if j == len(idx) - 1: fin += 1
edge = (ini + fin) / tot
print("  off-cylinder sign tokens: %d ; line-initial %d, line-final %d" % (tot, ini, fin))
print("  P(a random sign token sits at a line edge) = %.4f" % edge)
for cp in ["E402", "E404", "E498", "E41B", "E49A", "E416", "E412"]:
    n = e = 0
    for f in core:
        for l in f["lines"]:
            idx = [i for i, t in enumerate(l) if sign(t)]
            for j, i in enumerate(idx):
                if l[i]["cp"] == cp:
                    n += 1
                    if j == 0 or j == len(idx) - 1: e += 1
    p = (1 - edge) ** n if e == 0 else None
    print("  %-6s %-42s n=%2d edge=%d  %s"
          % (cp, T[cp]["name"], n, e,
             ("P(0 edges | ordinary sign) = %.4f" % p) if p is not None else ""))

print()
print("=" * 78)
print("G. RE-READING THE THREE HELD-OUT LOCI WITH E402 AS A DIVIDER")
print("=" * 78)
for f in core:
    for li, l in enumerate(f["lines"], 1):
        if any(sign(t) and t["cp"] == "E49A" for t in l):
            raw, seg = [], []
            for t in l:
                if sign(t) and t["cp"] in DIV:
                    raw.append("|"); seg.append("|")
                elif sign(t):
                    raw.append(t["cp"] + ("?" if t["guess"] else "")); seg.append(t["cp"])
                else:
                    raw.append("[" + t["kind"][:4] + "]"); seg.append("[" + t["kind"][:4] + "]")
            print("  BYBL %-3s line %d : %s" % (f["id"], li, " ".join(raw)))

print("""
  Under the divider reading:
    BYBL i IX : ... E442 | E49A | E48F E40D? ...   -> E49A is a ONE-SIGN word,
                                                      flanked by dividers
    BYBL k IV : E45A E497 E439 E49A | E412 E45A    -> E49A word-FINAL, E412 in
                                                      the NEXT word
    BYBL m II : [frac][x] E410 E49A | E48F E46B    -> E49A word-FINAL
  The claimed three-sign unit E49A-E402-E48F does not exist; the invariant
  'first internal transition' is the word boundary itself.""")

print()
print("=" * 78)
print("H. IS 'ME IS ALWAYS FOLLOWED BY A DIVIDER' STILL SURPRISING?")
print("=" * 78)
# unconditional
pairs = dv = 0
for f in core:
    for l in f["lines"]:
        for a, b in zip(l, l[1:]):
            if sign(a) and sign(b):
                pairs += 1
                if b["cp"] in DIV: dv += 1
print("  whole off-cylinder corpus : %d adjacent pairs, %d end in a divider -> p=%.4f"
      % (pairs, dv, dv / pairs))
print("    3 of 3 -> naive p = %.3e" % ((dv / pairs) ** 3))
# conditional on the object actually using dividers  (E49A only occurs in i,k,m,
# and i,k,m are all divider-using objects -- that is a selection effect)
divobj = sorted({f["id"] for f in core
                 if any(sign(t) and t["cp"] in DIV for l in f["lines"] for t in l)})
print("  objects that use a divider at all: %s" % ", ".join(divobj))
print("  objects containing off-cylinder E49A: i, k, m  (all three are divider-using)")
p2 = d2 = 0
for f in core:
    if f["id"] not in divobj: continue
    for l in f["lines"]:
        for a, b in zip(l, l[1:]):
            if sign(a) and sign(b):
                p2 += 1
                if b["cp"] in DIV: d2 += 1
print("  restricted to those 6 objects : %d pairs, %d end in a divider -> p=%.4f"
      % (p2, d2, d2 / p2))
print("    3 of 3 -> p = %.3e   (1 in %.0f)" % ((d2 / p2) ** 3, 1 / (d2 / p2) ** 3))
# budget: how many 3-token signs in those objects are always divider-followed?
occ = defaultdict(list)
for f in core:
    if f["id"] not in divobj: continue
    for l in f["lines"]:
        for i, t in enumerate(l):
            if sign(t) and t["cp"] not in DIV:
                nxt = l[i + 1] if i + 1 < len(l) else None
                occ[t["cp"]].append(nxt["cp"] if nxt is not None and sign(nxt) else None)
elig = {k: v for k, v in occ.items() if len(v) >= 3}
hit = [k for k, v in elig.items() if all(x in DIV for x in v)]
print("  signs with >=3 tokens inside those 6 objects: %d ; always divider-followed: %s"
      % (len(elig), hit))

print()
print("=" * 78)
print("I. THE CYLINDER VARIANT-READING BUDGET")
print("=" * 78)
rb = {f["id"]: [t["cp"] for l in f["lines"] for t in l if sign(t)]
      for f in FR if f["id"].startswith("rb")}
rc = {f["id"]: [t["cp"] for l in f["lines"] for t in l if sign(t)]
      for f in FR if f["id"].startswith("rc")}
for k, v in list(rb.items()) + list(rc.items()):
    print("  %-14s %s" % (k, " ".join("%s(%s)" % (c, T[c]["name"].split("  ")[-1][:26]) for c in v)))
ok = []
for kb, vb in rb.items():
    for kc, vc in rc.items():
        shared_term = vb[-1] == vc[-1]
        me_onset = vb[0] in ("E49A", "E4B0") and vc[0] in ("E49A", "E4B0")
        if shared_term and me_onset:
            ok.append((kb, kc))
print("\n  of the %d x %d = %d combinations of OCBI variant readings, the ones where"
      % (len(rb), len(rc), len(rb) * len(rc)))
print("  BOTH daughters start with a ME-family sign AND end with the same exact sign:")
print("   ", ok if ok else "NONE")
print("  -> the two 'external constraints' 3 in PARTIAL_BIGRAPH_KERNEL section 2 select")
print("     1 of %d variant-reading combinations, and that budget is never charged."
      % (len(rb) * len(rc)))
