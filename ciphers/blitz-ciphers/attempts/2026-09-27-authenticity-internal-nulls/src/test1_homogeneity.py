"""Test 1 of FREEZE.md (EXPLORATORY): do Blitz pages 7 and 8 share a symbol
distribution?  Two-sample chi-square homogeneity, standardised against a
pooled-permutation null at the observed sizes (470, 159), with length-matched
reference distributions from Copiale and Borg.

between-page: 470 contiguous tokens from page i, 159 from page i+1.
within-page : 470 then the next 159 tokens of the same page.

Usage: python3 src/test1_homogeneity.py <comparanda_dir> [nperm]
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from blitzlib import load_blitz, load_canonical, flat

COMP = sys.argv[1]
NPERM = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NA, NB = 470, 159


def hz(a, b, nperm=NPERM, seed=0):
    vocab = {t: i for i, t in enumerate(sorted(set(a) | set(b)))}
    K = len(vocab)
    pool = np.array([vocab[t] for t in list(a) + list(b)])
    na, n = len(a), len(a) + len(b)
    tot = np.bincount(pool, minlength=K).astype(float)
    ea, eb = tot * na / n, tot * (n - na) / n

    def chi2(idx):
        ca = np.bincount(pool[idx[:na]], minlength=K).astype(float)
        cb = tot - ca
        return float(((ca - ea) ** 2 / ea).sum() + ((cb - eb) ** 2 / eb).sum())

    obs = chi2(np.arange(n))
    rng = np.random.default_rng(seed)
    v = np.empty(nperm)
    for p in range(nperm):
        v[p] = chi2(rng.permutation(n))
    m, sd = float(v.mean()), float(v.std(ddof=1))
    return dict(obs=obs, mean=m, sd=sd, z=(obs - m) / sd,
                p_upper=float((int((v >= obs).sum()) + 1) / (nperm + 1)), K=K)


blitz = load_blitz(os.path.join(HERE, "data"))
a, b = flat(blitz["p7"]), flat(blitz["p8"])
assert (len(a), len(b)) == (NA, NB)
bl = hz(a, b, seed=1)
print(f"BLITZ p7 vs p8: chi2={bl['obs']:.1f} (df={bl['K']-1}) null_mean={bl['mean']:.1f} "
      f"sd={bl['sd']:.1f}  z={bl['z']:+.2f}  p={bl['p_upper']:.5f}")
sys.stdout.flush()

res = {"sizes": [NA, NB], "nperm": NPERM, "blitz": bl, "reference": {}}


def block(lines, want, skip=0):
    out = []
    for l in lines:
        out.extend(l)
        if len(out) >= skip + want:
            break
    return out[skip:skip + want] if len(out) >= skip + want else None


for label, doc in (("copiale", load_canonical(os.path.join(COMP, "copiale"))),
                   ("borg", load_canonical(os.path.join(COMP, "borg")))):
    ks = sorted(doc)
    btw, wth = [], []
    for i in range(len(ks) - 1):
        x, y = block(doc[ks[i]], NA), block(doc[ks[i + 1]], NB)
        if x and y:
            btw.append(hz(x, y, seed=100 + i)["z"])
    for i, k in enumerate(ks):
        x, y = block(doc[k], NA), block(doc[k], NB, skip=NA)
        if x and y:
            wth.append(hz(x, y, seed=500 + i)["z"])
    q = lambda v, p: sorted(v)[min(len(v) - 1, int(p * len(v)))]
    res["reference"][label] = dict(
        n_between=len(btw), n_within=len(wth),
        between_z=btw, within_z=wth,
        n_between_ge_blitz=sum(1 for z in btw if z >= bl["z"]),
        n_within_ge_blitz=sum(1 for z in wth if z >= bl["z"]))
    print(f"{label} between-page n={len(btw)}: z p05={q(btw,.05):+.2f} med={q(btw,.5):+.2f} "
          f"p95={q(btw,.95):+.2f} max={max(btw):+.2f}  >=Blitz: "
          f"{res['reference'][label]['n_between_ge_blitz']}/{len(btw)}")
    if wth:
        print(f"{label} within-page  n={len(wth)}: z p05={q(wth,.05):+.2f} med={q(wth,.5):+.2f} "
              f"p95={q(wth,.95):+.2f} max={max(wth):+.2f}  >=Blitz: "
              f"{res['reference'][label]['n_within_ge_blitz']}/{len(wth)}")
    sys.stdout.flush()

json.dump(res, open(os.path.join(HERE, "out", "test1_homogeneity.json"), "w"), indent=1)
print("\nwrote out/test1_homogeneity.json")
