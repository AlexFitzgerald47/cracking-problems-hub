"""What would another crib actually buy?

crib_constraints.py measured the cribs' power by Monte Carlo. That measurement
turns out to have an exact structural explanation, verified in
results/crib_value.json: a period p is testable if and only if two crib
positions differing by a multiple of p carry the *same* plaintext letter.
Nothing else matters. With the current cribs, every period having such a pair
shows a null survival rate below 3.5%, and every period without one shows
16.7% or more - a clean separation with no overlap.

That converts "how much would a third crib be worth" from a simulation into a
combinatorial count, which is worth having: it says precisely what to ask for.
"""
import sys, os, json, itertools, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import k4

SEED = 20260904 + 11
N_DRAW = 4000
N = 97
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'crib_value.json')

# Lewand's English letter frequencies; letters are drawn i.i.d. from these.
# Real English repeats letters slightly more than i.i.d. at short distances, so
# this is a mildly conservative estimate of what a crib buys.
LEWAND = dict(zip('ETAOINSHRDLCUMWFGYPBVKJXQZ',
                  [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987,
                   4.253, 4.025, 2.782, 2.758, 2.406, 2.360, 2.228, 2.015, 1.974,
                   1.929, 1.492, 0.978, 0.772, 0.153, 0.150, 0.095, 0.074]))


def powered_periods(letters_by_pos, nmax=N):
    """Periods with at least one same-letter pair inside a residue class."""
    items = sorted(letters_by_pos.items())
    out = set()
    for (i, a), (j, b) in itertools.combinations(items, 2):
        if a == b:
            dgt = j - i
            for p in range(1, nmax + 1):
                if dgt % p == 0:
                    out.add(p)
    return out


def main():
    rng = np.random.default_rng(SEED)
    d = k4.load()
    known = d['known']
    alpha = list(LEWAND)
    probs = np.array([LEWAND[c] for c in alpha], dtype=float)
    probs /= probs.sum()

    base = powered_periods(known)
    res = {'seed': SEED, 'n_draws': N_DRAW,
           'baseline_powered_periods': sorted(base),
           'baseline_count': len(base),
           'structural_rule': ('a period p is testable iff two crib positions '
                               'differing by a multiple of p carry the same '
                               'plaintext letter'),
           'by_length': {}, 'best_placement': {}}

    free = [i for i in range(N) if i not in known]
    for L in (5, 10, 15, 20, 25, 30, 40):
        counts, low30 = [], []
        for _ in range(N_DRAW):
            starts = [x for x in range(N - L + 1)]
            x = int(rng.choice(starts))
            letters = dict(known)
            for k in range(L):
                letters[x + k] = alpha[int(rng.choice(len(alpha), p=probs))]
            pw = powered_periods(letters)
            counts.append(len(pw))
            low30.append(len([p for p in pw if p <= 30]))
        res['by_length'][str(L)] = {
            'mean_powered_periods': float(np.mean(counts)),
            'mean_powered_periods_up_to_30': float(np.mean(low30)),
            'p10': float(np.percentile(counts, 10)),
            'p90': float(np.percentile(counts, 90)),
        }

    # best fixed placement for a crib of length 12, averaged over letter draws
    L = 12
    best = []
    for x in range(N - L + 1):
        c = []
        for _ in range(300):
            letters = dict(known)
            for k in range(L):
                letters[x + k] = alpha[int(rng.choice(len(alpha), p=probs))]
            c.append(len([p for p in powered_periods(letters) if p <= 30]))
        best.append((x + 1, float(np.mean(c))))
    best.sort(key=lambda t: -t[1])
    res['best_placement'] = {'crib_length': L, 'metric': 'mean powered periods <= 30',
                             'top': best[:8], 'worst': best[-4:]}

    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('baseline: %d powered periods -> %s' % (len(base), sorted(base)))
    print('          of which <= 30: %s' % sorted(p for p in base if p <= 30))
    print()
    print('extra crib   mean powered periods   mean powered <= 30   (10th-90th pct)')
    for L, v in res['by_length'].items():
        print('  L=%-3s          %5.1f                 %5.1f            (%.0f-%.0f)'
              % (L, v['mean_powered_periods'], v['mean_powered_periods_up_to_30'],
                 v['p10'], v['p90']))
    print()
    print('best placement for a 12-character crib (1-based start, mean powered periods <=30):')
    for x, m in res['best_placement']['top']:
        print('   start %2d -> %.2f' % (x, m))
    print('worst:', [(x, round(m, 2)) for x, m in res['best_placement']['worst']])


if __name__ == '__main__':
    main()
