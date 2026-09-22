"""Pull the R_Date entries of each Dataset block out of Manning (2022) Table S2
(the OxCal runfiles), so that no determination is retyped by hand."""
import re, sys


def blocks(path):
    txt = open(path, encoding='utf-8').read()
    # Dataset (a) ... Dataset (b) ... etc.
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'^Dataset \(([a-z0-9\-]+)\)\s*$', txt, re.M)]
    out = {}
    for k, (pos, name) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(txt)
        out[name] = txt[pos:end]
    return out


RD = re.compile(r'R_Date\s*\(\s*"([^"]*)"\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')


def dates(block):
    return [(m.group(1), int(m.group(2)), int(m.group(3))) for m in RD.finditer(block)]


if __name__ == '__main__':
    bs = blocks(sys.argv[1])
    for k in sorted(bs):
        ds = dates(bs[k])
        print('Dataset (%s): %d R_Date entries' % (k, len(ds)))
        if len(sys.argv) > 2 and sys.argv[2] == k:
            for d in ds:
                print('   ', d)
