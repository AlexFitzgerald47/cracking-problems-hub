#!/usr/bin/env python3
"""Crop, upscale and sharpen a region of a bar photograph for reading.

    python3 src/crop.py <image> <out.png> <left,top,right,bottom> <scale> [rotate]

Requires pillow. This is the tool the 2026-09-25 re-transcription was done with;
every reading in data/instances_photographic.tsv came from a crop at scale 4-9.
"""
import sys
from PIL import Image, ImageOps, ImageFilter
src, out, box, scale = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
rot = int(sys.argv[5]) if len(sys.argv) > 5 else 0
l, t, r, b = [int(x) for x in box.split(",")]
im = Image.open(src).convert("L").crop((l, t, r, b))
if rot: im = im.rotate(rot, expand=True)
im = im.resize((int(im.width*scale), int(im.height*scale)), Image.LANCZOS)
im = ImageOps.autocontrast(im, cutoff=2)
im = im.filter(ImageFilter.UnsharpMask(radius=4, percent=180, threshold=2))
im.save(out); print(out, im.size)
