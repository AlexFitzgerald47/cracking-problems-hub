"""Which of the four orthographic rules carries the effect?

Each rule applied alone, then all four, on the identical protocol. Reported on the
two measures that matter: ±10 accuracy with the time gap, and the unconditioned
date-drivenness rho. Manhattan distance throughout, so this isolates orthography from
the distance-measure effect.
"""
import os, re, json
import numpy as np
import shared
from date_drivenness import measure

_RUN = re.compile(r'(.)\1+')
T = 10


def make(uv=False, ij=False, finale=False, doubles=False):
    def key(w):
        w = w.replace("'", '')
        if not w:
            return '_'
        if uv:
            w = w.replace('u', 'v')
        if ij:
            w = w.replace('j', 'i').replace('y', 'i')
        if finale:
            while len(w) > 2 and w.endswith('e'):
                w = w[:-1]
        if doubles:
            w = _RUN.sub(r'\1', w)
        return w or '_'
    return key


def gap_acc(X, y, yr):
    n = len(y); ok = tot = 0
    for i in range(n):
        keep = np.ones(n, bool); keep[i] = False
        keep &= ~(np.abs(yr - yr[i]) <= T)
        if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
            continue
        tot += 1
        ok += shared.attribute(X[keep], y[keep], X[i:i+1])[0] == y[i]
    return ok / tot, tot


def main():
    plays = shared.load()
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])
    variants = [('none (raw)', {}),
                ('u->v only', {'uv': True}),
                ('final -e only', {'finale': True}),
                ('collapse doubles only', {'doubles': True}),
                ('i/j and y->i only', {'ij': True}),
                ('u->v + final -e', {'uv': True, 'finale': True}),
                ('all four (NORM)', {'uv': True, 'ij': True, 'finale': True, 'doubles': True})]
    out = []
    for name, kw in variants:
        k = make(**kw)
        for p in plays:
            p['k'] = [k(w) for w in p['words']]
        vocab = shared.vocabulary(plays, words_key='k')
        X = shared.vectors(plays, vocab, words_key='k')
        acc, n = gap_acc(X, y, yr)
        dd = measure(X, y, yr, 'manhattan')
        out.append({'rule': name, 'gap10_accuracy': acc, 'n_tested': n,
                    'date_drivenness_rho': dd['mean_spearman_distance_vs_dateproximity'],
                    'rho_se': dd['se']})
        print('%-24s ±10 accuracy %.3f    date-drivenness rho %+.3f ± %.3f'
              % (name, acc, out[-1]['date_drivenness_rho'], out[-1]['rho_se']), flush=True)
    json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', 'results',
                                     'rule_decomposition.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
