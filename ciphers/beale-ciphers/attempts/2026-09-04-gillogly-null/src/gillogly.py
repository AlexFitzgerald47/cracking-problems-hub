"""How improbable are the alphabetical runs in B1?

Decoding Beale cipher 1 with the Declaration of Independence produces stretches
that run through the alphabet - most famously `abcdefghiijklmmnohpp`. Gillogly
noticed this in 1980. It is the single most-cited piece of evidence in the hoax
argument, and it is almost always presented qualitatively.

This puts a number on it. Two statistics, both fixed before any null was run:

  R1  longest run whose consecutive steps are all in {0, +1}
      (alphabetical, repeats allowed - this is the shape the strings actually have)
  R2  longest run whose consecutive steps are all exactly +1

Undecodable numbers (past the end of the 1311-word key) break a run.

The null that matters is a *permutation* of each cipher's own numbers. It keeps
the multiset of numbers exactly as published and asks only whether their ORDER
is special. That is precisely the hoax question: a forger picking words in
alphabetical order leaves a signature in the ordering, not in the numbers used.

B2 is the control. It is a genuine message, enciphered against the same key text
by whoever wrote it, so whatever R1 a real Beale-style plaintext produces, B2
produces it.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import beale_data

SEED = 20260904
N_NULL = 100_000
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'gillogly_results.json')


def to_idx(decoded):
    """letter -> 0..25, gap -> -1"""
    return np.array([(ord(c) - 97) if 'a' <= c <= 'z' else -1 for c in decoded],
                    dtype=np.int16)


def longest_run(idx, steps):
    """Longest run of consecutive positions whose successive differences all lie
    in `steps`. Gaps (-1) break runs."""
    best = cur = 0
    prev = None
    for v in idx:
        if v < 0:
            cur, prev = 0, None
            continue
        if prev is None or (v - prev) not in steps:
            cur = 1
        else:
            cur += 1
        best = max(best, cur)
        prev = v
    return best


def runs_of(idx, steps, min_len):
    """All maximal runs of length >= min_len, as (start, length, text)."""
    out, start, prev = [], None, None
    for i, v in enumerate(idx):
        if v < 0:
            if start is not None and i - start >= min_len:
                out.append((start, i - start))
            start, prev = None, None
            continue
        if prev is None or (v - prev) not in steps:
            if start is not None and i - start >= min_len:
                out.append((start, i - start))
            start = i
        prev = v
    if start is not None and len(idx) - start >= min_len:
        out.append((start, len(idx) - start))
    return out


def main():
    rng = np.random.default_rng(SEED)
    d = beale_data.load()
    doi, special = d['doi'], d['special']
    res = {'seed': SEED, 'n_null': N_NULL,
           'validation': {'cross_check': d['cross_check'],
                          'b2': d['b2_validation']},
           'ciphers': {}}

    STEPS = {'R1': frozenset((0, 1)), 'R2': frozenset((1,))}

    for n in (1, 2, 3):
        cipher = d['ciphers'][n]
        dec = beale_data.decode(cipher, doi, special if n == 2 else None)
        idx = to_idx(dec)
        entry = {'n_tokens': len(cipher), 'n_gaps': int((idx < 0).sum()),
                 'decoded': dec, 'observed': {}, 'null': {}}
        for name, steps in STEPS.items():
            obs = longest_run(idx, steps)
            null = np.empty(N_NULL, dtype=np.int32)
            work = idx.copy()
            for k in range(N_NULL):
                rng.shuffle(work)
                null[k] = longest_run(work, steps)
            entry['observed'][name] = obs
            entry['null'][name] = {
                'mean': float(null.mean()), 'sd': float(null.std(ddof=1)),
                'max': int(null.max()), 'p99.9': float(np.percentile(null, 99.9)),
                'p_value': float((null >= obs).mean()),
                'n_at_or_above': int((null >= obs).sum()),
            }
        # the actual strings, for the record
        entry['runs_R1_min8'] = [
            {'start': s, 'length': L, 'text': dec[s:s + L]}
            for s, L in runs_of(idx, STEPS['R1'], 8)]
        res['ciphers']['B%d' % n] = entry

    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)

    print('%-4s %7s %6s   %-28s %-28s' % ('', 'tokens', 'gaps', 'R1 (steps in {0,+1})', 'R2 (steps = +1)'))
    for k, e in res['ciphers'].items():
        r1, r2 = e['null']['R1'], e['null']['R2']
        print('%-4s %7d %6d   obs %2d  null %.1f+-%.1f p=%-8.5f obs %2d  null %.1f+-%.1f p=%.5f'
              % (k, e['n_tokens'], e['n_gaps'],
                 e['observed']['R1'], r1['mean'], r1['sd'], r1['p_value'],
                 e['observed']['R2'], r2['mean'], r2['sd'], r2['p_value']))
    print()
    for k, e in res['ciphers'].items():
        if e['runs_R1_min8']:
            print('%s alphabetical runs of length >= 8:' % k)
            for r in e['runs_R1_min8']:
                print('   index %3d  length %2d  %s' % (r['start'], r['length'], r['text']))


if __name__ == '__main__':
    main()
