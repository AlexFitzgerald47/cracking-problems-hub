"""The period-gap experiment under five feature conditions.

RAW        the 2026-09-05 feature set, unchanged (replication anchor)
DETREND    per-feature linear regression on year, fit on training plays only,
           residuals used for attribution  (the 2026-09-05 handover's proposal 3)
DROP       the n most date-loaded raw features deleted, date-loading measured on
           training plays only  (matched control: same number of features removed
           as the orthographic merge consumes, but no merging)
NORM       features rebuilt on the orthographic key of ortho.py
NORMDET    NORM plus DETREND

Every condition runs the identical leave-one-play-out protocol and the identical
matched-subset control: for each gap T, accuracy is reported both with the gap and
with no gap on exactly the plays that gap condition could test.
"""
import sys, os, json, time, collections
import numpy as np
import shared, ortho

GAPS = (0, 5, 10, 20, 30)
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'conditions.json')


def build():
    plays = shared.load()
    for p in plays:
        p['keys'] = [ortho.key(w) for w in p['words']]
    return plays


def detrend(Xtr, yrtr, Xte, yrte):
    """Fit feature ~ a + b*year on training plays only; return residuals for both."""
    t = yrtr - yrtr.mean()
    denom = (t ** 2).sum()
    if denom == 0:
        return Xtr, Xte
    a = Xtr.mean(0)
    b = ((Xtr - a) * t[:, None]).sum(0) / denom
    Rtr = Xtr - a - b[None, :] * t[:, None]
    Rte = Xte - a - b[None, :] * (yrte - yrtr.mean())[:, None]
    return Rtr, Rte


def date_loading(Xtr, yrtr):
    Z = (Xtr - Xtr.mean(0)) / np.where(Xtr.std(0) == 0, 1, Xtr.std(0))
    t = (yrtr - yrtr.mean())
    sd = t.std() or 1
    t = t / sd
    beta = (Z * t[:, None]).sum(0) / (t ** 2).sum()
    fit = beta[None, :] * t[:, None]
    ss = (Z ** 2).sum(0)
    ss[ss == 0] = 1
    return 1 - ((Z - fit) ** 2).sum(0) / ss


def run(cond, X, y, yr, ndrop=0):
    """Returns per-gap {n, acc_gap, acc_nogap_same_plays}."""
    n = len(y)
    out = []
    for T in GAPS:
        tested = gap_ok = full_ok = 0
        for i in range(n):
            keep = np.ones(n, bool); keep[i] = False
            keep &= ~(np.abs(yr - yr[i]) <= T)
            if (y[keep] == y[i]).sum() < 1 or len(set(y[keep])) < 2:
                continue
            full = np.ones(n, bool); full[i] = False
            for mask, which in ((keep, 'gap'), (full, 'full')):
                Xtr, Xte = X[mask], X[i:i + 1]
                if cond in ('DETREND', 'NORMDET'):
                    Xtr, Xte = detrend(Xtr, yr[mask], Xte, yr[i:i + 1])
                if cond == 'DROP' and ndrop:
                    r2 = date_loading(X[mask], yr[mask])
                    sel = np.argsort(r2)[:X.shape[1] - ndrop]
                    Xtr, Xte = Xtr[:, sel], Xte[:, sel]
                ok = shared.attribute(Xtr, y[mask], Xte)[0] == y[i]
                if which == 'gap':
                    gap_ok += ok
                else:
                    full_ok += ok
            tested += 1
        out.append({'gap_years': T, 'n_tested': tested,
                    'accuracy_with_gap': gap_ok / tested,
                    'accuracy_same_plays_no_gap': full_ok / tested,
                    'drop': gap_ok / tested - full_ok / tested})
    return out


def main():
    t0 = time.time()
    plays = build()
    y = np.array([p['author'] for p in plays])
    yr = np.array([float(p['year']) for p in plays])

    vocab_raw = shared.vocabulary(plays, words_key='words')
    Xraw = shared.vectors(plays, vocab_raw, words_key='words')
    vocab_key = shared.vocabulary(plays, words_key='keys')
    Xkey = shared.vectors(plays, vocab_key, words_key='keys')

    # how many raw features does the merge consume? -> matched n for DROP
    merged = collections.Counter(ortho.key(w) for w in vocab_raw)
    n_collapsed = sum(c - 1 for c in merged.values() if c > 1)

    res = {'n_plays': len(plays), 'n_authors': len(set(y)),
           'year_range': [int(yr.min()), int(yr.max())],
           'raw_features': len(vocab_raw), 'key_features': len(vocab_key),
           'raw_features_absorbed_by_merge': n_collapsed,
           'merge_groups': {k: [w for w in vocab_raw if ortho.key(w) == k]
                            for k, c in merged.items() if c > 1},
           'mean_r2_date_raw': float(date_loading(Xraw, yr).mean()),
           'mean_r2_date_norm': float(date_loading(Xkey, yr).mean()),
           'conditions': {}}

    for cond, X, nd in (('RAW', Xraw, 0), ('DETREND', Xraw, 0),
                        ('DROP', Xraw, n_collapsed),
                        ('NORM', Xkey, 0), ('NORMDET', Xkey, 0)):
        s = time.time()
        res['conditions'][cond] = run(cond, X, y, yr, ndrop=nd)
        print('%-8s done in %5.0fs' % (cond, time.time() - s), flush=True)

    res['runtime_seconds'] = time.time() - t0
    json.dump(res, open(OUT, 'w'), indent=1)

    print('\nraw features absorbed by the orthographic merge: %d '
          '(%d raw -> %d key features)'
          % (n_collapsed, len(vocab_raw), len(vocab_key)))
    print('mean R2(feature ~ year):  raw %.4f   normalised %.4f'
          % (res['mean_r2_date_raw'], res['mean_r2_date_norm']))
    print('\naccuracy WITH the gap (matched no-gap accuracy in brackets)')
    print('%-9s' % 'gap', ''.join('%-22s' % c for c in res['conditions']))
    for gi, T in enumerate(GAPS):
        row = '±%-8d' % T
        for c in res['conditions']:
            d = res['conditions'][c][gi]
            row += '%-22s' % ('%.3f [%.3f] n=%d' % (d['accuracy_with_gap'],
                                                    d['accuracy_same_plays_no_gap'],
                                                    d['n_tested']))
        print(row)
    print('\nruntime %.0fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
