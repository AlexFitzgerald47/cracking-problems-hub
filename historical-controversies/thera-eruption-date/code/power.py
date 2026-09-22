"""
Discriminating power of radiocarbon for the Thera dispute.

The question the eruption debate turns on is not "what is the calibrated date"
but "can these data separate candidate year A from candidate year B at all?".
That is a pure property of the calibration curve plus the measurement error,
and it can be computed before a single determination is looked at.

For two candidate calendar years t1, t2, a determination of precision s drawn
under t1 has expected log Bayes factor (t1 over t2)

    E[log BF] = (mu1-mu2)^2 / (2 * v)            with v = s^2 + sigma_curve^2
    Var[log BF] = (mu1-mu2)^2 / v

so the separation is governed by d = |mu1-mu2| / sqrt(v), the ordinary
two-Gaussian d-prime.  n independent determinations give d_n = d * sqrt(n)
(exactly, when the curve error is treated as independent per sample; see the
note in RESULTS about shared curve error, which makes this an UPPER bound on
the power).
"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from calib import Curve, bp_to_bc


def dprime(curve, bc1, bc2, s):
    i = int(np.where(curve.grid == bc1 + 1949)[0][0])
    j = int(np.where(curve.grid == bc2 + 1949)[0][0])
    v = s * s + 0.5 * (curve.sd[i] ** 2 + curve.sd[j] ** 2)
    return abs(curve.mu[i] - curve.mu[j]) / np.sqrt(v)


def n_needed(curve, bc1, bc2, s, target_d=3.0):
    """n determinations of precision s to reach d' = target (approx 3 = decisive)."""
    d = dprime(curve, bc1, bc2, s)
    if d == 0:
        return np.inf
    return (target_d / d) ** 2
