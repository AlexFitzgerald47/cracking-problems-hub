#!/usr/bin/env python3
"""Two follow-ups: (1) the IACR-vs-Pelling transcription dispute, adjudicated
by the balance statistic; (2) degrees of freedom in the one public solution
claim."""
import collections, math
A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def chi2(t):
    c=collections.Counter(t); e=len(t)/26
    return sum((c.get(a,0)-e)**2/e for a in A)
def gil(a,x,n=4000):
    s=t=1.0/a
    for i in range(1,n):
        t*=x/(a+i); s+=t
        if abs(t)<1e-18*abs(s): break
    return s*math.exp(-x+a*math.log(x)-math.lgamma(a))
cdf=lambda x,k: gil(k/2,x/2)

iacr=[l.strip() for l in open("data/cryptograms.txt") if l.strip()]
# Pelling / Cipher Foundation differ on exactly two strings
pell=[("UGMNCBXCKDBEY" if s=="UGMNCBXCFLDBEY" else
       "KOWVRSRWTMLDH" if s=="KOWVRSRKWTMLDH" else s) for s in iacr]

print("=== Transcription dispute: IACR vs Pelling/CipherFoundation ===")
print("  disputed strings: UGMNCBXCFLDBEY / UGMNCBXCKDBEY")
print("                    KOWVRSRKWTMLDH / KOWVRSRWTMLDH")
for name,S in [("IACR    ",iacr),("Pelling ",pell)]:
    t="".join(S); c=collections.Counter(t)
    n10=sum(1 for a in A if c[a]==10)
    print(f"  {name} N={len(t)}  chi2={chi2(t):7.3f}  P(chi2_25<=obs)={cdf(chi2(t),25):.3e}"
          f"   letters at exactly 10: {n10}/26")
    print(f"           counts: {' '.join(f'{a}{c[a]}' for a in A if c[a]!=10) or '(all exactly 10)'}")
print("  -> the balance statistic PREFERS the IACR reading; it is a checkable")
print("     prediction about the two disputed characters on bar 5.1.")

print()
print("=== Degrees of freedom in the Milton Kim (2024) claim ===")
ct="FEWGDRHDDEEUMFFTEEMJXZR"; pt="OUSTGOVPBANKCTGOLEESVOG"
print(f"  cipher: {ct}  ({len(ct)})")
print(f"  plain : {pt}  ({len(pt)})")
m=collections.defaultdict(set)
for a,b in zip(ct,pt): m[a].add(b)
incons={k:sorted(v) for k,v in m.items() if len(v)>1}
print(f"  ciphertext letters mapping to MORE THAN ONE plaintext letter: {len(incons)}")
for k,v in sorted(incons.items()): print(f"    {k} -> {','.join(v)}")
tot=sum(len(v)-1 for v in m.values())
print(f"  minimum extra free choices beyond a single substitution alphabet: {tot}")
print("  -> the mapping is not a function, so it is not a substitution of any")
print("     kind; with an unpublished position-dependent rule the output is")
print("     unconstrained and the claim carries no evidential weight as stated.")
