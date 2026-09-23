import re, json, collections
src = open('foldlib.py').read()
exec(src)
def prep(t):
    return re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
DA=set('og er den det som til paa af han hans blev der ikke var sig kongen mod over efter fra alle sin sine jeg med de hvor'.split())
def is_da(s): return len(set(s.split()) & DA) >= 4
EAGLE = r'\b(ari|ara|arnar|erni|ernir|arna|arnir|ornu|orn|ornum|orns|gemlir)\b'
RAVEN = r'\b(hrafn|hrafns|hrafni|hrafnar|hrafna|hrafnum|krakr)\b'
WOLF  = r'\b(ulfr|ulfs|ulfi|ulfa|ulfar|ulfum|vargr|vargs|vargi|vargar|varga|freki|freka|frekr|geri|gera|ylgr)\b'
BLADE = r'\b(skera|skar|skaru|sker|skerr|skorinn|skorin|skorit|skorna|skornir|rista|reist|ristu|ristinn|ristit|ristin|hoggva|hjo|hjoggu|hogginn|kljufa|klauf|snida|sneid)\b'
FEED  = r'\b(metta|mettr|saddi|sadda|saddr|seddi|fylla|fyldi|gleddi|gladdi|gladdisk|gledja|soeddi|foeddi|foeda|foeddr|neyta|drekka|drakk|drukku|gaf|gefa|gefr|rjoda|raud|rauo|rudu|rodinn|vada|od|odu|slita|sleit|rifa|reif|bita|beit|bitu)\b'

def run(tag, paths):
    rows=[]
    for p in paths:
        t = fold(prep(open(p,encoding='utf-8',errors='replace').read()))
        for bn,bp in [('eagle',EAGLE),('raven',RAVEN),('wolf',WOLF)]:
            for m in re.finditer(bp,t):
                a=max(0,m.start()-70); b=min(len(t),m.end()+70); ctx=t[a:b]
                if is_da(ctx): continue
                rows.append((bn,m.group(0),bool(re.search(BLADE,ctx)),bool(re.search(FEED,ctx)),ctx))
    nb=sum(1 for r in rows if r[2]); nf=sum(1 for r in rows if r[3])
    print(f'{tag:10s} beast occurrences in ON verse = {len(rows):4d} | near BLADE verb = {nb:3d} | near FEED/COLOUR verb = {nf:3d}')
    return rows

A = run('scan-A', ['/tmp/be/corpus/dennorskislandsk03finn.txt','/tmp/be/corpus/dennorskislandsk04finn.txt'])
Brep = run('scan-B', ['/tmp/be/corpus/dennorskislandsk03finnu.txt','/tmp/be/corpus/dennorskislandsk04finnu.txt'])
print()
print('--- scan-B BLADE co-occurrences (independent replicate), for adjudication ---')
for bn,w,bl,fd,ctx in Brep:
    if bl: print(f'  {bn}:{w} | {ctx}')
