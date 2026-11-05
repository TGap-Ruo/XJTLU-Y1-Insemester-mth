# -*- coding: utf-8 -*-
"""Chapter 1 (Q1-50) bilingual solutions: E[n] = (english, chinese)"""
E = {}


def e(n, en, zh):
    E[n] = (en, zh)


# ---- 1.1 natural domain of a logarithm ----
e(1,
  r"A log needs a strictly positive argument: $-x^{2}-3x+28>0\iff x^{2}+3x-28<0\iff(x+7)(x-4)<0$, so $-7<x<4$. Both ends are excluded because the argument is $0$ there, hence $(-7,4)$.",
  r"真数须严格大于 $0$：两边乘 $-1$ 反转不等号，得 $(x+7)(x-4)<0$，解集 $-7<x<4$。端点处真数为 $0$，一律取不到，故为开区间 $(-7,4)$。")
e(2,
  r"Factor the argument: $x^{2}+2x-15=(x+5)(x-3)>0$. An upward parabola is positive outside its roots, so $x<-5$ or $x>3$.",
  r"真数因式分解 $(x+5)(x-3)>0$。开口向上的抛物线在两根外侧为正，故取外侧区间，端点不含。")
e(3,
  r"$-x^{2}-10x-16>0\iff x^{2}+10x+16<0\iff(x+8)(x+2)<0$, giving $-8<x<-2$.",
  r"乘 $-1$ 得 $x^{2}+10x+16<0$，即 $(x+8)(x+2)<0$。开口向上取内侧，得 $(-8,-2)$。")
e(4,
  r"$-x^{2}-2x+8>0\iff(x+4)(x-2)<0$, so $-4<x<2$.",
  r"化为 $(x+4)(x-2)<0$，开口向上取两根之间，得 $(-4,2)$。")
e(5,
  r"$-x^{2}-7x-6>0\iff(x+6)(x+1)<0$, so $-6<x<-1$.",
  r"化为 $(x+6)(x+1)<0$，取两根之间，得 $(-6,-1)$。")
e(6,
  r"A quotient is positive when numerator and denominator share a sign. Zeros are $x=-5$ and $x=-\tfrac34$; testing $x=0$ gives $\tfrac{5}{3}>0$, so the sign is $+$ outside the interval and the domain is $(-\infty,-5)\cup(-\tfrac34,\infty)$.",
  r"分式为正等价于分子分母同号。临界点 $x=-5$ 与 $x=-\tfrac34$，取 $x=0$ 检验得 $\tfrac53>0$，说明两根外侧为正，故定义域为 $(-\infty,-5)\cup(-\tfrac34,\infty)$。")
e(7,
  r"Zeros of numerator and denominator are $x=-\tfrac53$ and $x=-5$. Testing $x=-2$ gives $\tfrac{1}{3}>0$, so the sign is $+$ only between the roots: $(-5,-\tfrac53)$. The source answer key labels this item \"none of these\", which is an error in that key.",
  r"分子零点 $x=-\tfrac53$，分母零点 $x=-5$。取 $x=-2$ 检验得 $\tfrac13>0$，说明正号只在两根之间，故为 $(-5,-\tfrac53)$。原题库答案标为\"以上都不对\"，属原答案笔误。")
e(8,
  r"Zeros are $x=-\tfrac54$ and $x=-5$. At $x=-2$ the quotient is $\tfrac{3}{3}=1>0$, so the positive region is between the roots: $(-5,-\tfrac54)$.",
  r"两根为 $x=-\tfrac54$ 与 $x=-5$。取 $x=-2$ 得 $\tfrac33=1>0$，正号区间夹在两根之间，故为 $(-5,-\tfrac54)$。")
e(9,
  r"Zeros are $x=-6$ and $x=\tfrac54$. At $x=0$ the quotient is $\tfrac{-6}{-5}>0$, so the domain is the open interval $(-6,\tfrac54)$. The source key again says \"none of these\", which is a key error.",
  r"两根为 $x=-6$ 与 $x=\tfrac54$。取 $x=0$ 得 $\tfrac{-6}{-5}>0$，正号区间在两根之间，故为 $(-6,\tfrac54)$。原答案标为\"以上都不对\"，同样是原答案笔误。")
e(10,
  r"Zeros are $x=-6$ and $x=2$; testing $x=0$ gives $\tfrac{-6}{-2}=3>0$, so the domain is $(-6,2)$.",
  r"两根为 $x=-6$、$x=2$。代 $x=0$ 得 $\tfrac{-6}{-2}=3>0$，取两根之间，得 $(-6,2)$。")

# ---- 1.2 evaluating composite functions ----
e(11,
  r"$(g\circ f)(x_0)$ means $g$ applied to $f(x_0)$: $f(\tfrac{\pi}{6})=3\cdot\tfrac{\pi}{6}=\tfrac{\pi}{2}$, then $g(\tfrac{\pi}{2})=\sec(\pi)=-1$.",
  r"$(g\circ f)(x_0)$ 是先算内层 $f$：$f(\tfrac{\pi}{6})=\tfrac{\pi}{2}$，再代入 $g$ 得 $\sec(\pi)=-1$。顺序反过来会得到完全不同的值。")
e(12,
  r"Inner first: $g(\tfrac{\pi}{6})=\cos\tfrac{\pi}{2}=0$, then $f(0)=2-0=2$.",
  r"先算内层：$g(\tfrac{\pi}{6})=\cos\tfrac{\pi}{2}=0$，再代入 $f$ 得 $f(0)=2$。")
e(13,
  r"$g(\tfrac{\pi}{6})=\tan\tfrac{2\pi}{3}=-\sqrt3$, then $f(-\sqrt3)=2(-\sqrt3)=-2\sqrt3$.",
  r"内层 $g(\tfrac{\pi}{6})=\tan\tfrac{2\pi}{3}=-\sqrt3$，外层 $f$ 只是乘 $2$，得 $-2\sqrt3$。")
e(14,
  r"$g(\tfrac{\pi}{4})=\cos\tfrac{\pi}{2}=0$, so $f(0)=2-2(0)^2=2$.",
  r"$g(\tfrac{\pi}{4})=\cos\tfrac{\pi}{2}=0$，故 $f(0)=2$。余弦在 $\tfrac{\pi}{2}$ 处为零是本题的关键。")
e(15,
  r"$(g\circ f)$: $f(\tfrac{\pi}{3})=\tfrac{2\pi}{3}$, then $\tan\bigl(2\cdot\tfrac{2\pi}{3}\bigr)=\tan\tfrac{4\pi}{3}=\sqrt3$.",
  r"先 $f(\tfrac{\pi}{3})=\tfrac{2\pi}{3}$，再算 $g$ 得 $\tan\tfrac{4\pi}{3}=\sqrt3$。第三象限正切为正。")
e(16,
  r"$g(\tfrac{5\pi}{24})=\cos\tfrac{5\pi}{6}=-\tfrac{\sqrt3}{2}$, so $f=\;2-\bigl(\tfrac{\sqrt3}{2}\bigr)^{2}=2-\tfrac34=\tfrac54$.",
  r"$g(\tfrac{5\pi}{24})=\cos\tfrac{5\pi}{6}=-\tfrac{\sqrt3}{2}$，平方后负号消失，$f=2-\tfrac34=\tfrac54$。")
e(17,
  r"$g(\tfrac{5\pi}{18})=\sec\tfrac{5\pi}{6}=-\tfrac{2}{\sqrt3}$, then $f=2\cdot\bigl(-\tfrac{2}{\sqrt3}\bigr)=-\tfrac{4}{\sqrt3}=-\tfrac{4\sqrt3}{3}$.",
  r"$\sec\tfrac{5\pi}{6}=\tfrac{1}{\cos}=-\tfrac{2}{\sqrt3}$，乘 $2$ 后有理化分母，得 $-\tfrac{4\sqrt3}{3}$。")
e(18,
  r"$g(\tfrac{3\pi}{16})=\tan\tfrac{3\pi}{4}=-1$, so $f=2-(-1)^{2}=1$.",
  r"$\tan\tfrac{3\pi}{4}=-1$，平方为 $1$，故 $f=2-1=1$。")
e(19,
  r"$(g\circ f)$: $f(\tfrac{\pi}{3})=\pi$, and $\tan\pi=0$.",
  r"$f(\tfrac{\pi}{3})=3\cdot\tfrac{\pi}{3}=\pi$，而 $\tan\pi=0$。注意 $\pi$ 是正切的零点。")
e(20,
  r"$g(\tfrac{\pi}{3})=\sec\tfrac{\pi}{3}=2$, so $f=2-2(2)^{2}=-6$.",
  r"$\sec\tfrac{\pi}{3}=2$，平方后乘 $2$ 得 $8$，故 $f=2-8=-6$。")

# ---- 1.3 inverse function ----
e(21,
  r"Write $y=\frac{1-\sqrt{x}}{3\sqrt{x}+1}$ and solve: $y(3\sqrt x+1)=1-\sqrt x\Rightarrow\sqrt x(3y+1)=1-y\Rightarrow\sqrt x=\frac{1-y}{3y+1}$. Squaring gives $f^{-1}(x)=\frac{(x-1)^{2}}{(3x+1)^{2}}$, and $\sqrt x\ge0$ forces $\frac{1-x}{3x+1}\ge0$, i.e. $-\tfrac13<x\le1$.",
  r"把 $y$ 与 $x$ 对调后解出 $\sqrt x=\frac{1-y}{3y+1}$，平方得反函数；再用 $\sqrt x\ge0$ 要求 $\frac{1-x}{3x+1}\ge0$，得定义域 $(-\tfrac13,1]$。定义域不是随便写的，由根号非负决定。")
e(22,
  r"$y(5\sqrt x+2)=2-3\sqrt x\Rightarrow\sqrt x=\frac{2-2y}{5y+3}$, so $f^{-1}(x)=\frac{4(1-x)^{2}}{(5x+3)^{2}}$ with $\frac{2-2x}{5x+3}\ge0$, i.e. $-\tfrac35<x\le1$.",
  r"同法解出 $\sqrt x=\frac{2-2y}{5y+3}$，分子提出 $2$ 后平方得 $4(1-x)^2$；定义域由 $\sqrt x\ge0$ 定出 $(-\tfrac35,1]$。")
e(23,
  r"$y(\sqrt x+3)=1-2\sqrt x\Rightarrow\sqrt x=\frac{1-3y}{y+2}$, so $f^{-1}(x)=\frac{(3x-1)^{2}}{(x+2)^{2}}$ with $x\in(-2,\tfrac13]$.",
  r"解出 $\sqrt x=\frac{1-3y}{y+2}$，平方后分子写成 $(3x-1)^2$ 更整齐；定义域由非负性得 $(-2,\tfrac13]$。")
e(24,
  r"$y(2\sqrt x+1)=2-\sqrt x\Rightarrow\sqrt x=\frac{2-y}{2y+1}$, giving $f^{-1}(x)=\frac{(x-2)^{2}}{(2x+1)^{2}}$ on $(-\tfrac12,2]$.",
  r"解出 $\sqrt x=\frac{2-y}{2y+1}$，平方得反函数；要求 $\frac{2-x}{2x+1}\ge0$，得 $(-\tfrac12,2]$。")
e(25,
  r"$y(2\sqrt x+3)=2-3\sqrt x\Rightarrow\sqrt x=\frac{2-3y}{2y+3}$, so $f^{-1}(x)=\frac{(3x-2)^{2}}{(2x+3)^{2}}$ on $(-\tfrac32,\tfrac23]$.",
  r"解出 $\sqrt x=\frac{2-3y}{2y+3}$，平方得反函数；由 $\sqrt x\ge0$ 得 $(-\tfrac32,\tfrac23]$。")

# ---- 1.4a principal values, same function ----
e(26,
  r"Reduce the angle modulo $2\pi$: $\frac{34\pi}{7}=4\pi+\frac{6\pi}{7}$, and $\cos$ has period $2\pi$, so the value is $\cos\frac{6\pi}{7}$. Since $\frac{6\pi}{7}\in[0,\pi]$, $\arccos$ returns it unchanged.",
  r"先化角：$\frac{34\pi}{7}-4\pi=\frac{6\pi}{7}$，余弦以 $2\pi$ 为周期。$\frac{6\pi}{7}$ 落在 $\arccos$ 的值域 $[0,\pi]$ 内，直接取它。")
e(27,
  r"$\frac{17\pi}{7}-2\pi=\frac{3\pi}{7}$, which already lies in $[0,\pi]$, so $\arccos\bigl(\cos\frac{17\pi}{7}\bigr)=\frac{3\pi}{7}$.",
  r"减去一个 $2\pi$ 得 $\frac{3\pi}{7}$，已在 $[0,\pi]$ 内，故结果就是它。")
e(28,
  r"$\cos$ is even, so $\cos(-\frac{\pi}{5})=\cos\frac{\pi}{5}$; $\frac{\pi}{5}\in[0,\pi]$ gives $\frac{\pi}{5}$ directly.",
  r"余弦是偶函数，$\cos(-\frac{\pi}{5})=\cos\frac{\pi}{5}$，且 $\frac{\pi}{5}$ 在 $[0,\pi]$ 内，故答案为 $\frac{\pi}{5}$。")
e(29,
  r"$\frac{9\pi}{7}$ exceeds $\pi$, so replace it by $2\pi-\frac{9\pi}{7}=\frac{5\pi}{7}$ (same cosine), which is inside $[0,\pi]$.",
  r"$\frac{9\pi}{7}>\pi$，超出值域。用 $\cos(2\pi-\theta)=\cos\theta$ 换成 $\frac{5\pi}{7}$，落在 $[0,\pi]$ 内。")
e(30,
  r"$\frac{72\pi}{7}-10\pi=\frac{2\pi}{7}$, inside $[0,\pi]$, so the principal value is $\frac{2\pi}{7}$.",
  r"减去 $10\pi$（$2\pi$ 的整数倍）得 $\frac{2\pi}{7}$，落在 $[0,\pi]$ 内，即为主值。")
e(31,
  r"$\frac{26\pi}{5}-4\pi=\frac{6\pi}{5}$, and $\sin\frac{6\pi}{5}=-\sin\frac{\pi}{5}$. As $-\frac{\pi}{5}\in[-\frac{\pi}{2},\frac{\pi}{2}]$, the answer is $-\frac{\pi}{5}$.",
  r"$\frac{26\pi}{5}-4\pi=\frac{6\pi}{5}$，而 $\sin\frac{6\pi}{5}=-\sin\frac{\pi}{5}$。$-\frac{\pi}{5}$ 在 $\arcsin$ 的值域内，故为 $-\frac{\pi}{5}$。")
e(32,
  r"$-\frac{59\pi}{7}+8\pi=-\frac{3\pi}{7}$, which is already inside $[-\frac{\pi}{2},\frac{\pi}{2}]$, so the principal value is $-\frac{3\pi}{7}$.",
  r"加 $8\pi$ 得 $-\frac{3\pi}{7}$，已在 $[-\frac{\pi}{2},\frac{\pi}{2}]$ 内，直接取它。")
e(33,
  r"$\frac{27\pi}{7}-4\pi=-\frac{\pi}{7}\in[-\frac{\pi}{2},\frac{\pi}{2}]$, so the value is $-\frac{\pi}{7}$.",
  r"减 $4\pi$ 得 $-\frac{\pi}{7}$，落在 $\arcsin$ 的值域内，故答案为 $-\frac{\pi}{7}$。")
e(34,
  r"$\frac{48\pi}{7}-6\pi=\frac{6\pi}{7}$; then $\sin\frac{6\pi}{7}=\sin\frac{\pi}{7}$ (supplementary angles), and $\frac{\pi}{7}$ is inside the range.",
  r"减去 $6\pi$ 得 $\frac{6\pi}{7}$。用 $\sin(\pi-\theta)=\sin\theta$ 化到 $\frac{\pi}{7}$，落在值域内。")
e(35,
  r"$-\frac{47\pi}{7}+6\pi=-\frac{5\pi}{7}$; then $\sin(-\frac{5\pi}{7})=-\sin\frac{2\pi}{7}$, and $-\frac{2\pi}{7}$ lies in $[-\frac{\pi}{2},\frac{\pi}{2}]$.",
  r"加 $6\pi$ 得 $-\frac{5\pi}{7}$，再用 $\sin(\pi-\theta)=\sin\theta$ 化为 $-\sin\frac{2\pi}{7}$，故主值为 $-\frac{2\pi}{7}$。")
e(36,
  r"$\tan$ has period $\pi$: $-\frac{29\pi}{7}+4\pi=-\frac{\pi}{7}$, which is inside $(-\frac{\pi}{2},\frac{\pi}{2})$.",
  r"正切以 $\pi$ 为周期，加 $4\pi$ 得 $-\frac{\pi}{7}$，落在 $(-\frac{\pi}{2},\frac{\pi}{2})$ 内。")
e(37,
  r"$\frac{66\pi}{7}-8\pi=\frac{10\pi}{7}$; subtracting one more $\pi$ gives $\frac{3\pi}{7}$, inside $(-\frac{\pi}{2},\frac{\pi}{2})$.",
  r"减 $8\pi$ 得 $\frac{10\pi}{7}$，再减 $\pi$ 得 $\frac{3\pi}{7}$。正切周期为 $\pi$，可以反复加减。")
e(38,
  r"$-\frac{2\pi}{7}$ already lies in $(-\frac{\pi}{2},\frac{\pi}{2})$, so $\tan^{-1}\bigl(\tan(-\frac{2\pi}{7})\bigr)=-\frac{2\pi}{7}$.",
  r"$-\frac{2\pi}{7}$ 已在 $(-\frac{\pi}{2},\frac{\pi}{2})$ 内，无需化角，直接取原值。")
e(39,
  r"$-\frac{7\pi}{5}+\pi=-\frac{2\pi}{5}$, which is inside $(-\frac{\pi}{2},\frac{\pi}{2})$, so the value is $-\frac{2\pi}{5}$.",
  r"加一个 $\pi$ 得 $-\frac{2\pi}{5}$，落在值域内，故为 $-\frac{2\pi}{5}$。")
e(40,
  r"$\frac{20\pi}{7}-2\pi=\frac{6\pi}{7}$, which exceeds $\frac{\pi}{2}$; subtracting $\pi$ gives $-\frac{\pi}{7}$, inside the range.",
  r"减 $2\pi$ 得 $\frac{6\pi}{7}>\frac{\pi}{2}$，再减 $\pi$ 得 $-\frac{\pi}{7}$，落在 $(-\frac{\pi}{2},\frac{\pi}{2})$ 内。")

# ---- 1.4b converting between inverse trig functions ----
e(41,
  r"$\sin(-\frac{23\pi}{5})=-\sin\frac{3\pi}{5}$, and $\sin\frac{3\pi}{5}=\cos\frac{\pi}{10}$. So the expression is $\arccos(-\cos\frac{\pi}{10})=\pi-\frac{\pi}{10}=\frac{9\pi}{10}$.",
  r"先化角：$\sin(-\frac{23\pi}{5})=-\sin\frac{3\pi}{5}$。再用 $\sin\theta=\cos(\frac{\pi}{2}-\theta)$ 转成余弦，最后用 $\arccos(-u)=\pi-\arccos u$ 得 $\frac{9\pi}{10}$。")
e(42,
  r"$\cos(-\frac{8\pi}{7})=\cos\frac{8\pi}{7}=\cos\frac{6\pi}{7}=-\cos\frac{\pi}{7}$. Hence $\arcsin(-\cos\frac{\pi}{7})=-\arcsin(\cos\frac{\pi}{7})=-\bigl(\frac{\pi}{2}-\frac{\pi}{7}\bigr)=-\frac{5\pi}{14}$.",
  r"$\cos\frac{8\pi}{7}=\cos\frac{6\pi}{7}=-\cos\frac{\pi}{7}$。用 $\arcsin(\cos\theta)=\frac{\pi}{2}-\theta$ 与奇函数性质，得 $-\frac{5\pi}{14}$。")
e(43,
  r"$\cos(-\frac{5\pi}{7})=\cos\frac{5\pi}{7}=-\cos\frac{2\pi}{7}$, so the value is $-\arcsin(\cos\frac{2\pi}{7})=-\bigl(\frac{\pi}{2}-\frac{2\pi}{7}\bigr)=-\frac{3\pi}{14}$.",
  r"$\cos\frac{5\pi}{7}=-\cos\frac{2\pi}{7}$，再用 $\arcsin(\cos\theta)=\frac{\pi}{2}-\theta$，得 $-\frac{3\pi}{14}$。")
e(44,
  r"$\frac{30\pi}{7}-4\pi=\frac{2\pi}{7}$, so $\cos\frac{30\pi}{7}=\cos\frac{2\pi}{7}$ and $\arcsin(\cos\frac{2\pi}{7})=\frac{\pi}{2}-\frac{2\pi}{7}=\frac{3\pi}{14}$.",
  r"减 $4\pi$ 得 $\frac{2\pi}{7}$。用 $\arcsin(\cos\theta)=\frac{\pi}{2}-\theta$（$\theta\in[0,\frac{\pi}{2}]$）得 $\frac{3\pi}{14}$。")
e(45,
  r"$\frac{24\pi}{7}-2\pi=\frac{10\pi}{7}$ and $\cos\frac{10\pi}{7}=\cos\frac{4\pi}{7}=-\cos\frac{3\pi}{7}$, so the value is $-\arcsin(\cos\frac{3\pi}{7})=-\bigl(\frac{\pi}{2}-\frac{3\pi}{7}\bigr)=-\frac{\pi}{14}$.",
  r"$\frac{24\pi}{7}-2\pi=\frac{10\pi}{7}$，且 $\cos\frac{10\pi}{7}=\cos\frac{4\pi}{7}=-\cos\frac{3\pi}{7}$。再用余角关系得 $-\frac{\pi}{14}$。")

# ---- 1.4c nested inverse trig ----
e(46,
  r"Let $\theta=\arccos\frac{2}{7}$; then $\cos\theta=\frac27$ with $\theta\in(0,\frac{\pi}{2})$ and $\sin\theta=\sqrt{1-\frac{4}{49}}=\frac{\sqrt{45}}{7}=\frac{3\sqrt5}{7}$. This value is not listed, so none of the four options is correct.",
  r"设 $\theta=\arccos\frac27$，则 $\cos\theta=\frac27$，$\sin\theta=\sqrt{1-\frac{4}{49}}=\frac{3\sqrt5}{7}$。四个选项里没有这个值，故选\"以上都不对\"。")
e(47,
  r"With $\cos\theta=-\frac29$ and $\theta\in(\frac{\pi}{2},\pi)$, $\sin\theta=+\sqrt{1-\frac{4}{81}}=\frac{\sqrt{77}}{9}$.",
  r"$\cos\theta=-\frac29$ 且 $\theta$ 在第二象限，正弦取正：$\sqrt{1-\frac{4}{81}}=\frac{\sqrt{77}}{9}$。")
e(48,
  r"Draw the right triangle for $\sin\theta=\frac17$: opposite $1$, hypotenuse $7$, adjacent $\sqrt{49-1}=4\sqrt3$. Then $\cos\theta=\frac{4\sqrt3}{7}$ and $\sec\theta=\frac{7}{4\sqrt3}=\frac{7\sqrt3}{12}$.",
  r"由 $\sin\theta=\frac17$ 画直角三角形：对边 $1$、斜边 $7$、邻边 $\sqrt{49-1}=4\sqrt3$。故 $\cos\theta=\frac{4\sqrt3}{7}$，$\sec\theta=\frac{7}{4\sqrt3}=\frac{7\sqrt3}{12}$（分母有理化）。")
e(49,
  r"$\tan\theta=-4$: take opposite $-4$, adjacent $1$, hypotenuse $\sqrt{17}$, so $\sec\theta=\sqrt{17}$.",
  r"$\tan\theta=-4$ 画三角形：邻边 $1$、对边 $-4$、斜边 $\sqrt{17}$，故 $\sec\theta=\sqrt{17}$。正割为正，因为 $\cos>0$。")
e(50,
  r"$\tan\theta=-\frac14$ gives hypotenuse $\sqrt{1+\frac{1}{16}}=\frac{\sqrt{17}}{4}$, and $\sec\theta=\frac{\sqrt{17}}{4}$.",
  r"$\tan\theta=-\frac14$，斜边为 $\sqrt{1+\frac1{16}}=\frac{\sqrt{17}}{4}$，故 $\sec\theta=\frac{\sqrt{17}}{4}$。")
