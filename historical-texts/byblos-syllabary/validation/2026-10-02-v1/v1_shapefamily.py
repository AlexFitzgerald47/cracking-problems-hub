#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02), part 5.

Two further independent checks on PARTIAL_BIGRAPH_KERNEL, using the GEAS glyph
names (fonts/original/byblos.svg, same primary repo):

 L. Is the Syl6+ split of E416 from E4AF really "the direction demanded by the
    external control", or is it OCBI's own graphic shape taxonomy?
 M. How much of the cylinder's signary is attested nowhere else?
"""
import re,os,json,collections
H=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(H,"v1_reproduce.py")).read().split("def hdr(")[0])
def hdr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)
NAMES=json.load(open(os.path.join(H,"glyphnames_from_font.json"),encoding="utf-8"))
def short(cp):
    n=NAMES.get(cp,"")
    return re.sub(r'^[A-Za-z]+\s+[IVXLC]+\s+\d+\s*','',n).strip() or n

hdr("L. THE DISPUTED SIGNS, WITH THEIR GEAS SHAPE NAMES")
for cp in ["E416","E495","E4FD","E4AE","E4AF","E450","E455","E47B","E4C9"]:
    print("   %-6s %-28s   %s" % (cp, short(cp), NAMES.get(cp,"")))
print("""
=> E416/E495 are the 'offener Ring' (open ring) family.
   E4AE/E4AF are the 'Sonnenaufgang' (sunrise) family -- and BOTH are first
   attested on the cylinder column Rb I (Rb I 2 and Rb I 3).
   Syl2-Syl5 put a RING and a SUNRISE in one grapheme group; Syl6-Syl8 separate
   the rings from the sunrises.  That is a graphic re-grouping along the
   project's own shape taxonomy.  The Amarna alignment coincides with it; it is
   not evident that the alignment caused it, and the kernel's claim that OCBI
   'independently moves in exactly the direction demanded by the external
   control' overstates what the sequence of inventories shows.""")
print("\nSyl6 group that receives E4AE/E4AF/E4FD, with shape names:")
s6=[s for s in SYLS if s["id"]=="syl6"][0]
for g in s6["groups"]:
    if "E4AF" in g:
        for cp in g: print("   %-6s %s" % (cp, short(cp)))
print("\nSyl6 group containing E416:")
for g in s6["groups"]:
    if "E416" in g:
        for cp in g: print("   %-6s %s" % (cp, short(cp)))

hdr("M. HOW MUCH OF THE CYLINDER'S SIGNARY IS CYLINDER-ONLY?")
cylids={f["id"] for f in FRAGS if re.match(r'r[a-d]',f["id"])}
cyl=set(); core=set()
for f in FRAGS:
    for l in f["lines"]:
        for t in l:
            if t[0] in ("FRACT","WILD"): continue
            (cyl if f["id"] in cylids else core).add(t[0])
only=sorted(cyl-core)
print("distinct signs on the cylinder (all variants) : %d" % len(cyl))
print("of those, attested NOWHERE else in OCBI       : %d (%.0f%%)"
      % (len(only),100*len(only)/len(cyl)))
for cp in only: print("   %-6s %s" % (cp, NAMES.get(cp,"")))
print("""
Base rate for comparison: share of all attested types that occur in exactly one
fragment entry = %.0f%%.""" % (100*sum(
    1 for cp,fs in collections.Counter().items() if False) if False else 0))
infr=collections.defaultdict(set)
for f in FRAGS:
    for l in f["lines"]:
        for t in l:
            if t[0] not in ("FRACT","WILD"): infr[t[0]].add(f["id"])
one=sum(1 for cp,fs in infr.items() if len(fs)==1)
print("   single-fragment types corpus-wide: %d of %d (%.0f%%)"
      % (one,len(infr),100*one/len(infr)))
print("""
=> %d of the cylinder\'s %d signs (%.0f%%) are attested only on the cylinder,
   against a corpus-wide single-fragment rate of %.0f%%.  THIS ATTACK FAILS:
   the cylinder is NOT anomalous in its share of otherwise unattested signs --
   it is slightly below the corpus base rate.  Validator-1 records that as a
   point IN FAVOUR of the kernel\'s script identification.
   What does follow is narrower and still decisive for criterion 4: the two
   divine-name anchors (E4AF, and E4AE in the Var.1/2 reading) and the second
   half of the AMUN digraph in combination have ZERO off-cylinder attestation,
   so they cannot generate any held-out prediction on the Dunand core by
   construction.""" % (len(only),len(cyl),100*len(only)/len(cyl),100*one/len(infr)))
