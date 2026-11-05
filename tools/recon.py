# -*- coding: utf-8 -*-
"""把每道题的题干与选项按版面重建成 LaTeX，落盘 build/latex.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdfplumber
import layoutmath as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"


def tidy(s):
    s = s.replace("Findthe", "Find the ").replace("Evaluatetan", "Evaluate tan")
    for w in ("Find", "Evaluate", "Define", "Let", "The", "Which", "Consider",
              "Determine", "Compute", "Solve", "Given", "Suppose", "For"):
        s = s.replace(w + "the", w + " the ").replace(w + "a", w + " a ")
    return " ".join(s.split())


def main():
    seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))
    doc = pdfplumber.open(SRC)
    out = {}
    for q in sorted(seg, key=int):
        r = seg[q]
        pg = doc.pages[r["page"] - 1]
        b = r["stem"]
        c = pg.crop((b[0], b[1], b[2], b[3]))
        stem = " ".join(h["text"] for h in L.parse_page(c))
        opts = {}
        for L_, ob in r["options"].items():
            oc = pg.crop((ob[0], ob[1], ob[2], ob[3]))
            opts[L_] = " ".join(h["text"] for h in L.parse_page(oc))
        out[q] = {"stem": tidy(stem), "opts": {k: tidy(v) for k, v in opts.items()}}
    json.dump(out, open(os.path.join(ROOT, "build", "latex.json"), "w"),
              ensure_ascii=False, indent=0)
    print("重建题数", len(out))


if __name__ == "__main__":
    main()
