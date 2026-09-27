#!/usr/bin/env python3
"""Glyph-identity evidence for RESULTS.md (post-freeze; the scan decides identity, FREEZE section 4).

1. Instrument validation: does max-NCC over small scale changes cluster the poem's ten TCURL
   tokens with each other? (If it cannot, it has no power on any identity question.)
2. The signature's third glyph (Sektu's NU = <N U>) against every stacked-stroke glyph type in the
   poem: exact rank-sum test for TCURL. Run twice and both reported: the first crop included the
   background blot above the glyph; the second is restricted to the strokes (y 630-656).
3. Specificity: the signature's other glyphs as probes should NOT pull TCURL up.
4. The mark above each of the 25 dotted-X tokens: size and elongation (dot vs tick).
5. Comparison sheets (PNG) for the evidence folder.

    python3 glyph_identity.py <cyphersolver targets/debosnys dir> <output dir>
"""
import sys
from itertools import combinations

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps

D = sys.argv[1] if len(sys.argv) > 1 else "."
OUT = sys.argv[2] if len(sys.argv) > 2 else "."
PG = {k: np.array(Image.open(f"{D}/c{k}.png").convert("L")).astype(np.float32) for k in ["2a", "2b", "4a", "4b"]}

# Origins (page, x, y) of cyphersolver's 4x half-line crops of the poem, found by NCC >= 0.999.
HALF = {}
for i, y in enumerate([365, 438, 510, 585, 660, 735, 810, 885, 960, 1038, 1112, 1190, 1260, 1338, 1410], 1):
    HALF[(i, "a")] = ("4a", 295, y)
    HALF[(i, "b")] = ("4a", 607, y)
for i, y in zip(range(16, 21), [15, 85, 160, 235, 310]):
    HALF[(i, "a")] = ("4b", 340, y)
    HALF[(i, "b")] = ("4b", 600, y)

SIG = {  # the fitting line on c2b (page coordinates)
    "NU_with_blot": (662, 622, 692, 670), "NU": (662, 630, 693, 656), "O2RNO": (721, 628, 750, 660),
    "CROSSB": (752, 628, 773, 660), "C2B2": (608, 628, 633, 664),
}
# Poem glyphs: (line, half, x0, x1) in 4x-crop pixels, read off the viewed crops.
CANDS = {
    ("L1 end", "TCURL"): (1, "b", 230, 380), ("L2 end", "TCURL"): (2, "b", 230, 380),
    ("L5", "TCURL"): (5, "a", 1215, 1380), ("L6", "TCURL"): (6, "a", 515, 650),
    ("L8", "TCURL"): (8, "b", 170, 310), ("L9", "TCURL"): (9, "a", 930, 1070),
    ("L13", "TCURL"): (13, "a", 1150, 1300), ("L14", "TCURL"): (14, "b", 340, 490),
    ("L17 end", "TCURL"): (17, "b", 1050, 1200), ("L18 end", "TCURL"): (18, "b", 810, 960),
    ("L3 t1", "DBLWAVE"): (3, "a", 120, 290), ("L12 t7", "DBLWAVE"): (12, "a", 900, 1060),
    ("L10 t1", "DBLWAVE_XX"): (10, "a", 130, 300), ("L18 t1", "LOOP"): (18, "a", 110, 260),
    ("L1 t5", "N_O"): (1, "a", 520, 650), ("L9 t13", "N_O"): (9, "b", 530, 650),
    ("L4 t6", "N_OO"): (4, "a", 690, 810), ("L6 t8", "N_OO"): (6, "a", 1080, 1210),
    ("L4 t12", "N_X"): (4, "b", 180, 300), ("L10 t12", "N_X"): (10, "b", 440, 550),
    ("L13 t11", "N_X"): (13, "b", 270, 400), ("L16 t8", "N_DASH_X"): (16, "a", 1030, 1200),
    ("L15 t8", "N_SLO"): (15, "a", 990, 1150), ("L20 t6", "MTAIL"): (20, "a", 680, 820),
    ("L5 t1", "OMEGA"): (5, "a", 100, 230),
}
XD = [(2, "a", 10, 985, 1065), (3, "a", 4, 595, 665), (3, "a", 5, 685, 755), (3, "b", 12, 345, 435),
      (4, "a", 5, 605, 675), (4, "b", 13, 325, 415), (5, "a", 4, 455, 545), (6, "a", 7, 935, 1015),
      (7, "a", 6, 835, 905), (7, "a", 7, 925, 990), (8, "a", 6, 785, 865), (9, "a", 5, 675, 755),
      (11, "a", 6, 770, 850), (11, "a", 11, 1260, 1335), (11, "b", 16, 645, 725), (11, "b", 17, 735, 815),
      (13, "b", 17, 1065, 1145), (14, "b", 12, 520, 625), (15, "a", 4, 510, 580), (15, "a", 5, 590, 665),
      (16, "a", 3, 390, 475), (17, "a", 6, 875, 955), (19, "a", 4, 495, 580), (20, "a", 2, 275, 345),
      (20, "a", 3, 335, 400)]


def box(line, half, x0, x1, y0=60, y1=230):
    p, ox, oy = HALF[(line, half)]
    return p, (ox + x0 // 4, oy + y0 // 4, ox + x1 // 4, oy + y1 // 4)


def tight(p, b, thr=140, pad=2):
    a = PG[p][b[1]:b[3], b[0]:b[2]]
    ys, xs = np.where(a < thr)
    return a[max(0, ys.min() - pad):ys.max() + pad + 1, max(0, xs.min() - pad):xs.max() + pad + 1]


def norm(a, S=40):
    h, w = a.shape
    s = S / max(h, w)
    a = cv2.resize(a, (max(1, round(w * s)), max(1, round(h * s))), interpolation=cv2.INTER_AREA)
    out = np.full((S + 8, S + 8), 255, np.float32)
    oy, ox = (S + 8 - a.shape[0]) // 2, (S + 8 - a.shape[1]) // 2
    out[oy:oy + a.shape[0], ox:ox + a.shape[1]] = a
    return 255 - out


def score(t, c):
    best = -1.0
    for s in (0.85, 0.92, 1.0, 1.08, 1.15):
        tt = cv2.resize(t, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        big = cv2.copyMakeBorder(c, 12, 12, 12, 12, cv2.BORDER_CONSTANT, value=0)
        if tt.shape[0] <= big.shape[0] and tt.shape[1] <= big.shape[1]:
            best = max(best, float(cv2.matchTemplate(big, tt, cv2.TM_CCOEFF_NORMED).max()))
    return best


def rank_sum_p(labels):
    """Exact P(sum of TCURL ranks <= observed) over all placements of the TCURL labels."""
    n, k = len(labels), sum(labels)
    obs = sum(i for i, x in enumerate(labels) if x)
    tot = cnt = 0
    for comb in combinations(range(n), k):
        tot += 1
        cnt += sum(comb) <= obs
    return cnt / tot


def main():
    G = {k: norm(tight(*box(*v))) for k, v in CANDS.items()}
    keys = list(G)
    tc = [k for k in keys if k[1] == "TCURL"]
    print("1. instrument validation (each TCURL as probe; mean rank of the other nine among 24):")
    ranks = []
    for probe in tc:
        sc = sorted(((score(G[probe], G[k]), k) for k in keys if k != probe), reverse=True)
        r = np.mean([i for i, (_s, k) in enumerate(sc) if k[1] == "TCURL"])
        ranks.append(r)
    print(f"   mean {np.mean(ranks):.2f} (chance 11.5, best possible 4.0); per probe {[round(x, 1) for x in ranks]}")
    for crop in ("NU_with_blot", "NU"):
        sig = norm(tight("2b", SIG[crop]))
        rows = sorted(((score(sig, G[k]), k) for k in keys), reverse=True)
        lab = [k[1] == "TCURL" for _s, k in rows]
        r = [i for i, x in enumerate(lab) if x]
        print(f"2. signature {crop}: TCURL mean rank {np.mean(r):.1f} of 24 (chance 12.0); "
              f"exact rank-sum p = {rank_sum_p(lab):.2e}; top5 = {[k[0] + '/' + k[1] for _s, k in rows[:5]]}")
    for probe in ("O2RNO", "CROSSB", "C2B2"):
        t = norm(tight("2b", SIG[probe]))
        rows = sorted(((score(t, G[k]), k) for k in keys), reverse=True)
        r = [i for i, (_s, k) in enumerate(rows) if k[1] == "TCURL"]
        print(f"3. specificity: probe {probe:6s} -> TCURL mean rank {np.mean(r):.1f}")
    print("4. dotted-X marks: line token height width ink_px gap elongation")
    for (l, h, t, x0, x1) in XD:
        p, ox, oy = HALF[(l, h)]
        a = PG[p][oy + 10:oy + 60, ox + x0 // 4:ox + x1 // 4]
        ink = a < 120
        rows_ = ink.sum(1)
        runs, s = [], None
        for y in range(len(rows_)):
            if rows_[y] > 0 and s is None:
                s = y
            if rows_[y] == 0 and s is not None:
                runs.append((s, y - 1))
                s = None
        if s is not None:
            runs.append((s, len(rows_) - 1))
        body = max(runs, key=lambda r_: r_[1] - r_[0])
        marks = [r_ for r_ in runs if r_[1] < body[0]]
        m = max(marks, key=lambda r_: int(ink[r_[0]:r_[1] + 1].sum()))  # the mark, not a stray pixel
        sub = ink[m[0]:m[1] + 1]
        yy, xx = np.where(sub)
        ev = np.sort(np.linalg.eigvalsh(np.cov(np.vstack([xx, yy])))) if sub.sum() > 2 else np.array([1, 1])
        print(f"   L{l:2d} t{t:2d} {m[1]-m[0]+1:2d} {xx.max()-xx.min()+1:2d} {int(sub.sum()):3d} "
              f"{body[0]-m[1]-1:2d} {np.sqrt(ev[1]/max(ev[0],1e-3)):.2f}")
    sheet(G)


def sheet(G):
    tiles = []
    items = [("SIG NU (#2b)", ("2b", SIG["NU"]))] + [(k[0] + " " + k[1], box(*v)) for k, v in CANDS.items()
                                                     if k[1] == "TCURL"]
    for lab, (p, b) in items:
        c = Image.fromarray(tight(p, b).astype(np.uint8))
        c = ImageOps.autocontrast(c, cutoff=1).resize((c.width * 6, c.height * 6), Image.LANCZOS)
        t = Image.new("L", (240, 230), 255)
        t.paste(c, ((240 - c.width) // 2, 30))
        ImageDraw.Draw(t).text((5, 5), lab, fill=0)
        tiles.append(t)
    cols = 6
    out = Image.new("L", (cols * 240, ((len(tiles) + cols - 1) // cols) * 230), 255)
    for i, t in enumerate(tiles):
        out.paste(t, ((i % cols) * 240, (i // cols) * 230))
    out.save(f"{OUT}/signature_NU_vs_poem_TCURL.png")


if __name__ == "__main__":
    main()
