"""Parse Manning (2022) PLOS ONE 17(9):e0274835 Table S1 (S1 File, .docx) into CSV.

Source: https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0274835.s001
Downloaded 2026-09-22. The .docx is re-downloadable at that URL; this script turns it
into the flat dataset in data/manning2022_S1.csv. Sub-table (A/B/C/D) is recorded
because Manning's own datasets are built from those blocks.
"""
import csv, sys, zipfile
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
SUBTABLE_MARK = 'Table S1'


def docx_blocks(path):
    root = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml').decode('utf-8'))
    body = root.find(W + 'body')
    ptext = lambda p: ''.join(t.text or '' for t in p.iter(W + 't'))
    for el in body:
        tag = el.tag.replace(W, '')
        if tag == 'p':
            yield ('p', ptext(el).strip())
        elif tag == 'tbl':
            rows = []
            for tr in el.findall(W + 'tr'):
                rows.append([' '.join(ptext(p).strip() for p in tc.findall(W + 'p')).strip()
                             for tc in tr.findall(W + 'tc')])
            yield ('tbl', rows)


def parse(path):
    sub, out = '?', []
    for kind, val in docx_blocks(path):
        if kind == 'p':
            if val.startswith(SUBTABLE_MARK) and len(val) > 8 and val[8] in 'ABCD':
                sub = val[8]
            continue
        for r in val:
            if len(r) < 8 or r[0].strip().lower() in ('no.', 'no'):
                continue
            try:
                no = int(r[0])
                bp = int(r[5].replace(',', ''))
                sd = int(r[6])
            except ValueError:
                continue
            out.append(dict(no=no, subtable=sub, lab_id=r[1].strip(), site=r[2].strip(),
                            context=r[3].strip(), material=r[4].strip(), c14bp=bp, sd=sd,
                            ref=r[7].strip()))
    return out


if __name__ == '__main__':
    rows = parse(sys.argv[1])
    with open(sys.argv[2], 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print('rows', len(rows), 'nos', min(r['no'] for r in rows), '-', max(r['no'] for r in rows))
    from collections import Counter
    print(Counter(r['subtable'] for r in rows))
