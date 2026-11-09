#!/usr/bin/env python3
"""Extract every MTH028 question from the 30 Moodle review PDFs (v2).

Why v2: the original pipelined guessed a crop bottom from "Your answer is" /
"The correct answer is" text anchors.  The Quiz 3 exports have no verdict line
at all -- Moodle prints an inline feedback card directly under the stem card --
so the old heuristic sliced the worked solution (and the printed answer) into
the question screenshot.  That is the "截图问题".

v2 loses nothing to guessing: every card in the export is a drawn rounded
rectangle with a fixed border colour, so the exact stem box and the exact
feedback box can be read from page.get_drawings():

    header card  #CAD0D7  (0.7922, 0.8157, 0.8431)  "Question N" + verdict
    stem card    #B3D9E0  (0.7020, 0.8510, 0.8784)  the question itself
    feedback     #FBE6CA  (0.9843, 0.9020, 0.7922)  solution + correct answer

The question crop is then exactly the stem card (never the feedback card) and
the answer crop is exactly the feedback card.

Output: data/extract_v2.json (one record per question, 450 of them).
"""
import json
import os
import re
import pymupdf

ROOT = "/Users/zhj/WorkBuddy/2026-11-05-22-50-04/mth028"
MAT = os.path.join(os.path.dirname(ROOT), "mth028-material")
SRC = os.path.join(MAT, "MTH028-Quizzes")
T2 = os.path.join(MAT, "题库2")
OUT = os.path.join(ROOT, "data", "extract_v2.json")

# border colours of the three card types (RGB 0-1, from the PDF content stream)
CARD = {
    "head": (0.7922, 0.8157, 0.8431),
    "stem": (0.7020, 0.8510, 0.8784),
    "feed": (0.9843, 0.9020, 0.7922),
}
RADIO_GREY = (0.6627, 0.6627, 0.6627)
RADIO_DOT = (0.4627, 0.4627, 0.4627)
INPUT_BORDER = (0.5608, 0.5843, 0.6196)
PUA_TICK, PUA_CROSS = "\uf058", "\uf057"


def near(c, ref, tol=0.02):
    return c and len(c) >= 3 and all(abs(c[i] - ref[i]) < tol for i in range(3))


def card_kind(dr):
    c = dr.get("color")
    for k, ref in CARD.items():
        if near(c, ref):
            return k
    return None


def lines_of(words):
    """Group (rect, text) words into visual lines, then join left-to-right."""
    rows = []
    for r, t in sorted(words, key=lambda w: (round(w[0].y0, 1), w[0].x0)):
        placed = False
        for row in rows:
            if abs(row["y"] - r.y0) <= 2.5:
                row["w"].append((r.x0, t))
                placed = True
                break
        if not placed:
            rows.append({"y": r.y0, "w": [(r.x0, t)]})
    rows.sort(key=lambda r: r["y"])
    return ["".join(t for _, t in sorted(row["w"])) for row in rows]


def words_in(page, rect, pad=1.0):
    out = []
    for w in page.get_text("words"):
        r = pymupdf.Rect(w[:4])
        if r.x0 >= rect.x0 - pad and r.x1 <= rect.x1 + pad \
                and r.y0 >= rect.y0 - pad and r.y1 <= rect.y1 + pad:
            out.append((r, w[4]))
    return out


def clean(s):
    s = re.sub(r"\s+", " ", s).strip()
    return s


def parse_page(page):
    """Return the cards and marks of one page in reading order."""
    cards, radios, inputs = [], [], []
    for dr in page.get_drawings():
        r = dr["rect"]
        k = card_kind(dr)
        if k and r.width > 300:
            cards.append({"kind": k, "rect": r})
            continue
        c = dr.get("color")
        f = dr.get("fill")
        if r.width < 12 and r.height < 12 and r.width > 6:
            if near(c, RADIO_GREY) or near(f, RADIO_DOT) or near(f, RADIO_GREY):
                radios.append(r)
        # answer inputs come in two shapes: a wide "Answer: [____]" box with a
        # blue-grey border, and a small inline box inside the sentence drawn
        # with a plain black border.  Both hold the student's typed value.
        if near(c, INPUT_BORDER, 0.06) and 6 < r.width < 560 and 6 < r.height < 60:
            inputs.append(r)
        elif near(c, (0.0, 0.0, 0.0), 0.05) and near(f, (1.0, 1.0, 1.0), 0.02) \
                and 10 < r.width < 70 and 10 < r.height < 45:
            inputs.append(r)
    cards.sort(key=lambda c: (round(c["rect"].y0, 1), c["rect"].x0))
    # radios: one representative rect per radio (ring first, dot adds a second)
    uniq = []
    for r in sorted(radios, key=lambda r: (r.y0, r.x0)):
        if not any(abs(r.y0 - u.y0) < 2 and abs(r.x0 - u.x0) < 2 for u in uniq):
            uniq.append(r)
    return cards, uniq, inputs


def question_of(cards, i):
    """The stem card at index i -> (head card above it, feed card below it)."""
    stem = cards[i]
    head = None
    for c in reversed(cards[:i]):
        if c["kind"] == "head" and c["rect"].y1 <= stem["rect"].y0 + 2:
            head = c
            break
    feed = None
    for c in cards[i + 1:]:
        if c["kind"] == "feed" and c["rect"].y0 >= stem["rect"].y1 - 2:
            feed = c
            break
        if c["kind"] in ("head", "stem"):
            break
    return head, feed


def main():
    files = [(os.path.join(SRC, "%d.pdf" % i), "%d" % i, "p%d" % i, i)
             for i in range(1, 16)]
    files += [(os.path.join(T2, "2-%d.pdf" % i), "B%d" % i, "b%d" % i, 20 + i)
              for i in range(1, 16)]

    rows = []
    for path, tag, qidtag, quizno in files:
        if not os.path.exists(path):
            print("! missing", path)
            continue
        doc = pymupdf.open(path)
        first = re.sub(r"\s+", "", doc[0].get_text())
        m = re.search(r"PracticeQuiz(\d)", first)
        quiz_label = int(m.group(1)) if m else None
        n_before = len(rows)
        for pno, page in enumerate(doc):
            cards, radios, inputs = parse_page(page)
            for i, c in enumerate(cards):
                if c["kind"] != "stem":
                    continue
                head, feed = question_of(cards, i)
                if head is None:
                    continue
                stem_rect = c["rect"]
                hw = words_in(page, head["rect"])
                hl = lines_of(hw)
                qno = None
                htext = " ".join(hl)
                # "Question" and its number are separate text runs that sit on
                # slightly different baselines, so match them word by word.
                for wr, wt in hw:
                    if wt.strip() != "Question":
                        continue
                    # the number can sort *before* "Question" (its baseline is
                    # a few points higher); scan the whole header card.
                    cands = [(abs(wr2.y0 - wr.y0), int(wt2)) for wr2, wt2 in hw
                             if re.fullmatch(r"\d{1,2}", wt2.strip())
                             and abs(wr2.y0 - wr.y0) < 14 and wr2.x0 > wr.x1 - 2]
                    if cands:
                        qno = min(cands)[1]
                        break
                if qno is None:
                    mq = re.search(r"(?i)question\D{0,4}(\d{1,2})", htext)
                    if mq:
                        qno = int(mq.group(1))
                verdict = None
                for v in ("Not answered", "Partially correct", "Incorrect", "Correct"):
                    if v.lower() in htext.lower():
                        verdict = v
                        break
                if qno is None:
                    print("  ! no question number on page", pno + 1, path)
                    continue

                sw = words_in(page, stem_rect)
                marks = [(r, t) for r, t in sw
                         if any(0xE000 <= ord(ch) <= 0xF8FF for ch in t)]
                txt = [(r, t) for r, t in sw
                       if not any(0xE000 <= ord(ch) <= 0xF8FF for ch in t)]

                labels = [(r, t) for r, t in txt if re.fullmatch(r"[A-E]\.", t)]
                is_choice = bool(labels) or "Selectone:" in re.sub(r"\s+", "", " ".join(t for _, t in txt))
                ans_label = None
                for r, t in txt:
                    if t.strip() == "Answer:":
                        ans_label = r
                        break

                # ---- answer input boxes inside this card ----
                boxes = [ib for ib in inputs
                         if stem_rect.y0 - 2 <= ib.y0 and ib.y1 <= stem_rect.y1 + 2]

                def in_box(r):
                    return any(r.x0 >= b.x0 - 1 and r.x1 <= b.x1 + 3
                               and r.y0 >= b.y0 - 3 and r.y1 <= b.y1 + 4
                               for b in boxes)

                # the typed value is the only text inside those boxes; it must
                # never reach the stem text (it would leak the answer)
                student = clean(" ".join(t for r, t in txt if in_box(r))) or None

                # ---- stem text: stop above the "Answer:" input row ----
                stem_words = []
                for r, t in txt:
                    if t.strip() == "Select one:":
                        continue
                    if ans_label is not None and r.y0 > ans_label.y0 - 3:
                        continue
                    if in_box(r):
                        continue
                    stem_words.append((r, t))
                stem_lines = lines_of(stem_words)
                stem = clean(" ".join(stem_lines))

                # ---- options ----
                options = []
                labels.sort(key=lambda w: (w[0].y0, w[0].x0))
                for k, (lr, lt) in enumerate(labels):
                    y0 = lr.y0 - 6
                    y1 = labels[k + 1][0].y0 - 6 if k + 1 < len(labels) else stem_rect.y1
                    band = [(r, t) for r, t in txt
                            if r.y0 >= y0 and r.y0 < y1 and r.x0 > lr.x1 - 2
                            and r is not lr]
                    options.append({"L": lt[0],
                                    "text": clean(" ".join(lines_of(band))),
                                    "y": round(lr.y0, 1)})

                # ---- marks: tick = correct option, cross = student's pick ----
                tick_L = cross_L = None
                for r, t in marks:
                    if t.strip() == PUA_TICK or PUA_TICK in t:
                        tick_L = nearest_option(r, labels) or tick_L
                    elif t.strip() == PUA_CROSS or PUA_CROSS in t:
                        cross_L = nearest_option(r, labels) or cross_L

                # ---- feedback card: solution + printed answer ----
                printed, printed_full, sol = None, None, None
                if feed is not None:
                    fw = [(r, t) for r, t in words_in(page, feed["rect"])
                          if not any(0xE000 <= ord(ch) <= 0xF8FF for ch in t)]
                    sol = clean(" ".join(lines_of(fw)))
                    phrase = None
                    for pat in ("The correct answer is:", "The correct answer is",
                                "The answer is:", "The answer is"):
                        hits = [h for h in page.search_for(pat)
                                if feed["rect"].x0 - 2 <= h.x0 and h.y1 <= feed["rect"].y1 + 2]
                        if hits:
                            phrase = min(hits, key=lambda h: h.y0)
                            break
                    if phrase is not None:
                        # the answer box holds either a single value on the
                        # marker line, a multi-line system below it, or a matrix
                        # whose top rows sit ABOVE the baseline -- take all three
                        onmark = [(r, t) for r, t in fw
                                  if abs(r.y0 - phrase.y0) < 9 and r.x0 >= phrase.x1 - 3]
                        below = [(r, t) for r, t in fw if r.y0 > phrase.y1 - 2]
                        above = [(r, t) for r, t in fw
                                 if phrase.y0 - 46 <= r.y0 <= phrase.y0 - 6
                                 and r.x0 >= phrase.x1 - 3]
                        printed = clean(" ".join(lines_of(onmark))) or None
                        printed_full = clean(" ".join(
                            lines_of(above) + lines_of(onmark) + lines_of(below))) or None
                    else:
                        printed_full = sol
                    # drop a leading copy of the marker itself ("... The correct
                    # answer is: 4") that some exports keep in the same line
                    printed_full = re.sub(
                        r"(?i)^.*?the\s*correct\s*answer\s*is\s*:?\s*", "", printed_full or "")
                    printed = re.sub(
                        r"(?i)^.*?the\s*correct\s*answer\s*is\s*:?\s*", "", printed or "")
                    printed_full = clean(printed_full) or None
                    printed = clean(printed) or None

                rows.append({
                    "qid": "%s-%02d" % (qidtag, qno),
                    "tag": tag,
                    "file": os.path.basename(path),
                    "quiz": quizno,
                    "quiz_label": quiz_label,
                    "qno": qno,
                    "page": pno,
                    "type": "choice" if is_choice else "fill",
                    "verdict": verdict,
                    "student": student,
                    "stem": stem,
                    "options": options,
                    "tick": tick_L,
                    "cross": cross_L,
                    "printed": printed,
                    "printedFull": printed_full,
                    "solution": sol,
                    "rects": {
                        "stem": [round(v, 2) for v in stem_rect],
                        "feed": [round(v, 2) for v in feed["rect"]] if feed else None,
                        "head": [round(v, 2) for v in head["rect"]],
                        "radios": [[round(v, 2) for v in r] for r in radios
                                   if stem_rect.y0 - 2 <= r.y0 <= stem_rect.y1],
                        "inputs": [[round(v, 2) for v in r] for r in inputs
                                   if stem_rect.y0 - 2 <= r.y0 <= stem_rect.y1],
                        "pua": [[round(v, 2) for v in r] for r, t in marks],
                    },
                })
        doc.close()
        got = rows[n_before:]
        print("%-6s quiz=%-4s pages=%-3d questions=%-3d choice=%-3d feed=%-3d"
              % (tag, quiz_label, len(pymupdf.open(path)),
                 len(got), sum(1 for r in got if r["type"] == "choice"),
                 sum(1 for r in got if r["rects"]["feed"])))

    json.dump(rows, open(OUT, "w"), ensure_ascii=False, indent=1)
    print("\ntotal", len(rows))
    print("choice", sum(1 for r in rows if r["type"] == "choice"),
          "fill", sum(1 for r in rows if r["type"] == "fill"))
    print("with printed answer", sum(1 for r in rows if r["printed"]))
    print("with feedback card", sum(1 for r in rows if r["rects"]["feed"]))
    print("choice without tick", sum(1 for r in rows if r["type"] == "choice" and not r["tick"]))
    print("saved", OUT)


def nearest_option(rect, labels):
    """The option whose label sits on the same line as this mark."""
    best, bestd = None, 1e9
    for lr, lt in labels:
        d = abs(lr.y0 - rect.y0)
        if d < bestd:
            best, bestd = lt[0], d
    return best if bestd < 30 else None


if __name__ == "__main__":
    main()
