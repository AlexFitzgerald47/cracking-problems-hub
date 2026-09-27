"""Independent falsifier for the date-stamp mechanism.

If what survives the gap is a date stamp, then when Delta gets it wrong under a time
gap it should not err at random: it should prefer an author whose surviving training
plays sit *closer in time* to the questioned play than the true author's do.

Statistic, per erroneous attribution: the mean |year| distance from the questioned play
to the predicted author's training plays, minus the mean of that same quantity taken
over every *other* wrong author available in that fold. Negative = the prediction was
date-biased. The comparison set is all other wrong authors in the same fold, so the
mechanical fact that the gap puts every training play at least T years away cancels.
"""
import os, json
import numpy as np
import shared, ortho

GAPS = (0, 5, 10, 20)
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'error_direction.json')


def run(X, y, yr, authors, idx_of, n, T):
    bias_err, bias_ok, signed_err = [], [], []
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        pred = shared.attribute(X[keep], y[keep], X[i:i+1])[0]
        avail = sorted(set(y[keep]))
        dist = {a: float(np.abs(yr[keep][y[keep] == a] - yr[i]).mean()) for a in avail}
        wrong = [a for a in avail if a != y[i]]
        if not wrong:
            continue
        others = [dist[a] for a in wrong if a != pred]
        if not others:
            continue
        b = dist[pred] - float(np.mean(others))
        if pred == y[i]:
            bias_ok.append(b)
        else:
            bias_err.append(b)
            signed_err.append(float(np.sign(yr[keep][y[keep] == pred].mean() - yr[i])))
    return bias_err, bias_ok, signed_err


def main():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    n = len(plays)
    authors = sorted(set(y))
    idx_of = {a: np.where(y == a)[0] for a in authors}

    res = {}
    for tag, key in (('RAW', 'words'), ('NORM', 'keys')):
        vocab = shared.vocabulary(plays, words_key=key)
        X = shared.vectors(plays, vocab, words_key=key)
        rows = []
        for T in GAPS:
            be, bo, sg = run(X, y, yr, authors, idx_of, n, T)
            # paired bootstrap on the error set
            rng = np.random.default_rng(20260908)
            boot = [np.mean(rng.choice(be, len(be))) for _ in range(4000)] if be else [0]
            rows.append({'gap_years': T, 'n_errors': len(be), 'n_correct': len(bo),
                         'date_bias_errors_years': float(np.mean(be)) if be else None,
                         'date_bias_errors_ci95': [float(np.percentile(boot, 2.5)),
                                                   float(np.percentile(boot, 97.5))],
                         'date_bias_correct_years': float(np.mean(bo)) if bo else None,
                         'frac_errors_more_date_proximate': float(np.mean(np.array(be) < 0)) if be else None})
            r = rows[-1]
            print('%-5s ±%-3d errors=%-4d  date-bias %+.2f yr  CI [%+.2f, %+.2f]  '
                  '%.0f%% of errors date-proximate   (correct: %+.2f yr)'
                  % (tag, T, r['n_errors'], r['date_bias_errors_years'],
                     r['date_bias_errors_ci95'][0], r['date_bias_errors_ci95'][1],
                     100 * r['frac_errors_more_date_proximate'],
                     r['date_bias_correct_years']), flush=True)
        res[tag] = rows
    json.dump(res, open(OUT, 'w'), indent=1)


if __name__ == '__main__':
    main()
