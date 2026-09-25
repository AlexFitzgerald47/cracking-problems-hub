#!/usr/bin/env python3
"""Is a bar face's letter balance INHERITED from the inventory, or its own?

The refuter's objection to the 2026-09-24 claim was structural: the claim said
the balance holds only on a deduplicated inventory, which is not a physical
object, so only a person composing the text could have produced it -- and the
refuter answered that a bar FACE is a physical object and is itself balanced.

Both can be true without the objection biting. A face is stamped with a subset
of the same 16 strings, so if the 16 strings are balanced then a face that
carries most of them once each is *forced* to be nearly balanced. The test:
hold each face's layout fixed -- same number of lines, same string identity in
each slot, same lengths -- and replace the 16 strings with 16 pseudo-strings
made by dealing the observed 261-letter inventory into the observed lengths.
That null preserves the inventory balance and destroys everything else. If the
observed face chi2 sits inside it, the face carries no balance information of
its own.
"""
import collections, random, os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RNG = random.Random(20260925)

strings = [l.strip() for l in open(os.path.join(HERE,"data","cryptograms_corrected.txt")) if l.strip()]
lengths = [len(s) for s in strings]
pool = list("".join(strings))
idx = {s:i for i,s in enumerate(strings)}

rows=[]
for line in open(os.path.join(HERE,"data","instances_photographic.tsv")):
    if line.startswith("#") or line.startswith("face\t"): continue
    f, ln, s, conf, new = line.rstrip("\n").split("\t")
    rows.append((f, s))
faces = sorted(set(f for f,_ in rows))

def chi2(text):
    c=collections.Counter(text); n=len(text); e=n/26
    return sum((c.get(x,0)-e)**2 for x in A)/e

def deal():
    p = pool[:]; RNG.shuffle(p); out=[]; k=0
    for L in lengths:
        out.append("".join(p[k:k+L])); k+=L
    return out

REPS = 20000
print(f"null: {REPS} deals of the observed 261-letter inventory into the observed 16 lengths\n")
print(f"{'face':>22} {'lines':>5} {'distinct':>8} {'n':>5} {'chi2':>8} {'null mean':>10} {'null sd':>8} {'p(<=)':>8}")
res=[]
# precompute face slot lists
face_slots = {f: [idx[s] for ff,s in rows if ff==f] for f in faces}
face_slots["ALL INSTANCES"] = [idx[s] for _,s in rows]
face_slots["16 distinct"] = list(range(16))
nulls = {k: [] for k in face_slots}
for _ in range(REPS):
    d = deal()
    for k, slots in face_slots.items():
        nulls[k].append(chi2("".join(d[i] for i in slots)))
for k, slots in face_slots.items():
    obs_text = "".join(strings[i] for i in slots)
    o = chi2(obs_text)
    arr = sorted(nulls[k]); m = sum(arr)/len(arr)
    sd = (sum((x-m)**2 for x in arr)/len(arr))**0.5
    p = (sum(1 for x in arr if x <= o)+1)/(len(arr)+1)
    print(f"{k:>22} {len(slots):>5} {len(set(slots)):>8} {len(obs_text):>5} {o:>8.3f} {m:>10.3f} {sd:>8.3f} {p:>8.4f}")
    res.append({"face":k,"lines":len(slots),"distinct":len(set(slots)),"n":len(obs_text),
                "chi2":o,"null_mean":m,"null_sd":sd,"p_le":p})
json.dump(res, open(os.path.join(HERE,"out","inherit.json"),"w"), indent=2)
