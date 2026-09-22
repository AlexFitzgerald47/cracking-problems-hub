import re, os, sys, time, queue, threading, urllib.parse as up, urllib.request
BASE="https://www.thelatinlibrary.com/"
OUT=sys.argv[1]
os.makedirs(OUT, exist_ok=True)
seen=set(); lock=threading.Lock(); q=queue.Queue()
q.put("indices.html"); seen.add("indices.html")
hdr={"User-Agent":"Mozilla/5.0 (research corpus build; philology)"}
count=[0]
def norm(base, href):
    if href.startswith(("mailto:","javascript:","#")): return None
    u=up.urljoin(BASE+base, href)
    if not u.startswith(BASE): return None
    u=u.split("#")[0]
    p=u[len(BASE):]
    if not p or not p.lower().endswith((".html",".shtml",".htm")): return None
    return p
def worker():
    while True:
        try: path=q.get(timeout=8)
        except queue.Empty: return
        fn=os.path.join(OUT, path.replace("/","__"))
        try:
            if os.path.exists(fn) and os.path.getsize(fn)>0:
                html=open(fn,encoding="utf-8",errors="replace").read()
            else:
                req=urllib.request.Request(BASE+path, headers=hdr)
                raw=urllib.request.urlopen(req, timeout=30).read()
                try: html=raw.decode("utf-8")
                except UnicodeDecodeError: html=raw.decode("latin-1")
                open(fn,"w",encoding="utf-8").write(html)
                with lock:
                    count[0]+=1
                    if count[0]%200==0: print(count[0], "files", q.qsize(), "queued", flush=True)
            for href in re.findall(r'href="([^"]+)"', html, re.I):
                n=norm(path, href)
                if n:
                    with lock:
                        if n not in seen:
                            seen.add(n); q.put(n)
        except Exception as e:
            print("ERR", path, e, flush=True)
        finally:
            q.task_done()
ths=[threading.Thread(target=worker,daemon=True) for _ in range(4)]
[t.start() for t in ths]
[t.join() for t in ths]
print("DONE files downloaded:", count[0], "urls seen:", len(seen))
