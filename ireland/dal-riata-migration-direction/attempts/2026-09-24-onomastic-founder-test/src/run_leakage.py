# -*- coding: utf-8 -*-
"""LEAKAGE MEASUREMENT: why the onomastic channel cannot work on this corpus.

Both ways of building an "Irish" reference pool from the Irish annals are biased, in
opposite directions, and the bias is structural rather than a matter of sample size:

  permissive pool (every entry with no north-channel place/ethnonym marker)
      -> CONTAMINATED.  Annalistic entries very often name a person with no toponym at
         all ("The death of Brude son of Foth"), so Pictish, British and Argyll people
         land in the reference.  A distinctively non-Irish name then scores as
         "attested in Ireland" because ANOTHER non-Irish person carries it.  That is
         the failure of the frozen negative control.

  marked pool (entry must carry a positive Irish place/people marker)
      -> DEPLETED.  It discards ~1,800 name-bearing in-window entries, most of them
         bare obits, which is a large and non-random slice of the Irish name stock.
         Every out-of-sample group is then depressed against an in-sample null.  That
         is the failure of the frozen positive control.

This script measures the first.  NON_IRISH is a short list of names whose Pictish or
British identity is not in dispute and which have no Irish currency, so any occurrence
inside a pool that claims to be Irish is leakage by definition.

Usage: python3 src/run_leakage.py <entries.jsonl>
"""
import json, sys, os, collections
sys.path.insert(0, os.path.dirname(__file__))
import regions, regions2, names2

YMIN, YMAX = 550, 900
NON_IRISH = {                      # skeleton -> gloss
    "bruide": "Bruide/Bridei, Pictish royal name",
    "brude": "Bruide/Bridei, Pictish royal name",
    "tolarg": "Talorc/Talorgan, Pictish royal name",
    "tolartac": "Talorcan, Pictish",
    "drust": "Drest/Drust, Pictish royal name",
    "drest": "Drest/Drust, Pictish royal name",
    "bile": "Bili, British (Dumbarton) royal name",
    "maelcu": "Maelchon, Pictish/British",
    "maelcon": "Maelchon, Pictish/British",
    "alpin": "Alpin, Pictish/Dal Riata",
    "ailpin": "Alpin, Pictish/Dal Riata",
    "eilpin": "Alpin, Pictish/Dal Riata",
    "uurad": "Uurad, Pictish",
}

def main(path):
    E = [json.loads(l) for l in open(path)]
    W = [e for e in E if YMIN <= e["year"] < YMAX]
    pool = [e for e in W if not regions.region(e["text"], "STRICT")]
    marked = [e for e in W if regions2.is_irish_pool(e["text"], "STRICT")
              and regions.IRISH.search(e["text"])]
    tok = lambda es: [names2.skeleton(x) for e in es for x in names2.extract(e["text"])]
    pt, mt = tok(pool), tok(marked)
    c = collections.Counter(pt)
    leak = {k: c[k] for k in NON_IRISH if c[k]}
    ex = []
    for e in pool:
        s = set(names2.skeleton(x) for x in names2.extract(e["text"]))
        hit = s & set(NON_IRISH)
        if hit: ex.append({"id": e["id"], "names": sorted(hit),
                           "text": e["text"][:160].replace("\n", " ")})
    res = {"window": [YMIN, YMAX],
           "permissive_pool": {"entries": len(pool), "tokens": len(pt)},
           "marked_pool": {"entries": len(marked), "tokens": len(mt)},
           "tokens_discarded_by_marking": len(pt) - len(mt),
           "leak_tokens": sum(leak.values()), "leak_by_name": leak,
           "leak_entries": len(ex), "examples": ex[:20]}
    return res

if __name__ == "__main__":
    r = main(sys.argv[1])
    json.dump(r, open("results/leakage.json", "w"), indent=1)
    print("permissive Irish pool : %d entries / %d name-tokens"
          % (r["permissive_pool"]["entries"], r["permissive_pool"]["tokens"]))
    print("marked Irish pool     : %d entries / %d name-tokens  (marking discards %d tokens, %.0f%%)"
          % (r["marked_pool"]["entries"], r["marked_pool"]["tokens"],
             r["tokens_discarded_by_marking"],
             100*r["tokens_discarded_by_marking"]/r["permissive_pool"]["tokens"]))
    print("\nuncontroversially NON-IRISH name tokens inside the permissive 'Irish' pool: %d"
          " across %d entries" % (r["leak_tokens"], r["leak_entries"]))
    for k, v in sorted(r["leak_by_name"].items(), key=lambda kv: -kv[1]):
        print("   %-10s %3d   (%s)" % (k, v, NON_IRISH[k]))
    print("\nexamples:")
    for e in r["examples"][:8]:
        print("   %-10s %-22s %s" % (e["id"], ",".join(e["names"]), e["text"][:100]))
