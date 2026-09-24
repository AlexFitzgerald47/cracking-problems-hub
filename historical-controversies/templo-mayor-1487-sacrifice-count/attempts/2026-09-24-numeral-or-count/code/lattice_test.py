#!/usr/bin/env python3
"""Vigesimal-lattice test on quantities extracted from the chronicles.

VIG      : n % 400 == 0          (round in Nahuatl tzontli units)
DEC      : n % 1000 == 0         (round in Spanish decimal units)
VIG\\DEC  : round in vigesimal but NOT in decimal -> the diagnostic class.
           Note 400k is divisible by 1000 iff k = 0 mod 5, so 4/5 of all
           multiples of 400 lie in VIG\\DEC. A purely decimal rounder lands
           there never; an arbitrary tally lands there with prob 1/500.
XIQ      : n % 8000 == 0         (whole xiquipilli)
"""
import csv, sys, collections, random, math

WORKS = {
 'duran':          ['duran_v1_scanA','duran_v2_scanA'],
 'duran_REPLICATE':['duran_v1_scanB','duran_v2_scanB'],
 'ixtlilxochitl':  ['ixtl_B0'],
 'ixtlilxochitl_REPLICATE':['ixtl_C0'],
 'mendieta':       ['mendieta_scanA'],
 'tezozomoc':      ['tezozomoc_scanB'],
 'tezozomoc_1878_with_editor_notes':['tezozomoc_scanA'],
 'torquemada':     ['torquemada_v1','torquemada_v2'],
}

def load(path):
    rows=[]
    for r in csv.DictReader(open(path), delimiter='\t'):
        r['value']=int(r['value']); rows.append(r)
    return rows

def classify(n):
    return dict(vig=n%400==0, dec=n%1000==0, xiq=n%8000==0,
                vignotdec=(n%400==0 and n%1000!=0))

def table(rows, minv, subject=None):
    out=[]
    for w,files in WORKS.items():
        sel=[r for r in rows if r['text'] in files and r['value']>=minv
             and r['value']<10_000_000
             and (subject is None or r['subject']==subject)]
        vals=[r['value'] for r in sel]
        n=len(vals)
        if n==0: out.append((w,0,0,0,0,0)); continue
        c=[classify(v) for v in vals]
        out.append((w,n,
                    sum(x['vig'] for x in c)/n,
                    sum(x['dec'] for x in c)/n,
                    sum(x['vignotdec'] for x in c)/n,
                    sum(x['xiq'] for x in c)/n))
    return out

def show(title, t):
    print("\n"+title)
    VD='%VIG_not_DEC'
    print(f"{'work':42s} {'n':>5s} {'%div400':>8s} {'%div1000':>9s} {VD:>9s} {'%div8000':>9s}")
    for w,n,a,b,c,d in t:
        print(f"{w:42s} {n:5d} {a*100:7.1f}% {b*100:8.1f}% {c*100:8.1f}% {d*100:8.1f}%")

if __name__=='__main__':
    rows=load(sys.argv[1] if len(sys.argv)>1 else 'quantities.tsv')
    show("ALL quantities >= 400", table(rows,400))
    show("PERSON quantities >= 400", table(rows,400,'person'))
    show("PERSON quantities >= 2000", table(rows,2000,'person'))
    show("ALL quantities >= 10000", table(rows,10000))

    # --- distinct-value view (a repeated stock phrase should not count 30x) ---
    print("\nDistinct values >= 2000, person, per work:")
    for w,files in WORKS.items():
        vals=sorted({r['value'] for r in rows if r['text'] in files
                     and r['subject']=='person' and 2000<=r['value']<10_000_000})
        vd=[v for v in vals if v%400==0 and v%1000!=0]
        print(f"  {w:42s} n={len(vals):3d}  VIGnotDEC={len(vd):2d} {vd}")
