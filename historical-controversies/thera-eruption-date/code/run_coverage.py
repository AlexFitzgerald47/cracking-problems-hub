"""Frequentist calibration of the published Bayesian intervals.

For a dense grid of assumed true eruption years, simulate datasets with the
real design (n and 1-sigma errors of Manning's dataset (a) or (b)), run the
same model, and ask two questions the literature never asks:

  1. COVERAGE. How often does the model's nominal 68.3% / 95.4% HPD actually
     contain the true year? If the plateau makes the intervals overconfident,
     this is where it shows.
  2. CALIBRATED LIKELIHOOD. What is the sampling distribution of the recovered
     posterior median given T? Inverting it turns the observed median into a
     bias-corrected statement about T.
"""
import sys, json, time, numpy as np
sys.path.insert(0, 'code')
from calib import Curve
from parse_oxcal import blocks, dates
from power_sim import Sim, median_bce
from exact import hpd_years

c = Curve('data/intcal20.14c')
bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')

DESIGNS = {
    'b_akrotiri_vdl': [d[2] for d in dates(bl['b'])],
    'a_non_thera': [17, 22, 19, 20, 17, 22, 27, 19, 30, 30, 46, 48, 35, 35, 40, 40, 40, 25],
}
TRUTHS = list(range(1680, 1469, -10))
NREP = 400
TAU_TRUE = 28
OUT = {}
for name, sig in DESIGNS.items():
    S = Sim(c, seed=hash(name) % 9999)
    rows = []
    t0 = time.time()
    for T in TRUTHS:
        cov68 = cov95 = 0
        meds = []
        for _ in range(NREP):
            r, s = S.draw(-T + 1, sig, TAU_TRUE)
            p = S.end_posterior(r, s)
            meds.append(median_bce(S.years, p))
            for lv, box in ((0.683, 'a'), (0.954, 'b')):
                hp = hpd_years(S.years, p, lv)
                hit = any(b - 0.5 <= T <= a + 0.5 for a, b, _ in hp)
                if lv == 0.683:
                    cov68 += hit
                else:
                    cov95 += hit
        meds = np.array(meds)
        rows.append(dict(T=T, cov68=cov68 / NREP, cov95=cov95 / NREP,
                         med_mean=float(meds.mean()), med_sd=float(meds.std()),
                         meds=meds.tolist()))
        print('%s T=%4d  cov68=%.3f cov95=%.3f  median %6.1f +- %4.1f  (%.0fs)' %
              (name, T, cov68 / NREP, cov95 / NREP, meds.mean(), meds.std(), time.time() - t0),
              flush=True)
    OUT[name] = dict(n=len(sig), sigmas=sig, truths=TRUTHS, rows=rows, nrep=NREP,
                     tau_true=TAU_TRUE)
json.dump(OUT, open('data/coverage_sim.json', 'w'))
print('written data/coverage_sim.json')
