# -*- coding: utf-8 -*-
"""PDF 组装与页码戳记"""
import io, os, re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
pdfmetrics.registerFont(TTFont("CJKU", FONT))


def escape_math(s):
    """把数学模式里的 < > 转义，避免被当成 HTML 标签。"""
    def f(m):
        return m.group(0).replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\$[^$]{1,800}\$", f, s)


def assemble(parts, title):
    from common import head, tail
    body = "".join(p if isinstance(p, str) else p for p in parts)
    body = escape_math(body)
    body = re.sub(r"([★☆]{3})", r'<span class="stars">\1</span>', body)
    return head(title) + body + tail()


def _overlay(total, w, h, n, left, right, rule_color=(0.82, 0.86, 0.91), foot=""):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(w, h))
    top = h - 12 * 2.8346
    c.setStrokeColorRGB(*rule_color)
    c.setLineWidth(0.5)
    c.line(15 * 2.8346, top, w - 15 * 2.8346, top)
    c.setFont("CJKU", 6.6)
    c.setFillColorRGB(0.52, 0.57, 0.64)
    c.drawString(15 * 2.8346, top + 3.2, left)
    rw = c.stringWidth(right, "CJKU", 6.6)
    c.drawRightString(w - 15 * 2.8346, top + 3.2, right)
    # footer
    c.line(15 * 2.8346, 12.5 * 2.8346, w - 15 * 2.8346, 12.5 * 2.8346)
    num = f"{n} / {total}"
    c.drawRightString(w - 15 * 2.8346, 8.6 * 2.8346, num)
    nm = c.stringWidth(num, "CJKU", 6.6)
    c.setFillColorRGB(0.62, 0.66, 0.72)
    c.drawRightString(w - 15 * 2.8346 - nm - 3, 8.6 * 2.8346, foot or "MTH026 · 期中复习")
    c.showPage()
    c.save()
    buf.seek(0)
    return buf


def stamp(src, dst, left, right, skip_first=True, foot=""):
    r = PdfReader(src)
    total = len(r.pages)
    w = float(r.pages[0].mediabox.width)
    h = float(r.pages[0].mediabox.height)
    out = PdfWriter()
    for i, page in enumerate(r.pages):
        if not (skip_first and i == 0):
            ov = PdfReader(_overlay(total, w, h, i + 1, left, right, foot=foot)).pages[0]
            page.merge_page(ov)
        out.add_page(page)
    out.add_metadata({"/Title": right, "/Producer": "MTH026 Study Pack"})
    with open(dst, "wb") as f:
        out.write(f)
    return dst
