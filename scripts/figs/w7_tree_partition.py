# W7 §1.1–1.2 구조: 같은 트리를 ① node·leaf 구조로, ② CRP×나이 평면을 축에 평행한 직사각형으로 나눈 모습으로 나란히 (분할값은 설명용)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w7")

YES, NO = CAT[0], CAT[2]
ARR = "#9AA1AB"


def qnode(ax, cx, cy, text, w=1.55, h=0.5):
    box(ax, cx - w / 2, cy - h / 2, w, h, fc="white", ec=PRIMARY, lw=1.6, r=0.1)
    label(ax, cx, cy, text, fs=12, w="semibold")


def leaf(ax, cx, cy, cls, tag, w=0.95, h=0.46):
    c = YES if cls == "Yes" else NO
    box(ax, cx - w / 2, cy - h / 2, w, h, fc=c, ec="none", r=0.1)
    label(ax, cx, cy, cls, fs=12, w="bold", c=on(c))
    tagc(ax, cx - w / 2, cy + h / 2, tag)


def tagc(ax, x, y, t):
    """small letter badge on the upper-left corner of a leaf/region"""
    ax.add_patch(mp.Circle((x, y), 0.14, fc="white", ec=TEXT, lw=1.2, zorder=6))
    label(ax, x, y, t, fs=11, w="bold", z=7)


def edge(ax, x1, y1, x2, y2, txt, side):
    arrow(ax, x1, y1, x2, y2, color=ARR, lw=1.5, ms=11)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx = -0.12 if side == "l" else 0.12
    label(ax, mx + dx, my + 0.04, txt, fs=11, c=TEXT2, ha="right" if side == "l" else "left")


fig, ax = new(8.4, 4.05)

# ── ① tree ────────────────────────────────────────────────────────────────
label(ax, 0.0, 3.85, "① 트리 구조", fs=12, w="semibold", ha="left")
rx, ry = 2.15, 3.15            # root
ix, iy = 3.05, 1.85            # internal
qnode(ax, rx, ry, "CRP > 10 ?")
qnode(ax, ix, iy, "나이 > 60 ?")
leaf(ax, 1.05, 1.85, "No", "A")
leaf(ax, 2.35, 0.55, "No", "B")
leaf(ax, 3.75, 0.55, "Yes", "C")
edge(ax, rx - 0.35, ry - 0.25, 1.05 + 0.2, 1.85 + 0.23, "아니오", "l")
edge(ax, rx + 0.35, ry - 0.25, ix - 0.2, iy + 0.25, "예", "r")
edge(ax, ix - 0.3, iy - 0.25, 2.35 + 0.15, 0.55 + 0.23, "아니오", "l")
edge(ax, ix + 0.3, iy - 0.25, 3.75 - 0.15, 0.55 + 0.23, "예", "r")
# role tags
label(ax, rx + 0.88, ry, "root node", fs=11, c=TEXT2, ha="left")
label(ax, ix + 0.88, iy, "internal node", fs=11, c=TEXT2, ha="left")
label(ax, 1.05, 1.85 - 0.42, "leaf", fs=11, c=TEXT2)
label(ax, 2.35, 0.55 - 0.42, "leaf", fs=11, c=TEXT2)
label(ax, 3.75, 0.55 - 0.42, "leaf", fs=11, c=TEXT2)

# divider
ax.plot([4.95, 4.95], [0.1, 3.9], color=LINE, lw=1, zorder=1)

# ── ② feature space ───────────────────────────────────────────────────────
label(ax, 5.25, 3.85, "② feature 공간", fs=12, w="semibold", ha="left")
X0, X1, Y0, Y1 = 5.75, 8.0, 0.55, 3.4
xs = X0 + (X1 - X0) / 3          # CRP = 10   (axis 0..30)
ys = Y0 + (Y1 - Y0) / 2          # 나이 = 60  (axis 30..90)
regions = [((X0, Y0, xs - X0, Y1 - Y0), NO, "No", "A"),
           ((xs, Y0, X1 - xs, ys - Y0), NO, "No", "B"),
           ((xs, ys, X1 - xs, Y1 - ys), YES, "Yes", "C")]
for (x, y, w, h), c, cls, t in regions:
    ax.add_patch(mp.Rectangle((x, y), w, h, fc=mix(c, 0.22), ec="none", zorder=1))
    label(ax, x + w / 2, y + h / 2, cls, fs=13, w="bold", c=c)
    tagc(ax, x + 0.2, y + h - 0.2, t)
# split lines
ax.plot([xs, xs], [Y0, Y1], color=PRIMARY, lw=2, zorder=3)
ax.plot([xs, X1], [ys, ys], color=PRIMARY, lw=2, zorder=3)
# axes
arrow(ax, X0, Y0, X1 + 0.15, Y0, color=TEXT2, lw=1.2, ms=10)
arrow(ax, X0, Y0, X0, Y1 + 0.15, color=TEXT2, lw=1.2, ms=10)
label(ax, xs, Y0 - 0.2, "10", fs=11, c=TEXT2)
label(ax, X0 - 0.1, ys, "60", fs=11, c=TEXT2, ha="right")
label(ax, X1 + 0.15, Y0 - 0.2, "CRP", fs=12, ha="right")
label(ax, X0 - 0.1, Y1 + 0.1, "나이", fs=12, ha="right")

save(fig, os.path.join(OUT, "tree_partition.png"))
