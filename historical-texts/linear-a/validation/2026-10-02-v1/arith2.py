#!/usr/bin/env python3
"""V1 reproduction, part 2b: arithmetic audit under TWO frozen segmentations, with a
numeral-level damage flag.  Reported together so the claim gets its best case.

  SEG-MAX : walk back from the total marker to the previous total marker or face start.
  SEG-SCOPE: same, but also stop at an administrative heading 'X .' (a sign-group
             immediately followed by the word divider) -- i.e. respect the forward-
             scoping 'KI-RO .' construction the claim asserts.
  A total COUNTS AS EXACT if it is exact under either segmentation.
Damage is judged at the numerals: GORILA lacuna glyph in the face, or a bracketed
numeral token.  (VIR+[?] etc. is ideogram uncertainty, not numeric loss.)
"""
import sys, re, collections
sys.path.insert(0,'.')
from census import A, is_sg, is_num, ival, DIV, LAC, basedoc
TOTALS={"KU-RO","PO-TO-KU-RO"}

def numeric_damage(v):
    if LAC in (v.get('transcription','') or '') or LAC in (v.get('parsedInscription','') or ''):
        return True
    for w in v['transliteratedWords']:
        if ('[' in w or ']' in w) and any(c.isdigit() for c in w): return True
    return False

def walk(ws, i, respect_heading):
    ents=[]; j=i-1; stop="start"
    while j>=0:
        t=ws[j]
        if t in TOTALS: stop="prev-total"; break
        if respect_heading and is_sg(t) and j+1<len(ws) and ws[j+1]==DIV:
            stop="heading:"+t; break
        if ival(t) is not None: ents.append(ival(t))
        j-=1
    return sum(ents), len(ents), stop

rows=[]
for k in sorted(A):
    v=A[k]; ws=v['transliteratedWords']
    for i,w in enumerate(ws):
        if w not in TOTALS: continue
        tot = ival(ws[i+1]) if i+1<len(ws) else None
        if tot is None: continue
        mx = walk(ws,i,False); sc = walk(ws,i,True)
        exact = abs(mx[0]-tot)<1e-9 or abs(sc[0]-tot)<1e-9
        rows.append(dict(face=k, site=v.get('site'), scribe=v.get('scribe') or '-',
                         dmg=numeric_damage(v), mark=w, tot=tot,
                         mx=mx, sc=sc, exact=exact))

n=len(rows); ex=[r for r in rows if r['exact']]; no=[r for r in rows if not r['exact']]
print(f"### all numeral-bearing KU-RO/PO-TO-KU-RO totals in the corpus: {n}")
print(f"  exact under at least one frozen segmentation : {len(ex)}  ({100*len(ex)/n:.1f}%)")
und=[r for r in rows if not r['dmg']]
undex=[r for r in und if r['exact']]
print(f"  on faces with NO numeric damage ({len(und)} totals): exact {len(undex)} "
      f"({100*len(undex)/max(1,len(und)):.1f}%)")
dam=[r for r in rows if r['dmg']]
print(f"  on damaged faces ({len(dam)} totals)              : exact "
      f"{len([r for r in dam if r['exact']])} ({100*len([r for r in dam if r['exact']])/max(1,len(dam)):.1f}%)")

print("\n--- NON-EXACT totals on UNDAMAGED faces (the hard counterexamples) ---")
for r in sorted(und, key=lambda r: r['face']):
    if r['exact']: continue
    print(f"  {r['face']:10s} {r['mark']:11s} stated {r['tot']:7g}  "
          f"SEG-MAX {r['mx'][0]:7g} (n={r['mx'][1]})  SEG-SCOPE {r['sc'][0]:7g} "
          f"(n={r['sc'][1]}, {r['sc'][2]})  [{r['scribe']}]")

print("\n--- every total on a tablet the claim names ---")
NAMED={"HT85a","HT85b","HT87","HT88","HT94a","HT94b","HT112a","HT112b","HT117a","HT117b",
       "HT119","HT122a","HT122b","HT128a","HT128b","HT132","HT135a","HT135b","HT1","HT2",
       "HT15","HT28","HT30","HT34","HT37","HT86","HT95","HT123+124a","HT123+124b"}
for r in rows:
    if r['face'] not in NAMED: continue
    tag = "EXACT" if r['exact'] else "NOT-EXACT"
    print(f"  {r['face']:11s} {r['mark']:11s} stated {r['tot']:6g}  SEG-MAX {r['mx'][0]:6g}"
          f"  SEG-SCOPE {r['sc'][0]:6g} ({r['sc'][2]})  {tag:9s} numeric-damage={r['dmg']}"
          f"  [{r['scribe']}]")
