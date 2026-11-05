# -*- coding: utf-8 -*-
"""像素比对定答案：答案文本与正确选项在原 PDF 中是同一套渲染，用墨迹掩膜相关度判定"""
import json, os, re, sys
import numpy as np
import pdfplumber
from PIL import Image
import pypdfium2 as pdfium

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layoutmath import parse_page

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"
seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))
SCALE = 3.0


def ink(img):
    a = np.asarray(img.convert("L"))
    m = a < 200
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def norm_h(mask, h=40):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    w = max(1, int(round(im.width * h / im.height)))
    return np.asarray(im.resize((w, h), Image.LANCZOS)) > 127


def score(a, b):
    """两墨迹掩膜的最佳重合度（等高、水平滑动）"""
    H = 40
    A = norm_h(a, H)
    B = norm_h(b, H)
    best = 0.0
    for dx in range(-6, 7):
        if dx >= 0:
            w = min(A.shape[1], B.shape[1] - dx)
            if w <= 4:
                continue
            a1, b1 = A[:, :w], B[:, dx:dx + w]
        else:
            w = min(A.shape[1] + dx, B.shape[1])
            if w <= 4:
                continue
            a1, b1 = A[:, -dx:-dx + w], B[:, :w]
        inter = np.logical_and(a1, b1).sum()
        union = np.logical_or(a1, b1).sum()
        if union:
            best = max(best, inter / union)
    return best


def answer_boxes(pdf):
    """答案区块内每条答案的包围盒"""
    out = {}
    for pi, page in enumerate(pdf.pages):
        rows = parse_page(page)
        in_ans = False
        cur = None
        for r in rows:
            t = r["text"].strip()
            if "参考答案" in t:
                in_ans = True
                continue
            if re.match(r"^\d\.\d[a-c]?\s", t):
                in_ans = False
                continue
            if not in_ans:
                continue
            m = re.match(r"^(\d{1,3})\.\s*(.+)$", t)
            if m and 1 <= int(m.group(1)) <= 351:
                cur = int(m.group(1))
                out[cur] = [pi, r["x0"], r["top"], r["x1"], r["bot"]]
            elif cur and out.get(cur) and not t[0].isdigit():
                b = out[cur]
                b[3] = max(b[3], r["x1"])
                b[4] = max(b[4], r["bot"])
    return out


def main():
    with pdfplumber.open(SRC) as pdf:
        ab = answer_boxes(pdf)
        print("答案盒:", len(ab))
        doc = pdfium.PdfDocument(SRC)
        cache = {}

        def page_img(pi):
            if pi not in cache:
                cache[pi] = doc[pi].render(scale=SCALE).to_pil()
            return cache[pi]

        res = {}
        for q, rec in seg.items():
            if int(q) not in ab:
                continue
            pi, ax0, ay0, ax1, ay1 = ab[int(q)]
            A = ink(page_img(pi).crop((int(ax0 * SCALE), int(ay0 * SCALE),
                                       int((ax1 + 3) * SCALE), int((ay1 + 3) * SCALE))))
            if A is None:
                continue
            sc = {}
            for L, b in rec["options"].items():
                img = page_img(rec["page"] - 1)
                B = ink(img.crop((int((b[0] + 14) * SCALE), int(b[1] * SCALE),
                                  int(b[2] * SCALE), int(b[3] * SCALE))))
                if B is None:
                    sc[L] = 0.0
                    continue
                sc[L] = round(score(A, B), 4)
            order = sorted(sc.items(), key=lambda kv: -kv[1])
            res[q] = {"ans": order[0][0], "px": order[0][1], "px2": order[1][1], "all": sc}

        json.dump(res, open(os.path.join(ROOT, "build", "answers_px.json"), "w"), indent=0)
        agree = sum(1 for q in res if q in json.load(open(os.path.join(ROOT, "build", "answers_map.json")))
                    and res[q]["ans"] == json.load(open(os.path.join(ROOT, "build", "answers_map.json")))[q]["ans"])
        print("像素判定:", len(res), "与文本判定一致:", agree)
        for q in ["1", "6", "10", "17", "21", "24", "25"]:
            if q in res:
                print(" Q%s -> %s (%.2f vs %.2f) %s" % (q, res[q]["ans"], res[q]["px"], res[q]["px2"], res[q]["all"]))


if __name__ == "__main__":
    main()
