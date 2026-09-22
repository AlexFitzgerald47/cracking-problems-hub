"""
Power analysis: can the Thera radiocarbon evidence, at its actual size and
precision, recover a known eruption year?

The literature argues about which century the eruption falls in. Nobody in it
appears to have asked the prior question: if the eruption HAD happened in year
T, would this dataset, run through this model, return T? That is answerable by
simulation, and the answer bounds everything else.

Procedure, for each candidate true year T:
  1. draw n sample calendar years from the fitted within-phase prior
     (exponential rising to T with the time constant the real data support),
  2. draw a 14C age for each from N(mu(t), sigma_lab^2 + sigma_curve(t)^2),
     recycling the actual 1-sigma errors of the real dataset,
  3. run exactly the model Manning runs (Tau_Boundary .. Phase .. Boundary,
     IntCal20), and record the posterior median and 95.4% HPD of the end
     boundary.

Everything except the true year is held at the real dataset's values, so the
spread of recovered years is the dataset's own resolving power.
"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from scipy.signal import lfilter
from calib import Curve
from exact import _logsum, hpd_years


class Sim:
    def __init__(self, curve, lo=-1900, hi=-1300, tau_max=300, seed=0):
        self.c = curve
        self.years = np.arange(lo, hi + 1)
        cal = 1950 - self.years                      # cal BP for each year
        idx = np.searchsorted(curve.grid, cal)
        self.mu = curve.mu[idx]
        self.sd = curve.sd[idx]
        self.taus = np.arange(1, tau_max + 1)
        self.m = len(self.years)
        self.rng = np.random.default_rng(seed)
        self.K = np.arange(1, self.m + 1)

    def loglik_curves(self, r, s):
        v = s[:, None] ** 2 + self.sd[None, :] ** 2
        return np.exp(-0.5 * (r[:, None] - self.mu[None, :]) ** 2 / v) / np.sqrt(v)

    def end_posterior(self, r, s):
        L = np.maximum(self.loglik_curves(r, s), 1e-300)
        n = L.shape[0]
        lp = np.empty((len(self.taus), self.m))
        for j, tau in enumerate(self.taus):
            rho = np.exp(-1.0 / tau)
            g = lfilter([1.0], [1.0, -rho], L, axis=1)
            lognorm = np.log(np.maximum(1.0 - rho ** self.K, 1e-300)) - np.log(1.0 - rho)
            lp[j] = np.log(np.maximum(g, 1e-300)).sum(axis=0) - n * lognorm
        l = _logsum(lp, axis=0)
        p = np.exp(l - l.max())
        return p / p.sum()

    def draw(self, T, sigmas, tau_true):
        """Sample calendar years from the exponential phase ending at T, then 14C ages."""
        n = len(sigmas)
        off = self.rng.exponential(tau_true, n)
        t = np.rint(T - off).astype(int)
        t = np.clip(t, self.years[0], self.years[-1])
        k = t - self.years[0]
        r = self.rng.normal(self.mu[k], np.sqrt(np.asarray(sigmas) ** 2 + self.sd[k] ** 2))
        return r, np.asarray(sigmas, float)


def median_bce(years, p):
    return 1 - float(np.interp(0.5, np.cumsum(p), years))
