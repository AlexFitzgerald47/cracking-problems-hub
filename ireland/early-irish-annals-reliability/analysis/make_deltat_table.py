"""Generate results/delta_t_stephenson2016.csv.

Delta-T (TT - UT1) for the study window, from the cubic-spline fit of

    F. R. Stephenson, L. V. Morrison & C. Y. Hohenkerk, "Measurement of the
    Earth's rotation: 720 BC to AD 2015", Proc. R. Soc. A 472:20160404 (2016),
    with the Morrison et al. (2021) addendum, Proc. R. Soc. A 477:20200776.

The spline coefficients are not re-typed here.  They are read from the reference
implementation at https://github.com/ytliu0/DeltaT (GPL-3), cloned alongside this
repository; only the *values* it produces are stored, as data.  Provenance check
run before use: that implementation returns Delta-T(2000) = 63.8 s, which is the
observed value, and reproduces the published first-millennium magnitudes.

Why this matters here: the Morrison & Stephenson (2004) long-term parabola, which
is what a quick calculation reaches for, is wrong by -182 s at AD 664 and by -481 s
at AD 1000.  481 s is 2.0 degrees of Earth rotation, roughly 220 km at Irish
latitudes, which is a tenth of a magnitude on the edge of a partial eclipse.  The
parabola is not good enough for this problem; the spline, at +/-15 to 50 s, is far
better than it needs to be.

Usage:  python make_deltat_table.py /path/to/ytliu0/DeltaT
"""

import csv
import os
import sys

DEFAULT_REF = "/home/user/ytliu0/deltat"


def main(ref=None, y0=300, y1=1310):
    ref = ref or DEFAULT_REF
    sys.path.insert(0, ref)
    from DeltaT import DeltaT, DeltaT_error_estimate  # noqa: E402

    anchor = float(DeltaT(2000))
    assert abs(anchor - 63.8) < 0.5, "provenance check failed: dT(2000)=%s" % anchor

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results",
                       "delta_t_stephenson2016.csv")
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["year", "delta_t_s", "sigma_s"])
        w.writeheader()
        for y in range(y0, y1 + 1):
            w.writerow({"year": y,
                        "delta_t_s": round(float(DeltaT(y)), 1),
                        "sigma_s": round(float(DeltaT_error_estimate(y)), 1)})
    print("wrote %s (%d rows)" % (out, y1 - y0 + 1))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
