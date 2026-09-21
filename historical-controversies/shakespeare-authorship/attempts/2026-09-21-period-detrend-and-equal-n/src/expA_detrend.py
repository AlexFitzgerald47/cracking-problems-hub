"""Experiment A — is the register gap the period confound wearing a different hat?

This folder has measured two confounds on Burrows's Delta and never asked whether
they are one thing. 2026-09-05: withholding an author's own work from within
+/-10 years of the questioned play drops leave-one-out accuracy 0.824 -> 0.475.
2026-09-17: an author's own non-dramatic writing sits 22.60 Delta further from his
plays than a different dramatist's plays do.

Both could be the same effect. Non-dramatic pamphlets are not distributed over
time the way plays are - Heywood's prose is thirty years later than his plays,
Lyly's is ten years earlier - so a "register" gap could be a date gap with a
literary name.

Two independent ways of holding period constant, because they fail differently:

  1. DETREND. Fit a polynomial in year to each word frequency on a reference set,
     subtract it, and redo everything on the residuals. Assumes the period effect
     has that functional form, and removes it globally.
  2. YEAR-MATCHED PAIRING. Never compare two documents more than W years apart.
     Assumes nothing about form, but throws away most pairs and can only speak
     about the pairs that survive.

If the margin survives both, register and period are separate problems and the
method is in worse trouble than either result alone implies.

A4 is the control that makes A1 and A3 mean anything: a detrend aggressive enough
to flatten the register gap by flattening *all* authorial signal has explained
nothing. Within-register attribution must survive.
"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
import delta as D

WINDOWS = [5, 10, 20]


def cells(Z, docs, window=None, min_pairs=1):
    """Mean Delta in the four register x author cells.

    Same-work pairs are always excluded (two chunks of one play share plot and
    character names). `window` additionally restricts to pairs whose years differ
    by at most that many years, which is how period is held constant without a
    model. A document contributes to a cell only if it has at least `min_pairs`
    partners there, so the four cells are not silently computed on different
    document sets.
    """
    n = len(docs)
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    wk = np.array([d['work'] for d in docs])
    yr = np.array([d['yr'] for d in docs], float)
    acc = collections.defaultdict(list)
    contributors = collections.defaultdict(set)
    for i in range(n):
        d = np.abs(Z[i] - Z).sum(1)
        ok = (wk != wk[i])
        if window is not None:
            ok = ok & (np.abs(yr - yr[i]) <= window)
        sa, da = (au == au[i]) & ok, (au != au[i]) & ok
        cr, sr = (rg != rg[i]), (rg == rg[i])
        for name, m in (('same_author_same_register', sa & sr),
                        ('same_author_cross_register', sa & cr),
                        ('diff_author_same_register', da & sr),
                        ('diff_author_cross_register', da & cr)):
            if m.sum() >= min_pairs:
                acc[name].append(d[m].mean())
                contributors[name].add(au[i])
    return {k: {'mean': float(np.mean(v)), 'median': float(np.median(v)),
                'n_docs': len(v), 'n_authors': len(contributors[k])}
            for k, v in acc.items()}


def margin(c):
    if 'same_author_cross_register' not in c or 'diff_author_same_register' not in c:
        return None
    return c['same_author_cross_register']['mean'] - c['diff_author_same_register']['mean']


def attribute(Ztr, ytr, Zte, yte, authors):
    cent = np.stack([Ztr[ytr == a].mean(0) for a in authors])
    pred = [authors[i] for i in np.abs(Zte[:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
    per = {}
    for a in authors:
        m = yte == a
        per[a] = float(np.mean([p == a for p, k in zip(pred, m) if k])) if m.any() else None
    return {'micro': float(np.mean([p == t for p, t in zip(pred, yte)])),
            'macro': float(np.mean([v for v in per.values() if v is not None])),
            'per_author': per,
            'share': {a: float(np.mean([p == a for p in pred])) for a in authors}}


def within_register_loo(Z, docs, authors):
    """Leave-one-WORK-out attribution inside drama. The positive control (A4)."""
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    wk = np.array([d['work'] for d in docs])
    Zd, ad, wd = Z[rg == 'drama'], au[rg == 'drama'], wk[rg == 'drama']
    preds, truth = [], []
    for w in sorted(set(wd)):
        te = wd == w
        tr = ~te
        if len(set(ad[tr])) < len(authors):
            continue
        cent = np.stack([Zd[tr][ad[tr] == a].mean(0) for a in authors])
        p = [authors[i] for i in np.abs(Zd[te][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
        preds += p
        truth += list(ad[te])
    per = {}
    for a in authors:
        h = [p == t for p, t in zip(preds, truth) if t == a]
        per[a] = float(np.mean(h)) if h else None
    return {'micro': float(np.mean([p == t for p, t in zip(preds, truth)])),
            'macro': float(np.mean([v for v in per.values() if v is not None])),
            'per_author': per, 'n': len(preds)}


def main():
    docs_full, _ = C.load()                 # every chunk, year or not
    docs_all, dropped = C.load(require_year=True)
    panel = [d for d in docs_all if d['author'] in C.PANEL]
    # Vocabulary is built on the FULL chunk set, exactly as analysis.py does, so
    # the untreated baseline reproduces 2026-09-17 to the printed digit. The ten
    # year-less chunks are one Pix play, outside the 8-author panel; dropping
    # them from the panel changes nothing, but dropping them from the vocabulary
    # would shift the top-500 list and move every number by ~0.3%.
    vocab = D.vocabulary(docs_full)
    X = D.vectors(panel, vocab)
    years = np.array([d['yr'] for d in panel], float)
    rg = np.array([d['register'] for d in panel])
    au = np.array([d['author'] for d in panel])
    drama_mask = rg == 'drama'
    pooled_mask = np.ones(len(panel), bool)

    out = {'n_docs_panel': len(panel), 'dropped_no_year': dropped,
           'n_drama': int(drama_mask.sum()), 'n_nondrama': int((~drama_mask).sum()),
           'year_range': [float(years.min()), float(years.max())],
           'top_k': D.TOP_K}

    treatments = [
        ('baseline_drama_scaled', 0, drama_mask),
        ('detrend_linear_drama_fit', 1, drama_mask),
        ('detrend_quadratic_drama_fit', 2, drama_mask),
        ('detrend_linear_pooled_fit', 1, pooled_mask),
    ]
    for tag, deg, ref in treatments:
        Xt = X if deg == 0 else C.detrend(X, years, ref, degree=deg)
        Z = C.zscale(Xt, ref)
        c = cells(Z, panel)
        cross = attribute(Z[drama_mask], au[drama_mask], Z[~drama_mask], au[~drama_mask], C.PANEL)
        within = within_register_loo(Z, panel, C.PANEL)
        out[tag] = {'cells': c, 'margin': margin(c),
                    'cross_register': {k: v for k, v in cross.items() if k != 'per_author'},
                    'cross_register_per_author': cross['per_author'],
                    'within_register': within}
        print('--- %s' % tag)
        for k in ('same_author_same_register', 'diff_author_same_register',
                  'same_author_cross_register', 'diff_author_cross_register'):
            print('    %-28s %8.2f  (n_docs=%d)' % (k, c[k]['mean'], c[k]['n_docs']))
        print('    MARGIN (same-author-cross minus diff-author-same) %+8.2f' % margin(c))
        print('    cross-register  micro %.3f macro %.3f   |  within-register micro %.3f macro %.3f'
              % (cross['micro'], cross['macro'], within['micro'], within['macro']))
        print()

    # ---- year-matched pairing, on the UNDETRENDED features ----
    Zb = C.zscale(X, drama_mask)
    out['year_matched'] = {}
    print('--- year-matched pairing (undetrended features, drama-scaled)')
    print('    %-6s %10s %10s %10s %10s %10s' %
          ('W', 'saSR', 'daSR', 'saCR', 'daCR', 'MARGIN'))
    for w in WINDOWS + [None]:
        c = cells(Zb, panel, window=w)
        m = margin(c)
        out['year_matched']['W%s' % (w if w is not None else 'inf')] = {
            'cells': c, 'margin': m}
        g = lambda k: ('%10.2f' % c[k]['mean']) if k in c else '%10s' % '-'
        print('    %-6s %s %s %s %s %10s' % (
            w if w is not None else 'all', g('same_author_same_register'),
            g('diff_author_same_register'), g('same_author_cross_register'),
            g('diff_author_cross_register'),
            ('%+.2f' % m) if m is not None else '-'))
        if w is not None:
            print('           n_docs: saSR %d / daSR %d / saCR %d / daCR %d' % tuple(
                c[k]['n_docs'] if k in c else 0 for k in
                ('same_author_same_register', 'diff_author_same_register',
                 'same_author_cross_register', 'diff_author_cross_register')))
            print('           n_authors contributing to saCR: %d of 8' %
                  (c['same_author_cross_register']['n_authors']
                   if 'same_author_cross_register' in c else 0))

    C.save('expA_detrend.json', out)


if __name__ == '__main__':
    main()
