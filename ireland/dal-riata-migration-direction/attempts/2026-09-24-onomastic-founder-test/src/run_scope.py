# -*- coding: utf-8 -*-
"""SCOPING RUN (exploratory, pre-freeze).  Reports SAMPLE SIZES ONLY.

Deliberately does not compute the outcome statistic, so that the predictions in
FREEZE.md are written without having seen the answer.
Usage: python3 src/run_scope.py <entries.jsonl>
"""
import json, sys, collections, os
sys.path.insert(0, os.path.dirname(__file__))
import regions, names

def main(path):
    E = [json.loads(l) for l in open(path)]
    out = {}
    for ts in ("STRICT", "WIDE"):
        rec = {}
        for e in E:
            e_nm = names.extract(e["text"])
            reg = regions.region(e["text"], ts)
            for g in reg:
                r = rec.setdefault(g, {"entries": 0, "tokens": 0, "types": set(),
                                       "by_cent": collections.Counter()})
                r["entries"] += 1; r["tokens"] += len(e_nm)
                r["types"].update(names.skeleton(n) for n in e_nm)
                r["by_cent"][(e["year"] // 50) * 50] += len(e_nm)
            if regions.is_irish_ref(e["text"], ts):
                r = rec.setdefault("IRISH", {"entries": 0, "tokens": 0, "types": set(),
                                             "by_cent": collections.Counter()})
                r["entries"] += 1; r["tokens"] += len(e_nm)
                r["types"].update(names.skeleton(n) for n in e_nm)
                r["by_cent"][(e["year"] // 50) * 50] += len(e_nm)
        out[ts] = {g: {"entries": v["entries"], "tokens": v["tokens"],
                       "types": len(v["types"]),
                       "by_cent": dict(sorted(v["by_cent"].items()))}
                   for g, v in rec.items()}
    return out

if __name__ == "__main__":
    res = main(sys.argv[1])
    for ts, rec in res.items():
        print("==== tagset %s ====" % ts)
        for g in ("IONA", "DALR", "PICT", "IRISH"):
            if g not in rec: continue
            v = rec[g]
            print("  %-6s entries=%5d  name-tokens=%5d  distinct=%4d" %
                  (g, v["entries"], v["tokens"], v["types"]))
        print("  -- name-tokens by half-century (550-900 window in brackets) --")
        for g in ("IONA", "DALR", "PICT", "IRISH"):
            if g not in rec: continue
            bc = rec[g]["by_cent"]
            w = sum(n for y, n in bc.items() if 550 <= y < 900)
            print("     %-6s total=%5d  [550-900]=%5d  %s" %
                  (g, sum(bc.values()), w,
                   {y: n for y, n in bc.items() if 450 <= y < 950}))
    json.dump(res, open("results/scope.json", "w"), indent=1, default=str)
