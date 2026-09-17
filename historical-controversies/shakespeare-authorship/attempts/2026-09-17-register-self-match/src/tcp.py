"""Extraction of running text from EEBO-TCP XML, and structural classification.

Both registers in this attempt come from the same source - EEBO-TCP - so that
register is not confounded with edition or transcription convention. The
engdracor play corpus used by the 2026-09-05 calibration is itself derived from
these same TCP transcriptions (its `sourceid` attributes ARE TCP ids), which is
what makes the comparison legitimate; `pipeline_control.py` measures the residual
extraction difference rather than assuming it away.

Drama is identified by MARKUP, not by title: a TCP text with <sp> speech
elements is a performance text. Titles lie ("A strange horse-race ... comes in
the catch-poles masque" is a prose pamphlet); <sp> does not.
"""
import re, os, collections

TCP_DIR = os.environ.get('TCP_XML_DIR', '/tmp/w/xml')
WORD = re.compile(r"[a-z']+")


def raw(tcp_id):
    p = os.path.join(TCP_DIR, tcp_id + '.xml')
    return open(p, errors='replace').read()


def structure(s):
    """Counts that decide register, plus the TCP gap rate (the data-quality
    metric analogous to a long-s damage rate: <gap> marks text the transcriber
    could not read)."""
    return {
        'sp': len(re.findall(r'<sp\b', s)),
        'speaker': len(re.findall(r'<speaker\b', s)),
        'stage': len(re.findall(r'<stage\b', s)),
        'l': len(re.findall(r'<l\b', s)),
        'p': len(re.findall(r'<p\b', s)),
        'gap': len(re.findall(r'<gap\b', s)),
    }


def words(s):
    """Running text only.

    Drops the teiHeader, and drops <speaker>/<stage> exactly as the 2026-09-05
    play pipeline does, so that a play extracted here is comparable with the
    same play extracted there. <desc> is dropped because TCP uses it for
    editorial descriptions of illegible passages and ornaments - leaving it in
    injects modern English into an early modern text.
    """
    body = s.split('<text', 1)[-1]
    body = re.sub(r'<teiHeader.*?</teiHeader>', ' ', body, flags=re.S)
    body = re.sub(r'<speaker>.*?</speaker>', ' ', body, flags=re.S)
    body = re.sub(r'<stage>.*?</stage>', ' ', body, flags=re.S)
    body = re.sub(r'<desc>.*?</desc>', ' ', body, flags=re.S)
    body = re.sub(r'<note>.*?</note>', ' ', body, flags=re.S)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = body.replace('&amp;', '&').replace('&apos;', "'")
    return WORD.findall(body.lower())


def jaccard(a, b, k=3000):
    """Near-duplicate detection between two word streams, on the multiset of
    their commonest types. Two editions of the same work share nearly all of it."""
    ca, cb = collections.Counter(a), collections.Counter(b)
    va = set(w for w, _ in ca.most_common(k))
    vb = set(w for w, _ in cb.most_common(k))
    return len(va & vb) / max(1, len(va | vb))


def shingles(ws, n=8):
    return set(hash(tuple(ws[i:i + n])) for i in range(0, len(ws) - n, 3))


def overlap(a, b):
    """Fraction of the shorter text's 8-grams that appear in the longer.
    This is what catches a reprint under a new title."""
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / min(len(sa), len(sb))
