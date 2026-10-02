#!/usr/bin/env python3
"""
VALIDATOR 1 (2026-10-02), part 6: check the kernel against the primary
published source it rests on.

Sources fetched fresh 2026-10-02 (both HTTP 200):
  https://center-for-decipherment.ch/news/2021-03-01-james-hoch-1990-confirmed/
     -> literally contains "<U+E4AF> ATON" and "<U+E42A><U+E483> AMUN",
        and attributes pa to "<U+E44D>; <U+E49B>" (TWO forms, not one).
  https://center-for-decipherment.ch/journal/2024_01__Schmutz-%26-Maeder__...pdf
     -> local text dump saved as schmutz_maeder_2024.txt; its abstract states the
        daughter-name bigraph proves Woudhuizen/Best "attestedly incorrect", and a
        footnote extends this to Mendenhall (1985) and Colless's rescue hypotheses.
     -> and it segments the names as
            anch-es-en-pa-a-mun / me-'-ke(t)-ATON / me-ri-t-ATON
"""
import re,os,json,collections
H=os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(H,"v1_reproduce.py")).read().split("def hdr(")[0])
NAMES=json.load(open(os.path.join(H,"glyphnames_from_font.json"),encoding="utf-8"))
SM=open(os.path.join(H,"schmutz_maeder_2024.txt"),encoding="utf-8").read()

print("="*78); print("N. PUBLISHED SEGMENTATION vs THE HUB'S FROZEN ANCHOR SET"); print("="*78)
for kw in ["anch-es-en","Mendenhall (1985)","attestedly incorrect"]:
    i=SM.find(kw)
    print("\n[%s] ... %s ..." % (kw, " ".join(SM[max(0,i-260):i+260].split())) if i>=0
          else "[%s] NOT FOUND" % kw)
print("""
Published segmentation under rb Var.3 / rc Var.3:
   rb: E49A=me   E416=' (ayin)   E491=ke(t)   E4AF=ATON
   rc: E4B0=me   E443=ri         E429=t       E4AF=ATON
PARTIAL_BIGRAPH_KERNEL section 7 freezes only ME / PA / ATON / AMUN.
So three published values (E416=', E491=ke(t), E429=t) are left on the table,
and ME_ANCHOR_TRANSFER reaches a weaker CONDITIONAL T-class for E491 via the
OCBI E491~E412 merge when the published source states ke(t) outright.
""")
print("%-6s %-32s %5s %5s  %s" % ("sign","GEAS name","tot","off","off-cylinder objects"))
for cp in ["E49A","E4B0","E44D","E49B","E4AF","E416","E491","E443","E429","E42A","E483"]:
    occ=[(f["id"],) for f in FRAGS for l in f["lines"] for t in l if t[0]==cp]
    off=[o for o in occ if not re.fullmatch(r'r[a-d]',o[0])]
    print("%-6s %-32s %5d %5d  %s" % (cp,NAMES.get(cp,"")[:32],len(occ),len(off),
          sorted({o[0] for o in off})))
print("""
=> E429 (published value 't') has 25 off-cylinder tokens on 8 objects and E416
   (published ''') has 17 on 6.  These are by far the best criterion-4 probes in
   the corpus and NEITHER is tested anywhere in the folder.  The folder's only
   criterion-4 attempt uses E49A, which has 3 off-cylinder tokens.""")
