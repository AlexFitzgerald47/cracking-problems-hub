"""Build the vita-level Historia Augusta corpus and the control corpora.

Sources (both fetched from public GitHub mirrors; see PROVENANCE.md):
  * Perseus canonical-latinLit TEI (perseus-lat2) -- primary witness.
    Historia Augusta = urn:cts:latinLit:phi2331, editio: Magie, Loeb 1921-32.
  * CLTK latin_text_latin_library -- independent second witness, used only
    to check that the Perseus OCR is stylometrically stable.

Output: data/segments.json -- one record per text segment with metadata.
"""

import json
import os
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

TEI = "{http://www.tei-c.org/ns/1.0}"
SCRATCH = os.environ.get(
    "HA_SCRATCH",
    "/tmp/claude-0/-home-user-cracking-problems-hub/"
    "4d387805-5a98-5775-b701-2d4d61b62a9e/scratchpad",
)
PERSEUS = os.path.join(SCRATCH, "plit", "data")
LATLIB = os.path.join(SCRATCH, "ll")
OUT = os.path.join(os.path.dirname(__file__), "..", "data")

# Non-text elements. Perseus lat2 files carry English editorial notes and
# bibliography inline; leaving them in would inject English function words.
DROP = {TEI + "note", TEI + "bibl", TEI + "head", TEI + "teiHeader",
        TEI + "ref", TEI + "cit", TEI + "gap", TEI + "orig"}


def text_of(el, drop=None):
    drop = DROP if drop is None else drop
    if el.tag in drop:
        return ""
    out = [el.text or ""]
    for child in el:
        out.append(text_of(child, drop))
        out.append(child.tail or "")
    return "".join(out)


def normalise(raw):
    """Lowercase, strip accents/markup residue, fold u/v and i/j.

    Fold is required because the two witnesses disagree on orthography:
    Perseus/Loeb prints consonantal u as 'u', the Latin Library sometimes 'v'.
    Any feature that survives the fold is a feature both witnesses agree on.
    """
    s = unicodedata.normalize("NFKD", raw)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = s.replace("v", "u").replace("j", "i")
    s = re.sub(r"[^a-z\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def tokens(raw):
    return normalise(raw).split()


# ---------------------------------------------------------------- Perseus

def perseus_work(group, work):
    path = os.path.join(PERSEUS, group, work,
                        "%s.%s.perseus-lat2.xml" % (group, work))
    if not os.path.exists(path):
        return None
    root = ET.parse(path).getroot()
    body = root.find(".//" + TEI + "text/" + TEI + "body")
    title = root.findtext(".//" + TEI + "titleStmt/" + TEI + "title") or work
    # Second stream with <q> stripped: the HA embeds hundreds of letters,
    # senatorial acclamations and speeches, most of them forged. Quoted
    # material is a different compositional register and could produce a
    # stylistic break that has nothing to do with a change of hand.
    return title.strip(), text_of(body), text_of(body, DROP | {TEI + "q"})


def perseus_group_works(group):
    d = os.path.join(PERSEUS, group)
    return sorted(w for w in os.listdir(d) if re.fullmatch(r"phi\d+|\w+\d+", w)
                  and os.path.isdir(os.path.join(d, w)))


# ------------------------------------------------------- HA metadata table
# order  = position in the transmitted collection (Palatine order)
# siglum = the name the collection itself claims as author
# rubric = primary (Hauptvita: a reigning emperor treated in sequence)
#          secondary (Nebenvita: co-emperor, caesar, usurper, or pretender)
# block  = pre-lacuna / post-lacuna. The Palatine manuscripts lose the lives
#          from Philip to Valerian; Stover & Kestemont 2016 report a stylistic
#          discontinuity that corresponds roughly to this break.
HA = [
    # work,   order, key,           siglum,       rubric,      block
    ("phi001", 1, "hadrianus", "Spartianus", "primary", "pre"),
    ("phi002", 2, "aelius", "Spartianus", "secondary", "pre"),
    ("phi003", 3, "antoninus_pius", "Capitolinus", "primary", "pre"),
    ("phi004", 4, "marcus", "Capitolinus", "primary", "pre"),
    ("phi005", 5, "verus", "Capitolinus", "secondary", "pre"),
    ("phi006", 6, "avidius_cassius", "Gallicanus", "secondary", "pre"),
    ("phi007", 7, "commodus", "Lampridius", "primary", "pre"),
    ("phi008", 8, "pertinax", "Capitolinus", "primary", "pre"),
    ("phi009", 9, "didius_iulianus", "Capitolinus", "primary", "pre"),
    ("phi010", 10, "septimius_severus", "Spartianus", "primary", "pre"),
    ("phi011", 11, "pescennius_niger", "Spartianus", "secondary", "pre"),
    ("phi012", 12, "clodius_albinus", "Capitolinus", "secondary", "pre"),
    ("phi013", 13, "caracalla", "Spartianus", "primary", "pre"),
    ("phi014", 14, "geta", "Spartianus", "secondary", "pre"),
    ("phi015", 15, "macrinus", "Capitolinus", "primary", "pre"),
    ("phi016", 16, "diadumenianus", "Lampridius", "secondary", "pre"),
    ("phi017", 17, "heliogabalus", "Lampridius", "primary", "pre"),
    ("phi018", 18, "alexander_severus", "Lampridius", "primary", "pre"),
    ("phi019", 19, "maximini_duo", "Capitolinus", "primary", "pre"),
    ("phi020", 20, "gordiani_tres", "Capitolinus", "primary", "pre"),
    ("phi021", 21, "maximus_balbinus", "Capitolinus", "primary", "pre"),
    ("phi022", 22, "valeriani_duo", "Pollio", "primary", "post"),
    ("phi023", 23, "gallieni_duo", "Pollio", "primary", "post"),
    ("phi024", 24, "tyranni_triginta", "Pollio", "secondary", "post"),
    ("phi025", 25, "claudius", "Pollio", "primary", "post"),
    ("phi026", 26, "aurelianus", "Vopiscus", "primary", "post"),
    ("phi027", 27, "tacitus", "Vopiscus", "primary", "post"),
    ("phi028", 28, "probus", "Vopiscus", "primary", "post"),
    ("phi029", 29, "quadrigae_tyrannorum", "Vopiscus", "secondary", "post"),
    ("phi030", 30, "carus_carinus_numerianus", "Vopiscus", "primary", "post"),
]

# Suetonius, Lives of the Caesars. One author, same genre, comparable lengths,
# and a real internal break in source quality: Suetonius was dismissed from the
# imperial secretariat and the last six lives are markedly shorter and thinner.
# This is the matched single-author null for the HA two-layer claim.
SUET = [
    ("abo011", 1, "iulius"), ("abo012", 2, "augustus"),
    ("abo013", 3, "tiberius"), ("abo014", 4, "caligula"),
    ("abo015", 5, "claudius"), ("abo016", 6, "nero"),
    ("abo017", 7, "galba"), ("abo018", 8, "otho"),
    ("abo019", 9, "vitellius"), ("abo020", 10, "vespasianus"),
    ("abo021", 11, "titus"), ("abo022", 12, "domitianus"),
]

# Nepos, De viris illustribus: a second single-author collection of short
# lives in transmitted order. Shorter and more formulaic than the HA, which
# makes it the harder of the two nulls.
NEPOS_ORDER = [
    "miltiades", "themistocles", "aristides", "pausanias", "cimon",
    "lysander", "alcibiades", "thrasybulus", "conon", "dion", "iphicrates",
    "chabrias", "timotheus", "datames", "epaminondas", "pelopidas",
    "agesilaus", "eumenes", "phocion", "timoleon", "de_regibus", "hamilcar",
    "hannibal", "cato", "atticus",
]

# Latin Library file names for the HA, for the second-witness check.
LATLIB_HA = {
    "hadrianus": "hadr", "aelius": "aelii", "antoninus_pius": "ant",
    "marcus": "marcant", "verus": "verus", "avidius_cassius": "avid",
    "commodus": "com", "pertinax": "pert", "didius_iulianus": "didiul",
    "septimius_severus": "sepsev", "pescennius_niger": "pesc",
    "clodius_albinus": "clod", "caracalla": "car", "geta": "geta",
    "macrinus": "mac", "diadumenianus": "diad", "heliogabalus": "helio",
    "alexander_severus": "alexsev", "maximini_duo": "max",
    "gordiani_tres": "gord", "maximus_balbinus": "maxbal",
    "valeriani_duo": "val", "gallieni_duo": "gall",
    "tyranni_triginta": "30", "claudius": "claud", "aurelianus": "aurel",
    "tacitus": "tacitus", "probus": "probus",
    "quadrigae_tyrannorum": "firmus", "carus_carinus_numerianus": "carus",
}


def main():
    segs = []

    for work, order, key, siglum, rubric, block in HA:
        title, raw, raw_nq = perseus_work("phi2331", work)
        tk = tokens(raw)
        segs.append(dict(corpus="HA", seg_id="HA:" + key, author="?",
                         siglum=siglum, order=order, rubric=rubric,
                         block=block, title=title, n_tokens=len(tk),
                         tokens=tk, tokens_nq=tokens(raw_nq)))

    for work, order, key in SUET:
        title, raw, raw_nq = perseus_work("phi1348", work)
        tk = tokens(raw)
        segs.append(dict(corpus="SUET", seg_id="SUET:" + key,
                         author="Suetonius", siglum="Suetonius", order=order,
                         rubric="primary",
                         block="pre" if order <= 6 else "post",
                         title=title, n_tokens=len(tk), tokens=tk,
                         tokens_nq=tokens(raw_nq)))

    for i, key in enumerate(NEPOS_ORDER, start=1):
        got = perseus_work("phi0588", "abo%03d" % i)
        if not got:
            continue
        title, raw, raw_nq = got
        tk = tokens(raw)
        segs.append(dict(corpus="NEPOS", seg_id="NEPOS:" + key,
                         author="Nepos", siglum="Nepos", order=i,
                         rubric="primary",
                         block="pre" if i <= 13 else "post",
                         title=title, n_tokens=len(tk), tokens=tk,
                         tokens_nq=tokens(raw_nq)))

    # Second witness for the HA, from the Latin Library.
    for key, stem in LATLIB_HA.items():
        p = os.path.join(LATLIB, "sha", stem + ".txt")
        raw = open(p, encoding="utf-8", errors="replace").read()
        # Drop the site header/footer lines the Latin Library appends.
        raw = raw.replace("The Latin Library", " ").replace(
            "The Classics Page", " ").replace("Historia Augusta", " ")
        tk = tokens(raw)
        segs.append(dict(corpus="HA_LL", seg_id="HA_LL:" + key, author="?",
                         siglum="", order=0, rubric="", block="",
                         title=key, n_tokens=len(tk), tokens=tk,
                         tokens_nq=tk))

    # Known-author control pool for the power curve. Prose only.
    controls = {
        "phi0588": ("Nepos", None),           # biography, 1st c. BC
        "phi1351": ("Tacitus", None),         # historiography
        "phi0631": ("Sallust", None),
        "phi0448": ("Caesar", None),
        "phi1254": ("Gellius", None),
        "phi1318": ("PliniusMinor", None),
        "phi1242": ("Florus", None),
        "stoa0023": ("Ammianus", None),       # 4th c., the HA's own period
        "stoa0162": ("Hieronymus", None),     # 4th c.
    }
    for group, (name, _) in controls.items():
        if not os.path.isdir(os.path.join(PERSEUS, group)):
            print("missing control group", group, file=sys.stderr)
            continue
        for work in perseus_group_works(group):
            got = perseus_work(group, work)
            if not got:
                continue
            title, raw, raw_nq = got
            tk = tokens(raw)
            if len(tk) < 500:
                continue
            segs.append(dict(corpus="CTRL", seg_id="%s:%s" % (name, work),
                             author=name, siglum=name, order=0,
                             rubric="", block="", title=title,
                             n_tokens=len(tk), tokens=tk,
                             tokens_nq=tokens(raw_nq)))

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "segments.json"), "w") as fh:
        json.dump(segs, fh)

    for c in ("HA", "SUET", "NEPOS", "HA_LL", "CTRL"):
        sub = [s for s in segs if s["corpus"] == c]
        print("%-6s %3d segments %8d tokens" %
              (c, len(sub), sum(s["n_tokens"] for s in sub)))


if __name__ == "__main__":
    main()
