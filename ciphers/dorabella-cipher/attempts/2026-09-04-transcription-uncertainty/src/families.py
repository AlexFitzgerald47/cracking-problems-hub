"""Clusters the high-scoring local optima into families.

Two optima belong to the same family if their plaintexts differ at no more than
`THRESHOLD` of the 87 positions — i.e. they are the same reading modulo the
assignment of a few rare symbols. Families that are further apart than that are
genuinely different messages, and if several of them score at or above a
published claimed solution, that solution's score is not evidence for it.
"""
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(__file__))

R = os.path.join(os.path.dirname(__file__), '..', 'results')
THRESHOLD = 8


def hamming(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)


def cluster(cands, threshold=THRESHOLD):
    fams = []
    for pt, sc in sorted(cands, key=lambda t: -t[1]):
        for f in fams:
            if hamming(pt, f['representative']) <= threshold:
                f['members'].append({'plaintext': pt, 'score': sc})
                break
        else:
            fams.append({'representative': pt, 'score': sc,
                         'members': [{'plaintext': pt, 'score': sc}]})
    return fams


def main():
    r = json.load(open(os.path.join(R, 'claimed_results.json')))
    cands = [(x['plaintext'], x['score']) for x in r['at_or_above_claimed']]
    fams = cluster(cands)
    dists = [{'a': i, 'b': j, 'hamming': hamming(fams[i]['representative'],
                                                 fams[j]['representative'])}
             for i, j in itertools.combinations(range(len(fams)), 2)]
    out = {
        'clustering_threshold_hamming': THRESHOLD,
        'claimed_score': r['claimed_score'],
        'claimed_plaintext': r['claimed_plaintext'],
        'n_optima_at_or_above_claimed': len(cands),
        'n_families': len(fams),
        'families': [{'score': f['score'], 'n_members': len(f['members']),
                      'representative': f['representative']} for f in fams],
        'family_distances': dists,
        'min_distance_between_families': min(d['hamming'] for d in dists) if dists else None,
        'median_distance_between_families': sorted(d['hamming'] for d in dists)[len(dists) // 2] if dists else None,
    }
    with open(os.path.join(R, 'claimed_families.json'), 'w') as fh:
        json.dump(out, fh, indent=1)
    print('%d optima >= claimed, forming %d distinct families' % (len(cands), len(fams)))
    for f in out['families']:
        print('  %.4f  x%-2d  %s' % (f['score'], f['n_members'], f['representative']))
    print('median distance between families: %s of 87' % out['median_distance_between_families'])


if __name__ == '__main__':
    main()
