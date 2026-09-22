import os,re,json
base="/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad/corpus/perseus/data"
meta={}
for tg in sorted(os.listdir(base)):
    tgp=os.path.join(base,tg)
    if not os.path.isdir(tgp): continue
    gname=""
    ctsf=os.path.join(tgp,"__cts__.xml")
    if os.path.exists(ctsf):
        t=open(ctsf,encoding="utf-8",errors="replace").read()
        m=re.search(r'<ti:groupname[^>]*>(.*?)</ti:groupname>',t,re.S) or re.search(r'<groupname[^>]*>(.*?)</groupname>',t,re.S)
        if m: gname=re.sub(r'\s+',' ',m.group(1)).strip()
    for wk in sorted(os.listdir(tgp)):
        wkp=os.path.join(tgp,wk)
        if not os.path.isdir(wkp): continue
        title=""
        wf=os.path.join(wkp,"__cts__.xml")
        if os.path.exists(wf):
            t=open(wf,encoding="utf-8",errors="replace").read()
            m=re.search(r'<ti:title[^>]*>(.*?)</ti:title>',t,re.S) or re.search(r'<title[^>]*>(.*?)</title>',t,re.S)
            if m: title=re.sub(r'\s+',' ',m.group(1)).strip()
        meta[f"{tg}/{wk}"]={"author":gname,"work":title}
json.dump(meta,open("/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad/perseus_meta.json","w"),ensure_ascii=False,indent=0)
print(len(meta),"works")
for k in ["phi0836/phi002","phi0448/phi002","phi0978/phi001","phi1212/phi002","phi0474/phi043"]:
    print(k, meta.get(k))
