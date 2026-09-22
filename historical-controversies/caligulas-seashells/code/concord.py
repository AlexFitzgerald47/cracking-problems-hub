import json,re,os,sys
SP="/tmp/claude-0/-home-user-cracking-problems-hub/690785eb-da97-59b7-92cb-ad6e5d37866c/scratchpad"
MARK=re.compile(r'‖(\d|m)=([^‖]*)‖')
def citation(text,pos):
    # collect markers before pos, keep last value per level
    lv={}
    for m in MARK.finditer(text,0,pos):
        l,n=m.group(1),m.group(2)
        if l=="m": continue
        lv[l]=n
        for deeper in [str(x) for x in range(int(l)+1,6)]: lv.pop(deeper,None)
    return ".".join(lv[k] for k in sorted(lv) if lv[k])
def clean(s): return re.sub(r'\s+',' ',MARK.sub(' ',s)).strip()
def search(pattern,ctx=160):
    pat=re.compile(pattern,re.I); rows=[]
    for cf,corp in (("perseus.jsonl","PERSEUS"),("latinlibrary.jsonl","LL")):
        fp=os.path.join(SP,"corpus_txt",cf)
        if not os.path.exists(fp): continue
        for line in open(fp):
            d=json.loads(line); t=d["text"]
            for m in pat.finditer(t):
                s=max(0,m.start()-ctx); e=min(len(t),m.end()+ctx)
                rows.append({"corpus":d["corpus"],"id":d["id"],
                             "author":d.get("author","") or d.get("title","")[:60],
                             "work":d.get("work",""),
                             "cit":citation(t,m.start()) if d["corpus"]=="PERSEUS" else "",
                             "form":m.group(0),"ctx":clean(t[s:e])})
    return rows
if __name__=="__main__":
    rows=search(sys.argv[1], int(sys.argv[2]) if len(sys.argv)>2 else 160)
    json.dump(rows,open(sys.argv[3],"w"),ensure_ascii=False,indent=0)
    print("hits:",len(rows))
