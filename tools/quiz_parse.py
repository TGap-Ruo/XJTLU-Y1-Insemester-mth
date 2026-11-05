# -*- coding: utf-8 -*-
"""Parse the 15 Moodle attempt print-outs into crop-ready question blocks.

Each attempt is a "Attempt review" page: the question number sits above a
"Question" label, then a status line, the stem, "Select one:", options A-E,
then "Answer: ..." and the printed solution, then "The correct answer is: ...".

Output build/quiz_blocks.json:
    [{file, quiz, qno, page, stem:[y0,y1], opts:[y0,y1], sol:[y0,y1],
      options:{A:..,E:}, answer_text, correct_line, stem_text}, ...]
"""
import json
import os
import re
import sys

import pdfplumber

SRC = "/Users/zhj/Downloads/MTH026-Quiz"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "quiz_blocks.json")

STATUS = ("Not answered", "Correct", "Partially correct", "Incorrect",
          "Marked out of", "Mark 1.00 out of", "Mark 0.00 out of")


def rows_of(page, tol=3.0):
    """Cluster chars into text rows: [(top, bottom, text, chars)]."""
    ch = sorted(page.chars, key=lambda c: (round(c["top"], 1), c["x0"]))
    rows = []
    for c in ch:
        if rows and abs(c["top"] - rows[-1][0]) <= tol:
            rows[-1][3].append(c)
            r = rows[-1]
            rows[-1] = (min(r[0], c["top"]), max(r[1], c["bottom"]), r[2], r[3])
        else:
            rows.append((c["top"], c["bottom"], None, [c]))
    out = []
    for top, bot, _, cs in rows:
        cs.sort(key=lambda c: c["x0"])
        out.append((top, bot, "".join(c["text"] for c in cs).strip(), cs))
    return out


def rows_fine(chars, tol=1.6):
    """Cluster into visual rows (tight tolerance so a fraction bar separates
    numerator and denominator instead of merging everything)."""
    ch = sorted(chars, key=lambda c: c["top"])
    rows = []
    for c in ch:
        if rows and abs(c["top"] - rows[-1][0]) <= tol:
            rows[-1][1].append(c)
        else:
            rows.append([c["top"], [c]])
    out = []
    for top, cs in rows:
        cs.sort(key=lambda c: c["x0"])
        out.append((top, "".join(c["text"] for c in cs).strip()))
    return [r for r in out if r[1]]


def rebuild_band(page_chars, y0, y1):
    """Reading order text for the slice y0..y1, fractions kept together."""
    sub = [c for c in page_chars if y0 <= c["top"] < y1]
    rows = rows_fine(sub)
    return " ".join(t for _y, t in rows)


def is_green(chars):
    """Moodle draws the tick / correct option in green; that is the only
    reliable marker in the text layer (the option itself is not bolded)."""
    for c in chars:
        col = c.get("non_stroking_color") or ()
        if len(col) != 3:
            continue
        r, g, b = col
        if g > 0.30 and g > r + 0.12 and g > b + 0.12:
            return True
    return False


def parse_pdf(path, fname):
    blocks = []
    with pdfplumber.open(path) as pdf:
        quiz = None
        for pi, page in enumerate(pdf.pages):
            rows = rows_of(page)
            if quiz is None:
                for t, b, txt, cs in rows[:12]:
                    m = re.search(r"Practice quiz \d+ - W\d+", txt)
                    if m:
                        quiz = m.group(0)
                        break
            # locate "Question" labels (block starts)
            starts = [i for i, r in enumerate(rows) if r[2] == "Question"]
            if not starts:
                continue
            bounds = starts + [len(rows)]
            for k, s in enumerate(starts):
                end = bounds[k + 1]
                seg = rows[s:end]
                # question number = the row right above the label
                qno = None
                if s > 0:
                    m = re.match(r"^(\d{1,2})$", rows[s - 1][2])
                    if m:
                        qno = int(m.group(1))
                # split off the "Question" label and the status lines
                i = 1 if seg[0][2] == "Question" else 0
                while i < len(seg) and any(seg[i][2].startswith(p) for p in STATUS):
                    i += 1
                body = seg[i:]
                # drop the printed page footer (url + page numbers) and the
                # next question's number, which sits above its "Question" label
                body = [r for r in body if not r[2].startswith("https://")]
                while body and (re.match(r"^\d{1,2}$", body[-1][2]) or body[-1][2] == "Question"):
                    body.pop()
                if not body:
                    continue
                # find markers inside the block
                sel = next((j for j, r in enumerate(body) if r[2].startswith("Select one")), None)
                if sel is None:
                    continue
                ans = next((j for j, r in enumerate(body) if r[2].startswith("Answer:")), None)
                # the printed answer is a stacked fraction: its numerator sits
                # above the "Answer:" label and its denominator below, so grow
                # the answer block outwards from the label along the same column
                first_ans = ans
                last_ans = ans
                if ans is not None:
                    lx = body[ans][3][0]["x0"] if body[ans][3] else 0
                    def is_step(t):
                        return bool(re.match(r"^(\d+\.|The correct answer)", t))

                    j = ans - 1
                    while j >= sel + 1 and body[j][0] > body[ans][0] - 11 and \
                            body[j][3] and body[j][3][0]["x0"] > lx + 25 and not is_step(body[j][2]):
                        first_ans = j
                        j -= 1
                    j = ans + 1
                    while j < len(body) and body[j][0] < body[ans][0] + 15 and \
                            body[j][3] and body[j][3][0]["x0"] > lx + 25 and not is_step(body[j][2]):
                        last_ans = j
                        j += 1
                stem = body[:sel]
                opts = body[sel + 1: first_ans if first_ans is not None else len(body)]
                sol = body[first_ans:] if ans is not None else []
                # option lines: A. B. C. D. E.
                options = {}
                green = {}
                cur = None
                for _t, _b, txt, cs in opts:
                    m = re.match(r"^([A-E])\.\s*(.*)$", txt)
                    if m:
                        cur = m.group(1)
                        options[cur] = m.group(2)
                        green[cur] = is_green(cs)
                    elif cur and txt:
                        options[cur] += " " + txt
                        green[cur] = green.get(cur, False) or is_green(cs)
                # layout-aware rebuild of the option lines and the answer value
                pc = page.chars
                letter_rows = []
                for _t, _b, txt, cs in opts:
                    m = re.match(r"^([A-E])\.", txt)
                    if m:
                        letter_rows.append((m.group(1), _t))
                opt_layout = {}
                for j, (L, y) in enumerate(letter_rows):
                    y_prev = letter_rows[j - 1][1] if j else y - 9
                    nxt = letter_rows[j + 1][1] if j + 1 < len(letter_rows) else (sol[0][0] if sol else y + 40)
                    opt_layout[L] = rebuild_band(pc, max(y_prev + 1, y - 9), nxt)[2:]
                ans_layout = ""
                if sol:
                    ans_layout = rebuild_band(pc, sol[0][0], sol[0][0] + 12)

                opt_y = {}
                for j, (L, y) in enumerate(letter_rows):
                    nxt = letter_rows[j + 1][1] - 5 if j + 1 < len(letter_rows) else (sol[0][0] - 2 if sol else y + 40)
                    opt_y[L] = [round(y - 6, 1), round(nxt, 1)]
                ans_y = [round(body[first_ans][0] - 2, 1), round(body[last_ans][1] + 2, 1)] \
                    if ans is not None else None

                blocks.append({
                    "opt_y": opt_y,
                    "ans_y": ans_y,
                    "opt_layout": opt_layout,
                    "ans_layout": ans_layout,
                    "file": fname, "quiz": quiz, "qno": qno, "page": pi,
                    "page_h": round(page.height, 1),
                    "stem": [round(stem[0][0], 1), round(stem[-1][1], 1)],
                    "opts": [round(opts[0][0], 1), round(opts[-1][1], 1)] if opts else None,
                    "sol": [round(sol[0][0], 1), round(body[-1][1], 1)] if sol else None,
                    "ans_band": [round(body[first_ans][0], 1), round(body[last_ans][1], 1)]
                                if ans is not None else None,
                    "options": options,
                    "green": green,
                    "stem_text": " ".join(r[2] for r in stem),
                    "answer_text": " ".join(r[2] for r in sol[:2]) if sol else "",
                    "block_text": "\n".join(r[2] for r in body),
                    "block_end": round(body[-1][1], 1),
                })
    return blocks


def main():
    allb = []
    for i in range(1, 16):
        f = "%d.pdf" % i
        b = parse_pdf(os.path.join(SRC, f), f)
        allb += b
        print(f, len(b), b[0]["quiz"] if b else "-")
    json.dump(allb, open(OUT, "w"), ensure_ascii=False)
    print("blocks", len(allb), "->", OUT)


if __name__ == "__main__":
    main()
