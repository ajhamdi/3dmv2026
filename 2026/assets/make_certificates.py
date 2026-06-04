#!/usr/bin/env python3
"""Generate Program Committee (reviewer) certificates for 3DMV @ CVPR 2026.

Produces one landscape PDF per reviewer in assets/certificates/, styled after
the workshop award certificates: light background, decorative dot grids, and a
blue accent matching the 3DMV website.
"""

import os
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# --- palette (matches the 3DMV site / award aesthetic) ---
BLUE = HexColor("#164FC9")      # site accent blue
TEAL = HexColor("#143A4A")      # deep heading teal
PURPLE = HexColor("#7B2D8E")    # dot-grid accent
GREY = HexColor("#9AA0A6")      # secondary text / dots
DARK = HexColor("#2B2F33")      # primary text
LIGHT = HexColor("#F4F6FA")     # background tint

PAGE = landscape(A4)            # 842 x 595 pt
W, H = PAGE

# (First name, Last name, Affiliation)
REVIEWERS = [
    ("Akhmedkhan", "Shabanov", "Simon Fraser University"),
    ("Boris", "Chidlovskii", "Naver Labs Europe"),
    ("Daniel", "Duckworth", "Google DeepMind"),
    ("Gopal", "Sharma", "University of British Columbia"),
    ("Gordon Guocheng", "Qian", "Snap"),
    ("Jan", "Held", "University of Liège"),
    ("Jiading", "Fang", "Toyota Technological Institute at Chicago"),
    ("Jianqi", "Chen", "Beihang University"),
    ("Jinjie", "Mai", "KAUST"),
    ("Nitish", "Agarwal", "KinaTrax"),
    ("Priyam", "Parashar", "FAIR, Meta"),
    ("Renaud", "Vandeghen", "University of Liège"),
    ("Sara", "Rojas Martinez", "KAUST"),
    ("Shuzhou", "Yang", "Peking University"),
    ("Silvio", "Giancola", "KAUST"),
    ("Tak Yeon", "Lee", "KAIST"),
    ("Tianhao", "Wu", "Nanyang Technological University"),
    ("Vitor", "Guizilini", "Toyota Research Institute"),
    ("Xingguang", "Yan", "Simon Fraser University"),
    ("Yan", "Xia", "Technical University of Munich"),
]


def dot_grid(c, x0, y0, cols, rows, gap, r, color, alpha=1.0):
    """Draw a grid of dots, anchored at lower-left (x0, y0)."""
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


def draw_certificate(path, first, last, affiliation):
    c = canvas.Canvas(path, pagesize=PAGE)

    # background
    c.setFillColor(HexColor("#FFFFFF"))
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # soft tinted corner wash (top-right + bottom)
    c.saveState()
    c.setFillColor(LIGHT)
    c.circle(W + 40, H + 40, 230, stroke=0, fill=1)
    c.circle(W - 120, -60, 180, stroke=0, fill=1)
    c.circle(-40, -40, 150, stroke=0, fill=1)
    c.restoreState()

    # decorative dot grids in opposing corners
    dot_grid(c, 44, H - 66, 5, 4, 13, 2.0, PURPLE, 0.9)        # top-left
    dot_grid(c, 44, 38, 4, 3, 13, 2.0, PURPLE, 0.9)            # bottom-left
    dot_grid(c, W - 95, H - 120, 3, 5, 13, 1.8, GREY, 0.7)     # top-right accent
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
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(cx, H - 95, "3DMV @ CVPR 2026")

    c.setFillColor(GREY)
    c.setFont("Helvetica", 11)
    c.drawCentredString(
        cx, H - 114,
        "Third Workshop for Learning 3D with Multi-View Supervision")

    # short divider
    c.setStrokeColor(PURPLE)
    c.setLineWidth(1.2)
    c.line(cx - 55, H - 128, cx + 55, H - 128)

    # title
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 38)
    c.drawCentredString(cx, H - 185, "Certificate of Appreciation")

    # presented to
    c.setFillColor(DARK)
    c.setFont("Helvetica-Oblique", 13)
    c.drawCentredString(cx, H - 222, "This certificate is proudly presented to")

    # recipient name (auto-shrink to fit)
    name = f"{first} {last}"
    size = 40
    c.setFont("Helvetica-Bold", size)
    while c.stringWidth(name, "Helvetica-Bold", size) > W - 200 and size > 20:
        size -= 1
        c.setFont("Helvetica-Bold", size)
    c.setFillColor(BLUE)
    c.drawCentredString(cx, H - 272, name)

    # underline under name
    nw = c.stringWidth(name, "Helvetica-Bold", size)
    c.setStrokeColor(GREY)
    c.setLineWidth(0.8)
    c.line(cx - max(nw, 120) / 2 - 20, H - 284, cx + max(nw, 120) / 2 + 20, H - 284)

    # affiliation
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(cx, H - 308, affiliation)

    # recognition statement (two centered lines)
    c.setFillColor(DARK)
    c.setFont("Helvetica", 12.5)
    line1 = "in recognition of their valuable service as a member of the Program Committee"
    line2 = "(Reviewer) for the 3DMV Workshop at the IEEE / CVF Conference on"
    line3 = "Computer Vision and Pattern Recognition (CVPR) 2026."
    c.drawCentredString(cx, H - 348, line1)
    c.drawCentredString(cx, H - 366, line2)
    c.drawCentredString(cx, H - 384, line3)

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
    for first, last, aff in REVIEWERS:
        fname = f"{first}_{last}".replace(" ", "_") + ".pdf"
        draw_certificate(os.path.join(out_dir, fname), first, last, aff)
        print("wrote", fname)
    print(f"\n{len(REVIEWERS)} certificates -> {out_dir}")


if __name__ == "__main__":
    main()
