"""Can cross-period attribution be made period-invariant?

The honest target is not the full-data baseline. It is the size-matched random
ablation: the accuracy the same method reaches with the same amount of training data
removed at random in time. chronology_effect = acc(time gap) - acc(random ablation).
Driving that to zero is what "period-invariant" means.

Grid: feature vocabulary (raw / orthographic key) x feature restriction (top 500 /
ubiquitous words only) x distance (Manhattan on z = Burrows's Delta / cosine on z =
Cosine Delta, Evert et al. 2017).
"""
import os, json, time, itertools, collections
import numpy as np
import shared, ortho

GAPS = (5, 10, 20)
REPS = 8
SEED = 20260908
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'grid.json')


def zsc(Xtr, Xte):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1
    return (Xtr - mu) / sd, (Xte - mu) / sd


def att_manhattan(Xtr, ytr, Xte):
    Ztr, Zte = zsc(Xtr, Xte)
    a = sorted(set(ytr))
    c = np.stack([Ztr[ytr == k].mean(0) for k in a])
    return a[int(np.abs(Zte[0] - c).sum(1).argmin())]


def att_cosine(Xtr, ytr, Xte):
    Ztr, Zte = zsc(Xtr, Xte)
    a = sorted(set(ytr))
    c = np.stack([Ztr[ytr == k].mean(0) for k in a])
    cn = c / np.maximum(np.linalg.norm(c, axis=1, keepdims=True), 1e-12)
    v = Zte[0] / max(np.linalg.norm(Zte[0]), 1e-12)
    return a[int((cn @ v).argmax())]


def evaluate(X, y, yr, att, gaps=GAPS, reps=REPS):
    n = len(y)
    authors = sorted(set(y))
    idx_of = {a: np.where(y == a)[0] for a in authors}
    rng = np.random.default_rng(SEED)
    rows = []
    for T in gaps:
        tested = gap_ok = full_ok = 0
        rand_ok = np.zeros(reps)
        for i in range(n):
            keep = np.ones(n, bool); keep[i] = False
            keep &= ~(np.abs(yr - yr[i]) <= T)
            if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
                continue
            tested += 1
            full = np.ones(n, bool); full[i] = False
            gap_ok += att(X[keep], y[keep], X[i:i+1]) == y[i]
            full_ok += att(X[full], y[full], X[i:i+1]) == y[i]
            want = {a: int(keep[idx_of[a]].sum()) for a in authors}
            for r in range(reps):
                m = np.zeros(n, bool)
                for a in authors:
                    pool = idx_of[a][idx_of[a] != i]
                    k = min(want[a], len(pool))
                    if k:
                        m[rng.permutation(pool)[:k]] = True
                if (y[m] == y[i]).sum() < 1 or len(set(y[m])) < 2:
                    continue
                rand_ok[r] += att(X[m], y[m], X[i:i+1]) == y[i]
        acc_r = rand_ok / tested
        rows.append({'gap_years': T, 'n_tested': tested,
                     'acc_time_gap': gap_ok / tested,
                     'acc_random_ablation': float(acc_r.mean()),
                     'acc_random_ablation_sd': float(acc_r.std(ddof=1)),
                     'acc_full': full_ok / tested,
                     'chronology_effect': gap_ok / tested - float(acc_r.mean())})
    return rows


def main():
    t0 = time.time()
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])

    feats = {}
    for tag, key in (('raw', 'words'), ('norm', 'keys')):
        vocab = shared.vocabulary(plays, words_key=key)
        X = shared.vectors(plays, vocab, words_key=key)
        feats[(tag, 'top500')] = (X, vocab)
        # ubiquitous restriction: present in >=95% of plays, author-blind and date-blind
        pres = (X > 0).mean(0)
        sel = np.where(pres >= 0.95)[0]
        feats[(tag, 'ubiq')] = (X[:, sel], [vocab[j] for j in sel])

    res = {'seed': SEED, 'reps': REPS, 'cells': []}
    for (vtag, rtag), (X, vocab) in feats.items():
        for dtag, att in (('manhattan', att_manhattan), ('cosine', att_cosine)):
            rows = evaluate(X, y, yr, att)
            res['cells'].append({'vocab': vtag, 'restrict': rtag, 'distance': dtag,
                                 'n_features': X.shape[1], 'gaps': rows})
            s = '  '.join('±%d: gap %.3f rand %.3f chron %+.3f'
                          % (r['gap_years'], r['acc_time_gap'],
                             r['acc_random_ablation'], r['chronology_effect'])
                          for r in rows)
            print('%-5s %-6s %-9s k=%-4d %s' % (vtag, rtag, dtag, X.shape[1], s), flush=True)

    res['runtime_seconds'] = time.time() - t0
    json.dump(res, open(OUT, 'w'), indent=1)
    print('\nruntime %.0fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
