#!/usr/bin/env python3
"""Full-corpus concordance for Latin lemmata over the Latin Library and Perseus
canonical-latinLit corpora.

Design notes
------------
* Orthography is normalised (lowercase, v->u, j->i, ae/oe left alone) before matching,
  because the Latin Library prints headers in classical capitals with V for U.
* Matching is against an explicit list of inflected FORMS, with word boundaries, so
  `musculus` never silently collects `musculosus`.
* Every hit carries its source file so any count in the write-up can be re-derived.
"""
import os, re, sys, json, unicodedata, argparse

TOKEN_RE = re.compile(r"[a-z]+")

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def normalise(text):
    text = strip_accents(text.lower())
    text = text.replace('v', 'u').replace('j', 'i')
    return text

def decl2_masc(stem):
    """Second-declension masculine forms for a stem like 'muscul'."""
    return [stem + e for e in
            ('us', 'i', 'o', 'um', 'e', 'orum', 'is', 'os')]

def decl1_fem(stem):
    return [stem + e for e in ('a', 'ae', 'am', 'arum', 'is', 'as')]

def iter_latin_library(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith('.txt'):
                continue
            if fn in ('README.md', 'LICENSE.md'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding='utf-8', errors='replace') as fh:
                    yield os.path.relpath(path, root), fh.read()
            except OSError:
                continue

TAG_RE = re.compile(r'<[^>]+>')

def iter_perseus(root):
    """Perseus TEI XML. Strip tags crudely: we only need word-level context, and the
    locator we report is the file, not the TEI citation path."""
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if not fn.endswith('.xml'):
                continue
            if 'lat' not in fn:      # skip Greek-side and English translations
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding='utf-8', errors='replace') as fh:
                    raw = fh.read()
            except OSError:
                continue
            body = raw.split('<text', 1)[-1]
            yield os.path.relpath(path, root), TAG_RE.sub(' ', body)

def concordance(corpora, forms, window=18):
    formset = set(forms)
    hits = []
    stats = {}
    for corpus_name, iterator in corpora:
        nfiles = ntokens = 0
        for locator, text in iterator:
            norm = normalise(text)
            toks = TOKEN_RE.findall(norm)
            nfiles += 1
            ntokens += len(toks)
            if not formset & set(toks):
                continue
            # re-tokenise keeping original-case surface for display
            surf = TOKEN_RE.findall(strip_accents(text.lower()))
            for i, t in enumerate(toks):
                if t in formset:
                    lo, hi = max(0, i - window), min(len(toks), i + window + 1)
                    hits.append({
                        'corpus': corpus_name,
                        'file': locator,
                        'form': surf[i] if i < len(surf) else t,
                        'norm_form': t,
                        'token_index': i,
                        'left': ' '.join(surf[lo:i]) if i < len(surf) else ' '.join(toks[lo:i]),
                        'right': ' '.join(surf[i+1:hi]) if hi <= len(surf) else ' '.join(toks[i+1:hi]),
                    })
        stats[corpus_name] = {'files': nfiles, 'tokens': ntokens}
    return hits, stats

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ll', required=True, help='path to Latin Library corpus root')
    ap.add_argument('--perseus', default=None, help='path to Perseus canonical-latinLit root')
    ap.add_argument('--forms', required=True, help='comma-separated inflected forms')
    ap.add_argument('--out', required=True)
    ap.add_argument('--window', type=int, default=18)
    args = ap.parse_args()

    corpora = [('latin_library', iter_latin_library(args.ll))]
    if args.perseus:
        corpora.append(('perseus', iter_perseus(args.perseus)))

    forms = [normalise(f.strip()) for f in args.forms.split(',') if f.strip()]
    hits, stats = concordance(corpora, forms, args.window)
    out = {'forms': forms, 'corpus_stats': stats, 'n_hits': len(hits), 'hits': hits}
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"forms={forms}")
    for k, v in stats.items():
        print(f"  {k}: {v['files']} files, {v['tokens']:,} tokens")
    print(f"  hits: {len(hits)}")

if __name__ == '__main__':
    main()
