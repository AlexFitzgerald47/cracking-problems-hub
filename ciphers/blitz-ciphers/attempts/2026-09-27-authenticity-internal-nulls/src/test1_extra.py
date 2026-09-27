import sys, os, json
from collections import Counter
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_blitz, load_canonical, flat

COMP = sys.argv[1]
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def hz(a, b, nperm=4000, seed=0):
    vocab = {t: i for i, t in enumerate(sorted(set(a) | set(b)))}
    K = len(vocab)
    pool = np.array([vocab[t] for t in list(a) + list(b)])
    na, n = len(a), len(a) + len(b)
    tot = np.bincount(pool, minlength=K).astype(float)
    ea, eb = tot * na / n, tot * (n - na) / n
    f = lambda idx: float((((np.bincount(pool[idx[:na]], minlength=K) - ea) ** 2 / ea)
                           + ((tot - np.bincount(pool[idx[:na]], minlength=K) - eb) ** 2 / eb)).sum())
    obs = f(np.arange(n))
    rng = np.random.default_rng(seed)
    v = np.array([f(rng.permutation(n)) for _ in range(nperm)])
    return (obs - v.mean()) / v.std(ddof=1)


def block(lines, want, skip=0):
    out = []
    for l in lines:
        out.extend(l)
        if len(out) >= skip + want:
            break
    return out[skip:skip + want] if len(out) >= skip + want else None


borg = load_canonical(os.path.join(COMP, "borg"))
ks = sorted(borg)
zs = []
for i in range(len(ks) - 1):
    x, y = block(borg[ks[i]], 250), block(borg[ks[i + 1]], 159)
    if x and y:
        zs.append(hz(x, y, seed=700 + i))
zs.sort()
q = lambda p: zs[min(len(zs) - 1, int(p * len(zs)))]
print(f"(a) borg between-page at (250,159): n={len(zs)}  z p05={q(.05):+.2f} "
      f"med={q(.5):+.2f} p95={q(.95):+.2f} max={zs[-1]:+.2f}   >= 8.29: "
      f"{sum(1 for z in zs if z >= 8.29)}/{len(zs)}")

blitz = load_blitz(os.path.join(HERE, "data"))
a, b = flat(blitz["p7"]), flat(blitz["p8"])
ca, cb = Counter(a), Counter(b)
na, nb, n = len(a), len(b), len(a) + len(b)
rows = []
for s in set(ca) | set(cb):
    tot = ca[s] + cb[s]
    ea, eb = tot * na / n, tot * nb / n
    c = (ca[s] - ea) ** 2 / ea + (cb[s] - eb) ** 2 / eb
    rows.append((c, s, ca[s], cb[s], 1000 * ca[s] / na, 1000 * cb[s] / nb))
rows.sort(reverse=True)
tot_chi = sum(r[0] for r in rows)
print(f"\n(b) Blitz p7-vs-p8 chi2 = {tot_chi:.1f}; top contributors "
      f"(rate per 1000 tokens):")
cum = 0
for c, s, x, y, rx, ry in rows[:12]:
    cum += c
    print(f"    {s!r:5s} chi2={c:6.2f} ({100*c/tot_chi:4.1f}%, cum {100*cum/tot_chi:4.1f}%)  "
          f"p7 {x:3d} ({rx:5.1f}/k)   p8 {y:3d} ({ry:5.1f}/k)")
print(f"    types only in p7: {sorted(set(ca)-set(cb))}")
print(f"    types only in p8: {sorted(set(cb)-set(ca))}")
json.dump({"borg_250_159_z": zs,
           "blitz_symbol_contributions": [[s, x, y, c] for c, s, x, y, _, _ in rows]},
          open(os.path.join(HERE, "out", "test1_extra.json"), "w"), indent=1)
