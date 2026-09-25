#!/usr/bin/env python3
"""P4: within-string letter reuse against the exact-multiset deal null.

Validator 2's only discriminating lead: max distinct letters in any one string,
observed 15 against a null mean 17.89, p = 0.010 on the IACR corpus. Re-run on
the photographic corpus, with the other reuse statistics alongside so the
multiple-comparison budget is visible rather than implicit.
"""
import collections, random, os, json
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p):
    return [l.strip() for l in open(os.path.join(HERE,"data",p)) if l.strip()]

def stats(strings):
    d = [len(set(s)) for s in strings]
    return {
        "max_distinct": max(d),
        "sum_distinct": sum(d),
        "mean_distinct_frac": sum(len(set(s))/len(s) for s in strings)/len(strings),
        "repeated_letter_events": sum(len(s)-len(set(s)) for s in strings),
        "doubles": sum(1 for s in strings for a,b in zip(s,s[1:]) if a==b),
        "max_multiplicity": max(max(collections.Counter(s).values()) for s in strings),
    }

def run(name, path, reps=200000, seed=7):
    strings = load(path); lengths=[len(s) for s in strings]
    pool=list("".join(strings)); rng=random.Random(seed)
    obs=stats(strings)
    null=collections.defaultdict(list)
    for _ in range(reps):
        p=pool[:]; rng.shuffle(p); k=0; sim=[]
        for L in lengths: sim.append("".join(p[k:k+L])); k+=L
        st=stats(sim)
        for kk,v in st.items(): null[kk].append(v)
    print(f"\n=== {name} ({len(strings)} strings, {sum(lengths)} letters), exact-multiset deal null, {reps:,} reps ===")
    out={}
    for kk,v in obs.items():
        arr=null[kk]; m=sum(arr)/len(arr)
        sd=(sum((x-m)**2 for x in arr)/len(arr))**0.5
        p_lo=(sum(1 for x in arr if x<=v)+1)/(reps+1)
        p_hi=(sum(1 for x in arr if x>=v)+1)/(reps+1)
        print(f"  {kk:<24} obs={v:>9.4f}  null={m:>8.3f} +/- {sd:<6.3f}  p(<=)={p_lo:.5f}  p(>=)={p_hi:.5f}")
        out[kk]={"obs":v,"null_mean":m,"null_sd":sd,"p_le":p_lo,"p_ge":p_hi}
    return out

r1=run("IACR corpus", "../../2026-09-24-is-it-a-cipher/data/cryptograms.txt")
r2=run("photographic corpus", "cryptograms_corrected.txt")
json.dump({"iacr":r1,"photographic":r2}, open(os.path.join(HERE,"out","reuse.json"),"w"), indent=2)
print("\nSix statistics were computed, so the Bonferroni-corrected 0.05 threshold is 0.0083.")
