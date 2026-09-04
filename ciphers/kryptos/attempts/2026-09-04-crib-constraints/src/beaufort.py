"""Beaufort variant of the shift test.

crib_constraints.py tests Vigenere (key = C - P). Beaufort uses key = C + P, a
different invariant, so it needs its own pass before the Vigenere *family* can
be claimed as eliminated.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import k4

SEED = 20260904 + 7
N_NULL = 20000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'beaufort_results.json')


def conflicts(ct, known, p):
    ks = collections.defaultdict(set)
    for i, pt in known.items():
        ks[i % p].add((ord(ct[i]) + ord(pt)) % 26)
    return sum(len(v) - 1 for v in ks.values())


def main():
    rng = np.random.default_rng(SEED)
    d = k4.load()
    ct, known = d['ciphertext'], d['known']
    letters = np.array([ord(c) - 65 for c in ct])
    freq = np.bincount(letters, minlength=26) / len(letters)
    idx = sorted(known)
    nullpass = collections.defaultdict(int)
    for _ in range(N_NULL):
        draw = rng.choice(26, size=len(idx), p=freq)
        fake = list(ct)
        for j, i in enumerate(idx):
            fake[i] = chr(65 + draw[j])
        fake = ''.join(fake)
        for p in range(1, 98):
            if conflicts(fake, known, p) == 0:
                nullpass[p] += 1
    rows = [{'period': p, 'conflicts': conflicts(ct, known, p),
             'survives': conflicts(ct, known, p) == 0,
             'null_rate': nullpass[p] / N_NULL} for p in range(1, 98)]
    powered = [r for r in rows if r['null_rate'] < 0.10]
    out = {'seed': SEED, 'n_null': N_NULL, 'rows': rows,
           'surviving': [r['period'] for r in rows if r['survives']],
           'powered_periods': [r['period'] for r in powered],
           'powered_survivors': [r['period'] for r in powered if r['survives']],
           'expected_powered_survivors_under_null': sum(r['null_rate'] for r in powered)}
    with open(OUT, 'w') as fh:
        json.dump(out, fh, indent=1)
    print('powered periods %d; survivors %s (expected under null %.2f)'
          % (len(powered), out['powered_survivors'],
             out['expected_powered_survivors_under_null']))


if __name__ == '__main__':
    main()
