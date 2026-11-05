# -*- coding: utf-8 -*-
"""Recover the correct option letter by comparing rendered images.

The text layer cannot be trusted for fractions (Moodle's MathJax puts the
numerator on a different baseline), but the printed "Answer: <value>" and the
correct option are *the same LaTeX*, so their pixels match.  Every option crop
is scored against the answer crop; the winner is the key.

Ground truth for the score check: the items where the option text already
matched the answer text exactly, plus items that carry a green tick.
"""
import json
import os
import re
import sys
import unicodedata

import numpy as np
import pypdfium2 as pdfium
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Downloads/MTH026-Quiz"
BLOCKS = os.path.join(ROOT, "build", "quiz_blocks.json")
S = 2.0
W, H = 180, 56


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\u2212", "-")
    s = re.sub(r"^[A-E]\.", "", s.strip())
    return re.sub(r"\s+", "", s).lower().rstrip(".")


def render(file, page, cache={}):
    key = (file, page)
    if key not in cache:
        if len(cache) > 40:
            cache.clear()
        doc = pdfium.PdfDocument(os.path.join(SRC, file))
        cache[key] = doc[page].render(scale=S).to_pil().convert("L")
        doc.close()
    return cache[key]


def strip(img, y0, y1, x0=26.0, x1=568.0):
    """Binarised, ink-trimmed, scale-normalised patch of one line."""
    im = img.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    a = np.asarray(im)
    m = a < 205
    ys, xs = np.where(m)
    if len(ys) < 4:
        return None
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    return np.asarray(im.resize((W, H)))


def score(a, b):
    if a is None or b is None:
        return 0.0
    a = (a < 205).astype(np.float32)
    b = (b < 205).astype(np.float32)
    num = float((a * b).sum())
    den = float(np.sqrt((a * a).sum() * (b * b).sum()))
    return num / den if den else 0.0


def decide(block):
    img = render(block["file"], block["page"])
    ya = block["ans_y"]
    ans = strip(img, ya[0], ya[1], x0=76.0)      # skip the "Answer:" label
    if ans is None:
        return None, {}
    sc = {}
    for L in "ABCDE":
        band = block["opt_y"].get(L)
        if not band:
            continue
        sc[L] = round(score(ans, strip(img, band[0], band[1], x0=68.0)), 3)
    if not sc:
        return None, {}
    best = max(sc, key=sc.get)
    return best, sc


def main():
    blocks = json.load(open(BLOCKS))
    # ground truth from exact text equality and the green tick
    gt = {}
    for i, b in enumerate(blocks):
        na = norm(b["ans_layout"].replace("Answer:", ""))
        for L in "ABCDE":
            if na and norm(b["opt_layout"].get(L, "")) == na:
                gt[i] = L
                break
        else:
            g = [L for L in "ABCDE" if b.get("green", {}).get(L)]
            if len(g) == 1:
                gt[i] = g[0]

    agree = 0
    disagree = []
    for i, L in list(gt.items()):
        best, sc = decide(blocks[i])
        if best == L:
            agree += 1
        else:
            disagree.append((i, L, best, sc))
    print("ground truth %d, image agrees %d (%.0f%%)" % (len(gt), agree, 100.0 * agree / max(1, len(gt))))
    for d in disagree[:8]:
        print("  block", d[0], "text says", d[1], "image says", d[2], d[3])


if __name__ == "__main__":
    main()
