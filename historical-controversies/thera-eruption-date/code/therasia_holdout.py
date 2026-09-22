"""
Out-of-sample test: the Therasia olive shrub.

Pearson, Sbonias, Tzachili & Heaton (2023) Sci Rep 13:6994,
doi 10.1038/s41598-023-33696-w, Table 1 (nine determinations, verified against
the journal's own table HTML on 2026-09-22 and stored in
data/pearson2023_therasia.csv).

These postdate Manning (2022) and are in none of his datasets, so they are a
genuine holdout for anything fitted to his data. The shrub was carbonised in
place by the eruption, so its OUTERMOST material dates the eruption directly,
with at most a few years of in-built age -- the inner material is older by the
shrub's own age and is not a death estimate.

The question asked here is deliberately narrow and is the one the calibration
can actually answer: which of the candidate eruption years does the outermost
Therasia material support, and by how much?
"""
import sys, csv, numpy as np
sys.path.insert(0, 'code')
from calib import Curve, calibrate, hpd_bc, fmt_bc, median_bc
from scipy.stats import chi2 as chi2dist

c = Curve('data/intcal20.14c')
rows = list(csv.DictReader(open('data/pearson2023_therasia.csv')))
for r in rows:
    r['c14bp'] = float(r['c14bp']); r['sd'] = float(r['sd'])

OUTER = [r for r in rows if r['part'] in ('outer', 'bark')]
INNER = [r for r in rows if r['part'] == 'inner']


def pooled(rs):
    w = sum(1 / r['sd'] ** 2 for r in rs)
    m = sum(r['c14bp'] / r['sd'] ** 2 for r in rs) / w
    s = (1 / w) ** 0.5
    x2 = sum((r['c14bp'] - m) ** 2 / r['sd'] ** 2 for r in rs)
    return m, s, x2, len(rs) - 1


for label, rs in [('outermost + bark (n=%d)' % len(OUTER), OUTER),
                  ('inner (n=%d)' % len(INNER), INNER),
                  ('all nine', rows)]:
    m, s, x2, df = pooled(rs)
    print('%-24s pooled %7.1f +- %4.1f   chi2 %5.1f / %d df  p=%.3f' %
          (label, m, s, x2, df, chi2dist.sf(x2, df)))

m, s, _, _ = pooled(OUTER)
print('\nCalibration of the pooled outermost Therasia material (%.0f +- %.0f, IntCal20):' % (m, s))
g, p = calibrate(c, m, s, 3100, 3900)
print('   68.3%%: %s' % fmt_bc(hpd_bc(g, p, 0.683)))
print('   95.4%%: %s' % fmt_bc(hpd_bc(g, p, 0.954)))
print('   Pearson et al. 2023 published for 88-2/88-3 outermost: 1610-1510 BCE (95.4%)')

print('\nSupport of the Therasia outermost material for each candidate eruption year')
print('(z = (pooled - curve(T)) / sqrt(s^2 + sigma_curve(T)^2); log Bayes factor')
print(' is relative to the best-supported year on the grid)')
best = None
res = []
for T in [1650, 1640, 1630, 1620, 1610, 1600, 1590, 1580, 1570, 1560, 1550,
          1540, 1530, 1520, 1510, 1500]:
    i = int(np.where(c.grid == T + 1949)[0][0])
    mu, sc = c.mu[i], c.sd[i]
    v = s * s + sc * sc
    z = (m - mu) / np.sqrt(v)
    ll = -0.5 * z * z - 0.5 * np.log(v)
    res.append((T, mu, z, ll))
mx = max(r[3] for r in res)
for T, mu, z, ll in res:
    bar = '#' * int(round(20 * np.exp(ll - mx)))
    print('   %4d BCE  curve %4.0f  z = %+5.2f   lnBF %6.2f  %s' % (T, mu, z, ll - mx, bar))
