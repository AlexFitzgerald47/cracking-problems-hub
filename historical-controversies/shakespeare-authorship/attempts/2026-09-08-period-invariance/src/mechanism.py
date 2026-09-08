"""What the merge actually does, and whether the crude key's bad merges matter.

repair_test.py showed merging makes features far less date-loaded (mean R2 0.323 ->
0.029) but LOWERS raw author F (12.70 -> 6.21). Raw author F is confounded: authors
occupy narrow date windows, so a date-locked spelling scores as an excellent author
discriminator. The test that separates them is author F computed on the *date residual*.

Part 2 rebuilds the key conservatively, refusing the four merges the inspection of
repair_test.json shows are wrong (the/thee/th', us/vs/use, ile/i'le/i'll/ill, done/don),
and reruns the headline. If the effect is an artefact of those merges it dies here.
"""
import os, re, json, collections
import numpy as np
import shared, ortho
from grid import att_cosine, att_manhattan
from date_drivenness import measure

T = 10
BAD = {'th', 'vs', 'il', 'don'}   # keys whose groups the inspection rejects


def resid_F(x, y, yr):
    z = (x - x.mean()) / (x.std() or 1)
    t = (yr - yr.mean()) / yr.std()
    b = (z * t).sum() / (t ** 2).sum()
    r = z - b * t
    a = sorted(set(y)); g = r.mean()
    bet = sum((y == k).sum() * (r[y == k].mean() - g) ** 2 for k in a)
    wit = sum(((r[y == k] - r[y == k].mean()) ** 2).sum() for k in a)
    return (bet / (len(a) - 1)) / max(wit / (len(r) - len(a)), 1e-12)


def gap_acc(X, y, yr, att):
    n = len(y); ok = tot = 0
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        tot += 1
        ok += att(X[keep], y[keep], X[i:i+1]) == y[i]
    return ok / tot, tot


def main():
    plays = shared.load()
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    vr = shared.vocabulary(plays, words_key='words')
    Xr = shared.vectors(plays, vr, words_key='words')

    grp = collections.defaultdict(list)
    for j, w in enumerate(vr):
        grp[ortho.key(w)].append(j)
    groups = {k: g for k, g in grp.items() if len(g) > 1}

    better = []
    for k, g in groups.items():
        m = resid_F(Xr[:, g].sum(1), y, yr)
        c = max(resid_F(Xr[:, j], y, yr) for j in g)
        better.append((m > c, m, c, k))
    print('PART 1 — author F on the DATE RESIDUAL (the unconfounded version)')
    print('  merged beats its best component in %.0f%% of the %d groups'
          % (100 * np.mean([b[0] for b in better]), len(better)))
    print('  mean residualised F: components (max) %.2f -> merged %.2f'
          % (np.mean([b[2] for b in better]), np.mean([b[1] for b in better])))
    print('  (raw, date-confounded F went 12.70 -> 6.21 — the opposite direction)')

    print('\nPART 2 — conservative key, four bad merges refused: %s' % sorted(BAD))

    def conservative(w):
        k = ortho.key(w)
        return w if k in BAD else k
    out = {}
    for tag, fn in (('raw', lambda w: w), ('full key', ortho.key),
                    ('conservative key', conservative)):
        for p in plays:
            p['k'] = [fn(w) for w in p['words']]
        v = shared.vocabulary(plays, words_key='k')
        X = shared.vectors(plays, v, words_key='k')
        am, _ = gap_acc(X, y, yr, att_manhattan)
        ac, n = gap_acc(X, y, yr, att_cosine)
        rho = measure(X, y, yr, 'manhattan')['mean_spearman_distance_vs_dateproximity']
        out[tag] = {'gap10_manhattan': am, 'gap10_cosine': ac, 'rho_manhattan': rho,
                    'n_tested': n}
        print('  %-18s ±10 Manhattan %.3f   ±10 cosine %.3f   rho %+.3f'
              % (tag, am, ac, rho))

    json.dump({'residual_F': {'frac_merged_better': float(np.mean([b[0] for b in better])),
                              'mean_component_max': float(np.mean([b[2] for b in better])),
                              'mean_merged': float(np.mean([b[1] for b in better]))},
               'key_robustness': out},
              open(os.path.join(os.path.dirname(__file__), '..', 'results', 'mechanism.json'), 'w'),
              indent=1)


if __name__ == '__main__':
    main()
