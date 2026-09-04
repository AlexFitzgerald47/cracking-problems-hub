"""English character-stream model used as the null/reference language for the
Dorabella experiments.

Design note: this session had no egress to any natural-language corpus, so the
reference language is *generated* from a frequency-weighted English lexicon
(`wordfreq`) under a unigram word model, then written out spaceless and
uppercase to match the cipher (which has no word separators).

The model is therefore correct for letter frequencies and for within-word
n-grams, and approximately correct for cross-word-boundary n-grams (it gets the
marginal distribution of adjacent word pairs right, but not their syntax).
`validate()` checks it against published English letter frequencies and against
the textbook index of coincidence before anything downstream relies on it.
"""
import random, math, pickle, os
import numpy as np
from wordfreq import top_n_list, word_frequency

A = 26
ORD_A = ord('A')
CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'lang_cache.pkl')

# Published English letter frequencies (%), Lewand's ordering, for validation only.
LEWAND = {
    'E': 12.702, 'T': 9.056, 'A': 8.167, 'O': 7.507, 'I': 6.966, 'N': 6.749,
    'S': 6.327, 'H': 6.094, 'R': 5.987, 'D': 4.253, 'L': 4.025, 'C': 2.782,
    'U': 2.758, 'M': 2.406, 'W': 2.360, 'F': 2.228, 'G': 2.015, 'Y': 1.974,
    'P': 1.929, 'B': 1.492, 'V': 0.978, 'K': 0.772, 'J': 0.153, 'X': 0.150,
    'Q': 0.095, 'Z': 0.074,
}


def build_lexicon(n=120_000):
    words, weights = [], []
    for w in top_n_list('en', n):
        u = ''.join(ch for ch in w.upper() if 'A' <= ch <= 'Z')
        if not u:
            continue
        f = word_frequency(w, 'en')
        if f <= 0:
            continue
        words.append(u)
        weights.append(f)
    return words, np.array(weights, dtype=np.float64) / sum(weights)


def make_corpus(n_chars=4_000_000, seed=1):
    """Spaceless uppercase English stream sampled under a unigram word model."""
    rng = np.random.default_rng(seed)
    words, p = build_lexicon()
    out, total = [], 0
    while total < n_chars:
        idx = rng.choice(len(words), size=20000, p=p)
        chunk = ''.join(words[i] for i in idx)
        out.append(chunk)
        total += len(chunk)
    return ''.join(out)[:n_chars]


def to_ints(s):
    return np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64) - ORD_A


def quadgram_logprobs(corpus_ints, k=0.5):
    """Add-k smoothed log10 quadgram probabilities as a flat 26^4 array."""
    idx = (corpus_ints[:-3] * A**3 + corpus_ints[1:-2] * A**2
           + corpus_ints[2:-1] * A + corpus_ints[3:])
    counts = np.bincount(idx, minlength=A**4).astype(np.float64)
    probs = (counts + k) / (counts.sum() + k * A**4)
    return np.log10(probs)


def load(n_chars=4_000_000, seed=1, rebuild=False):
    if os.path.exists(CACHE) and not rebuild:
        with open(CACHE, 'rb') as fh:
            return pickle.load(fh)
    corpus = make_corpus(n_chars, seed)
    ci = to_ints(corpus)
    obj = {'corpus': corpus, 'corpus_ints': ci, 'quad': quadgram_logprobs(ci)}
    with open(CACHE, 'wb') as fh:
        pickle.dump(obj, fh, protocol=4)
    return obj


def index_of_coincidence(ints, alphabet=A):
    n = len(ints)
    c = np.bincount(ints, minlength=alphabet).astype(np.float64)
    return float((c * (c - 1)).sum() / (n * (n - 1)))


def validate(model):
    ci = model['corpus_ints']
    counts = np.bincount(ci, minlength=A).astype(np.float64)
    pct = 100 * counts / counts.sum()
    rows, sq_err = [], 0.0
    for i in range(A):
        ch = chr(ORD_A + i)
        rows.append((ch, pct[i], LEWAND[ch]))
        sq_err += (pct[i] - LEWAND[ch]) ** 2
    return {
        'letter_freq': rows,
        'rms_error_pct_points': math.sqrt(sq_err / A),
        'ic': index_of_coincidence(ci),
        'ic_reference_english': 0.0667,
    }


def sample_english(model, n, count, rng):
    """`count` spaceless English strings of length `n`, as int arrays."""
    ci = model['corpus_ints']
    starts = rng.integers(0, len(ci) - n - 1, size=count)
    return np.stack([ci[s:s + n] for s in starts])
