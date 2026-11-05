# -*- coding: utf-8 -*-
"""Chapter 6-9 (Q217-351) bilingual solutions."""
E = {}


def e(n, en, zh):
    E[n] = (en, zh)


# ---- 6.1 slope of the tangent ----
e(217, r"$f'(x)=2x+3$, so the slope at $x=-3$ is $2(-3)+3=-3$.",
  r"先求导 $f'(x)=2x+3$，代入 $x=-3$ 得斜率 $-3$。切线斜率就是该点导数。")
e(218, r"$f'(x)=-3x^{2}-8x-3$; at $x=-3$: $-27+24-3=-6$.",
  r"$f'(x)=-3x^2-8x-3$，代入 $x=-3$ 得 $-6$。三项分别计算，注意负号。")
e(219, r"$f'(x)=-3x^{2}-12x-4$, so the slope is $-27+36-4=5$, which is not among the choices.",
  r"$f'(x)=-3x^2-12x-4$，代入得 $5$。选项中没有 $5$，故选\"以上都不对\"。")
e(220, r"$f'(x)=-3x^{2}-8x+3$; at $-3$: $-27+24+3=0$, a horizontal tangent.",
  r"$f'(x)=-3x^2-8x+3$，代入得 $0$，即切线水平。导数为零不代表没有切线。")
e(221, r"$f'(x)=-3x^{2}-10x-3$; at $-3$: $-27+30-3=0$, not listed.",
  r"$f'(x)=-3x^2-10x-3$，代入得 $0$，选项中无此值，故选\"以上都不对\"。")

# ---- 6.2 derivative at a point ----
e(222, r"$f(x)=-4(3x)^{-1/2}$, so $f'(x)=6(3x)^{-3/2}$. At $x=27$, $3x=81$ and $81^{3/2}=729$, giving $\frac{6}{729}=\frac{2}{243}$.",
  r"写成 $f=-4(3x)^{-1/2}$，求导得 $6(3x)^{-3/2}$。$x=27$ 时 $3x=81$，$81^{3/2}=729$，故为 $\frac{6}{729}=\frac{2}{243}$。内层 $3x$ 的系数 $3$ 不能漏。")
e(223, r"$f=3\sqrt2\,x^{1/2}$, so $f'(x)=\frac{3\sqrt2}{2}x^{-1/2}$; at $x=2$ this is $\frac{3\sqrt2}{2\sqrt2}=\frac32$, which is not listed (only $-\frac32$).",
  r"$f=3\sqrt2\,x^{1/2}$，$f'=\frac{3\sqrt2}{2\sqrt2}=\frac32$。选项只给了 $-\frac32$，故选\"以上都不对\"。")
e(224, r"$f=2(7x)^{-1/2}\Rightarrow f'=-7(7x)^{-3/2}$; at $x=28$, $7x=196$, $196^{3/2}=2744$, so $-\frac{7}{2744}=-\frac{1}{392}$.",
  r"$f=2(7x)^{-1/2}$，$f'=-7(7x)^{-3/2}$。$x=28$ 时 $7x=196$，$196^{3/2}=2744$，得 $-\frac{1}{392}$。")
e(225, r"$f=-(5x)^{-1/2}\Rightarrow f'=\frac52(5x)^{-3/2}$; at $x=5$, $25^{3/2}=125$, so $\frac{5/2}{125}=\frac{1}{50}$.",
  r"$f=-(5x)^{-1/2}$，$f'=\frac52(5x)^{-3/2}$；$25^{3/2}=125$，得 $\frac{1}{50}$。")
e(226, r"$f=-4(6x)^{-1/2}\Rightarrow f'=12(6x)^{-3/2}$; at $x=24$, $144^{3/2}=1728$, so $\frac{12}{1728}=\frac{1}{144}$.",
  r"$f=-4(6x)^{-1/2}$，$f'=12(6x)^{-3/2}$；$144^{3/2}=1728$，得 $\frac{1}{144}$。")

# ---- 6.3 equation of the tangent line ----
e(227, r"$y'=-\frac{12x}{(x^{2}+8)^{2}}$, so at $x=-1$ the slope is $\frac{12}{81}=\frac{4}{27}$. Then $y-\frac23=\frac{4}{27}(x+1)$ rearranges to $4x-27y+22=0$.",
  r"$y'=-\frac{12x}{(x^2+8)^2}$，在 $x=-1$ 处斜率 $\frac{4}{27}$。点斜式化简得 $4x-27y+22=0$。")
e(228, r"$y'=\frac{6x}{(x^{2}+4)^{2}}$, slope at $-1$ is $-\frac{6}{25}$, and $y+\frac35=-\frac{6}{25}(x+1)$ gives $6x+25y+21=0$.",
  r"$y'=\frac{6x}{(x^2+4)^2}$，斜率 $-\frac{6}{25}$；化简得 $6x+25y+21=0$。")
e(229, r"$y'=-\frac{22x}{(x^{2}+10)^{2}}$, slope at $-1$ is $\frac{2}{11}$; then $y-1=\frac{2}{11}(x+1)$ gives $2x-11y+13=0$.",
  r"$y'=-\frac{22x}{(x^2+10)^2}$，斜率 $\frac{2}{11}$；整理得 $2x-11y+13=0$。")
e(230, r"$y'=\frac{4x}{(x^{2}+1)^{2}}$, slope at $-1$ is $-1$; $y+1=-(x+1)$ gives $x+y+2=0$.",
  r"$y'=\frac{4x}{(x^2+1)^2}$，斜率 $-1$；得 $x+y+2=0$。")
e(231, r"$y'=-\frac{4x}{(x^{2}+1)^{2}}$, slope at $1$ is $-1$; $y-1=-(x-1)$ gives $x+y-2=0$.",
  r"$y'=-\frac{4x}{(x^2+1)^2}$，$x=1$ 处斜率 $-1$；得 $x+y-2=0$。")

# ---- 6.4 basic differentiation ----
e(232, r"$(-7\cos x)'=7\sin x$.",
  r"$\cos$ 的导数是 $-\sin$，负负得正，故为 $7\sin x$。")
e(233, r"$(10\tan x)'=10\sec^{2}x$.",
  r"$\tan$ 的导数为 $\sec^2$，系数保留，得 $10\sec^2x$。")
e(234, r"$(-6\sin x)'=-6\cos x$.",
  r"$\sin$ 的导数为 $\cos$，系数与符号不变，得 $-6\cos x$。")
e(235, r"$(\csc x)'=-\csc x\cot x=-\csc^{2}x\cos x$, which matches none of the listed forms.",
  r"$\csc x$ 的导数为 $-\csc x\cot x=-\csc^2x\cos x$。四个选项都不是这个式子，故选\"以上都不对\"。")
e(236, r"Product rule: $(-2x^{3})'\tan x+(-2x^{3})(\tan x)'=-6x^{2}\tan x-2x^{3}\sec^{2}x$.",
  r"用乘积法则：前导后不导 + 前不导后导，得 $-6x^2\tan x-2x^3\sec^2x$。")
e(237, r"$-\sin x\cos x=-\frac12\sin2x$, whose derivative is $-\cos2x$.",
  r"先化积为和：$-\sin x\cos x=-\frac12\sin2x$，求导得 $-\cos2x$。先化简再求导往往更快。")
e(238, r"$(-3x^{2})'\tan x+(-3x^{2})(\sec^{2}x)=-6x\tan x-3x^{2}\sec^{2}x$.",
  r"乘积法则得 $-6x\tan x-3x^2\sec^2x$。两项都要写全。")
e(239, r"Differentiate termwise: $3\cos x+6\sec x\tan x+4\csc^{2}x$ (the derivative of $-4\cot x$ is $+4\csc^{2}x$).",
  r"逐项求导：$-4\cot x$ 的导数为 $+4\csc^2x$，符号变化是本题唯一难点。")
e(240, r"$3\sin^{4}x+2\sin^{-4}x$ gives $12\sin^{3}x\cos x-8\sin^{-5}x\cos x$.",
  r"用链式法则：$\frac{2}{\sin^4x}=2\sin^{-4}x$，求导得 $-8\sin^{-5}x\cos x$。负指数写法更省事。")
e(241, r"$-\sin^{2}x+\sin^{-2}x$ gives $-2\sin x\cos x-2\cos x\sin^{-3}x$; no option has $\sin^{3}$ in the denominator, so “none of these”.",
  r"求导得 $-2\sin x\cos x-2\cos x\sin^{-3}x$，即分母为 $\sin^3x$。选项 A、B 的幂次或符号都不对，故选\"以上都不对\"。")

# ---- 6.5 chain rule ----
e(242, r"$y=-4[F(x)]^{3}\Rightarrow y'=-12[F(x)]^{2}F'(x)$.",
  r"外层三次、内层 $F$：$y'=-12[F(x)]^2F'(x)$。别忘最后乘 $F'(x)$。")
e(243, r"$2(3x^{2}-5)\cdot6x=12x(3x^{2}-5)=6x(6x^{2}-10)$.",
  r"$2(3x^2-5)\cdot6x=12x(3x^2-5)$，提出公因子写成 $6x(6x^2-10)$ 与选项一致。")
e(244, r"$(\tan u)'=\sec^{2}u\cdot u'$ with $u=x^{2}+5$, giving $2x\sec^{2}(x^{2}+5)=\frac{2x}{\cos^{2}(x^{2}+5)}$.",
  r"$\tan$ 的导数是 $\sec^2u\cdot u'$，$u'=2x$；也可写成 $\frac{2x}{\cos^2(x^2+5)}$。")
e(245, r"$3(-3x^{2}-3)^{2}\cdot(-6x)=-18x(-3x^{2}-3)^{2}$.",
  r"外层三次得 $3(\cdot)^2$，内层导数 $-6x$，合并为 $-18x(-3x^2-3)^2$。")
e(246, r"$8F(x^{2})\Rightarrow y'=8F'(x^{2})\cdot2x=16xF'(x^{2})$.",
  r"$y'=8F'(x^2)\cdot2x=16xF'(x^2)$。$F$ 只是符号，照常写 $F'$。")
e(247, r"$7F(x^{6})\Rightarrow y'=7F'(x^{6})\cdot6x^{5}=42x^{5}F'(x^{6})$.",
  r"内层导数 $6x^5$，乘系数 $7$ 得 $42x^5F'(x^6)$。")
e(248, r"$6F(x^{4})\Rightarrow y'=6F'(x^{4})\cdot4x^{3}=24x^{3}F'(x^{4})$.",
  r"$6\cdot4x^3=24x^3$，得 $24x^3F'(x^4)$。")
e(249, r"$-9F(x^{2})\Rightarrow y'=-9F'(x^{2})\cdot2x=-18xF'(x^{2})$.",
  r"$y'=-9\cdot2x\,F'(x^2)=-18xF'(x^2)$。")
e(250, r"Outer cosine, then the square, then the inside: $-\sin u\cdot2(5x^{2}-6)\cdot10x$ with $u=(5x^{2}-6)^{2}$, i.e. $-20x(5x^{2}-6)\sin u=-10x(10x^{2}-12)\sin u$.",
  r"三层复合：$\cos\to$ 平方 $\to 5x^2-6$，逐层乘 $2(5x^2-6)$ 与 $10x$，得 $-10x(10x^2-12)\sin((5x^2-6)^2)$。")
e(251, r"With $u=(-x-2)^{-4}$, $u'=-4(-x-2)^{-5}\cdot(-1)=4(-x-2)^{-5}$, so $f'=4(-x-2)^{-5}\cos\bigl((-x-2)^{-4}\bigr)$.",
  r"令 $u=(-x-2)^{-4}$，则 $u'=4(-x-2)^{-5}$，故 $f'=4(-x-2)^{-5}\cos u$。负指数与内层负号要一起处理。")

# ---- 6.6 higher-order derivatives ----
e(252, r"$f'=-10x-5$, $f''=-10$.",
  r"一阶导 $-10x-5$，二阶导 $-10$。二次函数二阶导为常数。")
e(253, r"$f'=-10x-6$, so $f''=-10$.",
  r"$f'=-10x-6$，故 $f''=-10$。常数项求导即为零。")
e(254, r"$f'=-15x^{2}-12x-6$, $f''=-30x-12$; at $x=1$: $-42$.",
  r"两阶求导得 $-30x-12$，代入 $x=1$ 得 $-42$。")
e(255, r"Differentiate twice: $f''=-150x^{4}-120x^{3}-72x^{2}-36x-12$, which at $x=1$ is $-390$.",
  r"逐项求两次导，得 $-150x^4-120x^3-72x^2-36x-12$，代入 $x=1$ 得 $-390$。逐项算比套公式稳。")
e(256, r"The constant term does not affect second derivatives, so $f''(1)=-390$ again.",
  r"常数项求导为零，二阶导与上一题相同，$f''(1)=-390$。")
e(257, r"$f'=-16\sin4x$, $f''=-64\cos4x=-4\cdot4^{2}\cos4x$.",
  r"每次求导都多乘一个 $4$：$f''=-4\cdot4^2\cos4x=-64\cos4x$。")
e(258, r"$f'=4\cos x$, $f''=-4\sin x$, $f'''=-4\cos x$.",
  r"连续三次求导，$f'''=-4\cos x$。$\sin$ 的四阶导回到自身。")
e(259, r"$f'''=-125\cos5x=-5^{3}\cos5x$; the listed options all carry an extra factor $5$, so none matches.",
  r"$f'''=-125\cos5x=-5^3\cos5x$。选项都多乘了一个 $5$，故为\"以上都不对\"。")
e(260, r"The $n$-th derivative of $-\cos6x$ is $-6^{n}\cos(6x+\frac{n\pi}{2})$; for $n=10$ this is $-6^{10}\cos(6x+5\pi)=6^{10}\cos6x$.",
  r"每次求导乘 $6$ 并加 $\frac{\pi}{2}$ 相位；$n=10$ 时相位移 $5\pi$，余弦变号两次，得 $6^{10}\cos6x$。")
e(261, r"The derivatives of $-5\sin x$ cycle with period four; $11\equiv3\pmod 4$ gives $5\cos x$, which is not listed.",
  r"$-5\sin x$ 的导数以 $4$ 为周期循环，$11\equiv3$，对应 $5\cos x$。选项中没有，故选\"以上都不对\"。")

# ---- 6.7 kinematics ----
e(262, r"$s''=-10$, so the acceleration is constant $-10\ \mathrm{cm/s^{2}}$.",
  r"位置二次，二阶导为常数 $-10$，故加速度恒为 $-10$ cm/s²。")
e(263, r"$v=s'=-10t-2$; at $t=5$: $-52$.",
  r"$v=s'=-10t-2$，代入 $t=5$ 得 $-52$ cm/s。负号表示向负方向运动。")
e(264, r"$v=-10t-4$; at $t=2$: $-24$.",
  r"$v=-10t-4$，$t=2$ 时为 $-24$ m/s。")
e(265, r"$v=-15t^{2}-12t-6$, $a=-30t-12$.",
  r"先求速度再求导得 $a=-30t-12$。题目要的是函数而非某点的值。")
e(266, r"$v=-15t^{2}-12t-3$, $a=-30t-12$; at $t=1$: $-42$.",
  r"$a=-30t-12$，代入 $t=1$ 得 $-42$ cm/s²。")

# ---- 7.1 exp and log derivatives ----
e(267, r"$\ln\sqrt{14x+15}=\frac12\ln(14x+15)$, so the derivative is $\frac12\cdot\frac{14}{14x+15}=\frac{7}{14x+15}=\frac{14}{28x+30}$.",
  r"先化简：$\ln\sqrt{u}=\frac12\ln u$，求导得 $\frac{7}{14x+15}$，通分后与选项 $\frac{14}{28x+30}$ 相同。先化简能省一大半计算。")
e(268, r"$\frac{d}{dx}\ln(10x^{3}-19x)=\frac{30x^{2}-19}{10x^{3}-19x}$; no option keeps the denominator together with the correct numerator, so “none of these”.",
  r"对数求导公式给出 $\frac{30x^2-19}{10x^3-19x}$。选项要么分子错、要么丢了分母，故选\"以上都不对\"。")
e(269, r"$(\ln u)'=\frac{u'}{u}=\frac{26x-19}{13x^{2}-19x}$.",
  r"$\frac{u'}{u}=\frac{26x-19}{13x^2-19x}$。分子是内层导数，别漏乘。")
e(270, r"$\frac12\ln(7x-15)\Rightarrow\frac12\cdot\frac{7}{7x-15}=\frac{7}{14x-30}$.",
  r"提 $\frac12$ 后求导得 $\frac{7}{14x-30}$。系数 $\frac12$ 与 $7$ 相乘。")
e(271, r"$\frac{84x^{5}+13}{14x^{6}+13x}$.",
  r"内层导数 $84x^5+13$ 作分子，原式作分母。")
e(272, r"$(e^{u})'=u'e^{u}$ with $u=8x^{2}+4x+6$, so $u'=16x+4$.",
  r"$u'=16x+4$ 乘上 $e^u$ 即为答案。指数函数求导只多一个内层导数。")
e(273, r"$u=-11x^{2}-6x+4$, $u'=-22x-6$.",
  r"$u'=-22x-6$，与 $e^u$ 相乘。三项分别求导。")
e(274, r"$u=-2x^{2}-7x+2$, $u'=-4x-7$.",
  r"$u'=-4x-7$，故 $f'=(-4x-7)e^{u}$。")
e(275, r"$u=-2x^{2}-x+6$, $u'=-4x-1$, so $f'=(-4x-1)e^{u}$ — no option matches (A has the wrong sign).",
  r"$u'=-4x-1$，故 $f'=(-4x-1)e^u$。选项 A 符号相反、E 少了一项，故选\"以上都不对\"。")
e(276, r"$u=-x^{2}+x+1$, $u'=1-2x$, so $f'=(1-2x)e^{-x^{2}+x+1}$.",
  r"$u'=1-2x$，得 $f'=(1-2x)e^{-x^2+x+1}$。")
e(277, r"With $u=x^{4}\ln(17x)$, $u'=4x^{3}\ln(17x)+x^{4}\cdot\frac{1}{x}=x^{3}(4\ln17x+1)$, so $f'=x^{3}(4\ln(17x)+1)e^{u}$.",
  r"$u=x^4\ln(17x)$，用乘积法则得 $u'=x^3(4\ln17x+1)$（因为 $x^4\cdot\frac1x=x^3$），故 $f'=x^3(4\ln17x+1)e^u$。")
e(278, r"$u=-11x^{5}\ln(12x)$, $u'=-55x^{4}\ln(12x)-11x^{4}=-11x^{4}(5\ln12x+1)$.",
  r"$u'=-11x^4(5\ln12x+1)$，再乘 $e^u$。系数 $-11$ 要提出来。")
e(279, r"$u=11x\ln(7x)$, $u'=11\ln(7x)+11$, so $f'=(11\ln(7x)+11)e^{u}$.",
  r"$u'=11\ln7x+11\cdot\frac{x}{x}=11(\ln7x+1)$，故 $f'=11(\ln7x+1)e^u$。")
e(280, r"$u=-x^{6}\ln(18x)$, $u'=-6x^{5}\ln(18x)-x^{5}=-x^{5}(6\ln18x+1)$.",
  r"$u'=-x^5(6\ln18x+1)$，与 $e^u$ 相乘。")
e(281, r"$u=-4x^{4}\ln(17x)$, $u'=-16x^{3}\ln(17x)-4x^{3}=-4x^{3}(4\ln17x+1)$.",
  r"$u'=-4x^3(4\ln17x+1)$，再乘 $e^u$。")
e(282, r"The function reduces to $\sqrt{361-400x^{2}}$ after simplification, so its derivative is the one shown.",
  r"化简后被开方式为 $361-400x^2$，答案即该根式本身。遇到复杂分式先化简再动笔。")

# ---- 7.2 derivative of an inverse ----
e(283, r"$(f^{-1})'(b)=\frac{1}{f'(a)}$ where $f(a)=b$. Here $f(-4)=-128-48-19=-195$, so $(f^{-1})'(-195)=\frac{1}{f'(-4)}=\frac{1}{6(-4)^{2}+12}$.",
  r"用公式 $(f^{-1})'(b)=\frac{1}{f'(a)}$，其中 $f(a)=b$。由 $f(-4)=-195$ 得 $a=-4$，故为 $\frac{1}{6(-4)^2+12}$。先找 $a$ 再求导。")
e(284, r"$f(-1)=-9-10=-19$, so the answer is $\frac{1}{f'(-1)}=\frac{1}{27(-1)^{2}+10}$.",
  r"由 $f(-1)=-19$ 定出 $a=-1$，故为 $\frac{1}{27(-1)^2+10}$。")
e(285, r"$f(-4)=-384-36-4=-424$, hence $\frac{1}{f'(-4)}=\frac{1}{18(-4)^{2}+9}$.",
  r"$f(-4)=-424$，故 $a=-4$，答案为 $\frac{1}{18(-4)^2+9}$。")
e(286, r"$f(3)=324+6+18=348$, so the value is $\frac{1}{f'(3)}=\frac{1}{36\cdot9+2}=\frac{1}{326}$ — none of the options has this.",
  r"$f(3)=348$，故答案为 $\frac{1}{36\cdot3^2+2}=\frac{1}{326}$。选项里分母都写错了（用了 $348$ 或 $4$），故选\"以上都不对\"。")
e(287, r"$f(2)=40+12-19=33$, so $\frac{1}{f'(2)}=\frac{1}{15(2)^{2}+6}$.",
  r"$f(2)=33$，故 $a=2$，答案为 $\frac{1}{15(2)^2+6}$。")

# ---- 7.3 inverse trig derivatives ----
e(288, r"$\frac{d}{dx}\arccos(e^{-68x})=-\frac{1}{\sqrt{1-(e^{-68x})^{2}}}\cdot(-68e^{-68x})=\frac{68e^{-68x}}{\sqrt{1-e^{-136x}}}$.",
  r"$\arccos$ 的导数是 $-\frac{1}{\sqrt{1-u^2}}$，内层导数 $-68e^{-68x}$，两个负号相消，得 $\frac{68e^{-68x}}{\sqrt{1-e^{-136x}}}$。")
e(289, r"$\arctan u$ with $u=8\ln(10x)-1$: $u'=\frac{8}{x}$, so the derivative is $\frac{8}{x\,(1+(8\ln(10x)-1)^{2})}$.",
  r"内层 $u=8\ln10x-1$ 的导数为 $\frac8x$；套 $\frac{u'}{1+u^2}$，得 $\frac{8}{x(1+(8\ln10x-1)^2)}$。")
e(290, r"$\arcsin(75x^{3})$: derivative $\frac{225x^{2}}{\sqrt{1-(75x^{3})^{2}}}$.",
  r"内层导数 $225x^2$，套 $\frac{u'}{\sqrt{1-u^2}}$，得 $\frac{225x^2}{\sqrt{1-(75x^3)^2}}$。")
e(291, r"Same pattern with $u=e^{-28x}$: $\frac{28e^{-28x}}{\sqrt{1-e^{-56x}}}$.",
  r"$u'=-28e^{-28x}$，与 $\arccos$ 的负号相消，得 $\frac{28e^{-28x}}{\sqrt{1-e^{-56x}}}$。")
e(292, r"$\frac{70e^{-70x}}{\sqrt{1-e^{-140x}}}$.",
  r"内层导数 $-70e^{-70x}$ 消掉外层负号，得 $\frac{70e^{-70x}}{\sqrt{1-e^{-140x}}}$。")

# ---- 7.4 logarithmic differentiation ----
e(293, r"Write $y=(\sin19x+14)^{\ln19x}$ and take logs: $\ln y=\ln19x\cdot\ln(\sin19x+14)$. Then $\frac{y'}{y}=\frac{19\ln(\sin19x+14)}{19x}+\ln(19x)\cdot\frac{19\cos19x}{\sin19x+14}$.",
  r"幂指函数先取对数：$\ln y=\ln19x\cdot\ln(\sin19x+14)$，两边对 $x$ 求导后乘回 $y$。两项分别来自 $19x$ 与 $\sin$ 的求导。")
e(294, r"Logs: $\ln y=\sin9x\ln(9x^{8}+17)$, so $\frac{y'}{y}=9\cos9x\ln(9x^{8}+17)+\frac{72x^{7}\sin9x}{9x^{8}+17}$.",
  r"$\ln y=\sin9x\ln(9x^8+17)$，求导时乘积法则给出两项：$9\cos9x\ln(\cdot)$ 与 $\frac{72x^7\sin9x}{9x^8+17}$。")
e(295, r"$\ln y=\sin2x\ln(6x^{2}+18)$, so $\frac{y'}{y}=2\cos2x\ln(6x^{2}+18)+\frac{12x\sin2x}{6x^{2}+18}$.",
  r"取对数后求导，得 $2\cos2x\ln(\cdot)+\frac{12x\sin2x}{6x^2+18}$，再乘 $y$。")
e(296, r"Here $\ln y=\sin7x\ln(7x^{4}+3)$. At $x=\frac{\pi}{7}$ we have $\sin7x=0$ and $\cos7x=-1$, so $y'=y\cdot7(-1)\ln(7x^{4}+3)=-7\ln\bigl(7(\frac{\pi}{7})^{4}+3\bigr)$.",
  r"在 $x=\frac{\pi}{7}$ 处 $\sin7x=0$、$\cos7x=-1$，故 $y'=-7\ln(7(\frac{\pi}{7})^4+3)$。利用 $\sin=0$ 可直接消掉一整项。")

# ---- 7.5 implicit differentiation ----
e(297, r"Differentiate $9x^{4}+9xy=10y^{2}$: $36x^{3}+9y+9xy'=20yy'$. At $(-2,3)$: $-288+27-18y'=60y'$, so $y'=-\frac{87}{26}$.",
  r"两边求导得 $36x^3+9y+9xy'=20yy'$，代入 $(-2,3)$ 解出 $y'=-\frac{87}{26}$。含 $y$ 的项要乘 $y'$。")
e(298, r"$6x^{6}+2xy^{2}=5y^{3}$ gives $36x^{5}+2y^{2}+4xyy'=15y^{2}y'$, hence $y'=\frac{36x^{5}+2y^{2}}{15y^{2}-4xy}$ with the sign convention of the option.",
  r"求导得 $36x^5+2y^2+4xyy'=15y^2y'$，整理出 $y'$。$2xy^2$ 要用乘积法则。")
e(299, r"$18y^{2}-27y=2x^{5}$ gives $(36y-27)y'=10x^{4}$. At $(3,6)$: $y'=\frac{10\cdot81}{216-27}=\frac{810}{189}=\frac{30}{7}$.",
  r"求导得 $(36y-27)y'=10x^4$，代入 $(3,6)$ 得 $\frac{810}{189}=\frac{30}{7}$。")
e(300, r"$8x^{2}+18xy=-9y^{2}$ gives $16x+18y+18xy'=-18yy'$. At $(-3,2)$: $-48+36-54y'=-36y'$, so $y'=-\frac23$.",
  r"求导后代 $(-3,2)$ 解出 $y'=-\frac23$。左右两边都要把 $y$ 当函数处理。")
e(301, r"$13x^{5}+17xy^{3}=-29y^{4}$ gives $65x^{4}+17y^{3}+51xy^{2}y'=-116y^{3}y'$, so $y'=-\frac{65x^{4}+17y^{3}}{51xy^{2}+116y^{3}}$.",
  r"逐项求导后把含 $y'$ 的项归到一边，得 $y'=-\frac{65x^4+17y^3}{51xy^2+116y^3}$。")

# ---- 7.6 tangent from an implicit curve ----
e(302, r"$5\sqrt y+4xy^{4}=5$: $\frac{5}{2\sqrt y}y'+4y^{4}+16xy^{3}y'=0$. At $(0,1)$: $\frac52y'+4=0$, so $y'=-\frac85$ and $y=1-\frac85x$.",
  r"隐函数求导后代 $(0,1)$ 得 $y'=-\frac85$，切线为 $y=1-\frac85x$。")
e(303, r"$5\sqrt y+6xy^{3}=5$: at $(0,1)$, $\frac52y'+6=0$, so $y'=-\frac{12}{5}$ and the tangent is $y=1-\frac{12x}{5}$ — not listed.",
  r"在 $(0,1)$ 处 $y'=-\frac{12}{5}$，切线为 $y=1-\frac{12x}{5}$。选项 B 的斜率符号相反、D 缺常数项，故选\"以上都不对\"。")
e(304, r"$9\sqrt y+8xy^{2}=9$: at $(0,1)$, $\frac92y'+8=0$, so $y=1-\frac{16x}{9}$ — none of the options states it.",
  r"在 $(0,1)$ 处 $y'=-\frac{16}{9}$，切线 $y=1-\frac{16x}{9}$，四个选项都不对。")
e(305, r"$4\sqrt y+xy=0$: $\frac{2}{\sqrt y}y'+y+xy'=0$. At $(-2,4)$: $y'+4-2y'=0$, so $y'=4$ and $y=4x+12$.",
  r"在 $(-2,4)$ 处解出 $y'=4$，切线为 $y-4=4(x+2)$，即 $y=4x+12$。")
e(306, r"$8\sqrt y+5xy=-2$: $\frac{4}{\sqrt y}y'+5y+5xy'=0$. At $(-2,1)$: $4y'+5-10y'=0$, so $y'=\frac56$ and $y=\frac{5x}{6}+\frac83$.",
  r"在 $(-2,1)$ 处 $y'=\frac56$，由点斜式得 $y=\frac{5x}{6}+\frac83$。")

# ---- 8.1 rising balloon ----
e(307, r"$D^{2}=100^{2}+h^{2}$ gives $2DD'=2hh'$, so $D'=\frac{h}{D}h'=\frac{120\cdot3}{\sqrt{100^{2}+120^{2}}}$; that exact form is not among the options.",
  r"由 $D^2=100^2+h^2$ 求导得 $D'=\frac{h}{D}h'=\frac{120\cdot3}{\sqrt{100^2+120^2}}$。选项 A 把 $120$ 写成了 $100$，故选\"以上都不对\"。")
e(308, r"$D'=\frac{130\cdot6}{\sqrt{170^{2}+130^{2}}}$.",
  r"同一模型：$D'=\frac{h}{D}h'=\frac{130\cdot6}{\sqrt{170^2+130^2}}$。先列关系式再对 $t$ 求导。")
e(309, r"$r=\frac{7}{25}h$ so $V=\frac{\pi}{3}\cdot\frac{49}{625}h^{3}$, and $V'=\frac{49\pi}{625}h^{2}h'$. At $h=10$: $h'=\frac{27\cdot625}{49\pi\cdot100}$, which differs from every option by a factor $3$.",
  r"相似三角形给 $r=\frac7{25}h$，故 $V=\frac{\pi}{3}\cdot\frac{49}{625}h^3$，求导得 $h'=\frac{27\cdot625}{49\pi\cdot100}$。选项 C 多了一个 $3$，故选\"以上都不对\"。")
e(310, r"The same cone model: $h'=\frac{23}{\pi(8/21)^{2}h^{2}}$ with $h=17$, i.e. $\frac{23\cdot21^{2}}{\pi\cdot8^{2}\cdot17^{2}}$.",
  r"同一模型代入：$h'=\frac{23\cdot21^2}{\pi\cdot8^2\cdot17^2}$。相似比 $\frac{8}{21}$ 要先平方。")

# ---- 8.3 boat and telescope ----
e(311, r"$\tan\theta=\frac{x}{190}$ gives $\sec^{2}\theta\,\theta'=\frac{x'}{190}$, so $\theta'=\frac{15\cdot190}{190^{2}+310^{2}}$ with a minus sign because the angle shrinks.",
  r"$\tan\theta=\frac{x}{190}$ 求导得 $\theta'=\frac{190x'}{190^2+x^2}$；$x'=-15$（船在靠近），故结果为 $-\frac{15\cdot190}{190^2+310^2}$。")

# ---- 9.1 stationary and singular points ----
e(312, r"$f'=-3(x+2)^{2}$ vanishes at $x=-2$, a stationary point. The derivative exists everywhere, so there are no singular points.",
  r"$f'=-3(x+2)^2$ 在 $x=-2$ 为零，是驻点；导数处处存在，无奇点。驻点看 $f'=0$，奇点看 $f'$ 不存在。")
e(313, r"$f'=6(x+2)^{2}=0$ at $x=-2$, and the derivative exists on $[-4,0]$, so no singular points.",
  r"$f'=6(x+2)^2$ 在 $x=-2$ 为零；区间内导数处处存在，故只有驻点。")
e(314, r"$f'=3(x+1)^{2}$ vanishes at $x=-1$; no point where the derivative fails to exist.",
  r"$f'=3(x+1)^2$ 在 $x=-1$ 为零，无奇点。")
e(315, r"$f=-(x+1)^{2/3}$ has $f'=-\frac{2}{3}(x+1)^{-1/3}$, which is never zero but fails to exist at $x=-1$: a singular point, no stationary point.",
  r"$f'=-\frac23(x+1)^{-1/3}$ 永不为零，但在 $x=-1$ 处不存在，故只有奇点没有驻点。分数幂在端点处常出奇点。")
e(316, r"$f=-2\sqrt{x+7}+3$ has $f'=-\frac{1}{\sqrt{x+7}}$, never zero and defined on the whole interval $[-6,2]$ except the endpoint behaviour, so neither type occurs.",
  r"$f'=-\frac{1}{\sqrt{x+7}}$ 在 $(-6,2]$ 内不为零且处处存在，故既无驻点也无奇点。")

# ---- 9.2 extrema on a closed interval ----
e(317, r"$f'=-\frac43(x+2)^{-1/3}$ never vanishes but is undefined at $x=-2$; so the candidates are the endpoints $-3,0$ and the critical point $-2$.",
  r"$f'$ 在 $x=-2$ 不存在，端点为 $-3$ 与 $0$，故候选点为 $-3,-2,0$。闭区间最值必须同时考虑端点与内部临界点。")
e(318, r"Write $u=x+2$; then $f'=-\frac{u^{1/3}(u+12)}{3(u+5)^{2}}$, which vanishes and is undefined at the same point $u=0$. So the only interior candidate is $x=-2$, and with the endpoints the list is $-4,-2,4$.",
  r"令 $u=x+2$，求导得 $f'=-\frac{u^{1/3}(u+12)}{3(u+5)^2}$，零点与不可导点重合于 $u=0$。故内部候选点只有 $x=-2$，加上端点即 $-4,-2,4$。")
e(319, r"$f'=-\frac{1}{\sqrt{x+7}}$ is never zero and is defined on $(-6,2)$, so only the endpoints matter: $-6$ and $2$.",
  r"导数在区间内恒不为零且处处存在，故只需比较端点 $-6$ 与 $2$。没有临界点时端点就是全部候选。")
e(320, r"The radical forces $x\ge-2$, and on that domain $f=-(x+2)+10$ is linear with slope $-1$, so there is no interior stationary point; the candidates are the interval ends and the edge of the domain, $-3$, $-2$, $0$.",
  r"根号要求 $x\ge-2$，在该段上 $f=-(x+2)+10$ 是斜率为 $-1$ 的直线，内部无驻点；候选点为两个端点与定义域边界，即 $-3,-2,0$。")
e(321, r"$f'=e^{-x-2}(x+1)$ vanishes at $x=-1$; together with the endpoints $-2,2$ the candidates are $-2,-1,2$, a set no option lists.",
  r"$f'=e^{-x-2}(x+1)$ 在 $x=-1$ 为零，加上端点得 $-2,-1,2$。选项都没有这三个点，故选\"以上都不对\"。")
e(322, r"$f=(x+1)^{2}(4x-14)$ has $f'=2(x+1)(4x-14)+4(x+1)^{2}=6(x+1)(2x-4)$, zero at $x=-1$ and $x=2$. Comparing with the endpoints, the maximum is at $x=5$ and the minimum at $x=-\frac52$ and $x=2$.",
  r"求导得 $6(x+1)(2x-4)$，临界点 $x=-1,2$。与端点比较：最大值在 $x=5$，最小值在 $x=-\frac52$ 与 $x=2$。")
e(323, r"$f=(x+1)^{2/3}$ is decreasing to $x=-1$ then increasing, so the maximum is at the left endpoint $-9$ and the minimum at $x=-1$.",
  r"$f$ 在 $x=-1$ 左侧递减、右侧递增，故最大值在左端点 $-9$，最小值在 $x=-1$。")
e(324, r"$f=-2(x-2)^{2/3}$ peaks at $x=2$ and decreases away from it, so the maximum is at $x=2$ and the minimum at the farther endpoint $x=-6$.",
  r"$f$ 在 $x=2$ 取最大值，向两侧递减；端点 $-6$ 比 $4$ 更远，故最小值在 $x=-6$。")
e(325, r"$f=(x-1)^{2}(2x-5)$ has critical points $x=1$ and $x=2$; evaluating at endpoints and these gives maximum at $x=3$, minimum at $x=\frac12$ and $x=2$.",
  r"展开求导得临界点 $x=1,2$，与端点比较得最大值在 $x=3$、最小值在 $x=\frac12$ 与 $x=2$。")
e(326, r"$f=-2(x+1)^{2/3}$ peaks at $x=-1$; the endpoints $-9$ and $7$ tie for the minimum.",
  r"$f$ 在 $x=-1$ 取最大值；两端点 $-9$ 与 $7$ 对称，最小值同时取到。")
e(327, r"$f=3\frac{(x-2)^{4/3}}{x+1}$ on $[0,8]$: the maximum is $3\cdot\frac{6^{4/3}}{9}=6\sqrt[3]{2}$ (at $x=8$) and the minimum is $0$ (at $x=2$).",
  r"在 $[0,8]$ 上比较端点与临界点：$x=8$ 处取最大值 $6\sqrt[3]2$，$x=2$ 处函数值为 $0$ 即最小值。")
e(328, r"$f=3(x+1)^{2/3}$ on $[-2,1]$: values are $3$ at $x=-2$, $0$ at $x=-1$, $3\sqrt[3]{4}$ at $x=1$. The maximum is $3\sqrt[3]{4}\approx4.76$ and the minimum $0$, a pair no option states.",
  r"三点取值：$f(-2)=3$、$f(-1)=0$、$f(1)=3\sqrt[3]4\approx4.76$。最大 $3\sqrt[3]4$、最小 $0$，选项都没有这一对，故选\"以上都不对\"。")
e(329, r"$f=-\sqrt{x+7}$ is decreasing, so the maximum is at $x=-6$ ($-1$) and the minimum at $x=2$ ($-3$).",
  r"$f$ 单调递减，最大值在左端点 $-6$ 处为 $-1$，最小值在右端点 $2$ 处为 $-3$。")
e(330, r"The critical point $x=0$ gives $7$; at $x=-2$ the value is $4\sqrt[3]{2}+7\approx12.04$ and at $x=6$ it is $\frac{4\sqrt[3]{6}}{3}+7\approx9.4$. The true pair (max $4\sqrt[3]2+7$, min $7$) appears in no option.",
  r"临界点 $x=0$ 处为 $7$；$x=-2$ 处 $4\sqrt[3]2+7\approx12.04$，$x=6$ 处约 $9.4$。真正的最值对（最大 $4\sqrt[3]2+7$、最小 $7$）不在选项中。")
e(331, r"$f=-2\frac{(x-1)^{4/3}}{x+2}$ on $[-1,7]$: at $x=1$ the value is $0$ (maximum) and at $x=7$ it is $-\frac{2\cdot6^{4/3}}{9}=-4\sqrt[3]2$ (minimum).",
  r"$x=1$ 处函数值为 $0$ 是最大值；$x=7$ 处为 $-4\sqrt[3]2$ 是最小值。分子在 $x=1$ 为零是关键。")

# ---- 9.3 monotonicity ----
e(332, r"$f'=-3x^{2}\le0$ everywhere and is zero only at a single point, so $f$ is decreasing on $\mathbb{R}$ and increasing nowhere.",
  r"$f'=-3x^2\le0$ 恒成立，仅在一点为零，故函数在 $\mathbb{R}$ 上单调递减，没有递增区间。导数偶尔为零不改变单调性。")
e(333, r"With $u=x+1$, $f'=\frac{u(8-4u^{2})}{4}$: sign $+$ on $(-\infty,-3]$ and $[-1,1]$, $-$ elsewhere, so $f$ increases there and decreases on $[-3,-1]$ and $[1,\infty)$.",
  r"令 $u=x+1$，$f'=\frac{u(8-4u^2)}{4}$。符号在 $(-\infty,-3]$、$[-1,1]$ 为正，其余为负，故这些区间递增，$[-3,-1]$ 与 $[1,\infty)$ 递减。")
e(334, r"With $u=x-2$, $f'=\frac{u(u^{2}-4)}{2}$, positive on $[0,2]$ and $[4,\infty)$, negative on $(-\infty,0]$ and $[2,4]$.",
  r"令 $u=x-2$，$f'=\frac{u(u^2-4)}{2}$。$[0,2]$、$[4,\infty)$ 上为正（递增），$(-\infty,0]$、$[2,4]$ 上为负（递减）。")
e(335, r"$f'=2x(x^{2}-4)$, so the critical points are $x=-2,0,2$. The sign pattern $-,+,-,+$ gives increasing on $[-2,0]$ and $[2,\infty)$, decreasing on $(-\infty,-2]$ and $[0,2]$.",
  r"$f'=2x(x^2-4)$，临界点 $-2,0,2$。符号依次为 $-,+,-,+$，故 $[-2,0]$ 与 $[2,\infty)$ 递增，$(-\infty,-2]$ 与 $[0,2]$ 递减。")
e(336, r"$f=2|x-1|$ has slope $-2$ for $x<1$ and $+2$ for $x>1$: increasing on $[1,\infty)$, decreasing on $(-\infty,1]$.",
  r"$f=2|x-1|$ 在 $x<1$ 斜率为 $-2$、$x>1$ 为 $+2$，故在 $[1,\infty)$ 递增、$(-\infty,1]$ 递减。")

# ---- 9.4 concavity and inflection ----
e(337, r"$f=-\ln(|x-2|+1)+3$ has $f''=\frac{1}{(|x-2|+1)^{2}}$ on each side of $x=2$, always positive, so the maximal open intervals of upward concavity are $(-\infty,2)$ and $(2,\infty)$ — the single interval $(-\infty,\infty)$ is not a valid answer because $f$ is not differentiable at $2$, and no option states the split, hence “none of these”.",
  r"$f''=\frac{1}{(|x-2|+1)^2}>0$ 恒成立，但 $x=2$ 处不可导，故凹向上的最大开区间是 $(-\infty,2)$ 与 $(2,\infty)$ 两段，而非 $(-\infty,\infty)$。选项都没写这个拆分，故选\"以上都不对\"。")
e(338, r"$f=-\frac{1}{3\sqrt{x-1}}+3$ has $f''$ that changes sign at $x=1$: the graph is concave up on $(-\infty,1)$ and concave down on $(1,\infty)$ within the domain.",
  r"二阶导在 $x=1$ 两侧变号：$(-\infty,1)$ 上凹向上，$(1,\infty)$ 上凹向下。拐点与定义域边界要分开看。")
e(339, r"With $u=x-1$, $\sin^{2}u=\frac{1-\cos2u}{2}$ gives $f''=-2(6+2\cos2u)=-12-4\cos2u\le-8<0$ everywhere. Hence $f$ is concave down on $\mathbb{R}$ and never concave up.",
  r"令 $u=x-1$，用 $\sin^2u=\frac{1-\cos2u}{2}$ 得 $f''=-12-4\cos2u\le-8<0$ 恒成立，故函数处处凹向下，没有凹向上的区间。")
e(340, r"$f=e^{(x+2)^{2}}$ has $f''=2e^{(x+2)^{2}}(1+2(x+2)^{2})>0$, so it is concave up on $(-\infty,\infty)$ and never concave down.",
  r"$f''=2e^{(x+2)^2}(1+2(x+2)^2)>0$ 恒成立，故在整个 $\mathbb{R}$ 上凹向上，没有凹向下区间。")
e(341, r"With $u=x+2$, $f''=\frac{4u(u^{2}-12)}{(u^{2}+4)^{3}}$, which changes sign at $u=0$ and $u=\pm2\sqrt3$. The sign is $+$ on $(-2\sqrt3,0)$ and on $(2\sqrt3,\infty)$, so $f$ is concave up on $(-2\sqrt3-2,-2)$ and on $(-2+2\sqrt3,\infty)$.",
  r"令 $u=x+2$，$f''=\frac{4u(u^2-12)}{(u^2+4)^3}$，变号点在 $u=0,\pm2\sqrt3$。符号在 $(-2\sqrt3,0)$ 与 $(2\sqrt3,\infty)$ 为正，故凹向上区间为 $(-2\sqrt3-2,-2)$ 与 $(-2+2\sqrt3,\infty)$。")
e(342, r"$f=(x-2)e^{(x-2)^{2}}+2$ has $f''=e^{u^{2}}\cdot2u(3+2u^{2})$ with $u=x-2$, zero at $u=0$ and changing sign there: the only inflection point is $(2,2)$.",
  r"令 $u=x-2$，$f''\propto u(3+2u^2)$ 只在 $u=0$ 变号，故唯一拐点为 $(2,2)$。拐点要求二阶导变号，仅为零不够。")
e(343, r"$f=(x+1)^{4}+7$ has $f''=12(x+1)^{2}\ge0$, never changing sign, so there are no inflection points.",
  r"$f''=12(x+1)^2\ge0$ 不变号，故没有拐点。四阶多项式的二阶导常只为零而不变号。")
e(344, r"$f=2\sqrt[3]{x+2}+2$ has $f''$ changing sign at $x=-2$, so the inflection point is $(-2,2)$.",
  r"二阶导在 $x=-2$ 两侧变号，故拐点为 $(-2,2)$。立方根类函数常在内部点出拐点。")
e(345, r"$f=2\frac{x}{x^{2}+9}+2$ has $f''$ zero at $x=0$ and $x=\pm3\sqrt3$, all sign-changing, giving three inflection points.",
  r"$f''$ 在 $x=0$ 与 $x=\pm3\sqrt3$ 处变号，故有三个拐点。奇函数结构常给出对称的三个。")
e(346, r"$f=\sqrt[3]{x-2}+2$ has $f''$ changing sign only at $x=2$, so one inflection point at $(2,2)$.",
  r"二阶导只在 $x=2$ 变号，拐点为 $(2,2)$。")

# ---- 9.5 number of real roots ----
e(347, r"$f'=3x^{2}+2>0$, so $f$ is strictly increasing and has exactly one root; $f(1)=-5<0$ and $f(2)=10>0$ locate it in $(1,2)$.",
  r"$f'=3x^2+2>0$，函数严格递增，故恰有一个实根；$f(1)<0$、$f(2)>0$ 把它定位在 $(1,2)$。单调性定个数，介值定理定位置。")
e(348, r"$f'=3x^{2}+2>0$ gives exactly one root; $f(-1)=-2<0$ and $f(0)=1>0$, so it lies in $(-1,0)$.",
  r"导数恒正故只有一根；$f(-1)<0$、$f(0)>0$，根在 $(-1,0)$。")
e(349, r"$f'=3x^{2}+4>0$: exactly one root, and $f(1)=-2<0$, $f(2)=9>0$ place it in $(1,2)$.",
  r"导数恒正，唯一根；$f(1)<0$、$f(2)>0$ 得根在 $(1,2)$。")
e(350, r"$f'=3x^{2}+1>0$: one root; $f(-1)=-1<0$ and $f(0)=1>0$ put it in $(-1,0)$.",
  r"$f'>0$，唯一根；端点异号说明根在 $(-1,0)$。")
e(351, r"$f'=3x^{2}+4>0$, so exactly one real root; $f(-3)=-27-12+20=-19<0$ and $f(-2)=-8-8+20=4>0$ place it in $(-3,-2)$.",
  r"导数恒正，故只有一根；$f(-3)<0$、$f(-2)>0$，根落在 $(-3,-2)$。")
