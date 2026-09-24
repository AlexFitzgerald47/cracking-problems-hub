#!/usr/bin/env python3
"""EXPERIMENT 2 -- power analysis on a validated corpus.

How does attribution accuracy depend on (a) the length of the questioned text
L and (b) the amount of attested text per candidate T?

Run on the Federalist (prose, 3 authors, pipeline validated in exp1), so the
curve is a BEST CASE: one genre, one register, one decade, one collaboration.
"The Night Before Larry Was Stretched" is ~470 words and its candidates have
far less attested text than this, in a different register. Whatever this curve
says at L=470 is an UPPER BOUND on what is achievable for Larry.

Holdout is by PAPER, so no test text contributes to its own author profile.
"""
import json, sys, os, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens, DIST

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
papers = json.load(open(f'{S}/corpus/federalist.json'))
AUTHORS = ['HAMILTON', 'MADISON', 'JAY']
pool = {a: [tokens(p['text']) for p in papers if p['author'] == a] for a in AUTHORS}
for a in AUTHORS:
    print(f"{a}: {len(pool[a])} papers, {sum(len(t) for t in pool[a])} tokens")

def window(toks, L, rng):
    if len(toks) <= L:
        return toks
    s = rng.randrange(0, len(toks) - L)
    return toks[s:s+L]

def vec(counter, n, mfw):
    return [counter[w] / n for w in mfw]

def zfit(vecs):
    k = len(vecs[0]); means = []; sds = []
    for j in range(k):
        col = [v[j] for v in vecs]
        m = sum(col)/len(col)
        var = sum((x-m)**2 for x in col)/len(col)
        means.append(m); sds.append(var**0.5 if var > 0 else 1e-12)
    return means, sds

def z(v, m, s):
    return [(v[j]-m[j])/s[j] for j in range(len(v))]

def run(L, T, metric='cosine', n_mfw=100, reps=6, seed=0, authors=AUTHORS):
    rng = random.Random(seed)
    correct = tot = 0
    for rep in range(reps):
        for a in authors:
            for pi, p in enumerate(pool[a]):
                if len(p) < L:
                    continue
                test = window(p, L, rng)
                tr = {}
                ok = True
                for b in authors:
                    w = []
                    for qi, q in enumerate(pool[b]):
                        if b == a and qi == pi:
                            continue
                        w.extend(q)
                    if len(w) < T:
                        ok = False; break
                    st = rng.randrange(0, len(w) - T) if len(w) > T else 0
                    tr[b] = w[st:st+T]
                if not ok:
                    return None
                # MFW over the pooled training material only
                cnt = Counter()
                for w in tr.values():
                    cnt.update(w)
                mfw = [x for x, _ in cnt.most_common(n_mfw)]
                tv = {b: vec(Counter(w), len(w), mfw) for b, w in tr.items()}
                # z-scale on training profiles + the training material split in
                # halves, so the scale is estimated from >k vectors
                scale_src = list(tv.values())
                for b, w in tr.items():
                    h = len(w)//2
                    scale_src.append(vec(Counter(w[:h]), h, mfw))
                    scale_src.append(vec(Counter(w[h:]), len(w)-h, mfw))
                m, s = zfit(scale_src)
                prof = {b: z(v, m, s) for b, v in tv.items()}
                q = z(vec(Counter(test), len(test), mfw), m, s)
                d = {b: DIST[metric](q, pv) for b, pv in prof.items()}
                if min(d, key=d.get) == a:
                    correct += 1
                tot += 1
    return correct, tot

if __name__ == '__main__':
    Ls = (5000, 2000, 1000, 700, 470, 300, 200)
    Ts = (6000, 3000, 1500, 750, 470, 250)
    print("\nFederalist power curve -- 3 authors, chance = 0.333, cosine Delta, MFW=100")
    print("rows: T = training words per candidate; cols: L = questioned-text words\n")
    print('T \\ L'.rjust(8) + ''.join(f"{L:>8d}" for L in Ls))
    grid = {}
    for T in Ts:
        row = f"{T:>8d}"
        for L in Ls:
            r = run(L, T, reps=6, seed=T*7+L)
            if r is None:
                row += "     n/a"
            else:
                c, n = r
                grid[(T, L)] = (c, n)
                row += f"{c/n:>8.3f}"
        print(row)
    json.dump({f"{k[0]}_{k[1]}": v for k, v in grid.items()},
              open(f'{S}/results/exp2_federalist_power.json', 'w'), indent=1)
