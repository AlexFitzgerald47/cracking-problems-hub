"""Build one open dataset of every determination this session verified.

Sources, each read from the publisher's own table (not from a secondary
summary) on 2026-09-22:
  manning2022   Manning SW (2022) PLoS ONE 17(9):e0274835, S1 Table (.docx
                supplement, parsed by code/parse_s1.py). 257 rows. This is
                itself a compilation citing ~15 original publications; the
                'ref' column carries Manning's own reference numbers.
  pearson2023   Pearson C, Sbonias K, Tzachili I, Heaton TJ (2023) Sci Rep
                13:6994, Table 1 (journal table HTML). 9 rows.
  bruins2025    Bruins HJ, van der Plicht J (2025) PLoS ONE 20(9):e0330702,
                Tables 4-6 (article JATS XML). 12 rows.
"""
import csv

OUT = 'data/thera_determinations_consolidated.csv'
FIELDS = ['source', 'lab_id', 'site_or_object', 'context', 'material',
          'c14bp', 'sd', 'orig_ref', 'relevance']
rows = []

for r in csv.DictReader(open('data/manning2022_S1.csv')):
    rel = {'A': 'eruption-related (Manning dataset a/b/c/d pool)',
           'B': 'Aegean sequence around the eruption',
           'C': 'LMIB / LMII destructions on Crete',
           'D': 'pre- or post-eruption context'}.get(r['subtable'], '')
    rows.append(dict(source='manning2022_S1' + r['subtable'], lab_id=r['lab_id'],
                     site_or_object=r['site'], context=r['context'],
                     material=r['material'], c14bp=r['c14bp'], sd=r['sd'],
                     orig_ref='Manning 2022 ref ' + r['ref'], relevance=rel))

for r in csv.DictReader(open('data/pearson2023_therasia.csv')):
    rows.append(dict(source='pearson2023_T1', lab_id=r['lab_id'],
                     site_or_object='Therasia olive shrub, trench AB, Koimisis',
                     context='carbonised below Minoan pumice; ' + r['sample_id'],
                     material='Olea europaea stem (%s)' % r['part'],
                     c14bp=r['c14bp'], sd=r['sd'], orig_ref='Pearson et al. 2023',
                     relevance='eruption-killed shrub; outermost = eruption TPQ'))

for r in csv.DictReader(open('data/bruins2025_egypt.csv')):
    rows.append(dict(source='bruins2025_' + r['source_table'], lab_id=r['lab_id'],
                     site_or_object='%s (%s)' % (r['object'], r['museum_no']),
                     context=r['attribution'], material=r['material'],
                     c14bp=r['c14bp'], sd=r['sd'],
                     orig_ref='Bruins & van der Plicht 2025',
                     relevance='Egyptian 17th/early-18th Dynasty comparison'))

with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader(); w.writerows(rows)
print('%s: %d determinations' % (OUT, len(rows)))
from collections import Counter
for k, v in sorted(Counter(r['source'] for r in rows).items()):
    print('   %-20s %d' % (k, v))
