# -*- coding: utf-8 -*-
"""Chapter 3-5 (Q127-216) bilingual solutions."""
E = {}


def e(n, en, zh):
    E[n] = (en, zh)


# ---- 3.1 limits at infinity of rational functions ----
e(127, r"The numerator is linear and the denominator quadratic, so the denominator wins: the limit is $0$.",
  r"分子一次、分母二次，分母阶数更高，故极限为 $0$。比次数是最快的判据。")
e(128, r"Linear over quadratic → $0$.",
  r"分子一次、分母二次，极限为 $0$。")
e(129, r"Linear over quadratic → $0$; the sign of the leading coefficient is irrelevant.",
  r"一次除以二次，极限为 $0$，首项系数的正负不影响结论。")
e(130, r"Divide by $x^{2}$: $-2+\frac{2\cos(6x-5)}{x^{2}}\to-2$, since the cosine term is bounded over $x^{2}\to\infty$.",
  r"同除 $x^2$：$-2+\frac{2\cos(6x-5)}{x^2}$，有界量除以 $x^2$ 趋于 $0$，故极限为 $-2$。")
e(131, r"Same degree: the limit is the ratio of leading coefficients $\frac{4}{-2}=-2$.",
  r"同次，取首项系数之比 $\frac{4}{-2}=-2$。")
e(132, r"Split: $\frac{-2x}{x}=-2$, $\frac{\sin(2x+2)}{x}\to0$, $\frac{2}{x}\to0$; total $-2$.",
  r"拆成三项：$\frac{-2x}{x}=-2$，其余两项都有界除以 $x$ 趋于 $0$，故为 $-2$。")
e(133, r"Divide by $x^{3}$: $-2-\frac{3}{x}-\frac{5\sin(2x+6)}{x^{3}}\to-2$.",
  r"同除 $x^3$：$-2-\frac3x-\frac{5\sin(\cdot)}{x^3}$，后两项趋于 $0$，故为 $-2$。")
e(134, r"Divide by $x^{3}$: $1+\frac1x+\frac{6\cos(3x-2)}{x^{3}}\to1$.",
  r"同除 $x^3$ 得 $1+\frac1x+\frac{6\cos(\cdot)}{x^3}\to1$。")
e(135, r"$\frac{-4x^{2}}{x^{2}}=-4$ and the remaining terms vanish; limit $-4$.",
  r"首项之比为 $-4$，其余项趋于 $0$，故为 $-4$。")
e(136, r"Numerator degree $3$ exceeds denominator degree $2$, and the leading coefficient is positive, so the limit is $+\infty$.",
  r"分子三次、分母二次，次数更高且首项为正，故极限为 $+\infty$。")

# ---- 3.2 with radicals ----
e(137, r"For $x\to-\infty$, $\sqrt{16x^{2}-7x+8}\approx4|x|=-4x$. The quotient is $\frac{4x}{-4x}=-1$.",
  r"$x\to-\infty$ 时 $\sqrt{16x^2}\approx4|x|=-4x$，故商为 $\frac{4x}{-4x}=-1$。$|x|=-x$ 是本题唯一考点。")
e(138, r"Same argument: denominator $\approx-4x$, numerator $4x$, so the limit is $-1$.",
  r"分母 $\approx-4x$、分子 $4x$，极限为 $-1$。")
e(139, r"$\sqrt{25x^{2}-8x+3}\approx-5x$ as $x\to-\infty$, and the numerator $\approx-5x$, so the limit is $1$.",
  r"$x\to-\infty$ 时根号 $\approx-5x$，分子 $\approx-5x$，故极限为 $1$。两个负号相消。")
e(140, r"As $x\to+\infty$ the square root $\approx5x$, so $\frac{-5x}{5x}=-1$, which is not among the choices.",
  r"$x\to+\infty$ 时根号 $\approx5x$，商为 $-1$。选项中没有 $-1$，故选\"以上都不对\"。")
e(141, r"At $+\infty$: numerator $\approx2x$, denominator $\approx-2x$, so the limit is $-1$.",
  r"$x\to+\infty$ 时分子 $\approx2x$、分母 $\approx-2x$，故为 $-1$。")

# ---- 3.3 radical differences ----
e(142, r"Multiply by the conjugate: $\frac{(x^{2}-9)-(x^{2}+5x+3)}{\sqrt{x^{2}-9}+\sqrt{x^{2}+5x+3}}\approx\frac{-5x-12}{2x}\to-\frac52$.",
  r"乘共轭后分子为 $-5x-12$，分母 $\approx2x$，故极限为 $-\frac52$。根式差一律先乘共轭。")
e(143, r"Conjugate: $\frac{(9x^{2}-4x-5)-(9x^{2}-x+6)}{6x}=\frac{-3x-11}{6x}\to-\frac12$.",
  r"乘共轭得分子 $-3x-11$，分母 $\approx6x$，极限为 $-\frac12$。")
e(144, r"Conjugate gives $\frac{(16x^{2}+4x+3)-(16x^{2}-3x-9)}{-8x}$ (note the sign for $x\to-\infty$), so $\frac{7x+12}{-8x}\to-\frac78$.",
  r"乘共轭后分子 $7x+12$，而 $x\to-\infty$ 时分母为 $-8x$，故极限 $-\frac78$。负无穷时根号引出的符号要单独处理。")
e(145, r"Conjugate: numerator $3x+6$, denominator $8x$, so the limit is $\frac38$ — not listed.",
  r"共轭后分子 $3x+6$、分母 $8x$，极限 $\frac38$，选项中不存在，故选\"以上都不对\"。")
e(146, r"Conjugate: numerator $(4x^{2}+x+2)-(4x^{2}-5x+2)=6x$, denominator $4x$, so the limit is $\frac32$.",
  r"共轭后分子 $6x$、分母 $4x$，极限 $\frac32$。")

# ---- 3.4 sequences ----
e(147, r"Divide by $n$: numerator $4/n-2\to-2$, denominator $\sqrt{9-9/n-3/n^{2}}\to3$, so the limit is $-\frac23$.",
  r"同除 $n$：分子趋于 $-2$，分母趋于 $3$，故极限 $-\frac23$。数列极限与函数极限同一套做法。")
e(148, r"Divide by $n$: $\frac{4/n-2}{3+3/n}\to-\frac23$.",
  r"同除 $n$ 得 $\frac{4/n-2}{3+3/n}\to-\frac23$。")
e(149, r"Divide by $n$: $\frac{2-2/n}{\sqrt{25+9/n+1/n^{2}}}\to\frac25$.",
  r"同除 $n$：分子趋于 $2$、分母趋于 $5$，得 $\frac25$。")
e(150, r"Divide by $n$: $\frac{6+9/n}{\sqrt{36+6/n+3/n^{2}}}\to\frac66=1$.",
  r"同除 $n$ 得 $\frac{6}{6}=1$。")
e(151, r"Divide by $n$: $\frac{5+6/n}{\sqrt{36-3/n+7/n^{2}}}\to\frac56$.",
  r"同除 $n$ 得 $\frac56$。")

# ---- 3.5 asymptotes ----
e(152, r"Vertical: the denominator vanishes at $x=-\frac45$ while the numerator does not. Horizontal: degree trick gives $y=\frac{-4}{5}$.",
  r"垂直渐近线看分母零点 $x=-\frac45$（分子在此不为零）；水平渐近线取首项系数之比 $-\frac45$。")
e(153, r"Denominator zero at $6-4x=0$, i.e. $x=\frac32$; horizontal asymptote $y=\frac{-5}{-4}=\frac54$.",
  r"分母零点 $x=\frac32$ 给出垂直渐近线；水平渐近线为首项系数比 $\frac54$。")
e(154, r"Denominator $5x=0$ gives $x=0$; horizontal asymptote $y=\frac35$.",
  r"分母零点 $x=0$ 为垂直渐近线；水平渐近线 $y=\frac35$。")
e(155, r"The denominator vanishes at $x=-3$ and $x=-4$; since the numerator is only linear, the horizontal asymptote is $y=0$.",
  r"分母零点 $x=-3,-4$ 给出两条垂直渐近线；分子次数低于分母，水平渐近线为 $y=0$。")
e(156, r"Vertical asymptotes at $x=-5$ and $x=-4$; horizontal $y=0$ because the numerator has lower degree.",
  r"垂直渐近线 $x=-5,-4$；分子次数低，水平渐近线 $y=0$。")

# ---- 4.1 exponential limits ----
e(157, r"$3x+5\to+\infty$, so $2^{3x+5}\to+\infty$.",
  r"指数 $3x+5\to+\infty$，底数 $2>1$，故极限为 $+\infty$。")
e(158, r"As $x\to-\infty$, $4x-6\to-\infty$, so $(1/2)^{4x-6}=(1/2)^{-\infty}=2^{+\infty}=+\infty$.",
  r"$x\to-\infty$ 时 $4x-6\to-\infty$，而底数 $\frac12<1$，故 $(\frac12)^{-\infty}=2^{+\infty}=+\infty$。底数小于 $1$ 时方向反转。")
e(159, r"$2x-4\to+\infty$, hence $e^{2x-4}\to+\infty$ — not one of the listed choices.",
  r"$2x-4\to+\infty$，故 $e^{2x-4}\to+\infty$。选项只给了 $-\infty$，故为\"以上都不对\"。")
e(160, r"Exponent $x-2\to-2$, so $(1/2)^{-2}=4$.",
  r"指数 $x-2\to-2$，故 $(\frac12)^{-2}=4$。负指数就是取倒数再平方。")
e(161, r"$e^{-x}=1/e^{x}\to0$.",
  r"$e^{-x}=\frac{1}{e^{x}}\to0$。")
e(162, r"Divide numerator and denominator by $e^{-x}$: $\frac{1-3e^{x}}{5+e^{x}}\to\frac15$ as $x\to-\infty$.",
  r"分子分母同除 $e^{-x}$，得 $\frac{1-3e^{x}}{5+e^{x}}$；$x\to-\infty$ 时 $e^x\to0$，故极限 $\frac15$。")
e(163, r"Same division: $\frac{5-3e^{x}}{3+e^{x}}\to\frac53$.",
  r"同除 $e^{-x}$ 得 $\frac{5-3e^x}{3+e^x}\to\frac53$。")
e(164, r"At $+\infty$ the $e^{x}$ terms dominate: $\frac{-2-6e^{-x}}{1+5e^{-x}}\to-2$.",
  r"$x\to+\infty$ 时同除 $e^x$，得 $\frac{-2-6e^{-x}}{1+5e^{-x}}\to-2$。")
e(165, r"Division by $e^{x}$ gives $\frac{-2+3e^{-x}}{1+2e^{-x}}\to-2$.",
  r"同除 $e^x$ 得 $\frac{-2+3e^{-x}}{1+2e^{-x}}\to-2$。")

# ---- 4.2 logarithmic limits ----
e(166, r"$8x\to0^{+}$, so $\ln(8x)\to-\infty$.",
  r"$8x\to0^{+}$，故 $\ln(8x)\to-\infty$。对数在 $0$ 右侧趋向负无穷。")
e(167, r"At $x=1$ the argument is $3-3+e^{-2}=e^{-2}$, so the limit is $\ln(e^{-2})=-2$.",
  r"$x=1$ 时真数为 $3-3+e^{-2}=e^{-2}$，故极限为 $\ln e^{-2}=-2$。")
e(168, r"$5x^{3}+1\to+\infty$, so the log tends to $+\infty$.",
  r"真数 $\to+\infty$，对数也 $\to+\infty$。")
e(169, r"$4x^{6}+1\to+\infty$, so $\ln(\cdot)\to+\infty$ — not listed.",
  r"真数 $\to+\infty$，极限为 $+\infty$，选项中未给，故选\"以上都不对\"。")
e(170, r"$4x^{5}\to0^{+}$, so the log tends to $-\infty$.",
  r"$4x^5\to0^{+}$，故对数趋于 $-\infty$。")

# ---- 4.3 sign of a logarithmic quotient ----
e(171, r"Write $\frac{\ln x}{\sqrt{(\ln x)^{2}+4}}=\frac{\ln x}{|\ln x|}\cdot\frac{1}{\sqrt{1+4/(\ln x)^{2}}}$; as $x\to0^{+}$, $\ln x<0$ so the first factor is $-1$ and the second tends to $1$.",
  r"把分母写成 $|\ln x|\sqrt{1+4/(\ln x)^2}$，于是原式 $=\frac{\ln x}{|\ln x|}\cdot\frac{1}{\sqrt{1+4/(\ln x)^2}}$。$x\to0^{+}$ 时 $\ln x<0$，第一因子为 $-1$，故极限为 $-1$。")

# ---- 4.4 1^inf indeterminate forms ----
e(172, r"Base $=1+\frac4x$ and exponent $\approx4x$; $(1+\frac4x)^{4x}\to e^{16}$.",
  r"底数写成 $1+\frac4x$，指数 $\approx4x$；由 $(1+u)^{1/u}\to e$ 得 $e^{4\cdot4}=e^{16}$。")
e(173, r"Base $=1-\frac{1}{x-3}$, exponent $x$; the product (base$-$1)$\cdot$exponent $\to-1$, so the limit is $e^{-1}$.",
  r"底数写成 $1-\frac{1}{x-3}$，指数 $x$；二者乘积（底数减一的差乘指数）趋于 $-1$，故极限 $e^{-1}$。")
e(174, r"With $u=x-4$, base $=1+4u$ and exponent $=\frac{5u+4}{u}=5+\frac4u$; the decisive product is $4u\cdot\frac4u=16$, so the limit is $e^{16}$.",
  r"令 $u=x-4$，底数 $1+4u$，指数 $5+\frac4u$。决定性乘积 $4u\cdot\frac4u=16$，故极限 $e^{16}$。常数项 $5$ 只贡献因子 $1$。")
e(175, r"With $u=x-5$, base $=1-5u$ and exponent $=5-\frac1u$; the product $(-5u)\cdot(-\frac1u)=5$ gives $e^{5}$.",
  r"令 $u=x-5$，底数 $1-5u$，指数 $5-\frac1u$；乘积 $(-5u)(-\frac1u)=5$，故极限 $e^{5}$。")
e(176, r"Base $x=1+u$ and exponent $\frac{6x-5}{x-1}=6+\frac1u$; the governing product is $u\cdot\frac1u=1$, so the limit is $e$.",
  r"令 $u=x-1$，底数 $1+u$，指数 $6+\frac1u$；关键乘积 $u\cdot\frac1u=1$，故极限为 $e$。")

# ---- 4.5 (e^u-1)/u and ln(1+u)/u ----
e(177, r"Near $x=-4$, $5x+21=1+5(x+4)$ so $\ln(5x+21)\approx5(x+4)$, and the denominator is $7(x+4)$; the limit is $\frac57$.",
  r"$5x+21=1+5(x+4)$，用 $\ln(1+u)\sim u$ 得分子 $\approx5(x+4)$；分母 $7(x+4)$，故极限 $\frac57$。")
e(178, r"With $u=-x-4\to0$, the expression is exactly $\frac{e^{u}-1}{u}\to1$ — not among the options.",
  r"令 $u=-x-4\to0$，原式恰为 $\frac{e^u-1}{u}\to1$。选项中没有 $1$，故选\"以上都不对\"。")
e(179, r"$-3x-11=1-3(x+4)$, so the numerator is $\approx-3(x+4)$ and the limit is $-\frac35$.",
  r"$-3x-11=1-3(x+4)$，分子 $\approx-3(x+4)$，除以 $5(x+4)$ 得 $-\frac35$。")
e(180, r"With $u=-x-4$, the denominator is $6u$, so the limit is $\frac16$ — not listed.",
  r"令 $u=-x-4$，分母为 $6u$，极限为 $\frac16$，选项中未给。")
e(181, r"$7x+28=7(x+4)$, so numerator $\approx7(x+4)$ over $-(x+4)$ gives $-7$.",
  r"$7x+28=7(x+4)$，分子 $\approx7(x+4)$，分母 $-(x+4)$，故极限 $-7$。")

# ---- 4.6 compound interest ----
e(182, r"Monthly compounding: $A=P(1+\frac{r}{12})^{12t}=4400(1+\frac{1}{600})^{96}$.",
  r"按月复利 $A=P(1+\frac{r}{12})^{12t}$，代入 $r=\frac{1}{50}$、$t=8$ 得 $4400(1+\frac{1}{600})^{96}$。$12t=96$ 别写成 $8$。")
e(183, r"Continuous compounding doubles the money when $e^{rt}=2$, i.e. $t=\frac{\ln2}{r}=\frac{100\ln2}{7}$, which none of the options states.",
  r"连续复利下翻倍即 $e^{rt}=2$，解得 $t=\frac{\ln2}{r}=\frac{100\ln2}{7}$。选项 C 写成了 $\frac{100}{7\ln2}$，倒数关系不对，故选\"以上都不对\"。")
e(184, r"$A=1500(1+\frac{1}{240})^{84}$ since $\frac{0.05}{12}=\frac{1}{240}$ and $12\cdot7=84$.",
  r"$\frac{0.05}{12}=\frac{1}{240}$，$12\cdot7=84$，故 $A=1500(1+\frac{1}{240})^{84}$。")
e(185, r"Continuous: $A=3400e^{0.08\cdot8}=3400e^{16/25}$.",
  r"连续复利 $A=Pe^{rt}=3400e^{0.64}=3400e^{16/25}$。指数是 $rt$ 的乘积，不是 $r+t$。")
e(186, r"$4900(1+\frac{7}{1200})^{36}$: monthly rate $\frac{0.07}{12}=\frac{7}{1200}$, and $12\cdot3=36$.",
  r"月利率 $\frac{0.07}{12}=\frac{7}{1200}$，期数 $36$，故 $4900(1+\frac{7}{1200})^{36}$。")

# ---- 5.1 choosing L for continuity ----
e(187, r"Continuity needs $L=\lim_{x\to-2}\frac{3x^{2}+4x-4}{x+2}$; the numerator is $(3x-2)(x+2)$, so $L=3(-2)-2=-8$.",
  r"连续要求 $L$ 等于该点极限。分子分解为 $(3x-2)(x+2)$，约分后代入得 $L=-8$。")
e(188, r"$\frac{x^{2}+2x-8}{x+4}=(x-2)$, so $L=-4-2=-6$.",
  r"分子 $=(x+4)(x-2)$，约分后为 $x-2$，代入 $x=-4$ 得 $L=-6$。")
e(189, r"$\frac{x^{2}-x-20}{x+4}=x-5$, so $L=-9$.",
  r"分子 $=(x-5)(x+4)$，约分后为 $x-5$，故 $L=-9$。")
e(190, r"Near $x=-2$ the quotient behaves like $\frac{8(x+2)}{6(x+2)}=\frac43$, so $L=\frac43$.",
  r"$x\to-2$ 时分子 $\sin(8(x+2))\sim8(x+2)$，分母 $6(x+2)$，故 $L=\frac43$。用等价无穷小代替 $\sin$。")
e(191, r"$3x^{2}+3x-6=3(x+2)(x-1)$, so $L=3(-3)=-9$.",
  r"分子 $=3(x+2)(x-1)$，约去 $x+2$ 后代入得 $L=-9$。")

# ---- 5.2 classifying discontinuities ----
e(192, r"Left limit $-(-3)-5=-2$, right limit $-3+1=-2$: continuous. Slopes are $-1$ and $1$, so there is a corner — continuous but not differentiable.",
  r"左右极限都是 $-2$，故连续；两侧斜率 $-1$ 与 $1$ 不等，故不可导，是尖点。")
e(193, r"Both branches give $-5$ at $x=-2$, and the one-sided slopes are $3$ and $-2x-1=3$ — equal, so $f$ is differentiable there.",
  r"两支在 $x=-2$ 都取 $-5$，且左右导数都是 $3$，故在该点可导。连续且左右导数相等才算可导。")
e(194, r"Both branches give $-3$, so it is continuous; the slopes $-1$ and $1$ differ, so it is not differentiable.",
  r"两支都取 $-3$，连续；但左右导数 $-1$ 与 $1$ 不等，故不可导。")
e(195, r"Left limit $-2$, right limit $2(-3)+4=-2$: continuous; slopes $-1$ versus $2$, so not differentiable.",
  r"左右极限同为 $-2$，连续；斜率分别为 $-1$ 与 $2$，故不可导。")
e(196, r"At $x=-3$ both branches give $-1$, so $f$ is continuous; but the one-sided slopes are $2$ and $-1$, so it is not differentiable.",
  r"两支在 $x=-3$ 都取 $-1$，连续；两侧斜率 $2$ 与 $-1$ 不等，故不可导。")
e(197, r"The numerator is $4(x-7)(x-2)$, so the factor $x-7$ cancels: the limit exists, hence a removable discontinuity at $x=7$.",
  r"分子 $=4(x-7)(x-2)$，$x-7$ 可约去，极限存在，故 $x=7$ 是可去间断点。")
e(198, r"Denominator $(x+6)(x+1)$; neither factor cancels with the constant numerator, so both discontinuities are non-removable (vertical asymptotes).",
  r"分母 $(x+6)(x+1)$，分子为常数无法约分，两个都是不可去间断点（垂直渐近线）。")
e(199, r"$\frac{(x-5)(x-8)}{x(x-8)}$: the $x=8$ factor cancels (removable), $x=0$ remains as a vertical asymptote (non-removable).",
  r"约去 $x-8$ 后 $x=8$ 可去；$x=0$ 无法约去，是不可去的垂直渐近线。")
e(200, r"$\frac{(x-7)(x+4)}{(x-1)(x-7)}$: $x=7$ cancels (removable), $x=1$ does not (non-removable).",
  r"分子分母都有 $x-7$，故 $x=7$ 可去；$x=1$ 不可约，属不可去间断。")
e(201, r"The numerator is $4(x+8)(x+6)$, so $x+8$ cancels and the only discontinuity at $x=-8$ is removable.",
  r"分子 $=4(x+8)(x+6)$，$x+8$ 可约，故 $x=-8$ 为可去间断点。")

# ---- 5.3 parameters for piecewise continuity ----
e(202, r"Match the two branches at $x=-1$: $7(-1)+3=-4$ and $5(-1)+q=q-5$, so $q=1$.",
  r"令两支在 $x=-1$ 相等：左边 $-4$，右边 $q-5$，得 $q=1$。")
e(203, r"$9(1)-2=7$ and $6+q=7$, so $q=1$.",
  r"左支 $7$，右支 $6+q$，令其相等得 $q=1$。")
e(204, r"$4(2)-1=7$ and $2(2)+q=4+q$, so $q=3$.",
  r"左支 $7$、右支 $4+q$，得 $q=3$。")
e(205, r"$5(1)-1=4$ and $4+q=4$, so $q=0$.",
  r"左支 $4$、右支 $4+q$，故 $q=0$。")
e(206, r"At $x=1$: $2(1)-3=-1=u+v$. At $x=4$: $3(4)-10=2=4u+v$. Subtracting gives $3u=3$, so $u=1$, $v=-2$.",
  r"两个连接点各列一方程：$u+v=-1$ 与 $4u+v=2$；两式相减得 $u=1$，回代 $v=-2$。两个未知数需要两个条件。")

# ---- 5.4 continuity versus limit ----
e(207, r"The one-sided limits are $-4$ and $4$: they differ, so the two-sided limit fails — a non-removable (jump) discontinuity.",
  r"左右极限 $-4$ 与 $4$ 不等，双侧极限不存在，属不可去的跳跃间断。")
e(208, r"The limit exists ($4$) but differs from the function value ($5$), so the discontinuity is removable.",
  r"极限存在（$4$）但不等于函数值（$5$），故为可去间断。")
e(209, r"Limit $-2$, value $-1$: they differ, hence a removable discontinuity.",
  r"极限 $-2$、函数值 $-1$，二者不等，是可去间断。")
e(210, r"Limit $4$, value $5$: removable.",
  r"极限 $4$、函数值 $5$，为可去间断。")
e(211, r"Left $-1$, right $1$: different, so the limit does not exist — non-removable.",
  r"左右极限 $-1$ 与 $1$ 不等，极限不存在，属不可去间断。")

# ---- 5.5 IVT ----
e(212, r"$f(1)=\ln\frac25<0$ and $f(\frac72)=\ln\frac75>0$; $f$ is continuous on the interval, so by the Intermediate Value Theorem it has at least one zero.",
  r"端点值 $\ln\frac25<0$ 与 $\ln\frac75>0$ 异号，且 $\ln$ 在区间上连续，由零点定理至少有一个零点。先验连续、再验异号。")
e(213, r"$f(0)=-1<0$ and $f(2)=29>0$, continuous → at least one root.",
  r"$f(0)=-1<0$、$f(2)=29>0$，连续，故由零点定理至少一根。")
e(214, r"$f$ jumps from $-3$ to $3$ at $x=0$, so it is not continuous on $[-3,3]$ and the theorem does not apply.",
  r"$f$ 在 $x=0$ 处从 $-3$ 跳到 $3$，在闭区间上不连续，零点定理的前提不满足，故不能应用。")
e(215, r"$f(0)=-2<0$ and $f(2)=2(4)+4-2=10>0$, continuous → at least one root.",
  r"$f(0)=-2<0$、$f(2)=10>0$，连续，故至少一根。")
e(216, r"The function has a vertical asymptote at $x=0$, so it is not continuous on $[-49,49]$; the theorem cannot be applied.",
  r"函数在 $x=0$ 处有垂直渐近线，在 $[-49,49]$ 上不连续，零点定理不适用。")
