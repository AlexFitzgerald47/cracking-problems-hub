# -*- coding: utf-8 -*-
"""EXPLORATORY (derived after seeing the term decomposition), then tested out of sample.

The term table showed the Scottish tag is not homogeneous.  Fine Argyll/Dal Riata
topography (Kintyre, Skye, Applecross, Kingarth, Dunadd, Cenel Loairn, Dal Riata
itself) behaves differently from mentions of Iona, which behave differently again
from Pictland.  A chronicle physically leaving Iona predicts something sharper
than "less Scottish news": it predicts the loss of LOCAL DETAIL specifically,
while Iona -- a famous house whose abbots' obits an Irish annalist would still
receive -- keeps being named.

Statistic: among entries that carry ANY Scottish tag, the share carrying local
Argyll detail.  This is scale-free with respect to everything outside the
Scottish class, so no movement in Irish or Anglo-Saxon reporting can drive it.
"""
import sys, os, json, re, collections
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer, changepoint as cp

LOCAL = re.compile(r"Dál Riat|Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|Mag Luinge|"
                   r"Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|Kingarth|"
                   r"Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|Druim Alban|"
                   r"Iardoman|Athfhotla|Circinn|Dún Nechtain")

REC=[json.loads(l) for l in open("data/entries.jsonl")]
USE=[r for r in REC if not r["is_kalend"] and r["n_words"]>=3]
for r in USE:
    r["tags"]=gazetteer.tag(r["text"]); r["local"]=bool(LOCAL.search(r["text"]))

def scot_series(w, lo, hi):
    yk=collections.Counter(); yn=collections.Counter()
    for r in USE:
        if r["witness"]==w and lo<=r["year"]<hi and r["tags"]["SCOT"]:
            yn[r["year"]]+=1
            if r["local"]: yk[r["year"]]+=1
    ys=sorted(yn); return ys,[yk[y] for y in ys],[yn[y] for y in ys]

out={}
y,k,n=scot_series("AU",550,1000)
print("AU Scottish-tagged entries 550-1000: %d, of which local-detail %d"%(sum(n),sum(k)))
s,c,l,r=cp.scan(y,k,n,min_entries=25)
nl=cp.permutation_null(y,k,n,n_perm=5000,min_entries=25)
bt=cp.bootstrap_cut(y,k,n,n_boot=2000,min_entries=25)
out["AU_local_share_of_scottish"]={"cut":c,"stat":s,
    "left":{"k":l[0],"n":l[1],"rate":l[0]/l[1]},"right":{"k":r[0],"n":r[1],"rate":r[0]/r[1]},
    "null":nl,"bootstrap_cut":bt}
print("AU local-share-of-Scottish: cut=%s stat=%.2f  %d/%d=%.3f -> %d/%d=%.3f  p=%.4f  boot95=[%s,%s]  null p95=%.2f"
      %(c,s,l[0],l[1],l[0]/l[1],r[0],r[1],r[0]/r[1],nl["p"],bt["lo95"],bt["hi95"],nl["null_p95"]))

# profile / support interval
K,N=sum(k),sum(n); base=cp._ll(K,N); prof=[]; ck=cn=0
for i in range(len(y)-1):
    ck+=k[i]; cn+=n[i]
    if cn<25 or N-cn<25: continue
    prof.append((y[i+1],2*(cp._ll(ck,cn)+cp._ll(K-ck,N-cn)-base)))
bestv=max(p[1] for p in prof); supp=[cc for cc,ss in prof if ss>=bestv-3.84]
out["AU_local_support_interval"]=[min(supp),max(supp)]
print("   chi2(1) support interval = [%d, %d]"%(min(supp),max(supp)))

# ---- out-of-sample: the other three witnesses, at AU's fitted cut -----------
print("\nOut-of-sample tests of the same within-class statistic (cut fixed at AU's %d):"%c)
oos={}
for w,(lo,hi) in {"CS":(550,1000),"AI":(550,1000),"AT":(550,767)}.items():
    yy,kk,nn=scot_series(w,lo,hi)
    pre_k=sum(kk[i] for i in range(len(yy)) if yy[i]<c); pre_n=sum(nn[i] for i in range(len(yy)) if yy[i]<c)
    po_k=sum(kk[i] for i in range(len(yy)) if yy[i]>=c); po_n=sum(nn[i] for i in range(len(yy)) if yy[i]>=c)
    p = cp.fisher_exact_greater(pre_k,pre_n-pre_k,po_k,po_n-po_k) if pre_n and po_n else None
    oos[w]={"pre":[pre_k,pre_n],"post":[po_k,po_n],"fisher_p_greater":p}
    print("  %-3s pre %d/%d=%s  post %d/%d=%s  fisher p=%s"%(w,pre_k,pre_n,
        "%.3f"%(pre_k/pre_n) if pre_n else "-",po_k,po_n,"%.3f"%(po_k/po_n) if po_n else "-",
        "%.4f"%p if p is not None else "undefined (empty cell)"))
# CS across its own lacuna -- the only clean independent comparison
yy,kk,nn=scot_series("CS",550,1000)
a=sum(kk[i] for i in range(len(yy)) if yy[i]<723); b=sum(nn[i] for i in range(len(yy)) if yy[i]<723)
cx=sum(kk[i] for i in range(len(yy)) if yy[i]>=804); d=sum(nn[i] for i in range(len(yy)) if yy[i]>=804)
pv=cp.fisher_exact_greater(a,b-a,cx,d-cx) if b and d else None
oos["CS_across_lacuna"]={"pre":[a,b],"post":[cx,d],"fisher_p_greater":pv}
print("  CS across its own 723-803 lacuna: pre %d/%d=%s  post %d/%d=%s  fisher p=%s"
      %(a,b,"%.3f"%(a/b) if b else "-",cx,d,"%.3f"%(cx/d) if d else "-","%.4f"%pv if pv is not None else "-"))
out["out_of_sample"]=oos
json.dump(out,open("results/local.json","w"),indent=1)
print("\nwrote results/local.json")
