"""
How much of the published eruption date is the data, and how much is the prior?

Manning (2022) models every Thera phase with a Tau_Boundary .. Boundary pair --
an exponential distribution of dated events rising to the terminating event.
That choice is argued for in the paper but its influence on the answer is not
quantified anywhere. Here the same data are run through four within-phase
priors and two calibration curves, with everything else held fixed.

  tau      Tau_Boundary .. Boundary   (Manning's choice; exponential rise)
  uniform  Boundary .. Boundary       (the standard Buck et al. 1992 phase)
  zero     Zero_Boundary .. Boundary  (linear rise from zero)
  combine  R_Combine                  (all samples date one calendar year)
"""
import sys, numpy as np
sys.path.insert(0, 'code')
from scipy.signal import lfilter
from calib import Curve
from parse_oxcal import blocks, dates
from oxmodel import Dates
from exact import _logsum, hpd_years, fmt, median_bce


def end_tau(L, m, tau_max=800):
    n = L.shape[0]; K = np.arange(1, m + 1)
    lp = np.empty((tau_max, m))
    for j in range(1, tau_max + 1):
        rho = np.exp(-1.0 / j)
        g = lfilter([1.0], [1.0, -rho], L, axis=1)
        ln = np.log(np.maximum(1.0 - rho ** K, 1e-300)) - np.log(1.0 - rho)
        lp[j - 1] = np.log(np.maximum(g, 1e-300)).sum(axis=0) - n * ln
    return _logsum(lp, axis=0)


def end_uniform(L, m, max_span=900):
    n = L.shape[0]
    C = np.concatenate([np.zeros((n, 1)), np.cumsum(L, axis=1)], axis=1)
    out = np.full((max_span, m), -np.inf)
    hi = np.arange(m)
    for j, sp in enumerate(range(1, max_span + 1)):
        lo = hi - sp; ok = lo >= 0
        acc = np.zeros(m)
        for i in range(n):
            seg = np.full(m, 1e-300)
            seg[ok] = C[i, hi[ok] + 1] - C[i, lo[ok]]
            acc += np.log(np.maximum(seg, 1e-300))
        out[j] = np.where(ok, acc - n * np.log(sp + 1.0), -np.inf)
    return _logsum(out, axis=0)


def end_zero(L, m, max_span=900):
    """w(t) proportional to (t - t_a) on [t_a, t_b]; normalised on the grid."""
    n = L.shape[0]
    out = np.full((max_span, m), -np.inf)
    hi = np.arange(m)
    for j, sp in enumerate(range(2, max_span + 2)):
        ramp = np.arange(sp + 1, dtype=float)          # 0 .. sp
        ramp /= ramp.sum()
        acc = np.zeros(m)
        ok = hi - sp >= 0
        for i in range(n):
            conv = np.convolve(L[i], ramp[::-1], mode='full')[:m]
            seg = np.where(ok, conv, 1e-300)
            acc += np.log(np.maximum(seg, 1e-300))
        out[j] = np.where(ok, acc, -np.inf)
    return _logsum(out, axis=0)


def end_combine(L):
    return np.log(np.maximum(L, 1e-300)).sum(axis=0)


def norm(l):
    p = np.exp(l - l.max()); return p / p.sum()


if __name__ == '__main__':
    bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')
    LO, HI = -2400, -1000
    for curve_file, cname in [('data/intcal20.14c', 'IntCal20'),
                              ('data/intcal13.14c', 'IntCal13')]:
        c = Curve(curve_file)
        for dsname in ['b', 'd']:
            ds = dates(bl[dsname])
            D = Dates(c, ds, LO, HI, q_outlier=0.05)
            m = len(D.years)
            print('\n### dataset (%s), n=%d, %s' % (dsname, D.n, cname))
            for kind, fn in [('tau      (Manning)', lambda L: end_tau(L, m)),
                             ('uniform           ', lambda L: end_uniform(L, m)),
                             ('zero              ', lambda L: end_zero(L, m)),
                             ('combine           ', lambda L: end_combine(L))]:
                p = norm(fn(np.maximum(D.Lmix, 1e-300)))
                r68 = hpd_years(D.years, p, 0.683)
                r95 = hpd_years(D.years, p, 0.954)
                print('  %s med %4.0f | 68.3%%: %-44s | 95.4%%: %s' %
                      (kind, median_bce(D.years, p), fmt(r68), fmt(r95)))
            # outlier model off
            D2 = Dates(c, ds, LO, HI, outliers=False)
            p = norm(end_tau(np.maximum(D2.Lmix, 1e-300), m))
            print('  tau, NO outlier mdl med %4.0f | 68.3%%: %-44s | 95.4%%: %s' %
                  (median_bce(D2.years, p), fmt(hpd_years(D2.years, p, 0.683)),
                   fmt(hpd_years(D2.years, p, 0.954))))
