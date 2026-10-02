#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02), part 4.

The decisive independent check: what is sign E402, the sign on which the whole
ME_ANCHOR_TRANSFER structural result rests?

Glyph names are taken from the PRIMARY GEAS source that ships the signs,
fetched fresh 2026-10-02:
   https://raw.githubusercontent.com/elamicon/elamicon/master/fonts/original/byblos.svg
(the same repository and project that supplies Byblos.elm and the ATON/AMUN labels
 the kernel relies on).
"""
import re, os, json, collections, math
H=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(H,"v1_reproduce.py")).read().split("def hdr(")[0])
def hdr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)
NAMES=json.load(open(os.path.join(H,"glyphnames_from_font.json"),encoding="utf-8"))

hdr("H. WHAT THE GEAS FONT CALLS THE SIGNS IN THE ME CLUSTER")
for cp in ["E49A","E402","E48F","E412","E404","E4B0","E44D","E4AF","E4AE","E416","E491"]:
    print("  %-6s %s" % (cp, NAMES.get(cp,"<absent>")))
div=[cp for cp,n in NAMES.items() if "worttrenner" in n.lower()]
print("\nALL signs whose GEAS glyph-name contains 'Worttrenner' (word divider):")
for cp in sorted(div): print("   %-6s %s" % (cp,NAMES[cp]))
print("\nByblos.elm sets  seperatorChars = \"%s\"  (i.e. the app declares NO separator),"
      % re.search(r'seperatorChars = "([^"]*)"',SRC).group(1))
print("which is presumably why the Hub pass never met the name.")

hdr("I. DOES E402 BEHAVE LIKE A DIVIDER, DISTRIBUTIONALLY? (name-free test)")
toks=[(f["id"],li+1,i,t[0],t[1],len(l))
      for f in FRAGS for li,l in enumerate(f["lines"]) for i,t in enumerate(l)]
sig=[t for t in toks if t[3] not in ("FRACT","WILD")]
edge=sum(1 for t in sig if t[2]==0 or t[2]==t[5]-1)
p_edge=edge/len(sig)
print("all sign tokens %d ; at a line edge %d -> P(edge)=%.4f" % (len(sig),edge,p_edge))
cnt=collections.Counter(t[3] for t in sig)
rows=[]
for cp in sorted(cnt, key=lambda c:-cnt[c]):
    n=cnt[cp]
    if n<6: continue
    e=sum(1 for t in sig if t[3]==cp and (t[2]==0 or t[2]==t[5]-1))
    rows.append((((1-p_edge)**n) if e==0 else 1.0, cp, n, e))
rows.sort()
print("\nsigns with n>=6 tokens and ZERO line-edge occurrences "
      "(a divider can never start or end a line):")
for p,cp,n,e in rows:
    if e==0: print("   %-6s n=%-3d edges=0  P(0 edges | ordinary sign)=%.4f   %s"
                   % (cp,n,p,NAMES.get(cp,"")))
print("\n=> E402 is one of very few mid-frequency signs that NEVER occupies a line edge,")
print("   which is what a word divider does and what an ordinary syllabogram does not.")

hdr("J. RE-READING THE THREE 'HELD-OUT' LOCI WITH E402 AS A DIVIDER")
for fid,li,ti,cp,g,n in [t for t in sig if t[3]=="E49A"]:
    pass
for f in FRAGS:
    if f["id"] not in ("i","k","m"): continue
    for li,l in enumerate(f["lines"]):
        sq=[t[0] for t in l]
        if "E49A" not in sq: continue
        rend=[]
        for t in l:
            if t[0]=="E402": rend.append("|")
            elif t[0]=="FRACT": rend.append("[frac]")
            elif t[0]=="WILD": rend.append("[x]")
            else: rend.append(t[0]+("?" if t[1] else ""))
        print("  BYBL %-2s line %-2d : %s" % (f["id"],li+1," ".join(rend)))
print("""
  BYBL i IX : ... E442 | E49A | E48F E40D? ...  -> E49A is a ONE-SIGN word
                                                  flanked by dividers
  BYBL k IV : E45A E497 E439 E49A | E412 E45A   -> E49A word-final; E412 is in
                                                  the NEXT word
  BYBL m II : [frac][x] E410 E49A | E48F E46B   -> E49A word-final

CONSEQUENCES FOR ME_ANCHOR_TRANSFER:
  * the claimed three-sign lexical unit E49A-E402-{E48F,E412} does not exist;
    it straddles a word boundary.
  * the 'invariant first internal transition E49A -> E402' IS the word boundary,
    so it carries no lexical information at all.
  * the stated asymmetry ('low variation inside, high variation outside') is
    reversed: the only invariant element is the boundary marker, and the
    genuinely lexical neighbours (E48F / E412 / E442 / E439 / E410) all vary.
  * the conditional 'ME - ? - T(?)' skeleton for BYBL k is void: under the
    divider reading E412 is not the third sign of a word beginning with ME.
  * what survives, and is still interesting, is a much narrower fact:
    all three clear off-cylinder E49A tokens sit immediately before a word
    divider, and in BYBL i E49A is a complete one-sign word.""")

hdr("K. IS 'ME ALWAYS PRECEDES A DIVIDER' STILL A REAL SIGNAL?")
DIV={"E402","E404"}
pairs=[]
for f in FRAGS:
    for l in f["lines"]:
        sq=[t[0] for t in l]
        pairs += list(zip(sq,sq[1:]))
pairs=[(a,b) for a,b in pairs if a not in("FRACT","WILD") and b not in("FRACT","WILD")]
pd=sum(1 for a,b in pairs if b in DIV)/len(pairs)
print("adjacent sign-sign pairs %d ; P(right member is a divider)=%.4f" % (len(pairs),pd))
print("3 of 3 under that rate, naive: %.3g" % pd**3)
users={f["id"] for f in FRAGS for l in f["lines"] for t in l if t[0] in DIV}
print("objects that use a divider at all:", sorted(users))
sub=[]
for f in FRAGS:
    if f["id"] not in users: continue
    for l in f["lines"]:
        sq=[t[0] for t in l]
        sub+=[(a,b) for a,b in zip(sq,sq[1:]) if a not in("FRACT","WILD") and b not in("FRACT","WILD")]
pd2=sum(1 for a,b in sub if b in DIV)/len(sub)
print("restricted to divider-using objects: %d pairs, P(divider follows)=%.4f, 3of3=%.3g"
      % (len(sub),pd2,pd2**3))
# family-wise: how many signs with >=3 tokens inside divider-using objects are always divider-followed
cnt2=collections.Counter(t[0] for f in FRAGS if f["id"] in users
                         for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD"))
always=[]
for cp,n in cnt2.items():
    if n<3: continue
    fol=[]
    for f in FRAGS:
        if f["id"] not in users: continue
        for l in f["lines"]:
            sq=[t[0] for t in l]
            for i,v in enumerate(sq):
                if v==cp and i+1<len(sq) and sq[i+1] not in("FRACT","WILD"): fol.append(sq[i+1])
    if fol and all(x in DIV for x in fol): always.append((cp,len(fol)))
print("signs with >=3 tokens in divider-using objects that are ALWAYS divider-followed:",
      [(c,n,NAMES.get(c,'')) for c,n in always])
print("""
=> even after the divider reinterpretation, 'E49A is always immediately
   followed by a word divider' remains a genuine and unusual positional fact
   (family-wise it is the only such sign).  But it is a BOUNDARY fact about a
   sign that may simply be word-final-only; it is not evidence for the value
   'me', and it is not the lexical unit the artifact claims.""")
