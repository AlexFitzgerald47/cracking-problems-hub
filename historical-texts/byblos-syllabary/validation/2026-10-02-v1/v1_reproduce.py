#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02) independent reproduction of the Byblos claims.

Re-derives corpus, inventory and positional statistics directly from the primary
OCBI source, fetched fresh on 2026-10-02:
    https://raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm
(md5 bbfb29fd2605d33999d9a7dc43c55797 -- byte-identical to the copy vendored by the
 2026-09-25 session, which is therefore confirmed faithful.)

Marker semantics read off Specialchars.elm in the same repo:
    's' = guessMarkerL, zero-width, applies to the PRECEDING glyph
    'a' = fractureMarker (line assumed incomplete here)
    'x' = wildcardChar  (unreadable sign)

Nothing outside this directory is written.
"""
import re, os, json, random, itertools, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = open(os.path.join(HERE, "Byblos.elm"), encoding="utf-8").read()

def C(ch): return "%04X" % ord(ch)
def name(cp): return "U+" + cp

# ---------------------------------------------------------------- parsing

FRAG = re.compile(
    r'\{\s*id\s*=\s*"(?P<id>[^"]*)"\s*,\s*source\s*=\s*"(?P<src>[^"]*)"\s*,'
    r'\s*group\s*=\s*"(?P<grp>[^"]*)"\s*,\s*dir\s*=\s*(?P<dir>\w+)\b'
    r'.*?text\s*=\s*\s*"""(?P<text>.*?)"""', re.S)

def parse_fragments(src):
    out = []
    for m in FRAG.finditer(src):
        lines = []
        for raw in m.group("text").strip().split("\n"):
            toks = []
            for ch in raw.strip():
                o = ord(ch)
                if ch == "s":
                    if toks: toks[-1][1] = True          # guess flag on previous
                elif ch == "a": toks.append(["FRACT", False])
                elif ch == "x": toks.append(["WILD",  False])
                elif ch == " ": continue
                elif 0xE000 <= o <= 0xF8FF: toks.append([C(ch), False])
                else: raise ValueError("unexpected %r in %s" % (ch, m.group("id")))
            lines.append(toks)
        out.append(dict(id=m.group("id"), source=m.group("src"),
                        group=m.group("grp"), dir=m.group("dir"), lines=lines))
    return out

SYL = re.compile(r'\{\s*id\s*=\s*"(?P<id>[^"]+)"\s*,\s*name\s*=\s*"(?P<nm>[^"]+)"\s*,'
                 r'\s*syllabary\s*=\s*String\.trim\s*"""(?P<body>.*?)"""', re.S)

def parse_syllabaries(src):
    out = []
    for m in SYL.finditer(src):
        grps = [[C(c) for c in ln.strip() if 0xE000 <= ord(c) <= 0xF8FF]
                for ln in m.group("body").strip().split("\n")]
        out.append(dict(id=m.group("id"), name=m.group("nm"),
                        groups=[g for g in grps if g]))
    return out

def parse_rawtokens(src):
    body = src.split('rawTokens = Token.toList <| String.trim """',1)[1].split('"""',1)[0]
    return [C(c) for c in body if 0xE000 <= ord(c) <= 0xF8FF]

def parse_syllablemap(src):
    body = src.split('syllableMap = String.trim """',1)[1].split('"""',1)[0]
    out = []
    for ln in body.strip().split("\n"):
        ln = ln.strip()
        if not ln: continue
        val, glyphs = ln.split(" ", 1)
        out.append((val, [C(c) for c in glyphs if 0xE000 <= ord(c) <= 0xF8FF]))
    return out

FRAGS = parse_fragments(SRC)
SYLS  = parse_syllabaries(SRC)
RAWT  = parse_rawtokens(SRC)
SMAP  = parse_syllablemap(SRC)

def hdr(s): print("\n" + "="*78 + "\n" + s + "\n" + "="*78)

# ---------------------------------------------------------------- 0. corpus shape
hdr("0. CORPUS SHAPE AS ACTUALLY ENCODED")
print("fragment entries in file : %d" % len(FRAGS))
print("rawTokens (declared sign repertoire) : %d codepoints" % len(RAWT))
bysrc = collections.Counter(f["source"] for f in FRAGS)
bygrp = collections.Counter(f["group"]  for f in FRAGS)
print("by `source` field :", dict(bysrc))
print("by `group`  field :", dict(bygrp))

def base(fid):
    """object id with variant/face suffix stripped"""
    return re.split(r'\s*\(', fid)[0].strip()
objs = {}
for f in FRAGS:
    objs.setdefault(base(f["id"]), set()).add(f["source"])
print("distinct object ids after stripping Var./face suffixes : %d" % len(objs))
print("   ", sorted(objs))
bybl  = [o for o,s in objs.items() if s == {"BYBL"}]
print("objects with source==BYBL : %d  -> %s" % (len(bybl), sorted(bybl)))
print("objects with source==BYBL? : %d" % len([o for o,s in objs.items() if s=={'BYBL?'}]))
# collapse cylinder r*
cyl = {o for o in objs if re.fullmatch(r'r[a-d]', o)}
print("collapsing cylinder r a-d into one object -> BYBL objects : %d"
      % (len(bybl) - len(cyl) + 1))
print("OCBI's own description text claims: 18 BYBL (a-s) and 14 BYBL? (t-d')")

ntok = sum(1 for f in FRAGS for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD"))
nwild= sum(1 for f in FRAGS for l in f["lines"] for t in l if t[0]=="WILD")
nguess=sum(1 for f in FRAGS for l in f["lines"] for t in l if t[1] and t[0] not in("FRACT","WILD"))
types = {t[0] for f in FRAGS for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD")}
print("\nsign tokens (all variants counted)      : %d" % ntok)
print("unreadable wildcard slots               : %d" % nwild)
print("guess-marked sign tokens                : %d (%.1f%%)" % (nguess, 100*nguess/ntok))
print("distinct sign TYPES actually attested    : %d" % len(types))
print("declared rawTokens not attested in texts : %d" % len(set(RAWT)-types))

# de-duplicated corpus: one variant per object (first listed)
seen=set(); DEDUP=[]
for f in FRAGS:
    b=base(f["id"])
    if b in seen: continue
    seen.add(b); DEDUP.append(f)
dtok=sum(1 for f in DEDUP for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD"))
dtypes={t[0] for f in DEDUP for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD")}
print("\nde-duplicated (first variant per object): %d tokens, %d types"%(dtok,len(dtypes)))
print("type/token ratio (dedup)                : %.3f" % (len(dtypes)/dtok))
hap=sum(1 for cp,c in collections.Counter(
    t[0] for f in DEDUP for l in f["lines"] for t in l if t[0] not in("FRACT","WILD")).items() if c==1)
print("hapax sign types (dedup)                : %d  (%.0f%% of types)"%(hap,100*hap/len(dtypes)))

# ---------------------------------------------------------------- 1. cylinder
hdr("1. THE AMARNA CYLINDER AS ENCODED (all variants, nothing selected)")
for f in FRAGS:
    if re.match(r'r[a-d]', f["id"]):
        for l in f["lines"]:
            print("  %-16s dir=%-4s  %s" % (f["id"], f["dir"],
                " ".join(("%s%s"%(t[0],"?" if t[1] else "")) for t in l)))
print("""
CLAIM (PARTIAL_BIGRAPH_KERNEL table):
  BYBL ra        = E4AC E4AD E41F E44D E42A E483   -> Ankhesen(pa)amun
  BYBL rb Var.3  = E49A E416 E491 E4AF             -> Meketaton
  BYBL rc Var.3  = E4B0 E443 E429 E4AF             -> Meritaton""")
want = {"ra":["E4AC","E4AD","E41F","E44D","E42A","E483"],
        "rb (Var. 3)":["E49A","E416","E491","E4AF"],
        "rc (Var. 3)":["E4B0","E443","E429","E4AF"]}
for f in FRAGS:
    if f["id"] in want:
        got=[t[0] for l in f["lines"] for t in l if t[0] not in("FRACT","WILD")]
        print("  %-14s claimed==encoded : %s" % (f["id"], got==want[f["id"]]))

hdr("1b. VARIANT SENSITIVITY OF THE CYLINDER READINGS  [validator-1 new test]")
print("""rb has 3 transcription variants and rc has 3, of the SAME physical columns.
The claim silently selects Var.3 for both. Consequences:""")
for f in FRAGS:
    if re.match(r'r[bc] ', f["id"]):
        sq=[t[0] for l in f["lines"] for t in l if t[0] not in("FRACT","WILD")]
        print("  %-14s = %-30s  len=%d  terminal=%s  contains E416=%s"
              %(f["id"]," ".join(sq),len(sq),sq[-1],"E416" in sq))

# ---------------------------------------------------------------- 2. syllabaries
hdr("2. INVENTORY MERGE / SPLIT, RE-DERIVED FOR EVERY SYLLABARY")
def grp_of(syl, cp):
    for i,g in enumerate(syl["groups"]):
        if cp in g: return i
    return None
pairs = [("E416","E4AF"),("E4AE","E4AF"),("E416","E4AE"),("E416","E495"),
         ("E4AF","E4FD"),("E491","E412"),("E49A","E4B0")]
print("%-10s %s" % ("syllabary", "  ".join("%s~%s"%p for p in pairs)))
for s in SYLS:
    row=[]
    for a,b in pairs:
        ga,gb = grp_of(s,a), grp_of(s,b)
        row.append("MERGED" if (ga is not None and ga==gb) else
                   ("split " if (ga is not None and gb is not None) else "absent"))
    print("%-10s %s" % (s["id"]+"/"+s["name"], "  ".join("%-6s"%r for r in row).replace("  "," ")))
print("""
CLAIM: 'Syl2-Syl5: E416 and E4AF merged; Syl6-Syl8: E416 E495 separated from
        the group containing E4AE E4AF E4FD.'""")

hdr("2b. WHAT THE SPLIT ARGUMENT LOOKS LIKE UNDER THE OTHER VARIANTS  [new test]")
print("""The argument is: 'two signs that OCBI merges both occur inside one 4-sign
proper name, forcing unnecessary polyfunctionality -> split them.'
Applying the SAME argument mechanically to every cylinder-name variant:""")
for f in FRAGS:
    if re.match(r'r[bc]', f["id"]) or f["id"]=="ra":
        sq=[t[0] for l in f["lines"] for t in l if t[0] not in("FRACT","WILD")]
        for s in SYLS:
            collisions=[]
            for i,j in itertools.combinations(range(len(sq)),2):
                if sq[i]==sq[j]: continue
                gi,gj=grp_of(s,sq[i]),grp_of(s,sq[j])
                if gi is not None and gi==gj: collisions.append((sq[i],sq[j]))
            if collisions and s["id"] in ("search","syl5","syl6","syl8"):
                print("  %-14s %-8s same-group pairs inside the name: %s"
                      %(f["id"],s["id"],collisions))

# ---------------------------------------------------------------- 3. distributions
hdr("3. POSITIONAL / DISTRIBUTIONAL FACTS FOR THE ANCHOR SIGNS")
def occurrences(cp):
    out=[]
    for f in FRAGS:
        for li,l in enumerate(f["lines"]):
            for ti,t in enumerate(l):
                if t[0]==cp: out.append((f["id"],f["dir"],li+1,ti,t[1],l))
    return out
for cp in ["E49A","E4B0","E44D","E4AF","E416","E4AE","E483","E42A","E491","E412","E402"]:
    occ=occurrences(cp)
    oncyl=[o for o in occ if re.match(r'r[a-d]',o[0])]
    print("%s: %3d tokens total, %2d on cylinder r*, %2d off-cylinder, in %d fragment entries"
          %(cp,len(occ),len(oncyl),len(occ)-len(oncyl),len({o[0] for o in occ})))
print("\nCLAIM: 'E4AF is cylinder-only in the current OCBI raw transcription'")
print("  -> off-cylinder E4AF tokens found:", len([o for o in occurrences('E4AF') if not re.match(r'r',o[0])]))
# digraph E42A E483
dig=0; digwhere=[]
for f in FRAGS:
    for l in f["lines"]:
        sq=[t[0] for t in l]
        for i in range(len(sq)-1):
            if sq[i]=="E42A" and sq[i+1]=="E483": dig+=1; digwhere.append(f["id"])
print("CLAIM: 'E42A E483 is cylinder-only as an exact digraph' -> occurrences:",dig,digwhere)
e483=[o[0] for o in occurrences("E483")]
print("  (E483 alone occurs in:",e483,")")

# ---------------------------------------------------------------- 4. ME anchor
hdr("4. THE ME ANCHOR TRANSFER (criterion-4 candidate), RE-DERIVED")
for fid,dirn,li,ti,guess,l in occurrences("E49A"):
    sq=["%s%s"%(t[0],"?" if t[1] else "") for t in l]
    L = sq[ti-1] if ti>0 else "(line start)"
    R = sq[ti+1] if ti+1<len(sq) else "(line end)"
    print("  %-14s dir=%-4s line %d pos %d  guess=%s" % (fid,dirn,li,ti,guess))
    print("        line: %s" % " ".join(sq))
    print("        string-left=%s   string-right=%s" % (L,R))
print("""
CLAIM (ME_ANCHOR_TRANSFER table 3) says the three left neighbours are
  BYBL i -> E442, BYBL k -> E439, BYBL m -> E410.""")
hdr("4b. NULL MODEL FOR THE 'E49A -> E402' ADJACENCY  [validator-1 new test]")
# how often does E402 follow an arbitrary sign, and what is P(3/3) by chance?
pairs_all=[]
for f in DEDUP:
    for l in f["lines"]:
        sq=[t[0] for t in l]
        pairs_all += list(zip(sq,sq[1:]))
nfollow=collections.Counter(b for a,b in pairs_all)
tot=len(pairs_all)
p402=nfollow["E402"]/tot
print("de-dup corpus bigram slots: %d ; E402 as right member: %d ; base rate p=%.4f"
      %(tot,nfollow["E402"],p402))
print("naive P(all 3 of 3 rare-sign followers are E402) = p^3 = %.3g" % p402**3)
# but the right question is the MAXIMUM over 212 candidate followers
# P(some sign is the follower all 3 times) under independence:
pany=sum((c/tot)**3 for c in nfollow.values())
print("P(ANY single sign is the follower all 3 times) = sum p_i^3 = %.3g" % pany)
# empirical: for every sign with exactly 3 off-cylinder tokens, is its follower constant?
cnt=collections.Counter(t[0] for f in DEDUP for l in f["lines"] for t in l
                        if t[0] not in ("FRACT","WILD"))
rare3=[cp for cp,c in cnt.items() if c==3]
const=0; tested=0
for cp in rare3:
    fols=[]
    for f in DEDUP:
        for l in f["lines"]:
            sq=[t[0] for t in l]
            for i,v in enumerate(sq):
                if v==cp and i+1<len(sq): fols.append(sq[i+1])
    if len(fols)==3:
        tested+=1
        if len(set(fols))==1: const+=1
print("EMPIRICAL null: signs with exactly 3 tokens in the de-dup corpus: %d"%len(rare3))
print("  of those with 3 recoverable followers: %d tested, %d (%.0f%%) have a CONSTANT follower"
      %(tested,const,100*const/max(tested,1)))
