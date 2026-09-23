import os, re
exec(open('foldlib.py').read())
def prep(t): return re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
P=os.environ.get('SKJ','/tmp/be/corpus')+'/dennorskislandsk0%sfinn.txt'
for tag,suf in [('A','finn'),('B','finnu')]:
    T=''.join(fold(prep(open((P%v).replace('finn',suf),encoding='utf-8',errors='replace').read())) for v in (3,4))
    # the CARRION formula: victim under the bird's talons/claws/feet
    TAL = r'\b(greipar|greipum|greip|klo|klom|klor|ilthorna|ilthornum|ilthorn|fotum|foeti|fot|klaufum)\b'
    BIRD= r'\b(ara|arnar|erni|orn|ornum|hergamr|gamr|gammi|hrafns|hrafna|nagr|nagrs|skari)\b'
    UND = r'\b(und|undir|undan)\b'
    n=0; ex=[]
    for m in re.finditer(UND,T):
        a=max(0,m.start()-40); b=min(len(T),m.end()+90); c=T[a:b]
        if re.search(BIRD,c) and re.search(TAL,c):
            n+=1; ex.append(c)
    print(f'scan-{tag}: "under the bird-of-prey\'s talons/feet" formula occurrences = {n}')
    if tag=='A':
        for c in ex: print('   ...'+c+'...')
