"""How much can a quadgram hill climber actually prove at 87 characters?

For genuine English enciphered with a known random key we can ask the question
nobody asks of a claimed Dorabella solution: does the highest-scoring key equal
the key that was actually used? If it frequently does not, then "my search
found a high-scoring readable key" is not evidence of a solution, and the
Dorabella literature's standard of proof is unattainable at this length.
"""
import sys, os, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, solver, dorabella as D

SEED = 20260904
N_CONTROLS = 150
N_SHUFFLES = 150
RESTARTS = 200
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'power_results.json')


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED + 1)
    model = lang.load()
    quad = model['quad']
    n = 87
    ident = np.arange(26)

    eng = lang.sample_english(model, n, N_CONTROLS, rng)
    rows = []
    for arr in eng:
        # encipher with a known random key; hill climb; compare to ground truth
        true_key = rng.permutation(26)
        ct = true_key[arr]
        ti, k = solver.encode(''.join(chr(ord('A') + c) for c in ct))
        tot, key = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
        rec = solver.decrypt(ti, key)
        truth = ''.join(chr(ord('a') + c) for c in arr)
        rows.append({
            'true_score': solver.per_quadgram(solver.score(arr, ident, quad), n),
            'best_score': solver.per_quadgram(tot, n),
            'char_accuracy': float(np.mean([a == b for a, b in zip(rec, truth)])),
            'exact': rec == truth,
        })

    dora = next(t for t in D.load()['transcriptions'] if t['label'] == 'Williams')['text']
    base = np.frombuffer(dora.encode(), dtype=np.uint8).copy()
    shuf = []
    for _ in range(N_SHUFFLES):
        rng.shuffle(base)
        ti, k = solver.encode(base.tobytes().decode())
        tot, _ = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
        shuf.append(solver.per_quadgram(tot, n))

    ti, k = solver.encode(dora)
    tot, key = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
    dora_score = solver.per_quadgram(tot, n)
    dora_pt = solver.decrypt(ti, key)

    best = np.array([r['best_score'] for r in rows])
    true = np.array([r['true_score'] for r in rows])
    acc = np.array([r['char_accuracy'] for r in rows])
    sh = np.array(shuf)

    res = {
        'seed': SEED + 1, 'restarts': RESTARTS, 'n_controls': N_CONTROLS,
        'n_shuffles': N_SHUFFLES,
        'recovery': {
            'exact_key_recovered': float(np.mean([r['exact'] for r in rows])),
            'char_accuracy_mean': float(acc.mean()),
            'char_accuracy_median': float(np.median(acc)),
            'frac_accuracy_above_90pct': float((acc > 0.9).mean()),
            'frac_accuracy_below_50pct': float((acc < 0.5).mean()),
            'frac_best_beats_truth': float((best > true).mean()),
            'mean_score_gap_best_minus_true': float((best - true).mean()),
        },
        'distributions': {
            'english_best': {'mean': float(best.mean()), 'sd': float(best.std(ddof=1)),
                             'p2.5': float(np.percentile(best, 2.5)),
                             'p5': float(np.percentile(best, 5)),
                             'p50': float(np.percentile(best, 50))},
            'shuffle_best': {'mean': float(sh.mean()), 'sd': float(sh.std(ddof=1)),
                             'p50': float(np.percentile(sh, 50)),
                             'p95': float(np.percentile(sh, 95)),
                             'p99': float(np.percentile(sh, 99)),
                             'max': float(sh.max())},
        },
        'test_power': {
            'threshold_shuffle_p95': float(np.percentile(sh, 95)),
            'power_at_5pct_fpr': float((best > np.percentile(sh, 95)).mean()),
            'threshold_shuffle_max': float(sh.max()),
            'power_at_shuffle_max': float((best > sh.max()).mean()),
        },
        'dorabella': {
            'best_score': dora_score,
            'best_plaintext': dora_pt,
            'p_value_vs_shuffles': float((sh >= dora_score).mean()),
            'pct_english_below': float((best < dora_score).mean()),
        },
        'english_best_scores': best.tolist(),
        'english_true_scores': true.tolist(),
        'english_char_accuracy': acc.tolist(),
        'shuffle_best_scores': sh.tolist(),
        'runtime_seconds': time.time() - t0,
    }
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    print('wrote', OUT, 'in %.1fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
