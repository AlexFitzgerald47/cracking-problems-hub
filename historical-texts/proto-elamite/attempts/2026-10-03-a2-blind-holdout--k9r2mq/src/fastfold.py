"""Numpy-accelerated re-implementation of crossfit.run_fold, for the null model.

Verified against the audited pure-python path on the real corpus before use
(src/verify_fast.py). The acceleration is in the contingency table construction
only; the Fisher test, the BH adjustment and the within-tablet exact
randomization test are the audited functions themselves, unchanged.
"""
from __future__ import annotations
import hashlib, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from common import load_audited

sa = load_audited()


def bucket(tablet: str) -> int:
    return int(hashlib.sha256(tablet.encode("ascii")).hexdigest()[:8], 16) % 5


class Design:
    """Line x sign incidence matrices plus the tablet/bucket index."""

    def __init__(self, lines):
        self.lines = lines
        self.m_vocab = sorted({s for ln in lines for s in ln.m_signs})
        self.n_vocab = sorted({s for ln in lines for s in ln.n_signs})
        mi = {s: i for i, s in enumerate(self.m_vocab)}
        ni = {s: i for i, s in enumerate(self.n_vocab)}
        self.M = np.zeros((len(lines), len(self.m_vocab)), dtype=np.int32)
        self.N = np.zeros((len(lines), len(self.n_vocab)), dtype=np.int32)
        for r, ln in enumerate(lines):
            for s in ln.m_signs:
                self.M[r, mi[s]] = 1
            for s in ln.n_signs:
                self.N[r, ni[s]] = 1
        self.tablet = np.array([ln.tablet for ln in lines])
        self.bucket = np.array([bucket(ln.tablet) for ln in lines])

    def permute_within_tablet(self, rng):
        """Null: permute whole N-sign SET assignments among lines of one tablet.

        Destroys M-numeral association; preserves tablet structure, line counts
        and the joint composition of every numeral expression exactly.
        """
        N2 = self.N.copy()
        order = np.argsort(self.tablet, kind="stable")
        t_sorted = self.tablet[order]
        starts = np.flatnonzero(np.r_[True, t_sorted[1:] != t_sorted[:-1]])
        ends = np.r_[starts[1:], len(t_sorted)]
        for s, e in zip(starts, ends):
            if e - s > 1:
                idx = order[s:e]
                N2[idx] = N2[rng.permutation(idx)]
        return N2


def run_fold_fast(d: Design, N, test_bucket: int):
    tr = d.bucket != test_bucket
    te = ~tr
    Mtr, Ntr = d.M[tr], N[tr]
    ntr = int(tr.sum())
    # a = co-occurrence, row totals = M counts, col totals = N counts
    A = Mtr.T @ Ntr                       # (m, n)
    ab = Mtr.sum(0)[:, None]              # lines bearing the M family
    ac = Ntr.sum(0)[None, :]              # lines bearing the N sign
    keep = (ab >= 20) & (ac >= 20)
    # candidate M families / N signs must exist in TRAIN, as the published rule has it
    keep &= (ab > 0) & (ac > 0)
    mi, nj = np.nonzero(keep)
    raw = []
    for i, j in zip(mi, nj):
        a = int(A[i, j]); b = int(ab[i, 0]) - a; c = int(ac[0, j]) - a
        dd = ntr - a - b - c
        raw.append((i, j, sa.odds_ratio(a, b, c, dd),
                    sa.fisher_exact_two_sided(a, b, c, dd)))
    if not raw:
        return []
    qs = sa.bh_adjust([r[3] for r in raw])
    sel = [r for r, q in zip(raw, qs) if q <= 0.01 and (r[2] >= 3.0 or r[2] <= 1 / 3)]
    if not sel:
        return []

    te_idx = np.flatnonzero(te)
    te_lines = [d.lines[k] for k in te_idx]
    Nte = N[te]
    Mte = d.M[te]
    tablets = {}
    for pos, ln in enumerate(te_lines):
        tablets.setdefault(ln.tablet, []).append(pos)

    ps, cl = [], []
    for i, j, tor, _ in sel:
        mcol = Mte[:, i]; ncol = Nte[:, j]
        a = int(np.dot(mcol, ncol)); b = int(mcol.sum()) - a
        c = int(ncol.sum()) - a; dd = len(te_lines) - a - b - c
        cl.append((a, b, c, dd))
        # within-tablet exact randomization, identical to the audited function
        dist = [1.0]; obs = 0
        for pos in tablets.values():
            n = len(pos)
            s = int(mcol[pos].sum()); t = int(ncol[pos].sum())
            obs += int(np.dot(mcol[pos], ncol[pos]))
            lo = max(0, s - (n - t)); hi = min(s, t)
            local = [0.0] * (hi + 1)
            for k in range(lo, hi + 1):
                local[k] = sa.hypergeom_probability(k, s, t, n)
            comb = [0.0] * (len(dist) + len(local) - 1)
            for x, px in enumerate(dist):
                if not px:
                    continue
                for y, py in enumerate(local):
                    if py:
                        comb[x + y] += px * py
            dist = comb
        ps.append(min(1.0, sum(dist[obs:]) if tor > 1 else sum(dist[:obs + 1])))
    qs2 = sa.bh_adjust(ps)

    out = []
    for (i, j, tor, _), cells, p, q in zip(sel, cl, ps, qs2):
        vor = sa.odds_ratio(*cells)
        same = (tor > 1 and vor > 1) or (tor < 1 and vor < 1)
        if (cells[0] + cells[1] >= 5 and same and q <= 0.05
                and (vor >= 1.5 or vor <= 1 / 1.5)):
            out.append(f"{d.m_vocab[i]}-{d.n_vocab[j]}")
    return out
