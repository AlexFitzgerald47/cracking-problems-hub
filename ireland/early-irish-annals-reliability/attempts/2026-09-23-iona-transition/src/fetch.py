"""Fetch the four CELT annal translations used by this attempt.

CELT's own availability statement is `restricted` ("available with prior consent of
the CELT project for purposes of academic research and teaching only") and the
underlying translations are in copyright (e.g. AU vol. 1 -> School of Celtic Studies,
DIAS).  We therefore DO NOT commit the raw texts.  This script re-creates them, and
everything committed downstream is derived quantitative data.

Usage:  python3 src/fetch.py data/raw
"""
import sys, os, urllib.request

TEXTS = {
    "AU": ("T100001A", "Annals of Ulster, vol. 1, English translation (Mac Airt & Mac Niocaill 1983; Hennessy & Mac Carthy after 1131)"),
    "AT": ("T100002A", "Annals of Tigernach, English translation (Stokes)"),
    "AI": ("T100004",  "Annals of Inisfallen, English translation (Mac Airt 1951)"),
    "CS": ("T100016",  "Chronicon Scotorum, English translation (Gleeson & Mac Airt / Hennessy)"),
}
BASE = "https://celt.ucc.ie/texts/%s.xml"

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for sig, (celt_id, desc) in TEXTS.items():
        url = BASE % celt_id
        dest = os.path.join(outdir, "%s.xml" % celt_id)
        if os.path.exists(dest):
            print("have  %s  %s" % (sig, dest)); continue
        print("fetch %s  %s" % (sig, url))
        with urllib.request.urlopen(url, timeout=120) as r:
            data = r.read()
        open(dest, "wb").write(data)
        print("      %d bytes  (%s)" % (len(data), desc))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/raw")
