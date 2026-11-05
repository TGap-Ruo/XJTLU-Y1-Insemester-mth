# -*- coding: utf-8 -*-
"""Build the English comprehensive question bank PDF."""
import html as H
import json, os, sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import ROOT, print_pdf
from sections import SECTIONS, CHAPTERS, BY_Q
from method_a import M1
from method_b import M2
from terms import GLOSSARY, SHORT, flat_glossary
import pb
import pdfkit

M = {**M1, **M2}
ASSETS = os.path.join(ROOT, "assets")
QDIR = os.path.join(ROOT, "qbank", "q")
ODIR = os.path.join(ROOT, "qbank", "o")
OUT = os.path.join(ROOT, "out")

SEG = json.load(open(os.path.join(ROOT, "build", "segments.json")))
LAT = json.load(open(os.path.join(ROOT, "build", "latex.json")))
ANS = json.load(open(os.path.join(ROOT, "build", "answers_final.json")))
ATXT = json.load(open(os.path.join(ROOT, "build", "ans_text.json")))

try:
    from expl_all import E
except Exception:
    E = {}

ZH = {en: zh for en, zh, _n, _c in flat_glossary()}
SCALE = 2.6
MM = 0.352778 * 1000 / SCALE / 1000  # px -> mm  (px/2.6 pt * 0.3528 mm/pt)

CSS = r"""
:root{
  --ink:#12171f; --ink2:#33404f; --ink3:#6d7c8d;
  --line:#dde4ec; --line2:#eef2f7;
  --pri:#16406e; --pri2:#2c6ba8; --pri-bg:#f1f6fb;
  --gold:#9a6a1c; --gold-bg:#fdf7ec;
  --green:#1e6446; --green-bg:#eef7f1;
  --red:#9c3a2e; --red-bg:#fbf1ef;
}
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{size:A4;margin:15mm 14mm 15mm 14mm;}
@page:first{margin:0;}
html,body{margin:0;padding:0;}
body{font-family:"Charter","Palatino","Songti SC",Georgia,serif;font-size:10pt;line-height:1.72;color:var(--ink);background:#fff;}
.sans,h1,h2,h3,h4,.lbl,.badge,.tag{font-family:"Avenir Next","Helvetica Neue","PingFang SC",sans-serif;}
.zh{font-family:"Songti SC","STSong",serif;}

/* cover */
.cover{height:297mm;position:relative;overflow:hidden;page-break-after:always;
  background:linear-gradient(155deg,#0d2138 0%,#16406e 48%,#255b96 100%);color:#fff;}
.cover .grid{position:absolute;inset:0;opacity:.14;
  background-image:linear-gradient(rgba(255,255,255,.55) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.55) 1px,transparent 1px);
  background-size:24px 24px;}
.cover .glow{position:absolute;width:560px;height:560px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,205,120,.34),transparent 66%);right:-160px;top:-150px;}
.cover .inner{position:relative;padding:36mm 22mm 18mm;height:100%;display:flex;flex-direction:column;}
.cover .brand{font-size:9.6pt;letter-spacing:.44em;color:#b6cee8;text-transform:uppercase;}
.cover .rule{width:52px;height:3px;background:#f0c479;margin:7mm 0 8mm;}
.cover h1{font-size:31pt;line-height:1.2;margin:0 0 6mm;font-weight:700;letter-spacing:.005em;}
.cover .sub{font-size:12.6pt;color:#d6e5f6;font-weight:300;letter-spacing:.04em;}
.cover .sub2{font-size:10pt;color:#9db8d8;margin-top:2mm;letter-spacing:.03em;}
.cover .tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:9mm;}
.cover .tag{font-size:8.4pt;padding:3px 9px;border:1px solid rgba(255,255,255,.32);border-radius:2px;
  color:#e4eefa;background:rgba(255,255,255,.07);}
.cover .cov-list{margin-top:15mm;}
.cover .cov-list div{display:flex;gap:5mm;font-size:9.2pt;color:#cfe0f2;padding:2.6mm 0;
  border-top:1px solid rgba(255,255,255,.14);line-height:1.5;}
.cover .cov-list div:last-child{border-bottom:1px solid rgba(255,255,255,.14);}
.cover .cov-list span{font-family:"Avenir Next",sans-serif;color:#f0c479;font-size:8.4pt;letter-spacing:.1em;min-width:8mm;}
.cover .stats{margin-top:auto;display:grid;grid-template-columns:repeat(4,1fr);gap:0;
  border-top:1px solid rgba(255,255,255,.2);padding-top:6mm;}
.cover .stats div{font-size:8.4pt;color:#a6c0dc;line-height:1.5;}
.cover .stats b{display:block;font-size:17pt;color:#fff;font-weight:600;letter-spacing:.01em;}
.cover .foot{margin-top:6mm;font-size:8pt;color:#7e9dbd;letter-spacing:.24em;}

/* chapter opener */
.chapter{page-break-before:always;padding-top:2mm;}
.ch-hero{background:linear-gradient(120deg,#16406e,#2c6ba8);color:#fff;padding:10mm 11mm 8mm;border-radius:2px;position:relative;overflow:hidden;margin-bottom:5mm;}
.ch-hero:after{content:attr(data-num);position:absolute;right:5mm;top:-10mm;font-size:92pt;font-weight:700;color:rgba(255,255,255,.12);}
.ch-hero .kicker{font-size:8.4pt;letter-spacing:.28em;color:#a6c9ea;margin-bottom:2.6mm;text-transform:uppercase;}
.ch-hero h2{margin:0;font-size:19pt;font-weight:700;}
.ch-hero .desc{font-size:9.6pt;color:#cfe0f2;margin-top:3mm;}
.ch-hero .src{font-size:8.2pt;color:#9dc0e2;margin-top:4mm;}

/* section */
.sec{margin:0 0 6mm;}
.sec-top{page-break-inside:avoid;}
.sec-h{display:flex;align-items:baseline;gap:3.5mm;border-bottom:1.6px solid var(--pri);
  padding-bottom:2mm;margin:7mm 0 3.4mm;page-break-after:avoid;}
.sec-id{font-size:8.4pt;font-weight:700;color:#fff;background:var(--pri);padding:1.1mm 2.4mm;border-radius:2px;letter-spacing:.05em;}
.sec-t{font-size:13pt;font-weight:700;color:var(--pri);flex:1;line-height:1.3;}
.sec-m{font-size:7.8pt;color:var(--ink3);white-space:nowrap;}
.sec-zh{font-size:9pt;color:var(--ink3);margin:-1.6mm 0 3mm;}

/* method card */
.mc{border:1px solid var(--line);border-left:3px solid var(--pri2);background:#fafcfe;
  border-radius:2px;padding:3mm 3.6mm 3.2mm;margin:0 0 4mm;page-break-inside:avoid;}
.mc .lbl{font-size:7.6pt;letter-spacing:.16em;color:var(--pri2);font-weight:700;text-transform:uppercase;margin-bottom:1.2mm;}
.mc p{margin:0 0 2mm;}
.mc ol{margin:0.6mm 0 0;padding-left:5mm;}
.mc li{margin:0.6mm 0;}
.mc .cols{display:grid;grid-template-columns:1.15fr 1fr;gap:0 6mm;margin-top:1mm;}
.mc .trap{margin-top:2.6mm;padding:2mm 3mm;background:var(--red-bg);border-left:2.5px solid var(--red);
  font-size:8.8pt;border-radius:2px;}
.mc .trap b{color:var(--red);font-size:8pt;letter-spacing:.08em;}
.kt-row{margin-top:2.4mm;padding-top:2mm;border-top:1px dashed var(--line);font-size:8.2pt;}
.kt-lbl{font-size:7.2pt;letter-spacing:.16em;color:var(--ink3);margin-right:2.4mm;font-family:"Avenir Next",sans-serif;}
.kt{display:inline-block;margin:0 3mm 1mm 0;color:var(--ink2);}
.kt b{color:var(--pri2);font-weight:600;margin-left:1mm;font-family:"Songti SC",serif;}
.mc .zhbox{background:#f7f9fc;border-radius:2px;padding:2mm 3mm;font-size:9.2pt;}

/* question */
.q{border:1px solid var(--line);border-radius:3px;margin:0 0 2.4mm;page-break-inside:avoid;}
.q-h{display:flex;align-items:center;gap:3mm;padding:1.2mm 3mm;background:#f2f6fb;border-bottom:1px solid var(--line);border-radius:2px 2px 0 0;}
.q-n{font-size:8.4pt;font-weight:700;color:#fff;background:#2c6ba8;padding:0.9mm 2.4mm;border-radius:2px;letter-spacing:.04em;}
.q-x{font-size:7.8pt;color:var(--ink3);letter-spacing:.06em;}
.q-b{padding:1.8mm 3mm 1.9mm;}
.q-img{display:block;max-width:100%;height:auto;margin:0;}
.ans{display:flex;align-items:baseline;gap:2.6mm;margin:1.3mm 0 0;padding:1.05mm 2.6mm;
  background:var(--green-bg);border-radius:2px;border-left:2.5px solid var(--green);}
.ans .k{font-size:7.6pt;letter-spacing:.14em;color:var(--green);font-weight:700;text-transform:uppercase;}
.ans .v{font-size:9.6pt;font-weight:700;color:var(--green);}
.ans img{height:5.8mm;width:auto;vertical-align:middle;}
.sol{margin-top:1.3mm;display:grid;grid-template-columns:1fr 1px 1fr;gap:0 4mm;}
.sol .bar{background:var(--line);}
.sol .en{font-size:8.8pt;line-height:1.9;}
.sol .zh{font-size:8.6pt;line-height:1.92;color:var(--ink2);}
.sol .tag{display:inline-block;font-size:7pt;letter-spacing:.14em;color:var(--ink3);
  border:1px solid var(--line);border-radius:2px;padding:0 1.4mm;margin-bottom:0.8mm;text-transform:uppercase;}

/* part B — items from the live practice quizzes */
.phead{display:flex;align-items:baseline;gap:4mm;margin:7mm 0 2.6mm;padding:1.8mm 0 1.5mm;
  border-top:1.4px solid #d9c9a8;border-bottom:1.4px solid #d9c9a8;}
.phead-t{font-family:"Avenir Next",sans-serif;font-size:8.2pt;font-weight:700;color:#8a5a12;
  letter-spacing:.16em;text-transform:uppercase;}
.phead-n{font-size:8pt;color:var(--ink3);}
/* card sits as an atomic inline box: that is the only break rule Chrome's
   print path honours, and shrink-to-fit stops a short item from sitting in a
   full-width panel with an empty right half.  No frame: the crop is 1:1 and
   often narrower than the column, and a box would just draw the gap. */
.prow{page-break-inside:avoid;break-inside:avoid;margin:0 0 4.4mm;}
.p{display:inline-block;vertical-align:top;max-width:176mm;}
.p-h{display:flex;align-items:center;gap:3mm;padding:0 0 1.5mm;margin-bottom:2mm;
  border-bottom:1px solid #eadfc9;}
.p-n{font-size:8.2pt;font-weight:700;color:#fff;background:#9a6a1c;padding:0.85mm 2.2mm;
  border-radius:2px;letter-spacing:.04em;}
.p-x{font-size:7.6pt;color:#8a7550;letter-spacing:.04em;}
.p-b{padding:0;}
.p-q{display:block;height:auto;margin:0;max-width:100%;}
.p-s{display:block;height:auto;margin:0;max-width:100%;}
.p-ans{background:#fbf7ee;border-left-color:#c79a3e;align-items:center;padding:1.05mm 2.6mm;margin:1.8mm 0 1.8mm;}
.ans .p-a{display:block;height:auto;width:auto;max-width:100%;}

/* front matter */
h2.major{font-size:15pt;color:var(--pri);margin:0 0 3mm;padding-bottom:2mm;border-bottom:2px solid var(--pri);}
h3.minor{font-size:10.6pt;color:var(--pri);margin:6mm 0 2mm;padding-left:7px;border-left:3px solid var(--pri2);}
p{margin:0 0 2.4mm;}
table{width:100%;border-collapse:collapse;margin:2.5mm 0 4mm;font-size:8.8pt;page-break-inside:auto;}
thead{display:table-header-group;} tr{page-break-inside:avoid;}
th{background:var(--pri);color:#fff;font-family:"Avenir Next",sans-serif;font-weight:600;font-size:8pt;padding:2mm 2.2mm;text-align:left;}
td{padding:1.5mm 2.2mm;border-bottom:1px solid var(--line2);vertical-align:top;}
tr:nth-child(even) td{background:#fafbfd;}
.pb{page-break-before:always;}
.two{display:grid;grid-template-columns:1fr 1fr;gap:0 7mm;}
.note{border-left:3px solid var(--gold);background:var(--gold-bg);padding:2.6mm 3.4mm;font-size:9pt;border-radius:2px;margin:3mm 0;}
.note b{color:var(--gold);font-size:8.2pt;letter-spacing:.1em;}
.toc-row{display:flex;align-items:baseline;font-size:9.4pt;padding:1.7mm 0;border-bottom:1px dotted var(--line);}
.toc-row .n{width:11mm;color:var(--pri2);font-weight:700;font-size:8.8pt;}
.toc-row .t{flex:1;}
.toc-row .s{color:var(--ink3);font-size:8.2pt;}
.grid-key{display:grid;grid-template-columns:repeat(10,1fr);gap:1px;font-size:8pt;margin-top:2mm;page-break-inside:avoid;}
.grid-key div{background:#f4f7fb;padding:0.85mm 0.5mm;line-height:1.25;text-align:center;border-radius:1px;}
.grid-key div b{color:var(--green);margin-left:0.9mm;}
.anspage{page-break-inside:avoid;}
.katex{font-size:1.02em;}
"""


def mm(px):
    return px * 0.352778 / SCALE * 0.86


def img(fn, cls=""):
    return '<img class="%s" src="file://%s">' % (cls, fn)


def imgw(iw, ih, cap_h=45.0, cap_w=180.0):
    """Crop width in mm, held to a height budget so three cards fit a page."""
    w = min(mm(iw), cap_w)
    h = w * ih / float(iw)
    if h > cap_h:
        w *= cap_h / h
    return w


def question_html(n):
    k = str(n)
    qn = QDIR + "/q%03d.png" % n
    w = SEG[k]["stem"]
    from PIL import Image
    iw, ih = Image.open(qn).size
    letter = ANS[k]["ans"]
    opt = ODIR + "/q%03d_%s.png" % (n, letter)
    has_opt = os.path.exists(opt)
    sec = BY_Q[n]["id"]
    parts = ['<div class="q">',
             '<div class="q-h"><span class="q-n">Q%d</span><span class="q-x">%s</span></div>' % (n, sec),
             '<div class="q-b">',
             '<img class="q-img" style="width:%.2fmm" src="file://%s">' % (imgw(iw, ih), qn),
             '<div class="ans"><span class="k">Answer</span><span class="v">%s</span>' % letter]
    # the answer expression is stated in the solution text; the letter is enough here
    parts.append('</div>')
    if n in E:
        en, zh = E[n]
        parts.append('<div class="sol"><div class="en">%s</div><div class="bar"></div>'
                     '<div class="zh">%s</div></div>'
                     % (H.escape(en, quote=False), H.escape(zh, quote=False)))
    parts.append('</div></div>')
    return "".join(parts)


def section_html(sec):
    m = M[sec["id"]]
    steps = "".join("<li>%s</li>" % s for s in m["steps"])
    h = ['<div class="sec">', '<div class="sec-top">',
         '<div class="sec-h"><span class="sec-id">%s</span><span class="sec-t">%s</span>'
         '<span class="sec-m">%d questions · Q%d–Q%d</span></div>' % (
             sec["id"], sec["en"], sec["n"], sec["start"], sec["end"]),
         '<div class="sec-zh zh">%s</div>' % sec["zh"],
         '<div class="mc"><div class="lbl">What the question is testing</div><p>%s</p>' % m["focus"],
         '<div class="cols"><div><div class="lbl">Method</div><ol>%s</ol></div>'
         '<div><div class="lbl">中文要点</div><div class="zhbox zh">%s</div></div></div>' % (steps, m["zh"]),
         '<div class="trap"><b>COMMON ERROR</b> &nbsp;%s</div>' % m["trap"]]
    kt = SHORT.get(sec["id"], [])
    if kt:
        h.append('<div class="kt-row"><span class="kt-lbl">KEY TERMS</span>%s</div>' % "".join(
            '<span class="kt">%s%s</span>' % (
                t, ('<b>' + ZH[t] + '</b>') if t in ZH else '') for t in kt))
    h.append('</div></div>')
    for n in range(sec["start"], sec["end"] + 1):
        h.append(question_html(n))
    h.append(pb.block(sec["id"]))
    h.append("</div>")
    return "".join(h)


def cover():
    return """
<div class="cover"><div class="grid"></div><div class="glow"></div>
<div class="inner">
  <div class="brand">XJTLU &middot; MTH026 Calculus I</div>
  <div class="rule"></div>
  <h1>Complete<br>Question Bank</h1>
  <div class="sub">351 compiled items + 323 from your own attempts &middot; 54 topics</div>
  <div class="sub2">English questions &middot; bilingual solutions (EN + 中文)</div>
  <div class="tags"><span class="tag">Practice Quiz 1 · W4</span><span class="tag">Practice Quiz 2 · W6</span>
  <span class="tag">Practice Quiz 3 · W8</span><span class="tag">9 chapters</span>
  <span class="tag">54 topics</span><span class="tag">Original page crops</span></div>
  <div class="cov-list">
    <div><span>01</span>674 items, every one cropped straight from the source page — no re-typing</div>
    <div><span>02</span>A method card per topic: what is tested, the routine, the standard error</div>
    <div><span>03</span>Bilingual solutions: one line of English reasoning, one line of 中文解析</div>
    <div><span>04</span>An answer grid at the back for timed self-testing</div>
  </div>
  <div class="stats">
    <div><b>674</b>items</div><div><b>54</b>topics</div>
    <div><b>15</b>source attempts</div><div><b>2</b>languages</div>
  </div>
  <div class="foot">STUDY EDITION &middot; FOR PERSONAL REVISION ONLY</div>
</div></div>"""


def provenance():
    rows = [
        ["1–5", "Practice quiz 1 – W4", "8 Oct 2026", "30–31", "30/32 – 32/32"],
        ["6–10", "Practice quiz 2 – W6", "22 Oct 2026", "15–16", "up to 16/16"],
        ["11–15", "Practice quiz 3 – W8", "4 Nov 2026", "16–17", "up to 17/17"],
    ]
    tr = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(r) for r in rows)
    return """
<div class="pb"></div>
<h2 class="major">How this book was built</h2>
<p>This volume merges two sources: the compiled bank <i>MTH026题库分类汇总</i> and the folder
<i>MTH026-Quiz</i>. They overlap far less than the titles suggest, and the difference matters.</p>

<p>The compiled bank is <b>351 items</b>, numbered Q1–Q351, and makes up the body of each topic below.
The folder holds <b>fifteen Moodle attempt print-outs</b> of three practice quizzes (five attempts of each);
after de-duplication they contain <b>323 further items</b> — the ones you were actually served. The two sets
share the <i>wording</i> of a question but not its <i>numbers</i>: the pool randomises the parameters on every
draw, so the compiled bank's log₃(−x²−3x+28) and your paper's log₇(−x²−8x−12) are the same question type with
different data. Only 2 of the 323 appear in the compiled bank verbatim.</p>

<p>So both are printed, and they are labelled: <b>Q-numbers</b> are the compiled bank, <b>P-numbers</b> (gold
cards, “From your practice quizzes”) are your own attempts. Every P-item sits in the topic it belongs to, so a
topic runs: method card → compiled items → your items.</p>

<h3 class="minor">Source files absorbed</h3>
<table><thead><tr><th>Folder file(s)</th><th>Quiz</th><th>Attempt date</th><th>Pages</th><th>Best mark</th></tr></thead>
<tbody>%s</tbody></table>

<div class="note"><b>WHY THE QUESTIONS LOOK EXACTLY LIKE THE ORIGINALS</b><br>
Every question is a <b>crop of the original page</b>, not a re-typed version. Symbols, spacing,
fraction bars and answer layout are byte-for-byte what the course produced — there is no transcription
step where a minus sign or an exponent could go missing.</div>

<h3 class="minor">What each entry gives you</h3>
<table><thead><tr><th style="width:32mm">Part</th><th>What it is for</th></tr></thead><tbody>
<tr><td>The question</td><td>The original item, exactly as printed, with all five choices.</td></tr>
<tr><td>Answer</td><td>The correct letter; the value behind it is spelled out in the solution.</td></tr>
<tr><td>Solution (EN)</td><td>The decisive step — the one line that turns the question into the answer.</td></tr>
<tr><td>解析 (中文)</td><td>The same reasoning in Chinese, with the trap that usually costs the mark.</td></tr>
<tr><td>Method card</td><td>One per topic: what is being tested, the routine, and the standard error.</td></tr>
<tr><td>P-items (gold)</td><td>From your own attempts: the question, the paper's own “Answer: …” line and the
printed solution, all cropped from the attempt. The answer is the expression the paper printed, not a letter —
Moodle's fraction layout makes letter recovery unreliable, and a wrong letter is worse than none.</td></tr>
</tbody></table>

<h3 class="minor">How to use it</h3>
<div class="two"><div>
<p><b>Pass 1 — recognise.</b> Cover the solution, read only the question, and say out loud which
topic it belongs to. Do one question per topic. The goal is speed of recognition, not correctness.</p>
<p><b>Pass 2 — execute.</b> Work the remaining questions of each topic with the method card in view.
Check only after you have written your own line.</p>
</div><div>
<p><b>Pass 3 — repair.</b> Re-do only the items you missed, plus every topic with ten or more questions
(those are the ones the exam leans on).</p>
<p><b>Pass 4 — speed.</b> Use the answer grid at the back: read a question number, answer from memory,
check the letter. Twenty items in ten minutes is the target.</p>
</div></div>

<div class="note"><b>A NOTE ON THE SOURCE ANSWER KEY</b><br>
The compiled bank's own key was checked item by item. It is reliable except for
<b>Q7 and Q9</b>, where it prints “none of the other four choices is correct” although a correct
choice is visibly present; both are corrected here. Items whose key genuinely is “none of these”
were re-derived independently rather than copied — see the solution text for each.</div>
""" % tr


def contents():
    rows = []
    for ci, (_num, c_en, c_zh, secs) in enumerate(CHAPTERS):
        rows.append('<div class="toc-row" style="margin-top:3mm;border-bottom:1.6px solid var(--line)">'
                    '<span class="n">%d</span><span class="t"><b>%s</b></span>'
                    '<span class="s">%s</span></div>' % (ci + 1, c_en, c_zh))
        for sid, en, zh, n in secs:
            s = next(x for x in SECTIONS if x["id"] == sid)
            rows.append('<div class="toc-row"><span class="n">%s</span><span class="t">%s</span>'
                        '<span class="s">Q%d–Q%d · %d</span></div>' % (
                            sid, en, s["start"], s["end"], n))
    return '<h2 class="major" style="margin-top:9mm">Contents</h2>' + "".join(rows)


def chapter_opener(ci):
    num, c_en, c_zh, secs = CHAPTERS[ci]
    n = sum(s[3] for s in secs)
    first = next(x for x in SECTIONS if x["ch"] == ci)
    last = [x for x in SECTIONS if x["ch"] == ci][-1]
    return ('<div class="chapter"><div class="ch-hero" data-num="%d">'
            '<div class="kicker">Chapter %d</div><h2>%s</h2>'
            '<div class="desc zh">%s</div>'
            '<div class="src">%d questions &middot; %d topics &middot; Q%d–Q%d</div></div></div>'
            % (ci + 1, ci + 1, c_en, c_zh, n, len(secs), first["start"], last["end"]))


def glossary():
    out = ['<div class="pb"></div><h2 class="major">Terminology &nbsp;术语表</h2>',
           '<p>Every technical term used in this book appears here in English with its Chinese equivalent. '
           'Learn the English form first — the quiz, the lectures and the exam paper all use it.</p>']
    for ch_en, ch_zh, items in GLOSSARY:
        out.append('<h3 class="minor">%s &nbsp;<span style="color:#6d7c8d;font-weight:400">%s</span></h3>' % (ch_en, ch_zh))
        rows = "".join('<tr><td style="width:52mm"><b>%s</b></td><td style="width:30mm" class="zh">%s</td>'
                       '<td class="zh">%s</td></tr>' % (en, zh, note) for en, zh, note in items)
        out.append('<table><tbody>%s</tbody></table>' % rows)
    return "".join(out)


def answer_grid():
    cells = []
    for n in range(1, 352):
        cells.append('<div>%d<b>%s</b></div>' % (n, ANS[str(n)]["ans"]))
    return ('<div class="pb"></div><div class="anspage">'
            '<h2 class="major">Answer grid</h2>'
            '<p class="small">Answer from memory, then check the letter. Use this page for timed revision.</p>'
            '<div class="grid-key">' + "".join(cells) + "</div></div>")


def build(only_chapter=None, out_name="MTH026_QuestionBank_EN.pdf"):
    body = [cover(), provenance(), contents()]
    chs = range(len(CHAPTERS)) if only_chapter is None else [only_chapter]
    for ci in chs:
        body.append(chapter_opener(ci))
        for sec in SECTIONS:
            if sec["ch"] == ci:
                body.append(section_html(sec))
    if only_chapter is None:
        body.append(glossary())
        body.append(answer_grid())
    html = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
            '<title>MTH026 Complete Question Bank</title>'
            '<link rel="stylesheet" href="file://%s/katex.min.css">'
            '<style>%s</style></head><body>' % (ASSETS, CSS)
            + "".join(body) +
            '<script src="file://%s/katex.min.js"></script>'
            '<script src="file://%s/auto-render.min.js"></script>'
            '<script>document.addEventListener("DOMContentLoaded",function(){'
            'renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},'
            '{left:"$",right:"$",display:false}],throwOnError:false,strict:false});});</script>'
            '</body></html>' % (ASSETS, ASSETS))
    hp = os.path.join(OUT, "qbank.html")
    open(hp, "w", encoding="utf-8").write(html)
    raw = os.path.join(OUT, "_qbank_raw.pdf")
    print_pdf(hp, raw)
    final = os.path.join(OUT, out_name)
    pdfkit.stamp(raw, final, "MTH026 Calculus I · Complete Question Bank",
                 "674 items · 54 topics · EN / 中文",
                 foot="MTH026 · Complete Question Bank")
    import pypdf
    print("pages:", len(pypdf.PdfReader(final).pages), "->", final)
    return final


if __name__ == "__main__":
    ch = None if len(sys.argv) < 2 else int(sys.argv[1])
    name = "MTH026_QuestionBank_EN.pdf" if ch is None else "pilot_ch%d.pdf" % (ch + 1)
    build(ch, name)
