# -*- coding: utf-8 -*-
"""Lecture 1-2 题目：T1.1-T2.11。q(t, 题干, 正确项, [干扰项...], 解析)"""

Q = []
def q(t, stem, correct, wrongs, sol):
    Q.append(dict(t=t, q=stem, c=correct, w=list(wrongs), s=sol))

# ---------------- T1.1 对数函数自然定义域 ----------------
q("T1.1", r"求 $f(x)=\log_2(x^2+2x-15)$ 的自然定义域。",
  r"$(-\infty,-5)\cup(3,\infty)$",
  [r"$(-5,3)$", r"$[-5,3]$", r"$(-\infty,3)\cup(5,\infty)$"],
  r"真数须为正：$x^2+2x-15=(x+5)(x-3)>0$。两根 $-5,3$，开口向上取外侧，得 $(-\infty,-5)\cup(3,\infty)$。严格不等号，端点不含。")
q("T1.1", r"求 $f(x)=\log_3(-x^2-2x+8)$ 的自然定义域。",
  r"$(-4,2)$",
  [r"$(-\infty,-4)\cup(2,\infty)$", r"$[-4,2]$", r"$(-\infty,-4]$"],
  r"需 $-x^2-2x+8>0$，即 $x^2+2x-8<0$，$(x+4)(x-2)<0$，得 $-4<x<2$。二次项系数为负时先乘 $-1$ 变号，不等号方向随之翻转。")
q("T1.1", r"求 $f(x)=\log_5\dfrac{x+6}{2-x}$ 的自然定义域。",
  r"$(-6,2)$",
  [r"$(-\infty,-6)\cup(2,\infty)$", r"$(-2,6)$", r"$[-6,2)$"],
  r"需 $\dfrac{x+6}{2-x}>0$。临界点 $x=-6,2$，取 $x=0$ 检验得 $3>0$，故解集 $(-6,2)$；分母零点 $x=2$ 已被严格不等式排除。")
q("T1.1", r"求 $f(x)=\log_3\dfrac{x-1}{x+2}$ 的自然定义域。",
  r"$(-\infty,-2)\cup(1,\infty)$",
  [r"$(-2,1)$", r"$(-\infty,1)\cup(2,\infty)$", r"$(1,\infty)$"],
  r"分式 $>0$ 当且仅当分子分母同号：$x>1$ 或 $x<-2$。取点检验：$x=0$ 得 $-\frac12<0$（不在），$x=-3$ 得 $4>0$（在）。")

# ---------------- T1.2 复合函数 ----------------
q("T1.2", r"设 $f(x)=\sqrt{x+2}$，$g(x)=\dfrac{1}{x-1}$，求 $(f\circ g)(x)$ 及其定义域。",
  r"$\sqrt{\dfrac{2x-1}{x-1}}$，$\left(-\infty,\frac12\right]\cup(1,\infty)$",
  [r"$\sqrt{\dfrac{2x-1}{x-1}}$，$\left[\frac12,\infty\right)$",
   r"$\dfrac{1}{\sqrt{x+2}-1}$，$(-2,\infty)$",
   r"$\sqrt{\dfrac{2x+1}{x-1}}$，$\left(\frac12,\infty\right)$"],
  r"$(f\circ g)(x)=\sqrt{\frac{1}{x-1}+2}=\sqrt{\frac{2x-1}{x-1}}$。需 $x\neq1$ 且 $\frac{2x-1}{x-1}\ge0$：临界点 $\frac12,1$，取 $x=0$ 得 $1>0$，取外侧两段，含 $\frac12$、不含 $1$。")
q("T1.2", r"设 $f(x)=x^2+1$，$g(x)=\sqrt{2-x}$，求 $(f\circ g)(x)$ 及其定义域。",
  r"$3-x$，$(-\infty,2]$",
  [r"$3-x$，$[2,\infty)$", r"$\sqrt{2-x^2-1}$，$[-1,1]$", r"$2-x^2$，$\mathbb{R}$"],
  r"内层须 $2-x\ge0\Rightarrow x\le2$；$g$ 的值域 $[0,\infty)$ 全部落在 $f$ 的定义域 $\mathbb{R}$ 内，无需额外限制。故 $(f\circ g)(x)=3-x$，$x\le2$。")
q("T1.2", r"设 $f(x)=\dfrac{1}{x-3}$，$g(x)=\sqrt{x+1}$，求 $(g\circ f)(x)$ 的定义域。",
  r"$(-\infty,2]\cup(3,\infty)$",
  [r"$[-1,3)\cup(3,\infty)$", r"$(3,\infty)$", r"$[-1,\infty)$"],
  r"$(g\circ f)(x)=\sqrt{\frac{1}{x-3}+1}=\sqrt{\frac{x-2}{x-3}}$。需 $x\neq3$ 且 $\frac{x-2}{x-3}\ge0$，取 $x=0$ 得 $\frac23>0$，故 $(-\infty,2]\cup(3,\infty)$。")
q("T1.2", r"设 $f(x)=2x+1$，$g(x)=x^2$，求 $(f\circ g)(3)-(g\circ f)(3)$。",
  r"$-30$", [r"$-18$", r"$30$", r"$12$"],
  r"$(f\circ g)(3)=f(9)=19$，$(g\circ f)(3)=g(7)=49$，差 $-30$。$f\circ g\neq g\circ f$，必须由内向外逐层代入。")

# ---------------- T1.3 反函数 ----------------
q("T1.3", r"求 $f(x)=\dfrac{2x-1}{x+3}$ 的反函数及其定义域。",
  r"$f^{-1}(x)=\dfrac{3x+1}{2-x}$，$x\neq2$",
  [r"$f^{-1}(x)=\dfrac{3x+1}{x-2}$，$x\neq2$",
   r"$f^{-1}(x)=\dfrac{x+3}{2x-1}$，$x\neq\frac12$",
   r"$f^{-1}(x)=\dfrac{1-3x}{x+2}$，$x\neq-2$"],
  r"$y(x+3)=2x-1\Rightarrow x(y-2)=-3y-1\Rightarrow x=\dfrac{3y+1}{2-y}$。交换得 $f^{-1}(x)=\dfrac{3x+1}{2-x}$；定义域即原值域 $y\neq2$。")
q("T1.3", r"设 $f(x)=x^2-4x+7$（$x\ge2$），求 $f^{-1}(x)$。",
  r"$2+\sqrt{x-3}$，$[3,\infty)$",
  [r"$2-\sqrt{x-3}$，$[3,\infty)$", r"$\sqrt{x-3}+4$，$[3,\infty)$", r"$2+\sqrt{x+3}$，$[-3,\infty)$"],
  r"配方 $y=(x-2)^2+3$。因 $x\ge2$ 取正支：$x=2+\sqrt{y-3}$，故 $f^{-1}(x)=2+\sqrt{x-3}$，定义域为原值域 $[3,\infty)$。限定 $x\ge2$ 正是为保证一一对应。")
q("T1.3", r"求 $f(x)=e^{2x-1}$ 的反函数及其定义域。",
  r"$f^{-1}(x)=\dfrac{\ln x+1}{2}$，$(0,\infty)$",
  [r"$f^{-1}(x)=\dfrac{\ln x-1}{2}$，$(0,\infty)$",
   r"$f^{-1}(x)=\ln(2x-1)$，$\left(\frac12,\infty\right)$",
   r"$f^{-1}(x)=2\ln x+1$，$(0,\infty)$"],
  r"$y=e^{2x-1}\Rightarrow\ln y=2x-1\Rightarrow x=\dfrac{\ln y+1}{2}$。原函数值域 $(0,\infty)$ 即新定义域。")
q("T1.3", r"设 $f(x)=3+\sqrt{x-1}$（$x\ge1$），求 $f^{-1}(x)$。",
  r"$(x-3)^2+1$，$[3,\infty)$",
  [r"$(x-3)^2+1$，$[1,\infty)$", r"$(x+3)^2-1$，$[3,\infty)$", r"$\sqrt{x-3}+1$，$[3,\infty)$"],
  r"$y-3=\sqrt{x-1}\Rightarrow x=(y-3)^2+1$。$x\ge1$ 时 $y\ge3$，故 $f^{-1}(x)=(x-3)^2+1$，$x\ge3$。反函数定义域必须是原函数值域。")

# ---------------- T1.4 反三角 ----------------
q("T1.4", r"求 $\arccos\left(-\dfrac{\sqrt3}{2}\right)$。",
  r"$\dfrac{5\pi}{6}$", [r"$\dfrac{\pi}{6}$", r"$-\dfrac{\pi}{6}$", r"$\dfrac{2\pi}{3}$"],
  r"$\arccos$ 值域 $[0,\pi]$。由 $\arccos(-u)=\pi-\arccos u$，$\arccos\frac{\sqrt3}{2}=\frac\pi6$，故为 $\pi-\frac\pi6=\frac{5\pi}{6}$。")
q("T1.4", r"求 $\tan\left(\arcsin\dfrac35\right)$。",
  r"$\dfrac34$", [r"$\dfrac43$", r"$\dfrac35$", r"$\dfrac54$"],
  r"设 $\theta=\arcsin\frac35$，则 $\sin\theta=\frac35$，$\theta\in[0,\frac\pi2]$，邻边 $\sqrt{25-9}=4$，$\tan\theta=\frac34$。画直角三角形最稳。")
q("T1.4", r"求 $\cos\left(2\arcsin\dfrac13\right)$。",
  r"$\dfrac79$", [r"$-\dfrac79$", r"$\dfrac{2\sqrt2}{3}$", r"$\dfrac13$"],
  r"设 $\theta=\arcsin\frac13$，$\sin\theta=\frac13$，用 $\cos2\theta=1-2\sin^2\theta=1-\frac29=\frac79$。")
q("T1.4", r"求 $\arcsin\left(\sin\dfrac{5\pi}{6}\right)$。",
  r"$\dfrac{\pi}{6}$", [r"$\dfrac{5\pi}{6}$", r"$-\dfrac{\pi}{6}$", r"$\dfrac{\pi}{3}$"],
  r"$\sin\frac{5\pi}{6}=\frac12$，$\arcsin\frac12=\frac\pi6$。因 $\frac{5\pi}{6}\notin[-\frac\pi2,\frac\pi2]$，$\arcsin(\sin x)\neq x$——最经典的复合恒等式陷阱。")
q("T1.4", r"求 $\sec(\arctan 2)$。",
  r"$\sqrt5$", [r"$\dfrac{\sqrt5}{2}$", r"$\dfrac{2}{\sqrt5}$", r"$5$"],
  r"设 $\theta=\arctan2$，$\tan\theta=2$。由 $1+\tan^2\theta=\sec^2\theta$ 得 $\sec^2\theta=5$；$\theta\in(0,\frac\pi2)$ 时 $\sec\theta>0$，故 $\sqrt5$。")

# ---------------- T2.1 分段函数在某点的极限 ----------------
q("T2.1", r"设 $f(x)=\begin{cases}x^2+1,&x\neq2\\ 7,&x=2\end{cases}$，求 $\lim\limits_{x\to2}f(x)$。",
  r"$5$", [r"$7$", r"不存在", r"$4$"],
  r"极限只看 $x\to2$ 的去心邻域，用 $x\neq2$ 的分支：$2^2+1=5$。$f(2)=7$ 与极限无关。")
q("T2.1", r"设 $f(x)=\dfrac{x^2-9}{x-3}$（$x\neq3$），且 $f(3)=0$，求 $\lim\limits_{x\to3}f(x)$。",
  r"$6$", [r"$0$", r"不存在", r"$3$"],
  r"$\frac{x^2-9}{x-3}=x+3$（$x\neq3$），极限为 $6$。$x=3$ 处是可去间断，不影响极限。")
q("T2.1", r"设 $f(x)=\begin{cases}2x+1,&x<1\\ x^2+3,&x\ge1\end{cases}$，求 $\lim\limits_{x\to1}f(x)$。",
  r"不存在", [r"$3$", r"$4$", r"$1$"],
  r"左极限 $2(1)+1=3$，右极限 $1+3=4$，两者不等，故极限不存在（跳跃间断）。")

# ---------------- T2.2 左右极限 ----------------
q("T2.2", r"设 $f(x)=\begin{cases}x+3,&x<2\\ x^2-1,&x\ge2\end{cases}$，求 $\lim\limits_{x\to2}f(x)$。",
  r"不存在", [r"$5$", r"$3$", r"$2$"],
  r"左：$x+3\to5$；右：$x^2-1\to3$。左右不等，极限不存在。")
q("T2.2", r"设 $f(x)=\begin{cases}x^2,&x<2\\ 2x,&x\ge2\end{cases}$，求 $\lim\limits_{x\to2}f(x)$。",
  r"$4$", [r"不存在", r"$2$", r"$8$"],
  r"左：$2^2=4$；右：$2\cdot2=4$。左右相等，故极限为 $4$。")
q("T2.2", r"设 $f(x)=\begin{cases}2x-1,&x<1\\ 3x-4,&x\ge1\end{cases}$，求 $\lim\limits_{x\to1}f(x)$。",
  r"不存在", [r"$1$", r"$-1$", r"$0$"],
  r"左：$2-1=1$；右：$3-4=-1$。左右不等，极限不存在。")

# ---------------- T2.3 含绝对值的极限 ----------------
q("T2.3", r"求 $\lim\limits_{x\to3}\dfrac{|x-3|}{x-3}$。",
  r"不存在", [r"$1$", r"$-1$", r"$0$"],
  r"$x>3$ 时 $|x-3|=x-3$，比值为 $1$；$x<3$ 时为 $-(x-3)$，比值 $-1$。左右极限不等，故不存在。")
q("T2.3", r"求 $\lim\limits_{x\to0^+}\dfrac{|x|}{x}$。",
  r"$1$", [r"$-1$", r"$0$", r"不存在"],
  r"$x>0$ 时 $|x|=x$，比值恒为 $1$，右极限为 $1$。（左极限为 $-1$，双侧不存在，注意单侧与双侧的区别。）")
q("T2.3", r"求 $\lim\limits_{x\to1}\dfrac{|x-1|}{x^2-1}$。",
  r"不存在", [r"$\frac12$", r"$-\frac12$", r"$0$"],
  r"$\frac{|x-1|}{(x-1)(x+1)}$。$x>1$ 时约去得 $\frac{1}{x+1}\to\frac12$；$x<1$ 时得 $-\frac{1}{x+1}\to-\frac12$。左右不等，故不存在。")
q("T2.3", r"求 $\lim\limits_{x\to-2^-}\dfrac{|x+2|}{x+2}$。",
  r"$-1$", [r"$1$", r"$0$", r"不存在"],
  r"$x<-2$ 时 $x+2<0$，$|x+2|=-(x+2)$，比值 $-1$。单侧极限只用一个分支，不存在左右比较问题。")

# ---------------- T2.4 极限不存在 ----------------
q("T2.4", r"求 $\lim\limits_{x\to0}\sin\dfrac1x$。",
  r"不存在", [r"$0$", r"$1$", r"$\infty$"],
  r"$x\to0$ 时 $\frac1x\to\pm\infty$，$\sin$ 在 $[-1,1]$ 内无限振荡，不趋向任何定值，故极限不存在。")
q("T2.4", r"求 $\lim\limits_{x\to0}x\sin\dfrac1x$。",
  r"$0$", [r"不存在", r"$1$", r"$\infty$"],
  r"$|\sin\frac1x|\le1$ 有界，$x\to0$ 是无穷小，有界×无穷小 $=0$。与上一题对比：振荡因子被 $x$ 压住了。")
q("T2.4", r"求 $\lim\limits_{x\to2}\dfrac{1}{(x-2)^2}$。",
  r"$+\infty$（极限不存在）", [r"$0$", r"不存在且不趋于无穷", r"$-\infty$"],
  r"分母 $(x-2)^2>0$ 且 $\to0^+$，分子为 $1$，故趋于 $+\infty$。$\infty$ 不是数，严格说极限不存在，只是借记号表示无界增长。")

# ---------------- T2.5 因式分解 ----------------
q("T2.5", r"求 $\lim\limits_{x\to2}\dfrac{x^2-4}{x-2}$。",
  r"$4$", [r"$0$", r"$2$", r"不存在"],
  r"代入为 $\frac00$ 型。$x^2-4=(x-2)(x+2)$，约去 $(x-2)$ 得 $x+2\to4$。")
q("T2.5", r"求 $\lim\limits_{x\to2}\dfrac{x^2-5x+6}{x-2}$。",
  r"$-1$", [r"$1$", r"$0$", r"不存在"],
  r"$x^2-5x+6=(x-2)(x-3)$，约分后 $x-3\to-1$。")
q("T2.5", r"求 $\lim\limits_{x\to2}\dfrac{x^3-8}{x-2}$。",
  r"$12$", [r"$8$", r"$4$", r"$0$"],
  r"立方差 $x^3-8=(x-2)(x^2+2x+4)$，约分后代入 $4+4+4=12$。")
q("T2.5", r"求 $\lim\limits_{x\to2}\dfrac{x^2+3x-10}{x-2}$。",
  r"$7$", [r"$5$", r"$0$", r"不存在"],
  r"$x^2+3x-10=(x-2)(x+5)$，约分后 $x+5\to7$。")

# ---------------- T2.6 直接代入 ----------------
q("T2.6", r"求 $\lim\limits_{x\to4}\sqrt{x+5}$。",
  r"$3$", [r"$9$", r"$\sqrt5$", r"不存在"],
  r"$x=4$ 在定义域内，根式连续，直接代入：$\sqrt{9}=3$。")
q("T2.6", r"求 $\lim\limits_{x\to2}\dfrac{x^2+3x-1}{x+1}$。",
  r"$3$", [r"$\dfrac92$", r"$1$", r"$0$"],
  r"分母 $2+1=3\neq0$，有理函数在定义域内连续，直接代入：$\frac{4+6-1}{3}=3$。")
q("T2.6", r"求 $\lim\limits_{x\to9}\dfrac{\sqrt x+1}{x-1}$。",
  r"$\dfrac12$", [r"$\dfrac{4}{9}$", r"$\dfrac{1}{4}$", r"$4$"],
  r"$x=9$ 处分母 $8\neq0$，直接代入：$\frac{3+1}{8}=\frac12$。")
q("T2.6", r"求 $\lim\limits_{x\to0}\dfrac{3x^2-2x+5}{x^2+1}$。",
  r"$5$", [r"$0$", r"$3$", r"不存在"],
  r"分母 $x^2+1=1\neq0$，直接代入得 $\frac51=5$。")

# ---------------- T2.7 已知极限求组合 ----------------
q("T2.7", r"已知 $\lim\limits_{x\to c}f(x)=3$，$\lim\limits_{x\to c}g(x)=-2$，求 $\lim\limits_{x\to c}[2f(x)-3g(x)]$。",
  r"$12$", [r"$0$", r"$-12$", r"$6$"],
  r"由主极限定理：$2\cdot3-3\cdot(-2)=6+6=12$。")
q("T2.7", r"已知 $\lim\limits_{x\to c}f(x)=3$，$\lim\limits_{x\to c}g(x)=-2$，求 $\lim\limits_{x\to c}\dfrac{f(x)}{g(x)}$。",
  r"$-\dfrac32$", [r"$\dfrac32$", r"$-\dfrac23$", r"不存在"],
  r"商法则要求分母极限非零（$-2\neq0$），直接相除：$\frac{3}{-2}=-\frac32$。")
q("T2.7", r"已知 $\lim\limits_{x\to c}f(x)=3$，$\lim\limits_{x\to c}g(x)=-2$，求 $\lim\limits_{x\to c}\sqrt{f(x)+6}$。",
  r"$3$", [r"$\sqrt3$", r"$9$", r"不存在"],
  r"根号法则要求根号内极限非负：$3+6=9\ge0$，故极限为 $\sqrt9=3$。")
q("T2.7", r"已知 $\lim\limits_{x\to c}f(x)=3$，$\lim\limits_{x\to c}g(x)=-2$，求 $\lim\limits_{x\to c}[f(x)]^2+[g(x)]^3$。",
  r"$1$", [r"$17$", r"$-17$", r"$5$"],
  r"幂法则：$3^2+(-2)^3=9-8=1$。负数的奇次幂仍为负，别丢符号。")

# ---------------- T2.8 有理化 ----------------
q("T2.8", r"求 $\lim\limits_{x\to4}\dfrac{\sqrt x-2}{x-4}$。",
  r"$\dfrac14$", [r"$\dfrac12$", r"$0$", r"不存在"],
  r"乘共轭：$\frac{(\sqrt x-2)(\sqrt x+2)}{(x-4)(\sqrt x+2)}=\frac{x-4}{(x-4)(\sqrt x+2)}=\frac{1}{\sqrt x+2}\to\frac14$。")
q("T2.8", r"求 $\lim\limits_{x\to3}\dfrac{\sqrt{x+1}-2}{x-3}$。",
  r"$\dfrac14$", [r"$\dfrac12$", r"$4$", r"$0$"],
  r"乘共轭 $\sqrt{x+1}+2$，分子化为 $x-3$，约分后得 $\frac{1}{\sqrt{x+1}+2}\to\frac14$。")
q("T2.8", r"求 $\lim\limits_{x\to9}\dfrac{x-9}{\sqrt x-3}$。",
  r"$6$", [r"$3$", r"$0$", r"$12$"],
  r"乘共轭 $\sqrt x+3$：分子 $(x-9)(\sqrt x+3)$，分母 $x-9$，约分后 $\sqrt x+3\to6$。")
q("T2.8", r"求 $\lim\limits_{x\to0}\dfrac{\sqrt{4+x}-2}{x}$。",
  r"$\dfrac14$", [r"$\dfrac12$", r"$2$", r"$0$"],
  r"乘共轭：分子化为 $(4+x)-4=x$，与分母约去，得 $\frac{1}{\sqrt{4+x}+2}\to\frac14$。")

# ---------------- T2.9 单侧无穷极限 ----------------
q("T2.9", r"求 $\lim\limits_{x\to2^+}\dfrac{1}{x-2}$ 与 $\lim\limits_{x\to2^-}\dfrac{1}{x-2}$。",
  r"$+\infty$ 与 $-\infty$", [r"都为 $+\infty$", r"$-\infty$ 与 $+\infty$", r"都为 $0$"],
  r"$x\to2^+$ 时 $x-2\to0^+$，倒数为 $+\infty$；$x\to2^-$ 时 $x-2\to0^-$，倒数为 $-\infty$。两侧符号相反，故双侧极限不存在。")
q("T2.9", r"求 $\lim\limits_{x\to3^-}\dfrac{x+1}{x-3}$。",
  r"$-\infty$", [r"$+\infty$", r"$0$", r"$\dfrac43$"],
  r"分子 $\to4>0$；$x\to3^-$ 时 $x-3\to0^-$。正数除以负无穷小得 $-\infty$。")
q("T2.9", r"求 $\lim\limits_{x\to1^+}\dfrac{2x}{(x-1)^2}$。",
  r"$+\infty$", [r"$-\infty$", r"$0$", r"$2$"],
  r"分子 $\to2>0$，分母 $(x-1)^2\to0^+$ 恒正，故为 $+\infty$。平方使两侧同号。")

# ---------------- T2.10 三角极限 ----------------
q("T2.10", r"求 $\lim\limits_{x\to0}\dfrac{\sin 8x}{3x}$。",
  r"$\dfrac83$", [r"$\dfrac38$", r"$0$", r"$8$"],
  r"$\frac{\sin8x}{8x}\to1$，故原式 $=\frac{8}{3}\cdot1=\frac83$。关键是让角度与分母同阶。")
q("T2.10", r"求 $\lim\limits_{x\to0}\dfrac{\tan 4x}{\sin 5x}$。",
  r"$\dfrac45$", [r"$\dfrac54$", r"$1$", r"$0$"],
  r"$\tan4x\sim4x$，$\sin5x\sim5x$，比值 $\to\frac45$。乘除因子可直接用等价无穷小替换。")
q("T2.10", r"求 $\lim\limits_{x\to0}\dfrac{1-\cos 7x}{x^2}$。",
  r"$\dfrac{49}{2}$", [r"$\dfrac72$", r"$49$", r"$0$"],
  r"用 $1-\cos u\sim\frac{u^2}{2}$，$u=7x$ 得 $\frac{49x^2}{2x^2}=\frac{49}{2}$。也可用半角公式 $\frac{2\sin^2(7x/2)}{x^2}$ 计算。")
q("T2.10", r"求 $\lim\limits_{x\to0}\dfrac{\sin^2 3x}{x^2}$。",
  r"$9$", [r"$3$", r"$6$", r"$1$"],
  r"$\left(\frac{\sin3x}{x}\right)^2=\left(3\cdot\frac{\sin3x}{3x}\right)^2\to9$。")
q("T2.10", r"求 $\lim\limits_{x\to0}\dfrac{(x^2+4)\sin\left(3x+\frac\pi6\right)}{x+4}$。",
  r"$\dfrac12$", [r"$1$", r"$\dfrac18$", r"$0$"],
  r"角度 $\to\frac\pi6$ 为有限值，三角函数连续，直接代入：$\frac{(0+4)\cdot\frac12}{0+4}=\frac12$。")
q("T2.10", r"求 $\lim\limits_{x\to\pi}\dfrac{\sin x}{x-\pi}$。",
  r"$-1$", [r"$1$", r"$0$", r"不存在"],
  r"令 $u=x-\pi\to0$，则 $\sin x=\sin(u+\pi)=-\sin u$，原式 $=\frac{-\sin u}{u}\to-1$。")

# ---------------- T2.11 夹逼 ----------------
q("T2.11", r"求 $\lim\limits_{x\to0}x^2\sin\dfrac1x$。",
  r"$0$", [r"不存在", r"$1$", r"$\infty$"],
  r"$0\le\left|x^2\sin\frac1x\right|\le x^2$，两端 $\to0$，由夹逼定理得 $0$。")
q("T2.11", r"求 $\lim\limits_{x\to\infty}\dfrac{\sin x}{x}$。",
  r"$0$", [r"$1$", r"不存在", r"$\infty$"],
  r"$|\sin x|\le1$，$\frac1x\to0$，有界乘无穷小为 $0$。")
q("T2.11", r"求 $\lim\limits_{n\to\infty}\dfrac{\sin^3 n}{n}$。",
  r"$0$", [r"$1$", r"不存在", r"$\infty$"],
  r"$|\sin^3n|\le1$ 有界，$\frac1n\to0$，故极限为 $0$。数列同样适用夹逼。")
