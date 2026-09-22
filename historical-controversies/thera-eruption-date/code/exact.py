"""
Exact marginal posterior for a single-phase OxCal group model.

Given boundaries (t_a, t_b) the dated events t_i are conditionally independent,
so the boundary posterior can be written down without MCMC:

    p(t_a,t_b | data)  ~  prior(t_a,t_b) * prod_i  sum_t L_i(t) w(t | t_a,t_b)

where w is the within-group prior from the OxCal specification. Both integrals
below are computed in closed form on the 1-year grid:

  tau model   (Tau_Boundary .. Boundary, exponential rising to t_b)
      w(t) = (1/tau) exp(-(t_b - t)/tau),  t < t_b,  tau = t_b - t_a
      sum_t L(t) e^{-(t_b-t)/tau} is a one-sided exponential filter, O(m) by
      the recursion g(t) = L(t) + e^{-1/tau} g(t-1).

  uniform model (Boundary .. Boundary)
      w(t) = 1/(t_b - t_a) on [t_a, t_b]; the sum is a difference of cumsums.

  combine  (R_Combine): all dates share one t; posterior ~ prod_i L_i(t).

This removes every mixing question from the result, which matters here: a
Gibbs sampler on the same model sat in a local mode ~90 years away from the
true posterior mass (see PROGRESS 2026-09-22).
"""
import numpy as np


def _logsum(a, axis=None):
    m = np.max(a, axis=axis, keepdims=True)
    m = np.where(np.isfinite(m), m, 0.0)       # all -inf slice -> keep -inf, no nan
    out = m + np.log(np.sum(np.exp(a - m), axis=axis, keepdims=True))
    return np.squeeze(out, axis=axis) if axis is not None else float(out)


def tau_posterior(D, tau_max=800, tau_min=1):
    """Joint posterior over (tau, t_b) for the Tau_Boundary..Boundary model.

    Returns (taus, years, logp) with logp[j,k] for tau=taus[j], t_b=years[k].
    Uniform prior on (t_a, t_b) => uniform on (tau, t_b); Jacobian 1.
    """
    L = np.maximum(D.Lmix, 1e-300)
    n, m = L.shape
    taus = np.arange(tau_min, tau_max + 1)
    logp = np.empty((len(taus), m))
    for j, tau in enumerate(taus):
        rho = np.exp(-1.0 / tau)
        acc = np.zeros(m)
        # g(t) = sum_{s<=t} L(s) rho^{t-s}   (one-sided exponential filter)
        for i in range(n):
            g = np.empty(m)
            prev = 0.0
            Li = L[i]
            for t in range(m):
                prev = Li[t] + rho * prev
                g[t] = prev
            acc += np.log(np.maximum(g, 1e-300))
        K = np.arange(1, m + 1)
        lognorm = np.log(np.maximum(1.0 - rho ** K, 1e-300)) - np.log(1.0 - rho)
        logp[j] = acc - n * lognorm
    return taus, D.years, logp


def tau_posterior_fast(D, tau_max=800, tau_min=1):
    """Vectorised version of tau_posterior (scipy lfilter over the date axis)."""
    from scipy.signal import lfilter
    L = np.maximum(D.Lmix, 1e-300)
    n, m = L.shape
    taus = np.arange(tau_min, tau_max + 1)
    logp = np.empty((len(taus), m))
    for j, tau in enumerate(taus):
        rho = np.exp(-1.0 / tau)
        g = lfilter([1.0], [1.0, -rho], L, axis=1)
        # w(t) must be normalised ON THE 1-YEAR GRID, not in the continuum:
        # sum_{s<=t_b} rho^{t_b-s} = (1-rho^K)/(1-rho) -> 1/(1-rho) for a long grid.
        # Using the continuum 1/tau instead injects a spurious tau^-n that drives
        # tau -> 0 and silently turns the phase model into an R_Combine.
        K = np.arange(1, m + 1)
        lognorm = np.log(np.maximum(1.0 - rho ** K, 1e-300)) - np.log(1.0 - rho) \
            if rho < 1 else np.log(K)
        logp[j] = np.log(np.maximum(g, 1e-300)).sum(axis=0) - n * lognorm
    return taus, D.years, logp


def uniform_posterior(D, max_span=900):
    """Joint posterior over (span, t_b) for the Boundary..Boundary model."""
    L = np.maximum(D.Lmix, 1e-300)
    n, m = L.shape
    C = np.concatenate([np.zeros((n, 1)), np.cumsum(L, axis=1)], axis=1)  # C[:,k]=sum_{t<k}
    spans = np.arange(1, max_span + 1)
    logp = np.full((len(spans), m), -np.inf)
    for j, sp in enumerate(spans):
        hi = np.arange(m)                      # index of t_b
        lo = hi - sp
        ok = lo >= 0
        s = np.zeros(m)
        s[ok] = C[:, hi[ok] + 1].sum(axis=0) * 0  # placeholder, filled below
        # per-date sum over [lo, hi]
        acc = np.zeros(m)
        for i in range(n):
            seg = np.full(m, 1e-300)
            seg[ok] = C[i, hi[ok] + 1] - C[i, lo[ok]]
            acc += np.log(np.maximum(seg, 1e-300))
        logp[j] = np.where(ok, acc - n * np.log(sp + 1.0), -np.inf)
    return spans, D.years, logp


def marginal_end(taus_or_spans, years, logp):
    """Marginalise the span/tau axis -> posterior over the end boundary."""
    lp = _logsum(logp, axis=0)
    p = np.exp(lp - lp.max())
    return years, p / p.sum()


def marginal_span(taus_or_spans, years, logp):
    lp = _logsum(logp, axis=1)
    p = np.exp(lp - lp.max())
    return taus_or_spans, p / p.sum()


def hpd_years(years, p, level=0.683):
    order = np.argsort(p)[::-1]
    c = np.cumsum(p[order]); k = int(np.searchsorted(c, level)) + 1
    keep = np.zeros(len(p), bool); keep[order[:k]] = True
    out, i = [], 0
    while i < len(p):
        if keep[i]:
            j = i
            while j + 1 < len(p) and keep[j + 1]:
                j += 1
            out.append((1 - years[i], 1 - years[j], p[i:j + 1].sum()))
            i = j + 1
        else:
            i += 1
    return out


def fmt(regions, minmass=0.0):
    return ", ".join("%d-%d BCE (%.1f%%)" % (a, b, 100 * m)
                     for a, b, m in regions if m >= minmass)


def median_bce(years, p):
    c = np.cumsum(p)
    return 1 - float(np.interp(0.5, c, years))


def tau_outlier_probs(D, taus, years, logp, tau_max=None):
    """Posterior outlier probability per date under the tau model.

    P(o_i=1 | data) = E_{tau,t_b} [ q * <Lout_i> / <Lmix_i> ], where <.> is the
    within-group prior average at (tau, t_b). Comparable directly with the
    per-date outlier probabilities OxCal reports.
    """
    from scipy.signal import lfilter
    L = np.maximum(D.Lmix, 1e-300)
    Lo = np.maximum(D.Lout, 1e-300)
    n, m = L.shape
    w = np.exp(logp - logp.max()); w /= w.sum()
    acc = np.zeros(n)
    for j, tau in enumerate(taus):
        if w[j].sum() < 1e-12:
            continue
        rho = np.exp(-1.0 / tau)
        gm = lfilter([1.0], [1.0, -rho], L, axis=1)
        go = lfilter([1.0], [1.0, -rho], Lo, axis=1)
        ratio = D.q * go / np.maximum(gm, 1e-300)
        acc += (ratio * w[j][None, :]).sum(axis=1)
    return acc
