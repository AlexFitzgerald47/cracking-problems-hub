"""Does the best-known claimed monoalphabetic solution have any special status?

Scores the published ShadowWolf387/DorabellaCipher key, then runs a large
multi-restart search over the same reading and counts how many *distinct*
keys reach or beat it. If many do, and their plaintexts disagree with each
other, then reaching that score is not evidence of having found the message.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, solver, dorabella as D

SEED = 20260904 + 3
RESTARTS = 4000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'claimed_results.json')
# cipher letter A..Z -> plaintext, read off Texts/solkey.txt + Solution.txt in
# the public repo ShadowWolf387/DorabellaCipher (verified: it reproduces that
# repo's published plaintext exactly from the Williams reading).
CLAIMED_KEY = 'PSTYEHKWBARIGMXJFVOLDUNCZQ'


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    model = lang.load()
    quad = model['quad']
    w = next(t for t in D.load()['transcriptions'] if t['label'] == 'Williams')['text']

    claimed_pt = ''.join(CLAIMED_KEY[ord(c) - 65] for c in w)
    arr = np.array([ord(c) - 65 for c in claimed_pt])
    claimed_score = solver.per_quadgram(solver.score(arr, np.arange(26), quad), 87)

    ti, k = solver.encode(w)
    found = {}
    for _ in range(RESTARTS):
        tot, key = solver.hill_climb(ti, quad, k, rng, restarts=1)
        pt = solver.decrypt(ti, key)
        s = solver.per_quadgram(tot, 87)
        if pt not in found or s > found[pt]:
            found[pt] = s
    ranked = sorted(found.items(), key=lambda kv: -kv[1])
    at_or_above = [(p, s) for p, s in ranked if s >= claimed_score]

    res = {
        'seed': SEED, 'restarts': RESTARTS,
        'claimed_key': CLAIMED_KEY,
        'claimed_plaintext': claimed_pt.lower(),
        'claimed_score': claimed_score,
        'n_distinct_optima_found': len(ranked),
        'n_distinct_optima_at_or_above_claimed': len(at_or_above),
        'top_20': [{'score': s, 'plaintext': p} for p, s in ranked[:20]],
        'at_or_above_claimed': [{'score': s, 'plaintext': p} for p, s in at_or_above],
        'runtime_seconds': time.time() - t0,
    }
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('claimed score %.4f' % claimed_score)
    print('distinct local optima found: %d' % len(ranked))
    print('distinct keys scoring >= the claimed solution: %d' % len(at_or_above))
    for p, s in ranked[:12]:
        mark = '>=' if s >= claimed_score else '  '
        print(' %s %.4f  %s' % (mark, s, p))
    print('runtime %.1fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
