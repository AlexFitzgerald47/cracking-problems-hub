import os,re,json,html
SP="/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad"
base=os.path.join(SP,"corpus","perseus","data")
meta=json.load(open(os.path.join(SP,"perseus_meta.json")))
out=[]
for root,dirs,files in os.walk(base):
    for fn in sorted(files):
        if not fn.endswith(".xml") or "lat" not in fn: continue
        p=os.path.join(root,fn); rel=os.path.relpath(p,base)
        raw=open(p,encoding="utf-8",errors="replace").read()
        if "<text" not in raw: continue
        body=raw.split("<text",1)[1] if "<text" in raw else raw
        body=re.sub(r'(?is)<note[^>]*>.*?</note>',' ',body)
        # mark structural divisions with level+n
        def mk(m):
            tag=m.group(1).lower(); attrs=m.group(2)
            n=re.search(r'\bn="([^"]*)"',attrs); ty=re.search(r'\b(?:type|subtype)="([^"]*)"',attrs)
            lvl=re.search(r'div(\d)',tag)
            lv=lvl.group(1) if lvl else "m"
            return f" ‖{lv}={n.group(1) if n else ''}‖ "
        body=re.sub(r'(?i)<(div\d?|milestone)([^>]*?)/?>',mk,body)
        t=re.sub(r'<[^>]+>',' ',body); t=html.unescape(t)
        t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t).strip()
        if len(t)<200: continue
        key="/".join(rel.split(os.sep)[:2])
        m=meta.get(key,{})
        out.append({"corpus":"PERSEUS","id":rel,"author":m.get("author",""),"work":m.get("work",""),"text":t})
with open(os.path.join(SP,"corpus_txt","perseus.jsonl"),"w") as f:
    for d in out: f.write(json.dumps(d,ensure_ascii=False)+"\n")
print("works:",len(out),"tokens:",sum(len(d['text'].split()) for d in out))
