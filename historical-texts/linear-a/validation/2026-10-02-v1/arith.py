#!/usr/bin/env python3
"""V1 reproduction, part 2: scope-aware arithmetic audit of EVERY KU-RO / PO-TO-KU-RO
total in the corpus, independently of the claimant's intermediate files.

Segmentation rule (frozen before looking at outcomes):
  A total marker closes the run of entries immediately before it.  Walking backwards
  from the marker we collect numerals, and we STOP at (i) another total marker,
  (ii) a sign-group that is followed by a divider (an administrative heading, e.g.
  'KI-RO .' or 'A-DU .'), or (iii) the start of the face.  This is the minimum
  machinery needed to respect the forward-scoping 'KI-RO .' construction the claim
  asserts; the 2026-09-25 session's 'everything since the last marker' rule does not,
  and manufactures mismatches.
Damage flag: the face carries GORILA lacuna marks or bracketed/restored numerals.
"""
import sys, re, collections
sys.path.insert(0,'.')
from census import A, is_sg, is_num, ival, DIV, LAC, basedoc

TOTALS = {"KU-RO","PO-TO-KU-RO"}

def face_damaged(v):
    s = (v.get('transcription','') or '') + (v.get('parsedInscription','') or '')
    br = any('[' in w or ']' in w for w in v['transliteratedWords'])
    return (LAC in s) or br

def audit(face, v):
    ws = v['transliteratedWords']
    out = []
    for i,w in enumerate(ws):
        if w not in TOTALS: continue
        nxt = ws[i+1] if i+1 < len(ws) else None
        tot = ival(nxt) if nxt else None
        if tot is None: 
            out.append((w, None, None, 0, "no numeral after marker")); continue
        ents = []; j = i-1; stop = "start-of-face"
        while j >= 0:
            t = ws[j]
            if t in TOTALS: stop = "previous total"; break
            if is_sg(t) and j+1 < len(ws) and ws[j+1] == DIV:
                stop = "heading '%s .'" % t; break
            if ival(t) is not None: ents.append(ival(t))
            j -= 1
        out.append((w, tot, sum(ents), len(ents), stop))
    return out

print("### ARITHMETIC AUDIT of all KU-RO / PO-TO-KU-RO totals, witness A")
rows=[]
for k in sorted(A):
    v=A[k]
    if not any(w in TOTALS for w in v['transliteratedWords']): continue
    dmg = face_damaged(v)
    for mark, tot, ssum, n, stop in audit(k,v):
        rows.append((k, v.get('site'), v.get('scribe'), dmg, mark, tot, ssum, n, stop))

ok = [r for r in rows if r[5] is not None and r[6] is not None and abs(r[6]-r[5])<1e-9]
bad= [r for r in rows if r[5] is not None and r[6] is not None and abs(r[6]-r[5])>=1e-9]
non= [r for r in rows if r[5] is None]
print(f"total markers found: {len(rows)}   with a numeral: {len(rows)-len(non)}   "
      f"EXACT: {len(ok)}   mismatch: {len(bad)}   no numeral: {len(non)}")
print(f"  exact rate among numeral-bearing totals: {len(ok)}/{len(rows)-len(non)} "
      f"= {100*len(ok)/max(1,len(rows)-len(non)):.1f}%")
okd = [r for r in ok if r[3]]; bdd=[r for r in bad if r[3]]
print(f"  undamaged faces: EXACT {len(ok)-len(okd)}  mismatch {len(bad)-len(bdd)} "
      f"-> {100*(len(ok)-len(okd))/max(1,(len(ok)-len(okd))+(len(bad)-len(bdd))):.1f}% exact")
print(f"  damaged faces  : EXACT {len(okd)}  mismatch {len(bdd)}")

print("\n--- MISMATCHES (all) ---")
for r in sorted(bad, key=lambda x:-abs(x[6]-x[5])):
    k,site,sc,dmg,mark,tot,ssum,n,stop = r
    print(f"  {k:9s} {mark:11s} stated {tot:6g}  entries({n}) sum {ssum:6g}  "
          f"diff {ssum-tot:+7g}  damaged={dmg}  stop@{stop}  [{sc or '-'}]")

print("\n--- the claim's own named totals ---")
for k in ["HT85a","HT88","HT94a","HT94b","HT117a","HT119","HT122a","HT122b","HT2","HT97",
          "HT118","HT102","HT11b"]:
    if k not in A: print(f"  {k}: ABSENT from witness A"); continue
    v=A[k]
    for mark,tot,ssum,n,stop in audit(k,v):
        v_ = "n/a" if tot is None else f"{tot:g}"
        s_ = "n/a" if ssum is None else f"{ssum:g}"
        flag = "EXACT" if (tot is not None and ssum is not None and abs(ssum-tot)<1e-9) else "MISMATCH"
        print(f"  {k:7s} {mark:11s} stated {v_:>6s}  sum({n}) {s_:>6s}  {flag:8s} "
              f"damaged={face_damaged(v)}  stop@{stop}")
