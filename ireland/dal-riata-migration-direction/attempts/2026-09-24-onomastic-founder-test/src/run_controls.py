# -*- coding: utf-8 -*-
"""CONTROLS-ONLY RUN.  DALR is excluded by construction.

The frozen negative control failed: token-level coverage put the Picts -- a different
people speaking a different language -- inside the Irish provincial band, so the frozen
statistic has no demonstrated power on the Irish/non-Irish axis and pos(DALR) from it is
uninterpretable.  Before abandoning the axis, test whether a SHARPER statistic separates
the known controls.  DALR is not computed here, so the choice of statistic cannot be
made by looking at the answer; if a statistic passes, a fresh prediction for DALR is
frozen in FREEZE-2.md before it is ever applied to DALR.

Statistics, all at matched group size and matched reference size:
  cov        token-level attestation rate (the frozen statistic, for comparison)
  typecov    TYPE-level attestation rate -- distinctive names count once, so it is not
             swamped by a handful of very frequent shared names
  jsd        Jensen-Shannon divergence between the group's name-frequency distribution
             and the reference's.  Sensitive to composition, not just to presence.
Usage: python3 src/run_controls.py <entries.jsonl>
"""
import json, sys, os, random, math, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, regions2, names2
from run_corrected import load, toks, YMIN, YMAX, GRP_N, SEED

REF_N = 7500
NDRAW = 400
PROV = ("ULSTER", "MIDLAND", "NORTHWEST", "LEINSTER", "MUNSTER", "CONNACHT")
CONTROLS = PROV + ("IONA", "PICT")          # DALR deliberately absent

def jsd(p_counts, q_counts):
    keys = set(p_counts) | set(q_counts)
    np_, nq = sum(p_counts.values()), sum(q_counts.values())
    s = 0.0
    for k in keys:
        p = p_counts.get(k, 0)/np_; q = q_counts.get(k, 0)/nq
        m = (p+q)/2
        if p: s += 0.5*p*math.log(p/m, 2)
        if q: s += 0.5*q*math.log(q/m, 2)
    return s

def score(group_entries, pool, rnd):
    own = set(id(e) for e in group_entries)
    ref_tokens = toks([e for e in pool if id(e) not in own])
    g_all = toks(group_entries)
    if len(g_all) < GRP_N or len(ref_tokens) < REF_N: return None
    cov, tcov, dj = [], [], []
    for _ in range(NDRAW):
        rs = rnd.sample(ref_tokens, REF_N)
        R = names2.Reference(rs)
        g = rnd.sample(g_all, GRP_N)
        cov.append(sum(1 for t in g if R.attested(t))/GRP_N)
        ty = set(g)
        tcov.append(sum(1 for t in ty if R.attested(t))/len(ty))
        dj.append(jsd(collections.Counter(g), collections.Counter(rs)))
    f = lambda v: (sum(v)/len(v), sorted(v)[int(.025*len(v))], sorted(v)[int(.975*len(v))])
    return {"n_tokens": len(g_all), "cov": f(cov), "typecov": f(tcov), "jsd": f(dj)}

def main(path):
    out = {}
    for tagset in ("STRICT", "WIDE"):
        rnd = random.Random(SEED)
        groups, pool = load(path, tagset)
        res = {}
        for g in CONTROLS:
            s = score(groups[g], pool, rnd)
            if s: res[g] = s
        out[tagset] = res
    return out

if __name__ == "__main__":
    res = main(sys.argv[1])
    json.dump(res, open("results/controls.json", "w"), indent=1)
    for ts, r in res.items():
        print("========== %s  (controls only; DALR not computed) ==========" % ts)
        print("  group        tok     cov [95%%]              typecov [95%%]          jsd [95%%]")
        for g in CONTROLS:
            if g not in r: continue
            d = r[g]
            tag = "  <-- POS" if g == "IONA" else ("  <-- NEG" if g == "PICT" else "")
            print("  %-10s %5d  %.3f [%.3f,%.3f]   %.3f [%.3f,%.3f]   %.4f [%.4f,%.4f]%s"
                  % (g, d["n_tokens"], *d["cov"], *d["typecov"], *d["jsd"], tag))
        for stat in ("cov", "typecov", "jsd"):
            pv = [r[p][stat][0] for p in PROV if p in r]
            print("  province band %-8s %.4f - %.4f | IONA %.4f | PICT %.4f  ->  %s"
                  % (stat, min(pv), max(pv), r["IONA"][stat][0], r["PICT"][stat][0],
                     "PICT SEPARATES" if (r["PICT"][stat][0] < min(pv) or r["PICT"][stat][0] > max(pv))
                     else "PICT inside Irish band (no power)"))
