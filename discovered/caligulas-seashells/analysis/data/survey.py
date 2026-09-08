#!/usr/bin/env python3
"""
Caligula's Seashells — lexical base-rate survey.
Session 2026-09-07. Reproduces every count in
analysis/2026-09-07-concha-umbilicus-survey.md

Corpora (both cloned from GitHub; no other egress was available this session):
  A. https://github.com/cltk/latin_text_latin_library  (2,141 .txt files)
  B. https://github.com/cltk/latin_text_tesserae       (748 .tess files, 46.7M chars,
                                                        incl. the complete Pliny NH)

Usage:  python3 survey.py /path/to/latin_text_latin_library /path/to/latin_text_tesserae/texts
"""
import os, re, sys, collections

def load_ll(root):
    for d, _, fs in os.walk(root):
        for f in fs:
            if f.endswith('.txt'):
                p = os.path.join(d, f)
                yield os.path.relpath(p, root), open(p, encoding='utf-8', errors='replace').read()

def load_tess(root):
    """Tesserae lines are '<citation> text'; keep the citation tag for reference lookup."""
    for f in sorted(os.listdir(root)):
        if not f.endswith('.tess'):
            continue
        raw = open(os.path.join(root, f), encoding='utf-8', errors='replace').read()
        yield f, re.sub(r'^<[^>]*>\s*', '', raw, flags=re.M)

CONCHA = re.compile(r'\bconch(a|ae|am|as|arum|is|ula|ulae|ulas|ulis)\b', re.I)
UMBILIC = re.compile(r'\bumbilic\w*', re.I)
MUSCULUS = re.compile(r'\bmuscul(us|i|um|o|os|orum|is)\b', re.I)

# A concha window counts as "shell-context" for umbilicus only if it is genuinely marine.
MARINE = re.compile(r'conch|litor|litus|mar[ie]s?\b|ostre|cochl|coclea|testa\b|harena|arena', re.I)
# Woods's reading requires concha to be able to denote a vessel. This is the falsifier.
SHIP = re.compile(r'\b(navi|nave|navis|naves|navem|navib|rat[ei]s|scaph|lemb|carin|puppi'
                  r'|prora|remig|classi|liburn|cumba|linter)', re.I)
# "Is concha a worthless-object word?" — luxury/commodity association.
VALUE = re.compile(r'margarit|unio\b|unione|unionum|unionib|purpur|murice|murex|conchyli'
                   r'|gemm|aur[oi]\b|pretio|divit|luxuri', re.I)

def scan(corpus, rx, ctx=240):
    hits = []
    for name, text in corpus:
        for m in rx.finditer(text):
            hits.append((name, m.group(0),
                         ' '.join(text[max(0, m.start()-ctx):m.end()+ctx].split())))
    return hits

def report(label, hits, extra=()):
    print(f'\n### {label}: {len(hits)} hits in {len(set(h[0] for h in hits))} texts')
    for sub_label, pred in extra:
        sub = [h for h in hits if pred(h[2])]
        print(f'    {sub_label}: {len(sub)}')
        for name, word, ctxt in sub:
            print(f'      * {name} | {word}\n        {ctxt[:300]}')

if __name__ == '__main__':
    ll_root, tess_root = sys.argv[1], sys.argv[2]
    for corpus_name, loader, root in (('LATIN LIBRARY', load_ll, ll_root),
                                      ('TESSERAE', load_tess, tess_root)):
        corpus = list(loader(root))
        print(f'\n{"="*70}\n{corpus_name}: {len(corpus)} texts, '
              f'{sum(len(t) for _, t in corpus):,} chars\n{"="*70}')
        conchae = scan(corpus, CONCHA)
        report('concha (noun)', conchae, [
            ('WOODS FALSIFIER — windows containing ship vocabulary',
             lambda c: bool(SHIP.search(c)))])
        print(f'    concha windows with pearl/purple/luxury vocabulary: '
              f'{sum(1 for h in conchae if VALUE.search(h[2]))} / {len(conchae)}')
        report('umbilic*', scan(corpus, UMBILIC), [
            ('RARITY TEST — windows in a marine/shore context',
             lambda c: bool(MARINE.search(c)))])
        musculi = scan(corpus, MUSCULUS)
        print(f'\n### musculus: {len(musculi)} hits in '
              f'{len(set(h[0] for h in musculi))} texts '
              f'(sense classification is manual; see the analysis document)')
        print(collections.Counter(h[0] for h in musculi).most_common(10))
