# -*- coding: utf-8 -*-
"""解析 extract/bank.md → 结构化题目 JSON（英文原题，5 选项）"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "extract", "bank.md")
OUT = os.path.join(ROOT, "build", "bank_raw.json")

lines = open(SRC, encoding="utf-8").read().split("\n")

# 去掉页脚/页码噪声
DROP = re.compile(r"^(<!-- Page \d+ -->|X J T L U.*|https?://\S+|\d+/\d+$)")
lines = [l.rstrip() for l in lines if not DROP.match(l.strip())]

OPT = re.compile(r"(?:^|\s)([A-E])\.\s")
QNUM = re.compile(r"^(\d{1,3})\.\s+(.*)$")


def norm(s):
    s = s.replace("−", "-").replace("–", "-").replace("−", "-")
    s = s.replace("∪", "∪").replace("∞", "inf")
    s = re.sub(r"\s+", "", s)
    s = s.replace("\\[", "[").replace("\\]", "]")
    return s


# ---------- 1. 切出题目块 ----------
# 题目 = 以 "N. " 开头，且其后（到下一个题号前）含 A. 选项
raw_blocks = []           # (num, [lines])
i = 0
n = len(lines)
while i < n:
    m = QNUM.match(lines[i].strip())
    if m:
        start = i
        j = i + 1
        while j < n:
            nxt = QNUM.match(lines[j].strip())
            if nxt and (nxt.group(1).isdigit()):
                break
            j += 1
        blk = [l for l in lines[start:j] if l.strip()]
        body = "\n".join(blk)
        if re.search(r"(?:^|\s)A\.\s", body) and re.search(r"(?:^|\s)B\.\s", body):
            raw_blocks.append((int(m.group(1)), blk))
            i = j
            continue
    i += 1


def split_options(blk):
    """把块切成 stem 和 A-E 选项"""
    text = "\n".join(blk)
    text = QNUM.sub(lambda mm: mm.group(2), text, count=1)  # 去掉题号
    # 找第一个 A. 出现位置
    parts = re.split(r"(?:(?<=^)|(?<=\s))([A-E])\.\s", "\n" + text)
    # parts: [pre, 'A', txtA, 'B', txtB, ...]
    stem = parts[0].strip()
    opts, letters = {}, []
    k = 1
    while k + 1 < len(parts):
        letter = parts[k]
        body = parts[k + 1]
        opts[letter] = re.sub(r"\s+", " ", body).strip()
        letters.append(letter)
        k += 2
    return stem, opts, letters


parsed = []
for num, blk in raw_blocks:
    stem, opts, letters = split_options(blk)
    parsed.append({"num": num, "stem": stem, "options": [opts[l] for l in letters], "letters": letters})

print("题目块:", len(parsed))
nums = [p["num"] for p in parsed]
print("编号范围:", min(nums), max(nums), "缺失:", sorted(set(range(1, max(nums) + 1)) - set(nums))[:20])
from collections import Counter
print("选项数分布:", Counter(len(p["options"]) for p in parsed))

# ---------- 2. 答案解析 ----------
# 答案块：参考答案 ... 之后连续的 "N. xxx"，直到下一个题号+选项
ans_marks = [i for i, l in enumerate(lines) if "参考答案" in l]
print("答案块:", len(ans_marks))

answers = {}
for mi, pos in enumerate(ans_marks):
    end = ans_marks[mi + 1] if mi + 1 < len(ans_marks) else len(lines)
    cur = None
    for l in lines[pos + 1:end]:
        s = l.strip()
        if not s:
            continue
        if "答案与上方题目编号" in s:
            break
        m = re.match(r"^(\d{1,3})\.\s*(.*)$", s)
        if m:
            cur = int(m.group(1))
            answers[cur] = m.group(2).strip()
        elif cur and not re.match(r"^\d+\.\d+", s):
            answers[cur] = (answers.get(cur, "") + " " + s).strip()

print("答案条数:", len(answers))

# ---------- 3. 匹配答案 → 选项字母 ----------
unmatched = []
for p in parsed:
    a = answers.get(p["num"], "")
    na = norm(a)
    hit = None
    for idx, o in enumerate(p["options"]):
        if norm(o) == na:
            hit = idx
            break
    if hit is None:  # 容错：包含关系
        for idx, o in enumerate(p["options"]):
            no = norm(o)
            if no and (no in na or na in no) and abs(len(no) - len(na)) <= 2:
                hit = idx
                break
    p["answer"] = hit
    p["answer_text"] = a
    if hit is None:
        unmatched.append((p["num"], a[:40], [o[:30] for o in p["options"]]))

print("未匹配答案:", len(unmatched))
for u in unmatched[:12]:
    print("  ", u)

json.dump(parsed, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("→", OUT)
