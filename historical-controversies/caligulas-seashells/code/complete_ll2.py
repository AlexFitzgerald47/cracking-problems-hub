import re,os,time,urllib.parse as up, urllib.request, concurrent.futures as cf
BASE="https://www.thelatinlibrary.com/"
OUT="/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad/ll_raw"
hdr={"User-Agent":"Mozilla/5.0 (research corpus build)"}
def fname(p):
    n=p.replace("/","__")
    if "." not in n.split("__")[-1]: n=n+".idx.html"
    return os.path.join(OUT,n)
def links_of(path, text):
    out=set()
    for href in re.findall(r'href="([^"]+)"',text,re.I):
        if href.startswith(("mailto:","javascript:","#")): continue
        try: u=up.urljoin(BASE+path,href)
        except Exception: continue
        if not u.startswith(BASE): continue
        u=u.split("#")[0][len(BASE):]
        if not u: continue
        last=u.rstrip("/").split("/")[-1]
        if u.lower().endswith((".html",".shtml",".htm")) or "." not in last: out.add(u.rstrip("/"))
    return out
def get(p):
    fn=fname(p)
    if os.path.exists(fn) and os.path.getsize(fn)>0: return p,None
    for attempt in range(3):
        try:
            raw=urllib.request.urlopen(urllib.request.Request(BASE+p,headers=hdr),timeout=30).read()
            try: t=raw.decode("utf-8")
            except UnicodeDecodeError: t=raw.decode("latin-1")
            open(fn,"w",encoding="utf-8").write(t); return p,None
        except Exception as e:
            if attempt==2: return p,str(e)
            time.sleep(1.5*(attempt+1))

new_total=0; errs={}
for rnd in range(8):
    frontier=set()
    for f in os.listdir(OUT):
        p=f.replace("__","/")
        if p.endswith(".idx.html"): p=p[:-9]
        try: t=open(os.path.join(OUT,f),encoding="utf-8",errors="replace").read()
        except Exception: continue
        frontier|=links_of(p,t)
    todo=[p for p in frontier if not os.path.exists(fname(p)) and p not in errs]
    print(f"round {rnd}: {len(todo)} new to fetch", flush=True)
    if not todo: break
    with cf.ThreadPoolExecutor(4) as ex:
        for p,e in ex.map(get,todo):
            if e: errs[p]=e
            else: new_total+=1
print("newly downloaded:",new_total,"persistent errors:",len(errs))
for p,e in list(errs.items())[:25]: print("  ERR",p,e)
print("total files:",len(os.listdir(OUT)))
