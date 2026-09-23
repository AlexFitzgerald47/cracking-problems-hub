import os, re, csv
exec(open('foldlib.py').read())
def prep(t): return re.sub(r'\b[pq9g0O]rn(a|ar|i|u|um|s)?\b', lambda m:'orn'+(m.group(1) or ''), t)
DA=set('og er den det som til paa af han hans blev der ikke var sig kongen mod over efter fra alle sin sine jeg med de hvor'.split())
def is_da(s): return len(set(s.split()) & DA) >= 4
P=os.environ.get('SKJ','/tmp/be/corpus')+'/dennorskislandsk0%sfinn.txt'
BEAST=r'\b(ari|ara|arnar|erni|ernir|arna|arnir|ornu|orn|ornum|orns|hrafn|hrafns|hrafni|hrafnar|hrafna|hrafnum|ulfr|ulfs|ulfi|ulfa|ulfar|ulfum|vargr|vargs|vargi|vargar|varga|freki|freka|geri|gera|ylgr|sargammr|hergamr|gamr|nagr|skari)\b'
BLADE=r'\b(skera|skar|skaru|sker|skerr|skorinn|skorin|skorit|skorna|skornir|rista|reist|ristu|ristinn|ristit|ristin|hoggva|hjo|hjoggu|hogginn|kljufa|klauf|snida|sneid)\b'

rows=[]
for tag,suf in [('A','finn'),('B','finnu')]:
    T=''.join(fold(prep(open((P%v).replace('finn',suf),encoding='utf-8',errors='replace').read())) for v in (3,4))
    for m in re.finditer(BEAST,T):
        a=max(0,m.start()-70); b=min(len(T),m.end()+70); c=T[a:b]
        if is_da(c): continue
        if re.search(BLADE,c):
            rows.append(dict(scan=tag, beast=m.group(0),
                             blade=re.search(BLADE,c).group(0), context=c.strip()))
with open('beast_blade_adjudication.tsv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['scan','beast','blade','verdict','reason','context'],delimiter='\t')
    w.writeheader()
    for r in rows:
        r['verdict']=''; r['reason']=''
        w.writerow(r)
print('emitted', len(rows), 'rows to beast_blade_adjudication.tsv')
