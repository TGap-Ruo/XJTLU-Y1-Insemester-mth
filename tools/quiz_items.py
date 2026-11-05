# -*- coding: utf-8 -*-
"""Build the Part-B item table: dedupe, order, and tag each item with the
topic section it belongs to (by matching it to the closest item of Part A).

The correct option letter is deliberately *not* inferred: Moodle's MathJax
layout scrambles fractions in the text layer, and image comparison proved
unreliable (16% agreement against the 146 items whose letter is known).  Part B
therefore prints the paper's own "Answer: <value>" line, cropped, which is the
original statement of the answer and cannot be wrong.
"""
import collections
import difflib
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
from sections import BY_Q  # noqa: E402

BLOCKS = os.path.join(ROOT, "build", "quiz_blocks.json")
BOOK = os.path.join(ROOT, "build", "latex.json")
OUT = os.path.join(ROOT, "build", "pitems.json")


def norm(s):
    s = unicodedata.normalize("NFKC", s).replace("\u2212", "-")
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.lower()
    return re.sub(r"[^a-z0-9]", "", s)


def masked(s):
    return re.sub(r"\d+", "#", norm(s))


def main():
    blocks = json.load(open(BLOCKS))
    book = json.load(open(BOOK))
    bookm = []
    for k, v in book.items():
        st = re.sub(r"^\s*\d{1,3}\s*\.\s*", "", v["stem"])
        bookm.append((k, masked(st)))

    order = {"Practice quiz 1 - W4": 0, "Practice quiz 2 - W6": 1, "Practice quiz 3 - W8": 2}
    blocks.sort(key=lambda x: (order.get(x["quiz"], 9), int(x["file"].split(".")[0]), x["qno"] or 0))

    seen, items = {}, []
    for b in blocks:
        key = norm(b["stem_text"]) + "|" + "|".join(norm(b["options"].get(L, "")) for L in "ABCDE")
        if key in seen:
            seen[key]["files"].append(b["file"])
            seen[key]["qnos"].append(b["qno"])
            continue
        m = masked(b["stem_text"])
        best, bid = -1.0, None
        for k, bm in bookm:
            r = difflib.SequenceMatcher(None, m, bm).quick_ratio()
            if r > best:
                best, bid = r, k
        sec = BY_Q[int(bid)]["id"] if bid else None
        rec = {
            "pid": None, "quiz": b["quiz"], "qno": b["qno"], "file": b["file"],
            "files": [b["file"]], "qnos": [b["qno"]],
            "page": b["page"], "page_h": b["page_h"],
            "stem": b["stem"], "opts": b["opts"], "sol": b["sol"],
            "block_end": b["block_end"], "ans_y": b["ans_y"],
            "options": b["options"], "stem_text": b["stem_text"],
            "sec": sec, "sec_score": round(best, 3),
            "answer_line": b["ans_layout"].replace("Answer:", "").strip(),
        }
        seen[key] = rec
        items.append(rec)

    for i, it in enumerate(items, 1):
        it["pid"] = i

    print("items:", len(items), dict(collections.Counter(i["quiz"] for i in items)))
    print("tagged to a section:", sum(1 for i in items if i["sec"]))
    low = [i for i in items if i["sec_score"] < 0.80]
    print("weak tag:", len(low))
    for i in low[:6]:
        print("   %.2f %s" % (i["sec_score"], i["stem_text"][:70]))
    print("answer lines empty:", sum(1 for i in items if not i["answer_line"]))
    json.dump(items, open(OUT, "w"), ensure_ascii=False)
    print("->", OUT)


if __name__ == "__main__":
    main()
