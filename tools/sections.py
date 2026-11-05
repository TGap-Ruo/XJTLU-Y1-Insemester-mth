# -*- coding: utf-8 -*-
"""章节模型（54 小节，中英名称 + 题数）"""
CHAPTERS = [
    ("一", "Functions and Preliminaries", "函数与预备知识", [
        ("1.1", "Natural Domain of a Logarithmic Function", "对数函数的自然定义域", 10),
        ("1.2", "Evaluating Composite Functions", "复合函数求值", 10),
        ("1.3", "Inverse Function and Its Domain", "反函数及其定义域", 5),
        ("1.4a", "Principal Values of Inverse Trig (same function)", "反三角化主值（同函数）", 15),
        ("1.4b", "Converting Between Inverse Trig Functions", "反三角互化（异函数）", 5),
        ("1.4c", "Nested Inverse Trigonometric Evaluation", "反三角嵌套代数求值", 5),
    ]),
    ("二", "Limits: Concept and Evaluation", "极限的概念与计算", [
        ("2.1", "Limit of a Piecewise Function at a Point", "分段函数在某点的极限", 5),
        ("2.2", "One-Sided Limits of Piecewise Functions", "分段函数的左右极限", 5),
        ("2.3", "Limits Involving Absolute Value", "含绝对值的极限", 5),
        ("2.4", "Oscillation and Non-Existent Limits", "振荡函数与极限不存在", 5),
        ("2.5", "0/0 Form: Factoring and Cancelling", "0/0 型：因式分解约简", 10),
        ("2.6", "Direct Substitution for Continuous Functions", "连续函数直接代入", 5),
        ("2.7", "Algebra of Known Limits", "已知极限的四则组合", 5),
        ("2.8", "0/0 Form: Rationalising", "0/0 型：根式有理化", 5),
        ("2.9", "One-Sided Infinite Limits", "单侧无穷极限", 1),
        ("2.10", "Trigonometric Limits", "三角函数极限", 28),
        ("2.11", "Squeeze Theorem (bounded × infinitesimal)", "夹逼定理（有界乘无穷小）", 2),
    ]),
    ("三", "Limits at Infinity, Sequences and Asymptotes", "无穷远极限、数列与渐近线", [
        ("3.1", "Limits at Infinity of Rational Functions", "有理函数的无穷远极限", 10),
        ("3.2", "Limits at Infinity with Radicals", "含根号的无穷远极限", 5),
        ("3.3", "Radical Differences at Infinity", "根式差的无穷远极限", 5),
        ("3.4", "Limits of Sequences", "数列极限", 5),
        ("3.5", "Horizontal and Vertical Asymptotes", "水平与垂直渐近线", 5),
    ]),
    ("四", "Exponential and Logarithmic Limits, e and Compounding", "指数对数极限、数 e 与复利", [
        ("4.1", "Limits of Exponential Functions", "指数函数极限", 9),
        ("4.2", "Limits of Logarithmic Functions", "对数函数极限", 5),
        ("4.3", "Sign of a Logarithmic Quotient", "含对数分式的符号判断", 1),
        ("4.4", "Indeterminate Forms Involving e", "含 e 的未定式", 5),
        ("4.5", "(e^u-1)/u and ln(1+u)/u", "(e^u-1)/u 与 ln(1+u)/u 重要极限", 5),
        ("4.6", "Compound Interest Models", "复利模型", 5),
    ]),
    ("五", "Continuity", "连续性", [
        ("5.1", "Choosing L to Make f Continuous", "求 L 使函数在点连续", 5),
        ("5.2", "Classifying Discontinuities", "间断点识别与分类", 10),
        ("5.3", "Parameters for Piecewise Continuity", "分段函数求参数使连续", 5),
        ("5.4", "Continuity versus Limit", "连续与极限关系判断", 5),
        ("5.5", "IVT and Zeros", "零点定理 / 介值定理", 5),
    ]),
    ("六", "Derivatives: Concept and Basic Rules", "导数概念与基本求导", [
        ("6.1", "Slope of a Tangent Line", "切线斜率", 5),
        ("6.2", "Derivative at a Point", "某点的导数", 5),
        ("6.3", "Equation of a Tangent Line", "切线方程", 5),
        ("6.4", "Basic Differentiation (power, trig, algebra)", "基本求导（幂/三角/四则）", 10),
        ("6.5", "Chain Rule", "链式法则", 10),
        ("6.6", "Higher-Order Derivatives", "高阶导数", 10),
        ("6.7", "Kinematics: Velocity and Acceleration", "运动学：速度与加速度", 5),
    ]),
    ("七", "Derivatives of Exp, Log, Inverse Trig and Implicit", "指对、反三角与隐函数求导", [
        ("7.1", "Differentiating Exponential and Logarithmic Functions", "指数与对数求导", 16),
        ("7.2", "Derivative of an Inverse Function", "反函数求导", 5),
        ("7.3", "Derivatives of Inverse Trigonometric Functions", "反三角函数求导", 5),
        ("7.4", "Logarithmic Differentiation", "对数求导法（幂指函数）", 4),
        ("7.5", "Implicit Differentiation", "隐函数求导", 5),
        ("7.6", "Tangent Line from an Implicit Curve", "隐函数的切线方程", 5),
    ]),
    ("八", "Related Rates", "相关变化率", [
        ("8.1", "Rising Balloon (right triangle)", "气球上升（直角三角形）", 2),
        ("8.2", "Conical Tank", "圆锥水箱", 2),
        ("8.3", "Boat and Telescope (angle)", "船与望远镜（角度变化）", 1),
    ]),
    ("九", "Applications of Derivatives", "导数的应用", [
        ("9.1", "Critical and Singular Points", "驻点与奇点", 5),
        ("9.2", "Extrema on a Closed Interval", "闭区间最值", 15),
        ("9.3", "Intervals of Increase and Decrease", "单调区间", 5),
        ("9.4", "Concavity and Inflection Points", "凹凸区间与拐点", 10),
        ("9.5", "Number of Real Roots", "实根个数判断", 5),
    ]),
]

# 展平：sections[i] = dict(id, en, zh, n, chapter_index, start, end)
SECTIONS = []
_q = 1
for ci, (num, c_en, c_zh, secs) in enumerate(CHAPTERS):
    for sid, en, zh, n in secs:
        SECTIONS.append({"id": sid, "en": en, "zh": zh, "n": n,
                         "ch": ci, "ch_num": num, "ch_en": c_en, "ch_zh": c_zh,
                         "start": _q, "end": _q + n - 1})
        _q += n
TOTAL = _q - 1
BY_Q = {}
for s in SECTIONS:
    for i in range(s["start"], s["end"] + 1):
        BY_Q[i] = s

if __name__ == "__main__":
    print("小节", len(SECTIONS), "题目", TOTAL)
