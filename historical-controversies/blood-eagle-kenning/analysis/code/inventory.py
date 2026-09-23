import re, json, collections
exec(open('extract.py').read().split("CORP = ")[0])  # reuse fold(), loads B1,B2

# ---- OCR-tolerant beast lexemes -------------------------------------------
# pre-fold repairs for ǫ mis-OCR'd as p/q/9/g/0 in 'ǫrn'
def prep(t):
    t = re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
    return t

EAGLE = r'\b(ari|ara|arnar|arnari|erni|ernir|arna|arnir|ornu|orn|ornum|orns|gemlir)\b'
RAVEN = r'\b(hrafn|hrafns|hrafni|hrafnar|hrafna|hrafnum|hrafnninn|krakr)\b'
WOLF  = r'\b(ulfr|ulfs|ulfi|ulfa|ulfar|ulfum|vargr|vargs|vargi|vargar|varga|freki|freka|frekr|geri|gera|ylgr)\b'
# eagle/corpse-bird kennings (wound-/corpse- + bird)
KENN  = r'\b(benmar|benmarr|sargammr|valgammr|hraegammr|blodgagl|benglar|bengagl|hraefugl|valfugl|nagl|hraeva)\w*\b'

VERBS = {
 'feed/sate'   : r'\b(metta|mettr|mettir|saddi|sadda|saddr|saddir|seddi|sedda|fylla|fyldi|fylldi|gleddi|gladdi|gladdisk|gledja|soeddi|soeda|foeddi|foeda|foeddr|foedir|foedi|neyta|nasa)\b',
 'drink'       : r'\b(drekka|drakk|drukku|drukkinn|dreypa)\b',
 'tear/rend'   : r'\b(slita|sleit|slitu|slitinn|rifa|reif|rifu|rifinn|taeta|teitr|tygdi|sundr)\b',
 'redden/stain': r'\b(rjoda|raud|rudu|rodinn|rodin|rodit|roda|dreyra|dreyrdi|dreyrugr|blodugr)\b',
 'wade/tread'  : r'\b(vada|od|odu|vodu|vadinn|trada|troda)\b',
 'cry/scream'  : r'\b(gjalla|gall|gullu|gol|gala|gelr|hjalmar|skrikja|klaka)\b',
 'fly/come/go' : r'\b(fljuga|flaug|flugu|flygr|kom|koma|komu|gekk|ganga|for|foru|ferr|sotti|soekja|hljop|rann)\b',
 'bite'        : r'\b(bita|beit|bitu|bitr|bitinn)\b',
 'BLADE-CUT'   : r'\b(skera|skar|skaru|sker|skerr|skorinn|skorin|skorit|skorna|rista|reist|ristu|ristinn|ristit|ristin|hoggva|hjo|hjoggu|hogginn|kljufa|klauf|snida|sneid)\b',
}
DA=set('og er den det som til paa af han hans blev der ikke var sig kongen mod over efter fra alle sin sine jeg med de hvor jer den'.split())
def is_da(s):
    return len(set(s.split()) & DA) >= 4

WIN = 70   # +/- chars ~ one clause
rows=[]
for nm, raw in [('BI',B1),('BII',B2)]:
    f = fold(prep(raw))
    for bname, bpat in [('eagle',EAGLE),('raven',RAVEN),('wolf',WOLF),('bird-kenning',KENN)]:
        for m in re.finditer(bpat, f):
            a=max(0,m.start()-WIN); b=min(len(f), m.end()+WIN)
            ctx=f[a:b]
            if is_da(ctx): continue      # Old Norse verse only
            vs=[k for k,p in VERBS.items() if re.search(p,ctx)]
            rows.append(dict(vol=nm,beast=bname,word=m.group(0),verbs=vs,ctx=ctx,pos=m.start()))

print('Old Norse beast-of-battle occurrences found:', len(rows))
print('  by beast:', dict(collections.Counter(r['beast'] for r in rows)))
cnt=collections.Counter()
for r in rows:
    for v in r['verbs']: cnt[v]+=1
tot=len(rows)
print(f'\nVERB CLASS within +/-{WIN} chars of a beast lexeme (n={tot} occurrences):')
for v,c in cnt.most_common():
    print(f'  {v:14s} {c:4d}   {100*c/tot:5.1f}%')
json.dump(rows, open('beast_rows.json','w'))
