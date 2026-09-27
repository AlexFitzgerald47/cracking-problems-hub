#!/usr/bin/env python3
"""NULL MODEL for the Woods manoeuvre.

Woods's inference has the form: "the text names an ordinary creature/object X in a
military setting; Latin also has a siege device called X; therefore the source meant
the device and the biographer mistook it for the creature."

That inference is only evidence if such homonyms are RARE. If Roman siege vocabulary is
systematically zoomorphic, then a device-homonym can be found for very many concrete
nouns, and finding one for `conchae` is the expected outcome of looking, not a discovery.

So: count how many distinct Roman military devices are named after an ordinary animal or
object, verifying each against the corpus rather than from memory. Each candidate must
be shown BOTH in its ordinary sense AND in a military-technical context.
"""
import os, re, sys, json, collections

CANDIDATES = {
 # device name : (regex of inflected stem, gloss of ordinary sense)
 'musculus':  (r'\bmuscul(us|i|o|um|orum|is|os)\b',      'mussel / little mouse / muscle'),
 'testudo':   (r'\btestudin?(e|is|em|es|ibus|um)?\b',    'tortoise'),
 'aries':     (r'\b(aries|ariet(is|i|em|e|es|ibus|um))\b','ram (male sheep)'),
 'vinea':     (r'\bvine(a|ae|am|is|as|arum)\b',          'vineyard'),
 'corvus':    (r'\bcorv(us|i|o|um|orum|is|os)\b',        'raven'),
 'scorpio':   (r'\bscorpi(o|onis|onem|ones|onibus|onum)\b','scorpion'),
 'onager':    (r'\bonagr?(er|i|o|um|orum|is|os)\b',      'wild ass'),
 'lupus':     (r'\blup(us|i|o|um|orum|is|os)\b',         'wolf'),
 'cuniculus': (r'\bcunicul(us|i|o|um|orum|is|os)\b',     'rabbit'),
 'delphinus': (r'\bdelphin(us|i|o|um|orum|is|os)\b',     'dolphin'),
 'falx':      (r'\b(falx|falc(is|i|em|e|es|ibus|ium))\b','sickle / pruning hook'),
 'grus':      (r'\b(grus|gru(is|i|em|e|es|ibus|um))\b',  'crane (bird)'),
 'aper':      (r'\b(aper|apr(i|o|um|orum|is|os))\b',     'boar'),
}
MILITARY_MARKERS = re.compile(
  r'\b(mur(us|i|o|um|is)|oppid|obsid|obpugn|oppugn|castr|turr|hostium|hostes|hostibus|'
  r'milit|legio|legion|aggere|agger|fossat|machin|tormento|tormenta|bellator|'
  r'arietes|testudines|uineas|vineas|plutei|exercit)[a-z]*\b')

def files(root):
    for dp, _, fs in os.walk(root):
        for fn in fs:
            if fn.endswith('.txt'):
                yield os.path.join(dp, fn)

def norm(t):
    return re.sub(r'[^a-z ]', ' ', t.lower().replace('v','u').replace('j','i'))

def main(root):
    # normalise the patterns the same way the text is normalised
    pats = {k: (re.compile(norm_pat(v[0])), v[1]) for k, v in CANDIDATES.items()}
    tot = collections.Counter(); mil = collections.Counter()
    examples = collections.defaultdict(list)
    for path in files(root):
        try:
            txt = norm(open(path, encoding='utf-8', errors='replace').read())
        except OSError:
            continue
        for name, (pat, _) in pats.items():
            for m in pat.finditer(txt):
                tot[name] += 1
                lo, hi = max(0, m.start()-420), m.end()+420
                win = txt[lo:hi]
                if MILITARY_MARKERS.search(win):
                    mil[name] += 1
                    if len(examples[name]) < 2:
                        examples[name].append((os.path.basename(path),
                                               txt[max(0,m.start()-70):m.end()+70]))
    rows = []
    for name, (_, gloss) in sorted(pats.items(), key=lambda kv: -mil[kv[0]]):
        rows.append({'device': name, 'ordinary_sense': gloss,
                     'total_attestations': tot[name],
                     'in_military_context': mil[name],
                     'pct_military': round(100*mil[name]/tot[name], 1) if tot[name] else 0.0,
                     'examples': examples[name]})
        print(f"  {name:11s} {gloss:26s} total={tot[name]:5d}  military-context={mil[name]:4d} ({rows[-1]['pct_military']:4.1f}%)")
    json.dump(rows, open('results/zoonym_null.json','w'), indent=1, ensure_ascii=False)
    n = sum(1 for r in rows if r['in_military_context'] >= 5)
    print(f"\n  Ordinary-language nouns that ALSO denote a military device,")
    print(f"  attested >=5 times in a military context: {n} of {len(rows)} tested.")

def norm_pat(p):
    return p.replace('v','u').replace('j','i')

if __name__ == '__main__':
    main(sys.argv[1])
