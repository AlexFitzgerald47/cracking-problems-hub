#!/usr/bin/env python3
"""Fetch the proofread Wikisource text of the 1772 Woodfall *Letters of Junius*.

One file per letter, raw wikitext preserved so the signature line -- which is what
actually decides who wrote each numbered letter -- stays auditable. Batched 20
titles per request with backoff; Wikimedia rate-limits single-page hammering.
"""
import json, os, time, urllib.parse, urllib.request

API = "https://en.wikisource.org/w/api.php"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "raw", "wikisource")
UA = "cracking-problems-hub/junius-attribution (research; contact via repo)"


def api(**params):
    params.setdefault("format", "json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 5:
                time.sleep(2 ** attempt * 3)
                continue
            raise
    raise RuntimeError("unreachable")


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = [p["title"] for p in api(action="query", list="allpages",
             apprefix="Letters of Junius/", aplimit=500)["query"]["allpages"]]
    pages = [p for p in pages if "/Table of contents" not in p and not p.endswith("/Index")]
    print("pages:", len(pages))
    for i in range(0, len(pages), 20):
        batch = pages[i:i + 20]
        d = api(action="query", prop="revisions", rvprop="content", rvslots="main",
                titles="|".join(batch))
        for pid, pg in d["query"]["pages"].items():
            wt = pg["revisions"][0]["slots"]["main"]["*"]
            name = pg["title"].split("/", 1)[1].replace(" ", "_") + ".wiki"
            with open(os.path.join(OUT, name), "w") as f:
                f.write(wt)
        print("batch", i, "ok")
        time.sleep(4)


if __name__ == "__main__":
    main()
