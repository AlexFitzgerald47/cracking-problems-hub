"""Two things PREDICTIONS.md promised to report whatever they said.

1. A permutation null for the held-out pageant recovery, and the power available
   at n = 35 chunks. A zero can be unremarkable when n is small, and saying so is
   part of the result.
2. The TCP <gap> rate by author and register. TCP marks illegible passages with
   <gap>; if damage were systematically heavier in one register it would be a
   transcription confound riding alongside the register effect - the same check
   the Junius session ran on long-s damage.
"""
import sys, os, json, csv, collections, random
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import tcp, delta as D
from analysis import load, scaled, PANEL
from build_corpus import PAGEANTS, AUTH, chunks

HERE = os.path.dirname(__file__)
rng = random.Random(20260917)


def pageant_null():
    rows = {r['TCP']: r for r in csv.DictReader(
        open('/tmp/w/TCP.csv', encoding='utf-8', errors='replace'))}
    pag = []
    for tid in PAGEANTS:
        r = rows[tid]
        w, _ = tcp.words_with_damage(tcp.raw(tid))
        for j, c in enumerate(chunks(w)):
            pag.append({'id': '%s#%d' % (tid, j), 'author': AUTH[r['Author']],
                        'register': 'pageant', 'work': tid, 'year': r['Date'], 'words': c})
    docs = load(); vocab = D.vocabulary(docs)
    drama = [d for d in docs if d['register'] == 'drama']
    authors = sorted(set(d['author'] for d in drama))
    allv = docs + pag
    Z = scaled(allv, vocab, drama)
    au = np.array([d['author'] for d in allv]); rg = np.array([d['register'] for d in allv])
    cent = np.stack([Z[(au == a) & (rg == 'drama')].mean(0) for a in authors])
    idx = np.where(rg == 'pageant')[0]
    pred = [authors[i] for i in np.abs(Z[idx][:, None, :] - cent[None, :, :]).sum(2).argmin(1)]
    true = list(au[idx])
    obs = float(np.mean([p == t for p, t in zip(pred, true)]))

    # null 1: shuffle which of the four pageant authors owns each pageant WORK
    works = sorted(set(allv[i]['work'] for i in idx))
    owner = {w: next(allv[i]['author'] for i in idx if allv[i]['work'] == w) for w in works}
    pag_authors = sorted(set(owner.values()))
    nulls = []
    for _ in range(2000):
        perm = pag_authors[:]; rng.shuffle(perm)
        m = dict(zip(pag_authors, perm))
        fake = [m[owner[allv[i]['work']]] for i in idx]
        nulls.append(np.mean([p == t for p, t in zip(pred, fake)]))
    p_val = float(np.mean([n >= obs for n in nulls]))

    # power: if the method really recovered its own out-of-register work at rate r,
    # how often would we see 0 hits for Middleton (12), Heywood (8), Jonson (5)?
    power = {}
    for r in (0.10, 0.25, 0.50, 0.717):
        power['rate_%.3f' % r] = {
            'P(0 of 12)': (1 - r) ** 12, 'P(0 of 8)': (1 - r) ** 8,
            'P(0 of 5)': (1 - r) ** 5, 'P(0 of 25 combined)': (1 - r) ** 25}
    return {'observed_micro': obs, 'null_mean': float(np.mean(nulls)),
            'null_p95': float(np.percentile(nulls, 95)), 'p_value': p_val,
            'n_chunks': len(idx), 'power_if_true_rate_were': power}


def damage_rates():
    man = json.load(open(os.path.join(HERE, '..', 'data', 'manifest.json')))
    nd = collections.defaultdict(lambda: [0, 0])
    for r in man['kept']:
        nd[r['author']][0] += r['gap']; nd[r['author']][1] += r['n_words']
    dr = collections.defaultdict(lambda: [0, 0])
    sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-09-05-stylometry-calibration', 'src'))
    import corpus as pc
    have = set(f[:-4] for f in os.listdir(tcp.TCP_DIR))
    for p in pc.load():
        if p['author'] not in PANEL or p['id'] not in have:
            continue
        s = tcp.raw(p['id'])
        dr[p['author']][0] += tcp.structure(s)['gap']; dr[p['author']][1] += p['n_words']
    out = {}
    for a in PANEL:
        out[a] = {
            'nondrama_gaps_per_10k': round(nd[a][0] / max(1, nd[a][1]) * 10000, 2),
            'drama_gaps_per_10k': round(dr[a][0] / max(1, dr[a][1]) * 10000, 2)}
    return out


def main():
    res = {'pageant_null': pageant_null(), 'tcp_gap_rate_per_10k_words': damage_rates()}
    json.dump(res, open(os.path.join(HERE, '..', 'results', 'nulls_and_damage.json'), 'w'), indent=1)
    p = res['pageant_null']
    print('held-out pageant recovery: observed micro %.3f, n=%d' % (p['observed_micro'], p['n_chunks']))
    print('  permutation null (2000 shuffles of pageant ownership): mean %.3f, p95 %.3f, p=%.3f'
          % (p['null_mean'], p['null_p95'], p['p_value']))
    print('\npower - probability of seeing ZERO own-pageant hits if the true recovery rate were:')
    for k, v in p['power_if_true_rate_were'].items():
        print('  %s  Middleton(12) %.4f  Heywood(8) %.4f  Jonson(5) %.4f  all 25 %.6f'
              % (k, v['P(0 of 12)'], v['P(0 of 8)'], v['P(0 of 5)'], v['P(0 of 25 combined)']))
    print('\nTCP <gap> rate per 10,000 words (transcription damage, by register):')
    print('  %-22s %12s %12s' % ('author', 'nondrama', 'drama'))
    for a, v in res['tcp_gap_rate_per_10k_words'].items():
        print('  %-22s %12.2f %12.2f' % (a, v['nondrama_gaps_per_10k'], v['drama_gaps_per_10k']))


if __name__ == '__main__':
    main()
