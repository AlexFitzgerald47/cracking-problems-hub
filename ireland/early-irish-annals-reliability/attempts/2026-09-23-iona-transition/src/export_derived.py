# -*- coding: utf-8 -*-
"""Export the derived per-entry table that IS committed.

The CELT translations are restricted/in-copyright and are not redistributed here.
What is committed is the quantitative reduction every result in RESULTS.md is
computed from: one row per entry, with the year, the entry index, the word count
and the tag flags -- but no text.  `src/fetch.py` plus `src/parse.py` regenerate
the text locally and `sha1` lets anyone confirm they have the same bytes.
"""
import sys, os, json, hashlib, re, csv
sys.path.insert(0, os.path.dirname(__file__))
import gazetteer
IONA=re.compile(r"(?<!Dath )(?<!Mac )\bÍ\b|\bIa\b|\bIona\b")
TERR=re.compile(r"Dál Riat|Pict|Fortriu|Cenn Tíre|Kintyre|\bScí\b|\bMull\b|Tiriu|Tiree|\bEig\b|"
 r"Mag Luinge|Dún At\b|Dún Ollaigh|Aporcrosan|Apor Crossan|Applecross|Cenn Garad|Kingarth|"
 r"Ail Cluaithe|Dumbarton|Cenél Loairn|Cenél nGabráin|Cenél Comgaill|Druim Alban|Iardoman|"
 r"Athfhotla|Circinn|Dún Nechtain")
rows=[]
for line in open("data/entries.jsonl"):
    r=json.loads(line); t=gazetteer.tag(r["text"])
    rows.append({"witness":r["witness"],"year":r["year"],"idx":r["idx"],"id":r["id"],
        "raw_id":r["raw_id"],"is_kalend":int(r["is_kalend"]),"n_words":r["n_words"],
        "SCOT":int(t["SCOT"]),"SCOT_AMBIG":int(t["SCOT_AMBIG"]),"INSULAR":int(t["INSULAR"]),
        "MIDLAND":int(t["MIDLAND"]),"MUNSTER":int(t["MUNSTER"]),
        "TERRITORY":int(bool(TERR.search(r["text"]))),"IONA":int(bool(IONA.search(r["text"]))),
        "sha1":hashlib.sha1(r["text"].encode("utf-8")).hexdigest()[:12]})
with open("data/entries_derived.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print("wrote data/entries_derived.csv  (%d rows)"%len(rows))
