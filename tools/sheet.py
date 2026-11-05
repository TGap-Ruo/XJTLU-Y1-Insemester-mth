# -*- coding: utf-8 -*-
"""生成答案核对图：每题 = 题号 + 题干 + A–E + 答案提示（转写为纯文本）"""
import json, os, sys
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"
seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))
mp = json.load(open(os.path.join(ROOT, "build", "answers_map.json")))
ans = json.load(open(os.path.join(ROOT, "build", "answers.json")))

S = 2.9
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"


def tr(s):
    for a, b in [("∞", "inf"), ("∪", "U"), ("−", "-"), ("√", "sqrt"), ("π", "pi"), ("≤", "<="), ("≥", ">=")]:
        s = s.replace(a, b)
    return s


def main(start, count, out_path):
    doc = pdfium.PdfDocument(SRC)
    unc = json.load(open(os.path.join(ROOT, "build", "unknown.json")))
    qs = unc[start:start + count]
    f = ImageFont.truetype(FONT, 15)
    rows = []
    cache = {}
    for q in qs:
        r = seg[q]
        if r["page"] not in cache:
            cache[r["page"]] = doc[r["page"] - 1].render(scale=S).to_pil()

        def cp(box):
            return cache[r["page"]].crop((int(box[0] * S), int(box[1] * S),
                                          int(min(box[2], 560) * S), int(box[3] * S)))

        pieces = []
        for L in "ABCDE":
            im = cp(r["options"][L])
            g = im.convert("L")
            import numpy as _np
            a = _np.asarray(g) < 200
            rows_i = _np.where(a.any(axis=1))[0]
            if len(rows_i):
                im = im.crop((0, max(0, rows_i.min() - 1), im.width, min(im.height, rows_i.max() + 2)))
            pieces.append(im)
        w = max(p.width for p in pieces)
        h = sum(p.height for p in pieces)
        opts = Image.new("RGB", (w, h), "white")
        yy = 0
        for p in pieces:
            opts.paste(p, (0, yy)); yy += p.height
        cap = "ANS: " + tr(ans.get(q, ""))[:120]
        rows.append((q, None, opts, cap))

    W = max(x[2].width for x in rows) + 70
    H = sum(x[2].height + 26 for x in rows) + 10 * len(rows)
    canvas = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(canvas)
    y = 0
    for q, stem, opts, cap in rows:
        d.text((4, y + 2), "Q" + q, fill=(200, 0, 0), font=f)
        canvas.paste(opts, (56, y))
        y += opts.height
        d.text((60, y + 2), cap, fill=(0, 90, 200), font=f)
        y += 24
        d.line([(0, y), (W, y)], fill=(220, 220, 220))
        y += 6
    canvas.save(out_path)
    print(out_path, canvas.size, "questions", [x[0] for x in rows])


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
