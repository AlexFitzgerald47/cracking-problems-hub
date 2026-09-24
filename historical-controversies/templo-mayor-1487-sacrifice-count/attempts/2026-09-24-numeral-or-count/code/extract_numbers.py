#!/usr/bin/env python3
"""Extract quantities >= 400 from OCR'd Spanish colonial chronicles.

Parses Spanish number-words (with 16th-19th c. and OCR-tolerant spellings) and
digit-group forms. Emits the matched surface string alongside the parsed value so
every row can be hand-checked against the source.
"""
import re, sys, unicodedata, csv, os

def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

UNITS = {
 'un':1,'uno':1,'una':1,'dos':2,'tres':3,'cuatro':4,'quatro':4,'cinco':5,'seis':6,'seys':6,
 'siete':7,'ocho':8,'nueve':9,'nueue':9,'diez':10,'dies':10,'once':11,'onze':11,'doce':12,
 'doze':12,'trece':13,'treze':13,'catorce':14,'catorze':14,'quince':15,'quinze':15,
 'dieciseis':16,'diecisiete':17,'dieciocho':18,'diecinueve':19,
 'veinte':20,'beinte':20,'veynte':20,'treinta':30,'treynta':30,'cuarenta':40,'quarenta':40,
 'cincuenta':50,'cinquenta':50,'sesenta':60,'setenta':70,'fetenta':70,'ochenta':80,'noventa':90,
 'cien':100,'ciento':100,'doscientos':200,'docientos':200,'dozientos':200,'docientas':200,
 'doscientas':200,'trescientos':300,'trecientos':300,'trescientas':300,'trecientas':300,
 'cuatrocientos':400,'quatrocientos':400,'cuatrocientas':400,'quatrocientas':400,
 'quinientos':500,'quinientas':500,'seiscientos':600,'seyscientos':600,'seiscientas':600,
 'setecientos':700,'setecientas':700,'ochocientos':800,'ochocientas':800,
 'novecientos':900,'nouecientos':900,'novecientas':900,
}
WORDSET = set(UNITS)
MIL = {'mil','mill','mili'}
MILLON = {'millon','millones','millon,','milion'}
JOIN = {'y','e'}

TOKEN_RE = re.compile(r"[a-z]+|[0-9][0-9.,]*")

def parse_wordchain(toks):
    """Parse a chain of Spanish number tokens -> int, or None. Handles 'X mil Y'."""
    # split on mil
    if not toks: return None
    idx = [i for i,t in enumerate(toks) if t in MIL]
    if idx:
        i = idx[0]
        left, right = toks[:i], toks[i+1:]
        lv = parse_simple(left) if left else 1
        rv = parse_simple(right) if right else 0
        if lv is None or rv is None: return None
        return lv*1000 + rv
    return parse_simple(toks)

def parse_simple(toks):
    toks=[t for t in toks if t not in JOIN]
    if not toks: return 0
    tot=0
    for t in toks:
        if t not in UNITS: return None
        tot += UNITS[t]
    return tot

# Match a maximal run of number-words / 'y' / 'e' / digit groups
CHAIN_RE = re.compile(
    r"\b(?:(?:%s|mil|mill|mili|millon|millones|y|e)\b[\s,]*)+" % "|".join(sorted(WORDSET, key=len, reverse=True))
)
DIGIT_MIL_RE = re.compile(r"\b(\d{1,3})\s*(?:mil|mill)\b")
DIGIT_GROUP_RE = re.compile(r"\b(\d{1,3})[.,](\d{3})\b")

def norm_text(t):
    t = strip_acc(t.lower())
    t = t.replace('­','')
    # rejoin OCR hyphenated line breaks
    t = re.sub(r'-\s*\n\s*', '', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t

PERSON = re.compile(r"\b(hombres?|personas?|animas?|almas?|indios?|yndios?|cautiv|captiv|cautiu|captiu|esclavos?|esclauos?|soldados?|gentes?|vasallos?|basallos?|mexicanos?|guerreros?|calaver|calabern|cabezas?|cabecas?|sacrificad|muertos?|presos?|vecinos?|casados?|pobladores?|tarascos?|enemigos?|mugeres?|mujeres?|ninos?|companeros?)\b")

def scan(path, label):
    raw = open(path, encoding='utf-8', errors='replace').read()
    t = norm_text(raw)
    out=[]
    seen=set()
    def add(val, start, end, kind):
        if val is None or val < 400 or val > 100_000_000: return
        key=(start,end)
        if key in seen: return
        seen.add(key)
        ctx = re.sub(r'\s+',' ', t[max(0,start-120):min(len(t),end+120)])
        after = t[end:end+70]
        pre = t[max(0,start-40):start]
        if 400 <= val <= 1900 and re.search(r"an[o0]s?\s+(de\s+)?$|era\s+de\s+$|en\s+el\s+de\s+$", pre):
            return  # calendar year, not a quantity
        ptype = 'person' if PERSON.search(after) or PERSON.search(t[max(0,start-70):start]) else 'other'
        surf = re.sub(r'\s+',' ', t[start:end]).strip()
        out.append(dict(text=label, value=val, surface=surf, kind=kind,
                        subject=ptype, context=ctx))
    YEAR_CTX = re.compile(r"(an[o0]s?\s+(de\s+)?$|era\s+de\s+$|ano\s+de\s+mil)")
    for m in CHAIN_RE.finditer(t):
        toks = TOKEN_RE.findall(m.group(0))
        toks = [x for x in toks if x]
        # trim trailing joiners
        while toks and toks[-1] in JOIN: toks.pop()
        if not toks: continue
        if 'millon' in toks or 'millones' in toks:
            j=[i for i,x in enumerate(toks) if x in ('millon','millones')][0]
            lv=parse_wordchain(toks[:j]) or 1
            add(lv*1_000_000, m.start(), m.end(), 'words-millon'); continue
        v = parse_wordchain(toks)
        add(v, m.start(), m.end(), 'words')
    for m in DIGIT_MIL_RE.finditer(t):
        add(int(m.group(1))*1000, m.start(), m.end(), 'digit-mil')
    for m in DIGIT_GROUP_RE.finditer(t):
        add(int(m.group(1))*1000+int(m.group(2)), m.start(), m.end(), 'digit-group')
    return out

if __name__ == '__main__':
    files = sys.argv[1:]
    w = csv.writer(sys.stdout, delimiter='\t', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    w.writerow(['text','value','surface','kind','subject','context'])
    for f in files:
        label = os.path.basename(f).replace('.txt','')
        for r in scan(f, label):
            clean = lambda x: re.sub(r'\s+',' ',str(x)).replace('\t',' ')
            w.writerow([r['text'],r['value'],clean(r['surface']),r['kind'],r['subject'],clean(r['context'])])
