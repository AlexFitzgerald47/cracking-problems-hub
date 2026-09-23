"""Parse CELT annal XML into a flat per-entry table.

CELT's four texts use three slightly different nestings:
    AU  <div1 n="U493"> / <div2 n="U493.1">
    AT  <div1 n="T563"> / <div2 n="T563.1">
    AI  <div1 n="AI433"> / <div2 n="AI433.1">
    CS  <div2 n="CS563"> / <div3 n="CS563.1">
so we key off the @n attribute pattern rather than the element depth.

Output: one record per annalistic ENTRY (not per year).  Entry `.0` is the
chronological apparatus (kalend / feria / epact) and is flagged, not dropped --
its presence or absence is itself evidence about the underlying chronicle.
"""
import re, os, sys, json, html, unicodedata

SIG_RE = {
    "AU": re.compile(r"^U(\d+)(?:\.(\d+))?$"),
    "AT": re.compile(r"^T(\d+)(?:\.(\d+))?$"),
    "AI": re.compile(r"^AI(\d+)(?:\.(\d+))?$"),
    "CS": re.compile(r"^CS(\d+)(?:\.(\d+))?$"),
}
FILES = {"AU": "T100001A.xml", "AT": "T100002A.xml", "AI": "T100004.xml", "CS": "T100016.xml"}

XML_PREDEF = {"amp", "lt", "gt", "quot", "apos"}
ENT_RE = re.compile(r"&([A-Za-z][A-Za-z0-9]*);")
TAG_RE = re.compile(r"<[^>]+>")
DIV_OPEN = re.compile(r'<div([0-9])\s+n="([^"]+)"[^>]*>')
DATE_RE = re.compile(r'<date\s+value="(-?\d+)"[^>]*>(.*?)</date>', re.S)


def load(path):
    raw = open(path, "rb").read().decode("iso-8859-1")
    raw = re.sub(r"<!DOCTYPE.*?\]>", "", raw, flags=re.S)
    # expand HTML entities but leave the five XML-predefined ones intact
    def rep(m):
        name = m.group(1)
        if name in XML_PREDEF:
            return m.group(0)
        ch = html.unescape("&%s;" % name)
        return ch if ch != "&%s;" % name else " "
    return ENT_RE.sub(rep, raw)


def detag(chunk):
    """Strip markup, keeping the text.  Drop <note> and <bibl> bodies: editorial
    apparatus is not annalistic content."""
    chunk = re.sub(r"<note\b.*?</note>", " ", chunk, flags=re.S)
    chunk = re.sub(r"<bibl\b.*?</bibl>", " ", chunk, flags=re.S)
    txt = TAG_RE.sub(" ", chunk)
    txt = html.unescape(txt)
    txt = unicodedata.normalize("NFC", txt)
    return re.sub(r"\s+", " ", txt).strip()


def parse_one(sig, path):
    src = load(path)
    body_start = src.find("<text")
    src = src[body_start:] if body_start > 0 else src
    year_re = SIG_RE[sig]
    marks = []
    for m in DIV_OPEN.finditer(src):
        n = m.group(2)
        mm = year_re.match(n)
        if not mm:
            continue
        marks.append((m.start(), m.end(), int(mm.group(1)), mm.group(2), n))
    out, cur_year, typos = [], None, []
    for i, (s, e, ynum, sub, n) in enumerate(marks):
        if sub is None:
            # a year container: its @n carries the year for every entry beneath it
            cur_year = ynum
            continue
        if cur_year is None:
            continue
        if ynum != cur_year:
            # CELT id typos exist (e.g. AI969.4 is tagged "AI9695.4").  The
            # enclosing year container wins; record the discrepancy.
            typos.append((n, cur_year))
        nxt = marks[i + 1][0] if i + 1 < len(marks) else len(src)
        chunk = src[e:nxt]
        dm = DATE_RE.search(chunk)
        txt = detag(chunk)
        out.append({
            "witness": sig, "year": cur_year, "idx": int(sub),
            "id": "%s%d.%s" % (sig, cur_year, sub),
            "raw_id": n,
            "is_kalend": int(sub) == 0,
            "n_words": len(txt.split()),
            "date_attr": int(dm.group(1)) if dm else None,
            "text": txt,
        })
    if typos:
        print("   %s: %d entry ids disagree with their year container: %s"
              % (sig, len(typos), ", ".join("%s->%d" % t for t in typos[:6])))
    return out


def main(rawdir, outpath):
    allrec = []
    for sig, fn in FILES.items():
        recs = parse_one(sig, os.path.join(rawdir, fn))
        yrs = sorted({r["year"] for r in recs})
        print("%s  entries=%5d  years=%4d  range=%d-%d" % (sig, len(recs), len(yrs), yrs[0], yrs[-1]))
        allrec.extend(recs)
    with open(outpath, "w") as f:
        for r in allrec:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("wrote %s (%d entries)" % (outpath, len(allrec)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/raw",
         sys.argv[2] if len(sys.argv) > 2 else "data/entries.jsonl")
