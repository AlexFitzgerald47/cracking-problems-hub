#!/usr/bin/env python3
"""EXPERIMENT 4 -- how big is the cant-verse <-> prose register gap?

Five authors appear BOTH in Farmer's *Musa Pedestris* (canting songs) and in a
large non-song prose corpus. That lets the register gap be measured rather than
asserted. Identical candidate set (k=5), identical method, identical test
texts across conditions; only the register the PROFILE is built from changes,
so exactly one thing is permuted per control.

  A  same register   canting song  -> other canting songs by the 5 authors
  B  cross register  canting song  -> the same 5 authors' prose
  C  prose control   470-word prose -> the same 5 authors' prose

Prose profiles are capped at the same number of words in every condition so
that condition B is not also a corpus-size experiment.

Predictions frozen in FREEZE.md before this was run: C > A > B, B at chance.
"""
import json, sys, os, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from delta import tokens, DIST

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
songs = json.load(open(f'{S}/corpus/musa_songs.json'))
prose = json.load(open(f'{S}/corpus/prose_corpora.json'))
AUTHORS = sorted(prose)                       # the 5 dual-register authors
K = len(AUTHORS)

by_a = defaultdict(list)
for s in songs:
    if s['author'] in prose:
        by_a[s['author']].append(s)

print("dual-register authors (canting songs + prose):")
for a in AUTHORS:
    print(f"  {a:18s} songs={len(by_a[a])}  song words={sum(s['n_words'] for s in by_a[a]):5d}"
          f"  prose words={len(tokens(prose[a])):6d}")
print(f"k = {K}, chance = {1/K:.3f}\n")

def vec(seq, mfw):
    c = Counter(seq); n = len(seq) or 1
    return [c[w]/n for w in mfw]

def zfit(vs):
    m, s = [], []
    for j in range(len(vs[0])):
        col = [v[j] for v in vs]
        mu = sum(col)/len(col)
        var = sum((x-mu)**2 for x in col)/len(col)
        m.append(mu); s.append(var**0.5 if var > 0 else 1e-12)
    return m, s

def zz(v, m, s):
    return [(v[j]-m[j])/s[j] for j in range(len(v))]

def classify(test_toks, profiles_toks, n_mfw, metric):
    cnt = Counter()
    for t in profiles_toks.values():
        cnt.update(t)
    mfw = [w for w, _ in cnt.most_common(n_mfw)]
    pv = {a: vec(t, mfw) for a, t in profiles_toks.items()}
    scale = list(pv.values())
    for a, t in profiles_toks.items():          # halves, so scale has >k rows
        h = len(t)//2
        scale.append(vec(t[:h], mfw)); scale.append(vec(t[h:], mfw))
    m, s = zfit(scale)
    prof = {a: zz(v, m, s) for a, v in pv.items()}
    q = zz(vec(test_toks, mfw), m, s)
    d = {a: DIST[metric](q, p) for a, p in prof.items()}
    return min(d, key=d.get), d

PROSE_CAP = 8000     # words per author in every prose profile

def cond_A(n_mfw, metric, rng):
    """canting song -> other canting songs (same register)."""
    ok = tot = 0
    for a in AUTHORS:
        if len(by_a[a]) < 2:
            continue
        for i, s in enumerate(by_a[a]):
            prof = {}
            skip = False
            for b in AUTHORS:
                txts = [x['text'] for j, x in enumerate(by_a[b])
                        if not (b == a and j == i)]
                if not txts:
                    skip = True; break
                prof[b] = tokens('\n'.join(txts))
            if skip:
                continue
            pred, _ = classify(tokens(s['text']), prof, n_mfw, metric)
            ok += (pred == a); tot += 1
    return ok, tot

def prose_profiles(rng, cap=PROSE_CAP):
    out = {}
    for a in AUTHORS:
        t = tokens(prose[a])
        st = rng.randrange(0, max(1, len(t)-cap))
        out[a] = t[st:st+cap]
    return out

def cond_B(n_mfw, metric, rng, reps=12):
    """canting song -> prose (cross register)."""
    ok = tot = 0
    for _ in range(reps):
        prof = prose_profiles(rng)
        for a in AUTHORS:
            for s in by_a[a]:
                pred, _ = classify(tokens(s['text']), prof, n_mfw, metric)
                ok += (pred == a); tot += 1
    return ok, tot

def cond_C(n_mfw, metric, rng, L=470, reps=12):
    """470-word prose sample -> prose (same register, matched length).
    The test window is drawn from a held-out part of the author's prose and
    excluded from that author's profile, so there is no self-overlap."""
    ok = tot = 0
    for _ in range(reps):
        full = {a: tokens(prose[a]) for a in AUTHORS}
        for a in AUTHORS:
            t = full[a]
            st = rng.randrange(0, len(t)-L)
            test = t[st:st+L]
            prof = {}
            for b in AUTHORS:
                tb = full[b]
                if b == a:
                    tb = tb[:st] + tb[st+L:]        # hold the window out
                s2 = rng.randrange(0, max(1, len(tb)-PROSE_CAP))
                prof[b] = tb[s2:s2+PROSE_CAP]
            pred, _ = classify(test, prof, n_mfw, metric)
            ok += (pred == a); tot += 1
    return ok, tot

if __name__ == '__main__':
    rows = {}
    print(f"{'cond':6s} {'metric':8s} {'MFW':>5s} {'acc':>7s} {'n':>5s}")
    for metric in ('cosine', 'burrows'):
        for n_mfw in (50, 100, 200):
            rng = random.Random(4242 + n_mfw)
            for name, fn in (('A', cond_A), ('B', cond_B), ('C', cond_C)):
                ok, tot = fn(n_mfw, metric, rng)
                rows[f'{name}_{metric}_{n_mfw}'] = {'ok': ok, 'n': tot, 'acc': ok/tot}
                print(f"{name:6s} {metric:8s} {n_mfw:5d} {ok/tot:7.3f} {tot:5d}")
    json.dump({'k': K, 'chance': 1/K, 'authors': AUTHORS, 'rows': rows},
              open(f'{S}/results/exp4_register_gap.json', 'w'), indent=1)
    print("\nsummary (mean over the 6 metric x MFW cells):")
    for name in 'ABC':
        v = [r['acc'] for k, r in rows.items() if k.startswith(name + '_')]
        print(f"  {name}: {sum(v)/len(v):.3f}   (min {min(v):.3f}, max {max(v):.3f})")
