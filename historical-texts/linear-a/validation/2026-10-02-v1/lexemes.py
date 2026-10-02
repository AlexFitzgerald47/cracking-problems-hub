#!/usr/bin/env python3
"""V1 reproduction, part 5: every attestation of the claim's glossed sign-groups."""
import sys, collections
sys.path.insert(0,'.')
from census import A, is_sg, ival, DIV
TARGETS=["A-DU","A-KA-RU","KA-RU","DA-DU-MA-TA","KI-KI-RA-JA","MA-KA-RI-TE",
         "U-MI-NA-SI","SA-TA","*21F-TU-NE","KU-DA","PO-TO-KU-RO"]
for t in TARGETS:
    hits=[k for k in sorted(A) if t in A[k]['transliteratedWords']]
    print(f"\n### {t}  — {len(hits)} attestation(s)")
    for k in hits:
        v=A[k]; ws=v['transliteratedWords']
        i=ws.index(t); nxt=next((x for x in ws[i+1:] if x!="\n"), None)
        print(f"  {k:11s} [{v.get('scribe') or '-':13s}] next={nxt!r}")
        line=' '.join(ws).replace(' \n ',' | ')
        print("      "+line)

print("\n\n### HT95 polarity test: DA-DU-MA-TA (a, 'assessed') vs A-DU (b, 'rendered')")
def pairs(face):
    ws=A[face]['transliteratedWords']; out={}
    for i,w in enumerate(ws):
        if is_sg(w):
            nx=next((x for x in ws[i+1:] if x!="\n"), None)
            if nx is not None and ival(nx) is not None: out[w]=ival(nx)
    return out
a=pairs('HT95a'); b=pairs('HT95b')
print("  HT95a (DA-DU-MA-TA GRA):", {k:int(v) for k,v in a.items()})
print("  HT95b (A-DU):           ", {k:int(v) for k,v in b.items()})
for k in sorted(set(a)&set(b)):
    rel = "=" if a[k]==b[k] else ("rendered<assessed OK" if b[k]<a[k] else "rendered>ASSESSED  <-- contradicts polarity")
    print(f"    {k:10s} a={int(a[k]):3d}  b={int(b[k]):3d}   {rel}")
print("  -> on the only tablet that puts the two headings on opposite faces, the values are")
print("     mostly EQUAL and one entry runs the wrong way; the assessed/rendered polarity is")
print("     not recoverable from the numbers.")

print("\n### HT86: A-KA-RU as 'forward-declared aggregate'?")
for k in ['HT86a','HT86b','HT2']:
    print("  "+k+": "+' '.join(A[k]['transliteratedWords']).replace(' \n ',' | '))
print("  A-KA-RU is followed by a NUMERAL in 1 of its 3 attestations (HT2 only, and there")
print("  the numeral belongs to the ideogram OLE+U).  In HT86a/b it heads a list with no")
print("  aggregate at all, and HT86a then uses A-DU the same way after a ruling.")
