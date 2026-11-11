# W9 §1.5 학습기 생성 방식: Bagging(부트스트랩 표본 → 학습기 병렬 생성 → 평균/다수결) vs Boosting(틀린 샘플 weight ↑ → 순차 생성 → 가중 투표)
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medfig import *
import matplotlib.patches as mp

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "img", "w9")

GREY = "#9AA1AB"
DOT = "#B4BAC3"
BAG = CAT[0]
BOOST = ramp(3)
BIG = "#4B5563"             # 키운 점 = weight가 커진 샘플


def dots(ax, x, y, sizes, colors=None, gap=0.24):
    """Row of sample dots starting at x; radius encodes sample weight."""
    for i, s in enumerate(sizes):
        c = colors[i] if colors else DOT
        ax.add_patch(mp.Circle((x + i * gap, y), s, fc=c, ec="none", zorder=4))


fig, ax = new(8.4, 7.0)
U = 0.6                       # vertical offset of panel ①

# ── ① Bagging (병렬) ──────────────────────────────────────────────────────
top = 6.3 + U
label(ax, 0.05, top, "① Bagging — 병렬", fs=12.5, w="semibold", ha="left")

# training data
dx, dy, dw, dh = 0.05, 4.05 + U, 1.55, 0.9
box(ax, dx, dy, dw, dh, fc=FAINT, ec=LINE, r=0.08, z=1)
label(ax, dx + dw / 2, dy + dh - 0.25, "training data", fs=11, w="semibold")
dots(ax, dx + 0.2, dy + 0.3, [0.07] * 6)
label(ax, dx + dw / 2, dy - 0.2, "N개", fs=11, c=TEXT2)

# bootstrap samples (복원추출: 겹친 점 = 두 번 뽑힘, 빈 점 = 안 뽑힘) & learners
rows = [5.05 + U, 4.35 + U, 3.35 + U]
names = ["1", "2", "B"]
patterns = [[1, 2, 0, 1, 1, 1], [2, 0, 1, 1, 0, 2], [0, 1, 1, 2, 1, 1]]
sx, sw, sh = 2.35, 1.75, 0.5
lx, lw_ = 4.75, 1.3
label(ax, sx + sw / 2, 5.62 + U, "부트스트랩 표본", fs=11, w="semibold")
label(ax, lx + lw_ / 2, 5.62 + U, "깊은 트리", fs=11, w="semibold")
for y, nm, pat in zip(rows, names, patterns):
    arrow(ax, dx + dw + 0.06, dy + dh / 2, sx - 0.08, y, color=GREY, lw=1.3, ms=10)
    box(ax, sx, y - sh / 2, sw, sh, fc="white", ec=LINE, r=0.06)
    for i, p in enumerate(pat):
        xx = sx + 0.18 + i * 0.24
        if p == 0:
            ax.add_patch(mp.Circle((xx, y), 0.065, fc="white", ec=DOT, lw=1.1, ls=(0, (2, 1.5)), zorder=4))
        else:
            ax.add_patch(mp.Circle((xx, y), 0.07, fc=DOT, ec="none", zorder=4))
            if p == 2:
                ax.add_patch(mp.Circle((xx + 0.05, y + 0.07), 0.07, fc=DOT, ec="white", lw=1, zorder=5))
    label(ax, sx + sw - 0.12, y, nm, fs=11, c=TEXT2, ha="right")
    arrow(ax, sx + sw + 0.06, y, lx - 0.08, y, color=GREY, lw=1.3, ms=10)
    box(ax, lx, y - sh / 2, lw_, sh, fc=BAG, ec="none", r=0.06)
    label(ax, lx + lw_ / 2, y, f"학습기 {nm}", fs=11, w="semibold", c=on(BAG))
for x in (sx + sw / 2, lx + lw_ / 2):
    label(ax, x, 3.85 + U, "⋮", fs=14, c=TEXT2)
label(ax, sx + sw / 2, 2.9 + U, "복원추출로 N개씩", fs=11, c=TEXT2)

# combine
cx = 7.3
cy = 4.35 + U
for y in rows:
    arrow(ax, lx + lw_ + 0.06, y, cx - 0.5, cy, color=GREY, lw=1.3, ms=10)
box(ax, cx - 0.45, cy - 0.42, 1.5, 0.84, fc=mix(BAG, 0.14), ec="none", r=0.08)
label(ax, cx + 0.3, cy + 0.15, "평균 (회귀)", fs=11, w="semibold", c=BAG)
label(ax, cx + 0.3, cy - 0.15, "다수결 (분류)", fs=11, w="semibold", c=BAG)
label(ax, cx + 0.3, cy - 0.73, "Variance ↓", fs=12, w="bold", c=TEXT)

ax.plot([0.05, 8.35], [3.05, 3.05], color=LINE, lw=1, zorder=1)

# ── ② Boosting (순차) ─────────────────────────────────────────────────────
top2 = 2.75
label(ax, 0.05, top2, "② Boosting — 순차", fs=12.5, w="semibold", ha="left")

yd, yl = 1.45, 0.65           # sample-weight row, learner row
cols = [0.8, 3.15, 5.5]
bw = 1.5
wrong = [None, {1, 4}, {2}]    # 앞 학습기가 틀린 샘플 (설명용)
heads = ["같은 weight로 시작", "$h_1$이 틀린 샘플 weight ↑", "$h_{M-1}$이 틀린 샘플 weight ↑"]
lnames = ["$h_1$", "$h_2$", "$h_M$"]
for k, x in enumerate(cols):
    box(ax, x - bw / 2, yd - 0.25, bw, 0.5, fc="white", ec=LINE, r=0.06)
    if wrong[k] is None:
        dots(ax, x - 0.6, yd, [0.07] * 6)
    else:
        dots(ax, x - 0.6, yd, [0.11 if i in wrong[k] else 0.05 for i in range(6)],
             [BIG if i in wrong[k] else DOT for i in range(6)])
    label(ax, x, yd + 0.45, heads[k], fs=11, c=TEXT if k else TEXT2, w="semibold" if k else "regular")
    arrow(ax, x, yd - 0.3, x, yl + 0.25, color=GREY, lw=1.3, ms=10)
    box(ax, x - 0.55, yl - 0.21, 1.1, 0.42, fc=BOOST[k], ec="none", r=0.06)
    label(ax, x, yl, lnames[k], fs=13, c=on(BOOST[k]))
# learner k → reweighted samples for k+1 (the second link stands for many steps)
for k in range(2):
    x0, x1 = cols[k] + 0.6, cols[k + 1] - bw / 2 - 0.08
    arrow(ax, x0, yl + 0.08, x1, yd - 0.05, color=GREY, lw=1.3, ms=10, ls="-" if k == 0 else (0, (3, 2)))

# combine: weighted vote of ALL learners
cx2, cy2 = 7.3, 0.95
box(ax, cx2 - 0.45, cy2 - 0.42, 1.5, 0.84, fc=mix(BOOST[1], 0.14), ec="none", r=0.08)
label(ax, cx2 + 0.3, cy2 + 0.15, "가중 투표", fs=11, w="semibold", c=BOOST[1])
label(ax, cx2 + 0.3, cy2 - 0.16, r"$\Sigma\, \alpha_m h_m$", fs=12, c=BOOST[1])
yb = yl - 0.45
for x in cols:
    ax.plot([x, x], [yl - 0.21, yb], color=GREY, lw=1.3, zorder=2)
ax.plot([cols[0], cx2 + 0.3], [yb, yb], color=GREY, lw=1.3, zorder=2)
arrow(ax, cx2 + 0.3, yb, cx2 + 0.3, cy2 - 0.46, color=GREY, lw=1.3, ms=10)
label(ax, cx2 + 0.3, cy2 + 0.72, "Bias ↓", fs=12, w="bold", c=TEXT)

save(fig, os.path.join(OUT, "bagging_boosting.png"))
