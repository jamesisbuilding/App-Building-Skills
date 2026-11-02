#!/usr/bin/env python3
"""Solve the fold so it sits equidistant between the lowest animation content and the
presenter's head top. Assumes the presenter fills 1080 wide below the fold with
object-fit: cover; object-position: center 20%.
Usage: solve-fold.py <presenter.jpg|frame.png> [content_bottom=900] [--head-y N]
The head top is detected as the first row with a dark (hair) run in the centre third;
pass --head-y (in source-image px) when the footage has a light head or a dark backdrop."""
import sys
from PIL import Image

args = [a for a in sys.argv[1:] if not a.startswith('--')]
img = Image.open(args[0]).convert('L')
cb = float(args[1]) if len(args) > 1 else 900.0
iw, ih = img.size
if '--head-y' in sys.argv:
    hy = float(sys.argv[sys.argv.index('--head-y') + 1])
else:
    hy = next(y for y in range(ih) if sum(1 for x in range(iw // 3, 2 * iw // 3, 2) if img.getpixel((x, y)) < 90) > 8)

s = 1080 / iw  # width-limited cover scale (portrait footage)
def head_top(fold):
    return fold + hy * s + 0.2 * ((1920 - fold) - ih * s)

best = min(range(960, 1201, 4), key=lambda f: abs((f - cb) - (head_top(f) - f)))
print(f"head y in source {hy:.0f}px · scale {s:.4f}")
print(f"fold {best}px → gap above {best - cb:.0f}px · gap below {head_top(best) - best:.0f}px")
