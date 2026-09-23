import os, re, json, collections
exec(open('foldlib.py').read())
def prep(t): return re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
DA=set('og er den det som til paa af han hans blev der ikke var sig kongen mod over efter fra alle sin sine jeg med de hvor'.split())
def is_da(s): return len(set(s.split()) & DA) >= 4
P=os.environ.get('SKJ','/tmp/be/corpus')+'/dennorskislandsk0%sfinn.txt'
SCANS={'A':[P%3,P%4],'B':[(P%3).replace('finn','finnu'),(P%4).replace('finn','finnu')]}

BEAST = r'\b(ari|ara|arnar|erni|ernir|arna|arnir|ornu|orn|ornum|orns|hrafn|hrafns|hrafni|hrafnar|hrafna|hrafnum|ulfr|ulfs|ulfi|ulfa|ulfar|ulfum|vargr|vargs|vargi|vargar|varga|freki|freka|geri|gera|ylgr)\b'
BACK  = r'\b(bak|baki|baks)\b'
IDIOM = r'\ba bak\b|\bbak\b(?=\s+(ord|malum|molum|maelum))|\ba baki\b|\bat baki\b'
WEAPON= r'\b(sverd|sverdi|hjorr|hjor|egg|eggjum|eggjar|spjot|spjoti|fleinn|flein|oxi|oxar|geirr|geir|geira|brandr|brand|malmr|odd|oddi|knifr|knifi|vapn|vapnum)\b'
BLADE = r'\b(skera|skar|skaru|sker|skerr|skorinn|skorin|skorit|skorna|skornir|rista|reist|ristu|ristinn|ristit|ristin|hoggva|hjo|hjoggu|hogginn|kljufa|klauf|snida|sneid)\b'

for tag,paths in SCANS.items():
    T=''.join(fold(prep(open(p,encoding='utf-8',errors='replace').read())) for p in paths)
    # --- bak enumeration, ON verse only
    hits=[]
    for m in re.finditer(BACK,T):
        a=max(0,m.start()-70); b=min(len(T),m.end()+70); ctx=T[a:b]
        if is_da(ctx): continue
        hits.append(ctx)
    idiom=[c for c in hits if re.search(IDIOM,c)]
    withbeast=[c for c in hits if re.search(BEAST,c)]
    withweap=[c for c in hits if re.search(WEAPON,c)]
    withblade=[c for c in hits if re.search(BLADE,c)]
    print(f'== SCAN {tag} ==  `bak/baki/baks` in Old Norse verse: {len(hits)}')
    print(f'   of which idiomatic (a bak / at baki / ganga a bak ordum): {len(idiom)}  ({100*len(idiom)/max(1,len(hits)):.0f}%)')
    print(f'   co-occurring with a BEAST-OF-BATTLE lexeme            : {len(withbeast)}')
    print(f'   co-occurring with a WEAPON noun                       : {len(withweap)}')
    print(f'   co-occurring with a BLADE verb                        : {len(withblade)}')
    for c in withbeast: print(f'      BEAST+BAK: ...{c}...')
    print()
