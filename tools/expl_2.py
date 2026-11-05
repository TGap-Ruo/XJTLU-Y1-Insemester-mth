# -*- coding: utf-8 -*-
"""Chapter 2 (Q51-126) bilingual solutions."""
E = {}


def e(n, en, zh):
    E[n] = (en, zh)


# ---- 2.1 limit at a point, definition of the point irrelevant ----
e(51, r"The value $f(-3)=15$ is a decoy: a limit only looks at points near $-3$, where $f(x)=-3x-3$. Hence $\lim_{x\to-3}f(x)=-3(-3)-3=6$.",
  r"$f(-3)=15$ 是干扰项：极限只看 $x$ 靠近 $-3$ 时的函数值，那里用分支 $-3x-3$，代入得 $6$。函数在该点的取值不影响极限。")
e(52, r"Near $x=-1$ the function is $6-x$, so the limit is $6-(-1)=7$; the special value $-8$ at the point is irrelevant.",
  r"$x$ 靠近 $-1$ 时用分支 $6-x$，极限为 $7$。题目给出的 $f(-1)=-8$ 与极限无关。")
e(53, r"Use the branch that governs $x\to1$: $3(1)+1=4$. The separate value $-3$ at $x=1$ does not enter the limit.",
  r"取 $x\to1$ 对应的分支 $3x+1$，代入得 $4$。$x=1$ 处另行定义的 $-3$ 不参与极限。")
e(54, r"$\lim_{x\to-2}(5-2x)=5+4=9$.",
  r"$x\to-2$ 时用 $5-2x$，代入得 $9$。")
e(55, r"$\lim_{x\to3}(-4x-1)=-12-1=-13$.",
  r"代入分支 $-4x-1$ 得 $-13$。")

# ---- 2.2 two-sided limits of piecewise functions ----
e(56, r"Left branch at $x=-4$: $-2(-4)-7=1$. Right branch: $-2(16)+16+17=1$. Both one-sided limits agree, so the limit is $1$.",
  r"左支在 $x=-4$ 得 $1$，右支也得 $1$。左右极限相等，故双侧极限为 $1$。两侧都算一遍是这类题的固定动作。")
e(57, r"Left: $x-7=-10$; right: $-x^{2}+5x+14=-9-15+14=-10$. They agree, so the limit is $-10$.",
  r"左支 $x-7$ 得 $-10$，右支 $-x^2+5x+14$ 也得 $-10$，故极限为 $-10$。")
e(58, r"Left: $10-1=9$; right: $3-2+8=9$. Equal, so the limit is $9$.",
  r"左支得 $9$，右支 $3x^2-2x+8$ 也得 $9$，故极限为 $9$。")
e(59, r"Left: $-2(3)-5=-11$; right: $2(9)-3-26=-11$. Equal, so the limit is $-11$.",
  r"左支得 $-11$，右支 $2x^2-x-26$ 同为 $-11$，故极限为 $-11$。")
e(60, r"Left: $19-9=10$; right: $2(9)+9-17=10$. Equal, so the limit is $10$.",
  r"左支 $19-3x$ 得 $10$，右支 $2x^2+3x-17$ 也得 $10$，故极限为 $10$。")

# ---- 2.3 limits with absolute values ----
e(61, r"Factor the denominator: $2x^{2}+17x+36=(2x+9)(x+4)$. Then $\frac{3|x+4|}{(2x+9)(x+4)}=\pm\frac{3}{2x+9}$, where the sign depends on whether $x>-4$ or $x<-4$. At $x=-4$ the factor $2x+9=1$, so the one-sided limits are $+3$ and $-3$: they differ, hence DNE.",
  r"分母分解为 $(2x+9)(x+4)$，约去 $x+4$ 后剩下 $\pm\frac{3}{2x+9}$，正负由 $x>-4$ 还是 $x<-4$ 决定。左右极限分别为 $+3$ 与 $-3$，不相等，故极限不存在。")
e(62, r"Here $x\to2^{+}$ so $|x-2|=x-2$. The denominator is $2(x-2)(x+1)$, giving $\frac{5}{2(x+1)}\to\frac56$.",
  r"因为 $x\to2^{+}$，故 $|x-2|=x-2$。分母分解为 $2(x-2)(x+1)$，约分后得 $\frac{5}{2(x+1)}\to\frac56$。单侧极限要保留符号。")
e(63, r"For $x<3$, $|x-3|=3-x$ and $4x^{2}-29x+51=(x-3)(4x-17)$, so the ratio becomes $-\frac{4}{4x-17}\to-\frac{4}{-5}=\frac45$. That value is not listed, so none of the four choices is correct.",
  r"$x<3$ 时 $|x-3|=3-x$，分母分解为 $(x-3)(4x-17)$，约分后为 $-\frac{4}{4x-17}\to\frac45$。选项中无此值，故选\"以上都不对\"。")
e(64, r"With $|x+1|$ and denominator $(5-x)(x+1)$, the reduced ratio is $\pm\frac{2}{5-x}$; at $x=-1$ that is $\pm\frac{1}{3}$, so the two sides disagree and the limit does not exist. DNE is not offered, hence “none of these”.",
  r"约去 $x+1$ 后剩 $\pm\frac{2}{5-x}$，在 $x=-1$ 处为 $\pm\frac13$，左右不等，极限不存在。选项未给 DNE，故选\"以上都不对\"。")
e(65, r"Denominator $-x^{2}-8x-15=-(x+3)(x+5)$. After cancelling, $\pm\frac{3}{-(x+5)}\to\pm\frac32$; the two sides differ, so the limit does not exist — not among the choices.",
  r"分母 $-(x+3)(x+5)$ 约去 $x+3$ 后得 $\pm\frac{3}{-(x+5)}\to\pm\frac32$，左右不等，极限不存在，故为\"以上都不对\"。")

# ---- 2.4 oscillation ----
e(66, r"As $x\to0$, $3-\frac3x$ sweeps through all reals, so $\sin(3-\frac3x)$ keeps oscillating between $-1$ and $1$; no single value is approached, hence DNE.",
  r"$x\to0$ 时 $3-\frac3x$ 趋于无穷并扫过所有实数，$\sin$ 在 $-1$ 与 $1$ 之间无限振荡，没有确定的极限，故不存在。")
e(67, r"The term $5\sin(2-\frac2x)$ oscillates with amplitude $5$, so the whole expression never settles; DNE.",
  r"$5\sin(2-\frac2x)$ 以振幅 $5$ 振荡，整体不趋于任何数，故极限不存在。振幅大小不影响振荡结论。")
e(68, r"$-5\sin(1-\frac6x)-2$ oscillates between $-7$ and $3$, so the limit does not exist; “none of these” is the only correct label.",
  r"$-5\sin(1-\frac6x)-2$ 在 $-7$ 与 $3$ 之间振荡，极限不存在。选项未列 DNE，故选\"以上都不对\"。")
e(69, r"$\sin(3+\frac4x)$ oscillates as $x\to0$, so $-\sin(3+\frac4x)-3$ has no limit.",
  r"$\sin(3+\frac4x)$ 在 $x\to0$ 时振荡，故整体极限不存在。")
e(70, r"The oscillation of $\sin(2-\frac5x)$ survives the affine shift, so the limit is DNE.",
  r"$\sin(2-\frac5x)$ 的振荡不会被常数项与系数抹平，极限不存在。")

# ---- 2.5 0/0 by factoring ----
e(71, r"The numerator factors as $-(3x-4)(x+5)$, so after cancelling $x+5$ the limit is $-(3x-4)\to19$. Not listed, so “none of these”.",
  r"分子分解为 $-(3x-4)(x+5)$，约去 $x+5$ 后极限为 $-(3x-4)\to19$。选项中没有 $19$，故选\"以上都不对\"。")
e(72, r"Numerator $-(3x-4)(x+5)$, denominator $-(x+5)(x+6)$; after cancelling, $\frac{3x-4}{x+6}\to\frac{-19}{1}=-19$, which is not among the choices.",
  r"分子 $-(3x-4)(x+5)$、分母 $-(x+5)(x+6)$，约分后为 $\frac{3x-4}{x+6}\to-19$，选项中不存在，故为\"以上都不对\"。")
e(73, r"$5x^{2}+20x-25=5(x+5)(x-1)$, so the limit is $5(x-1)\to5(-6)=-30$.",
  r"分子提出 $5$ 后为 $5(x+5)(x-1)$，约去 $x+5$ 得 $5(x-1)\to-30$。")
e(74, r"Numerator $(3x+2)(x+4)$, denominator $-(x+3)(x+4)$; the limit is $\frac{3x+2}{-(x+3)}\to\frac{-10}{1}=-10$.",
  r"分子 $(3x+2)(x+4)$、分母 $-(x+3)(x+4)$，约分后代入 $x=-4$ 得 $-10$。")
e(75, r"$x^{2}+3x+2=(x+1)(x+2)$, so the limit is $x+1\to-1$.",
  r"分子为 $(x+1)(x+2)$，约去 $x+2$ 后得 $x+1\to-1$。")
e(76, r"$4x^{2}-26x+30=2(2x-3)(x-5)$ and $-x^{2}+13x-40=-(x-5)(x-8)$, so the limit is $\frac{2(2x-3)}{-(x-8)}\to\frac{14}{3}$.",
  r"分子 $2(2x-3)(x-5)$、分母 $-(x-5)(x-8)$，约分后代入 $x=5$ 得 $\frac{14}{3}$。")
e(77, r"$2x^{2}+4x-16=2(x+4)(x-2)$, so the limit is $2(x-2)\to-12$.",
  r"分子提出 $2$ 得 $2(x+4)(x-2)$，约去 $x+4$ 后为 $2(x-2)\to-12$。")
e(78, r"$-4x^{2}+x+5=-(4x-5)(x+1)$, so the limit is $-(4x-5)\to9$.",
  r"分子为 $-(4x-5)(x+1)$，约去 $x+1$ 后得 $-(4x-5)\to9$。")
e(79, r"Numerator $(2x-3)(x-4)$, denominator $-(2x+3)(x-4)$; the limit is $\frac{2x-3}{-(2x+3)}\to-\frac{5}{11}$.",
  r"分子 $(2x-3)(x-4)$、分母 $-(2x+3)(x-4)$，约分后得 $-\frac{5}{11}$。")
e(80, r"$x^{3}-8=(x-2)(x^{2}+2x+4)$ and $x^{2}-x-2=(x-2)(x+1)$, so the limit is $\frac{x^{2}+2x+4}{x+1}\to\frac{12}{3}=4$.",
  r"立方差 $x^3-8=(x-2)(x^2+2x+4)$，分母 $(x-2)(x+1)$；约分后代入 $x=2$ 得 $4$。")

# ---- 2.6 direct substitution ----
e(81, r"Substitution is legal here because the denominator is not zero: $\frac{\sqrt{10-6}}{6-14}=\frac{2}{-8}=-\frac14$. Not listed, hence “none of these”.",
  r"分母非零，可直接代入：分子 $\sqrt{4}=2$，分母 $6-14=-8$，得 $-\frac14$。选项中无此值，故选\"以上都不对\"。")
e(82, r"Direct substitution: $\frac{\sqrt{10-3}}{-4}=\frac{\sqrt7}{-4}=-\frac{\sqrt7}{4}$. Keep the minus sign from the denominator.",
  r"直接代入得 $\frac{\sqrt{10-3}}{-4}=-\frac{\sqrt7}{4}$。分母的负号不能丢，这是本题唯一的陷阱。")
e(83, r"$\sqrt{-3(16)+4(-4)+68}=\sqrt4=2$ and $4(-4)+9=-7$, so the limit is $-\frac27$ — not among the options.",
  r"分子为 $\sqrt{4}=2$，分母 $4(-4)+9=-7$，极限为 $-\frac27$，选项中没有，故选\"以上都不对\"。")
e(84, r"The denominator is non-zero at $x=1$, so substitute: $\frac{\sqrt{7-1}}{2-1}=\sqrt6$.",
  r"$x=1$ 处分母不为零，直接代入得 $\sqrt6$。不要把\"根号\"误当成需要有理化的信号。")
e(85, r"At $x=-3$: numerator $\sqrt{6-4}=\sqrt2$, denominator $-6+11=5$, so the limit is $\frac{\sqrt2}{5}$.",
  r"$x=-3$ 时分子 $\sqrt{2}$、分母 $5$，故极限为 $\frac{\sqrt2}{5}$。")

# ---- 2.7 algebra of known limits ----
e(86, r"Use the limit laws: $2(-3)^{3}\cdot\frac{\sqrt{36}}{8}=2(-27)\cdot\frac{6}{8}=-\frac{81}{2}$.",
  r"用极限的四则运算直接组装：$2\cdot(-27)\cdot\frac{6}{8}=-\frac{81}{2}$。根号与三次方都可以分开算。")
e(87, r"$3(-3)^{3}\cdot\frac{\sqrt{25}}{-10}=\frac{3(-27)(5)}{-10}=\frac{81}{2}$.",
  r"$3\cdot(-27)\cdot\frac{5}{-10}=\frac{81}{2}$。注意分母为负，最终结果为正。")
e(88, r"$4(3)^{3}\cdot\frac{6}{7}=\frac{648}{7}$.",
  r"$4\cdot27\cdot\frac67=\frac{648}{7}$。先算 $[f]^{3}$，再乘根号，最后除以 $h$。")
e(89, r"$-(-4)^{3}\cdot\frac{\sqrt4}{4}=\frac{64\cdot2}{4}=32$.",
  r"$-(-4)^3=64$，再乘 $\frac{2}{4}$，得 $32$。负号与立方相互作用，别漏。")
e(90, r"$-2(-2)^{2}\cdot\frac{3}{6}=-2\cdot4\cdot\frac12=-4$.",
  r"$-2\cdot4\cdot\frac{3}{6}=-4$。平方后符号为正，再乘前面的负号。")

# ---- 2.8 rationalising ----
e(91, r"Multiply by the conjugate: $\frac{(4x-18)-(27-5x)}{(x-5)(\sqrt{4x-18}+\sqrt{27-5x})}=\frac{9(x-5)}{(x-5)\cdot2\sqrt2}=\frac{9}{2\sqrt2}=\frac{9\sqrt2}{4}$. Not listed, so “none of these”.",
  r"乘共轭：分子化为 $(4x-18)-(27-5x)=9(x-5)$，分母为 $(x-5)\cdot2\sqrt2$，约分得 $\frac{9}{2\sqrt2}=\frac{9\sqrt2}{4}$。选项中无此值。")
e(92, r"Conjugate gives numerator $(-5x-5)-(5x+15)=-10(x+2)$ over $(x+2)\cdot2\sqrt5$, so the limit is $-\frac{10}{2\sqrt5}=-\sqrt5$ — not among the choices.",
  r"乘共轭后分子为 $-10(x+2)$，分母 $(x+2)\cdot2\sqrt5$，极限 $-\sqrt5$，选项中不存在。")
e(93, r"Conjugate: numerator $(2x+20)-(10-3x)=5(x+2)$ over $(x+2)\cdot8$, giving $\frac58$ — not listed.",
  r"乘共轭后分子 $5(x+2)$、分母 $(x+2)\cdot8$，得 $\frac58$，选项中没有。")
e(94, r"Conjugate: $(4x-7)-(3-x)=5(x-2)$ over $(x-2)(1+1)$, so the limit is $\frac52$.",
  r"乘共轭：分子 $(4x-7)-(3-x)=5(x-2)$，分母 $(x-2)(\sqrt1+\sqrt1)=2(x-2)$，得 $\frac52$。")
e(95, r"Conjugate: numerator $(2x+22)-(4x+28)=-2(x+3)$ over $(x+3)(4+4)$, so the limit is $-\frac{2}{8}=-\frac14$ — not among the options.",
  r"乘共轭后分子 $-2(x+3)$、分母 $8(x+3)$，得 $-\frac14$，选项中没有，故选\"以上都不对\"。")

# ---- 2.9 one-sided infinite limit ----
e(96, r"As $x\to4^{+}$, $x-4\to0^{+}$, so $\frac{1}{x-4}\to+\infty$ and the negative makes it $-\infty$.",
  r"$x\to4^{+}$ 时 $x-4\to0^{+}$，故 $\frac{1}{x-4}\to+\infty$，前面带负号即 $-\infty$。判断符号是这类题的全部内容。")

# ---- 2.10 trigonometric limits ----
e(97, r"Every factor is continuous and the denominator is non-zero at $0$: $\frac{4}{1\cdot\cos\frac{\pi}{3}}=\frac{4}{1/2}=8$.",
  r"各因子在 $0$ 处连续且分母非零，直接代入：$\frac{4}{1\cdot\frac12}=8$。三角函数极限不都要凑 $\frac{\sin u}{u}$。")
e(98, r"Substitute $x=0$: $\frac{4}{1\cdot\cos\frac{\pi}{3}}=8$.",
  r"直接代入 $x=0$ 得 $\frac{4}{1\cdot\frac12}=8$。")
e(99, r"The factors $\cos(2x+\frac{\pi}{4})$ cancel after substitution, leaving $\frac{-4}{-5}=\frac45$.",
  r"代入后 $\cos(2x+\frac{\pi}{4})$ 上下相消，只剩 $\frac{-4}{-5}=\frac45$。$0/0$ 时先看有没有公共因子。")
e(100, r"Substitute: $\frac{(-1)\cos\frac{\pi}{3}}{4}=\frac{-1/2}{4}=-\frac18$.",
  r"代入得 $\frac{-1\cdot\frac12}{4}=-\frac18$。余弦在 $\frac{\pi}{3}$ 处为 $\frac12$。")
e(101, r"$\frac{(0+4)\sin\frac{\pi}{6}}{0+4}=\frac{4\cdot\frac12}{4}=\frac12$.",
  r"代入得 $\frac{4\cdot\frac12}{4}=\frac12$。")
e(102, r"Use $\tan u\sim u$ and $\sin v\sim v$: $\frac{4x}{5x}=\frac45$.",
  r"用等价无穷小 $\tan u\sim u$、$\sin v\sim v$，得 $\frac{4x}{5x}=\frac45$。系数之比就是答案。")
e(103, r"$\frac{\sin8x}{3x}\sim\frac{8x}{3x}=\frac83$.",
  r"$\sin8x\sim8x$，与分母的 $3x$ 相约，得 $\frac83$。")
e(104, r"$\frac{\sin8x}{5x}\to\frac85$.",
  r"$\sin8x\sim8x$，系数之比为 $\frac85$。")
e(105, r"The minus sign survives: $-\frac{\tan7x}{\sin3x}\to-\frac{7}{3}$.",
  r"负号保留：$-\frac{7x}{3x}=-\frac73$。方括号外的负号最容易漏。")
e(106, r"$\frac{\tan8x}{\sin6x}\to\frac{8}{6}=\frac43$.",
  r"$\tan8x\sim8x$、$\sin6x\sim6x$，得 $\frac86=\frac43$。")
e(107, r"Use $1-\cos u\sim\frac{u^{2}}{2}$: $\frac{1-\cos7x}{5x^{2}}\sim\frac{49x^{2}/2}{5x^{2}}=\frac{49}{10}$, with the outer minus giving $-\frac{49}{10}$.",
  r"用 $1-\cos u\sim\frac{u^2}{2}$：$\frac{49x^2/2}{5x^2}=\frac{49}{10}$，再加外层负号得 $-\frac{49}{10}$。")
e(108, r"$\frac{1-\cos2x}{x^{2}}\sim\frac{2x^{2}}{x^{2}}=2$, and the outer minus makes it $-2$.",
  r"$1-\cos2x\sim\frac{(2x)^2}{2}=2x^2$，商为 $2$，带负号得 $-2$。")
e(109, r"$\frac{1-\cos2x}{6x^{2}}\to\frac{2x^{2}}{6x^{2}}=\frac13$.",
  r"分子 $\sim2x^2$，除以 $6x^2$ 得 $\frac13$。")
e(110, r"$\frac{1-\cos5x}{6x^{2}}\to\frac{25}{12}$, so with the minus the value is $-\frac{25}{12}$ — not among the options.",
  r"$\frac{25x^2/2}{6x^2}=\frac{25}{12}$，带负号为 $-\frac{25}{12}$，选项中不存在。")
e(111, r"$\frac{1-\cos8x}{2x^{2}}\to\frac{32x^{2}}{2x^{2}}=16$, so the value is $-16$.",
  r"$1-\cos8x\sim32x^2$，除以 $2x^2$ 得 $16$，带负号为 $-16$。")

# 2.10 continued: x -> infinity and pi/2 cases
e(112, r"With $u=\frac4x\to0$, $\sqrt x\sin\frac4x=\sqrt x\cdot\frac{4}{x}\cdot\frac{\sin u}{u}\to\frac{4}{\sqrt x}\to0$.",
  r"令 $u=\frac4x\to0$，则 $\sqrt x\sin\frac4x\approx\frac{4}{\sqrt x}\to0$。$x$ 在根号里、$\frac1x$ 在分子，量级决定结果。")
e(113, r"The same estimate gives $\frac{4}{\sqrt x}\to0$; the coefficient $-3$ does not change the limit.",
  r"同理得 $\frac{4}{\sqrt x}\to0$，系数 $-3$ 不改变极限。")
e(114, r"$\sqrt x\sin\frac8x\approx\frac{8}{\sqrt x}\to0$, which is not offered.",
  r"$\sqrt x\sin\frac8x\approx\frac{8}{\sqrt x}\to0$，选项中没有 $0$，故选\"以上都不对\"。")
e(115, r"Put $u=x+\frac{\pi}{2}\to0^{+}$; then $\tan(-x-\pi)=\cot u\sim\frac1u$, so the product tends to $\frac{2}{3}$.",
  r"令 $u=x+\frac{\pi}{2}\to0^{+}$，则 $\tan(-x-\pi)=\cot u\sim\frac1u$，乘积趋于 $\frac23$。用余切把小量搬到分子。")
e(116, r"With $u=x-\frac{\pi}{2}$, $\tan(-4x+\frac{5\pi}{2})=\cot(4u)\sim\frac{1}{4u}$; multiplying by $-\frac{6u}{5}$ gives $-\frac{3}{10}$.",
  r"令 $u=x-\frac{\pi}{2}$，则 $\tan(-4x+\frac{5\pi}{2})=\cot4u\sim\frac1{4u}$，乘 $-\frac{6u}{5}$ 得 $-\frac{3}{10}$。")
e(117, r"With $u=x-\frac{\pi}{2}\to0^{+}$, $\tan(-6x+\frac{7\pi}{2})=\cot(6u)\sim\frac{1}{6u}$, and the prefactor $\frac{u}{3}$ leaves $\frac{1}{18}$.",
  r"令 $u=x-\frac{\pi}{2}$，$\tan(-6x+\frac{7\pi}{2})=\cot6u\sim\frac1{6u}$，前面因子 $\frac u3$ 给出 $\frac1{18}$。")
e(118, r"With $u=x+\frac{\pi}{2}\to0^{-}$, $\tan(4x+\frac{3\pi}{2})=-\cot(4u)\sim-\frac{1}{4u}$; the product with $-\frac{4u}{5}$ is $\frac15$.",
  r"令 $u=x+\frac{\pi}{2}\to0^{-}$，$\tan(4x+\frac{3\pi}{2})=-\cot4u\sim-\frac1{4u}$，与 $-\frac{4u}{5}$ 相乘得 $\frac15$。")
e(119, r"With $u=x-\frac{\pi}{2}$, $\tan(2x-\frac{\pi}{2})=-\cot(2u)\sim-\frac{1}{2u}$, and $-\frac{5u}{3}$ times that gives $\frac56$.",
  r"令 $u=x-\frac{\pi}{2}$，$\tan(2x-\frac{\pi}{2})=-\cot2u\sim-\frac1{2u}$，乘 $-\frac{5u}{3}$ 得 $\frac56$。")

# 2.10 continued: expansions at 0
e(120, r"$\sin3t=3t-\frac{9}{2}t^{3}+\cdots$, so numerator $6t-2\sin3t\to9t^{3}$ while the denominator is $\sim3t$; the ratio is $\sim3t^{2}\to0$.",
  r"$\sin3t=3t-\frac92t^3+\cdots$，分子 $6t-2\sin3t\sim9t^3$，分母 $\sim3t$，比值 $\sim3t^2\to0$。线性项抵消时必须看更高阶。")
e(121, r"$2\sin4t=8t-\frac{64}{3}t^{3}+\cdots$, so the numerator is $\sim-\frac{64}{3}t^{3}$ and the ratio tends to $0$.",
  r"展开后线性项抵消，分子为 $O(t^3)$，分母 $O(t)$，故极限为 $0$。")
e(122, r"$\sin3t=3t+O(t^{3})$ cancels the $-8t$ only partly: the ratio of the linear coefficients is $\frac{-8+3}{4}=-\frac54$.",
  r"$\sin3t=3t+O(t^3)$，线性部分为 $-8t+3t=-5t$，除以 $4t$ 得 $-\frac54$。$\sec2t\to1$ 可以先代。")
e(123, r"Linear parts: $6t-2t=4t$, and $\sec3t\to1$, so the limit is $\frac44=1$.",
  r"线性部分 $6t-2t=4t$，$\sec3t\to1$，故极限为 $1$。")
e(124, r"Linear parts give $7t-4t=3t$ over $4t$, so the limit is $\frac34$.",
  r"线性部分 $7t-4t=3t$，除以 $4t$ 得 $\frac34$。")

# ---- 2.11 squeeze ----
e(125, r"$|\sin\frac{7}{x^{2}}|\le1$ while $3x^{3}\to0$, so the product is squeezed to $0$.",
  r"$\sin$ 有界而 $3x^3\to0$，由夹逼定理乘积趋于 $0$。有界量乘无穷小仍是无穷小。")
e(126, r"The oscillating term vanishes: $3x^{3}\cos\frac{6}{x}\to0$, leaving $0-3=-3$.",
  r"振荡项被 $x^3$ 压成 $0$，剩下的常数项给出 $-3$。")
