"""Monoalphabetic-substitution hill climber with quadgram fitness, plus the
calibration machinery that is the point of this attempt.

The fitness of a *solved* text is a property of the plaintext, not of the key.
So the distribution of best-achievable fitness over genuine 87-character
English tells us what score a correct solution of an 87-character English
monoalphabetic cipher should reach. Any claimed Dorabella solution that scores
below that distribution is not a solution; and if Dorabella's own best
achievable score sits inside the *noise* distribution instead, no solution of
this class can be validated at all.
"""
import numpy as np

A = 26


def encode(s):
    """Map an arbitrary symbol string onto 0..k-1 by first occurrence."""
    seen, out = {}, []
    for ch in s:
        if ch not in seen:
            seen[ch] = len(seen)
        out.append(seen[ch])
    return np.array(out, dtype=np.int64), len(seen)


def score(text_ints, key, quad):
    p = key[text_ints]
    idx = p[:-3] * 17576 + p[1:-2] * 676 + p[2:-1] * 26 + p[3:]
    return float(quad[idx].sum())


def hill_climb(text_ints, quad, k, rng, restarts=30):
    """Best key found over `restarts` random restarts of steepest-ascent
    pairwise-swap hill climbing."""
    best_s, best_k = -np.inf, None
    # Swapping two letters that no cipher symbol maps to is a no-op.
    pairs = [(i, j) for i in range(A) for j in range(i + 1, A) if i < k or j < k]
    for _ in range(restarts):
        key = rng.permutation(A)
        cur = score(text_ints, key, quad)
        improved = True
        while improved:
            improved = False
            for i, j in pairs:
                key[i], key[j] = key[j], key[i]
                s = score(text_ints, key, quad)
                if s > cur:
                    cur, improved = s, True
                else:
                    key[i], key[j] = key[j], key[i]
        if cur > best_s:
            best_s, best_k = cur, key.copy()
    return best_s, best_k


def per_quadgram(total, n):
    return total / (n - 3)


def decrypt(text_ints, key):
    return ''.join(chr(ord('a') + c) for c in key[text_ints])
