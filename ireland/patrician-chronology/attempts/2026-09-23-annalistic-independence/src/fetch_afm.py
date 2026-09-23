"""Fetch the Annals of the Four Masters (CELT), the holdout witness.

Same restriction as the other four texts: CELT's availability statement is
`restricted` and the O'Donovan translation is reproduced there by permission, so
the raw XML is not committed.  Everything committed downstream is derived.

Usage:  python3 src/fetch_afm.py <rawdir>
"""
import sys, os, urllib.request

VOLS = {"T100005A": "AFM vol. 1-2, AM 2242 - AD 902",
        "T100005B": "AFM vol. 2-3, AD 903 - 1171",
        "T100005C": "AFM vol. 3-4, AD 1172 - 1616"}
BASE = "https://celt.ucc.ie/texts/%s.xml"

def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    for cid, desc in VOLS.items():
        dest = os.path.join(outdir, cid + ".xml")
        if os.path.exists(dest):
            print("have  %s" % dest); continue
        with urllib.request.urlopen(BASE % cid, timeout=180) as r:
            data = r.read()
        open(dest, "wb").write(data)
        print("fetch %s  %d bytes  (%s)" % (cid, len(data), desc))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/raw")
