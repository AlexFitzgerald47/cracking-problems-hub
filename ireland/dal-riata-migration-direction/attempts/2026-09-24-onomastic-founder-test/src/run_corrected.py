# -*- coding: utf-8 -*-
"""CORRECTED CONFIRMATORY RUN.  Same frozen predictions (FREEZE.md), corrected pipeline.

Every group -- six Irish provinces and the three north-channel groups -- is scored by
ONE identical out-of-sample procedure, with group size AND reference size held equal:

    reference = (all in-window entries with no north-channel marker) minus this group's
                own entries, subsampled to REF_N tokens
    group     = this group's tokens, subsampled to GRP_N tokens
    cov       = fraction of the group's sampled tokens attested in the sampled reference

repeated NDRAW times.  Equalising the reference size matters: coverage rises with the
size of the set you score against, so groups of different sizes scored against their own
complements are not comparable (the board's standing rule about rescaled metrics and
shared denominators).

Usage: python3 src/run_corrected.py <entries.jsonl>
"""
import json, sys, os, random, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, regions2, names2

YMIN, YMAX = 550, 900
NDRAW = 400
GRP_N = 146          # DALR token count: the binding constraint
REF_N = 7600         # <= pool minus the largest group (9517 - 1854)
SEED = 20260924
NC = ("IONA", "DALR", "PICT")
PROV = ("ULSTER", "MIDLAND", "NORTHWEST", "LEINSTER", "MUNSTER", "CONNACHT")

def load(path, tagset):
    E = [json.loads(l) for l in open(path)]
    groups = collections.defaultdict(list)
    pool = []
    for e in E:
        if not (YMIN <= e["year"] < YMAX): continue
        nm = [names2.skeleton(x) for x in names2.extract(e["text"])]
        if not nm: continue
        rec = {"year": e["year"], "names": nm, "id": e["id"], "witness": e["witness"]}
        for g in regions.region(e["text"], tagset): groups[g].append(rec)
        for p in regions2.provinces(e["text"], tagset): groups[p].append(rec)
        if regions2.is_irish_pool(e["text"], tagset): pool.append(rec)
    return groups, pool

def toks(entries): return [t for e in entries for t in e["names"]]

def score(group_entries, pool, rnd, ndraw=NDRAW):
    own = set(id(e) for e in group_entries)
    ref_entries = [e for e in pool if id(e) not in own]
    ref_tokens = toks(ref_entries)
    gtoks = toks(group_entries)
    if len(gtoks) < GRP_N or len(ref_tokens) < REF_N: return None
    vals, ttrs = [], []
    for _ in range(ndraw):
        R = names2.Reference(rnd.sample(ref_tokens, REF_N))
        g = rnd.sample(gtoks, GRP_N)
        vals.append(sum(1 for t in g if R.attested(t)) / GRP_N)
        ttrs.append(len(set(g)) / GRP_N)
    vals.sort(); ttrs.sort()
    return {"n_entries": len(group_entries), "n_tokens": len(gtoks),
            "cov_mean": sum(vals)/len(vals), "cov_p2.5": vals[int(.025*len(vals))],
            "cov_p97.5": vals[int(.975*len(vals))],
            "ttr_mean": sum(ttrs)/len(ttrs), "ttr_p2.5": ttrs[int(.025*len(ttrs))],
            "ttr_p97.5": ttrs[int(.975*len(ttrs))]}

def direction(group_entries, pool):
    own = set(id(e) for e in group_entries)
    first_ir = {}
    for e in pool:
        if id(e) in own: continue
        for t in e["names"]: first_ir[t] = min(first_ir.get(t, 9999), e["year"])
    first_g = {}
    for e in group_entries:
        for t in e["names"]: first_g[t] = min(first_g.get(t, 9999), e["year"])
    shared = [t for t in first_g if t in first_ir]
    ir = sum(1 for t in shared if first_ir[t] < first_g[t])
    gr = sum(1 for t in shared if first_g[t] < first_ir[t])
    return {"shared": len(shared), "pool_first": ir, "group_first": gr,
            "ties": len(shared)-ir-gr, "pool_first_rate": ir/(ir+gr) if ir+gr else None}

def main(path):
    out = {}
    for tagset in ("STRICT", "WIDE"):
        rnd = random.Random(SEED)
        groups, pool = load(path, tagset)
        res = {"pool_entries": len(pool), "pool_tokens": len(toks(pool)),
               "GRP_N": GRP_N, "REF_N": REF_N, "NDRAW": NDRAW, "groups": {}}
        for g in PROV + NC:
            s = score(groups[g], pool, rnd)
            if s is None: continue
            s.update(direction(groups[g], pool))
            res["groups"][g] = s
        pv = [res["groups"][p]["cov_mean"] for p in PROV if p in res["groups"]]
        res["province_band"] = {"min": min(pv), "max": max(pv),
                                "mean": sum(pv)/len(pv), "n": len(pv)}
        c = res["groups"]
        den = c["IONA"]["cov_mean"] - c["PICT"]["cov_mean"]
        res["pos_DALR"] = (c["DALR"]["cov_mean"] - c["PICT"]["cov_mean"])/den if den else None
        out[tagset] = res
    return out

if __name__ == "__main__":
    res = main(sys.argv[1])
    json.dump(res, open("results/corrected.json", "w"), indent=1)
    for ts, r in res.items():
        print("========== %s   Irish reference pool: %d entries / %d tokens (%d-%d) =========="
              % (ts, r["pool_entries"], r["pool_tokens"], YMIN, YMAX))
        print("  all groups subsampled to %d tokens, reference to %d tokens, %d draws"
              % (r["GRP_N"], r["REF_N"], r["NDRAW"]))
        print("  group       ent   tok    cov   [95%% interval]     TTR    shared  pool-first-rate")
        for g in PROV + NC:
            if g not in r["groups"]: continue
            d = r["groups"][g]
            mark = "  <-- " + ("test set" if g == "DALR" else
                               "POS control" if g == "IONA" else
                               "NEG control" if g == "PICT" else "")
            print("  %-10s %4d %5d  %.4f [%.4f,%.4f]  %.4f   %4d   %s%s"
                  % (g, d["n_entries"], d["n_tokens"], d["cov_mean"], d["cov_p2.5"],
                     d["cov_p97.5"], d["ttr_mean"], d["shared"],
                     ("%.3f" % d["pool_first_rate"]) if d["pool_first_rate"] else "n/a",
                     mark if g in NC else ""))
        b = r["province_band"]
        print("  Irish provincial band (%d provinces): %.4f - %.4f  (mean %.4f)"
              % (b["n"], b["min"], b["max"], b["mean"]))
        print("  pos(DALR)  PICT=0, IONA=1 : %.3f" % r["pos_DALR"])
