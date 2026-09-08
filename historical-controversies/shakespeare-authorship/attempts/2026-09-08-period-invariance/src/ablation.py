"""Size-matched random ablation: the control that separates chronological distance
from author-specific data loss.

For each test play i and gap T, the time gap removes some number of plays from each
author. This removes the *same number from each author*, chosen at random in time.
If the accuracy is the same, the gap was measuring data loss, not chronology.
"""
import os, sys, json, time
import numpy as np
import shared, ortho

GAPS = (0, 5, 10, 20, 30)
REPS = 12
SEED = 20260908
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'ablation.json')


def features(plays, norm):
    key = 'keys' if norm else 'words'
    if norm:
        for p in plays:
            if 'keys' not in p:
                p['keys'] = [ortho.key(w) for w in p['words']]
    vocab = shared.vocabulary(plays, words_key=key)
    return shared.vectors(plays, vocab, words_key=key)


def main():
    t0 = time.time()
    plays = shared.load()
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    n = len(plays)
    authors = sorted(set(y))
    idx_of = {a: np.where(y == a)[0] for a in authors}
    rng = np.random.default_rng(SEED)

    res = {'seed': SEED, 'reps': REPS, 'n_plays': n, 'conditions': {}}

    for norm in (False, True):
        X = features(plays, norm)
        tag = 'NORM' if norm else 'RAW'
        rows = []
        for T in GAPS:
            tested = gap_ok = full_ok = 0
            rand_ok = np.zeros(REPS)
            own_gap = []
            for i in range(n):
                keep = np.ones(n, bool); keep[i] = False
                keep &= ~(np.abs(yr - yr[i]) <= T)
                if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
                    continue
                tested += 1
                own_gap.append((y[keep] == y[i]).sum())
                full = np.ones(n, bool); full[i] = False
                gap_ok += shared.attribute(X[keep], y[keep], X[i:i+1])[0] == y[i]
                full_ok += shared.attribute(X[full], y[full], X[i:i+1])[0] == y[i]
                # per-author removal counts imposed by the time gap
                want = {a: int(keep[idx_of[a]].sum()) for a in authors}
                for r in range(REPS):
                    m = np.zeros(n, bool)
                    for a in authors:
                        pool = idx_of[a][idx_of[a] != i]
                        k = min(want[a], len(pool))
                        if k:
                            m[rng.permutation(pool)[:k]] = True
                    if (y[m] == y[i]).sum() < 1 or len(set(y[m])) < 2:
                        rand_ok[r] += gap_ok and 0  # unattributable, count as miss
                        continue
                    rand_ok[r] += shared.attribute(X[m], y[m], X[i:i+1])[0] == y[i]
            accs = rand_ok / tested
            rows.append({'gap_years': T, 'n_tested': tested,
                         'mean_own_author_train': float(np.mean(own_gap)),
                         'accuracy_time_gap': gap_ok / tested,
                         'accuracy_full': full_ok / tested,
                         'accuracy_random_ablation_mean': float(accs.mean()),
                         'accuracy_random_ablation_sd': float(accs.std(ddof=1)),
                         'accuracy_random_ablation_min': float(accs.min()),
                         'accuracy_random_ablation_max': float(accs.max()),
                         'chronology_effect': gap_ok / tested - float(accs.mean()),
                         'data_loss_effect': float(accs.mean()) - full_ok / tested})
            print('%s ±%-3d  time %.3f  random %.3f±%.3f  full %.3f   (n=%d, own=%.2f)'
                  % (tag, T, rows[-1]['accuracy_time_gap'],
                     rows[-1]['accuracy_random_ablation_mean'],
                     rows[-1]['accuracy_random_ablation_sd'],
                     rows[-1]['accuracy_full'], tested,
                     rows[-1]['mean_own_author_train']), flush=True)
        res['conditions'][tag] = rows

    res['runtime_seconds'] = time.time() - t0
    json.dump(res, open(OUT, 'w'), indent=1)
    print('\nruntime %.0fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
