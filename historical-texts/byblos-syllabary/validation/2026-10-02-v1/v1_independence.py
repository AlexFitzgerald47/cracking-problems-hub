#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02), part 3: are BYBL i and BYBL m independent witnesses?

ME_ANCHOR_TRANSFER argues the E49A-E402-E48F trigraph is strong because it
"crosses medium (bronze vs stone), object, and publication cohort".  That
argument requires the two objects to be independent draws.  Tested here.
"""
import re, os, collections, itertools
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "v1_reproduce.py")).read().split("def hdr(")[0])
def hdr(s): print("\n"+"="*78+"\n"+s+"\n"+"="*78)
def base(fid): return re.split(r'\s*\(', fid)[0].strip()
seen=set(); DEDUP=[]
for f in FRAGS:
    b=base(f["id"])
    if b in seen: continue
    seen.add(b); DEDUP.append(f)
def runs(frags):
    out=[]
    for f in frags:
        for li,l in enumerate(f["lines"]):
            cur=[]
            for t in l:
                if t[0] in ("FRACT","WILD"):
                    if cur: out.append((base(f["id"]),cur)); cur=[]
                else: cur.append(t[0])
            if cur: out.append((base(f["id"]),cur))
    return out
R=runs(DEDUP)

hdr("F. SHARED n-GRAMS BETWEEN EVERY PAIR OF OBJECTS")
ng=collections.defaultdict(set)
for o,r in R:
    for n in (3,4,5):
        for i in range(len(r)-n+1):
            ng[tuple(r[i:i+n])].add(o)
pair=collections.Counter()
detail=collections.defaultdict(list)
for g,os_ in ng.items():
    if len(os_)>=2:
        for a,b in itertools.combinations(sorted(os_),2):
            pair[(a,b)]+=1; detail[(a,b)].append(" ".join(g))
for (a,b),c in pair.most_common():
    print("  %-4s ~ %-4s : %d shared >=3-grams   %s" % (a,b,c,detail[(a,b)]))
print("""
=> BYBL i and BYBL m share TWO distinct trigraphs (E498 E46B E45A and
   E49A E402 E48F) out of only 11 cross-object trigraphs in the whole
   de-duplicated corpus.  BYBL m is 3 short lines (%d certain signs in total).
   Two independent objects do not normally share two trigraphs; i and m are
   therefore better modelled as textually RELATED witnesses (shared formula,
   shared scribe or duplicate text) than as independent draws.  The
   ME_ANCHOR_TRANSFER 'crosses medium / object / publication cohort'
   independence argument does not survive that.""" %
   sum(1 for f in DEDUP if base(f["id"])=="m" for l in f["lines"]
       for t in l if t[0] not in ("FRACT","WILD")))
mfrag=[f for f in DEDUP if base(f["id"])=="m"][0]
print("\nBYBL m in full:")
for l in mfrag["lines"]:
    print("   "+" ".join(("%s%s"%(t[0],"?" if t[1] else "")) for t in l))
print("BYBL i line 3 (the other shared trigraph):")
ifrag=[f for f in DEDUP if base(f["id"])=="i"][0]
print("   "+" ".join(("%s%s"%(t[0],"?" if t[1] else "")) for t in ifrag["lines"][2]))

hdr("G. CRITERION-4 LEDGER: WHAT IS ACTUALLY PREDICTED AND TESTED OFF-CYLINDER")
anchors={"E49A (me)":"E49A","E4B0 (me, mirrored)":"E4B0","E44D (pa)":"E44D",
         "E4AF (ATON cand.)":"E4AF","E42A+E483 (AMUN cand.)":None}
for lab,cp in anchors.items():
    if cp is None:
        n=0
        for f in DEDUP:
            for l in f["lines"]:
                sq=[t[0] for t in l]
                n+=sum(1 for i in range(len(sq)-1) if sq[i]=="E42A" and sq[i+1]=="E483")
        off=n-1
        print("  %-24s off-cylinder tokens in de-dup corpus: %d" % (lab,off)); continue
    occ=[(base(f["id"]),li+1,i,t[1],[x[0] for x in l])
         for f in DEDUP for li,l in enumerate(f["lines"]) for i,t in enumerate(l) if t[0]==cp]
    off=[o for o in occ if not re.fullmatch(r'r[a-d]',o[0])]
    clean=[o for o in off if not o[3]]
    print("  %-24s off-cylinder tokens: %-3d of which not guess-marked: %-3d objects: %s"
          % (lab,len(off),len(clean),sorted({o[0] for o in off})))
print("""
=> Only ONE of the four anchors (E49A) has >=3 clean off-cylinder tokens.
   E4AF and the E42A+E483 digraph have ZERO off-cylinder tokens, so by
   construction they cannot generate any held-out prediction on the Dunand
   core.  E4B0 has one off-cylinder token and it is guess-marked with an
   unreadable follower.  E44D (pa) has off-cylinder tokens but no artifact in
   the folder tests it off-cylinder at all.""")
