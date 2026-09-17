"""The register self-match test.

Four distance cells, all on 2,000-word chunks, all in the same units:

    same author,      same register (drama-drama, DIFFERENT plays)
    same author,      cross register (a play chunk vs his own prose/verse)
    different author, same register
    different author, cross register

Plus the attribution experiments those distances predict, a permutation null,
and the per-author self-match that decides P4.

Two scaling choices are reported rather than one, because the answer must not
depend on them:
  primary     z-score on DRAMA chunks only. This is the real scenario: you hold
              a body of plays and ask where a candidate's non-dramatic writing
              falls against them.
  sensitivity z-score on the pooled corpus.

Same-work chunk pairs are never compared: two chunks of one play share topic,
plot and character names, and would make the same-author cell look far better
than authorship warrants.
"""
import sys, os, json, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import delta as D

HERE = os.path.dirname(__file__)
PANEL = ['Chapman, George', 'Dekker, Thomas', 'Greene, Robert', 'Heywood, Thomas',
         'Jonson, Ben', 'Lyly, John', 'Marston, John', 'Middleton, Thomas']
SEED = 20260917


def load():
    docs = json.load(open(os.path.join(HERE, '..', 'data', 'chunks.json')))
    return docs


def scaled(docs, vocab, ref):
    X = D.vectors(docs, vocab)
    R = D.vectors(ref, vocab)
    mu, sd = R.mean(0), R.std(0); sd[sd == 0] = 1
    return (X - mu) / sd


def cells(Z, docs):
    """Mean Delta in each of the four cells, excluding same-work pairs."""
    n = len(docs)
    au = np.array([d['author'] for d in docs])
    rg = np.array([d['register'] for d in docs])
    wk = np.array([d['work'] for d in docs])
    acc = collections.defaultdict(list)
    for i in range(n):
        d = np.abs(Z[i] - Z).sum(1)
        ok = (wk != wk[i])
        sa = (au == au[i]) & ok
        da = (au != au[i]) & ok
        cr = (rg != rg[i])
        sr = (rg == rg[i])
        for name, m in (('same_author_same_register', sa & sr),
                        ('same_author_cross_register', sa & cr),
                        ('diff_author_same_register', da & sr),
                        ('diff_author_cross_register', da & cr)):
            if m.any():
                acc[name].append(d[m].mean())
    return {k: {'mean': float(np.mean(v)), 'median': float(np.median(v)), 'n_docs': len(v)}
            for k, v in acc.items()}


def attribute_by_centroid(Ztrain, ytrain, Ztest, ytest, authors):
    cent = np.stack([Ztrain[ytrain == a].mean(0) for a in authors])
    d = np.abs(Ztest[:, None, :] - cent[None, :, :]).sum(2)
    pred = [authors[i] for i in d.argmin(1)]
    micro = float(np.mean([p == t for p, t in zip(pred, ytest)]))
    per = {}
    for a in authors:
        m = ytest == a
        per[a] = {'n': int(m.sum()),
                  'acc': float(np.mean([p == a for p, k in zip(pred, m) if k])) if m.any() else None}
    macro = float(np.mean([v['acc'] for v in per.values() if v['acc'] is not None]))
    return {'micro': micro, 'macro': macro, 'per_author': per, 'pred': pred}


def main():
    rng = random.Random(SEED)
    docs = load()
    panel = [d for d in docs if d['author'] in PANEL]
    vocab = D.vocabulary(docs)          # register-neutral: pooled corpus
    drama = [d for d in panel if d['register'] == 'drama']
    nond = [d for d in panel if d['register'] == 'nondrama']
    out = {'panel': PANEL, 'n_drama_chunks': len(drama), 'n_nondrama_chunks': len(nond),
           'chance': 1 / len(PANEL), 'top_k': D.TOP_K}

    for tag, ref in (('primary_drama_scaled', drama), ('sensitivity_pooled_scaled', panel)):
        Z = scaled(panel, vocab, ref)
        out[tag] = {'cells': cells(Z, panel)}

        au = np.array([d['author'] for d in panel])
        rg = np.array([d['register'] for d in panel])
        # cross-register: train on all play chunks, test on non-dramatic chunks
        cr = attribute_by_centroid(Z[rg == 'drama'], au[rg == 'drama'],
                                   Z[rg == 'nondrama'], au[rg == 'nondrama'], PANEL)
        cr.pop('pred')
        out[tag]['cross_register_attribution'] = cr
        # reverse direction
        rv = attribute_by_centroid(Z[rg == 'nondrama'], au[rg == 'nondrama'],
                                   Z[rg == 'drama'], au[rg == 'drama'], PANEL)
        rv.pop('pred')
        out[tag]['reverse_attribution'] = rv
        # within-register positive control: leave-one-WORK-out on drama
        wk = np.array([d['work'] for d in panel])
        Zd, ad, wd = Z[rg == 'drama'], au[rg == 'drama'], wk[rg == 'drama']
        preds, truth = [], []
        for w in sorted(set(wd)):
            te = wd == w
            tr = ~te
            if len(set(ad[tr])) < len(PANEL):
                continue
            r = attribute_by_centroid(Zd[tr], ad[tr], Zd[te], ad[te], PANEL)
            preds += r['pred']; truth += list(ad[te])
        per = {}
        for a in PANEL:
            hits = [p == t for p, t in zip(preds, truth) if t == a]
            per[a] = {'n': len(hits), 'acc': float(np.mean(hits)) if hits else None}
        out[tag]['within_register_attribution'] = {
            'micro': float(np.mean([p == t for p, t in zip(preds, truth)])),
            'macro': float(np.mean([v['acc'] for v in per.values() if v['acc'] is not None])),
            'per_author': per}

    # ---- permutation null on the primary scaling ----
    Z = scaled(panel, vocab, drama)
    au = np.array([d['author'] for d in panel])
    rg = np.array([d['register'] for d in panel])
    nd_idx = np.where(rg == 'nondrama')[0]
    works = sorted(set(panel[i]['work'] for i in nd_idx))
    true_owner = {w: next(panel[i]['author'] for i in nd_idx if panel[i]['work'] == w)
                  for w in works}
    nulls = []
    for _ in range(200):
        perm = PANEL[:]; rng.shuffle(perm)
        m = dict(zip(PANEL, perm))
        yfake = np.array([m[true_owner[panel[i]['work']]] for i in nd_idx])
        r = attribute_by_centroid(Z[rg == 'drama'], au[rg == 'drama'],
                                  Z[nd_idx], yfake, PANEL)
        nulls.append(r['macro'])
    out['permutation_null_cross_register'] = {
        'n': len(nulls), 'mean_macro': float(np.mean(nulls)),
        'p95': float(np.percentile(nulls, 95)), 'max': float(np.max(nulls))}

    json.dump(out, open(os.path.join(HERE, '..', 'results', 'analysis.json'), 'w'), indent=1)

    p = out['primary_drama_scaled']
    print('=== distance cells (2,000-word chunks, drama-scaled, same-work pairs excluded)')
    for k in ('same_author_same_register', 'diff_author_same_register',
              'same_author_cross_register', 'diff_author_cross_register'):
        c = p['cells'][k]
        print('  %-28s mean %8.2f  median %8.2f  (n=%d)' % (k, c['mean'], c['median'], c['n_docs']))
    print()
    print('=== attribution, 8-author panel, chance = %.3f' % out['chance'])
    for k in ('within_register_attribution', 'cross_register_attribution', 'reverse_attribution'):
        a = p[k]
        print('  %-30s micro %.3f  macro %.3f' % (k, a['micro'], a['macro']))
    print()
    print('=== per author, cross-register (plays -> his own non-dramatic writing)')
    for a in PANEL:
        v = p['cross_register_attribution']['per_author'][a]
        w = p['within_register_attribution']['per_author'][a]
        print('  %-20s n=%4d  cross %.3f   |  within n=%4d  %.3f' %
              (a, v['n'], v['acc'], w['n'], w['acc']))
    nl = out['permutation_null_cross_register']
    print()
    print('=== permutation null (200 author-label shuffles): mean macro %.3f, p95 %.3f, max %.3f'
          % (nl['mean_macro'], nl['p95'], nl['max']))


if __name__ == '__main__':
    main()
