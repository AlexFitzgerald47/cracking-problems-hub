"""Transposition composed with a periodic polyalphabetic cipher.

Sanborn's K3 was a transposition and he has hinted at 'masking'. So the obvious
untested family is a composite: the plaintext is enciphered by some periodic
polyalphabetic cipher, and the result is then transposed.

    ct = T(m),  m = periodic_poly(pt)

The useful structure here is that the polyalphabetic stage preserves position,
so `m` aligns positionally with the plaintext. That means for any candidate
transposition T we can undo it, m = T^-1(ct), and run exactly the same crib
tests on m at exactly the same crib positions.

Two consequences. First, the search is cheap: one permutation per candidate.
Second - and this is what makes it rigorous - the null distribution does not
change. The null survival rate per period depends only on the crib *positions*
and on the letter distribution, and T is a permutation, so it preserves the
multiset. The null rates already computed in crib_results.json and
beaufort_results.json apply unchanged, and no new Monte Carlo is needed.

With thousands of (T, period) hypotheses tested, the expected number of chance
survivors is what matters, so it is computed and reported alongside.
"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(__file__))
import k4
import crib_constraints as cc
import beaufort as bf

R = os.path.join(os.path.dirname(__file__), '..', 'results')
OUT = os.path.join(R, 'composite_results.json')
N = 97


def columnar(n, w):
    """Positions read out of a w-column grid, column by column."""
    order = []
    nrows = (n + w - 1) // w
    for c in range(w):
        for r in range(nrows):
            i = r * w + c
            if i < n:
                order.append(i)
    return order


def railfence(n, rails):
    rows = [[] for _ in range(rails)]
    r, d = 0, 1
    for i in range(n):
        rows[r].append(i)
        if r == 0:
            d = 1
        elif r == rails - 1:
            d = -1
        r += d
    return [i for row in rows for i in row]


def candidates():
    out = [('identity', list(range(N)))]
    for w in range(2, 49):
        out.append(('columnar_w%d' % w, columnar(N, w)))
    for r in range(2, 21):
        out.append(('railfence_r%d' % r, railfence(N, r)))
    return out


def apply_perm(s, order, inverse):
    """order[k] = source index for output k. inverse undoes that."""
    if not inverse:
        return ''.join(s[i] for i in order)
    out = [None] * len(s)
    for k, i in enumerate(order):
        out[i] = s[k]
    return ''.join(out)


def main():
    d = k4.load()
    ct, known = d['ciphertext'], d['known']
    gen_null = {r['period']: r['null_survival_rate_general']
                for r in json.load(open(os.path.join(R, 'crib_results.json')))['periods']}
    vig_null = {r['period']: r['null_survival_rate_vigenere']
                for r in json.load(open(os.path.join(R, 'crib_results.json')))['periods']}
    bf_null = {r['period']: r['null_rate']
               for r in json.load(open(os.path.join(R, 'beaufort_results.json')))['rows']}

    survivors, n_tested = [], 0
    exp_gen = exp_vig = exp_bf = 0.0          # over powered tests only
    n_pow = {'general': 0, 'vigenere': 0, 'beaufort': 0}
    obs = {'general': 0, 'vigenere': 0, 'beaufort': 0}
    powered_tested = 0
    for name, order in candidates():
        for inverse in (False, True):
            if name == 'identity' and inverse:
                continue
            m = apply_perm(ct, order, inverse)
            tag = name + ('_inv' if inverse else '')
            for p in range(1, N + 1):
                n_tested += 1
                if gen_null[p] < 0.10:
                    exp_gen += gen_null[p]; n_pow['general'] += 1
                if vig_null[p] < 0.10:
                    exp_vig += vig_null[p]; n_pow['vigenere'] += 1
                if bf_null[p] < 0.10:
                    exp_bf += bf_null[p]; n_pow['beaufort'] += 1
                powered = (gen_null[p] < 0.10) or (vig_null[p] < 0.10) or (bf_null[p] < 0.10)
                if powered:
                    powered_tested += 1
                c, mg, pairs = cc.violations(m, known, p)
                v = cc.vigenere_violations(m, known, p)
                b = bf.conflicts(m, known, p)
                if c + mg == 0 and gen_null[p] < 0.10: obs['general'] += 1
                if v == 0 and vig_null[p] < 0.10: obs['vigenere'] += 1
                if b == 0 and bf_null[p] < 0.10: obs['beaufort'] += 1
                hit = {'transposition': tag, 'period': p,
                       'general': c + mg == 0, 'vigenere': v == 0, 'beaufort': b == 0,
                       'null_general': gen_null[p], 'null_vigenere': vig_null[p],
                       'null_beaufort': bf_null[p], 'testable_pairs': pairs}
                # only record survivors of a test that actually had power
                if ((hit['general'] and gen_null[p] < 0.10)
                        or (hit['vigenere'] and vig_null[p] < 0.10)
                        or (hit['beaufort'] and bf_null[p] < 0.10)):
                    survivors.append(hit)

    res = {'n_transpositions': len(candidates()) * 2 - 1,
           'n_hypotheses_tested': n_tested,
           'n_powered_hypotheses': powered_tested,
           'powered_tests_per_family': n_pow,
           'observed_powered_survivors_per_family': obs,
           'expected_chance_survivors_among_powered': {
               'general': exp_gen, 'vigenere': exp_vig, 'beaufort': exp_bf},
           'powered_survivors': survivors,
           'n_powered_survivors': len(survivors)}

    by_t = collections.Counter(s['transposition'] for s in survivors)
    res['powered_survivors_by_transposition'] = dict(by_t)
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('transpositions tried: %d (identity, columnar w=2..48, rail fence r=2..20, each direction)'
          % res['n_transpositions'])
    print('(transposition, period) hypotheses tested: %d' % n_tested)
    print('of those, powered by at least one test: %d' % powered_tested)
    print()
    print('%-10s %8s %10s %10s' % ('family', 'powered', 'survived', 'expected'))
    for f, e in (('general', exp_gen), ('vigenere', exp_vig), ('beaufort', exp_bf)):
        print('%-10s %8d %10d %10.1f' % (f, n_pow[f], obs[f], e))
    print()
    for s in sorted(survivors, key=lambda s: min(s['null_general'], s['null_vigenere'], s['null_beaufort']))[:25]:
        fams = [f for f in ('general', 'vigenere', 'beaufort') if s[f]]
        print('  %-18s p=%-3d  survives %-28s min null %.3f  pairs %d'
              % (s['transposition'], s['period'], ','.join(fams),
                 min(s['null_general'] if s['general'] else 1,
                     s['null_vigenere'] if s['vigenere'] else 1,
                     s['null_beaufort'] if s['beaufort'] else 1), s['testable_pairs']))


if __name__ == '__main__':
    main()
