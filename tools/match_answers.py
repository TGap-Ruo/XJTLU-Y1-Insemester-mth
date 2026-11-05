# -*- coding: utf-8 -*-
"""元素级 y 带归属：把每个选项的内容盒子归到它自己的 y 带，重建 LaTeX 后与答案比对"""
import json, os, re, difflib, sys
import pdfplumber
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layoutmath import page_boxes, emit, parse_page

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/zhj/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/wxid_pu04hadszvwv32_5ef1/temp/drag/MTH026题库分类汇总.pdf"
seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))
ans_md = json.load(open(os.path.join(ROOT, "build", "answers.json")))

GLYPH = {"infty": "∞", "cup": "∪", "cap": "∩", "pi": "π", "sqrt": "√", "cdot": "·",
         "times": "×", "le": "≤", "ge": "≥", "ne": "≠", "to": "→", "pm": "±",
         "theta": "θ", "alpha": "α", "beta": "β", "varnothing": "∅"}


def flat(s):
    s = s.replace("−", "-").replace("–", "-")
    for _ in range(4):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1\2", s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"√\1", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"_\{([^{}]*)\}", r"\1", s)
    for k, v in sorted(GLYPH.items(), key=lambda kv: -len(kv[0])):
        s = re.sub(r"\\%s(?![A-Za-z])" % k, v, s)
    s = re.sub(r"\\left|\\right|\\,|\\;|\\!|\\ ", "", s)
    s = s.replace("\\", "").replace("{", "").replace("}", "")
    s = re.sub(r"\s+", "", s)
    s = s.replace("（", "(").replace("）", ")")
    s = re.sub(r"^[A-E]\.", "", s)
    if re.search(r"Noneoftheother", s, re.I):
        return "NONE"
    return s


def opt_texts(boxes, base, rec):
    """把每个盒子唯一地归到最近的选项带，再逐带重建 LaTeX"""
    opts = rec["options"]
    bands = []
    for L, b in opts.items():
        nxt = [o[1] for o in opts.values() if o[1] > b[1] + 3]
        y1 = min(nxt) + 1.0 if nxt else max(b[3], b[1] + 12)
        bands.append((L, b[1] + 1.0, y1))
    assign = {L: [] for L in opts}
    for x in boxes:
        if not (x.txt.strip() or x.kind in ("frac", "sqrt")):
            continue
        if x.x0 < 58:
            continue
        L = min(bands, key=lambda t: abs(x.cy - (t[1] + t[2]) / 2))[0]
        assign[L].append(x)
    out = {}
    for L, els in assign.items():
        els.sort(key=lambda x: (round(x.cy / 6), x.x0))
        out[L] = emit(els, base)
    return out


def parse_answers(pdf):
    out, in_ans = {}, False
    for page in pdf.pages:
        for r in parse_page(page):
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
                out[int(m.group(1))] = m.group(2).strip()
            elif out and t and not t[0].isdigit():
                k = max(out)
                out[k] = (out[k] + " " + t).strip()
    return out


def main():
    res, low, opt_all = {}, [], {}
    with pdfplumber.open(SRC) as pdf:
        ans_pdf = parse_answers(pdf)
        print("PDF 答案:", len(ans_pdf))
        cache = {}
        for q, rec in seg.items():
            pno = rec["page"]
            if pno not in cache:
                cache[pno] = page_boxes(pdf.pages[pno - 1])
            boxes, base = cache[pno]
            opt_all[q] = opt_texts(boxes, base, rec)

    for q, rec in seg.items():
        a = flat(ans_pdf.get(q) or ans_md.get(q, ""))
        sc = []
        for L in "ABCDE":
            o = flat(opt_all[q].get(L, ""))
            s = 1.0 if (a and a == o) else difflib.SequenceMatcher(None, a, o).ratio()
            sc.append((s, L))
        sc.sort(reverse=True)
        (s1, L1), (s2, L2) = sc[0], sc[1]
        res[q] = {"ans": L1, "score": round(s1, 3), "gap": round(s1 - s2, 3)}
        if s1 < 0.97 or (s1 - s2) < 0.08:
            low.append((q, a[:30], L1, s1, L2, s2,
                        {L: flat(opt_all[q].get(L, ""))[:22] for L in "ABCDE"}))

    print("高置信:", 351 - len(low), "/ 351")
    for x in low[:10]:
        print(" Q%s %r -> %s(%.2f) vs %s(%.2f)" % (x[0], x[1], x[2], x[3], x[4], x[5]))
        print("    ", x[6])
    json.dump(res, open(os.path.join(ROOT, "build", "answers_map.json"), "w"), indent=0)
    json.dump(opt_all, open(os.path.join(ROOT, "build", "option_text.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=0)


if __name__ == "__main__":
    main()
