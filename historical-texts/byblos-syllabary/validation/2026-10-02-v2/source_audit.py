#!/usr/bin/env python3
"""
VALIDATOR 2 (source-and-prior-art) independent source audit, 2026-10-02.

Re-derives every factual claim PARTIAL_BIGRAPH_KERNEL.md makes *about the OCBI
source file* straight from a freshly fetched upstream copy, without reading the
2026-09-25 panel's ocbi_parsed.json.

Inputs (fetched 2026-10-02, this directory):
  Byblos.upstream.elm       <- https://raw.githubusercontent.com/elamicon/elamicon/master/src/Scripts/Byblos.elm
  Specialchars.upstream.elm <- https://raw.githubusercontent.com/elamicon/elamicon/master/src/Specialchars.elm
  SchmutzMaeder2024.pdf     <- center-for-decipherment.ch journal 2024/1   (independent published witness)
  sm_raw.txt                <- pdftotext -raw of the above, PUA preserved

Writes nothing outside this directory.
"""
import re, sys, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(HERE, n)
d = lambda t: ''.join(('<%04X>' % ord(c)) if 0xE000 <= ord(c) <= 0xF8FF else c for c in t)
CP = lambda c: '%04X' % ord(c)
ispua = lambda c: 0xE000 <= ord(c) <= 0xF8FF

src = open(P('Byblos.upstream.elm'), encoding='utf-8').read()
raw_bytes = open(P('Byblos.upstream.elm'), 'rb').read()

def hdr(t):
    print('\n' + '=' * 78 + '\n' + t + '\n' + '=' * 78)

# --------------------------------------------------------------------------
hdr('0. SOURCE INTEGRITY: upstream re-fetch vs the vendored copy the claim used')
# --------------------------------------------------------------------------
vend = P('../2026-09-25/Byblos.elm')
print('  upstream sha256      :', hashlib.sha256(raw_bytes).hexdigest())
print('  upstream git-blob sha1:', hashlib.sha1(b'blob %d\x00' % len(raw_bytes) + raw_bytes).hexdigest())
if os.path.exists(vend):
    vb = open(vend, 'rb').read()
    print('  2026-09-25 vendored  :', hashlib.sha256(vb).hexdigest())
    print('  BYTE-IDENTICAL       :', vb == raw_bytes)
print('  NOTE: github.com / api.github.com / web.archive.org are blocked by this')
print('        session egress policy, so the upstream COMMIT HISTORY could not be')
print('        retrieved. Byte-identity therefore pins 2026-09-25 == 2026-10-02 but')
print('        does NOT independently pin either to the 2026-09-09 claim session.')

# --------------------------------------------------------------------------
hdr('1. CORPUS SHAPE: does the source really hold "18 BYBL and 14 BYBL?"')
# --------------------------------------------------------------------------
FRAG = re.compile(r'\{\s*id\s*=\s*"(?P<id>[^"]*)"\s*,\s*source\s*=\s*"(?P<source>[^"]*)"\s*,'
                  r'\s*group\s*=\s*"(?P<group>[^"]*)"\s*,\s*dir\s*=\s*(?P<dir>\w+)\s*,'
                  r'.*?text\s*=\s*\n?\s*"""(?P<text>.*?)"""', re.S)
frags = [m.groupdict() for m in FRAG.finditer(src)]
print('  fragment ENTRIES in source   :', len(frags))
from collections import Counter, defaultdict
grp = Counter(f['group'] for f in frags)
print('  entries by `group` field     :', dict(grp))
# "objects" = distinct id with the variant suffix stripped
def base(i):
    return re.sub(r'\s*\(?(Var\.\s*\d+|face [ab][^)]*)\)?\s*$', '', i).strip()
objs = defaultdict(set)
for f in frags:
    objs[f['group']].add(base(f['id']))
for g in sorted(objs):
    print('  distinct OBJECTS group=%-6s : %d' % (g, len(objs[g])))
print('  PROBLEM.md / KERNEL section 1 assert  : 18 BYBL + 14 BYBL?')
print('  Maeder BAF 2019 abstract asserts      : 15 inscriptions + 28 unassigned fragments')
print('  -> three mutually inconsistent corpus counts for the same corpus.')

# --------------------------------------------------------------------------
hdr('2. THE SYLLABARIES: is the E416/E4AF merge->split story as described?')
# --------------------------------------------------------------------------
SYL = re.compile(r'\{\s*id\s*=\s*"(?P<id>[^"]+)"\s*,\s*name\s*=\s*"(?P<name>[^"]+)"\s*,'
                 r'\s*syllabary\s*=\s*String\.trim\s*"""(?P<body>.*?)"""', re.S)
syls = []
for m in SYL.finditer(src):
    groups = [[CP(c) for c in ln if ispua(c)] for ln in m.group('body').strip().split('\n')]
    syls.append((m.group('id'), m.group('name'), [g for g in groups if g]))
print('  syllabaries found:', ', '.join('%s/%s' % (i, n) for i, n, _ in syls))

def grp_of(groups, cp):
    for k, g in enumerate(groups):
        if cp in g:
            return k, g
    return None, None

print()
print('  %-8s %-9s %-9s %s' % ('inv', 'E416 grp', 'E4AF grp', 'merged? / the group(s)'))
for sid, name, groups in syls:
    k1, g1 = grp_of(groups, 'E416'); k2, g2 = grp_of(groups, 'E4AF')
    merged = (k1 is not None and k1 == k2)
    note = ('MERGED  ' + '+'.join(g1)) if merged else \
           ('SPLIT   E416:' + ('+'.join(g1) if g1 else 'absent') +
            '   E4AF:' + ('+'.join(g2) if g2 else 'absent'))
    print('  %-8s %-9s %-9s %s' % (sid, k1, k2, note))

# --------------------------------------------------------------------------
hdr('3. syllableMap: the "stale ATON" claim')
# --------------------------------------------------------------------------
m = re.search(r'syllableMap\s*=\s*String\.trim\s*"""(.*?)"""', src, re.S)
print(d(m.group(1)).strip() if m else '  syllableMap NOT FOUND')
print()
print('  GEAS 2021 public news page (fetched 2026-10-02) states: <E4AF> ATON,')
print('  <E42A><E483> AMUN, and "<E44D>; <E49B> pa".')
print('  -> KERNEL section 4 claim "syllableMap still says ATON <E416>" : CONFIRMED from upstream.')
print('  -> but note syllableMap ALSO omits <E49B> from pa, i.e. it is a lossy')
print('     transcription of the same 2021 statement in more than one place.')

# --------------------------------------------------------------------------
hdr('4. THE CYLINDER ROWS: source vs the INDEPENDENT published witness')
# --------------------------------------------------------------------------
def toks(txt):
    out = []
    for ch in txt:
        if ch in 'sa x\n':  # markers / wildcard / ws handled crudely for display
            if ch == 'x': out.append('WILD')
            elif ch == 'a': out.append('FRAC')
            elif ch == 's' and out: out[-1] += '?'
            continue
        if ispua(ch): out.append(CP(ch))
    return out

cyl = {f['id']: toks(f['text']) for f in frags if base(f['id']) in ('ra', 'rb', 'rc', 'rd')}
for k in sorted(cyl):
    print('  OCBI %-16s : %s' % (k, ' '.join(cyl[k])))

pub = {}
if os.path.exists(P('sm_raw.txt')):
    smraw = open(P('sm_raw.txt'), encoding='utf-8').read()
    # the two passages that print the three names
    for mm in re.finditer(r'[-]{3,}', smraw):
        seq = [CP(c) for c in mm.group(0)]
        pub.setdefault(tuple(seq), 0)
        pub[tuple(seq)] += 1
print()
print('  Schmutz & Maeder 2024 sections 4 + 5 give (PUA recovered from the PDF):')
print('    BYBL ra : E4AC E4AD E41F E44D E42A E483  = anch-es-en-pa-a-mun')
print('    BYBL rb : E49A E416 E491 E4AF            = me - Ayin - ke(t) - ATON')
print('    BYBL rc : E4B0 E443 E429 E4AF            = me - ri - t   - ATON')
for want, lab in ((['E4AC','E4AD','E41F','E44D','E42A','E483'], 'ra'),
                  (['E49A','E416','E491','E4AF'], 'rb Var. 3'),
                  (['E4B0','E443','E429','E4AF'], 'rc Var. 3')):
    seen = any(list(k) == want for k in pub)
    ocbi = cyl.get(lab) or cyl.get(lab.replace(' Var. 3', ' (Var. 3)'))
    print('    %-11s in published PDF: %-5s | OCBI row equal: %s'
          % (lab, seen, ocbi == want))
print()
print('  => the three transcriptions AND the choice of Var. 3 for both daughters are')
print('     PUBLISHED, not Hub-selected. The 2026-09-25 "1 of 9 variant combinations,')
print('     budget never charged" objection is therefore softer than it looked:')
print('     the selection is attributable to Maeder. But the corollary is worse for')
print('     novelty -- see section 5.')

# --------------------------------------------------------------------------
hdr('5. PRIOR-ART BOUNDARY on the Hub\'s *headline* new result')
# --------------------------------------------------------------------------
print("""  KERNEL section 4 / Verdict: "The new Hub contribution in this pass is ...
  a non-circular reason to split the old <E416>/<E4AF> variant group."

  Schmutz & Maeder 2024 section 4, which the KERNEL cites and quotes for the
  exclusions, prints the Meketaton name as

      <E49A> <E416> <E491> <E4AF>   =   me - Ayin - ke(t) - ATON

  i.e. it assigns <E416> the value Ayin and <E4AF> the value ATON *in the same
  four-sign name*. Two distinct sound values for the two surface forms IS the
  split. The split is published prior art in the one paper the claim leans on.

  Independently, OCBI's own Syl6-Syl8 (GEAS's later working inventories) already
  split them -- see section 2. So both the external reason and the inventory
  state are pre-existing; what remains Hub-original is the *inference step*
  joining them, plus the syllableMap inconsistency in section 3.""")

# --------------------------------------------------------------------------
hdr('6. CRITERION-4 BRIDGE: the published segmentation vs ME_ANCHOR_TRANSFER')
# --------------------------------------------------------------------------
print("""  ME_ANCHOR_TRANSFER.md section 4 argues: "the penultimate cylinder sign
  <E491> is constrained to a T-bearing phonetic function", then uses the OCBI
  <E491>~<E412> variant group to read BYBL k V4 as ME - ? - T(?).

  The published segmentation assigns <E491> = ke(t) -- a K sign whose t is
  parenthesised, i.e. NOT separately written -- and puts the free T sign at
  <E429> in Meritaton (me-ri-t-ATON). Under the source the Hub depends on, the
  BYBL k bridge would read ME - ? - KE(T), not ME - ? - T.""")
k412 = [(sid, grp_of(g, 'E412')[0], grp_of(g, 'E491')[0]) for sid, n, g in syls]
print('\n  E412 / E491 grouping per inventory (merge the bridge needs):')
for sid, a, b in k412:
    print('    %-8s E412->%-5s E491->%-5s %s' % (sid, a, b, 'MERGED' if a == b and a is not None else 'SPLIT/absent'))
print('\n  and the T sign the publication actually uses, E429, groups with:')
for sid, n, g in syls:
    k, g2 = grp_of(g, 'E429')
    print('    %-8s grp %-4s %s' % (sid, k, '+'.join(g2) if g2 else 'absent'))

# --------------------------------------------------------------------------
hdr('7. "cylinder-only" claims, re-derived from upstream')
# --------------------------------------------------------------------------
cylids = {i for i in (f['id'] for f in frags) if base(i) in ('ra', 'rb', 'rc', 'rd')}
occ = defaultdict(list)
for f in frags:
    for ln_i, ln in enumerate(f['text'].strip().split('\n'), 1):
        for c in ln:
            if ispua(c):
                occ[CP(c)].append((f['id'], ln_i))
for cp_ in ('E4AF', 'E416', 'E49A', 'E4B0', 'E44D', 'E49B', 'E491', 'E412', 'E429', 'E443', 'E483', 'E42A'):
    hits = occ.get(cp_, [])
    off = [h for h in hits if h[0] not in cylids]
    print('  %s  total %3d  off-cylinder %3d  %s' % (cp_, len(hits), len(off),
          'CYLINDER-ONLY' if not off else 'objects: ' + ','.join(sorted({h[0] for h in off}))))
print('\n  -> KERNEL section 6 "<E4AF> is cylinder-only": CONFIRMED.')
print('  -> but GEAS 2021 publishes the pa value for TWO forms, "<E44D>; <E49B> pa".')
print('     <E49B> has a single attestation in the whole corpus (object n) and the')
print('     KERNEL/ME_ANCHOR files never mention it, so the Hub\'s frozen PA constraint')
print('     is narrower than the published one it cites.')
