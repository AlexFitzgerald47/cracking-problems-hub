import re,json
def norm(s):
    s=s.lower().replace("v","u").replace("j","i")
    s=re.sub(r'[^a-z ]',' ',s); s=re.sub(r'\s+',' ',s).strip()
    return s
def key(x):
    c=norm(x["ctx"]); f=norm(x["form"])
    i=c.find(f)
    if i<0: i=len(c)//2
    return (f, c[max(0,i-45):i+len(f)+45])
def dedupe(rows):
    seen={}; out=[]
    for x in rows:
        k=key(x)
        if k in seen:
            seen[k]["dups"].append(f'{x["corpus"]}:{x["id"]}')
            continue
        x=dict(x); x["dups"]=[]
        seen[k]=x; out.append(x)
    return out
