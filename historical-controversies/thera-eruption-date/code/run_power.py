import sys, time, numpy as np
sys.path.insert(0, 'code')
from calib import Curve
from parse_oxcal import blocks, dates
from power_sim import Sim, median_bce
from exact import hpd_years, fmt

c = Curve('data/intcal20.14c')
bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')
sig_b = [d[2] for d in dates(bl['b'])]                # real 1-sigma errors, n=31
S = Sim(c, seed=5)
TRUTHS = [1650, 1620, 1610, 1600, 1580, 1560, 1540, 1530, 1500]
NREP = 200
TAU_TRUE = 28                                          # posterior median from dataset (b)

print('Power of the dataset-(b) design (n=%d, real sigmas, tau=%d) under IntCal20' %
      (len(sig_b), TAU_TRUE))
print('true T | recovered median: mean   sd  |  P(|med-T|<=15) | P(1610 in 95.4%) P(1560 in 95.4%) | mean 95.4% width')
res = {}
for T in TRUTHS:
    meds, w, in1610, in1560 = [], [], 0, 0
    for _ in range(NREP):
        r, s = S.draw(-T + 1, sig_b, TAU_TRUE)
        p = S.end_posterior(r, s)
        meds.append(median_bce(S.years, p))
        hp = hpd_years(S.years, p, 0.954)
        w.append(sum(a - b + 1 for a, b, _ in hp))
        if any(b <= 1610 <= a for a, b, _ in hp): in1610 += 1
        if any(b <= 1560 <= a for a, b, _ in hp): in1560 += 1
    meds = np.array(meds); res[T] = meds
    print('%6d | %20.1f %5.1f | %14.2f | %16.2f %16.2f | %.0f' %
          (T, meds.mean(), meds.std(), np.mean(np.abs(meds - T) <= 15),
           in1610 / NREP, in1560 / NREP, np.mean(w)))
np.save('data/power_medians.npy', np.array([res[T] for T in TRUTHS]))
print('\nOverlap of the recovered-median distributions (fraction of simulated')
print('datasets from T1 whose recovered median is closer to T2 than to T1):')
for T1 in [1610, 1600, 1560]:
    row = []
    for T2 in TRUTHS:
        if T2 == T1: row.append('  --- '); continue
        row.append('%6.2f' % np.mean(np.abs(res[T1] - T2) < np.abs(res[T1] - T1)))
    print('  T=%4d ->' % T1, ' '.join(row), '  (cols %s)' % TRUTHS)
