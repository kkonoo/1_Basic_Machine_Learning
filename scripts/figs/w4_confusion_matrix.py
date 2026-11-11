# W4 §2 Confusion matrix: 네 칸(실제 × 예측)과, 파생 지표 다섯 개가 각각 어느 칸들의 비율인지 (진한 칸 = 분자, 진한+옅은 칸 = 분모)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w4")

ROWC, COLC = CAT[0], CAT[1]          # 실제 class 기준 지표 / 예측 기준 지표
CELLS = {(0, 0): ("TP", "True Positive"), (0, 1): ("FN", "False Negative"),
         (1, 0): ("FP", "False Positive"), (1, 1): ("TN", "True Negative")}

# (name, formula, numerator cell, other denominator cell, colour)
GROUPS = [
    ("실제 class 기준 · 유병률과 무관", ROWC, [
        ("Recall / Sensitivity", "TP / (TP + FN)", (0, 0), (0, 1)),
        ("Specificity", "TN / (TN + FP)", (1, 1), (1, 0)),
        ("FPR", "FP / (FP + TN) = 1 − specificity", (1, 0), (1, 1)),
    ]),
    ("예측 기준 · 유병률에 크게 의존", COLC, [
        ("Precision / PPV", "TP / (TP + FP)", (0, 0), (1, 0)),
        ("NPV", "TN / (TN + FN)", (1, 1), (0, 1)),
    ]),
]


def mini(ax, x, ytop, num_cell, den_cell, c, s=0.21, g=0.03):
    """2×2 icon, same layout as the big matrix; (x, ytop) = upper-left corner."""
    for (r, k) in CELLS:
        fc, ec = "white", "#C9CED6"
        if (r, k) == num_cell:
            fc, ec = c, c
        elif (r, k) == den_cell:
            fc, ec = mix(c, 0.28), mix(c, 0.28)
        box(ax, x + k * (s + g), ytop - (r + 1) * s - r * g, s, s, fc=fc, ec=ec, lw=0.9, r=0.03)


fig, ax = new(8.4, 4.1)

# ── ① big matrix ────────────────────────────────────────────────────────────
cs, x0, ytop = 1.25, 1.2, 3.3
label(ax, x0 + cs, ytop + 0.55, "예측", fs=12.5, w="bold")
for k, s in enumerate(["Positive", "Negative"]):
    label(ax, x0 + (k + 0.5) * cs, ytop + 0.22, s, fs=11.5, w="semibold", c=TEXT2)
label(ax, 0.22, ytop - cs, "실제", fs=12.5, w="bold", rotation=90)
for r, s in enumerate(["Positive", "Negative"]):
    label(ax, x0 - 0.1, ytop - (r + 0.5) * cs, s, fs=11.5, w="semibold", c=TEXT2, ha="right")
for (r, k), (ab, full) in CELLS.items():
    bx, by = x0 + k * cs, ytop - (r + 1) * cs
    box(ax, bx + 0.03, by + 0.03, cs - 0.06, cs - 0.06, fc=STEPS[3], ec=STEPS[2], lw=1.0, r=0.08)
    label(ax, bx + cs / 2, by + cs / 2 + 0.13, ab, fs=17, w="bold", c=PRIMARY)
    label(ax, bx + cs / 2, by + cs / 2 - 0.22, full, fs=11, c=TEXT2)

# legend under the matrix
ly = 0.25
box(ax, x0 - 0.05, ly + 0.02, 0.2, 0.2, fc=TEXT2, ec="none", r=0.03)              # one dark swatch
label(ax, x0 + 0.25, ly + 0.12, "진한 칸 = 분자", fs=11, c=TEXT2, ha="left")
box(ax, x0 - 0.05, ly - 0.28, 0.2, 0.2, fc=TEXT2, ec="none", r=0.03)              # dark + light swatches
box(ax, x0 + 0.19, ly - 0.28, 0.2, 0.2, fc=mix(TEXT2, 0.25), ec="none", r=0.03)
label(ax, x0 + 0.49, ly - 0.18, "진한 칸 + 옅은 칸 = 분모", fs=11, c=TEXT2, ha="left")

# ── ② derived metrics ───────────────────────────────────────────────────────
px, y = 4.45, 3.92
for head, c, items in GROUPS:
    label(ax, px, y, head, fs=12, w="bold", c=c, ha="left")
    y -= 0.38
    for name, f, nc, dc in items:
        mini(ax, px, y + 0.02, nc, dc, c)
        label(ax, px + 0.62, y - 0.09, name, fs=11.5, w="semibold", ha="left")
        label(ax, px + 0.62, y - 0.36, f, fs=11, c=TEXT2, ha="left")
        y -= 0.62
    y -= 0.24

save(fig, os.path.join(OUT, "confusion_matrix.png"))
