# -*- coding: utf-8 -*-
"""POWER / CEILING RUN (pre-freeze).  Uses the IRISH reference pool ONLY.

Question: with n name-tokens drawn from period-matched Irish material, what is the
sampling distribution of the coverage statistic cov = (fraction of tokens whose name
skeleton is attested elsewhere in the Irish pool)?  That distribution is the null, and
its spread says what effect this corpus can and cannot detect.  Nothing here touches
IONA / DALR / PICT, so it cannot leak the answer.

Held-out coverage: when a sample is drawn from the pool, the sampled ENTRIES are
removed from the reference before coverage is scored.  Without this the statistic is
guaranteed near 1.0 by construction -- the trap that produces spurious precision.

Usage: python3 src/run_power.py <entries.jsonl>
"""
import json, sys, os, random, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, names

YMIN, YMAX = 550, 900
NDRAW = 2000
SIZES = [100, 146, 150, 192, 200, 221, 250, 300, 400]

def load(path, tagset):
    E = [json.loads(l) for l in open(path)]
    irish = []
    for e in E:
        if not (YMIN <= e["year"] < YMAX): continue
        if regions.is_irish_ref(e["text"], tagset):
            nm = [names.skeleton(x) for x in names.extract(e["text"])]
            if nm: irish.append({"year": e["year"], "names": nm})
    return irish

def cov_heldout(sample_entries, pool_entries):
    """Fraction of tokens in sample whose skeleton appears in pool (sample excluded)."""
    ids = set(id(x) for x in sample_entries)
    ref = collections.Counter()
    for e in pool_entries:
        if id(e) in ids: continue
        ref.update(e["names"])
    toks = [n for e in sample_entries for n in e["names"]]
    if not toks: return None, 0
    return sum(1 for t in toks if ref[t] > 0) / len(toks), len(toks)

def main(path):
    out = {}
    for tagset in ("STRICT", "WIDE"):
        irish = load(path, tagset)
        ntok = sum(len(e["names"]) for e in irish)
        rnd = random.Random(20260924)
        res = {"n_entries": len(irish), "n_tokens": ntok, "draws": {}}
        for size in SIZES:
            vals = []
            for _ in range(NDRAW):
                samp, got = [], 0
                pool = irish[:]
                rnd.shuffle(pool)
                for e in pool:
                    samp.append(e); got += len(e["names"])
                    if got >= size: break
                c, n = cov_heldout(samp, irish)
                if c is not None: vals.append(c)
            vals.sort()
            res["draws"][size] = {
                "mean": sum(vals) / len(vals),
                "sd": (sum((v - sum(vals)/len(vals))**2 for v in vals)/(len(vals)-1))**0.5,
                "p2.5": vals[int(.025*len(vals))], "p50": vals[len(vals)//2],
                "p97.5": vals[int(.975*len(vals))],
            }
        out[tagset] = res
    return out

if __name__ == "__main__":
    res = main(sys.argv[1])
    for ts, r in res.items():
        print("==== %s : Irish reference pool %d entries / %d tokens (%d-%d) ===="
              % (ts, r["n_entries"], r["n_tokens"], YMIN, YMAX))
        print("   n_tok   mean_cov      sd     95%% null interval    detectable drop (2.5%% tail)")
        for size, d in sorted(r["draws"].items()):
            print("   %5d    %.4f    %.4f    [%.4f, %.4f]        %.4f"
                  % (size, d["mean"], d["sd"], d["p2.5"], d["p97.5"],
                     d["mean"] - d["p2.5"]))
    json.dump(res, open("results/power.json", "w"), indent=1)
