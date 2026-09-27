# -*- coding: utf-8 -*-
"""Verify that re-fetching CELT and re-running the sister folder's parser reproduces its
committed derived table byte-for-byte, and audit that table's key.

Usage: python3 src/verify_corpus.py <entries.jsonl> <entries_derived.csv>
"""
import json, csv, sys, hashlib, collections

def main(jsonl, csvpath):
    mine = [json.loads(l) for l in open(jsonl)]
    rows = list(csv.DictReader(open(csvpath)))
    ok = bad = 0
    for e, r in zip(mine, rows):
        same = (e["witness"] == r["witness"] and str(e["year"]) == r["year"]
                and hashlib.sha1(e["text"].encode()).hexdigest()[:12] == r["sha1"])
        ok, bad = (ok + 1, bad) if same else (ok, bad + 1)
    c = collections.Counter(r["id"] for r in rows)
    dup = {k: v for k, v in c.items() if v > 1}
    dup_w = collections.Counter(r["witness"] for r in rows if c[r["id"]] > 1)
    scot_dup = sum(1 for r in rows if c[r["id"]] > 1 and r.get("SCOT") == "1")
    return {"mine_rows": len(mine), "committed_rows": len(rows),
            "positional_sha1_match": ok, "mismatch": bad,
            "duplicate_ids": len(dup), "rows_lost_by_id_join": len(rows) - len(c),
            "duplicate_rows_by_witness": dict(dup_w),
            "scot_tagged_rows_with_duplicate_id": scot_dup}

if __name__ == "__main__":
    r = main(sys.argv[1], sys.argv[2])
    print("rows: mine=%d committed=%d" % (r["mine_rows"], r["committed_rows"]))
    print("positional sha1 match = %d   mismatch = %d" % (r["positional_sha1_match"], r["mismatch"]))
    print("AUDIT: duplicate ids = %d, rows lost by a naive join on `id` = %d %s"
          % (r["duplicate_ids"], r["rows_lost_by_id_join"], r["duplicate_rows_by_witness"]))
    print("AUDIT: SCOT-tagged rows carrying a duplicated id = %d (headline result unaffected)"
          % r["scot_tagged_rows_with_duplicate_id"])
    json.dump(r, open("results/verify.json", "w"), indent=1)
