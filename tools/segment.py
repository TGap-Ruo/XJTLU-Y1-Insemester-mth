# -*- coding: utf-8 -*-
"""纯几何切分：题号 / 选项字母坐标 → 每题、每选项的裁切框"""
import json, os, re
import pdfplumber

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"
OUT = os.path.join(ROOT, "build", "segments.json")

NUM_X = (35, 47)      # 题号列（正文，恒 x=40）
OPT_X = (60, 72)      # 选项字母列（恒 x=65）
CUT_X = (46, 60)      # 章节标题列（x≈52）
RIGHT = 560
PAD = 2.0
YCLUST = 6.0


def page_marks(page):
    marks = []
    for w in page.extract_words():
        t = w["text"].strip()
        y, x = w["top"], w["x0"]
        if re.fullmatch(r"\d{1,3}\.", t) and NUM_X[0] <= x <= NUM_X[1]:
            marks.append({"kind": "q", "num": int(t[:-1]), "x": x, "y": y})
        elif re.fullmatch(r"[A-E]\.", t) and OPT_X[0] <= x <= OPT_X[1]:
            marks.append({"kind": "o", "letter": t[0], "x": x, "y": y})
        elif re.fullmatch(r"\d\.\d[a-c]?", t) and CUT_X[0] <= x <= CUT_X[1]:
            marks.append({"kind": "cut", "x": x, "y": y})
        elif "参考答案" in t:
            marks.append({"kind": "cut", "x": x, "y": y})
    # 去重（同一 y 上重复的 cut）
    seen, uniq = set(), []
    for m in marks:
        k = (m["kind"], m["x"], round(m["y"], 1))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(m)
    return uniq


def main():
    per_page, cuts = [], []
    with pdfplumber.open(SRC) as pdf:
        for pno, page in enumerate(pdf.pages):
            ms = page_marks(page)
            ms.sort(key=lambda m: (m["y"], m["x"]))
            per_page.append((pno + 1, page.height, ms))

    recs = []
    for pno, H, ms in per_page:
        # 行聚类
        rows, cur = [], []
        for m in ms:
            if not cur or abs(m["y"] - cur[-1]["y"]) <= YCLUST:
                cur.append(m)
            else:
                rows.append(cur)
                cur = [m]
        if cur:
            rows.append(cur)
        for ri, row in enumerate(rows):
            row.sort(key=lambda m: m["x"])
            y0 = min(m["y"] for m in row) - PAD
            y1 = (min(m["y"] for m in rows[ri + 1]) - PAD) if ri + 1 < len(rows) else (H - 42)
            for mi, m in enumerate(row):
                x0 = m["x"] - 1
                x1 = RIGHT
                if mi + 1 < len(row):
                    x1 = row[mi + 1]["x"] - 4
                if y1 - y0 < 6:
                    y1 = y0 + 8
                box = [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)]
                if m["kind"] == "q":
                    recs.append({"q": m["num"], "page": pno, "stem": box})
                elif m["kind"] == "o":
                    recs.append({"q": None, "page": pno, "opt": m["letter"], "box": box})
                else:
                    recs.append({"q": None, "page": pno, "cut": True})

    out, cur = {}, None
    for r in recs:
        if r.get("q"):
            cur = r["q"]
            out.setdefault(cur, {"num": cur, "page": r["page"], "stem": r["stem"], "options": {}})
        elif r.get("opt") and cur:
            out[cur]["options"][r["opt"]] = r["box"]
        elif r.get("cut"):
            cur = None   # 遇到章节标题/答案块，之后的选项不再归属上一题

    nums = sorted(out)
    print("切出题数:", len(nums), "范围", nums[0], "-", nums[-1])
    print("缺号:", sorted(set(range(1, max(nums) + 1)) - set(nums)))
    bad = [(k, sorted(v["options"])) for k, v in out.items() if sorted(v["options"]) != list("ABCDE")]
    print("选项不全:", len(bad), bad[:6])
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("→", OUT)


if __name__ == "__main__":
    main()
