"""Shared loading for the 2026-09-21 session.

Everything here operates on the chunk corpus built by the 2026-09-17 attempt
(`../2026-09-17-register-self-match/data/chunks.json`, gitignored and regenerable
from that attempt's `fetch_tcp.py` + `build_corpus.py`). Nothing is re-extracted:
this session's whole point is to re-analyse the *same* documents under two
different treatments, so any change to the extraction would confound the answer.
"""
import sys, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PREV = os.path.join(HERE, '..', '..', '2026-09-17-register-self-match')
sys.path.insert(0, os.path.join(PREV, 'src'))
import delta as D                                        # noqa: E402

PANEL = ['Chapman, George', 'Dekker, Thomas', 'Greene, Robert', 'Heywood, Thomas',
         'Jonson, Ben', 'Lyly, John', 'Marston, John', 'Middleton, Thomas']
SEED = 20260921
RESULTS = os.path.join(HERE, '..', 'results')


def load(require_year=False):
    docs = json.load(open(os.path.join(PREV, 'data', 'chunks.json')))
    dropped = 0
    out = []
    for d in docs:
        y = None
        try:
            y = int(str(d['year'])[:4])
        except (TypeError, ValueError):
            y = None
        if y is None and require_year:
            dropped += 1
            continue
        d['yr'] = y
        out.append(d)
    return out, dropped


def save(name, obj):
    os.makedirs(RESULTS, exist_ok=True)
    json.dump(obj, open(os.path.join(RESULTS, name), 'w'), indent=1)


def detrend(X, years, ref_mask, degree=1):
    """Remove a polynomial-in-year trend, fitted on `ref_mask` rows only.

    Fitting on a reference set rather than on everything matters: the primary
    scenario is that you hold a body of plays and ask where a candidate's
    non-dramatic writing falls against them, so the trend you can actually
    estimate is the one visible in the plays. Applying a trend fitted on the
    pooled corpus would let the test documents help define their own correction.
    Both are reported.
    """
    y = years.astype(float)
    V = np.vander(y, degree + 1)                  # [y^d ... y 1]
    Vr = V[ref_mask]
    # Centre the year axis on the reference mean to keep the Vandermonde matrix
    # conditioned; 1600^2 against 1 is otherwise a badly scaled least squares.
    c = y[ref_mask].mean()
    V = np.vander(y - c, degree + 1)
    Vr = V[ref_mask]
    coef, *_ = np.linalg.lstsq(Vr, X[ref_mask], rcond=None)
    return X - V @ coef


def zscale(X, ref_mask):
    mu, sd = X[ref_mask].mean(0), X[ref_mask].std(0)
    sd[sd == 0] = 1
    return (X - mu) / sd
