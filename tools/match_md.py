# -*- coding: utf-8 -*-
"""从 md 文本层重建 351 道题的选项文本，与答案文本比对定 A–E（同源 mangling，一致性好）"""
import json, os, re, difflib
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "extract", "bank.md")
seg = json.load(open(os.path.join(ROOT, "build", "segments.json")))
ans = json.load(open(os.path.join(ROOT, "build", "answers.json")))

DROP = re.compile(r"^(<!-- Page \d+ -->|X J T L U.*|https?://\S+|\d+/\d+$)")
SEC = re.compile(r"^\d\.\d[a-c]?\s")


def load_lines():
    out = []
    for l in open(MD, encoding="utf-8"):
        l = l.rstrip("\n").strip()
        if not l or DROP.match(l):
            continue
        out.append(l)
    # 去掉答案区块（答案编号连续；遇到不连续的编号即视为新题）
    keep, skip, last = [], False, 0
    for l in out:
        if "参考答案" in l:
            skip, last = True, 0
            continue
        if SEC.match(l):
            skip = False
        if skip:
            m = re.match(r"^(\d{1,3})\.\s*(.*)$", l)
            if m:
                n = int(m.group(1))
                if last and n > last + 1:
                    skip = False          # 新题开始
                else:
                    last = n
                    continue
            elif last == 0 and not re.match(r"^\d", l):
                continue                  # 答案块表头说明
            if skip:
                continue
        keep.append(l)
    return keep


def flat(s):
    s = s.replace("−", "-").replace("–", "-")
    s = re.sub(r"\s+", "", s)
    s = s.replace("\\[", "[").replace("\\]", "]")
    s = s.replace("（", "(").replace("）", ")")
    return s


def split_questions(lines):
    """按题号 1..351 顺序切块"""
    text = "\n" + "\n".join(lines) + "\n"
    pos = {}
    for n in range(1, 352):
        # 题号出现在行首（或紧跟换行），后接 ". "
        pat = re.compile(r"(?<![\d.])%s\.\s" % n)
        m = pat.search(text)
        if m:
            pos[n] = m.start()
    return text, pos


def main():
    lines = load_lines()
    text, pos = split_questions(lines)
    order = sorted(pos)
    print("定位到题号:", len(order), "缺:", [n for n in range(1, 352) if n not in pos][:10])

    blocks = {}
    for i, n in enumerate(order):
        st = pos[n]
        en = pos[order[i + 1]] if i + 1 < len(order) else len(text)
        blocks[n] = text[st:en]

    opt, low = {}, []
    for n, body in blocks.items():
        parts = re.split(r"(?:^|(?<=\s))([A-E])\.\s*", body)
        d = {}
        k = 1
        while k + 1 < len(parts):
            d[parts[k]] = re.sub(r"\s+", " ", parts[k + 1]).strip()
            k += 2
        opt[n] = d

    res = {}
    for n in blocks:
        a = flat(ans.get(str(n), ""))
        sc = []
        for L in "ABCDE":
            o = flat(opt[n].get(L, ""))
            s = 1.0 if (a and a == o) else difflib.SequenceMatcher(None, a, o).ratio()
            sc.append((s, L))
        sc.sort(reverse=True)
        (s1, L1), (s2, L2) = sc[0], sc[1]
        res[str(n)] = {"ans": L1, "score": round(s1, 3), "gap": round(s1 - s2, 3)}
        if s1 < 0.99 or (s1 - s2) < 0.05:
            low.append((n, a[:32], L1, round(s1, 3), L2, round(s2, 3),
                        {L: flat(opt[n].get(L, ""))[:26] for L in "ABCDE"}))

    print("高置信:", 351 - len(low), "/ 351")
    for x in low[:12]:
        print(" Q%s %r -> %s(%.2f) vs %s(%.2f)" % x[:6])
        print("    ", x[6])
    json.dump(res, open(os.path.join(ROOT, "build", "answers_md.json"), "w"), indent=0)


if __name__ == "__main__":
    main()
