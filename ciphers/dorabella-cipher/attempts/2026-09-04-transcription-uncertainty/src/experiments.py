"""Runs every experiment for the 2026-09-04 Dorabella attempt and writes
results/raw_results.json. Deterministic given SEED."""
import sys, os, json, itertools, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import lang, dorabella as D, solver

SEED = 20260904
OUT = os.path.join(os.path.dirname(__file__), '..', 'results', 'raw_results.json')
N_NULL = 20000        # Monte Carlo draws for the descriptive-statistic nulls
N_SOLVE_ENGLISH = 150  # English controls put through the solver
N_SOLVE_SHUFFLE = 150  # Dorabella-shuffle controls put through the solver
RESTARTS = 40


def descriptive_nulls(model, rng, n=87):
    eng = lang.sample_english(model, n, N_NULL, rng)
    rows = []
    for arr in eng:
        s = ''.join(chr(ord('A') + c) for c in arr)
        rows.append(D.stats(s))
    return rows


def summarise(rows, key):
    v = np.array([r[key] for r in rows], dtype=np.float64)
    return {'mean': float(v.mean()), 'sd': float(v.std(ddof=1)),
            'p2.5': float(np.percentile(v, 2.5)), 'p50': float(np.percentile(v, 50)),
            'p97.5': float(np.percentile(v, 97.5)), 'min': float(v.min()),
            'max': float(v.max())}


def pct_below(rows, key, x):
    v = np.array([r[key] for r in rows], dtype=np.float64)
    return float((v < x).mean())


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    model = lang.load()
    res = {'seed': SEED, 'language_model_validation': lang.validate(model)}
    res['language_model_validation']['letter_freq'] = [
        {'letter': a, 'model_pct': b, 'reference_pct': c}
        for a, b, c in res['language_model_validation']['letter_freq']]

    d = D.load()
    ts = d['transcriptions']
    full = [t for t in ts if t['n'] == 87]

    # --- 1. per-reading descriptive statistics -------------------------------
    res['readings'] = [{'id': t['id'], 'label': t['label'], 'kind': t['kind'],
                        'canonical': D.canonical(t['text']), **D.stats(t['text'])}
                       for t in ts]

    # --- 2. relabelling-invariant agreement ----------------------------------
    res['pairwise_agreement'] = [
        {'a': a['label'], 'b': b['label'], **D.pair_agreement(a['text'], b['text'])}
        for a, b in itertools.combinations(full, 2)]

    # --- 3. consensus over the readings that are genuine transcriptions ------
    tx = [t for t in full if t['kind'] == 'transcription']
    # Williams and Robert S. are partition-identical; count the reading once.
    uniq, seen = [], set()
    for t in tx:
        c = D.canonical(t['text'])
        if c not in seen:
            seen.add(c)
            uniq.append(t)
    cons, forced = D.consensus([t['text'] for t in uniq])
    res['consensus'] = {'inputs': [t['label'] for t in uniq], 'text': cons,
                        'forced_merges': forced, **D.stats(cons)}

    # --- 4. descriptive statistics against an English null -------------------
    eng_rows = descriptive_nulls(model, rng)
    stat_keys = ['ic', 'distinct', 'doubles', 'repeated_bigram_types',
                 'repeated_trigram_types', 'longest_repeat', 'entropy_bits']
    res['english_null_87'] = {k: summarise(eng_rows, k) for k in stat_keys}
    res['english_null_87']['n_draws'] = N_NULL
    res['reading_vs_english_null'] = []
    for t in full:
        s = D.stats(t['text'])
        res['reading_vs_english_null'].append(
            {'label': t['label'], 'kind': t['kind'],
             **{k: {'value': s[k], 'pct_of_english_below': pct_below(eng_rows, k, s[k])}
                for k in stat_keys}})

    # --- 5. solver calibration ----------------------------------------------
    quad = model['quad']
    n = 87

    def solve(s):
        ti, k = solver.encode(s)
        tot, key = solver.hill_climb(ti, quad, k, rng, restarts=RESTARTS)
        return solver.per_quadgram(tot, len(ti)), solver.decrypt(ti, key)

    eng = lang.sample_english(model, n, N_SOLVE_ENGLISH, rng)
    eng_scores, eng_true = [], []
    for arr in eng:
        s = ''.join(chr(ord('A') + c) for c in arr)
        sc, _ = solve(s)
        eng_scores.append(sc)
        # fitness of the true plaintext, i.e. the target a correct solve hits
        eng_true.append(solver.per_quadgram(
            solver.score(arr, np.arange(26), quad), n))

    dora = next(t for t in full if t['label'] == 'Williams')['text']
    shuf_scores = []
    base = np.frombuffer(dora.encode(), dtype=np.uint8).copy()
    for _ in range(N_SOLVE_SHUFFLE):
        rng.shuffle(base)
        sc, _ = solve(base.tobytes().decode())
        shuf_scores.append(sc)

    res['solver'] = {'restarts': RESTARTS,
                     'english_solved': summarise([{'v': x} for x in eng_scores], 'v'),
                     'english_true_plaintext': summarise([{'v': x} for x in eng_true], 'v'),
                     'dorabella_shuffles': summarise([{'v': x} for x in shuf_scores], 'v'),
                     'n_english': N_SOLVE_ENGLISH, 'n_shuffles': N_SOLVE_SHUFFLE,
                     'english_scores': eng_scores, 'shuffle_scores': shuf_scores,
                     'readings': []}

    for t in full + [{'label': 'CONSENSUS', 'kind': 'consensus', 'text': cons, 'n': 87}]:
        sc, pt = solve(t['text'])
        e = np.array(eng_scores); sh = np.array(shuf_scores)
        res['solver']['readings'].append(
            {'label': t['label'], 'kind': t['kind'], 'best_per_quadgram': sc,
             'best_plaintext': pt,
             'pct_english_below': float((e < sc).mean()),
             'pct_shuffles_below': float((sh < sc).mean())})

    res['runtime_seconds'] = time.time() - t0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    print('wrote', OUT, 'in %.1fs' % res['runtime_seconds'])


if __name__ == '__main__':
    main()
