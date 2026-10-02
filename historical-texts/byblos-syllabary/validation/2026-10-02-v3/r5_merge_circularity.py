#!/usr/bin/env python3
"""
REFUTER ATTACK 2 -- IS THE E416 != E4AF "EXTERNAL ADJUDICATION" IDENTIFIED?

The kernel's one claimed NEW result is:
    "the external name alignment supplies a non-circular reason to split the
     old E416 / E4AF variant group"
on the argument that rb Var.3 = E49A E416 E491 E4AF "contains both E416 and
E4AF in the same four-sign name", so treating them as one grapheme "forces an
otherwise unnecessary polyfunctionality".

Four tests of that inference:
  N1  variant dependence: does the SAME argument, applied to the other OCBI
      readings of the same two columns, yield a DIFFERENT split?
  N2  is the premise ("a grapheme may not occur twice in a four-sign proper
      name") supported by the corpus, or is repetition inside a 4-sign window
      ordinary?
  N3  is the kernel's own anchor set self-consistent on polyfunctionality?
  N4  after the split, is the 'ATON' grapheme class still cylinder-only --
      i.e. does the split do any work beyond the cylinder?
"""
import collections, itertools
import lib_ocbi as L

src = L.load_src()
frags = L.parse_fragments(src)
syls = L.parse_syllabaries(src)
GN = L.glyphnames()
byid = {f["id"]: f for f in frags}


def nm(c):
    return GN.get(c, {}).get("name", "?")


def seq(fid):
    return [t["cp"] for t in byid[fid]["lines"][0] if t["kind"] == "sign"]


print("=" * 78)
print("N1.  VARIANT DEPENDENCE OF THE SPLIT")
print("=" * 78)
print("  The merged group that the kernel wants split.  In the default/search")
print("  inventory and in syl1-syl5, the group containing E4AF is:")
for s in syls:
    for g in s["groups"]:
        if "E4AF" in g:
            print("    %-7s group = %s" % (s["id"], " ".join(g)))
print()
print("  Now apply the kernel's own inference -- 'two members of one merged")
print("  group inside one four-sign name is an unnecessary polyfunctionality,")
print("  therefore split them' -- to each OCBI reading of rb and rc:")
for s in syls:
    cm = L.classmap(s)
    if s["id"] != "search":
        continue
    for fid in ["rb (Var. 1)", "rb (Var. 2)", "rb (Var. 3)",
                "rc (Var. 1)", "rc (Var. 2) ", "rc (Var. 3)"]:
        q = seq(fid)
        byclass = collections.defaultdict(list)
        for c in q:
            byclass[cm.get(c, "u" + c)].append(c)
        clash = {k: v for k, v in byclass.items() if len(set(v)) > 1}
        msg = "no two distinct forms of one class" if not clash else \
            "; ".join("class %s holds %s" % (k, "+".join(sorted(set(v)))) for k, v in clash.items())
        print("    %-14s %s" % (fid, msg))
print()
print("  -> rb Var. 1 and Var. 2 (E4FF E49A E4AE E4AF) put E4AE and E4AF -- two")
print("     forms OCBI names with the SAME motif ('%s' / '%s')" % (nm("E4AE").split("   ")[-1], nm("E4AF").split("   ")[-1]))
print("     inside the same four-sign name.  The kernel's inference, applied to")
print("     those readings, would demand E4AE != E4AF, a DIFFERENT split, and")
print("     one that cuts across OCBI's own motif naming.")
print("  -> rc Var. 2 (E4B0 E4B1 E4B2 E4FD) does not end in E4AF at all; its")
print("     terminal E4FD is another member of the same merged group, so under")
print("     that reading the two sisters do NOT share 'the exact same terminal")
print("     sign' and constraint (3) of kernel section 2 is false.")
print("  The conclusion is therefore not identified by the evidence: which")
print("  grapheme pair gets split is decided by which of the nine OCBI readings")
print("  is adopted, and the kernel adopts Var.3/Var.3 without argument.")

print()
print("=" * 78)
print("N2.  IS REPETITION INSIDE A FOUR-SIGN WINDOW ACTUALLY 'UNNECESSARY'?")
print("=" * 78)
off = L.corpus(canon=True, off_cylinder=True)
rs = L.runs(off)
wins = []
for fid, ln, r in rs:
    s = [t["cp"] for t in r]
    for i in range(len(s) - 3):
        wins.append(tuple(s[i:i + 4]))
print("  off-cylinder 4-sign windows: %d" % len(wins))
for s in syls:
    cm = L.classmap(s)
    same_class_two_forms = 0
    identical_repeat = 0
    for w in wins:
        cs = [cm.get(c, "u" + c) for c in w]
        cc = collections.Counter(cs)
        if any(v > 1 for v in cc.values()):
            same_class_two_forms += 1
        if len(set(w)) < 4:
            identical_repeat += 1
    print("    %-7s windows with >=2 tokens of ONE grapheme class: %4d (%.1f%%)"
          "   with an identical form repeated: %4d (%.1f%%)"
          % (s["id"], same_class_two_forms, 100 * same_class_two_forms / len(wins),
             identical_repeat, 100 * identical_repeat / len(wins)))
print()
print("  -> Under the inventories the kernel calls 'merged' (search, syl1-syl5)")
print("     a large fraction of all four-sign stretches in the real corpus")
print("     already contain two tokens of one grapheme class.  The configuration")
print("     the kernel treats as an anomaly requiring a split is the ordinary")
print("     case.  The premise of the inference is not supported.")
print("  -> Note also that mixed logographic + phonetic use of ONE sign inside")
print("     one name is standard in the Egyptian system the script is said to")
print("     imitate, so 'polyfunctionality' is not a cost that excludes.")

print()
print("=" * 78)
print("N3.  THE KERNEL'S OWN ANCHORS BREAK THE SAME RULE")
print("=" * 78)
smap = L.parse_syllable_map(src)
print("  OCBI syllableMap (the only machine-readable sound map in the source):")
for lab, signs in smap:
    print("     %-6s %s   %s" % (lab, " ".join(signs),
                                 " / ".join(nm(c).split("   ")[-1] for c in signs)))
tok = [t["cp"] for _, _, r in rs for t in r]
cnt = collections.Counter(tok)
rank = {c: i + 1 for i, (c, _) in enumerate(cnt.most_common())}
print()
print("  E42A is mapped to the single value 'i' AND is the first half of the")
print("  two-sign logogram 'AMUN'.  Off-cylinder it is the #%s most frequent"
      % rank.get("E42A"))
print("  form in the corpus (%d tokens of %d)." % (cnt.get("E42A", 0), len(tok)))
print("  So the kernel accepts, inside the six-sign name ra, exactly the")
print("  polyfunctionality it refuses to accept inside the four-sign name rb.")
print("  E483 off-cylinder tokens: %d" % cnt.get("E483", 0))
print()
print("  The kernel further declares the source's 'ATON E416' mapping 'stale")
print("  residue'.  Two things to note:")
print("    * E416 is named '%s' -- an open ring, i.e. a plausible" % nm("E416").split("   ")[-1])
print("      sun-disc; E4AF is named '%s'." % nm("E4AF").split("   ")[-1])
print("      Colless (2019) independently identifies the sun sign on this seal")
print("      as 'a circle with a dot in it' in the SECOND position of the long")
print("      column, i.e. E4AD (%s), not as either." % nm("E4AD").split("   ")[-1])
print("    * if ATON = E416, then rb Var.3 reads me-ATON-?-? and the kernel's")
print("      alignment fails.  The kernel resolves a conflict between its")
print("      alignment and the only machine-readable sound map in its primary")
print("      source by declaring the source stale.  That is an assertion, not")
print("      an external adjudication.  (The GEAS 2021 news page does give")
print("      'E4AF ATON', so GEAS is internally inconsistent with its own tool;")
print("      the kernel's report of the GEAS page is accurate.)")

print()
print("=" * 78)
print("N4.  AFTER THE SPLIT, DOES THE ATON CLASS LEAVE THE CYLINDER?")
print("=" * 78)
allfr = L.parse_fragments(src)
loc = collections.defaultdict(lambda: [0, 0])   # cp -> [on-cyl, off-cyl]
for f in allfr:
    oncyl = f["id"] in L.CYLINDER
    if (not oncyl) and f["id"] in L.CANON_DROP:
        continue            # off-cylinder: one reading per witness
    # on-cylinder: ALL OCBI variant readings are counted, so that no form the
    # seal might carry under some reading is silently dropped
    for ln in f["lines"]:
        for t in ln:
            if t["kind"] == "sign":
                loc[t["cp"]][0 if oncyl else 1] += 1
for c in ["E4AF", "E4AE", "E4FD", "E416", "E495", "E49A", "E4B0", "E44D", "E42A", "E483"]:
    print("    %-6s on-cylinder %2d  off-cylinder %3d   %s"
          % (c, loc[c][0], loc[c][1], nm(c)))
print()
for s in syls:
    cm = L.classmap(s)
    k = cm.get("E4AF")
    if k is None:
        print("    %-7s E4AF absent from this inventory" % s["id"])
        continue
    members = [c for c, v in cm.items() if v == k]
    offc = sum(loc[c][1] for c in members)
    print("    %-7s ATON class = %-28s off-cylinder tokens of the class: %d"
          % (s["id"], " ".join(members), offc))
print()
print("  -> E4AF itself is cylinder-only (as the kernel says), and so are E4AE")
print("     and E4FD: all three members of the 'Sonnenaufgang/Boot' end of the")
print("     merged group occur ONLY on the seal.  The 20 off-cylinder tokens the")
print("     merged class had were almost all E416 (17) plus E495 (3).")
print("  -> So the split's whole effect is to strip the one well-attested form")
print("     (E416) out of the ATON class, leaving an ATON class with 3")
print("     off-cylinder tokens under syl6-syl8.  That is a real change to the")
print("     inventory, but it makes the ATON anchor LESS testable off the")
print("     cylinder, not more: it generates no cross-text prediction at all,")
print("     and it is unfalsifiable from the Dunand core by construction.")
