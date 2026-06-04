#!/usr/bin/env python3
"""Generate Best Paper / Runner-up award certificates for 3DMV @ CVPR 2026.

One landscape PDF per awarded paper in assets/certificates/, styled to match
the reviewer certificates: light background, decorative dot grids, and the
3DMV blue/purple accent palette. Each certificate names the award, the paper
title, and all authors with their affiliations.
"""

import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas

# --- palette (matches the 3DMV site / reviewer certificates) ---
BLUE = HexColor("#164FC9")
TEAL = HexColor("#143A4A")
PURPLE = HexColor("#7B2D8E")
GREY = HexColor("#9AA0A6")
DARK = HexColor("#2B2F33")
LIGHT = HexColor("#F4F6FA")
GOLD = HexColor("#B8860B")

PAGE = landscape(A4)
W, H = PAGE

# short_name -> (award label, paper title, [(author, affiliation), ...])
AWARDS = [
    (
        "DanceNet3D",
        "Best Paper Award",
        "DanceNet3D: A 3D Dance Dataset with Multi-View Videos and "
        "3DGS Reconstructions",
        [
            ("Shihang Wei", "New York University"),
            ("Mingjian Li", "New York University"),
            ("Ran Gong", "New York University"),
            ("Yueyu Hu", "New York University"),
            ("Yao Wang", "New York University"),
        ],
    ),
    (
        "TerraSky3D",
        "Best Paper Runner-up Award",
        "TerraSky3D: Multi-View Reconstructions of European Landmarks in 4K",
        [
            ("Mattia D'Urso", "TU Graz"),
            ("Yuxi Hu", "TU Graz"),
            ("Christian Sormann", "Sony"),
            ("Mattia Rossi", "Sony"),
            ("Friedrich Fraundorfer", "TU Graz"),
        ],
    ),
]


def dot_grid(c, x0, y0, cols, rows, gap, r, color, alpha=1.0):
    c.saveState()
    c.setFillColor(color)
    try:
        c.setFillAlpha(alpha)
    except Exception:
        pass
    for i in range(cols):
        for j in range(rows):
            c.circle(x0 + i * gap, y0 + j * gap, r, stroke=0, fill=1)
    c.restoreState()


def wrap(c, text, font, size, max_w):
    """Greedy word-wrap into lines that fit within max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if c.stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_certificate(path, short, award, title, authors):
    c = canvas.Canvas(path, pagesize=PAGE)

    # background
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # soft tinted corner washes
    c.saveState()
    c.setFillColor(LIGHT)
    c.circle(W + 40, H + 40, 230, stroke=0, fill=1)
    c.circle(W - 120, -60, 180, stroke=0, fill=1)
    c.circle(-40, -40, 150, stroke=0, fill=1)
    c.restoreState()

    # decorative dot grids
    dot_grid(c, 44, H - 66, 5, 4, 13, 2.0, PURPLE, 0.9)        # top-left
    dot_grid(c, 44, 38, 4, 3, 13, 2.0, PURPLE, 0.9)            # bottom-left
    dot_grid(c, W - 95, H - 120, 3, 5, 13, 1.8, GREY, 0.7)     # top-right
    dot_grid(c, W - 95, 40, 3, 4, 13, 2.0, PURPLE, 0.9)        # bottom-right

    # accent frame
    margin = 26
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.4)
    c.rect(margin, margin, W - 2 * margin, H - 2 * margin, stroke=1, fill=0)
    c.setStrokeColor(PURPLE)
    c.setLineWidth(0.6)
    c.rect(margin + 5, margin + 5, W - 2 * margin - 10, H - 2 * margin - 10,
           stroke=1, fill=0)

    cx = W / 2

    # header: workshop name
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(cx, H - 78, "3DMV @ CVPR 2026")
    c.setFillColor(GREY)
    c.setFont("Helvetica", 10.5)
    c.drawCentredString(
        cx, H - 95,
        "Third Workshop for Learning 3D with Multi-View Supervision")
    c.setStrokeColor(PURPLE)
    c.setLineWidth(1.2)
    c.line(cx - 55, H - 108, cx + 55, H - 108)

    # award title
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(cx, H - 150, award)

    # citation line
    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 12.5)
    c.drawCentredString(cx, H - 180, "presented to the authors of")

    # paper title (wrapped, auto-fit)
    size = 21
    lines = wrap(c, f"“{title}”", "Helvetica-Bold", size, W - 200)
    while len(lines) > 2 and size > 15:
        size -= 1
        lines = wrap(c, f"“{title}”", "Helvetica-Bold", size, W - 200)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", size)
    ty = H - 210
    for ln in lines:
        c.drawCentredString(cx, ty, ln)
        ty -= size + 6

    # divider above authors
    ty -= 6
    c.setStrokeColor(GREY)
    c.setLineWidth(0.7)
    c.line(cx - 150, ty, cx + 150, ty)
    ty -= 22

    # authors with affiliations
    for name, aff in authors:
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 14)
        nw = c.stringWidth(name, "Helvetica-Bold", 14)
        aff_txt = f"   —   {aff}"
        aw = c.stringWidth(aff_txt, "Helvetica", 12)
        start = cx - (nw + aw) / 2
        c.drawString(start, ty, name)
        c.setFillColor(GREY)
        c.setFont("Helvetica", 12)
        c.drawString(start + nw, ty, aff_txt)
        ty -= 22

    # footer: date (left) and organizers (right)
    fy = margin + 46
    c.setStrokeColor(GREY)
    c.setLineWidth(0.8)
    c.line(margin + 60, fy, margin + 230, fy)
    c.line(W - margin - 230, fy, W - margin - 60, fy)

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(margin + 145, fy - 14, "June 2026")
    c.setFont("Helvetica", 9)
    c.setFillColor(GREY)
    c.drawCentredString(margin + 145, fy - 26, "Date")

    c.setFillColor(DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(W - margin - 145, fy - 14, "3DMV Organizing Committee")
    c.setFont("Helvetica", 9)
    c.setFillColor(GREY)
    c.drawCentredString(W - margin - 145, fy - 26, "On behalf of the 3DMV Workshop")

    c.showPage()
    c.save()


def main():
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "certificates")
    os.makedirs(out_dir, exist_ok=True)
    for short, award, title, authors in AWARDS:
        path = os.path.join(out_dir, short + ".pdf")
        draw_certificate(path, short, award, title, authors)
        print("wrote", short + ".pdf")
    print(f"\n{len(AWARDS)} award certificates -> {out_dir}")


if __name__ == "__main__":
    main()
