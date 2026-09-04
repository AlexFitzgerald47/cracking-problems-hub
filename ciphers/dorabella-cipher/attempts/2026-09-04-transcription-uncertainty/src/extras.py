"""Two supplementary tests: (a) is the mildly depressed index of coincidence
explained by a short polyalphabetic period? (b) where exactly do the
independent transcriptions disagree?"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, dorabella as D

OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'extras_results.json')
N_NULL = 20000


def periodic_ic(s, period):
    cols = [s[i::period] for i in range(period)]
    num = den = 0.0
    for c in cols:
        if len(c) < 2:
            continue
        _, counts = np.unique(np.frombuffer(c.encode(), dtype=np.uint8), return_counts=True)
        counts = counts.astype(np.float64)
        num += (counts * (counts - 1)).sum()
        den += len(c) * (len(c) - 1)
    return float(num / den) if den else float('nan')


def main():
    rng = np.random.default_rng(20260904 + 2)
    model = lang.load()
    d = D.load()
    tx = {t['label']: t['text'] for t in d['transcriptions'] if t['n'] == 87}

    eng = lang.sample_english(model, 87, N_NULL, rng)
    eng_s = [''.join(chr(ord('A') + c) for c in a) for a in eng]

    res = {'periodic_ic': {}, 'n_null': N_NULL}
    for p in range(1, 11):
        null = np.array([periodic_ic(s, p) for s in eng_s])
        entry = {'english_null': {'mean': float(null.mean()), 'sd': float(null.std(ddof=1)),
                                  'p2.5': float(np.percentile(null, 2.5)),
                                  'p97.5': float(np.percentile(null, 97.5))},
                 'readings': {}}
        for lab, s in tx.items():
            v = periodic_ic(s, p)
            entry['readings'][lab] = {'ic': v, 'pct_english_below': float((null < v).mean())}
        res['periodic_ic'][p] = entry

    # disagreement map across the genuinely independent transcriptions
    uniq, seen = [], set()
    for t in d['transcriptions']:
        if t['n'] == 87 and t['kind'] == 'transcription':
            c = D.canonical(t['text'])
            if c not in seen:
                seen.add(c)
                uniq.append((t['label'], t['text']))
    n = 87
    ems = [D.eq_matrix(s) for _, s in uniq]
    unstable = []
    for i in range(n):
        conflicts = 0
        for j in range(n):
            if i == j:
                continue
            vals = {bool(e[i, j]) for e in ems}
            if len(vals) > 1:
                conflicts += 1
        if conflicts:
            unstable.append({'position': i, 'line': 0 if i < 29 else (1 if i < 60 else 2),
                             'conflicting_partners': conflicts,
                             'symbols': [s[i] for _, s in uniq]})
    res['independent_transcriptions'] = [lab for lab, _ in uniq]
    res['unstable_positions'] = unstable
    res['n_unstable_positions'] = len(unstable)

    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('independent transcriptions:', res['independent_transcriptions'])
    print('unstable positions: %d of 87' % len(unstable))
    for u in unstable:
        print('  pos %2d (line %d) symbols %s  conflicts %d' % (
            u['position'], u['line'] + 1, u['symbols'], u['conflicting_partners']))
    print()
    print('period  englishNull(mean+-sd)   ' + '  '.join('%-10s' % l[:10] for l in tx))
    for p in range(1, 11):
        e = res['periodic_ic'][p]['english_null']
        row = 'p=%-4d %.4f+-%.4f   ' % (p, e['mean'], e['sd'])
        row += '  '.join('%.4f    ' % res['periodic_ic'][p]['readings'][l]['ic'] for l in tx)
        print(row)


if __name__ == '__main__':
    main()
