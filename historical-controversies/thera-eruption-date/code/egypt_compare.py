"""
Does the 2025 Ahmose result resolve the discrepancy, or relocate it?

Bruins & van der Plicht (2025), PLOS ONE 20(9):e0330702, argue that the Thera
eruption predates Ahmose. Their method is unusual and, on the evidence of this
session's curve analysis, well motivated: because every one of their objects
calibrates onto the 1610-1540 BCE plateau, they compare UNCALIBRATED 14C ages
rather than calendar dates. Their own words: "Since the above items cannot be
arranged in a stratigraphic sequence, Bayesian analysis could not be used. We
adopted an alternative strategy within radiocarbon time space."

That move is sound. What is checkable is whether the two series really do have
"a different time signature" once over-dispersion and the choice of which
Ahmose sample to trust are taken into account. All determinations below were
read from the article's own JATS XML tables on 2026-09-22
(data/bruins2025_egypt.csv).
"""
import sys, csv, numpy as np
sys.path.insert(0, 'code')
from scipy.stats import chi2 as chi2dist, norm
from parse_oxcal import blocks, dates


def pool(rs, inflate=True):
    r = np.array([x[0] for x in rs], float)
    s = np.array([x[1] for x in rs], float)
    w = 1 / s ** 2
    m = (w * r).sum() / w.sum()
    se = (1 / w.sum()) ** 0.5
    x2 = (w * (r - m) ** 2).sum()
    df = len(rs) - 1
    p = chi2dist.sf(x2, df) if df > 0 else 1.0
    if inflate and df > 0 and x2 > df:
        se *= (x2 / df) ** 0.5           # Birge ratio: honest SE under over-dispersion
    return m, se, x2, df, p


eg = list(csv.DictReader(open('data/bruins2025_egypt.csv')))
for e in eg:
    e['c14bp'] = float(e['c14bp']); e['sd'] = float(e['sd'])
bl = blocks('data/manning2022_S2_oxcal_runfiles.txt')
thera_b = [(d[1], d[2]) for d in dates(bl['b'])]
therasia_outer = [(3297, 23), (3341, 23), (3301, 23), (3320, 22), (3342, 24)]

groups = {
    'Thera Akrotiri VDL (Manning 2022 dataset b, n=31)': thera_b,
    'Therasia shrub outermost+bark (Pearson 2023, n=5)': therasia_outer,
    'Ahmose mudbrick, ALL 5 sub-samples': [(e['c14bp'], e['sd']) for e in eg if 'mudbrick' in e['object']],
    'Ahmose mudbrick, pure-straw date only (GrA-64347)': [(3230.0, 60.0)],
    'Satdjehuty linen (GrA-59770)': [(3310.0, 25.0)],
    '"17th Dynasty" stick shabtis (n=6)': [(e['c14bp'], e['sd']) for e in eg if 'shabti' in e['object']],
}
print('%-52s %8s %7s %8s %s' % ('group', 'pooled', 'SE*', 'chi2/df', 'p(homog)'))
P = {}
for k, v in groups.items():
    m, se, x2, df, p = pool(v)
    P[k] = (m, se)
    print('%-52s %8.1f %7.1f %8s %.3f' %
          (k, m, se, ('%.1f/%d' % (x2, df)) if df else '   -  ', p))
print('* SE inflated by the Birge ratio where the group is over-dispersed.')

print('\nPairwise comparison in 14C space (z = difference / combined SE; positive')
print('means the first group is OLDER in radiocarbon years):')
pairs = [
    ('Thera Akrotiri VDL (Manning 2022 dataset b, n=31)', 'Ahmose mudbrick, pure-straw date only (GrA-64347)'),
    ('Thera Akrotiri VDL (Manning 2022 dataset b, n=31)', 'Ahmose mudbrick, ALL 5 sub-samples'),
    ('Thera Akrotiri VDL (Manning 2022 dataset b, n=31)', 'Satdjehuty linen (GrA-59770)'),
    ('Thera Akrotiri VDL (Manning 2022 dataset b, n=31)', '"17th Dynasty" stick shabtis (n=6)'),
    ('Therasia shrub outermost+bark (Pearson 2023, n=5)', 'Ahmose mudbrick, pure-straw date only (GrA-64347)'),
    ('Therasia shrub outermost+bark (Pearson 2023, n=5)', 'Satdjehuty linen (GrA-59770)'),
    ('"17th Dynasty" stick shabtis (n=6)', 'Satdjehuty linen (GrA-59770)'),
    ('"17th Dynasty" stick shabtis (n=6)', 'Ahmose mudbrick, ALL 5 sub-samples'),
]
for a, b in pairs:
    ma, sa = P[a]; mb, sb = P[b]
    d = ma - mb; se = (sa ** 2 + sb ** 2) ** 0.5
    z = d / se
    print('  %-52s vs %-50s  %+7.1f +- %5.1f  z=%+5.2f  one-sided p=%.3f' %
          (a[:52], b[:50], d, se, z, norm.sf(abs(z))))

print('\nInternal consistency of the Egyptian series. Historically the "17th Dynasty"')
print('shabtis must be OLDER than the early-18th-Dynasty Satdjehuty linen, so the')
print('shabti pool should sit at a LARGER 14C age. It does not:')
ms, ss = P['"17th Dynasty" stick shabtis (n=6)']
ml, sl = P['Satdjehuty linen (GrA-59770)']
print('   shabtis %.1f +- %.1f  vs  linen %.1f +- %.1f  ->  %+.1f 14C yr (z=%+.2f)' %
      (ms, ss, ml, sl, ms - ml, (ms - ml) / (ss ** 2 + sl ** 2) ** 0.5))
