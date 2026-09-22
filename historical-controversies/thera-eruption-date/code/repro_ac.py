"""Reproduce Manning (2022) standalone datasets (a) and (c), and (a)+(c).

(a)  Tau_Boundary("TnoT") .. Phase{ non-Thera samples tied to the eruption } .. Boundary("EnoT")
     One phase element is the felling date of the Miletos oak, itself a
     D_Sequence wiggle match of 7 ring groups with Gap(10) and Gap(7) to the
     waney edge. Another is an R_Combine of the two Trianda twig dates.
(c)  Boundary("Start") .. Sequence{4 Friedrich olive segments, ORDER ONLY, no
     ring counts} .. Boundary("EOlive"), and in parallel
     Tau_Boundary("Tolive") .. Phase{14 other olive/root dates} .. Boundary("=EOlive"),
     the two sharing one end-boundary parameter.

Published (Fig 7A):
  (a)   1602-1555 (68.3%)   1606-1528 (95.4%)
  (c)   1610-1558 (68.3%)   1613-1525 (95.4%)
  (a+c) 1603-1561 (68.3%)   1607-1534 (95.4%)
"""
import sys, numpy as np
sys.path.insert(0, 'code')
from scipy.signal import lfilter
from calib import Curve
from oxmodel import Dates, cal_to_year
from exact import hpd_years, fmt, median_bce, _logsum

LO, HI = -2400, -1000
C = Curve('data/intcal20.14c')


def pool(dets):
    w = sum(1 / s ** 2 for _, s in dets)
    return sum(r / s ** 2 for r, s in dets) / w, (1 / w) ** 0.5


# ---- dataset (a) elements -------------------------------------------------
MILETOS = [  # (ring group, [(bp,sd)...], years before the waney-edge felling)
    ([(3439, 30), (3386, 31)], 67), ([(3467, 31), (3385, 34)], 57),
    ([(3404, 31), (3459, 31)], 47), ([(3416, 31), (3425, 31)], 37),
    ([(3361, 31), (3397, 32)], 27), ([(3345, 32), (3397, 32)], 17),
    ([(3388, 30), (3352, 31)], 7)]
A_SIMPLE = [('DEM-94', 3347, 46), ('DEM-93', 3358, 48),
            ('GrA-30336', 3310, 35), ('GrA-30339', 3390, 35),
            ('GrA-28991', 3325, 40), ('GrA-29041', 3345, 40), ('GrA-29042', 3385, 40),
            ('OxA-38858', 3275, 17), ('OxA-38881', 3367, 22), ('OxA-38973', 3318, 19),
            ('OxA-38972', 3316, 20), ('OxA-38857', 3312, 17), ('OxA-38950', 3384, 22),
            ('D-AMS019172', 3372, 27), ('OxA-38966', 3297, 19), ('D-AMS019173', 3291, 30),
            ('Lyon7920', 3295, 30)]
A_TRIANDA = pool([(3367, 39), (3344, 32)])

C_FRIEDRICH = [('Hd-23599-24426', 3383, 11), ('Hd-23587', 3372, 12),
               ('Hd-23589', 3349, 12), ('Hd-23588-24402', 3331, 10)]
C_PUMICE = [('VERA-5614', 3282, 21), ('VERA-5614HS', 3359, 33),
            ('VERA-5615', 3280, 24), ('VERA-5615HS', 3321, 24),
            ('VERA-5620', 3277, 25), ('VERA-5620HS', 3345, 24),
            ('VERA-5610', 3399, 25), ('VERA-5610HS', 3342, 26),
            ('VERA-5083', 3270, 36), ('VERA-5083HS', 3326, 77),
            ('VERA-5082', 3332, 38), ('VERA-5082HS', 3369, 36),
            ('VERA-5084', 3354, 32), ('VERA-5084HS', 3368, 34)]


def miletos_felling(q=0.05):
    """Likelihood of the felling year from the Miletos D_Sequence."""
    grps = [(pool(g)[0], pool(g)[1], off) for g, off in MILETOS]
    D = Dates(C, [('m%d' % k, r, s) for k, (r, s, _) in enumerate(grps)], LO, HI, q_outlier=q)
    m = len(D.years)
    tot = np.zeros(m)
    for k, (_, _, off) in enumerate(grps):
        L = D.Lmix[k]
        sh = np.full(m, 1e-300)                 # L_k(f - off)
        sh[off:] = L[:m - off]
        tot += np.log(np.maximum(sh, 1e-300))
    tot -= tot.max()
    return np.exp(tot)


def tau_phase_loglik(Lmix, taus, m):
    """log prod_i <L_i>_(tau,t_b) for a Tau_Boundary..Boundary phase."""
    n = Lmix.shape[0]
    out = np.empty((len(taus), m))
    K = np.arange(1, m + 1)
    for j, tau in enumerate(taus):
        rho = np.exp(-1.0 / tau)
        g = lfilter([1.0], [1.0, -rho], np.maximum(Lmix, 1e-300), axis=1)
        lognorm = np.log(np.maximum(1.0 - rho ** K, 1e-300)) - np.log(1.0 - rho)
        out[j] = np.log(np.maximum(g, 1e-300)).sum(axis=0) - n * lognorm
    return out


def end_posterior_tau(Lmix, years, tau_max=800):
    taus = np.arange(1, tau_max + 1)
    lp = tau_phase_loglik(Lmix, taus, len(years))
    l = _logsum(lp, axis=0)
    p = np.exp(l - l.max())
    return p / p.sum(), l


def report(name, years, p, published):
    print('%-8s 68.3%%: %-52s' % (name, fmt(hpd_years(years, p, 0.683))))
    print('         95.4%%: %-52s' % fmt(hpd_years(years, p, 0.954)))
    print('         median %.0f BCE   PUBLISHED %s' % (median_bce(years, p), published))


if __name__ == '__main__':
    # ---------------- dataset (a)
    dets_a = list(A_SIMPLE) + [('Trianda R_Combine', int(round(A_TRIANDA[0])),
                               int(round(A_TRIANDA[1])))]
    Da = Dates(C, dets_a, LO, HI, q_outlier=0.05)
    fell = miletos_felling()
    La = np.vstack([Da.Lmix, fell[None, :]])
    pa, la = end_posterior_tau(La, Da.years)
    report('(a)', Da.years, pa, '1602-1555 (68.3%) | 1606-1528 (95.4%)')

    # ---------------- dataset (c): ordered Friedrich sequence + tau phase, shared end
    Dfr = Dates(C, C_FRIEDRICH, LO, HI, q_outlier=0.05)
    m = len(Dfr.years)
    # Boundary("Start") .. ordered Sequence of 4 .. Boundary("EOlive") is a
    # UNIFORM-span group with an ordering constraint, so the prior carries a
    # (t_b-t_a)^-4 factor. Marginalising it needs the full 2-D (t_a,t_b) sweep:
    # dropping it (a bare cumulative integral) removes the penalty on EOlive
    # sitting far above the youngest ring segment and drags the boundary ~40
    # years too young -- the first version of this script did exactly that.
    Lf = np.maximum(Dfr.Lmix, 1e-300)
    l_seq = np.full(m, -np.inf)
    acc = np.full(m, -np.inf)
    for ia in range(0, m - 5):
        F = np.zeros(m)
        F[ia:] = 1.0
        for k in range(4):
            F = np.cumsum(Lf[k] * F)
            F[:ia] = 0.0
        span = np.arange(m) - ia
        with np.errstate(divide='ignore', invalid='ignore'):
            lz = np.where(span > 0, np.log(np.maximum(F, 1e-300)) - 4 * np.log(np.maximum(span, 1)), -np.inf)
        acc = np.logaddexp(acc, lz)
    l_seq = acc

    Dp = Dates(C, C_PUMICE, LO, HI, q_outlier=0.05)
    taus = np.arange(1, 801)
    l_pum = _logsum(tau_phase_loglik(Dp.Lmix, taus, m), axis=0)
    l_c = l_pum + l_seq
    pc = np.exp(l_c - l_c.max()); pc /= pc.sum()
    report('(c)', Dfr.years, pc, '1610-1558 (68.3%) | 1613-1525 (95.4%)')

    # ---------------- dataset (a)+(c): all of (a) and (c) in one phase -> product
    l_ac = la + l_c
    pac = np.exp(l_ac - l_ac.max()); pac /= pac.sum()
    report('(a+c)', Dfr.years, pac, '1603-1561 (68.3%) | 1607-1534 (95.4%)')
