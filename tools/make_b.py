# -*- coding: utf-8 -*-
"""生成《MTH026 题库分类精解 v2》"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, OUT, print_pdf
import pdfkit
from ui import *
from type_extra import EXTRA
import a1, a2, a3   # 仅用于登记 PDF A 已用题目，避免两册重复

J = "".join
TITLE = "MTH026 题库分类精解 v2"

CH_INTRO = {
 "一": ("这一章是“纯概念 + 一步计算”：定义域、复合、反函数、反三角。题目几乎不设陷阱，"
        "失分主要来自对反三角主值区间的记忆模糊。建议先把 4 类题型各做 3 题，再回看考点 1–5。"),
 "二": ("第二章占题库 76 题，是全卷最重的一章。表面上有 11 类题型，实质只有 4 个动作："
        "代入、约分、有理化、配 $\\dfrac{\\sin u}{u}$。练熟这 4 个动作，本章就是送分。"),
 "三": ("$x\\to\\infty$ 的题有一个统一的判据：<b>看最高次项的较量</b>。有理函数比次数，"
        "含根号的先提 $|x|$，根式差先乘共轭。三类处理完，剩下的只是符号。"),
 "四": ("指数对数的极限只有“底数与 1 的大小”一个问题；$1^\\infty$ 型只有“凑 $(1+u)^{1/u}$”一个动作。"
        "这一章的题看似长，实际两行就能出答案。"),
 "五": ("连续性是概念题与证明题的交界。求 $L$、分类间断点属于计算，零点定理属于证明——"
        "两类题的答题格式完全不同，别混用。"),
 "六": ("导数这一章的核心不是背公式，而是<b>认结构</b>：看到什么形状，就知道用哪条法则。"
        "幂、乘积、商、复合四种结构，决定了 90% 的题。"),
 "七": ("这一章的题有固定的“外壳”：指对求导、反三角求导、幂指函数、隐函数。"
        "每类都有稳定的四步流程，照着做不会错。"),
 "八": ("相关变化率题量最少（5 题），但几乎每次都有大题。它考的不是计算，而是"
        "“先求导、后代入”的纪律和画图建模的能力。"),
 "附": ("这一章属于 Lecture 1–6 之外的 Ch4 内容，<b>期中不考</b>。整理在此是为了让你在题库里"
        "遇到时不被吓到，也为期末留个入口。若时间紧张，只需读完题型特征即可。"),
}


def tc(tid, k=2):
    t = TYPES[tid]
    shape, variant = EXTRA[tid]
    body = J([
        "<div class='lbl'>题干长什么样</div><p style='margin:0 0 2.5mm'>" + shape + "</p>",
        "<div class='lbl'>解题模板</div>", steps_html(t["steps"]),
        "<div style='margin-top:3mm'></div>",
        tip("warn", "易错", t["trap"]),
        ex_free(tid, k),
        tip("link", "变形", variant),
    ])
    meta = "题库 %d 题 · 精练 %d 题 · %s" % (t["bank"], len(BY_TYPE[tid]), STAR[t["diff"]])
    return ("<div class='tc'><div class='tc-h'><span class='tc-n'>%s</span>"
            "<span class='tc-t'>%s</span><span class='tc-m'>%s</span></div>"
            "<div class='tc-b'>%s</div></div>" % (tid, t["name"], meta, body))


S = []

S.append(cover(
    "XJTLU · MTH026 Calculus I",
    "题库分类<br>精解",
    "Practice Quiz 351 题 · 49 类题型 · v2",
    "从“按考点罗列”升级为“按题型给模板”",
    ["9 章", "49 类题型", "模板化步骤", "双例题精解", "原题索引"],
    [("351", "题库唯一题"), ("49", "题型 Question Types"),
     ("98", "精解例题 Worked"), ("40", "超纲题（附章）")],
    "QUESTION-BANK EDITION"))

# 导读
S.append(J([
"""<section class="pb">""", h2("从“题库”到“解法库”"),
"""<p>v1 的《题库分类汇总》解决的是“有哪些题”，v2 解决的是“<b>这类题该怎么做</b>”。351 道唯一题被归并成 49 类题型，每一类给一张卡片：题干特征、四步模板、两道精解例题、一个陷阱、一个变形方向。掌握 49 张卡片，等于掌握了整个题库。</p>""",
"""<div class="two-col"><div>""", h3("三遍刷题法"),
bullets([
    "<b>第一遍（认类型）</b>：只做每类题型的第 1 题，做完立刻看模板。目标是“看到题干能报出题型编号”，不求快。",
    "<b>第二遍（练模板）</b>：按模板独立完成每类 2–3 题，卡住时只回看模板，不看解析。",
    "<b>第三遍（查漏洞）</b>：只做错题与“题库题量 ≥ 10”的高频题型，限时完成。"]),
"""</div><div>""", h3("四类动作，覆盖全卷"),
table(["动作", "适用题型", "占比"],
      [["代入 / 直接计算", "T1.1–T1.4、T2.6、T4.1–T4.5、T6.1–T6.7", "约 34%"],
       ["恒等变形后约分", "T2.3、T2.5、T2.8、T5.5、T7.4", "约 15%"],
       ["配标准极限", "T2.10、T2.11、T4.3、T4.4", "约 15%"],
       ["公式套用（求导/隐函数）", "T6.4–T8.1", "约 36%"]],
      compact=True, widths=["40mm", "auto", "16mm"]),
"""</div></div>""",
tip("how", "和 v1 的差别", "v1 每道题只给答案；v2 每类题型给可复用的模板，并把答案放在例题解析里，做题时可先遮住解析自测。两册 PDF 与刷题器使用同一套题型编号，可互相跳转。"),
h3("题型总表"),
"""<p class="small">下表是本册的完整目录：49 类题型、所在讲次、题库题量与难度。带“附”标记的属于六讲之外的 Ch4 内容。</p>""",
]))
_rows = []
for t in DATA["types"]:
    _rows.append([t["id"], t["name"], "L%d" % t["lec"] if t["lec"] != 9 else "附",
                  "§" + t["sec"], str(t["bank"]), STAR[t["diff"]]])
S.append(table(["编号", "题型", "讲次", "小节", "题库", "难度"], _rows, compact=True,
               widths=["16mm", "auto", "16mm", "20mm", "16mm", "20mm"]) + "</section>")

# 各章
for num, name, lec, sec, tids in DATA["chapters"]:
    amber = (num == "附")
    head_txt = ("Chapter %s｜%d 类题型" % (sec, len(tids)))
    S.append(J([
        chapter(num, name, head_txt,
                ("题库第%s章 · 共 %d 题 · 六讲范围外，期中不考" % (num, sum(TYPES[t]["bank"] for t in tids)))
                if amber else
                ("题库第%s章 · 共 %d 题 · 课件锚点 Ch%s" % (num, sum(TYPES[t]["bank"] for t in tids), sec)),
                amber=amber),
        """<p style="margin:2mm 0 4mm">""" + CH_INTRO[num] + "</p>",
    ] + [tc(t, 2 if TYPES[t]["bank"] >= 10 else 2) for t in tids]))

# 附录
S.append(J([
"""<section class="chapter">""", h2("附录　解题动作速查"),
"""<p class="small">考前最后一页：把“题干信号”直接映射到“第一个动作”。看到信号就动手，不要在原地想方法。</p>""",
table(["题干里的信号", "第一个动作", "对应题型"],
      [["log / ln 求定义域", "写真数 > 0，解不等式", "T1.1"],
       ["f、g 给两个函数问复合", "先写内层限制，再套外层", "T1.2"],
       ["问 f⁻¹ 或 (f⁻¹)′", "解出 x 或用 1/f′(x₀)", "T1.3、T7.2"],
       ["arcsin/arccos 求值", "落主值区间 → 画直角三角形", "T1.4"],
       ["分段函数求极限", "分别算左右，比较是否相等", "T2.1–T2.3"],
       ["含 $|x-a|$ 的分式", "去绝对值，左右符号相反", "T2.3"],
       ["代入得 0/0", "先试因式分解 → 再试有理化 → 再试等价替换", "T2.5、T2.8、T5.5"],
       ["含 $\\sqrt A-\\sqrt B$", "乘共轭有理化", "T2.8、T3.3"],
       ["$\\sin(ax)/bx$ 型", "配系数凑 1", "T2.10"],
       ["$\\sin(1/x)$、$\\cos(1/x)$", "夹逼（有界×无穷小）", "T2.11"],
       ["$x\\to\\infty$ 有理式", "比次数（或同除最高次）", "T3.1"],
       ["$x\\to-\\infty$ 含 $\\sqrt{x^2}$", "先写 $|x|=-x$", "T3.2"],
       ["问渐近线", "先水平（比次数）后垂直（分母零点）", "T3.5"],
       ["底趋于 1、指数趋于 ∞", "凑 $(1+u)^{1/u}$，答案 $e^{\\lim u\\cdot\\text{指数}}$", "T4.3"],
       ["含 $e^{ax}-1$ 或 $\\ln(1+bx)$", "换 $u$ 配系数", "T4.4"],
       ["本金利率计息", "写 $A_0(1+r/n)^{nt}$ 或 $A_0e^{rt}$", "T4.5"],
       ["问如何定义才连续", "求该点极限，令其等于函数值", "T5.1"],
       ["问间断点类型", "先算极限，存在即“可去”", "T5.2"],
       ["证明方程有根", "构造 $f$，验连续 + 端点异号", "T5.4"],
       ["给点求切线", "先 $f'(c)$ 再点斜式", "T6.1–T6.3、T7.6"],
       ["复杂复合函数求导", "由外向内逐层乘", "T6.5"],
       ["求 $f^{(n)}$", "先求 2–3 阶找规律", "T6.6"],
       ["含 $x$ 在指数与底", "取对数再求导", "T7.4"],
       ["隐式方程求 $dy/dx$", "含 $y$ 的项乘 $y'$", "T7.5"],
       ["两个量同时变化", "列方程 → 对 $t$ 求导 → 代瞬时值", "T8.1"],
       ["闭区间求最值", "临界点 + 端点比较", "T9.2"],
       ["判断实根个数", "单调区间 + 极值符号", "T9.5"]],
      compact=True, widths=["auto", "auto", "34mm"]),
tip("warn", "最后提醒", "所有模板都建立在“<b>先判断类型、再动笔计算</b>”之上。考场上的时间损失，八成不是因为算不出来，而是因为没认出题型就硬算。"),
"""</section>""",
]))

html = pdfkit.assemble(S, TITLE)
hp = os.path.join(OUT, "pdf_b.html")
open(hp, "w", encoding="utf-8").write(html)
raw = os.path.join(OUT, "_b_raw.pdf")
print_pdf(hp, raw)
final = os.path.join(OUT, "MTH026_题库分类精解_v2.pdf")
pdfkit.stamp(raw, final, "MTH026 Calculus I · 题库分类精解 v2", "XJTLU · 49 类题型")
import pypdf
print("页数:", len(pypdf.PdfReader(final).pages), "→", final)
