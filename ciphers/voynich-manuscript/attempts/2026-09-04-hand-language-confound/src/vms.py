"""Parse the ZL3b transliteration into pages with their scribal hand and
Currier language labels, and clean the EVA text.

The ZL (Zandbergen-Landini) transliteration carries per-page metadata in its
page headers, including $H (scribal hand, after Currier's hand identification)
and $L (Currier language A or B). That metadata is what makes the confound
between the two visible and testable.
"""
import re, os, collections

SRC = ('/home/user/matthewdgreen/cipher_benchmark/benchmark/unsolved/sources/'
       'voynich/transcriptions/ZL3b-n.txt')
HDR = re.compile(r'^<(f[^>\s]+)>\s+<!\s*([^>]*)>')
LOC = re.compile(r'^<(f[^>\s;]+)[.;]([^>]*)>\s*(.*)$')


def clean(line):
    """EVA line -> list of words.

    '.' and ',' separate words (',' marks an uncertain space); '<...>' are
    markers and comments; '[a:b]' is an ambiguous reading, for which the first
    alternative is taken; '?' and '!' mark unreadable/placeholder material.
    """
    s = re.sub(r'<[^>]*>', '', line)
    s = re.sub(r'\[([^\]:]*)[:][^\]]*\]', r'\1', s)
    s = s.replace('!', '').replace('%', '')
    words = re.split(r'[.,\s]+', s)
    return [w for w in words if w and '?' not in w]


def load(path=SRC):
    pages, cur = {}, None
    for ln in open(path, errors='replace'):
        ln = ln.rstrip('\n')
        m = HDR.match(ln)
        if m and '$Q=' in m.group(2):
            cur = m.group(1)
            pages[cur] = {'page': cur,
                          'attrs': dict(re.findall(r'\$([A-Z])=(\S+)', m.group(2))),
                          'words': []}
            continue
        m2 = LOC.match(ln)
        if m2 and m2.group(1) in pages:
            pages[m2.group(1)]['words'].extend(clean(m2.group(3)))
    for p in pages.values():
        p['hand'] = p['attrs'].get('H', '?')
        p['lang'] = p['attrs'].get('L', 'none')
        p['n_words'] = len(p['words'])
    return pages


def contingency(pages):
    return collections.Counter((p['lang'], p['hand']) for p in pages.values())
