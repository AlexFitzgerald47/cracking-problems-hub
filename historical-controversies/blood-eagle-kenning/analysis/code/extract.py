import os, re, sys, json, unicodedata, collections

def load(p):
    return open(p, encoding='utf-8', errors='replace').read()

B1 = load(os.environ.get('SKJ','/tmp/be/corpus')+'/dennorskislandsk03finn.txt')
B2 = load(os.environ.get('SKJ','/tmp/be/corpus')+'/dennorskislandsk04finn.txt')

# --- OCR folding for Old Norse search -------------------------------------
THORN = ['|>','j>','{>','J3','f)','(>','i>','J>','£>',']>','>','J?','j?','|?']
def fold(t):
    t = t.replace('­','')
    for s in THORN: t = t.replace(s,'th')
    trans = {
      'þ':'th','Þ':'th','ð':'d','Ð':'d','ø':'o','Ø':'o','œ':'oe','Œ':'oe',
      'æ':'ae','Æ':'ae','ǫ':'o','Ǫ':'o','ö':'o','Ö':'o','å':'a','Å':'a',
      'á':'a','é':'e','í':'i','ó':'o','ú':'u','ý':'y','Á':'a','É':'e','Í':'i',
      'Ó':'o','Ú':'u','Ý':'y','ä':'a','ü':'u','ë':'e',
    }
    t = ''.join(trans.get(c,c) for c in t)
    t = t.lower()
    # common OCR digit-for-letter inside words
    t = re.sub(r'(?<=[a-z])5(?=[a-z])','d',t)
    t = re.sub(r'(?<=[a-z])9(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])0(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])6(?=[a-z])','o',t)
    t = re.sub(r'(?<=[a-z])1(?=[a-z])','l',t)
    t = re.sub(r'[^a-z0-9\s]',' ',t)
    t = re.sub(r'\s+',' ',t)
    return t

def hits(name, text, pattern, width=190):
    f = fold(text)
    out=[]
    for m in re.finditer(pattern, f):
        a=max(0,m.start()-width); b=min(len(f), m.end()+width)
        out.append((name, m.group(0), f[a:b]))
    return out

CORP = [('BI',B1), ('BII',B2)]

pats = {
 'skera': r'\b(sker|skerr|skera|skar|skaru|skorin|skorinn|skorit|skorna|skornir|skorid|skeri|skorinnar)\b',
 'rista': r'\b(rist|ristr|rista|reist|ristu|ristinn|ristit|ristin|ristnir|ristnar)\b',
 'bak':   r'\b(bak|baki|baks|boku|bokum|hryggr|hrygg|hryggjar|herdar|herdum|herda|hnakka|hnakki)\b',
 'eagle': r'\b(ari|ara|arnar|erni|ernir|arna|ornu|arnir|orn)\b',
}
res={}
for k,p in pats.items():
    allh=[]
    for nm,t in CORP: allh += hits(nm,t,p)
    res[k]=allh
    print(f'{k:8s} {len(allh)}')
json.dump({k:[list(x) for x in v] for k,v in res.items()}, open('hits.json','w'))
