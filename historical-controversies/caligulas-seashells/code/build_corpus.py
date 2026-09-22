import os, re, sys, json, html, unicodedata
SP="/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad"
OUT=os.path.join(SP,"corpus_txt"); os.makedirs(OUT, exist_ok=True)

def strip_html(h):
    h=re.sub(r'(?is)<(script|style|head)[^>]*>.*?</\1>',' ',h)
    title=""
    m=re.search(r'(?is)<title[^>]*>(.*?)</title>',h)
    if m: title=re.sub(r'\s+',' ',html.unescape(re.sub('<[^>]+>','',m.group(1)))).strip()
    h=re.sub(r'(?i)<br[^>]*>','\n',h)
    h=re.sub(r'(?i)</(p|div|tr|h\d|li)>','\n',h)
    t=re.sub(r'<[^>]+>',' ',h)
    t=html.unescape(t)
    t=t.replace('\xa0',' ')
    t=re.sub(r'[ \t]+',' ',t)
    t=re.sub(r'\n\s*\n+','\n',t)
    return title, t.strip()

# ---- Latin Library ----
ll=[]
NAV=re.compile(r'(?i)(The Latin Library|The Classics Page|Medieval Latin|Christian Latin|Neo-Latin|The Miscellany)')
for fn in sorted(os.listdir(os.path.join(SP,"ll_raw"))):
    p=os.path.join(SP,"ll_raw",fn)
    raw=open(p,encoding="utf-8",errors="replace").read()
    title,txt=strip_html(raw)
    # drop trailing navigation lines
    lines=[l for l in txt.split("\n") if not NAV.fullmatch(l.strip())]
    txt="\n".join(lines)
    if len(txt)<200: continue
    ll.append((fn,title,txt))
print("LL texts kept:",len(ll))
with open(os.path.join(OUT,"latinlibrary.jsonl"),"w") as f:
    for fn,title,txt in ll:
        f.write(json.dumps({"corpus":"LL","id":fn,"title":title,"text":txt})+"\n")

# ---- Perseus canonical-latinLit ----
import xml.etree.ElementTree as ET
pe=[]
base=os.path.join(SP,"corpus","perseus","data")
for root,dirs,files in os.walk(base):
    for fn in files:
        if not fn.endswith(".xml"): continue
        if "lat" not in fn: continue
        p=os.path.join(root,fn)
        try:
            raw=open(p,encoding="utf-8",errors="replace").read()
        except Exception: continue
        if "<text" not in raw: continue
        title,_=strip_html(raw)
        # crude: strip tags but keep div n attributes as markers
        r=re.sub(r'(?is)<teiHeader.*?</teiHeader>',' ',raw)
        r=re.sub(r'(?i)<(div\d?|milestone)([^>]*)>', lambda m:" ‖"+(re.search(r'n="([^"]+)"',m.group(2)).group(1) if re.search(r'n="([^"]+)"',m.group(2)) else "")+"‖ ", r)
        r=re.sub(r'(?is)<note[^>]*>.*?</note>',' ',r)
        t=re.sub(r'<[^>]+>',' ',r)
        t=html.unescape(t); t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t).strip()
        if len(t)<200: continue
        pe.append((os.path.relpath(p,base),title,t))
print("Perseus texts kept:",len(pe))
with open(os.path.join(OUT,"perseus.jsonl"),"w") as f:
    for fn,title,txt in pe:
        f.write(json.dumps({"corpus":"PERSEUS","id":fn,"title":title,"text":txt})+"\n")
tot=sum(len(t.split()) for _,_,t in ll)
print("LL word tokens:",tot)
print("Perseus word tokens:",sum(len(t.split()) for _,_,t in pe))
