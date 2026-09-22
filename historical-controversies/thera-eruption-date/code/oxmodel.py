"""
A minimal re-implementation of the OxCal single-phase Bayesian chronological
model, written from the published specification so that the priors can be
swapped and their influence measured.

Specification followed (OxCal v4 help, "Analysis operations"):

  Group priors, for boundaries t_a < t_b (both with uniform priors):
    Boundary     / Boundary     : p(t_i) = pH(t_a,t_i,t_b) / (t_b-t_a)
    Tau_Boundary / Boundary     : p(t_i) = [pH(t_i,t_b)/(t_b-t_a)]
                                           exp(-(t_b-t_i)/(t_b-t_a))
    Zero_Boundary/ Boundary     : p(t_i) = 2 pH(t_a,t_i,t_b) (t_i-t_a)/(t_b-t_a)^2
  Outlier_Model("General", T(5), U(0,4), "t"):
    with prior probability q the sample's calendar position is displaced by
    delta = 10^u * z, u ~ U(0,4), z ~ Student-t(5). Marginalising the indicator
    gives the mixture likelihood used here,
        L_mix(t) = (1-q) L(t) + q * Lout(t),  Lout(t) = E_delta[L(t+delta)],
    and the posterior outlier probability is the posterior mean of the
    indicator, which this sampler records.

Time runs forward: t is a calendar year, negative = BC (astronomical, so
-1600 is 1601 BC). Conversion helpers are in calib.py.
"""
import numpy as np
from calib import Curve, loglik


def cal_to_year(calbp):
    """cal BP -> astronomical calendar year (1950 - calBP)."""
    return 1950 - calbp


class Dates:
    """Likelihood curves for a set of determinations on a calendar-year grid."""

    def __init__(self, curve, dets, lo_year, hi_year, q_outlier=0.05,
                 n_mc=20000, seed=11, outliers=True):
        self.curve, self.dets, self.q = curve, list(dets), q_outlier
        self.years = np.arange(lo_year, hi_year + 1)          # ascending forward
        cal_full = curve.grid                                  # ascending cal BP
        yr_full = cal_to_year(cal_full)                        # descending
        order = np.argsort(yr_full)
        self.yr_full = yr_full[order]
        self.mu_full = curve.mu[order]
        self.sd_full = curve.sd[order]
        self.i0 = int(np.searchsorted(self.yr_full, lo_year))
        self.i1 = int(np.searchsorted(self.yr_full, hi_year)) + 1
        assert self.yr_full[self.i0] == lo_year and self.yr_full[self.i1 - 1] == hi_year

        rng = np.random.default_rng(seed)
        L, Lout = [], []
        for (_, r, s) in self.dets:
            v = s * s + self.sd_full ** 2
            lfull = np.exp(-0.5 * (r - self.mu_full) ** 2 / v) / np.sqrt(v)
            L.append(lfull[self.i0:self.i1])
            if outliers:
                u = rng.uniform(0, 4, n_mc)
                z = rng.standard_t(5, n_mc)
                d = np.rint(10 ** u * z).astype(int)
                acc = np.zeros(self.i1 - self.i0)
                n = len(lfull)
                for dd in d:                    # L(t+delta): shift index by delta
                    a, b = self.i0 + dd, self.i1 + dd
                    if b <= 0 or a >= n:
                        continue
                    lo_pad = max(0, -a); hi_pad = max(0, b - n)
                    seg = lfull[max(a, 0):min(b, n)]
                    acc[lo_pad:len(acc) - hi_pad] += seg
                Lout.append(acc / n_mc)
            else:
                Lout.append(np.zeros(self.i1 - self.i0))
        self.L = np.array(L)
        self.Lout = np.array(Lout)
        self.outliers = outliers
        self.Lmix = (1 - self.q) * self.L + self.q * self.Lout if outliers else self.L
        self.n = len(self.dets)


def _sample_grid(rng, logw):
    logw = logw - logw.max()
    w = np.exp(logw)
    tot = w.sum()
    if not np.isfinite(tot) or tot <= 0:
        return None
    return int(rng.choice(len(w), p=w / tot))


def run_phase(d, kind='tau', n_iter=60000, burn=6000, thin=5, seed=3,
              span_lo=None, span_hi=None):
    """
    Gibbs sampler for one phase.
      kind = 'tau'      : Tau_Boundary(start) .. Boundary(end)   [exponential]
             'uniform'  : Boundary .. Boundary                   [uniform phase]
             'zero'     : Zero_Boundary(start) .. Boundary(end)  [linear rise]
             'combine'  : all dates share one calendar year (R_Combine)
             'none'     : no group prior at all (independent calibration)
    Returns dict with samples of the end boundary (and start), and posterior
    outlier probabilities.
    """
    rng = np.random.default_rng(seed)
    yrs = d.years
    m = len(yrs)
    Lmix = np.maximum(d.Lmix, 1e-300)
    logLmix = np.log(Lmix)

    if kind == 'combine':
        lp = logLmix.sum(axis=0)
        w = np.exp(lp - lp.max()); w /= w.sum()
        return dict(end=yrs, end_w=w, start=None, outlier_p=None, kind=kind)
    if kind == 'none':
        lp = logLmix.max(axis=0)   # not used for a boundary; placeholder
        return dict(end=None, start=None, outlier_p=None, kind=kind)

    lo_i = 0 if span_lo is None else int(np.searchsorted(yrs, span_lo))
    hi_i = m - 1 if span_hi is None else int(np.searchsorted(yrs, span_hi))

    # init: dates at their marginal modes, boundaries just outside
    ti = np.array([int(np.argmax(Lmix[i])) for i in range(d.n)])
    tb = min(m - 1, int(ti.max()) + 20)
    ta = max(0, int(ti.min()) - 20)

    keep_end, keep_start, out_acc = [], [], np.zeros(d.n)
    n_kept = 0
    for it in range(n_iter):
        # --- dates
        for i in range(d.n):
            if kind == 'tau':
                tau = max(tb - ta, 1)
                lp = logLmix[i].copy()
                lp[tb + 1:] = -np.inf
                lp[:tb + 1] += -(tb - np.arange(tb + 1)) / tau
            elif kind == 'uniform':
                lp = np.full(m, -np.inf)
                lp[ta:tb + 1] = logLmix[i][ta:tb + 1]
            elif kind == 'zero':
                lp = np.full(m, -np.inf)
                seg = np.arange(ta, tb + 1)
                lp[ta:tb + 1] = logLmix[i][ta:tb + 1] + np.log(
                    np.maximum(seg - ta, 1e-9))
            k = _sample_grid(rng, lp)
            if k is not None:
                ti[i] = k
        # --- boundaries
        if kind == 'tau':
            cand = np.arange(m)
            ok = cand > ti.max()
            tau = np.maximum(cand - ta, 1e-9)
            S = d.n * cand - ti.sum()
            lp = np.where(ok & (cand > ta), -d.n * np.log(tau) - S / tau, -np.inf)
            k = _sample_grid(rng, lp)
            if k is not None:
                tb = k
            cand = np.arange(m)
            tau = np.maximum(tb - cand, 1e-9)
            S = d.n * tb - ti.sum()
            lp = np.where(cand < tb, -d.n * np.log(tau) - S / tau, -np.inf)
            k = _sample_grid(rng, lp)
            if k is not None:
                ta = k
        else:
            cand = np.arange(m)
            span = np.maximum(cand - ta, 1e-9)
            lp = np.where(cand > ti.max(), -d.n * np.log(span), -np.inf)
            k = _sample_grid(rng, lp)
            if k is not None:
                tb = k
            span = np.maximum(tb - cand, 1e-9)
            lp = np.where(cand < ti.min(), -d.n * np.log(span), -np.inf)
            k = _sample_grid(rng, lp)
            if k is not None:
                ta = k
        if it >= burn and (it - burn) % thin == 0:
            keep_end.append(tb); keep_start.append(ta)
            if d.outliers:
                num = d.q * d.Lout[np.arange(d.n), ti]
                den = num + (1 - d.q) * d.L[np.arange(d.n), ti]
                out_acc += num / np.maximum(den, 1e-300)
            n_kept += 1
    end = yrs[np.array(keep_end)]
    start = yrs[np.array(keep_start)]
    return dict(end=end, start=start, outlier_p=out_acc / max(n_kept, 1),
                kind=kind, n_kept=n_kept)


# ---------------------------------------------------------------- reporting
def hpd_from_samples(samples, level=0.683, grid=None):
    """HPD of a sample of integer calendar years -> list of (startBC, endBC, mass)."""
    if grid is None:
        grid = np.arange(samples.min(), samples.max() + 1)
    cnt = np.bincount(samples - grid[0], minlength=len(grid)).astype(float)
    p = cnt / cnt.sum()
    order = np.argsort(p)[::-1]
    c = np.cumsum(p[order]); k = int(np.searchsorted(c, level)) + 1
    keep = np.zeros(len(p), bool); keep[order[:k]] = True
    out, i = [], 0
    while i < len(p):
        if keep[i]:
            j = i
            while j + 1 < len(p) and keep[j + 1]:
                j += 1
            out.append((grid[i], grid[j], p[i:j + 1].sum()))
            i = j + 1
        else:
            i += 1
    # calendar year -> BC label (year -1600 == 1601 BC)
    return [(1 - a, 1 - b, mss) for a, b, mss in out]


def fmt(regions):
    return ", ".join("%d-%d BCE (%.1f%%)" % (a, b, 100 * m) for a, b, m in regions)
