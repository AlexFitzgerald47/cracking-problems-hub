"""Budget-matched comparison.

Hill-climb scores rise with the number of restarts, so Dorabella, genuine
English and pure noise must all be given the *same* search budget before their
scores can be compared. This run gives every text an identical budget.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, solver, dorabella as D

SEED = 20260904 + 4
RESTARTS = 500
N = 100
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'matched_results.json')


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    model = lang.load()
    quad = model['quad']

    def best(s):
        ti, k = solver.encode(s)
        tot, key = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
        return solver.per_quadgram(tot, len(ti)), solver.decrypt(ti, key)

    d = D.load()
    w = next(t for t in d['transcriptions'] if t['label'] == 'Williams')['text']

    eng = lang.sample_english(model, 87, N, rng)
    eng_scores = []
    for arr in eng:
        true_key = rng.permutation(26)
        ct = ''.join(chr(ord('A') + c) for c in true_key[arr])
        eng_scores.append(best(ct)[0])

    base = np.frombuffer(w.encode(), dtype=np.uint8).copy()
    sh_scores = []
    for _ in range(N):
        rng.shuffle(base)
        sh_scores.append(best(base.tobytes().decode())[0])

    targets = {}
    for t in d['transcriptions']:
        if t['n'] == 87:
            sc, pt = best(t['text'])
            targets[t['label']] = {'score': sc, 'plaintext': pt}

    e, sh = np.array(eng_scores), np.array(sh_scores)
    res = {'seed': SEED, 'restarts': RESTARTS, 'n_each': N,
           'english': {'mean': float(e.mean()), 'sd': float(e.std(ddof=1)),
                       'p2.5': float(np.percentile(e, 2.5)), 'p5': float(np.percentile(e, 5)),
                       'p50': float(np.percentile(e, 50)), 'min': float(e.min())},
           'shuffles': {'mean': float(sh.mean()), 'sd': float(sh.std(ddof=1)),
                        'p50': float(np.percentile(sh, 50)), 'p95': float(np.percentile(sh, 95)),
                        'max': float(sh.max())},
           'english_scores': eng_scores, 'shuffle_scores': sh_scores,
           'readings': {}}
    for lab, v in targets.items():
        res['readings'][lab] = {
            **v,
            'pct_english_below': float((e < v['score']).mean()),
            'p_value_vs_shuffles': float((sh >= v['score']).mean()),
        }
    res['runtime_seconds'] = time.time() - t0
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    print('wrote', OUT, 'in %.0fs' % res['runtime_seconds'])
    for lab, v in res['readings'].items():
        print('%-14s %.4f  above %.0f%% of English, p=%.3f vs noise'
              % (lab, v['score'], 100 * v['pct_english_below'], v['p_value_vs_shuffles']))


if __name__ == '__main__':
    main()
