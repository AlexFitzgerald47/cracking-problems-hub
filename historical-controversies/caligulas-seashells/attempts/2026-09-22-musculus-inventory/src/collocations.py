#!/usr/bin/env python3
"""Which verbs govern `musculus` in each sense, and which govern `concha`?

Suetonius's order is `conchas legere ... galeas et sinus replere`. Woods's reading
requires that the underlying order was about `musculi`. So: is *legere/colligere*
ever construed with `musculus` in any sense, and what verbs are construed with the
military and nautical senses instead?

Verb families are matched on stems in a +-18-word window. This is a blunt instrument -
it finds co-occurrence, not syntactic government - so every hit it reports is printed
for inspection rather than counted silently.
"""
import json, re, sys, collections, csv

GATHER = {
  'lego (gather/pick up)':      r'\b(leg|colleg|collig|conleg|collect|lect)[a-z]*\b',
  'capto/capio (catch)':        r'\b(capt|capi|cepi|cap[ei]r)[a-z]*\b',
  'congero/coacervo (heap up)': r'\b(conger|congess|coacerv|cumul)[a-z]*\b',
  'quaero (seek)':              r'\b(quaer|quaesi|quaesit)[a-z]*\b',
  'repleo/impleo (fill)':       r'\b(reple|impl|inpl|compl)[a-z]*\b',
}
BUILD_MOVE = {
  'facio/construo (build)':     r'\b(fac[ei]r|faciunt|fecer|construe|struct|struan|aedific|instituer)[a-z]*\b',
  'ago/admoveo/promoveo (bring up)': r'\b(admou|admov|promou|promov|adigu|agere|agunt|proferr|profert|iung)[a-z]*\b',
  'incendo/uro (burn)':         r'\b(incend|uror|ussi|flamm|ignis|igni)[a-z]*\b',
  'sub + abl (shelter under)':  r'\bsub\b',
}

def scan(hits, label_of, families):
    out = collections.defaultdict(list)
    for h in hits:
        ctx = (h['left'] + ' ' + h['right']).lower()
        lab = label_of(h)
        for fam, pat in families.items():
            m = re.search(pat, ctx)
            if m:
                out[(lab, fam)].append((h['file'], m.group(0),
                                        h['left'][-45:] + ' [' + h['form'].upper() + '] ' + h['right'][:45]))
    return out

def main():
    senses = {}
    with open('results/musculus_senses.tsv', encoding='utf-8') as fh:
        for row in csv.DictReader(fh, delimiter='\t'):
            senses[(row['file'], int(row['token_index']))] = row['sense']
    m = json.load(open('results/musculus_canonical.json'))['hits']
    label = lambda h: senses.get((h['file'], h['token_index']), '?')

    print("=" * 78)
    print("A. GATHERING verbs in the context of `musculus`, by sense")
    print("=" * 78)
    res = scan(m, label, GATHER)
    for sense in ('MIL', 'NAV', 'SHELL', 'FISH', 'MOUSE', 'ANAT'):
        fams = {f: v for (s, f), v in res.items() if s == sense}
        n = sum(1 for h in m if label(h) == sense)
        if not fams:
            print(f"\n  {sense} (n={n}): NO gathering verb in any context")
            continue
        print(f"\n  {sense} (n={n}):")
        for f, v in fams.items():
            print(f"    {f}: {len(v)}")
            for fl, mt, kw in v[:4]:
                print(f"        <{mt}> {fl}")
                print(f"           {kw}")

    print("\n" + "=" * 78)
    print("B. BUILDING / MOVING verbs with military+nautical `musculus`")
    print("=" * 78)
    milnav = [h for h in m if label(h) in ('MIL', 'NAV')]
    res2 = scan(milnav, label, BUILD_MOVE)
    for (s, f), v in sorted(res2.items()):
        print(f"  {s} / {f}: {len(v)}")

    print("\n" + "=" * 78)
    print("C. `concha`: is *legere* its normal verb?")
    print("=" * 78)
    c = json.load(open('results/concha_canonical.json'))['hits']
    res3 = scan(c, lambda h: 'CONCHA', GATHER)
    for (s, f), v in sorted(res3.items(), key=lambda kv: -len(kv[1])):
        print(f"  {f}: {len(v)} of {len(c)} concha attestations")
        for fl, mt, kw in v[:5]:
            print(f"      <{mt}> {fl}: {kw}")

if __name__ == '__main__':
    main()
