"""Test the predictions frozen in analysis/2026-09-22-FROZEN-PREDICTIONS.md.

Run after the reproduction check in code/repro_*.py has passed.
"""
import sys, numpy as np
sys.path.insert(0, 'code')
from calib import Curve, calibrate, hpd_bc, fmt_bc, median_bc, r_combine
from parse_oxcal import blocks, dates

c20 = Curve('data/intcal20.14c')
c13 = Curve('data/intcal13.14c')
bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')
b = dates(bl['b'])
LO, HI = 3100, 3900          # cal BP window

print('=' * 78)
print('P1  pooled mean of the Akrotiri VDL short-lived set (predicted 3320-3365)')
w = sum(1 / d[2] ** 2 for d in b)
rbar = sum(d[1] / d[2] ** 2 for d in b) / w
sbar = (1 / w) ** 0.5
chi2 = sum((d[1] - rbar) ** 2 / d[2] ** 2 for d in b)
print('    n=%d  pooled %.1f +- %.1f 14C yr   chi2=%.1f on %d df (p=%.2g)' %
      (len(b), rbar, sbar, chi2, len(b) - 1,
       __import__('scipy.stats', fromlist=['chi2']).chi2.sf(chi2, len(b) - 1)))
print('    Manning et al. 2006 published VDL weighted average: 3344.9 +- 7.5')
print('    VERDICT: %s' % ('HOLDS' if 3320 <= rbar <= 3365 else 'FAILS'))

print()
print('=' * 78)
print('P2  a single VDL determination spans >=90 yr at 95.4% and contains 1620 and 1560 BCE')
fails = 0
mod = [d for d in b if d[2] <= 35]
for name, r, s in mod[:8] + [('pooled', int(round(rbar)), max(1, int(round(sbar))))]:
    g, p = calibrate(c20, r, s, LO, HI)
    reg = hpd_bc(g, p, 0.954)
    span = sum(a - bb + 1 for a, bb, _ in reg)
    has20 = any(bb <= 1620 <= a for a, bb, _ in reg)
    has60 = any(bb <= 1560 <= a for a, bb, _ in reg)
    ok = span >= 90 and has20 and has60
    if name != 'pooled' and not ok:
        fails += 1
    print('    %-14s %4d+-%2d  span %3d yr  1620:%s 1560:%s   %s' %
          (name, r, s, span, 'Y' if has20 else 'n', 'Y' if has60 else 'n', fmt_bc(reg)))
print('    VERDICT: %s (%d/8 single dates failed the >=90yr + both-anchors test)' %
      ('HOLDS' if fails == 0 else 'FAILS', fails))

print()
print('=' * 78)
print('P3  R_Combine of the VDL set is multi-modal, and the mode split moves >20pp')
print('    when the pooled 14C mean shifts by +-15 14C yr')
for shift in (-15, -10, -5, 0, 5, 10, 15):
    g, p = calibrate(c20, rbar + shift, sbar, LO, HI)
    reg = hpd_bc(g, p, 0.954)
    old = sum(m for a, bb, m in reg if bb >= 1590)          # mass older than 1590 BCE
    young = sum(m for a, bb, m in reg if a < 1590)
    print('      pooled %+3d -> %7.1f BP : %-46s  older-than-1590 share %.2f' %
          (shift, rbar + shift, fmt_bc(reg), old / max(old + young, 1e-9)))

print()
print('=' * 78)
print('P6  information bound: d-prime for separating two candidate years')
def g(curve, bc):
    i = int(np.where(curve.grid == bc + 1949)[0][0]); return curve.mu[i], curve.sd[i]
print('    pair            1 det sigma=25   n=31 (indep-curve, optimistic)   ceiling (shared curve)')
for a, bb in [(1620, 1530), (1620, 1500), (1610, 1560), (1610, 1540), (1600, 1560),
              (1600, 1530), (1580, 1560), (1610, 1530)]:
    m1, s1 = g(c20, a); m2, s2 = g(c20, bb)
    d1 = abs(m1 - m2) / np.sqrt(25 ** 2 + 0.5 * (s1 ** 2 + s2 ** 2))
    print('    %4d vs %4d BCE      %5.2f            %6.2f                     %6.2f' %
          (a, bb, d1, d1 * np.sqrt(31), abs(m1 - m2) / np.sqrt(s1 ** 2 + s2 ** 2)))

print()
print('=' * 78)
print('P7  the Friedrich olive branch with and without its ring-count constraint')
OL = [('rings 1-13', 3383, 11), ('rings 14-37', 3372, 12),
      ('rings 38-59', 3349, 12), ('rings 60-72', 3331, 10)]
# (i) wiggle match: ring offsets from the outermost segment midpoint
mid = [6, 25, 48, 66]
off = [mid[-1] - x for x in mid]              # years before the outer segment midpoint
gg = np.arange(LO, HI + 1)
def like(r, s, shift):
    idx = c20.window(LO, HI)
    mu = c20.mu[idx]; sd = c20.sd[idx]
    mu2 = np.roll(mu, -shift); sd2 = np.roll(sd, -shift)
    v = s * s + sd2 ** 2
    return np.exp(-0.5 * (r - mu2) ** 2 / v) / np.sqrt(v)
lp = np.zeros(gg.shape)
for (nm, r, s), o in zip(OL, off):
    lp += np.log(np.maximum(like(r, s, o), 1e-300))
p = np.exp(lp - lp.max()); p /= p.sum()
reg = hpd_bc(gg, p, 0.954)
print('    WITH ring counts (D_Sequence, offsets %s):' % off)
print('      95.4%%: %s   span %d yr' % (fmt_bc(reg), sum(a - b + 1 for a, b, _ in reg)))
# (ii) order only, no ring counts: R_Combine is the wrong comparator; use the
#      simple pooled calibration of the outermost segment alone
g2, p2 = calibrate(c20, 3331, 10, LO, HI)
reg2 = hpd_bc(g2, p2, 0.954)
print('    outermost segment alone (3331+-10), no model at all:')
print('      95.4%%: %s   span %d yr' % (fmt_bc(reg2), sum(a - b + 1 for a, b, _ in reg2)))
print('    Friedrich et al. 2006 published (IntCal04, wiggle match): 1627-1600 BCE (2 sigma)')
