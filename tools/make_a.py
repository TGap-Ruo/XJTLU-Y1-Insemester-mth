# -*- coding: utf-8 -*-
"""生成《MTH026 期中考点梳理 v2》"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, OUT, print_pdf
import pdfkit
import a1, a2, a3
from ui import toc, h2, table

J = "".join
TITLE = "MTH026 期中考点梳理 v2 · 六讲精讲版"

toc_page = J([
"""<section class="chapter">""", h2("目录 Contents"),
toc([
 ("01", "函数、反函数与初等函数　<span class='muted small'>Ch1.5–1.9</span>", "考点 1–5 · T1.1–T1.4"),
 ("02", "极限的引入与极限定理　<span class='muted small'>Ch2.1–2.3</span>", "考点 6–12 · T2.1–T2.11"),
 ("03", "无穷远极限、渐近线、数列与三角极限　<span class='muted small'>Ch2.4–2.5</span>", "考点 13–18 · T3.1–T3.5"),
 ("04", "指数对数极限、数 e、复利与连续性　<span class='muted small'>Ch2.6–2.7</span>", "考点 19–24 · T4.1–T5.4"),
 ("05", "无穷小、导数定义与求导法则　<span class='muted small'>Ch2.8 / 3.1–3.6</span>", "考点 25–31 · T5.5–T6.7"),
 ("06", "反函数求导、隐函数与相关变化率　<span class='muted small'>Ch3.7–3.10</span>", "考点 32–37 · T7.1–T8.1"),
 ("附", "导数的应用（超出六讲范围）　<span class='muted small'>Ch4.1–4.5</span>", "考点 38–42 · T9.1–T9.5"),
 ("A", "附录 A　一页纸公式速查", "考前 10 分钟"),
 ("B", "附录 B　24 条易错清单", "自测用"),
 ("C", "附录 C　七天冲刺计划", "按天执行"),
 ("D", "附录 D　题型索引（49 类）", "对接刷题器"),
]),
"""<div style="margin:5mm 0 0;padding:3mm 4mm;background:#f2f6fc;border-left:3px solid #2f6fb5;border-radius:2px;font-size:9pt">
<b class="sans" style="color:#2f6fb5;letter-spacing:.08em">范围声明</b>　正文六讲严格对应 Lecture Notes 1–6（Ch1.5 – Ch3.10）；<b>课件未覆盖的内容一律进入附章并明确标注</b>。题库 351 道唯一题按 49 类题型归并，刷题器中的 196 道精练题使用同一编号。</div>""",
"""<div style="margin-top:6mm">""",
"""<div style="margin:0 0 2mm"><span class="sans" style="font-size:8.6pt;letter-spacing:.16em;color:#2f6fb5;font-weight:700">复习进度打卡表</span><span class="sans" style="font-size:8pt;color:#6b7a8f">　建议每天填一行，第二次刷题正确率低于 80% 的讲次隔两天再刷</span></div>""",
table(["讲次", "题库题量", "首刷正确率", "错题数", "复刷日期", "状态"],
      [["第 1 讲　函数与反函数", "50", "　　　/ 50", "　　", "　　/　　", "☐ 待完成"],
       ["第 2 讲　极限与极限定理", "76", "　　　/ 76", "　　", "　　/　　", "☐ 待完成"],
       ["第 3 讲　无穷远与三角极限", "30", "　　　/ 30", "　　", "　　/　　", "☐ 待完成"],
       ["第 4 讲　e、复利与连续性", "60", "　　　/ 60", "　　", "　　/　　", "☐ 待完成"],
       ["第 5 讲　无穷小与求导法则", "50", "　　　/ 50", "　　", "　　/　　", "☐ 待完成"],
       ["第 6 讲　隐函数与相关变化率", "45", "　　　/ 45", "　　", "　　/　　", "☐ 待完成"],
       ["附章　导数的应用（超纲）", "40", "　　　/ 40", "　　", "　　/　　", "☐ 选做"]],
      compact=True, widths=["auto", "20mm", "26mm", "18mm", "26mm", "22mm"]),
"""</div>""",
"""</section>"""])

parts = [a1.S[0], a1.S[1], toc_page] + a1.S[2:] + a2.S + a3.S
html = pdfkit.assemble(parts, TITLE)
hp = os.path.join(OUT, "pdf_a.html")
open(hp, "w", encoding="utf-8").write(html)
raw = os.path.join(OUT, "_a_raw.pdf")
print_pdf(hp, raw)
final = os.path.join(OUT, "MTH026_期中考点梳理_v2.pdf")
pdfkit.stamp(raw, final, "MTH026 Calculus I · 期中考点梳理 v2", "XJTLU · 六讲精讲版")
import pypdf
print("页数:", len(pypdf.PdfReader(final).pages), "→", final)
