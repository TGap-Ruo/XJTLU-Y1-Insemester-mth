#!/usr/bin/env python3
"""Extract the MTH028 question index from the ten Moodle review PDFs.

The PDFs are *attempt review* pages: each question has a "Question N" header,
optionally a "Select one:" block (choice) or an "Answer:" input (numeric fill),
a "Your answer is correct/incorrect" verdict, and sometimes a printed
"The correct answer is: ..." box.  Questions that were answered incorrectly
often have NO printed correct answer -> those need an AI-supplied answer.

Output: data/quiz_index.json  (one row per question, with page/y anchors so the
cropper can render the question card and the answer card separately).
"""
import json
import os
import re
import pymupdf

ROOT = "/Users/zhj/WorkBuddy/2026-11-05-22-50-04/mth028"
SRC = os.path.join(os.path.dirname(ROOT), "mth028-material", "MTH028-Quizzes")
OUT = os.path.join(ROOT, "data", "quiz_index.json")

FOOTER_Y = 805.0          # printed URL / timestamp lives at y ~819
TOP_Y = 30.0              # browser chrome header at y ~16
HEADER_Y = 210.0          # the first page of each quiz carries a status table


def anchors(page):
    """y positions of the useful landmarks on one page."""
    def ys(text):
        return [round(r.y0, 1) for r in page.search_for(text)]

    out = {
        "questions": [],  # (y, number)
        "correct": ys("The correct answer is"),
        "verdict": ys("Your answer is"),
        "answer_input": ys("Answer:"),
        "select_one": ys("Select one:"),
    }
    # Word-level match: search_for("Question 1") also matches "Question 10"..15,
    # and the Moodle quiz navigation repeats every question label.  Pair the
    # literal word "Question" with the immediately following numeric word and
    # keep only the left-column header (x < 120).
    words = page.get_text("words")
    for i, w in enumerate(words):
        if w[4] != "Question" or w[0] > 120:
            continue
        if i + 1 >= len(words):
            continue
        nxt = words[i + 1]
        if not re.fullmatch(r"\d{1,2}", nxt[4]) or abs(nxt[1] - w[1]) > 12:
            continue
        if nxt[0] - w[2] > 30:       # not adjacent
            continue
        out["questions"].append((round(w[1], 1), int(nxt[4])))
    out["questions"].sort()
    # option labels A. B. C. D. E. (only on choice questions)
    opts = []
    for L in "ABCDE":
        for r in page.search_for("%s." % L):
            if r.x0 < 120:
                opts.append((round(r.y0, 1), L))
    out["options"] = sorted(opts)
    return out


def main():
    rows = []
    for qi in range(1, 11):
        path = os.path.join(SRC, "%d.pdf" % qi)
        doc = pymupdf.open(path)
        pages = [anchors(p) for p in doc]
        # flatten all question headers in reading order
        heads = []
        for pno, a in enumerate(pages):
            for y, n in a["questions"]:
                heads.append({"p": pno, "y": y, "qno": n})
        heads.sort(key=lambda h: (h["p"], h["y"]))
        print("quiz %-2d pages=%-3d question-headers=%d  %s" %
              (qi, len(doc), len(heads), [(h["p"] + 1, h["qno"]) for h in heads]))

        for idx, h in enumerate(heads):
            nxt = heads[idx + 1] if idx + 1 < len(heads) else None
            # region of this question: from its header to the next header (or EOF)
            p0, y0 = h["p"], h["y"]
            p1 = nxt["p"] if nxt else len(doc) - 1
            y1 = nxt["y"] if nxt else FOOTER_Y
            correct_ys, verdict_ys, input_ys, select_ys, option_ys = [], [], [], [], []
            for pno in range(p0, p1 + 1):
                a = pages[pno]
                lo = y0 if pno == p0 else TOP_Y
                hi = y1 if pno == p1 else FOOTER_Y
                def inwin(v):
                    return lo - 2 <= v <= hi + 2
                correct_ys += [(pno, y) for y in a["correct"] if inwin(y)]
                verdict_ys += [(pno, y) for y in a["verdict"] if inwin(y)]
                input_ys += [(pno, y) for y in a["answer_input"] if inwin(y)]
                select_ys += [(pno, y) for y in a["select_one"] if inwin(y)]
                option_ys += [(pno, y, L) for y, L in a["options"] if inwin(y)]
            # a printed answer box belongs to THIS question only if it is before
            # the next question header; Moodle puts it right after the verdict
            has_correct = bool(correct_ys)
            # type: "Select one:" or >=3 option labels => choice, else fill
            is_choice = bool(select_ys) or len({L for _, _, L in option_ys}) >= 3
            rows.append({
                "qid": "q%d-%02d" % (qi, h["qno"]),
                "quiz": qi,
                "qno": h["qno"],
                "type": "choice" if is_choice else "fill",
                "has_printed_answer": has_correct,
                "head": {"p": p0, "y": y0},
                "next": {"p": p1, "y": y1},
                "correct": correct_ys,
                "verdict": verdict_ys,
                "answer_input": input_ys,
                "select_one": select_ys,
                "options": [{"p": p, "y": y, "L": L} for p, y, L in option_ys],
            })
        doc.close()

    # text of each printed answer, for the AI-answer / answer-key comparison
    for r in rows:
        pno, y = (r["correct"][0] if r["correct"] else (None, None))
        if pno is None:
            r["printed_answer_text"] = None
            continue
        page = pymupdf.open(os.path.join(SRC, "%d.pdf" % r["quiz"]))[pno]
        # collect visual lines from the answer box until the next landmark
        lines = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    yy = s["bbox"][1]
                    if y - 4 <= yy <= y + 90 and s["text"].strip():
                        lines.append((round(yy, 1), s["bbox"][0], s["text"]))
        lines.sort()
        merged = []
        for yy, x, t in lines:
            if merged and abs(yy - merged[-1][0]) <= 2.0:
                merged[-1][1].append((x, t))
            else:
                merged.append([yy, [(x, t)]])
        txt = " | ".join("".join(t for _, t in sorted(parts)) for _, parts in merged)
        r["printed_answer_text"] = txt[:600]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("\nrows:", len(rows))
    print("choice:", sum(1 for r in rows if r["type"] == "choice"),
          " fill:", sum(1 for r in rows if r["type"] == "fill"))
    print("with printed answer:", sum(1 for r in rows if r["has_printed_answer"]),
          " WITHOUT (need AI):", sum(1 for r in rows if not r["has_printed_answer"]))
    print("saved", OUT)


if __name__ == "__main__":
    main()
