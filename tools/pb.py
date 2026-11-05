# -*- coding: utf-8 -*-
"""Part B: the items you were actually served in the three practice quizzes.

They are appended to the topic section they belong to, after the compiled-bank
items, so the book stays topic-ordered.  Nothing is retyped: the question, the
paper's own "Answer:" line and the printed solution are all page crops.
"""
import json
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDIR = os.path.join(ROOT, "qbank", "p")
ITEMS = json.load(open(os.path.join(ROOT, "build", "pitems.json")))

SCALE = 3.2


def mm(px):
    # natural size (factor 1.0): a P-item is printed exactly as wide as it was
    # on the attempt page, so its text keeps the original 10 pt
    return px * 0.352778 / SCALE


def by_section():
    out = {}
    for it in ITEMS:
        out.setdefault(it["sec"], []).append(it)
    return out


BY_SEC = by_section()


def _fit(path, cap_w=150.0, cap_h=60.0):
    """Width in mm for an image, held to a height budget."""
    w, h = Image.open(path).size
    wid = min(mm(w), cap_w)
    if h and wid * h / float(w) > cap_h:
        wid *= cap_h / (wid * h / float(w))
    return wid


def short_quiz(q):
    # "Practice quiz 1 - W4" -> "Quiz 1 · W4"
    parts = q.split()
    return "Quiz %s &middot; %s" % (parts[2], parts[-1])


def card(it, base, pre=""):
    pid = it["pid"]
    q = os.path.join(PDIR, "p%03d_q.png" % pid)
    a = os.path.join(PDIR, "p%03d_a.png" % pid)
    s = os.path.join(PDIR, "p%03d_s.png" % pid)
    if not (os.path.exists(q) and os.path.exists(a) and os.path.exists(s)):
        return ""
    # the answer line is printed at its own size: a stacked fraction is 12 mm
    # tall, a bare letter is 4 mm, and crushing either one makes it unreadable
    aw = min(mm(Image.open(a).size[0]), 176.0)
    return (
        '<div class="prow">%s<div class="p">'
        '<div class="p-h"><span class="p-n">P%d</span>'
        '<span class="p-x">%s &middot; printed as question %s</span></div>'
        '<div class="p-b">'
        '<img class="p-q" style="width:%.2fmm" src="file://%s">'
        '<div class="ans p-ans"><img class="p-a" style="width:%.2fmm" src="file://%s"></div>'
        '<img class="p-s" style="width:%.2fmm" src="file://%s">'
        "</div></div></div>"
        % (pre, pid, short_quiz(it["quiz"]), it["qnos"][0],
           _fit(q, 176.0, 64.0), q, aw, a, _fit(s, 176.0, 112.0), s)
    )


def block(sec_id):
    """The Part-B block for one section, or '' when that topic never came up."""
    items = BY_SEC.get(sec_id, [])
    if not items:
        return ""
    n = len(items)
    head = ('<div class="phead"><span class="phead-t">From your practice quizzes</span>'
            '<span class="phead-n">%d item%s &middot; answer and solution as printed</span></div>'
            % (n, "" if n == 1 else "s"))
    # the band rides inside the first card's row, so it can never be left
    # stranded at the foot of a page
    return (card(items[0], "", head)
            + "".join(card(it, "") for it in items[1:]))


if __name__ == "__main__":
    import collections
    c = collections.Counter(i["sec"] for i in ITEMS)
    print("items", len(ITEMS), "sections", len(c))
    print(c.most_common(5))
