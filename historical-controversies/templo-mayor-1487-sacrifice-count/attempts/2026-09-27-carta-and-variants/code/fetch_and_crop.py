#!/usr/bin/env python3
"""Rebuild every source this session read, and the image crops its counts rest on.

  python3 fetch_and_crop.py [outdir]        (default: ./work)

Writes <outdir>/raw/*.txt (OCR text), <outdir>/pages/*.jpg (full pages) and
<outdir>/crops/*.jpg. Needs Pillow (with JPEG 2000 support for the Torquemada leaf).

archive.org file names are resolved through the metadata API rather than typed:
several items store names in Unicode NFD (e.g. a decomposed 'n' + combining tilde),
and a typed precomposed name returns a 146-byte 404 page that curl saves without
complaint -- which is how the 2026-09-24 fetch_corpus.sh silently lost
motolinia_historia.txt. Every download is size-checked below.
"""
import json, os, sys, urllib.parse, urllib.request

OUT = sys.argv[1] if len(sys.argv) > 1 else 'work'
for d in ('raw', 'pages', 'crops'): os.makedirs(os.path.join(OUT, d), exist_ok=True)

def get(url, path, minsize=5000):
    if os.path.exists(path) and os.path.getsize(path) >= minsize: return path
    with urllib.request.urlopen(url, timeout=300) as r, open(path, 'wb') as f: f.write(r.read())
    if os.path.getsize(path) < minsize: raise SystemExit(f'too small, probably an error page: {url}')
    return path

def files(item):
    with urllib.request.urlopen(f'https://archive.org/metadata/{item}/files', timeout=120) as r:
        return [f['name'] for f in json.load(r)['result']]

def dl(item, name):
    return f'https://archive.org/download/{item}/' + urllib.parse.quote(name)

# --- texts: (local name, archive.org item, suffix of the file wanted) ---------------
TEXTS = [
 ('icazbalceta1858_colI_scanA.txt', 'coleccindedocum01motogoog', '_djvu.txt'),   # Carta pp. 251-277
 ('icazbalceta1858_colI_scanB.txt', 'bub_gb_WJk6nlChEKYC', '_djvu.txt'),
 ('kingsborough1848_vIX.txt', 'AntiquitiesMexiv9King', '_djvu.txt'),            # Cronica Mexicana pp. 1-106
 ('ternaux1853_tezozomoc_t2.txt', 'histoiredumexiq02tezogoog', '_djvu.txt'),
 ('simeon1889_chimalpahin.txt', 'annalesdedoming00simgoog', '_djvu.txt'),       # 7e Relation pp. 157-159
 ('anales_museo_nacional_t1_1877.txt', 'analesdelmuseona00muse', '_djvu.txt'),
 ('aubin1893_codex1576.txt', 'histoiredelanati00aubi', '_djvu.txt'),
 ('historia_mexicanos_pinturas1891.txt', 'historia-de-los-mexicanos-por-sus-pinturas', '_djvu.txt'),
 ('anales_tlatelolco_berlin1948.txt', 'anales-y-codice-de-tlatelolco-edicion-de-berlin-barlow', '_djvu.txt'),  # in copyright: read locally, do not commit
 ('motolinia_historia.txt', 'fray-toribio-de-benavente-motolinia.-historia-de-los-indios-de-la-nueva-espana-ocr-1988', '_djvu.txt'),
]
for local, item, suf in TEXTS:
    name = next(n for n in files(item) if n.endswith(suf))
    get(dl(item, name), os.path.join(OUT, 'raw', local)); print('text ', local)

# --- page images: (local, item, how) ------------------------------------------------
TORQ = 'monarquia-indiana.-vol-i_202109'
TQZ = 'Monarquia Indiana. Vol I_jp2.zip'
PAGES = [
 ('icazbalceta1858_p254.jpg', dl('coleccindedocum01motogoog', 'page/n414.jpg').replace('%2F', '/')),
 ('tezozomoc1878_p517.jpg', dl('cronicamexicana00alvaiala', 'page/n548.jpg').replace('%2F', '/')),
 ('tezozomoc1997_p304.jpg', 'https://archive.org/download/hernando-de-alvarado-tezozomoc.-cronica-mexicana-ocr-1997/page/n278.jpg'),
 ('torquemada1723_vI_p186.jp2', dl(TORQ, TQZ) + '/' + urllib.parse.quote('Monarquia Indiana. Vol I_jp2/Monarquia Indiana. Vol I_0231.jp2')),
 ('telleriano_BnF_f39r.jpg', 'https://archive.org/download/codex-telleriano-remensis/page/n104.jpg'),  # mirror of gallica ark:/12148/btv1b8458267s
 ('telleriano_hamy1899_f39r.jpg', 'https://archive.org/download/ayer_507_5_t4_1899/page/n134.jpg'),
 ('vaticanusA_1485-87.jpg', 'https://archive.org/download/codex-vaticanus-a/page/n212.jpg'),
 ('simeon1889_p159.jpg', 'https://archive.org/download/annalesdedoming00simgoog/page/n208.jpg'),
]
for local, url in PAGES:
    get(url, os.path.join(OUT, 'pages', local)); print('page ', local)

# --- crops (pixel boxes on the full-size page images above) --------------------------
from PIL import Image
CROPS = [
 ('carta_p254_80400.jpg', 'icazbalceta1858_p254.jpg', (270, 2560, 3560, 3800)),
 ('tezozomoc1878_p517_setenta.jpg', 'tezozomoc1878_p517.jpg', (150, 1800, 2450, 2120)),
 ('tezozomoc1997_p304_sesenta.jpg', 'tezozomoc1997_p304.jpg', (350, 2230, 3050, 2560)),   # in copyright: do not commit
 ('torquemada1723_p186_72344.jpg', 'torquemada1723_vI_p186.jp2', (2050, 240, 4409, 2600)),
 ('telleriano_BnF_f39r_numerals.jpg', 'telleriano_BnF_f39r.jpg', (520, 560, 1010, 1080)),
 ('telleriano_BnF_f39r_gloss.jpg', 'telleriano_BnF_f39r.jpg', (340, 850, 1010, 1300)),
 ('telleriano_hamy1899_numerals.jpg', 'telleriano_hamy1899_f39r.jpg', (1900, 2050, 3150, 2450)),
 ('telleriano_hamy1899_cell1487.jpg', 'telleriano_hamy1899_f39r.jpg', (1150, 500, 3270, 2500)),
 ('vaticanusA_1487_numerals.jpg', 'vaticanusA_1485-87.jpg', (1750, 2700, 3100, 3250)),     # rights unclear: do not commit
 ('simeon1889_p159_nahuatl.jpg', 'simeon1889_p159.jpg', (470, 650, 1700, 1520)),
 ('simeon1889_p159_note.jpg', 'simeon1889_p159.jpg', (470, 3920, 3400, 4100)),
]
for out, src, box in CROPS:
    im = Image.open(os.path.join(OUT, 'pages', src)).convert('RGB')
    c = im.crop(box); c.thumbnail((1400, 1400)); c.save(os.path.join(OUT, 'crops', out), quality=85)
    print('crop ', out, c.size)
