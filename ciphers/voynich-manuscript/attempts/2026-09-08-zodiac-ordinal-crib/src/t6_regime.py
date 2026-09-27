#!/usr/bin/env python3
"""T6: does the zodiac LABEL code shift along the astronomical order, and does the
surrounding ring text shift with it?

Order of the twelve zodiac diagrams is derived internally, not assumed: the four
15-label diagrams must be contiguous (Aries x2, Taurus x2, between Pisces 29 and
Gemini 29), which forces the verso-panel reversal on f70 and f72.
"""
import sys, os, math, random, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import labels as L

ORDER = ['f70v2', 'f70v1', 'f71r', 'f71v', 'f72r1', 'f72r2',
         'f72r3', 'f72v3', 'f72v2', 'f72v1', 'f73r', 'f73v']
SIGN = ['Pisces', 'Aries-1', 'Aries-2', 'Taurus-1', 'Taurus-2', 'Gemini',
        'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius']


def rankdata(v):
    s = sorted(range(len(v)), key=lambda i: v[i])
    r = [0.0] * len(v)
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[s[j + 1]] == v[s[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            r[s[k]] = avg
        i = j + 1
    return r


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def spearman(a, b):
    return pearson(rankdata(a), rankdata(b))


def perm_p(x, y, stat=spearman, nperm=100000, seed=1):
    obs = stat(x, y)
    rng = random.Random(seed)
    yy = list(y)
    cnt = 0
    for _ in range(nperm):
        rng.shuffle(yy)
        if abs(stat(x, yy)) >= abs(obs) - 1e-12:
            cnt += 1
    return obs, (cnt + 1) / (nperm + 1)


def collect(rows):
    z = L.ring_strings(rows)
    lab = {f: [w for (ff, r), v in z.items() if ff == f for w in v] for f in ORDER}
    ring = {}
    for r in rows:
        if r['folio'] in ORDER and r['ltype'] == 'R':
            ring.setdefault(r['folio'], []).extend(r['words'])
    return lab, ring


def feat(ws):
    s = ''.join(ws)
    n = max(len(s), 1)
    a, e = s.count('a'), s.count('e')
    return {
        'a_rate': a / n, 'e_rate': e / n,
        'a_over_ae': a / (a + e) if a + e else float('nan'),
        'eo_rate': s.count('eo') / n,
        'ee_rate': s.count('ee') / n,
        'chars': len(s), 'tokens': len(ws),
    }


def main():
    rows = L.load()
    lab, ring = collect(rows)
    idx = list(range(1, 13))

    print("== per-diagram feature profiles, in derived astronomical order ==")
    print(f"{'i':>2s} {'sign':13s} {'nlab':>4s} {'lab a/(a+e)':>11s} {'lab eo':>7s} "
          f"{'nring':>5s} {'ring a/(a+e)':>12s} {'ring eo':>8s}")
    labr, ringr, labeo, ringeo = [], [], [], []
    for i, f in enumerate(ORDER):
        A, B = feat(lab[f]), feat(ring[f])
        labr.append(A['a_over_ae']); ringr.append(B['a_over_ae'])
        labeo.append(A['eo_rate']); ringeo.append(B['eo_rate'])
        print(f"{i+1:2d} {SIGN[i]:13s} {A['tokens']:4d} {A['a_over_ae']:11.3f} {A['eo_rate']:7.4f} "
              f"{B['tokens']:5d} {B['a_over_ae']:12.3f} {B['eo_rate']:8.4f}")

    print("\n== T6a: monotone trend along the zodiac order (permutation of diagram order) ==")
    for name, series in (("LABELS a/(a+e)", labr), ("RING TEXT a/(a+e)", ringr),
                         ("LABELS eo-rate", labeo), ("RING TEXT eo-rate", ringeo)):
        rho, p = perm_p(idx, series, nperm=200000, seed=7)
        print(f"  {name:20s} Spearman rho = {rho:+.3f}   perm p = {p:.5f}")

    print("\n== T6b: paired label-vs-ring difference (same page, same scribe) ==")
    d = [labr[i] - ringr[i] for i in range(12)]
    rho, p = perm_p(idx, d, nperm=200000, seed=11)
    print(f"  difference series  Spearman rho = {rho:+.3f}   perm p = {p:.5f}")
    print(f"  early(1-7) mean diff = {sum(d[:7])/7:+.3f}   late(8-12) mean diff = {sum(d[7:])/5:+.3f}")

    json.dump({'order': ORDER, 'sign': SIGN, 'lab_a_over_ae': labr,
               'ring_a_over_ae': ringr, 'lab_eo': labeo, 'ring_eo': ringeo},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..',
                                'results', 't6_regime.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
