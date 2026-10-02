#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02), part 2.

Supplies the two things criterion 1 and criterion 4 require and that the claim
artifacts do not contain:
  (a) an explicit power analysis of the OCBI corpus;
  (b) a null model for "a short sign sequence recurs across objects",
      i.e. the background rate against which the ME_ANCHOR_TRANSFER trigraph
      has to be judged.

Reads only ./Byblos.elm (fresh fetch, md5 bbfb29fd2605d33999d9a7dc43c55797).
"""
import re, os, math, collections, itertools, random
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
    """maximal runs of certain readable signs (break at wildcard/fracture/line end)"""
    out=[]
    for f in frags:
        for li,l in enumerate(f["lines"]):
            cur=[]
            for t in l:
                if t[0] in ("FRACT","WILD"):
                    if cur: out.append((f["id"],li+1,cur)); cur=[]
                else: cur.append(t[0])
            if cur: out.append((f["id"],li+1,cur))
    return out

# ------------------------------------------------------------- power analysis
hdr("A. POWER ANALYSIS OF THE OCBI CORPUS  (absent from the claim artifacts)")
toks=[t for f in DEDUP for l in f["lines"] for t in l if t[0] not in ("FRACT","WILD")]
N=len(toks); cnt=collections.Counter(t[0] for t in toks); V=len(cnt)
print("de-duplicated corpus (one transcription variant per object)")
print("  sign tokens N                      = %d" % N)
print("  attested sign types V              = %d" % V)
print("  declared repertoire (rawTokens)    = %d" % len(set(RAWT)))
print("  tokens per type N/V                = %.2f" % (N/V))
print("  hapax legomena V1                  = %d (%.0f%% of V)" %
      (sum(1 for c in cnt.values() if c==1), 100*sum(1 for c in cnt.values() if c==1)/V))
print("  types with <=2 tokens              = %d (%.0f%% of V)" %
      (sum(1 for c in cnt.values() if c<=2), 100*sum(1 for c in cnt.values() if c<=2)/V))
nw=sum(1 for f in DEDUP for l in f["lines"] for t in l if t[0]=="WILD")
ng=sum(1 for t in toks if t[1])
print("  unreadable (wildcard) slots        = %d (%.0f%% of all slots)" % (nw,100*nw/(N+nw)))
print("  guess-marked sign tokens           = %d (%.0f%% of signs)" % (ng,100*ng/N))
print("  Good-Turing est. unseen-type mass  = V1/N = %.3f" %
      (sum(1 for c in cnt.values() if c==1)/N))
# longest usable run lengths
R=sorted((len(r[2]) for r in runs(DEDUP)), reverse=True)
print("  maximal uninterrupted certain-sign runs: n=%d, longest=%d, median=%d, "
      "runs of length>=6: %d" % (len(R),R[0],R[len(R)//2],sum(1 for x in R if x>=6)))
print("""
WHAT THIS CAN AND CANNOT SUPPORT (validator-1 statement):
  * Estimating a value for one sign type needs that type to recur in several
    independent, readable environments. %d/%d types (%.0f%%) occur <=2 times, so
    for the majority of the signary there is no distributional evidence at all,
    at ANY sample size, from this corpus.
  * A free CV syllabary of 60-120 values over %d types implies >=%d
    independent constraints; the corpus offers %d bigram slots, %.0f%% of which
    are adjacent to an unreadable or guessed slot.
  * Unseen-type mass V1/N = %.3f means ~%.0f%% of the next sign token drawn
    would be a type seen once or not at all: the inventory is not closed, so any
    claim of the form "sign X occurs only on object Y" is a statement about the
    transcription, not about the script.""" %
 (sum(1 for c in cnt.values() if c<=2),V,100*sum(1 for c in cnt.values() if c<=2)/V,
  V,V,sum(max(0,len(r[2])-1) for r in runs(DEDUP)),
  100*nw/(N+nw), sum(1 for c in cnt.values() if c==1)/N,
  100*sum(1 for c in cnt.values() if c==1)/N))

# ------------------------------------------------------------- n-gram null
hdr("B. NULL MODEL: HOW OFTEN DOES A TRIGRAPH RECUR ACROSS OBJECTS ANYWAY?")
R2=runs(DEDUP)
def ngrams(n):
    d=collections.defaultdict(set); c=collections.Counter()
    for fid,li,r in R2:
        for i in range(len(r)-n+1):
            g=tuple(r[i:i+n]); d[g].add(base(fid)); c[g]+=1
    return d,c
for n in (2,3,4):
    d,c=ngrams(n)
    multi={g:objs for g,objs in d.items() if len(objs)>=2}
    print("%d-grams: %d distinct, %d (%.1f%%) occur on >=2 distinct OBJECTS"
          % (n,len(d),len(multi),100*len(multi)/len(d)))
d3,c3=ngrams(3)
multi3={g:o for g,o in d3.items() if len(o)>=2}
print("\nAll trigraphs attested on >=2 distinct objects in the de-dup corpus:")
for g,o in sorted(multi3.items(), key=lambda kv:-len(kv[1])):
    print("   %-20s objects=%s" % (" ".join(g), sorted(o)))
tgt=("E49A","E402","E48F")
print("\nME_ANCHOR_TRANSFER target trigraph %s : on objects %s"
      % (" ".join(tgt), sorted(d3.get(tgt,set()))))
print("""
=> The claimed cross-object trigraph is one of %d cross-object trigraphs in a
   corpus of this size. Recurring on 2 objects is therefore NOT by itself
   surprising; what is unusual is only that it exhausts the distribution of a
   sign with 3 tokens.""" % len(multi3))

# ------------------------------------------------------------- E402 contexts
hdr("C. IS 'E402 E48F' SPECIAL, OR THE ORDINARY FATE OF E402?")
ctx=[]
for f in DEDUP:
    for li,l in enumerate(f["lines"]):
        sq=[t[0] for t in l]
        for i,v in enumerate(sq):
            if v=="E402":
                ctx.append((f["id"],li+1,sq[max(0,i-1)] if i else "^",
                            sq[i+1] if i+1<len(sq) else "$"))
print("every E402 token in the de-dup corpus, with its string neighbours:")
for c in ctx: print("   %-16s line %-2d  L=%-6s R=%-6s" % c)
fol=collections.Counter(c[3] for c in ctx)
print("\nfollowers of E402:", dict(fol))
print("E402 -> E48F happens %d/%d times (%.0f%%); both are inside the ME cluster"
      % (fol['E48F'], len(ctx), 100*fol['E48F']/len(ctx)))

# ------------------------------------------------------------- syl9
hdr("D. SYLLABARY 9 -- THE NEWEST OCBI INVENTORY, UNMENTIONED BY THE CLAIM")
s9=[s for s in SYLS if s["id"]=="syl9"][0]
def grp(s,cp):
    for i,g in enumerate(s["groups"]):
        if cp in g: return i,g
    return None,None
for cp in ("E416","E495","E4AE","E4AF","E4FD","E491","E412","E49A","E4B0","E402","E48F"):
    i,g=grp(s9,cp)
    print("  %-6s -> %s" % (cp, ("group %-3d = %s"%(i," ".join(g))) if g else "ABSENT from syl9"))
print("""
Consequences the claim does not state:
  * syl9 contains neither E4AF nor E4AE nor E4FD at all, so the 'Syl6-Syl8
    split' is not the end state of the OCBI inventory series.
  * syl9 SPLITS E491 from E412. ME_ANCHOR_TRANSFER's conditional
    'ME - ? - T(?)' reading of BYBL k depends on E491 ~ E412 being MERGED,
    which is true only of the OLDER syllabaries (search..syl8).
  * So the claim promotes the LATER OCBI decision where it supports the kernel
    (E416 != E4AF) and relies on the EARLIER decision where it supports the
    transfer (E491 ~ E412). Those two moves are in opposite directions.""")

# ------------------------------------------------------------- syllableMap
hdr("E. syllableMap AS ENCODED")
for v,g in SMAP: print("   %-7s = %s" % (v," ".join(g)))
