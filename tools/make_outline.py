# -*- coding: utf-8 -*-
"""MTH026 期中考点梳理 v3 —— 中文为主，术语英文密集，末尾术语表"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import ROOT, print_pdf
from sections import SECTIONS, CHAPTERS
from method_a import M1
from method_b import M2
from terms import GLOSSARY, SHORT, flat_glossary
from make_qbank import CSS
import pdfkit

M = {**M1, **M2}

# how many of the practice-quiz originals landed in each topic
import collections
_PIT = json.load(open(os.path.join(ROOT, "build", "pitems.json")))
PC = collections.Counter(i["sec"] for i in _PIT)
ZH = {en: zh for en, zh, _n, _c in flat_glossary()}
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "out")

# 每章导语（中文）
CH_INTRO = {
    0: "这一章是「纯概念 + 一步计算」：定义域、复合、反函数、反三角。题目几乎不设陷阱，失分几乎都来自两件事——"
       "反三角主值区间记混，以及把「反函数的值域」当成「反函数的定义域」。先把四类各做三题，再回看本节。",
    1: "第二章是全卷最重的一章（76 题，11 个考点）。表面上有十一类题，实质只有四个动作：代入、约分、有理化、"
       "配 $\\frac{\\sin u}{u}$。认出是哪一类，动作就是固定的。",
    2: "无穷远的题有统一判据——看最高次项的较量。有理函数比次数，含根号的先提 $|x|$，根式差先乘共轭。"
       "三类处理完，剩下的只是符号。",
    3: "指数对数极限只有两个问题：底数与 $1$ 的大小关系，以及 $1^{\\infty}$ 型怎么凑 $(1+u)^{1/u}$。"
       "复利题是同一套东西套上应用题外壳。",
    4: "连续性是「概念题」与「计算题」的交界。求 $L$、分间断点属于计算；零点定理属于证明——"
       "两类题的答题格式完全不同，别混用。",
    5: "导数这一章的核心不是背公式，而是认结构：看到什么形状，就知道用哪条法则。"
       "幂、乘积、商、复合四种结构决定 90% 的题。",
    6: "这一章的题有固定外壳：指对求导、反三角求导、幂指函数、隐函数。每类都有稳定的四步流程，照着做不会错。",
    7: "相关变化率题量最少（5 题），但几乎每次都有大题。它考的不是计算，而是「先列关系式、再对 $t$ 求导、最后代瞬时值」的纪律。",
    8: "导数的应用分两半：前三节是计算（临界点、端点、符号表），后两节是判断题（单调性、凹凸性、根的个数）。"
        "计算题按流程走，判断题靠符号表说话。",
}

# 每个考点的中文易错提示
ZHT = {
    "1.1": "把 $>0$ 写成 $\\ge 0$，或把两根留在区间内。真数为零处函数无定义，端点一律取不到。",
    "1.2": "把 $f\\circ g$ 与 $g\\circ f$ 弄反；忘记先算内层再用外层。",
    "1.3": "只写出反函数表达式，忘了由 $\\sqrt x\\ge0$ 反推定义域。",
    "1.4a": "直接用 $\u03c0$ 的整数倍化角，忘了 $\u03c0$ 的整数倍要落在主值区间内才算数。",
    "1.4b": "用余角关系时符号处理错误，尤其是负角与超出 $\u03c0$ 的角。",
    "1.4c": "画三角形时把邻边与对边搞反；忘记锐角保证符号为正。",
    "2.1": "被该点单独定义的函数值干扰，把 $f(a)$ 当作极限。",
    "2.2": "只算一侧就下结论；两段表达式代错分支。",
    "2.3": "去绝对值时不讨论左右；约分后丢了 $\\pm$ 号。",
    "2.4": "以为有界就能求极限；振荡函数的极限不存在。",
    "2.5": "因式分解错符号；约分后忘记回代。",
    "2.6": "见根号就急着有理化，其实分母非零时直接代入即可。",
    "2.7": "先算根号再乘方，顺序错；忘记开方后取正。",
    "2.8": "乘共轭时只乘分子；约分前忘了分子也要展开。",
    "2.9": "不判断 $x-4$ 的符号方向，$+\\infty$ 与 $-\\infty$ 混淆。",
    "2.10": "等价无穷小用错对象：$1-\\cos u\\sim\\frac{u^2}{2}$ 而不是 $u$；括号外的负号漏掉。",
    "2.11": "把有界量当成无穷小；夹逼需要「有界 × 无穷小」两个条件。",
    "3.1": "次数相同时忘记取首项系数之比；含三角函数项时忘记它被 $x^n$ 压成 $0$。",
    "3.2": "$x\\to-\\infty$ 时忘记 $\\sqrt{x^2}=|x|=-x$，符号整体反了。",
    "3.3": "不乘共轭直接相减；乘共轭后忘记分母也变。",
    "3.4": "把 $n$ 当成连续变量处理；同除 $n$ 时根号内要除 $n^2$。",
    "3.5": "先求水平还是先求垂直搞混；分母零点与分子零点重合时不是渐近线。",
    "4.1": "底数小于 $1$ 时方向没反转；$e^{-\\infty}=0$ 与 $e^{+\\infty}=\\infty$ 写反。",
    "4.2": "$\\ln 0^{+}=-\\infty$ 记成 $0$；真数趋于 $0$ 与趋于 $\\infty$ 混淆。",
    "4.3": "忘记 $\\ln x<0$（$x\\to0^{+}$），导致符号判反。",
    "4.4": "把 $1^{\\infty}$ 当成 $1$；凑 $(1+u)^{1/u}$ 时指数少乘一项。",
    "4.5": "换元后系数没配对；分母的常数倍漏掉。",
    "4.6": "月利率写成年利率；期数 $nt$ 少乘 $n$；连续复利用成离散公式。",
    "5.1": "只让函数值等于极限，忘了先确认极限存在。",
    "5.2": "约分后仍判为「不可去」；把垂直渐近线当成可去间断。",
    "5.3": "只代一个连接点；两个连接点要列两个方程。",
    "5.4": "极限存在但不等于函数值 → 可去；左右极限不等 → 不可去。两类别混。",
    "5.5": "不验证连续性就套零点定理；端点同号时定理不给出结论。",
    "6.1": "求导后忘记代点；把 $f(a)$ 当成斜率。",
    "6.2": "根式求导时内层系数漏乘；负指数化简出错。",
    "6.3": "点斜式化简成一般式时符号错；忘记先算 $y_0$。",
    "6.4": "$\\csc$、$\\sec$、$\\cot$ 的导数符号记错；乘积法则漏项。",
    "6.5": "链式法则只乘一层；内层是 $F(x^2)$ 时漏掉 $2x$。",
    "6.6": "高阶导数逐次求导时系数累积错；三角函数周期没利用。",
    "6.7": "速度是位置的一阶导、加速度是二阶导，弄反。",
    "7.1": "先化简再求导能省一半计算（如 $\\ln\\sqrt{u}=\\frac12\\ln u$），硬算容易错。",
    "7.2": "忘记先解 $f(a)=b$ 找 $a$，直接把 $b$ 代进 $f'$。",
    "7.3": "$\\arccos$ 的导数自带负号，与内层负号相消时容易丢。",
    "7.4": "取对数后忘记乘回 $y$；乘积法则漏一项。",
    "7.5": "含 $y$ 的项求导时忘乘 $y'$；代入点之前就把 $y'$ 解出来。",
    "7.6": "隐函数切线要先求斜率再写点斜式；$\\sqrt y$ 的导数含 $\\frac{1}{2\\sqrt y}$。",
    "8.1": "把「气球高度」当成斜边；漏掉 $D$ 也在随时间变化。",
    "8.2": "相似三角形比例写反；$V=\\frac{\\pi}{3}r^2h$ 里的 $r$ 要换成 $h$ 的函数。",
    "8.3": "角度变化率带负号（船在靠近）；$\\tan\\theta$ 求导后要乘 $\\sec^2\\theta$。",
    "9.1": "只找 $f'=0$，漏掉 $f'$ 不存在的点（奇点）。",
    "9.2": "只比较临界点，漏掉端点；闭区间最值必须两者都算。",
    "9.3": "符号表区间端点开闭写错；把 $f'=0$ 的点当成单调性改变点。",
    "9.4": "拐点要求 $f''$ 变号，仅 $f''=0$ 不够；定义域断点处要单独说明。",
    "9.5": "不先用单调性定个数，直接解方程；区间定位要靠介值定理。",
}

FORMULAS = [
    ("极限与等价无穷小 Limits", [
        (r"\lim_{u\to0}\frac{\sin u}{u}=1", r"\sin u\sim u"),
        (r"\lim_{u\to0}\frac{1-\cos u}{u^{2}}=\frac12", r"1-\cos u\sim\frac{u^{2}}{2}"),
        (r"\lim_{u\to0}\frac{e^{u}-1}{u}=1", r"e^{u}-1\sim u"),
        (r"\lim_{u\to0}\frac{\ln(1+u)}{u}=1", r"\ln(1+u)\sim u"),
        (r"\lim_{u\to0}(1+u)^{1/u}=e", r"(1+u)^{1/u}\to e"),
    ]),
    ("求导法则 Differentiation", [
        (r"(x^{n})'=nx^{n-1}", r"(\sin x)'=\cos x"),
        (r"(\cos x)'=-\sin x", r"(\tan x)'=\sec^{2}x"),
        (r"(\sec x)'=\sec x\tan x", r"(\csc x)'=-\csc x\cot x"),
        (r"(e^{u})'=u'e^{u}", r"(\ln u)'=\frac{u'}{u}"),
        (r"(uv)'=u'v+uv'", r"\left(\frac uv\right)'=\frac{u'v-uv'}{v^{2}}"),
        (r"(\arcsin u)'=\frac{u'}{\sqrt{1-u^{2}}}", r"(\arctan u)'=\frac{u'}{1+u^{2}}"),
        (r"(\arccos u)'=-\frac{u'}{\sqrt{1-u^{2}}}", r"(f^{-1})'(b)=\frac{1}{f'(a)}"),
    ]),
    ("三角值表 Exact values", [
        (r"\sin\frac{\pi}{6}=\frac12", r"\cos\frac{\pi}{6}=\frac{\sqrt3}{2}"),
        (r"\sin\frac{\pi}{4}=\frac{\sqrt2}{2}", r"\tan\frac{\pi}{4}=1"),
        (r"\sin\frac{\pi}{3}=\frac{\sqrt3}{2}", r"\cos\frac{\pi}{3}=\frac12"),
        (r"\sec\frac{\pi}{3}=2", r"\tan\frac{\pi}{3}=\sqrt3"),
    ]),
    ("主值区间 Principal ranges", [
        (r"\arcsin:\ \left[-\frac{\pi}{2},\frac{\pi}{2}\right]", r"\arccos:\ [0,\pi]"),
        (r"\arctan:\ \left(-\frac{\pi}{2},\frac{\pi}{2}\right)", r"\sin(\pi-\theta)=\sin\theta"),
        (r"\cos(2\pi-\theta)=\cos\theta", r"\tan(\theta+\pi)=\tan\theta"),
    ]),
    ("复利 Compounding", [
        (r"A=P\left(1+\frac rn\right)^{nt}", r"A=Pe^{rt}"),
        (r"e^{rt}=2\Rightarrow t=\frac{\ln2}{r}", r"\text{monthly}: n=12"),
    ]),
]


def topic_card(sec):
    m = M[sec["id"]]
    steps = "".join("<li>%s</li>" % s for s in m["steps"])
    kt = SHORT.get(sec["id"], [])
    kts = "".join('<span class="kt">%s%s</span>' % (t, ('<b>' + ZH[t] + '</b>') if t in ZH else "")
                  for t in kt)
    return """
<div class="topic">
  <div class="t-h"><span class="t-id">%s</span>
    <div class="t-t"><b>%s</b><span class="zh">%s</span></div>
    <span class="t-m">Q%d–Q%d · %d 题</span></div>
  <div class="t-b">
    <div class="lbl">考什么 &nbsp;What is tested</div>
    <p class="en">%s</p>
    <p class="zh-note">%s</p>
    <div class="lbl">步骤 &nbsp;Method</div>
    <ol class="steps">%s</ol>
    <div class="trap"><b>易错 &nbsp;COMMON ERROR</b><span class="en">%s</span><span class="zh">%s</span></div>
    <div class="kt-row"><span class="kt-lbl">术语</span>%s</div>
  </div>
</div>""" % (sec["id"], sec["en"], sec["zh"], sec["start"], sec["end"], sec["n"],
             m["focus"], m["zh"], steps, m["trap"], ZHT.get(sec["id"], ""), kts)


def cover():
    return """
<div class="cover"><div class="grid"></div><div class="glow"></div>
<div class="inner">
  <div class="brand">XJTLU &middot; MTH026 Calculus I</div>
  <div class="rule"></div>
  <h1>考点梳理<br><span style="font-size:19pt;font-weight:300;letter-spacing:.02em">Knowledge Map</span></h1>
  <div class="sub">9 章 · 54 个考点 · 674 道题一一对应</div>
  <div class="sub2">中文讲解为主 &middot; 术语首次出现给英文 &middot; 末尾附完整术语表</div>
  <div class="tags"><span class="tag">自然定义域</span><span class="tag">极限 four moves</span>
  <span class="tag">反三角 principal value</span><span class="tag">链式法则 chain rule</span>
  <span class="tag">相关变化率 related rates</span><span class="tag">凹凸性 concavity</span></div>
  <div class="cov-list">
    <div><span>01</span>每个考点一页：考什么、怎么做、错在哪、对应哪几道题</div>
    <div><span>02</span>关键术语中英并列，考试读题不再卡在单词上</div>
    <div><span>03</span>末尾公式速查 + 完整术语表（Terminology）</div>
    <div><span>04</span>与《Complete Question Bank》共用同一套考点编号</div>
  </div>
  <div class="stats">
    <div><b>54</b>考点 topics</div><div><b>674</b>对应题量</div>
    <div><b>9</b>章 chapters</div><div><b>80</b>术语 terms</div>
  </div>
  <div class="foot">STUDY EDITION &middot; FOR PERSONAL REVISION ONLY</div>
</div></div>"""


def front():
    return """
<div class="pb"></div>
<h2 class="major">怎么用这本 &nbsp;<span style="font-size:10pt;color:#6d7c8d;font-weight:400">How to use this book</span></h2>
<p>这本册子只做一件事：把 674 道题背后的 54 个考点讲清楚——其中 351 道来自精编题库，323 道是你三次练习测验里真正抽到的原题。它<b>不重复题目</b>——题目、答案与逐题解析在配套的
《Complete Question Bank》里，两册用同一套编号（1.1–9.5），看到考点编号就能跳到对应题目。</p>

<h3 class="minor">三步走</h3>
<table><thead><tr><th style="width:26mm">阶段</th><th>做什么</th><th style="width:34mm">配合</th></tr></thead><tbody>
<tr><td><b>认考点</b></td><td>读「考什么」与「步骤」，然后只看题库里该考点的第 1 题，试着报出它属于哪个考点。</td><td>题库 Q 起止</td></tr>
<tr><td><b>练动作</b></td><td>按「步骤」独立做该考点的其余题目，卡住时只回看步骤，不看解析。</td><td>题库逐题解析</td></tr>
<tr><td><b>补漏洞</b></td><td>只做错过的题 + 题量 ≥ 10 的高频考点（2.10、7.1、9.2、1.4a 等）。</td><td>题库答案表</td></tr>
</tbody></table>

<div class="note"><b>关于英文 ABOUT THE ENGLISH</b><br>
所有数学术语在<b>首次出现</b>时给出英文，并在末尾的术语表（Terminology）中汇总。原因很直接：
课件、Quiz 与考卷都用英文表述，读题速度往往比计算速度更影响得分。看到
<i>natural domain</i>、<i>indeterminate form</i>、<i>inflection point</i> 这些词，要能立刻反应出中文含义。</div>

<h3 class="minor">题量即优先级</h3>
<p>目录里每个考点后面都标了题量与题号区间（Q = 精编题库，P = 你考过的原题）。题量越大，考场上撞见的
概率越高：2.10 三角极限（51 题）、7.1 指对求导（32 题）、9.2 闭区间最值（30 题）、2.5 约分型 0/0（29 题）
这四个考点加起来就占了全卷约 21%，时间紧就先攻它们。</p>
<div class="note"><b>常见误区 MISCONCEPTION</b><br>
很多人把「题量大」理解成「简单」。恰恰相反：题库里同一考点的题越多，说明命题人在这类结构上反复出题，
而每道题的<b>参数都在变</b>。背答案没有用，要背的是<b>动作</b>——也就是每个考点「步骤」里的那几条。</div>
"""


def toc():
    rows = []
    for num, c_en, c_zh, secs in CHAPTERS:
        rows.append('<div class="toc-row" style="margin-top:3mm;border-bottom:1.6px solid var(--line)">'
                    '<span class="n">第%s章</span><span class="t"><b>%s</b> &nbsp;<span style="color:#6d7c8d;font-weight:400">%s</span></span>'
                    '<span class="s">%d 题%s</span></div>' % (
                        num, c_zh, c_en, sum(s[3] for s in secs),
                        (" + %dP" % sum(PC.get(s[0], 0) for s in secs))
                        if any(PC.get(s[0]) for s in secs) else ""))
        for sid, en, zh, n in secs:
            s = next(x for x in SECTIONS if x["id"] == sid)
            rows.append('<div class="toc-row"><span class="n">%s</span><span class="t">%s &nbsp;<span style="color:#6d7c8d;font-size:8.4pt">%s</span></span>'
                        '<span class="s">Q%d–Q%d · %d%s</span></div>' % (
                            sid, zh, en, s["start"], s["end"], n,
                            (" · +%dP" % PC[sid]) if PC.get(sid) else ""))
    return '<div class="pb"></div><h2 class="major">目录 &nbsp;<span style="font-size:10pt;color:#6d7c8d;font-weight:400">Contents</span></h2>' + "".join(rows)


def formulas():
    out = ['<div class="pb"></div><h2 class="major">公式速查 &nbsp;<span style="font-size:10pt;color:#6d7c8d;font-weight:400">Formula sheet</span></h2>',
           '<p>考前最后一页。左边是要用的式子，右边是同价的写法或常用特值。</p>']
    for name, rows in FORMULAS:
        out.append('<h3 class="minor">%s</h3><div class="fbox"><div class="frow">' % name)
        for a, b in rows:
            out.append('<div><span>$%s$</span><span>$%s$</span></div>' % (a, b))
        out.append('</div></div>')
    return "".join(out)


def glossary():
    out = ['<div class="pb"></div><h2 class="major">术语表 &nbsp;<span style="font-size:10pt;color:#6d7c8d;font-weight:400">Terminology</span></h2>',
           '<p>按章排列。<b>先记英文</b>——考卷上是英文；中文用来确认理解。</p>']
    for ch_en, ch_zh, items in GLOSSARY:
        out.append('<h3 class="minor">%s &nbsp;<span style="color:#6d7c8d;font-weight:400">%s</span></h3>' % (ch_zh, ch_en))
        rows = "".join('<tr><td style="width:54mm"><b>%s</b></td><td style="width:30mm" class="zh">%s</td>'
                       '<td class="zh">%s</td></tr>' % (en, zh, note) for en, zh, note in items)
        out.append('<table><tbody>%s</tbody></table>' % rows)
    return "".join(out)


def checklist():
    items = [
        ("log 求定义域", "真数 > 0，解不等式", "natural domain"),
        ("反三角求值", "先化角到主值区间", "principal value"),
        ("分段函数求极限", "左右各算一次", "one-sided limit"),
        ("代入得 0/0", "因式分解 → 有理化 → 等价无穷小", "indeterminate form"),
        ("含 |x-a|", "左右符号相反", "absolute value"),
        ("sin(ax)/bx", "配系数，答案 = 系数比", "sin u / u"),
        ("x→∞ 有理式", "比次数 / 同除最高次", "degree comparison"),
        ("x→-∞ 含 √(x²)", "写成 |x| = -x", "dominant term"),
        ("√A - √B", "乘共轭", "conjugate"),
        ("求渐近线", "先水平后垂直", "asymptote"),
        ("1^∞ 型", "凑 (1+u)^{1/u}，答案 e^{lim u·指数}", "1^∞ form"),
        ("e^u - 1、ln(1+u)", "换元配系数", "equivalent infinitesimal"),
        ("复利", "A=P(1+r/n)^{nt} 或 Pe^{rt}", "compounding"),
        ("求 L 使连续", "令 L = 该点极限", "continuous"),
        ("分间断点", "极限存在 → 可去", "removable"),
        ("证明有根", "连续 + 端点异号", "IVT"),
        ("给点求切线", "先 f'(a)，再点斜式", "tangent line"),
        ("复杂复合求导", "由外向内逐层乘", "chain rule"),
        ("求 f⁽ⁿ⁾", "先求 2–3 阶找规律", "higher-order"),
        ("x 在底与指数", "取对数再求导", "logarithmic differentiation"),
        ("隐式方程 dy/dx", "含 y 的项乘 y'", "implicit"),
        ("两个量同时变", "列式 → 对 t 求导 → 代瞬时值", "related rates"),
        ("闭区间最值", "临界点 + 端点", "closed interval method"),
        ("凹凸与拐点", "f'' 变号才算拐点", "inflection point"),
        ("实根个数", "单调性定个数，介值定位置", "real root"),
    ]
    rows = "".join('<tr><td style="width:44mm"><b>%s</b></td><td>%s</td><td style="width:44mm;color:#2c6ba8">%s</td></tr>'
                   % (a, b, c) for a, b, c in items)
    return ('<div class="pb"></div><h2 class="major">考前 25 条 &nbsp;<span style="font-size:10pt;color:#6d7c8d;font-weight:400">Signal → first move</span></h2>'
            '<p>看到左边的「信号」，立刻做中间那个动作，不要停在原地想方法。</p>'
            '<table><thead><tr><th>题干信号</th><th>第一个动作</th><th>术语 English</th></tr></thead><tbody>'
            + rows + '</tbody></table>')


def build(name="MTH026_KnowledgeMap_v3.pdf"):
    body = [cover(), front(), toc()]

    for ci, (num, c_en, c_zh, secs) in enumerate(CHAPTERS):
        first = [s for s in SECTIONS if s["ch"] == ci][0]
        last = [s for s in SECTIONS if s["ch"] == ci][-1]
        body.append(
            '<div class="chapter"><div class="ch-hero" data-num="%d">'
            '<div class="kicker">CHAPTER %d &nbsp;·&nbsp; %s</div><h2>%s</h2>'
            '<div class="desc">%s questions &middot; %d topics &middot; Q%d–Q%d</div></div></div>'
            % (ci + 1, ci + 1, c_en, c_zh, sum(s[3] for s in secs), len(secs),
               first["start"], last["end"]))
        body.append('<p class="ch-intro">%s</p>' % CH_INTRO[ci])
        for sec in [s for s in SECTIONS if s["ch"] == ci]:
            body.append(topic_card(sec))

    body.append(formulas())
    body.append(glossary())
    body.append(checklist())

    extra = """
.topic{border:1px solid var(--line);border-radius:3px;margin:0 0 5mm;page-break-inside:avoid;}
.t-h{display:flex;align-items:center;gap:3mm;padding:2.4mm 3.4mm;background:linear-gradient(90deg,#eef3fa,#f8fbfe);border-bottom:1px solid var(--line);border-radius:2px 2px 0 0;}
.t-id{font-size:8.4pt;font-weight:700;color:#fff;background:#2c6ba8;padding:1mm 2.4mm;border-radius:2px;}
.t-t{flex:1;line-height:1.28;}
.t-t b{display:block;font-size:11pt;color:#16406e;font-family:"Avenir Next",sans-serif;}
.t-t span{font-size:8.6pt;color:#6d7c8d;}
.t-m{font-size:7.8pt;color:#6d7c8d;white-space:nowrap;}
.t-b{padding:3mm 3.6mm 3mm;}
.lbl{font-size:7.4pt;letter-spacing:.14em;color:#2c6ba8;font-weight:700;text-transform:uppercase;margin:0 0 1.2mm;font-family:"Avenir Next",sans-serif;}
.t-b p{margin:0 0 2mm;}
.t-b p.en{font-size:9.4pt;color:#33404f;}
.t-b p.zh-note{font-size:9.2pt;color:#12171f;}
ol.steps{margin:0 0 2.4mm;padding-left:5mm;font-size:9.2pt;color:#33404f;}
ol.steps li{margin:0.5mm 0;}
.trap{background:#fbf1ef;border-left:2.5px solid #9c3a2e;border-radius:2px;padding:2mm 3mm;margin:1mm 0 2mm;font-size:8.8pt;}
.trap b{display:block;font-size:7.2pt;letter-spacing:.14em;color:#9c3a2e;font-family:"Avenir Next",sans-serif;margin-bottom:0.8mm;}
.trap .en{display:block;color:#33404f;margin-bottom:0.8mm;}
.trap .zh{display:block;color:#12171f;}
.kt-row{border-top:1px dashed var(--line);padding-top:1.8mm;font-size:8.2pt;}
.kt-lbl{font-size:7.2pt;letter-spacing:.16em;color:#6d7c8d;margin-right:2.4mm;font-family:"Avenir Next",sans-serif;}
.kt{display:inline-block;margin:0 3mm 1mm 0;color:#33404f;}
.kt b{color:#2c6ba8;font-weight:600;margin-left:1mm;font-family:"Songti SC",serif;}
.ch-intro{font-size:9.6pt;color:#33404f;margin:0 0 5mm;padding:3mm 4mm;background:#f7f9fc;border-left:3px solid #2c6ba8;border-radius:2px;}
.fbox{border:1px solid var(--line);background:#fafcfe;border-radius:2px;padding:2.6mm 3.4mm;margin:0 0 4mm;page-break-inside:avoid;}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:1mm 5mm;font-size:9.4pt;}
.frow div{display:flex;justify-content:space-between;gap:4mm;padding:0.8mm 0;border-bottom:1px dotted var(--line);}
"""
    html = ('<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<title>MTH026 期中考点梳理 v3</title>'
            '<link rel="stylesheet" href="file://%s/katex.min.css">'
            '<style>%s%s</style></head><body>' % (ASSETS, CSS, extra)
            + "".join(body) +
            '<script src="file://%s/katex.min.js"></script>'
            '<script src="file://%s/auto-render.min.js"></script>'
            '<script>document.addEventListener("DOMContentLoaded",function(){'
            'renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},'
            '{left:"$",right:"$",display:false}],throwOnError:false,strict:false});});</script>'
            '</body></html>' % (ASSETS, ASSETS))
    hp = os.path.join(OUT, "outline.html")
    open(hp, "w", encoding="utf-8").write(html)
    raw = os.path.join(OUT, "_outline_raw.pdf")
    print_pdf(hp, raw)
    final = os.path.join(OUT, name)
    pdfkit.stamp(raw, final, "MTH026 Calculus I · 考点梳理 v3",
                 "54 考点 · 674 题 · 中英术语",
                 foot="MTH026 · 考点梳理 Knowledge Map")
    import pypdf
    print("pages:", len(pypdf.PdfReader(final).pages), "->", final)
    return final


if __name__ == "__main__":
    build()
