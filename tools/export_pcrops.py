# -*- coding: utf-8 -*-
"""Export the three crops that make up one Part-B entry.

    p{pid}_q.png   stem + the five options
    p{pid}_a.png   the paper's own "Answer: <value>" line
    p{pid}_s.png   the printed solution, ending with "The correct answer is:"

Everything is cut from the original attempt page, so no figure, symbol or
fraction can drift in transcription.
"""
import json
import os

import numpy as np
import pypdfium2 as pdfium
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Downloads/MTH026-Quiz"
ITEMS = os.path.join(ROOT, "build", "pitems.json")
OUT = os.path.join(ROOT, "qbank", "p")
S = 3.2
X0, X1 = 20.0, 578.0


def trim(im, pad=3, ink=165):
    g = np.asarray(im.convert("L"))
    mask = g < ink
    rc, cc = mask.sum(axis=1), mask.sum(axis=0)
    rows = np.where(rc >= 2)[0]
    cols = np.where(cc >= 2)[0]
    if len(rows) == 0 or len(cols) == 0:
        return None
    box = (max(0, cols.min() - pad), max(0, rows.min() - pad),
           min(im.width, cols.max() + 1 + pad), min(im.height, rows.max() + 1 + pad))
    out = im.crop(box)
    if out.width < 12 or out.height < 8:
        return None
    return out


def vstack(top, bot, gap=14):
    """Stack two crops, left aligned, on white."""
    if top is None:
        return bot
    if bot is None:
        return top
    w = max(top.width, bot.width)
    h = top.height + gap + bot.height
    out = Image.new("RGB", (w, h), "white")
    out.paste(top, (0, 0))
    out.paste(bot, (0, top.height + gap))
    return out


def main():
    items = json.load(open(ITEMS))
    os.makedirs(OUT, exist_ok=True)
    cache = {}
    n = 0
    for it in items:
        key = (it["file"], it["page"])
        if key not in cache:
            cache.clear()
            doc = pdfium.PdfDocument(os.path.join(SRC, it["file"]))
            cache[key] = doc[it["page"]].render(scale=S).to_pil()
            doc.close()
        page = cache[key]

        def cut(y0, y1, x0=X0):
            return trim(page.crop((int(x0 * S), int(y0 * S), int(X1 * S), int(y1 * S))))

        # stem and options are pasted as two blocks: that drops the "Select one:"
        # line and the radio buttons that sit left of the option letters
        # +1 not +3: the "Select one:" line sits ~7 pt lower, and clipping its
        # ascenders left a row of dots under the stem
        stem = cut(it["stem"][0] - 2, it["stem"][1] + 1, x0=22.0)
        opts = cut(it["opts"][0] - 4, it["opts"][1] + 3, x0=43.0)
        q = vstack(stem, opts)
        a = cut(it["ans_y"][0], it["ans_y"][1] + 1)
        s = cut(it["ans_y"][1] + 1, it["block_end"] + 3)
        pid = it["pid"]
        if q is not None:
            q.save(os.path.join(OUT, "p%03d_q.png" % pid))
        if a is not None:
            a.save(os.path.join(OUT, "p%03d_a.png" % pid))
        if s is not None:
            s.save(os.path.join(OUT, "p%03d_s.png" % pid))
        n += 1
    print("items", n, "->", OUT)
    for pid in (1, 2, 60, 200):
        for suf in "qas":
            f = os.path.join(OUT, "p%03d_%s.png" % (pid, suf))
            if os.path.exists(f):
                print(" ", os.path.basename(f), Image.open(f).size)


if __name__ == "__main__":
    main()
