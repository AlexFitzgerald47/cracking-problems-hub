#!/usr/bin/env python3
"""Render the proofread Wikisource *Letters of Junius* (Woodfall, 1772) to plain text.

Notes for whoever reruns this -- each of these cost time to discover:

* The wikitext is a <pages> transclusion of the Page: namespace of the 1772 djvu, so
  wikitext alone contains no prose. It has to be rendered.
* TextExtracts (prop=extracts) returns an EMPTY string for these pages -- it does not
  follow the ProofreadPage transclusion. It fails silently; do not use it here.
* ws-export.wmcloud.org (whole-work txt export) timed out at 180s from this environment.
* Wikimedia rate-limits this shared egress hard: single requests return HTTP 429
  intermittently whether issued from python-urllib, curl, or the REST API. The only
  thing that works is patience. This script retries a page up to 40 times with a
  25s gap and resumes from whatever is already on disk, so it is safe to rerun.

Authorship warning: the Wikisource header says `author = Junius` on EVERY numbered
letter. That is wrong. The 1772 collection interleaves replies by Sir William Draper,
Modestus and others; Letter II is signed WILLIAM DRAPER. Only the signature at the
foot of the letter is authoritative. Segmentation happens in build_corpus.py.
"""
import html, json, os, re, subprocess, sys, time

API = "https://en.wikisource.org/w/api.php"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "raw", "wikisource_text")
UA = "cracking-problems-hub/junius-attribution (research)"


def curl(params, tries=40, gap=25):
    cmd = ["curl", "-sS", "--max-time", "60", "-A", UA, "-G", API]
    for k, v in params.items():
        cmd += ["--data-urlencode", f"{k}={v}"]
    for attempt in range(tries):
        p = subprocess.run(cmd, capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip().startswith("{"):
            try:
                d = json.loads(p.stdout)
            except json.JSONDecodeError:
                d = None
            if d and "error" not in d:
                return d
        time.sleep(gap)
    return None


def strip_html(h):
    t = re.sub(r'(?s)<(script|style|table).*?</\1>', ' ', h)
    t = re.sub(r'(?s)<sup[^>]*class="[^"]*reference[^"]*".*?</sup>', ' ', t)
    t = re.sub(r'(?s)<div[^>]*class="[^"]*(?:reflist|smallrefs)[^"]*".*?</div>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    t = t.replace('​', '')            # ProofreadPage page-join zero-width space
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r'\n\s*\n+', '\n\n', t)
    return t.strip()


def main():
    os.makedirs(OUT, exist_ok=True)
    d = curl(dict(action="query", list="allpages", apprefix="Letters of Junius/",
                  aplimit=500, format="json"))
    pages = [p["title"] for p in d["query"]["allpages"]]
    pages = [p for p in pages if "/Table of contents" not in p and not p.endswith("/Index")]
    print(f"{len(pages)} pages", flush=True)
    missed = []
    for t in pages:
        name = t.split("/", 1)[1].replace(" ", "_") + ".txt"
        path = os.path.join(OUT, name)
        if os.path.exists(path) and os.path.getsize(path) > 200:
            continue
        d = curl(dict(action="parse", page=t, prop="text", formatversion=2, format="json"))
        if d is None:
            missed.append(t)
            print(f"  MISSED {name}", flush=True)
            continue
        txt = strip_html(d["parse"]["text"])
        with open(path, "w") as f:
            f.write(txt)
        print(f"  {name}: {len(txt)}", flush=True)
        time.sleep(3)
    print("missed:", missed, flush=True)


if __name__ == "__main__":
    main()
