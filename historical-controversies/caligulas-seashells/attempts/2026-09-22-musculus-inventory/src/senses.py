#!/usr/bin/env python3
"""Sense classification of every unique `musculus` attestation.

Senses are assigned BY HAND from the KWIC context (see results/musculus_senses.tsv for
the per-item record with the phrase that decided it). The categories are:

  MIL    military-technical: the siege shed / sapper hut
  NAV    nautical: a small boat or a naval unit named from it
  MOUSE  the animal: little mouse, field mouse (dim. of mus)
  ANAT   anatomical: a muscle of the body
  FISH   the sea-beast that accompanies the whale (the "whale's guide")
  SHELL  the shellfish: mussel, as food or as a shore creature
  PLANT  a plant name (myosotis, "mouse-ear")
  NOISE  editorial apparatus, not a running-text attestation
  POST   post-classical author outside the ancient corpus (Descartes, Newton)

Assignment is a judgement call and is recorded item by item so it can be attacked.
"""
import json, sys, collections

# (file-substring, token_index) -> (sense, deciding phrase)
# Where a whole file is one sense, the token_index is given as '*'.
ASSIGN = {
 ('apuleius/apuleius2.txt','*'):      ('MOUSE','"ad tui similes musculos recondis" - insult, "go hide with mice like you"'),
 ('apuleius/apuleius8.txt','*'):      ('ANAT','"morsibus suos incursantes musculos" - biting their own muscles'),
 ('phi1212','*'):                     ('ANAT','Perseus copy of Apuleius Met. 8, same passage'),
 ('caesar/alex.txt','*'):             ('MIL','"testudinibus ac musculis aptantur"'),
 ('caesar/bc2.txt','*'):              ('MIL','BC 2.10, the extended description of the musculus at Massilia'),
 ('phi0448','*'):                     ('MIL','Perseus copy of Caesar BC 2.10'),
 ('caesar/gall7.txt','*'):            ('MIL','"crates longurios musculos falces" - siege gear at Alesia'),
 ('cassiodorus/varia7.txt','*'):      ('ANAT','"musculos tumentes" of a bronze statue'),
 ('cicero/divinatione2.txt','*'):     ('MOUSE','"musculorum iecuscula bruma augeri" - mice livers'),
 ('phi0474','*'):                     ('MOUSE','Perseus copy of Cic. Div. 2'),
 ('cicero/repub3.txt','*'):           ('MOUSE','"tamquam hos ex arvis musculos extitisse" - field mice'),
 ('columella/columella.rr6.txt','*'): ('ANAT','"nervisque et musculis robusta"; "musculorum toris" - ox and horse'),
 ('phi0845','*'):                     ('ANAT','Perseus copy of Columella 6'),
 ('descartes/des.med6.txt','*'):      ('POST','Descartes, Meditationes - anatomical, 17th c.'),
 ('newton.scholium.txt','*'):         ('POST','Newton, Scholium Generale - anatomical, 18th c.'),
 ('fronto.txt','*'):                  ('MOUSE','"ne musculus iste aliquid rimari possit" - a prying little mouse'),
 ('isidore/11.txt','*'):              ('ANAT','Etym. 11.1, "tori id est musculi"; etymology from mice given explicitly'),
 ('isidore/12.txt',None):             (None,None),   # mixed, itemised below
 ('isidore/18.txt','*'):              ('MIL','Etym. 18.11 DEFINITION: "musculus cuniculo similis fit quo murus perfoditur"'),
 ('isidore/19.txt','*'):              ('NAV','Etym. 19.1 DEFINITION: "musculus curtum navigium"'),
 ('lucan/lucan9.txt','*'):            ('ANAT','"femorum quoque musculus omnis liquitur"'),
 ('phi0917','*'):                     ('ANAT','Perseus copy of Lucan 9'),
 ('notitia2.txt','*'):                ('NAV','"cohortis ... musculorum Scythicorum et classis" - a riverine naval command'),
 ('pliny.ep3.txt','*'):               ('ANAT','"ossa musculi nervi venae" - a portrait bust'),
 ('pliny.ep5.txt','*'):               ('ANAT','"ossa musculi nervi" - oratorical style metaphor'),
 ('pliny.nh2.txt','*'):               ('MOUSE','"aquatiles musculi" at Stymphalus - water-mice among marvels of springs'),
 ('plautus/rudens.txt','*'):          ('SHELL','fisherman\'s catalogue: "conchas ... musculos plagusias"'),
 ('phi0119','*'):                     ('SHELL','Perseus copy of Plautus Rudens'),
 ('phi0428','*'):                     ('MIL','Perseus copy of Bell. Alex.'),
 ('sidonius1.txt','*'):               ('ANAT','"musculis prominentibus latus" - description of a body'),
 ('sidonius5.txt','*'):               ('FISH','"musculis similis ... ballaenarum corpulentiam praegubernantibus"'),
 ('solinus3.txt','*'):                ('MOUSE','"odorem muris ... pabula quae a musculis contacta sunt recusant"'),
 ('solinus3a.txt','*'):               ('MOUSE','same passage, variant Solinus file'),
 ('solinus5.txt','*'):                ('MOUSE','same passage, variant Solinus file'),
 ('tertullian/tertullian.carne.txt','*'): ('ANAT','"sine musculis solidam"; "musculos ut glebas"'),
 ('stoa0275','*'):                    ('ANAT','Perseus copy of Tertullian De Carne Christi'),
 ('stoa0045','*'):                    ('SHELL','Ausonius Ep., "de ostreis et musculis"; "iunctus limicolis musculus ostreis"'),
 ('stoa0261','*'):                    ('FISH','Sidonius Ep., whale-companion simile'),
 ('testamentum.txt','*'):             ('ANAT','Testamentum Porcelli, "musculos cursoribus" - the pig\'s muscles'),
 ('vegetius2.txt','*'):               ('MIL','2.25 "testudines musculos arietes uineas"'),
 ('vegetius4.txt','*'):               ('MIL','4.13/4.16 DEFINITION: "musculos dicunt minores machinas"'),
 ('phi0836','*'):                     (None,None),   # Celsus, itemised below
}

# Celsus: one food-list attestation is SHELL, the other 23 are ANAT.
CELSUS_SHELL_MARKER = 'conchulae'


# Pliny NH (Perseus phi0978) is a text with critical apparatus interleaved, so some
# "hits" are apparatus repetitions rather than running-text attestations. Assigned by
# token index after reading each context.
PLINY = {
 71250:  ('MOUSE','NH 2: "aquatiles musculi" at Stymphalus, among marvels of springs'),
 223159: ('MOUSE','NH 8: "ruinis inminentibus musculi praemigrant" - mice flee before a collapse'),
 257502: ('MOUSE','NH 9: mice half-formed from Nile mud, "musculi reperiuntur inchoato opere"'),
 258257: ('FISH', 'NH 9: "societatem ballaena et musculus" - the whale and its companion'),
 279127: ('MOUSE','NH 10: birds/cats "in musculos exiliunt" - pounce on mice'),
 298118: ('FISH', 'NH 11: "musculus marinus qui ballaenam antecedit nullos habet [dentes]"'),
 298119: ('NOISE','apparatus repetition of the preceding lemma'),
 496866: ('ANAT', 'NH 23-ish: remedy applied "musculis nervis articulis"'),
 499226: ('ANAT', 'NH: "musculorum nervorum articulorum cervicium" - body parts'),
 500674: ('NOISE','apparatus: "ramusculus v MUSCULUS b del. Verc." - a variant reading, not text'),
 618464: ('MOUSE','NH 25: the plant imitates "musculorum aures" - mouse-ear, myosotis'),
 621557: ('MOUSE','NH 29: ink "litteras a musculis tuetur" - protects writing from mice'),
 621558: ('NOISE','apparatus repetition of the preceding lemma'),
 735424: ('FISH', 'NH 32: sea-creature list "rotae orcae arietes musculi et alii piscium forma"'),
}

# Isidore 12 is mixed: 12.1 (horse) ANAT, 12.6 FISH/SHELL cluster.
def classify(h):
    f = h['file']
    ctx = (h['left'] + ' ' + h['right'])
    if 'phi0978' in f:
        return PLINY.get(h['token_index'], ('UNCLASSIFIED', ''))
    if 'phi0836' in f:
        return ('SHELL', 'Celsus 2.18 food list: "ostrea pelorides echini musculi et omnes fere conchulae"') \
            if CELSUS_SHELL_MARKER in ctx else \
            ('ANAT', 'Celsus, surgical/anatomical context (De Medicina bks 5-8)')
    if 'isidore/12.txt' in f:
        if 'ballenae masculus' in ctx:
            return ('FISH', 'Etym. 12.6: "musculus quod sit ballenae masculus"')
        if 'coclearum' in ctx or 'cochleae' in ctx or 'quasi masculi' in ctx:
            return ('SHELL', 'Etym. 12.6: "musculi ... cochleae a quorum lacte concipiunt ostreae"')
        return ('ANAT', 'Etym. 12.1, the horse: "corpus omne musculorum densitate nodosum"')
    for (key, idx), val in ASSIGN.items():
        if key in f and val[0] is not None:
            return val
    return ('UNCLASSIFIED', '')

def main(inp, tsv, summary):
    d = json.load(open(inp))
    rows = []
    for h in sorted(d['hits'], key=lambda x: (x['file'], x['token_index'])):
        s, why = classify(h)
        rows.append((s, h['file'], h['token_index'], h['form'], why,
                     (h['left'][-60:] + ' [' + h['form'].upper() + '] ' + h['right'][:60])))
    with open(tsv, 'w', encoding='utf-8') as fh:
        fh.write('sense\tfile\ttoken_index\tform\tdeciding_evidence\tkwic\n')
        for r in rows:
            fh.write('\t'.join(str(x) for x in r) + '\n')
    c = collections.Counter(r[0] for r in rows)
    tot = sum(c.values())
    out = {'total_attestations': tot, 'by_sense': dict(c),
           'by_sense_pct': {k: round(100*v/tot, 1) for k, v in c.items()}}
    json.dump(out, open(summary, 'w'), indent=1)
    for k, v in c.most_common():
        print(f"  {k:14s} {v:3d}  {100*v/tot:5.1f}%")
    print(f"  {'TOTAL':14s} {tot:3d}")

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
