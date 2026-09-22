import sys, time, numpy as np
sys.path.insert(0, 'code')
from calib import Curve
from parse_oxcal import blocks, dates
from oxmodel import Dates
from exact import tau_posterior_fast, uniform_posterior, marginal_end, marginal_span, hpd_years, fmt, median_bce

c = Curve('data/intcal20.14c')
ds = dates(blocks('data/manning2022_S2_oxcal_runfiles.txt')['b'])
D = Dates(c, ds, -2400, -1000, q_outlier=0.05, n_mc=20000, seed=11)
print('dataset (b): n=%d' % D.n)
t0 = time.time()
taus, yrs, lp = tau_posterior_fast(D, tau_max=600)
y, p = marginal_end(taus, yrs, lp)
print('tau model  (%.0fs)' % (time.time() - t0))
print('  68.3%%: %s' % fmt(hpd_years(y, p, 0.683)))
print('  95.4%%: %s' % fmt(hpd_years(y, p, 0.954)))
print('  median %.0f BCE' % median_bce(y, p))
tg, tp = marginal_span(taus, yrs, lp)
print('  tau posterior: median %.0f yr, 95%% [%.0f, %.0f]' % (
    np.interp(0.5, np.cumsum(tp), tg), np.interp(0.025, np.cumsum(tp), tg),
    np.interp(0.975, np.cumsum(tp), tg)))
print('  PUBLISHED   : 1615-1583 (57.0%), 1571-1560 (11.3%) | 1618-1537 (95.4%)')
