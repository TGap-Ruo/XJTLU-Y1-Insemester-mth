# -*- coding: utf-8 -*-
"""导出裁图：整题图（PDF 用）+ 题干/选项图（刷题器用）"""
import json, os, sys
import numpy as np
import pypdfium2 as pdfium
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"
seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))

QDIR = os.path.join(ROOT, "qbank", "q")
SDIR = os.path.join(ROOT, "qbank", "s")
ODIR = os.path.join(ROOT, "qbank", "o")


def trim(im, pad=3, thr=226):
    a = np.asarray(im.convert("L")) < thr
    # drop rows/cols with only a few dark pixels (faint separators, dust)
    rc, cc = a.sum(axis=1), a.sum(axis=0)
    rows = np.where(rc >= 3)[0]
    cols = np.where(cc >= 3)[0]
    a = a[rows.min():rows.max() + 1, cols.min():cols.max() + 1]
    ys, xs = np.where(a)
    if len(ys) == 0:
        return im
    y0, y1 = max(0, ys.min() - pad), min(im.height, ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(im.width, xs.max() + pad + 1)
    return im.crop((x0, y0, x1, y1))


def trim_ink(im, pad=4, ink=150):
    """Crop to the last row that carries real ink.

    The source page ends each block with a pale green answer banner and a
    hairline rule.  Those are light (L > 200), so a plain dark-threshold trim
    keeps them and the crop shows a stray coloured strip under the options.
    Here only genuinely dark pixels (the printed text) count as content.
    """
    g = np.asarray(im.convert("L"))
    mask = g < ink
    rc, cc = mask.sum(axis=1), mask.sum(axis=0)
    rows = np.where(rc >= 2)[0]
    cols = np.where(cc >= 2)[0]
    if len(rows) == 0 or len(cols) == 0:
        return im
    y0, y1 = max(0, rows.min() - pad), min(im.height, rows.max() + 1 + pad)
    x0, x1 = max(0, cols.min() - pad), min(im.width, cols.max() + 1 + pad)
    return im.crop((x0, y0, x1, y1))



def main():
    for d in (QDIR, SDIR, ODIR):
        os.makedirs(d, exist_ok=True)
    doc = pdfium.PdfDocument(SRC)
    S = 2.6
    cache = {}
    n = 0
    for q in sorted(seg, key=int):
        r = seg[q]
        pno = r["page"]
        if pno not in cache:
            cache.clear()
            cache[pno] = doc[pno - 1].render(scale=S).to_pil()
        page = cache[pno]
        stem = r["stem"]
        top = min(b[1] for b in r["options"].values())
        bot = max(b[3] for b in r["options"].values())
        whole = trim_ink(page.crop((int(stem[0] * S), int((stem[1] - 1) * S),
                                    int(559 * S), int((bot + 1) * S))))
        whole.save(os.path.join(QDIR, "q%03d.png" % int(q)))
        st = trim_ink(page.crop((int(stem[0] * S), int((stem[1] - 1) * S),
                                 int(559 * S), int((top - 1) * S))))
        st.save(os.path.join(SDIR, "q%03d.png" % int(q)))
        for L, b in r["options"].items():
            im = trim(page.crop((int((b[0] + 12) * S), int(b[1] * S), int(559 * S), int(b[3] * S))))
            im.save(os.path.join(ODIR, "q%03d_%s.png" % (int(q), L)))
        n += 1
    print("导出题数", n)


if __name__ == "__main__":
    main()
