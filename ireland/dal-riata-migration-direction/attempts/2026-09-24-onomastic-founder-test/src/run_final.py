# -*- coding: utf-8 -*-
"""FINAL CONFIRMATORY RUN.  Predictions frozen in FREEZE-2.md before execution.

Tight Irish comparanda (single houses and single dynasties, >=146 name-tokens) give the
matched band; IONA is the positive control, PICT the negative, DALR the test set.
All groups subsampled to GRP_N tokens and scored against a reference subsampled to
REF_N tokens, so neither group size nor reference size can drive a difference.

Usage: python3 src/run_final.py <entries.jsonl> [--drop-nechtan]
"""
import json, sys, os, re, random, math, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, regions2, names2

YMIN, YMAX, GRP_N, REF_N, NDRAW, SEED = 550, 900, 146, 7500, 600, 20260924

TIGHT = {
    "ARMAGH": r"Ard Macha|Armagh", "CLONMACNOIS": r"Cluain Moccu Nóis|Clonmacnois",
    "KILDARE": r"Cell Dara|Kildare", "ULAID": r"Ulaid|Ulidia|\bUlster\b",
    "MIDE": r"\bMide\b|\bMeath\b", "CIANNACHTA": r"Cianacht|Ciannacht",
    "BREGA": r"Brega", "UI_MAINE": r"Uí Maine|Uí Maini",
}
NC = ("IONA", "DALR", "PICT")

def load(path, tagset, drop_nechtan=False):
    E = [json.loads(l) for l in open(path)]
    groups = collections.defaultdict(list); pool = []
    tight = {k: re.compile(v) for k, v in TIGHT.items()}
    for e in E:
        if not (YMIN <= e["year"] < YMAX): continue
        txt = e["text"]
        nm = [names2.skeleton(x) for x in names2.extract(txt)]
        if not nm: continue
        rec = {"year": e["year"], "names": nm, "id": e["id"]}
        reg = regions.region(txt, tagset)
        if drop_nechtan and reg == {"PICT"} and not re.search(
                r"Pict|Fortr|Cruithentúaith|Circinn|Athfhotla|Atholl|Dún Nechtain|"
                r"Dún Caillen|Duncalden|Monoth|Druim Alban", txt):
            reg = set()
        for g in reg: groups[g].append(rec)
        if not reg:
            pool.append(rec)
            for k, rx in tight.items():
                if rx.search(txt): groups[k].append(rec)
    return groups, pool

def toks(es): return [t for e in es for t in e["names"]]

def jsd(p, q):
    np_, nq = sum(p.values()), sum(q.values()); s = 0.0
    for k in set(p) | set(q):
        a, b = p.get(k, 0)/np_, q.get(k, 0)/nq; m = (a+b)/2
        if a: s += .5*a*math.log(a/m, 2)
        if b: s += .5*b*math.log(b/m, 2)
    return s

def score(ents, pool, rnd):
    own = set(id(e) for e in ents)
    ref = toks([e for e in pool if id(e) not in own]); g_all = toks(ents)
    if len(g_all) < GRP_N or len(ref) < REF_N: return None
    J, C, T = [], [], []
    for _ in range(NDRAW):
        rs = rnd.sample(ref, REF_N); R = names2.Reference(rs)
        g = rnd.sample(g_all, GRP_N)
        J.append(jsd(collections.Counter(g), collections.Counter(rs)))
        C.append(sum(1 for t in g if R.attested(t))/GRP_N)
        T.append(len(set(g))/GRP_N)
    f = lambda v: (sum(v)/len(v), sorted(v)[int(.025*len(v))], sorted(v)[int(.975*len(v))])
    # direction
    fi = {}
    for e in pool:
        if id(e) in own: continue
        for t in e["names"]: fi[t] = min(fi.get(t, 9999), e["year"])
    fg = {}
    for e in ents:
        for t in e["names"]: fg[t] = min(fg.get(t, 9999), e["year"])
    sh = [t for t in fg if t in fi]
    a = sum(1 for t in sh if fi[t] < fg[t]); b = sum(1 for t in sh if fg[t] < fi[t])
    return {"n_entries": len(ents), "n_tokens": len(g_all), "jsd": f(J), "cov": f(C),
            "ttr": f(T), "shared": len(sh), "pool_first": a, "group_first": b,
            "pool_first_rate": a/(a+b) if a+b else None}

def main(path, drop_nechtan=False):
    out = {}
    for tagset in ("STRICT", "WIDE"):
        rnd = random.Random(SEED)
        groups, pool = load(path, tagset, drop_nechtan)
        res = {"pool_tokens": len(toks(pool)), "groups": {}}
        for g in list(TIGHT) + list(NC):
            s = score(groups[g], pool, rnd)
            if s: res["groups"][g] = s
        band = [res["groups"][k]["jsd"][0] for k in TIGHT if k in res["groups"]]
        res["tight_band"] = {"min": min(band), "max": max(band), "n": len(band),
                             "mean": sum(band)/len(band)}
        c = res["groups"]
        den = c["PICT"]["jsd"][0] - c["IONA"]["jsd"][0]
        res["pos_DALR"] = (c["PICT"]["jsd"][0]-c["DALR"]["jsd"][0])/den if den else None
        rband = [res["groups"][k]["pool_first_rate"] for k in TIGHT if k in res["groups"]]
        res["tight_dir_band"] = {"min": min(rband), "max": max(rband),
                                 "mean": sum(rband)/len(rband)}
        out[tagset] = res
    return out

if __name__ == "__main__":
    dn = "--drop-nechtan" in sys.argv
    res = main(sys.argv[1], dn)
    json.dump(res, open("results/final%s.json" % ("_nonechtan" if dn else ""), "w"), indent=1)
    for ts, r in res.items():
        print("===== %s%s   Irish pool %d tokens | groups->%d tok, ref->%d tok, %d draws ====="
              % (ts, " (Nechtan dropped)" if dn else "", r["pool_tokens"], GRP_N, REF_N, NDRAW))
        print("  group          ent  tok     JSD [95%]            cov     TTR    shared  pool-1st")
        for g in list(TIGHT) + list(NC):
            if g not in r["groups"]: continue
            d = r["groups"][g]
            tag = {"IONA": "  <-- POS control", "DALR": "  <-- TEST SET",
                   "PICT": "  <-- NEG control"}.get(g, "")
            print("  %-13s %4d %4d  %.4f [%.4f,%.4f]  %.3f  %.3f   %4d   %.3f%s"
                  % (g, d["n_entries"], d["n_tokens"], *d["jsd"], d["cov"][0], d["ttr"][0],
                     d["shared"], d["pool_first_rate"], tag))
        b = r["tight_band"]
        print("  tight Irish JSD band (%d groups): %.4f - %.4f  (mean %.4f)"
              % (b["n"], b["min"], b["max"], b["mean"]))
        for g in NC:
            v = r["groups"][g]["jsd"][0]
            print("     %-5s %.4f  -> %s" % (g, v, "INSIDE band" if b["min"] <= v <= b["max"]
                                             else ("ABOVE band" if v > b["max"] else "BELOW band")))
        print("  pos(DALR)  PICT=0, IONA=1 : %s" % ("%.3f" % r["pos_DALR"]))
        db = r["tight_dir_band"]
        print("  tight Irish pool-first-rate band: %.3f - %.3f (mean %.3f)"
              % (db["min"], db["max"], db["mean"]))
