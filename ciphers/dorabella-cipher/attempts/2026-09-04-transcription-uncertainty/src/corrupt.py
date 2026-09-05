"""Could transcription error alone explain Dorabella's score?

Dorabella sits in the gap between the English band and the noise floor. One
innocent explanation is that it *is* an English monoalphabetic cipher, and that
the readings available to us are corrupted enough to drag its score down. This
tests that directly: take genuine English, encipher it, corrupt a fraction q of
the ciphertext symbols the way a misread would, and see where the score lands.

q is bracketed by the observed disagreement between readings: the two closest
distinct transcriptions (Williams and Ernst) differ at 2 of 87 positions
(~2%), while the spread across all three distinct readings is far wider.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, solver, dorabella as D

SEED = 20260904 + 5
RESTARTS = 500      # same budget as matched.py, so the scores are comparable
N = 60
QS = [0.05, 0.10]
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'corrupt_results.json')


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    model = lang.load()
    quad = model['quad']
    eng = lang.sample_english(model, 87, N, rng)

    res = {'seed': SEED, 'restarts': RESTARTS, 'n_each': N, 'by_q': {}}
    for q in QS:
        scores = []
        for arr in eng:
            key = rng.permutation(26)
            ct = key[arr].copy()
            present = np.unique(ct)
            hit = rng.random(87) < q
            ct[hit] = rng.choice(present, size=int(hit.sum()))
            ti, k = solver.encode(''.join(chr(ord('A') + c) for c in ct))
            tot, _ = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
            scores.append(solver.per_quadgram(tot, 87))
        s = np.array(scores)
        res['by_q'][str(q)] = {'mean': float(s.mean()), 'sd': float(s.std(ddof=1)),
                               'p2.5': float(np.percentile(s, 2.5)),
                               'p50': float(np.percentile(s, 50)),
                               'min': float(s.min()), 'scores': scores}
        print('q=%.2f  mean %.4f  sd %.4f  min %.4f' % (q, s.mean(), s.std(ddof=1), s.min()))

    m = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'results',
                                    'matched_results.json')))
    dora = m['readings']['Williams']['score']
    res['dorabella_matched_score'] = dora
    for q, v in res['by_q'].items():
        s = np.array(v['scores'])
        v['pct_below_dorabella'] = float((s < dora).mean())
        print('q=%s: %.1f%% of corrupted English scores at or below Dorabella (%.4f)'
              % (q, 100 * v['pct_below_dorabella'], dora))
    res['runtime_seconds'] = time.time() - t0
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
