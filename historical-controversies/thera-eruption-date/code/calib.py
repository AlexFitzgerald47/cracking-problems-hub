"""
c14lib -- a from-scratch radiocarbon calibration and Bayesian-model engine.

Written for the Cracking Problems Hub, thera-eruption-date, 2026-09-22.
No dependency on OxCal / BCal / rcarbon. numpy + scipy only.

Conventions follow Stuiver & Reimer (1993) / Bronk Ramsey (2008,2009):

  For a determination (r, s) -- conventional radiocarbon age +- 1 sigma --
  and a calibration curve giving (mu(t), sigma(t)) on calendar year t (cal BP):

      L(t) = N(r ; mu(t), s^2 + sigma(t)^2)

  and the posterior on a calendar interval is p(t) ~ prior(t) * L(t).
  With a uniform prior this is the standard "single-date calibration".

Calendar convention: internally cal BP (BP = before 1950). Reported as BC
where BC_year = cal_BP - 1949  (1 cal BP = AD 1949; 1950 cal BP = 1 BC;
there is no year zero, so cal BP 1950 -> 1 BC, cal BP 3550 -> 1601 BC).
Helper: bp_to_bc(x) = x - 1949.
"""
import numpy as np


# ----------------------------------------------------------------- curve io
def load_curve(path):
    """Read an IntCal .14c file -> (calbp, c14age, c14err), ascending calbp."""
    cal, age, err = [], [], []
    with open(path, encoding="latin-1") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            cal.append(float(parts[0]))
            age.append(float(parts[1]))
            err.append(float(parts[2]))
    cal = np.array(cal); age = np.array(age); err = np.array(err)
    o = np.argsort(cal)
    return cal[o], age[o], err[o]


class Curve:
    """Calibration curve, linearly interpolated to a 1-year cal BP grid."""

    def __init__(self, path, name=None):
        self.name = name or path
        c, a, e = load_curve(path)
        self.raw_spacing = float(np.median(np.diff(c)))
        self.grid = np.arange(int(np.ceil(c.min())), int(np.floor(c.max())) + 1)
        self.mu = np.interp(self.grid, c, a)
        self.sd = np.interp(self.grid, c, e)

    def window(self, lo, hi):
        """Boolean index into the 1-year grid for cal BP in [lo, hi]."""
        return (self.grid >= lo) & (self.grid <= hi)


# ----------------------------------------------------------- likelihoods
def loglik(curve, r, s, idx=None):
    """log N(r ; mu(t), s^2+sigma(t)^2) over the curve grid (or a sub-index)."""
    mu = curve.mu if idx is None else curve.mu[idx]
    sd = curve.sd if idx is None else curve.sd[idx]
    v = s * s + sd * sd
    return -0.5 * np.log(2 * np.pi * v) - (r - mu) ** 2 / (2 * v)


def calibrate(curve, r, s, lo=None, hi=None):
    """Single determination, uniform prior. Returns (calbp_grid, density)."""
    if lo is None:
        lo, hi = curve.grid.min(), curve.grid.max()
    idx = curve.window(lo, hi)
    ll = loglik(curve, r, s, idx)
    p = np.exp(ll - ll.max())
    p /= p.sum()
    return curve.grid[idx], p


# ---------------------------------------------------------------- summaries
def hpd(x, p, level=0.954):
    """Highest-posterior-density region -> list of (lo, hi, mass), x ascending."""
    order = np.argsort(p)[::-1]
    csum = np.cumsum(p[order])
    k = int(np.searchsorted(csum, level)) + 1
    keep = np.zeros_like(p, dtype=bool)
    keep[order[:k]] = True
    out, i, n = [], 0, len(x)
    while i < n:
        if keep[i]:
            j = i
            while j + 1 < n and keep[j + 1]:
                j += 1
            out.append((float(x[i]), float(x[j]), float(p[i:j + 1].sum())))
            i = j + 1
        else:
            i += 1
    return out


def bp_to_bc(x):
    """cal BP -> BC (positive number = years BC). No year zero."""
    return x - 1949.0


def hpd_bc(x, p, level=0.954):
    """HPD reported as BC, oldest first, as (start_BC, end_BC, mass)."""
    out = []
    for lo, hi, m in hpd(x, p, level):
        out.append((bp_to_bc(hi), bp_to_bc(lo), m))
    out.sort(key=lambda t: -t[0])
    return out


def fmt_bc(regions, digits=0):
    return ", ".join(
        "%d-%d BC (%.1f%%)" % (round(a), round(b), 100 * m) for a, b, m in regions
    )


def median_bc(x, p):
    c = np.cumsum(p)
    return bp_to_bc(float(np.interp(0.5, c, x)))


# ------------------------------------------------------------- combination
def r_combine(curve, dets, lo=None, hi=None):
    """
    OxCal R_Combine: dets are (r,s) assumed to date the SAME calendar year.
    Returns (grid, density, chi2, df, pooled_r, pooled_s).
    """
    r = np.array([d[0] for d in dets], float)
    s = np.array([d[1] for d in dets], float)
    w = 1.0 / s ** 2
    rbar = float((w * r).sum() / w.sum())
    sbar = float(np.sqrt(1.0 / w.sum()))
    chi2 = float((w * (r - rbar) ** 2).sum())
    df = len(dets) - 1
    g, p = calibrate(curve, rbar, sbar, lo, hi)
    return g, p, chi2, df, rbar, sbar


def phase_posterior(curve, dets, lo, hi, n_iter=200000, seed=0, prior="uniform"):
    """
    Placeholder kept for API symmetry; the real sampler lives in phase.py.
    """
    raise NotImplementedError
