# -*- coding: utf-8 -*-
"""PDF 排版组件"""
import json, os
from common import ROOT, OUT

with open(os.path.join(OUT, "questions.json"), encoding="utf-8") as f:
    DATA = json.load(f)

QS = DATA["questions"]
TYPES = {t["id"]: t for t in DATA["types"]}
BY_TYPE = {}
for _q in QS:
    BY_TYPE.setdefault(_q["type"], []).append(_q)

STAR = {1: "★☆☆", 2: "★★☆", 3: "★★★"}


def esc(s):
    return s


def cover(kicker, title_html, sub, sub2, tags, meta, stamp):
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    meta_html = "".join(f"<div><b>{a}</b>{b}</div>" for a, b in meta)
    return f"""<section class="cover"><div class="grid"></div><div class="glow"></div>
<div class="inner"><div class="brand">{kicker}</div><div class="rule"></div>
<h1>{title_html}</h1><div class="sub">{sub}</div><div class="sub2">{sub2}</div>
<div class="tags">{tags_html}</div>
<div class="meta">{meta_html}</div></div><div class="stamp">{stamp}</div></section>"""


CN_NUM = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5", "六": "6",
          "七": "7", "八": "8", "九": "9", "附": "A"}


def chapter(num, title, desc, src, amber=False):
    cls = "ch-hero hero-amber" if amber else "ch-hero"
    num = CN_NUM.get(num, num)
    return f"""<section class="chapter"><div class="{cls}" data-num="{num}">
<div class="kicker">{'附章 · BEYOND SCOPE' if amber else 'LECTURE / CHAPTER'}</div>
<h2>{title}</h2><div class="desc">{desc}</div><div class="src">{src}</div></div>"""


def kp(num, title, meta, body):
    return f"""<div class="kp"><div class="kp-h"><span class="kp-n">{num}</span>
<span class="kp-t">{title}</span><span class="kp-a">{meta}</span></div>
<div class="kp-b">{body}</div></div>"""


def fbox(title, rows, cols=2):
    cells = "".join(f"<span>{r}</span>" for r in rows)
    style = "" if cols == 2 else ' style="display:block"'
    if cols == 1:
        return (f'<div class="fbox"><div class="t">{title}</div>'
                + "".join(f'<div style="margin:1.4mm 0">{r}</div>' for r in rows) + "</div>")
    return f'<div class="fbox"><div class="t">{title}</div><div class="row">{cells}</div></div>'


def tip(kind, label, text):
    return f'<div class="tip {kind}"><b>{label}</b> {text}</div>'


def bullets(items):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def table(headers, rows, compact=False, widths=None):
    cls = ' class="compact"' if compact else ""
    th = "".join(f"<th>{h}</th>" for h in headers)
    body = ""
    for r in rows:
        tds = ""
        for i, c in enumerate(r):
            w = f' style="width:{widths[i]}"' if widths else ""
            tds += f"<td{w}>{c}</td>"
        body += f"<tr>{tds}</tr>"
    return f"<table{cls}><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>"


def ex(label, qhtml, ahtml, meta=""):
    return f"""<div class="ex"><div class="ex-h"><span>{label}</span><span>{meta}</span></div>
<div class="ex-b"><div class="q">{qhtml}</div>
<div class="a"><b>解析</b>　{ahtml}</div></div></div>"""


def ex_auto(tid, idx=0, label=None):
    """从题库取一道例题渲染"""
    qs = BY_TYPE[tid]
    if idx >= len(qs):
        idx = 0
    item = qs[idx]
    label = label or f"例题 · {tid}"
    parts = []
    for i, o in enumerate(item["options"]):
        cls = " class='ok'" if i == item["answer"] else ""
        parts.append("<span%s><b>%s</b>%s</span>" % (cls, chr(65 + i), o))
    qh = item["stem"] + "<div class='opts'>" + "".join(parts) + "</div>"
    ans = chr(65 + item["answer"])
    sol = item["sol"] + "<span class='ansline'>▶ 正确答案 %s</span>" % ans
    return ex(label, qh, sol, "%s · %s" % (tid, STAR[item["diff"]]))


def toc(rows):
    out = ""
    for n, t, s in rows:
        out += f'<div class="toc-row"><span class="n">{n}</span><span class="t">{t}</span><span class="s">{s}</span></div>'
    return out


def h2(text):
    return f'<h2 class="sec">{text}</h2>'


def h3(text):
    return f'<h3 class="sub">{text}</h3>'


def h4(text):
    return f"<h4>{text}</h4>"


def lec_overview(lec, title="本讲速览"):
    """按讲次列出全部题型：编号 / 题型 / 一句话核心 / 题库题量"""
    rows = []
    total = 0
    for t in DATA["types"]:
        if t["lec"] != lec:
            continue
        n = t["bank"]
        total += n
        rows.append([t["id"], t["name"], t["core"], str(n), STAR[t["diff"]]])
    head = ('<div style="margin:5mm 0 3mm"><span class="sans" style="font-size:8.6pt;letter-spacing:.16em;'
            'color:#2f6fb5;font-weight:700">' + title + '</span>'
            '<span class="sans" style="font-size:8pt;color:#6b7a8f">　本讲共 ' + str(total)
            + ' 道题库题，下列 ' + str(len(rows)) + ' 类题型全部覆盖</span></div>')
    return head + table(["编号", "题型", "一句话核心", "题量", "难度"], rows, compact=True,
                        widths=["15mm", "42mm", "auto", "14mm", "17mm"])


USED = set()


def self_test(lec, n=8, title=None):
    """本讲自测：取该讲尚未作为例题出现的题目，末尾给答案速查。"""
    pool = [q for q in QS if q["lec"] == lec and q["id"] not in USED]
    if not pool:
        return ""
    pool.sort(key=lambda q: (q["diff"], q["id"]))
    pick = pool[:n]
    rows = []
    for k, q in enumerate(pick):
        USED.add(q["id"])
        opts = "　".join("<span style='white-space:nowrap'>%s. %s</span>" % (chr(65 + i), o)
                         for i, o in enumerate(q["options"]))
        rows.append("<div style='margin:0 0 2.4mm'><b style='color:#1d3f6e'>%d.</b> %s"
                    "<div class='small' style='color:#44546b;margin-top:0.6mm'>%s</div></div>"
                    % (k + 1, q["stem"], opts))
    keys = "　".join("<b>%d</b> %s" % (k + 1, chr(65 + q["answer"])) for k, q in enumerate(pick))
    head = title or "本讲自测"
    return ("<div class='selftest'><div class='st-h'><span>%s · %d 题</span>"
            "<span>限时 %d 分钟</span></div>" % (head, len(pick), max(3, len(pick) // 2))
            + "<div class='st-b'>" + "".join(rows) + "</div>"
            + "<div class='st-k'><b>答案速查</b>　" + keys + "</div></div>")


def ex_free(tid, k=2):
    """取该题型中尚未被使用的题目作为例题"""
    pool = [q for q in BY_TYPE[tid] if q["id"] not in USED]
    if len(pool) < k:
        pool = BY_TYPE[tid]
    out = []
    for q in pool[:k]:
        USED.add(q["id"])
        parts = []
        for i, o in enumerate(q["options"]):
            cls = " class='ok'" if i == q["answer"] else ""
            parts.append("<span%s><b>%s</b>%s</span>" % (cls, chr(65 + i), o))
        qh = q["stem"] + "<div class='opts'>" + "".join(parts) + "</div>"
        sol = q["sol"] + "<span class='ansline'>▶ 正确答案 %s</span>" % chr(65 + q["answer"])
        out.append(ex("例题 %d · %s" % (len(out) + 1, tid), qh, sol,
                      "%s · %s" % (tid, STAR[q["diff"]])))
    return "".join(out)


def steps_html(steps):
    items = "".join(
        "<div class='stepline'><b>%d</b><span>%s</span></div>" % (i + 1, s) for i, s in enumerate(steps))
    return "<div class='steps'>" + items + "</div>"
