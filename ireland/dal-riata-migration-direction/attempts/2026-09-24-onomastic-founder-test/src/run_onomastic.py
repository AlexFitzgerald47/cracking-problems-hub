# -*- coding: utf-8 -*-
"""CONFIRMATORY RUN.  Predictions frozen in FREEZE.md before this was executed.

Usage: python3 src/run_onomastic.py <entries.jsonl>
"""
import json, sys, os, random, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, names

YMIN, YMAX = 550, 900
NDRAW = 4000
SEED = 20260924

def load(path, tagset):
    E = [json.loads(l) for l in open(path)]
    groups = {"IONA": [], "DALR": [], "PICT": []}
    irish = []
    for e in E:
        if not (YMIN <= e["year"] < YMAX): continue
        nm = [names.skeleton(x) for x in names.extract(e["text"])]
        if not nm: continue
        rec = {"year": e["year"], "names": nm, "witness": e["witness"], "id": e["id"]}
        for g in regions.region(e["text"], tagset):
            groups[g].append(rec)
        if regions.is_irish_ref(e["text"], tagset):
            irish.append(rec)
    return groups, irish

def ref_counter(entries, exclude=()):
    ex = set(id(x) for x in exclude)
    c = collections.Counter()
    for e in entries:
        if id(e) in ex: continue
        c.update(e["names"])
    return c

def cov(group_entries, irish_entries):
    ref = ref_counter(irish_entries)          # groups are disjoint from irish by construction
    toks = [n for e in group_entries for n in e["names"]]
    hit = sum(1 for t in toks if ref[t] > 0)
    return hit / len(toks), len(toks), hit

def null_cov(irish, n_target, ndraw, rnd):
    vals = []
    for _ in range(ndraw):
        pool = irish[:]; rnd.shuffle(pool)
        samp, got = [], 0
        for e in pool:
            samp.append(e); got += len(e["names"])
            if got >= n_target: break
        ref = ref_counter(irish, exclude=samp)
        toks = [n for e in samp for n in e["names"]]
        vals.append(sum(1 for t in toks if ref[t] > 0) / len(toks))
    vals.sort(); return vals

def ttr_rarefied(entries, n, ndraw, rnd):
    toks = [t for e in entries for t in e["names"]]
    if len(toks) < n: return None
    out = []
    for _ in range(ndraw):
        s = rnd.sample(toks, n)
        out.append(len(set(s)) / n)
    out.sort(); return out

def pct(sorted_vals, v):
    lo = sum(1 for x in sorted_vals if x < v)
    return lo / len(sorted_vals)

def main(path):
    out = {}
    for tagset in ("STRICT", "WIDE"):
        rnd = random.Random(SEED)
        groups, irish = load(path, tagset)
        res = {"irish_entries": len(irish),
               "irish_tokens": sum(len(e["names"]) for e in irish), "groups": {}}
        covs = {}
        for g, ents in groups.items():
            c, ntok, hit = cov(ents, irish)
            covs[g] = c
            nulls = null_cov(irish, ntok, NDRAW, rnd)
            res["groups"][g] = {
                "entries": len(ents), "tokens": ntok, "hits": hit, "cov": c,
                "null_mean": sum(nulls)/len(nulls),
                "null_p2.5": nulls[int(.025*len(nulls))],
                "null_p97.5": nulls[int(.975*len(nulls))],
                "pct_in_null": pct(nulls, c),
                "p_one_sided_low": (sum(1 for x in nulls if x <= c)+1)/(len(nulls)+1),
            }
        # scale-free position between the controls
        denom = covs["IONA"] - covs["PICT"]
        res["pos_DALR"] = (covs["DALR"] - covs["PICT"]) / denom if denom else None
        res["pos_IONA"] = 1.0; res["pos_PICT"] = 0.0
        # P4: rarefied TTR at the DALR token count
        nD = res["groups"]["DALR"]["tokens"]
        for g in ("IONA", "DALR", "PICT"):
            t = ttr_rarefied(groups[g], min(nD, res["groups"][g]["tokens"]), 2000, rnd)
            res["groups"][g]["ttr_rarefied_at_%d" % nD] = (sum(t)/len(t)) if t else None
        tn = ttr_rarefied(irish, nD, 2000, rnd)
        res["ttr_null_mean"] = sum(tn)/len(tn)
        res["ttr_null_p2.5"] = tn[int(.025*len(tn))]
        res["ttr_null_p97.5"] = tn[int(.975*len(tn))]
        res["ttr_n"] = nD
        # P5: direction of first attestation for shared skeletons
        first_ir = {}
        for e in irish:
            for t in e["names"]: first_ir[t] = min(first_ir.get(t, 9999), e["year"])
        for g in ("IONA", "DALR", "PICT"):
            first_g = {}
            for e in groups[g]:
                for t in e["names"]: first_g[t] = min(first_g.get(t, 9999), e["year"])
            shared = [t for t in first_g if t in first_ir]
            ir_first = sum(1 for t in shared if first_ir[t] < first_g[t])
            gr_first = sum(1 for t in shared if first_g[t] < first_ir[t])
            res["groups"][g]["shared_types"] = len(shared)
            res["groups"][g]["irish_first"] = ir_first
            res["groups"][g]["group_first"] = gr_first
            res["groups"][g]["ties"] = len(shared) - ir_first - gr_first
            dec = ir_first + gr_first
            res["groups"][g]["irish_first_rate"] = ir_first/dec if dec else None
        out[tagset] = res
    return out

if __name__ == "__main__":
    res = main(sys.argv[1])
    json.dump(res, open("results/onomastic.json", "w"), indent=1)
    for ts, r in res.items():
        print("=========== tagset %s   (Irish ref: %d entries / %d tokens, %d-%d) ==========="
              % (ts, r["irish_entries"], r["irish_tokens"], YMIN, YMAX))
        print("  group   ent  tok   cov     null mean [2.5%,97.5%]        pctile   p(low)")
        for g in ("IONA", "DALR", "PICT"):
            d = r["groups"][g]
            print("  %-5s %5d %4d  %.4f   %.4f [%.4f, %.4f]   %6.4f   %.4f"
                  % (g, d["entries"], d["tokens"], d["cov"], d["null_mean"],
                     d["null_p2.5"], d["null_p97.5"], d["pct_in_null"], d["p_one_sided_low"]))
        print("  pos(DALR) between PICT=0 and IONA=1 : %.3f" % r["pos_DALR"])
        print("  -- P4 rarefied TTR at n=%d : null %.4f [%.4f, %.4f]"
              % (r["ttr_n"], r["ttr_null_mean"], r["ttr_null_p2.5"], r["ttr_null_p97.5"]))
        for g in ("IONA", "DALR", "PICT"):
            print("       %-5s %.4f" % (g, r["groups"][g]["ttr_rarefied_at_%d" % r["ttr_n"]]))
        print("  -- P5 first-attestation direction (shared skeletons) --")
        for g in ("IONA", "DALR", "PICT"):
            d = r["groups"][g]
            print("       %-5s shared=%3d  Irish-first=%3d  %s-first=%3d  ties=%3d  rate=%s"
                  % (g, d["shared_types"], d["irish_first"], g, d["group_first"], d["ties"],
                     ("%.3f" % d["irish_first_rate"]) if d["irish_first_rate"] is not None else "n/a"))
