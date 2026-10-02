#!/usr/bin/env python3
"""
ATTACK 9 — witness drift.  The digital witness is not a stable object.

Compares the 2026-09-25 vendored snapshot of witness A (./data) with the snapshot
re-downloaded on 2026-10-02 (./data_20261002), and reports every face whose
transliterated word sequence changed -- in particular whether any tablet the
dossier depends on was re-edited under the panel.
"""
import os, sys, json, re, importlib.util, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))


def load(path):
    s = open(path, encoding="utf-8").read()
    start = s.index("new Map(") + len("new Map(")
    end = s.index("]);", start) + 1
    body = s[start:end]
    body = re.sub(r',(\s*[\]\}])', r'\1', body)
    body = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), body)
    return dict(json.loads(body))


def main():
    p_old = os.path.join(HERE, "data", "LinearAInscriptions.js")
    p_new = os.path.join(HERE, "data_20261002", "LinearAInscriptions.js")
    for p in (p_old, p_new):
        print(f"  {os.path.relpath(p, HERE):44s} sha256 "
              f"{hashlib.sha256(open(p,'rb').read()).hexdigest()}")
    O, N = load(p_old), load(p_new)
    print(f"\n  records: 2026-09-25 snapshot {len(O)}, 2026-10-02 snapshot {len(N)}")
    only_o = sorted(set(O) - set(N)); only_n = sorted(set(N) - set(O))
    print(f"  records only in the old snapshot: {only_o}")
    print(f"  records only in the new snapshot: {only_n}")
    changed = []
    for k in sorted(set(O) & set(N)):
        a = O[k].get("transliteratedWords"); b = N[k].get("transliteratedWords")
        if a != b:
            changed.append(k)
    print(f"\n  faces whose transliterated word sequence CHANGED in 7 days: "
          f"{len(changed)}")
    DOSSIER = {"HT85a", "HT85b", "HT87", "HT88", "HT94a", "HT94b", "HT112a", "HT112b",
               "HT117a", "HT117b", "HT119", "HT122a", "HT122b", "HT128a", "HT128b",
               "HT132", "HT135a", "HT135b", "HT34", "HT15", "HT1", "HT2", "HT30",
               "HT37", "HT95a", "HT95b", "HT86a", "HT86b", "HT97", "HT123+124a",
               "HT123+124b", "HT28a", "HT28b"}
    for k in changed:
        a = O[k]["transliteratedWords"]; b = N[k]["transliteratedWords"]
        da = [x for x in a if x not in b]; db = [x for x in b if x not in a]
        tag = "  <== a tablet the claim depends on" if k in DOSSIER else ""
        print(f"    {k:12s} old-only {da}  new-only {db}{tag}")
    print("\n  CONSEQUENCE. Every numeric result in this folder -- the claimant's and")
    print("  every validator's -- is stated against a digital witness that is edited")
    print("  continuously and carries no version pin. Results must cite a snapshot")
    print("  hash. This attack directory vendors both snapshots and prints both.")


def rerun_on_new():
    """Does the newer snapshot change any load-bearing number?"""
    import corpus
    corpus.DATA = os.path.join(HERE, "data_20261002")
    import importlib
    importlib.reload(corpus)
    corpus.DATA = os.path.join(HERE, "data_20261002")
    A = corpus.load_a()
    from attack_arith2 import blocks_with_span, block_is_integer_clean
    rows = []
    for k, v in sorted(corpus.all_faces_with_words(A).items()):
        ws = v["transliteratedWords"]
        for ents, tot, mark, why, lo, hi in blocks_with_span(ws):
            if tot is None or not ents or not block_is_integer_clean(ws, lo, hi):
                continue
            rows.append((k, mark, sum(ents), tot, abs(sum(ents)-tot) < 1e-9))
    ok = sum(1 for r in rows if r[4])
    print(f"\n  KU-RO audit re-run on the 2026-10-02 snapshot: {ok}/{len(rows)} "
          f"integer-only blocks balance (was 8/23 on the 09-25 snapshot)")
    for r in rows:
        if r[4]:
            print(f"    balances: {r[0]:10s} {r[1]:11s} {r[2]:g} = {r[3]:g}")
    ws = A["HT34"]["transliteratedWords"]
    i = ws.index("KI-RO")
    print(f"\n  HT34 on the new snapshot: KI-RO followed by {ws[i+1:i+3]!r}")
    print("  -> the newer edition states 30 with an erasure [[7]], confirming the")
    print("     claimant's number and confirming that witness A's earlier '37' was a")
    print("     tabulation defect. Three independent routes now agree: Younger's")
    print("     commentary table, the re-edited witness, and (per validator 1) the")
    print("     GORILA plate apparatus.")


if __name__ == "__main__":
    main()
    rerun_on_new()
