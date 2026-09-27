"""Shared loaders and statistics for the Blitz authenticity battery.

A "document" is a list of pages; a page is a list of lines; a line is a list of
symbol tokens.  Blitz pages are one ASCII character per glyph.  Copiale and Borg
use the cipher_benchmark canonical global symbol map (S001...); Borg's '|' word
separator is stripped so that its text has the same no-word-boundary shape as the
Blitz transcription.
"""
import glob, os, random, math
from collections import Counter


def load_blitz(datadir):
    pages = {}
    for p in ("p7", "p8"):
        lines = [list(l.strip()) for l in open(os.path.join(datadir, p + ".txt")) if l.strip()]
        pages[p] = lines
    return pages


def load_canonical(dirpath):
    """cipher_benchmark canonical transcriptions -> {page_id: [[tok,...], ...]}"""
    pages = {}
    for f in sorted(glob.glob(os.path.join(dirpath, "*.txt"))):
        lines = []
        for l in open(f):
            l = l.replace("|", " ")
            tk = l.split()
            if tk:
                lines.append(tk)
        if lines:
            pages[os.path.basename(f)[:-4]] = lines
    return pages


def flat(lines):
    return [t for l in lines for t in l]


# ---------- statistics ----------

def bigram_ic(lines):
    """P(two randomly chosen within-line adjacent pairs are the same pair)."""
    c = Counter()
    n = 0
    for l in lines:
        for i in range(len(l) - 1):
            c[(l[i], l[i + 1])] += 1
            n += 1
    if n < 2:
        return None, 0
    s = sum(v * (v - 1) for v in c.values())
    return s / (n * (n - 1)), n


def doublets(lines):
    return sum(1 for l in lines for i in range(len(l) - 1) if l[i] == l[i + 1])


def shuffle_within_lines(lines, rng):
    out = []
    for l in lines:
        m = list(l)
        rng.shuffle(m)
        out.append(m)
    return out


def shuffle_null(lines, statfn, nperm, seed=0):
    """Return (observed, mean, sd, z, p_upper, p_lower) under within-line shuffling."""
    rng = random.Random(seed)
    obs = statfn(lines)
    vals = []
    for _ in range(nperm):
        vals.append(statfn(shuffle_within_lines(lines, rng)))
    m = sum(vals) / len(vals)
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    sd = math.sqrt(var)
    ge = sum(1 for v in vals if v >= obs)
    le = sum(1 for v in vals if v <= obs)
    z = (obs - m) / sd if sd > 0 else float("nan")
    return dict(obs=obs, mean=m, sd=sd, z=z,
                p_upper=(ge + 1) / (nperm + 1), p_lower=(le + 1) / (nperm + 1),
                nperm=nperm)


def chi2_homogeneity(a, b):
    """Two-sample chi-square homogeneity statistic over the pooled symbol set."""
    ca, cb = Counter(a), Counter(b)
    na, nb = len(a), len(b)
    n = na + nb
    x = 0.0
    for s in set(ca) | set(cb):
        tot = ca[s] + cb[s]
        ea, eb = tot * na / n, tot * nb / n
        x += (ca[s] - ea) ** 2 / ea + (cb[s] - eb) ** 2 / eb
    return x


def homogeneity_z(a, b, nperm=5000, seed=0):
    rng = random.Random(seed)
    obs = chi2_homogeneity(a, b)
    pool = list(a) + list(b)
    na = len(a)
    vals = []
    for _ in range(nperm):
        rng.shuffle(pool)
        vals.append(chi2_homogeneity(pool[:na], pool[na:]))
    m = sum(vals) / len(vals)
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    ge = sum(1 for v in vals if v >= obs)
    return dict(obs=obs, mean=m, sd=sd, z=(obs - m) / sd if sd else float("nan"),
                p_upper=(ge + 1) / (nperm + 1), nperm=nperm)


def contiguous_block(lines, want, start_line=0):
    """Contiguous token block of length `want` starting at a line boundary."""
    out = []
    for l in lines[start_line:]:
        out.extend(l)
        if len(out) >= want:
            break
    return out[:want] if len(out) >= want else None


def line_block(lines, want, start_line=0):
    """Contiguous whole lines totalling >= want tokens (keeps line structure)."""
    out, n = [], 0
    for l in lines[start_line:]:
        out.append(l)
        n += len(l)
        if n >= want:
            return out
    return None
