#!/usr/bin/env python3
"""EXPERIMENT 1 -- pipeline validation.

Reproduce the established Federalist result (Mosteller & Wallace 1964): the
disputed papers are Madison's. If the pipeline cannot recover this, any result
it gives on a 470-word ballad is a bug, not a finding.
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import *

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
papers = json.load(open(f'{S}/corpus/federalist.json'))

ham = [p for p in papers if p['author'] == 'HAMILTON']
mad = [p for p in papers if p['author'] == 'MADISON']
dis = sorted([p for p in papers if p['author'] == 'HAMILTON OR MADISON'],
             key=lambda p: p['no'])

print(f"Hamilton undisputed: {len(ham)} papers, {sum(p['n_words'] for p in ham)} words")
print(f"Madison  undisputed: {len(mad)} papers, {sum(p['n_words'] for p in mad)} words")
print(f"Disputed: {[p['no'] for p in dis]}\n")

for metric in ('burrows', 'cosine'):
    for n_mfw in (100, 300):
        train = {'HAMILTON': '\n'.join(p['text'] for p in ham),
                 'MADISON':  '\n'.join(p['text'] for p in mad)}
        mfw = mfw_list(list(train.values()), n_mfw)
        # z-scale over the individual training papers (standard practice)
        units = [(p['author'], p['text']) for p in ham + mad]
        means, sds = zscale([freq_vec(t, mfw) for _, t in units])
        prof = {a: zvec(freq_vec(t, mfw), means, sds) for a, t in train.items()}
        res = []
        for p in dis:
            q = zvec(freq_vec(p['text'], mfw), means, sds)
            d = {a: DIST[metric](q, v) for a, v in prof.items()}
            res.append((p['no'], min(d, key=d.get), d['HAMILTON'] - d['MADISON']))
        nmad = sum(1 for _, a, _ in res if a == 'MADISON')
        print(f"{metric:8s} MFW={n_mfw:4d}  disputed -> Madison: {nmad}/{len(res)}")
        print("          " + "  ".join(f"{n}:{a[:3]}" for n, a, _ in res))

# --- leave-one-out on the undisputed papers, full length
units = [(p['author'], p['text']) for p in ham + mad + [q for q in papers if q['author'] == 'JAY']]
for metric in ('burrows', 'cosine'):
    n, c, cases, k = attribute_loo(units, n_mfw=300, metric=metric)
    print(f"\nLOO undisputed, full papers, {metric}, MFW=300: {c}/{n} = {c/n:.3f} (k={k}, chance~{1/k:.3f})")
