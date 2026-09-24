#!/usr/bin/env python3
"""Tests of the predictions registered in FREEZE.md (P-A .. P-E).

Run AFTER FREEZE.md was committed. Nothing here was used to derive the
balance result, which rests on aggregate letter counts alone.
"""
import collections, random, math, os, json, re

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(20260924)
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

STRINGS = [l.strip() for l in open(os.path.join(HERE,"data","cryptograms.txt")) if l.strip()]
ALL = "".join(STRINGS); N = len(ALL); LENGTHS=[len(s) for s in STRINGS]

INST=[]
for i,line in enumerate(open(os.path.join(HERE,"data","instances.tsv"))):
    if i==0: continue
    bar,_,s = line.rstrip("\n").split("\t"); INST.append((bar,s))

def chi2(text):
    c=collections.Counter(text); e=len(text)/26
    return sum((c.get(a,0)-e)**2/e for a in A)

def gammainc_lower_reg(a,x,terms=4000):
    s=1.0/a; t=1.0/a
    for n in range(1,terms):
        t*=x/(a+n); s+=t
        if abs(t)<1e-18*abs(s): break
    return s*math.exp(-x+a*math.log(x)-math.lgamma(a))
def chi2_cdf(x,k): return gammainc_lower_reg(k/2, x/2)

def pooled_ic(strings):
    num=den=0
    for s in strings:
        c=collections.Counter(s); n=len(s)
        num+=sum(v*(v-1) for v in c.values()); den+=n*(n-1)
    return num/den if den else float("nan")

def deal():
    """Null: random deal of the EXACT observed letter multiset into the
    EXACT observed length structure. This is H2 made operational."""
    pool=list(ALL); random.shuffle(pool)
    out=[];i=0
    for L in LENGTHS: out.append("".join(pool[i:i+L])); i+=L
    return out

R=20000
def pctl(v,q):
    v=sorted(v); return v[min(int(q*len(v)),len(v)-1)]
def report(name,obs,sims,direction="two"):
    n=len(sims); ge=sum(1 for x in sims if x>=obs); le=sum(1 for x in sims if x<=obs)
    p = min(1.0,2*min((ge+1)/(n+1),(le+1)/(n+1))) if direction=="two" else (ge+1)/(n+1)
    m=sum(sims)/n
    print(f"    {name:34s} obs={obs:9.4f}  null mean={m:8.4f} "
          f"95%=[{pctl(sims,.025):8.4f},{pctl(sims,.975):8.4f}]  p={p:.4f}")
    return p

out={}
print("="*78)
print("P-A  Is the balance a property of the INVENTORY or of the PHYSICAL TEXT?")
print("="*78)
inst_text="".join(s for _,s in INST)
c_inv, c_ins = chi2(ALL), chi2(inst_text)
print(f"  inventory  (16 distinct strings, {N} letters): chi2 = {c_inv:.3f}   "
      f"P(chi2_25<=obs) = {chi2_cdf(c_inv,25):.3e}")
print(f"  instances  (44 stamped lines, {len(inst_text)} letters): chi2 = {c_ins:.3f}  "
      f"P(chi2_25>=obs) = {1-chi2_cdf(c_ins,25):.3e}")
print(f"  -> instance corpus is {'NON-UNIFORM (P-A CONFIRMED)' if c_ins>25 else 'still flat (P-A FAILED)'}")
cc=collections.Counter(inst_text)
print("  instance counts:", " ".join(f"{a}{cc[a]}" for a in A))
out["P_A"]={"chi2_inventory":c_inv,"chi2_instances":c_ins,
            "n_instances":len(inst_text),"confirmed":bool(c_ins>25)}

print()
print("="*78)
print("P-B  Is any per-bar SUBSET as balanced as the whole inventory?")
print("="*78)
bars=collections.OrderedDict()
for bar,s in INST: bars.setdefault(bar,[]).append(s)
sub=[]
for bar,ss in bars.items():
    d=sorted(set(ss)); t="".join(d)
    # chi2 scaled to be comparable: report chi2/df and the uniform-CDF position
    print(f"  bar {bar:6s} {len(d):2d} distinct strings, {len(t):3d} letters:"
          f"  chi2={chi2(t):7.3f}  P(chi2_25<=obs)={chi2_cdf(chi2(t),25):.4f}")
    sub.append(chi2_cdf(chi2(t),25))
print(f"  whole inventory: P(chi2_25<=obs) = {chi2_cdf(c_inv,25):.3e}")
print(f"  -> {'no subset approaches the whole-set balance (P-B CONFIRMED)' if min(sub)>chi2_cdf(c_inv,25)*100 else 'a subset rivals it (P-B FAILED)'}")
out["P_B"]={"bar_cdf":sub,"inventory_cdf":chi2_cdf(c_inv,25)}

print()
print("="*78)
print("P-C  Order structure: anything a random deal of the pool cannot produce?")
print("="*78)
def maxmult(ss): return max(max(collections.Counter(s).values()) for s in ss)
def doubles(ss): return sum(1 for s in ss for a,b in zip(s,s[1:]) if a==b)
def maxstr_ic(ss): return max(pooled_ic([s]) for s in ss if len(s)>=12)
def periodic_ic(ss,p):
    num=den=0
    for s in ss:
        if len(s)<2*p: continue
        for r in range(p):
            cs=s[r::p]; c=collections.Counter(cs); n=len(cs)
            num+=sum(v*(v-1) for v in c.values()); den+=n*(n-1)
    return num/den if den else float("nan")
stats={"max letter multiplicity/string":maxmult,
       "adjacent doubles":doubles,
       "max single-string IC":maxstr_ic,
       "pooled IC":pooled_ic}
for p in range(2,9): stats[f"periodic IC, period {p}"]=(lambda p: (lambda ss: periodic_ic(ss,p)))(p)
sims={k:[] for k in stats}
for _ in range(R):
    d=deal()
    for k,fn in stats.items(): sims[k].append(fn(d))
out["P_C"]={}
fails=[]
for k,fn in stats.items():
    o=fn(STRINGS); p=report(k,o,sims[k])
    out["P_C"][k]={"observed":o,"p":p}
    if p<0.05: fails.append(k)
print(f"  -> {'ALL inside the deal null (P-C CONFIRMED)' if not fails else 'OUTLIERS: '+str(fails)}")

print()
print("  Power check for the periodic tests (can they even fire?):")
for p in [2,3,4,5]:
    den=sum(len(s[r::p])*(len(s[r::p])-1) for s in STRINGS if len(s)>=2*p for r in range(p))
    se=math.sqrt(0.038*(1-0.038)/max(den,1))*2
    print(f"    period {p}: {den:5d} coset pairs -> IC s.e. ~{se:.4f}; "
          f"English IC 0.066 is {(0.066-0.038)/se:5.1f} s.e. away")

print()
print("="*78)
print("P-D  Is GALLOW evidence of leakage?")
print("="*78)
words=set()
for w in re.findall(r"[A-Za-z]{6,}", open(os.path.join(HERE,"..","..","..","..",
        "historical-controversies/junius-letters-authorship/attempts/"
        "2026-09-17-genre-matched-openset/data/raw/gutenberg_2173.txt"),
        encoding="utf-8",errors="ignore").read()):
    words.add(w.upper())
print(f"  wordlist: {len(words)} distinct English words of length>=6")
def nwords(ss):
    n=0
    for s in ss:
        for i in range(len(s)):
            for L in range(6,min(9,len(s)-i)+1):
                if s[i:i+L] in words: n+=1
    return n
o=nwords(STRINGS)
sim=[nwords(deal()) for _ in range(R)]
p=report("English substrings len>=6",o,sim)
print(f"  observed hits: {[s[i:i+L] for s in STRINGS for i in range(len(s)) for L in range(6,min(9,len(s)-i)+1) if s[i:i+L] in words]}")
print(f"  -> {'GALLOW is NOT evidence of plaintext (P-D CONFIRMED)' if p>0.05 else 'excess English substrings (P-D FAILED)'}")
out["P_D"]={"observed":o,"p":p}

print()
print("="*78)
print("P-E  Can transcription error explain the observed chi2 from each origin?")
print("="*78)
def corrupt(text,k):
    t=list(text)
    for i in random.sample(range(len(t)),k): t[i]=random.choice(A)
    return "".join(t)
balanced="".join(a*10 for a in A)+"EIS"          # exactly-balanced 263-letter original
print("  origin = exactly balanced (10 each + 3):")
for k in [0,2,4,6,8,12,20]:
    v=[chi2(corrupt(balanced,k)) for _ in range(4000)]
    print(f"    {k:2d} misread letters: chi2 median={pctl(v,.5):6.2f}  "
          f"95%=[{pctl(v,.025):5.2f},{pctl(v,.975):6.2f}]  "
          f"P(chi2<=1.251)={sum(1 for x in v if x<=1.251)/len(v):.3f}")
print("  origin = a genuine flat-output cipher (uniform random 263 letters):")
for k in [0,10,30]:
    v=[chi2(corrupt("".join(random.choice(A) for _ in range(263)),k)) for _ in range(4000)]
    print(f"    {k:2d} misread letters: chi2 median={pctl(v,.5):6.2f}  "
          f"95%=[{pctl(v,.025):5.2f},{pctl(v,.975):6.2f}]  "
          f"P(chi2<=1.251)={sum(1 for x in v if x<=1.251)/len(v):.4f}")
out["P_E"]="see stdout"

json.dump(out,open(os.path.join(HERE,"out","confirm.json"),"w"),indent=1,default=str)
print("\nwrote out/confirm.json")
