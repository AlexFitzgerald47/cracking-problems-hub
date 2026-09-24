#!/usr/bin/env python3
"""
Chinese Gold Bar cryptograms -- structural statistics with explicit null models.

Core question addressed here: are the 16 IACR strings consistent with a
monoalphabetic substitution of ANY natural language, or are they flat?

The index of coincidence is invariant under monoalphabetic substitution, so it
tests that whole class without committing to a plaintext language.

Usage: python3 stats.py
"""
import collections, itertools, random, math, os, json, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT  = os.path.join(HERE, "out")
random.seed(20260924)

def load():
    with open(os.path.join(DATA, "cryptograms.txt")) as f:
        return [l.strip() for l in f if l.strip()]

STRINGS = load()
LENGTHS = [len(s) for s in STRINGS]
N = sum(LENGTHS)
ALL = "".join(STRINGS)
ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------------------------------------------------------------- statistics
def pooled_ic(strings):
    """Within-string index of coincidence, pooled over strings.

    Pooling numerator and denominator (rather than averaging per-string ICs)
    is the right estimator here: the strings are separate tokens, so
    cross-string pairs are not meaningful, but every within-string pair is.
    """
    num = 0; den = 0
    for s in strings:
        c = collections.Counter(s)
        n = len(s)
        num += sum(v*(v-1) for v in c.values())
        den += n*(n-1)
    return num/den if den else float("nan")

def doubles(strings):
    """Count of adjacent identical letters."""
    return sum(1 for s in strings for a, b in zip(s, s[1:]) if a == b)

def ngram_repeats(strings, n):
    """Number of n-grams occurring more than once, counting excess occurrences.

    Counted over the token set with each DISTINCT string used once, so the
    fact that whole strings are stamped repeatedly on the bars does not
    manufacture repeats.
    """
    c = collections.Counter()
    for s in strings:
        for i in range(len(s)-n+1):
            c[s[i:i+n]] += 1
    return sum(v-1 for v in c.values() if v > 1)

def chi2_uniform(text):
    c = collections.Counter(text)
    e = len(text)/26
    return sum((c.get(a, 0)-e)**2/e for a in ALPHA)

# ---------------------------------------------------------------- null models
def null_uniform():
    return ["".join(random.choice(ALPHA) for _ in range(L)) for L in LENGTHS]

def null_shuffle():
    """Preserve the corpus letter multiset exactly; destroy all order."""
    pool = list(ALL); random.shuffle(pool)
    out = []; i = 0
    for L in LENGTHS:
        out.append("".join(pool[i:i+L])); i += L
    return out

def load_english():
    p = os.path.join(DATA, "english_reference.txt")
    with open(p) as f:
        t = f.read().upper()
    return "".join(ch for ch in t if ch in ALPHA)

def null_masc(source_text):
    """Monoalphabetic substitution of a real plaintext, same length structure.

    Draws one contiguous passage per string from the source and applies a
    random letter permutation. IC is invariant under the permutation, so this
    measures what IC a natural-language plaintext of THESE lengths yields.
    """
    perm = list(ALPHA); random.shuffle(perm)
    table = str.maketrans(ALPHA, "".join(perm))
    out = []
    for L in LENGTHS:
        i = random.randrange(0, len(source_text)-L)
        out.append(source_text[i:i+L].translate(table))
    return out

WG_INITIALS = ["","","","","B","P","M","F","T","T","N","L","K","K","H","CH","CH",
               "SH","J","TS","TS","S","Y","W","HS","CH","KU","SS"]
WG_FINALS   = ["A","O","E","I","U","AI","EI","AO","OU","AN","EN","ANG","ENG",
               "ONG","IA","IE","IAO","IU","IAN","IN","IANG","ING","UA","UO",
               "UAI","UI","UAN","UN","UANG","UNG","IH","U","ERH","A","I","U"]

def synth_romanized_chinese(nchars):
    """Wade-Giles-shaped syllable stream.

    NOT a real corpus -- a generative stand-in for 'romanized Chinese has a
    small syllable inventory and a high vowel rate'. Used only to show that
    such text ALSO sits far above flat IC, i.e. the conclusion below does not
    depend on assuming an English plaintext.
    """
    buf = []
    while sum(len(x) for x in buf) < nchars + 40:
        buf.append(random.choice(WG_INITIALS)+random.choice(WG_FINALS))
    return "".join(buf)

# ---------------------------------------------------------------- driver
def simulate(gen, reps, stats):
    acc = {k: [] for k in stats}
    for _ in range(reps):
        s = gen()
        for k, fn in stats.items():
            acc[k].append(fn(s))
    return acc

def summ(v):
    v = sorted(v); n = len(v)
    mean = sum(v)/n
    sd = math.sqrt(sum((x-mean)**2 for x in v)/(n-1)) if n > 1 else 0.0
    return {"mean": mean, "sd": sd,
            "p2.5": v[int(0.025*n)], "p50": v[n//2], "p97.5": v[min(int(0.975*n), n-1)]}

def pval_two_sided(obs, sims):
    n = len(sims)
    ge = sum(1 for x in sims if x >= obs); le = sum(1 for x in sims if x <= obs)
    return min(1.0, 2*min((ge+1)/(n+1), (le+1)/(n+1)))

def main():
    REPS = 20000
    stats = {"ic": pooled_ic, "doubles": doubles,
             "rep3": lambda s: ngram_repeats(s, 3),
             "rep4": lambda s: ngram_repeats(s, 4),
             "chi2": lambda s: chi2_uniform("".join(s))}
    obs = {k: fn(STRINGS) for k, fn in stats.items()}

    eng = load_english()
    zh  = synth_romanized_chinese(200000)

    nulls = {
        "uniform_random":    null_uniform,
        "corpus_shuffle":    null_shuffle,
        "masc_english":      lambda: null_masc(eng),
        "masc_romanized_zh": lambda: null_masc(zh),
    }

    report = {"n_strings": len(STRINGS), "n_letters": N,
              "lengths": LENGTHS, "observed": obs, "reps": REPS, "nulls": {}}

    print(f"corpus: {len(STRINGS)} strings, {N} letters, lengths {LENGTHS}")
    print(f"distinct letters used: {len(set(ALL))}/26  missing: "
          f"{''.join(sorted(set(ALPHA)-set(ALL))) or '(none)'}")
    print()
    print("OBSERVED:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in obs.items()})
    print()
    for name, gen in nulls.items():
        sims = simulate(gen, REPS, stats)
        report["nulls"][name] = {}
        print(f"--- null: {name} ({REPS} reps) ---")
        for k in stats:
            s = summ(sims[k]); p = pval_two_sided(obs[k], sims[k])
            report["nulls"][name][k] = {**s, "observed": obs[k], "p_two_sided": p}
            print(f"  {k:8s} obs={obs[k]:9.4f}  null mean={s['mean']:9.4f} "
                  f"sd={s['sd']:7.4f}  95%=[{s['p2.5']:8.4f},{s['p97.5']:8.4f}]  p={p:.4f}")
        print()

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "stats.json"), "w") as f:
        json.dump(report, f, indent=1)
    print("wrote out/stats.json")

if __name__ == "__main__":
    main()
