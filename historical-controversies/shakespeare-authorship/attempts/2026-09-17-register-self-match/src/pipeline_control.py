"""P5. How far apart are the SAME PLAY extracted two ways?

The play half of this corpus comes from engdracor; the non-dramatic half comes
straight from EEBO-TCP. engdracor is derived from TCP, but it is not byte-identical
to it - it strips speakers and stage directions slightly differently and drops
some front matter. If that extraction difference were comparable in size to the
between-author distance, then any "register gap" measured here could be an
artefact of which pipeline touched the text.

So: for every play that exists in both, extract it both ways, chunk both the same
way, and measure the Delta distance between the two versions of the same play.
That distance is the pipeline artefact, in the same units as everything else.
"""
import sys, os, json, re, collections
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import tcp, delta as D

HERE = os.path.dirname(__file__)


def main():
    docs = json.load(open(os.path.join(HERE, '..', 'data', 'chunks.json')))
    vocab = D.vocabulary(docs)
    # reference scaling: the drama chunks, which is what everything is compared in
    dram = [d for d in docs if d['register'] == 'drama']
    Xd = D.vectors(dram, vocab)
    mu, sd = Xd.mean(0), Xd.std(0); sd[sd == 0] = 1

    sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-05-stylometry-calibration', 'src'))
    import corpus as playcorpus
    plays = playcorpus.load()
    have = set(f[:-4] for f in os.listdir(tcp.TCP_DIR))

    rows = []
    for p in plays:
        if p['id'] not in have:
            continue
        w_tcp = tcp.words(tcp.raw(p['id']))
        if len(w_tcp) < 6000 or len(p['words']) < 6000:
            continue
        n = min(len(w_tcp), len(p['words']))
        a = {'words': w_tcp[:n]}
        b = {'words': p['words'][:n]}
        X = D.vectors([a, b], vocab)
        Z = (X - mu) / sd
        rows.append({'play': p['slug'], 'author': p['author'],
                     'n_words': n,
                     'len_ratio': round(len(w_tcp) / len(p['words']), 4),
                     'dist': float(np.abs(Z[0] - Z[1]).sum())})
    d = np.array([r['dist'] for r in rows])
    out = {'n_plays': len(rows), 'mean': float(d.mean()), 'median': float(np.median(d)),
           'p90': float(np.percentile(d, 90)), 'max': float(d.max()),
           'worst': sorted(rows, key=lambda r: -r['dist'])[:5]}
    json.dump(out, open(os.path.join(HERE, '..', 'results', 'pipeline_control.json'), 'w'), indent=1)
    print('same play, engdracor vs TCP, n=%d' % len(rows))
    print('  mean Delta %.3f   median %.3f   p90 %.3f   max %.3f' %
          (out['mean'], out['median'], out['p90'], out['max']))
    print('  worst:', [(r['play'][:34], round(r['dist'], 1), r['len_ratio']) for r in out['worst']])


if __name__ == '__main__':
    main()
