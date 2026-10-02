#!/usr/bin/env python3
"""
VALIDATOR 2, 2026-10-02 -- "two scans" check applied to a LIVE source.

The Hub's own practice note (board/log/2026-09-23-two-scans-and-the-proximity-trap.md,
carried into HANDOVER.md on 2026-09-24) says scholarly editions usually exist as two or
more independent witnesses that disagree, and that running the pipeline on both is one
extra curl. The OCBI corpus has exactly two public witnesses:

  W1  raw master source   https://raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm
  W2  the DEPLOYED build  https://center-for-decipherment.ch/tool/elamicon.js   (compiled Elm bundle)

W2 is what a human actually reads when they "check OCBI", and it is built from some
commit that need not be master. This script compares the two on everything the claim
depends on: the syllabary groups, the syllableMap, and the cylinder rows.
"""
import re, os, json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)
ispua = lambda c: 0xE000 <= ord(c) <= 0xF8FF
CP = lambda c: '%04X' % ord(c)
d = lambda t: ''.join(('<%04X>' % ord(c)) if ispua(c) else c for c in t)

w1 = open(P('Byblos.upstream.elm'), encoding='utf-8').read()
w2 = open(P('elamicon.deployed.js'), encoding='utf-8', errors='replace').read()

def hdr(t):
    print('\n' + '=' * 78 + '\n' + t + '\n' + '=' * 78)

# ---------------------------------------------------------------- syllabaries
SYL = re.compile(r'\{\s*id\s*=\s*"(?P<id>[^"]+)"\s*,\s*name\s*=\s*"(?P<name>[^"]+)"\s*,'
                 r'\s*syllabary\s*=\s*String\.trim\s*"""(?P<body>.*?)"""', re.S)
def groups_from_body(body):
    out = []
    for ln in body.strip().split('\n'):
        g = tuple(CP(c) for c in ln if ispua(c))
        if g:
            out.append(g)
    return out

w1_syl = {m.group('id'): groups_from_body(m.group('body')) for m in SYL.finditer(w1)}

# In the compiled bundle the same strings survive as JS literals with \n escapes.
# A syllabary is a maximal run of >=10 "\n"-separated PUA-only lines.
def groups_from_js(js):
    blocks = []
    for m in re.finditer(r'"((?:\\n(?:[-]+))+\\n?\s*)"', js):
        lines = [tuple(CP(c) for c in ln if ispua(c))
                 for ln in m.group(1).split('\\n')]
        lines = [l for l in lines if l]
        if len(lines) >= 10:
            blocks.append(lines)
    return blocks
w2_blocks = groups_from_js(w2)

hdr('1. SYLLABARY BLOCKS: W1 (master source) vs W2 (deployed build)')
print('  W1 syllabaries : %d  (%s)' % (len(w1_syl), ', '.join(w1_syl)))
print('  W2 blocks >=10 groups found in the bundle : %d' % len(w2_blocks))
w1_sets = {k: frozenset(v) for k, v in w1_syl.items()}
w2_sets = [frozenset(b) for b in w2_blocks]
matched, unmatched = {}, []
for b in w2_blocks:
    fb = frozenset(b)
    hit = [k for k, v in w1_sets.items() if v == fb]
    if hit:
        matched.setdefault(hit[0], 0)
        matched[hit[0]] += 1
    else:
        unmatched.append(b)
print('  W1 ids exactly reproduced in W2 : %s' % (sorted(matched) or 'NONE'))
print('  W1 ids NOT found in W2          : %s' % sorted(set(w1_syl) - set(matched)))
print('  W2 blocks with no W1 counterpart: %d' % len(unmatched))
for b in unmatched:
    best, score = None, -1
    for k, v in w1_sets.items():
        ov = len(v & frozenset(b))
        if ov > score:
            best, score = k, ov
    print('    block of %d groups; closest W1 = %s (%d/%d groups identical)'
          % (len(b), best, score, len(b)))
    only_w2 = frozenset(b) - w1_sets[best]
    only_w1 = w1_sets[best] - frozenset(b)
    for g in sorted(only_w2)[:6]:
        print('       only in W2: ' + '+'.join(g))
    for g in sorted(only_w1)[:6]:
        print('       only in W1: ' + '+'.join(g))

hdr('2. THE LOAD-BEARING PAIR E416 / E4AF IN BOTH WITNESSES')
def verdicts(blocks):
    out = []
    for b in blocks:
        k1 = next((i for i, g in enumerate(b) if 'E416' in g), None)
        k2 = next((i for i, g in enumerate(b) if 'E4AF' in g), None)
        out.append('merged' if (k1 is not None and k1 == k2) else 'split/absent')
    return Counter(out)
print('  W1 per-inventory verdicts :', dict(verdicts(list(w1_syl.values()))))
print('  W2 per-block  verdicts    :', dict(verdicts(w2_blocks)))

hdr('3. syllableMap IN BOTH WITNESSES')
m1 = re.search(r'syllableMap\s*=\s*String\.trim\s*"""(.*?)"""', w1, re.S)
print('  W1:', json.dumps(d(m1.group(1)).strip()) if m1 else 'absent')
m2 = re.search(r'"\\nme [-](?:\\n[^"\\]*)*\\n"', w2)
if not m2:
    m2 = re.search(r'"((?:\\n(?:me|pa|ATON)[^"]{0,400}))"', w2)
print('  W2:', json.dumps(d(m2.group(0))) if m2 else 'absent')
print('  IDENTICAL ATON ASSIGNMENT IN BOTH WITNESSES:',
      bool(m1 and m2 and 'ATON ' in m1.group(1) and 'ATON <E416>' in d(m2.group(0))))

hdr('4. CYLINDER ROWS IN BOTH WITNESSES')
FRAG = re.compile(r'\{\s*id\s*=\s*"(?P<id>[^"]*)"\s*,\s*source\s*=\s*"(?P<source>[^"]*)"\s*,'
                  r'\s*group\s*=\s*"(?P<group>[^"]*)"\s*,\s*dir\s*=\s*(?P<dir>\w+)\s*,'
                  r'.*?text\s*=\s*\n?\s*"""(?P<text>.*?)"""', re.S)
w1_frag = {m.group('id'): m.group('text').strip() for m in FRAG.finditer(w1)}
rows = {k: v for k, v in w1_frag.items() if k.startswith(('ra', 'rb', 'rc', 'rd'))}
for k, v in sorted(rows.items()):
    seq = ''.join(c for c in v if ispua(c))
    present = seq in w2
    print('  %-16s W1=%s   byte-for-byte present in W2: %s'
          % (k, d(seq), present))

hdr('5. CORPUS COUNTS IN BOTH WITNESSES')
print('  W1 group field counts :', dict(Counter(m.group('group') for m in FRAG.finditer(w1))))
print('  W2 occurrences of the literal "BYBL?" :', w2.count('BYBL?'))
print('  W2 occurrences of the literal "BYBL"  :', w2.count('BYBL'))
print('  (W2 is minified, so these are upper bounds, not object counts.)')
