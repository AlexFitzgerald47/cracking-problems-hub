#!/usr/bin/env python3
"""P3: can a depleting physical letter supply produce this inventory?

Validator 2's alternative to deliberate composition is "a compositor's case at
ten sorts per letter, or a tile bag, drawn once while the 16 strings were first
drafted". Formally that is a UNIFORM URN of c tiles per letter drawn without
replacement. Such a model has exactly one free parameter, c, and it is
squeezed from both sides:

  * to be as flat as the observed inventory the urn must be nearly exhausted,
    which forces c to be small (E[chi2] = 25 * (M-n)/(M-1) for M = 26c);
  * to contain 13 of any letter it must have c >= 13, which makes it big.

This measures the squeeze directly by simulation: for each c, the joint
probability of being at least this flat AND containing a letter used 13 times.
"""
import random, collections, os, sys, json
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

txt = "".join(l.strip() for l in open(os.path.join(HERE,"data","cryptograms_corrected.txt")) if l.strip())
cnt = collections.Counter(txt)
obs = [cnt.get(x,0) for x in A]
n = sum(obs); K = 26
e = n / K
obs_chi2 = sum((x-e)**2 for x in obs)/e
obs_max = max(obs)
print(f"observed: n={n}  chi2={obs_chi2:.4f}  max letter count={obs_max}")
print(f"\nuniform urn of c tiles per letter, draw {n} without replacement, {'{:,}'.format(50000)} reps each\n")
print(f"{'c':>3} {'urn M':>6} {'E[chi2] theory':>15} {'P(chi2<=obs)':>14} {'P(max>=13)':>12} {'P(both)':>10}")
rows=[]
REPS=50000
for c in range(10, 27):
    M = K*c
    if M < n: 
        print(f"{c:>3} {M:>6}  urn smaller than the text -- impossible"); continue
    rng = random.Random(4242+c)
    theory = 25*(M-n)/(M-1)
    flat=0; big=0; both=0
    urn0 = []
    for i,ch in enumerate(A): urn0 += [i]*c
    for _ in range(REPS):
        draw = rng.sample(urn0, n)
        cc=[0]*K
        for d in draw: cc[d]+=1
        f = sum((x-e)**2 for x in cc)/e <= obs_chi2 + 1e-12
        b = max(cc) >= obs_max
        flat+=f; big+=b; both+= (f and b)
    rows.append({"c":c,"M":M,"theory":theory,"P_flat":flat/REPS,"P_max":big/REPS,"P_both":both/REPS})
    print(f"{c:>3} {M:>6} {theory:>15.3f} {flat/REPS:>14.5f} {big/REPS:>12.5f} {both/REPS:>10.5f}")
json.dump(rows, open(os.path.join(HERE,"out","urn.json"),"w"), indent=2)
best = max(rows, key=lambda r: r["P_both"])
print(f"\nbest uniform urn: c={best['c']} with P(both) = {best['P_both']:.5f}")
print(f"P3 predicted every c below 0.01 -> {'CONFIRMED' if best['P_both'] < 0.01 else 'REFUTED'}")
