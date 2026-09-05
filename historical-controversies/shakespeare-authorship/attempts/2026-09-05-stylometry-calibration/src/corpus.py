"""Builds the play corpus from dracor-org/engdracor (TEI, from EarlyPrint/TCP).

Only single-author plays are kept, and only authors with enough plays to be
trained on. Anonymous plays and Seneca (translations, not original English
composition) are excluded.

Note on Shakespeare: engdracor contains none of his plays. They appear in the
metadata CSV but have no TEI file. This is left as-is rather than patched from
another repository, because mixing editions would confound authorship with
spelling and normalisation convention - which is exactly the kind of artefact
this attempt exists to measure.
"""
import os, re, csv, json, collections

ROOT = '/home/user/dracor-org/engdracor'
CACHE = os.path.join(os.path.dirname(__file__), '..', 'data', 'corpus.json')
EXCLUDE = {'Anon.', 'Seneca, Lucius Annaeus', ''}
MIN_PLAYS = 6

TAG = re.compile(r'<[^>]+>')
WORD = re.compile(r"[a-z']+")


def _text(path):
    s = open(path, errors='replace').read()
    body = s.split('<body', 1)[-1]
    body = re.sub(r'<teiHeader.*?</teiHeader>', ' ', body, flags=re.S)
    body = re.sub(r'<speaker>.*?</speaker>', ' ', body, flags=re.S)
    body = re.sub(r'<stage>.*?</stage>', ' ', body, flags=re.S)
    body = TAG.sub(' ', body)
    body = body.replace('&amp;', '&').replace('&apos;', "'")
    return WORD.findall(body.lower())


def _date(path):
    s = open(path, errors='replace').read()[:8000]
    m = re.search(r'<date type="creation_date"[^>]*>\s*(\d{4})', s)
    if not m:
        m = re.search(r'<date type="publication_date"[^>]*>\s*(\d{4})', s)
    if not m:
        m = re.search(r'<date[^>]*>\s*(\d{4})', s)
    return int(m.group(1)) if m else None


def build():
    idx = dict(re.findall(r'sourceid="([^"]+)" slug="([^"]+)"',
                          open(os.path.join(ROOT, 'index.xml')).read()))
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'meta', 'author_titles.csv'))))
    plays = []
    for r in rows:
        a = r['authors'].strip()
        if ';' in a or a in EXCLUDE:
            continue
        slug = idx.get(r['id'])
        if not slug:
            continue
        path = os.path.join(ROOT, 'tei', slug + '.xml')
        if not os.path.exists(path):
            continue
        words = _text(path)
        if len(words) < 5000:
            continue
        plays.append({'id': r['id'], 'slug': slug, 'author': a,
                      'title': r['title'][:80], 'year': _date(path),
                      'n_words': len(words), 'words': words})
    counts = collections.Counter(p['author'] for p in plays)
    plays = [p for p in plays if counts[p['author']] >= MIN_PLAYS]
    return plays


def load(rebuild=False):
    if os.path.exists(CACHE) and not rebuild:
        return json.load(open(CACHE))
    plays = build()
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(plays, open(CACHE, 'w'))
    return plays
