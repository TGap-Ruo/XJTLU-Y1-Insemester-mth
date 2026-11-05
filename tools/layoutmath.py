# -*- coding: utf-8 -*-
"""PDF 版面 → LaTeX（盒子模型 + 锚点区域）
1) 字符 → 盒子；√ + 上划线、横线 + 上下组 → 根号 / 分数盒子（递归）
2) 以正文字符基线聚“子行”，高盒子（分数/根号）按竖直中心归入最近子行
3) 子行按 top 排序，子行内按 x 排序；以「12.」「A.」为锚点切出区域
"""
import re

SPECIAL = {
    "−": "-", "–": "-", "∞": r"\infty", "∪": r"\cup", "∩": r"\cap",
    "π": r"\pi", "θ": r"\theta", "α": r"\alpha", "β": r"\beta",
    "≤": r"\le", "≥": r"\ge", "≠": r"\ne", "→": r"\to", "·": r"\cdot",
    "×": r"\times", "∈": r"\in", "∅": r"\varnothing", "√": r"\sqrt",
    "\u00a0": " ",
}
ANCHOR_Q = re.compile(r"^(\d{1,3})\.$")
ANCHOR_O = re.compile(r"^([A-E])\.$")


class B:
    __slots__ = ("x0", "x1", "top", "bot", "txt", "size", "kind", "num", "den")

    def __init__(self, x0, x1, top, bot, txt="", size=10.0, kind="c"):
        self.x0, self.x1, self.top, self.bot = x0, x1, top, bot
        self.txt, self.size, self.kind = txt, size, kind
        self.num = self.den = None

    @property
    def cx(self):
        return (self.x0 + self.x1) / 2

    @property
    def cy(self):
        return (self.top + self.bot) / 2

    @property
    def h(self):
        return self.bot - self.top


def _boxes(page):
    out = []
    for c in page.chars:
        t = c["text"]
        out.append(B(c["x0"], c["x1"], c["top"], c["bottom"], t if t.strip() else " ", c["size"]))
    return out


def _lines_rects(page):
    rs = []
    for r in page.rects + page.lines:
        h, w = r["bottom"] - r["top"], r["x1"] - r["x0"]
        if 0 < h <= 2.2 and w >= 3:
            rs.append((r["x0"], r["x1"], r["top"], r["bottom"]))
    return rs


def merge_sqrt(boxes, rects):
    changed = True
    while changed:
        changed = False
        for e in list(boxes):
            if not (e.kind == "c" and e.txt.strip() == "√"):
                continue
            cand = [r for r in rects
                    if r[2] <= e.top + 3.0 and r[2] >= e.top - 6.0
                    and r[0] >= e.x1 - 2.0 and r[0] - e.x1 <= 12]
            if not cand:
                continue
            r = min(cand, key=lambda r: r[0])
            rad = [b for b in boxes if b is not e
                   and b.cx >= r[0] - 1.0 and b.cx <= r[1] + 1.0
                   and b.top >= r[3] - 2.5 and b.bot <= r[3] + 22]
            if not rad:
                continue
            for b in rad:
                boxes.remove(b)
            boxes.remove(e)
            rects.remove(r)
            s = B(e.x0, max(r[1], max(b.x1 for b in rad)), min([e.top] + [b.top for b in rad]),
                  max(b.bot for b in rad), "", e.size, "sqrt")
            s.num = rad
            boxes.append(s)
            changed = True
    return boxes


def merge_frac(boxes, rects):
    for (x0, x1, top, bot) in sorted(rects, key=lambda r: r[1] - r[0]):
        w = x1 - x0
        if w < 2.5 or w > 260:    # 极窄是杂点，极宽是装饰性分隔线
            continue
        num = [b for b in boxes if x0 - 2.5 <= b.cx <= x1 + 2.5
               and b.bot <= top + 1.3 and b.bot >= top - 17]
        den = [b for b in boxes if x0 - 2.5 <= b.cx <= x1 + 2.5
               and b.top >= bot - 1.3 and b.top <= bot + 17]
        if not num or not den:
            continue
        for b in num + den:
            if b in boxes:
                boxes.remove(b)
        f = B(x0, x1, min(b.top for b in num), max(b.bot for b in den), "", 10.0, "frac")
        f.num, f.den = num, den
        boxes.append(f)
    return boxes


def emit(seq, base):
    seq = sorted(seq, key=lambda b: b.x0)
    out, i, prev = [], 0, None
    while i < len(seq):
        b = seq[i]
        sup, sub, j = [], [], i + 1
        while j < len(seq):
            n = seq[j]
            last = sup[-1] if sup else (sub[-1] if sub else b)
            if n.size < base * 0.92 and (n.x0 - last.x1) <= 4.0:
                if n.cy < b.cy - 0.3:
                    sup.append(n)
                elif n.cy > b.cy + 0.3:
                    sub.append(n)
                else:
                    break
                j += 1
            else:
                break
        s = _atom(b, base)
        if sup:
            s += "^{%s}" % emit(sup, base)
        if sub:
            s += "_{%s}" % emit(sub, base)
        if prev is not None:
            gap = b.x0 - prev.x1
            if gap > 2.3 and not (b.txt and b.txt[0] in ",.;:)]}"):
                out.append(" ")
        out.append(s)
        prev = seq[j - 1] if (sup or sub) else b
        i = j
    return "".join(out)


def _atom(b, base):
    if b.kind == "frac":
        return r"\frac{%s}{%s}" % (emit(b.num, base), emit(b.den, base))
    if b.kind == "sqrt":
        return r"\sqrt{%s}" % emit(b.num, base)
    return SPECIAL.get(b.txt, b.txt)


def parse_page(page):
    """返回 [{'x','top','text','anchor'}] —— 按阅读顺序排列的行"""
    boxes = _boxes(page)
    rects = _lines_rects(page)
    from collections import Counter
    sizes = Counter(round(b.size, 1) for b in boxes if b.txt.strip())
    base = sizes.most_common(1)[0][0] if sizes else 10.0

    boxes = merge_sqrt(boxes, rects)
    boxes = merge_frac(boxes, rects)

    chars = [b for b in boxes if b.kind == "c" and b.txt.strip()]
    normal = [b for b in chars if b.size >= base * 0.92]
    small = [b for b in chars if b.size < base * 0.92]
    tall = [b for b in boxes if b.kind in ("frac", "sqrt")] + [b for b in chars if not b.txt.strip()]

    normal.sort(key=lambda b: b.bot)
    rows, cur = [], []
    for b in normal:
        if not cur or abs(b.bot - cur[-1].bot) <= 3.6:
            cur.append(b)
        else:
            rows.append(cur)
            cur = [b]
    if cur:
        rows.append(cur)
    if not rows:
        rows = [[]]

    # 上/下标：按“水平最近的正文字符”归行
    rows = [r for r in rows if r]
    for b in small:
        if not rows:
            rows = [[b]]
            continue
        cand = [i for i in range(len(rows)) if rows[i]]
        if not cand:
            continue
        k = min(cand, key=lambda i: min(
            (min(abs(b.x0 - m.x1), abs(m.x0 - b.x1)), abs(b.cy - m.cy)) for m in rows[i]))
        rows[k].append(b)

    # 分数/根号/空白：按竖直中心归行
    rows = [r for r in rows if r]
    for b in tall:
        if not rows:
            rows = [[b]]
            continue
        k = min(range(len(rows)), key=lambda i: abs(
            (sum(x.cy for x in rows[i]) / len(rows[i])) - b.cy))
        rows[k].append(b)

    rows = [r for r in rows if r]
    rows.sort(key=lambda r: min(b.top for b in r))

    # 同一视觉行但基线不同（如“A.”与高公式）：x 不相交且竖直相邻 → 合并
    merged = True
    while merged:
        merged = False
        for i in range(len(rows) - 1):
            a, b_ = rows[i], rows[i + 1]
            ax0, ax1 = min(x.x0 for x in a), max(x.x1 for x in a)
            bx0, bx1 = min(x.x0 for x in b_), max(x.x1 for x in b_)
            gap = min(x.top for x in b_) - max(x.bot for x in a)
            if (ax1 < bx0 - 1 or bx1 < ax0 - 1) and gap < 9:
                rows[i] = a + b_
                rows.pop(i + 1)
                merged = True
                break

    out = []
    for row in rows:
        row.sort(key=lambda b: b.x0)
        txt = emit(row, base)
        txt = re.sub(r"\s+", " ", txt).strip()
        if not txt:
            continue
        out.append({"x": row[0].x0, "top": min(b.top for b in row), "text": txt,
                    "x0": min(b.x0 for b in row), "x1": max(b.x1 for b in row),
                    "bot": max(b.bot for b in row)})
    out.sort(key=lambda r: r["top"])
    for r in out:
        t = r["text"]
        if ANCHOR_Q.match(t):
            r["anchor"], r["num"] = "q", int(ANCHOR_Q.match(t).group(1))
        elif ANCHOR_O.match(t):
            r["anchor"], r["letter"] = "o", ANCHOR_O.match(t).group(1)
        else:
            r["anchor"] = None
    return out


def page_boxes(page):
    """返回合并后的盒子（分数/根号已归并）与基准字号，供按区域取文本"""
    boxes = _boxes(page)
    rects = _lines_rects(page)
    from collections import Counter
    sizes = Counter(round(b.size, 1) for b in boxes if b.txt.strip())
    base = sizes.most_common(1)[0][0] if sizes else 10.0
    boxes = merge_sqrt(boxes, rects)
    boxes = merge_frac(boxes, rects)
    return boxes, base
