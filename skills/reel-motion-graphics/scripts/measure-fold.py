#!/usr/bin/env python3
"""Verify the fold rule on a rendered snapshot: lowest bright text above the fold vs the
first dark hair row below it. Usage: measure-fold.py <snapshot.png> <fold>"""
import sys
from PIL import Image

im = Image.open(sys.argv[1]).convert('L')
fold = int(sys.argv[2])
h = im.size[1]
cb = max(y for y in range(600, fold) if sum(1 for x in range(172, 830, 2) if im.getpixel((x, y)) > 150) > 2)
ht = next(y for y in range(fold + 5, h) if sum(1 for x in range(360, 720, 2) if im.getpixel((x, y)) < 90) > 8)
a, b = fold - cb, ht - fold
print(f"content bottom {cb} · gap above {a}px | head top {ht} · gap below {b}px · {'OK' if abs(a - b) <= 4 else 'ADJUST --fold'}")
