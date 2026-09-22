"""Reproduction check: Manning (2022) standalone dataset (b), Akrotiri VDL stages (ii)/(iii).

Published (PLOS ONE 17(9):e0274835, Fig 7A, OxCal v4.4.4, IntCal20):
   E2/3 boundary = 1615-1583 BCE (57.0%), 1571-1560 BCE (11.3%)   [68.3% total]
                   1618-1537 BCE (95.4%)
Model in Manning's own runfile (Table S2, dataset (b)):
   Tau_Boundary("Stages 2/3"); Phase{31 R_Dates, Outlier General 0.05}; Boundary("E2/3")
"""
import sys, time, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from calib import Curve
from parse_oxcal import blocks, dates
from oxmodel import Dates, run_phase, hpd_from_samples, fmt

c = Curve('data/intcal20.14c', 'IntCal20')
bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')
ds = dates(bl['b'])
print('dataset (b): %d determinations, pooled mean %.1f' %
      (len(ds), sum(d[1] / d[2] ** 2 for d in ds) / sum(1 / d[2] ** 2 for d in ds)))

LO, HI = -2400, -1000
t0 = time.time()
D = Dates(c, ds, LO, HI, q_outlier=0.05, n_mc=20000, seed=11)
print('likelihoods built in %.1fs' % (time.time() - t0))

for kind in ['tau', 'uniform']:
    t0 = time.time()
    r = run_phase(D, kind=kind, n_iter=40000, burn=5000, thin=4, seed=7)
    e = r['end']
    print('\n--- %s boundary  (%.0fs, %d kept)' % (kind, time.time() - t0, r['n_kept']))
    print('   68.3%%: %s' % fmt(hpd_from_samples(e, 0.683)))
    print('   95.4%%: %s' % fmt(hpd_from_samples(e, 0.954)))
    print('   median %d BCE   mean %d BCE' % (1 - int(np.median(e)), 1 - int(e.mean())))
    if r['outlier_p'] is not None:
        top = np.argsort(r['outlier_p'])[::-1][:4]
        print('   top outlier probs: ' + ', '.join(
            '%s %.0f%%' % (ds[i][0].split()[0], 100 * r['outlier_p'][i]) for i in top))
