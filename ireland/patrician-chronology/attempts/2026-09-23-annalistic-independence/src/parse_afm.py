"""Parse the Four Masters into the same per-entry schema as the other four.

The Annals folder's parser is imported rather than copied, so the holdout is
processed by exactly the code that reproduced the committed corpus byte for
byte.  Only two things differ and both are AFM-specific:

  * the CELT id pattern is `M<year>` / `M<year>.<idx>`;
  * volume 1 opens with the Anno Mundi section (AM 2242 - 5194) before the
    AD years begin at 1.  Those are dropped: `n` values >= 2000 in volume A are
    AM, and there is exactly one place where the sequence falls back (5194 -> 1),
    which the parse asserts it finds.
"""
import sys, os, re, json, importlib.util

ANNALS = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..",
                      "early-irish-annals-reliability",
                      "attempts", "2026-09-23-iona-transition", "src", "parse.py")
spec = importlib.util.spec_from_file_location("annals_parse", os.path.abspath(ANNALS))
ap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ap)

VOLS = ["T100005A", "T100005B", "T100005C"]


def main(rawdir, outpath):
    ap.SIG_RE["AFM"] = re.compile(r"^M(\d+)(?:\.(\d+))?$")
    ap.FILES["AFM"] = None
    allrec = []
    for cid in VOLS:
        recs = ap.parse_one("AFM", os.path.join(rawdir, cid + ".xml"))
        if cid == "T100005A":
            am = [r for r in recs if r["year"] >= 2000]
            recs = [r for r in recs if r["year"] < 2000]
            print("  %s: dropped %d Anno Mundi entries (AM 2242-5194)" % (cid, len(am)))
            assert am, "expected an Anno Mundi block in volume A"
        allrec.extend(recs)
    seen = set(); dedup = []
    for r in allrec:
        if r["id"] in seen: continue
        seen.add(r["id"]); dedup.append(r)
    yrs = sorted({r["year"] for r in dedup})
    print("AFM entries=%d  years=%d  range=%d-%d" % (len(dedup), len(yrs), yrs[0], yrs[-1]))
    with open(outpath, "w") as f:
        for r in dedup:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote", outpath)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
