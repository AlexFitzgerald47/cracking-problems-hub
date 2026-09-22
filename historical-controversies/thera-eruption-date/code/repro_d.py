import sys, numpy as np
sys.path.insert(0, 'code')
from calib import Curve
from parse_oxcal import blocks, dates
from oxmodel import Dates
from exact import tau_posterior_fast, marginal_end, marginal_span, hpd_years, fmt, median_bce

c = Curve('data/intcal20.14c')
ds = dates(blocks('data/manning2022_S2_oxcal_runfiles.txt')['d'])
print('dataset (d): n=%d' % len(ds))
D = Dates(c, ds, -2400, -1000, q_outlier=0.05, n_mc=20000, seed=11)
taus, yrs, lp = tau_posterior_fast(D, tau_max=800)
y, p = marginal_end(taus, yrs, lp)
print('  68.3%%: %s' % fmt(hpd_years(y, p, 0.683)))
print('  95.4%%: %s' % fmt(hpd_years(y, p, 0.954)))
print('  median %.0f BCE' % median_bce(y, p))
print('  PUBLISHED: 1607-1579 (34.5%), 1577-1554 (25.0%), 1553-1545 (8.7%) | 1613-1517 (95.4%)')

from exact import tau_outlier_probs
op = tau_outlier_probs(D, taus, yrs, lp)
print('\n  posterior outlier probabilities (this engine) vs Manning S1 File:')
pub = {'P-1697': 91, 'P-1888': 77, 'ETH-3315': 57, 'DEM-1607': 19, 'P-2794': 22,
       'Hd-6059-7967': 19}
for i in np.argsort(op)[::-1][:12]:
    nm = ds[i][0].split()[0]
    hit = ''
    for k, v in pub.items():
        if nm.startswith(k):
            hit = '   <-- Manning: ~%d%%' % v
    print('    %-26s %5.1f%%%s' % (ds[i][0][:26], 100 * op[i], hit))
